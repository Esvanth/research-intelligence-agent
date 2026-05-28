"""
agents/orchestrator.py — Master coordinator (updated with progress_callback for web)
"""

from __future__ import annotations
from typing import Callable, Optional

from agents.search_agent    import SearchAgent
from agents.reader_agent    import ReaderAgent
from agents.factcheck_agent import FactCheckAgent
from agents.synthesis_agent import SynthesisAgent


class OrchestratorAgent:
    """
    Coordinates all agents in sequence:
    Search → Read → Fact-Check → Synthesise

    progress_callback: optional function(str) called at each step
    so the FastAPI backend can stream progress to the frontend.
    """

    def __init__(self, progress_callback: Optional[Callable[[str], None]] = None):
        self.search_agent    = SearchAgent()
        self.reader_agent    = ReaderAgent()
        self.factcheck_agent = FactCheckAgent()
        self.synthesis_agent = SynthesisAgent()
        self._progress       = progress_callback or (lambda msg: print(msg))

    def run(self, query: str) -> str:
        """
        Execute the full multi-agent research pipeline.

        Args:
            query: The research question from the user.

        Returns:
            The final structured research report as a string.
        """
        self._progress(f"🔍 Search Agent: Searching for '{query}'...")
        search_output = self.search_agent.run({"query": query})
        self._progress(f"✅ Search Agent: Found {len(search_output['results'])} sources")

        self._progress("📖 Reader Agent: Reading and extracting content...")
        reader_output = self.reader_agent.run(search_output)
        self._progress(f"✅ Reader Agent: Extracted from {len(reader_output['extracted_info'])} sources")

        self._progress("🔎 Fact-Check Agent: Cross-referencing sources...")
        factcheck_output = self.factcheck_agent.run(reader_output)
        note = " ⚠️ Contradictions detected!" if factcheck_output["has_contradictions"] else ""
        self._progress(f"✅ Fact-Check Agent: Done{note}")

        self._progress("📝 Synthesis Agent: Writing your report...")
        synthesis_output = self.synthesis_agent.run(factcheck_output)
        self._progress("✅ All agents complete — report ready!")

        return synthesis_output["final_report"]
