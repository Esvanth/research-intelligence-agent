"""
app.py — FastAPI backend for Research Intelligence Agent
Multi-Agent Research Intelligence System | Agents League Hackathon 2026
Track: Reasoning Agents | IQ Layer: Foundry IQ
"""

import asyncio
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

import config

# ── App setup ─────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Research Intelligence Agent",
    description="Multi-Agent Research System powered by Microsoft Foundry IQ",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory job store (keeps track of running/completed research jobs)
jobs: dict = {}


# ── Request / Response models ─────────────────────────────────────────────────
class ResearchRequest(BaseModel):
    query: str


class JobStatus(BaseModel):
    job_id: str
    status: str          # "pending" | "running" | "done" | "error"
    query: str
    progress: list[str]  # live step messages
    report: Optional[str] = None
    error: Optional[str] = None
    created_at: str


# ── Background research task ──────────────────────────────────────────────────
async def run_research(job_id: str, query: str):
    """Runs the full multi-agent pipeline in the background."""
    jobs[job_id]["status"] = "running"

    try:
        # Import here to avoid circular issues at startup
        from agents.orchestrator import OrchestratorAgent

        def add_progress(msg: str):
            jobs[job_id]["progress"].append(msg)

        add_progress("🔍 Search Agent: Finding relevant sources...")
        orchestrator = OrchestratorAgent(progress_callback=add_progress)

        # Run the pipeline (blocking — wrap in thread so FastAPI stays async)
        loop = asyncio.get_event_loop()
        report = await loop.run_in_executor(None, orchestrator.run, query)

        # Save report to file
        output_dir = Path("outputs")
        output_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_query = "".join(c if c.isalnum() else "_" for c in query[:40])
        filepath = output_dir / f"report_{safe_query}_{timestamp}.md"
        filepath.write_text(report, encoding="utf-8")

        jobs[job_id]["status"]  = "done"
        jobs[job_id]["report"]  = report
        add_progress("✅ Report ready!")

    except Exception as e:
        jobs[job_id]["status"] = "error"
        jobs[job_id]["error"]  = str(e)


# ── API Routes ────────────────────────────────────────────────────────────────
@app.get("/api/health")
def health():
    return {"status": "ok", "service": "Research Intelligence Agent"}


@app.post("/api/research", response_model=JobStatus)
async def start_research(req: ResearchRequest):
    """Start a new research job. Returns a job_id to poll for status."""
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    job_id = str(uuid.uuid4())
    jobs[job_id] = {
        "job_id":     job_id,
        "status":     "pending",
        "query":      req.query,
        "progress":   [],
        "report":     None,
        "error":      None,
        "created_at": datetime.now().isoformat(),
    }

    # Fire and forget — runs in background
    asyncio.create_task(run_research(job_id, req.query))
    return jobs[job_id]


@app.get("/api/research/{job_id}", response_model=JobStatus)
def get_status(job_id: str):
    """Poll this endpoint to get live progress and final report."""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found.")
    return jobs[job_id]


# ── Serve React frontend ──────────────────────────────────────────────────────
frontend_dist = Path("frontend/dist")
if frontend_dist.exists():
    app.mount("/assets", StaticFiles(directory=str(frontend_dist / "assets")), name="assets")

    @app.get("/{full_path:path}")
    def serve_frontend(full_path: str):
        return FileResponse(str(frontend_dist / "index.html"))


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    try:
        config.validate_config()
    except EnvironmentError as e:
        print(f"[ERROR] {e}")
        exit(1)
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
