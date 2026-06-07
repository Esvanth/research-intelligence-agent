"""
agents/orchestrator.py — Master coordinator with an adaptive reasoning loop
"""

from __future__ import annotations
import re
from typing import Callable, Optional

from agents.search_agent    import SearchAgent
from agents.reader_agent    import ReaderAgent
from agents.factcheck_agent import FactCheckAgent
from agents.synthesis_agent import SynthesisAgent
import config


_NO_GAP_PHRASES = (
    "no gaps", "none identified", "no significant gaps",
    "no major gaps", "none found", "no notable gaps", "no gap",
)


def _extract_section(report: str, heading: str) -> str:
    """Pull the body text under a `## Heading` from a markdown report."""
    match = re.search(
        rf"##\s*{re.escape(heading)}\s*\n(.*?)(?=\n##|\Z)",
        report, re.IGNORECASE | re.DOTALL,
    )
    return match.group(1).strip() if match else ""


def _first_gap_phrase(gaps_text: str) -> str:
    """Reduce a Gaps section to a short phrase usable as a follow-up search query."""
    for line in gaps_text.splitlines():
        cleaned = line.strip(" -*•0123456789.").strip()
        if cleaned:
            return cleaned[:120]
    return ""


def _has_open_gaps(gaps_text: str) -> bool:
    if len(gaps_text) < 20:
        return False
    lowered = gaps_text.lower()
    return not any(phrase in lowered for phrase in _NO_GAP_PHRASES)


class OrchestratorAgent:
    """
    Coordinates a multi-step reasoning pipeline:

        Search → Read → Fact-Check
                            │
                  open gaps? ──yes──▶ targeted follow-up Search → Read, then re-Fact-Check
                            │                                            │
                            no  ◀───────────────────────────────────────┘
                            ▼
                       Synthesise

    Rather than always running the pipeline once, the orchestrator inspects
    the Fact-Check Agent's "Gaps" findings and decides whether another
    research round is worth running — that decision-and-retry step is the
    multi-step reasoning loop, capped by config.MAX_RESEARCH_ROUNDS so the
    agent always converges on a final report.

    progress_callback: optional function(str) called at each step
    so the FastAPI backend can stream progress to the frontend.
    """

    def __init__(self, progress_callback: Optional[Callable[[str], None]] = None):
        self.search_agent    = SearchAgent()
        self.reader_agent    = ReaderAgent()
        self.factcheck_agent = FactCheckAgent()
        self.synthesis_agent = SynthesisAgent()
        self._progress       = progress_callback or (lambda msg: print(msg))

    def _search_and_read(self, query: str) -> dict:
        self._progress(f"🔍 Search Agent: Searching for '{query}'...")
        search_output = self.search_agent.run({"query": query})
        self._progress(f"✅ Search Agent: Found {len(search_output['results'])} sources")

        self._progress("📖 Reader Agent: Reading and extracting content...")
        reader_output = self.reader_agent.run(search_output)
        self._progress(f"✅ Reader Agent: Extracted from {len(reader_output['extracted_info'])} sources")
        return reader_output

    def run(self, query: str) -> str:
        """
        Execute the multi-agent, multi-step research pipeline.

        Returns:
            The final structured research report as a string.
        """
        reader_output  = self._search_and_read(query)
        extracted_info = list(reader_output["extracted_info"])
        seen_urls      = {info["url"] for info in extracted_info}

        for round_num in range(1, config.MAX_RESEARCH_ROUNDS + 1):
            self._progress("🔎 Fact-Check Agent: Cross-referencing sources...")
            factcheck_output = self.factcheck_agent.run({"query": query, "extracted_info": extracted_info})
            note = " ⚠️ Contradictions detected!" if factcheck_output["has_contradictions"] else ""
            self._progress(f"✅ Fact-Check Agent: Done{note}")

            if round_num == config.MAX_RESEARCH_ROUNDS:
                break

            gaps_text = _extract_section(factcheck_output["fact_check_report"], "Gaps")
            if not _has_open_gaps(gaps_text):
                break

            follow_up       = _first_gap_phrase(gaps_text)
            follow_up_query = f"{query} {follow_up}".strip() if follow_up else query
            self._progress(f"🧭 Reasoning Loop: Open question detected — digging deeper on \"{follow_up or query}\"...")

            more     = self._search_and_read(follow_up_query)
            new_info = [info for info in more["extracted_info"] if info["url"] not in seen_urls]
            if not new_info:
                self._progress("ℹ️ Reasoning Loop: No new sources found — concluding research with current evidence.")
                break

            seen_urls.update(info["url"] for info in new_info)
            extracted_info.extend(new_info)

        self._progress("📝 Synthesis Agent: Writing your report...")
        synthesis_output = self.synthesis_agent.run(factcheck_output)
        self._progress("✅ Synthesis Agent: Report complete!")

        return synthesis_output["final_report"]
