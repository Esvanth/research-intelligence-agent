"""
agents/search_agent.py — Finds and evaluates relevant sources for a research query
"""

from agents.base_agent import BaseAgent
from tools.web_search import web_search


INSTRUCTIONS = """
You are a Search Specialist Agent. Your job is to:
1. Analyse the research query to understand what information is needed
2. Review the raw search results provided (titles + snippets)
3. Select the most relevant ones and briefly explain WHY each is relevant

Be concise and precise. Output a numbered list of relevant results with reasoning.
"""


class SearchAgent(BaseAgent):

    def __init__(self):
        super().__init__(name="SearchAgent", instructions=INSTRUCTIONS)

    def run(self, input_data: dict) -> dict:
        """
        Args:
            input_data: {"query": str}

        Returns:
            {"query": str, "results": list[dict], "relevance_notes": str}
        """
        query   = input_data["query"]
        results = web_search(query)

        if not results:
            return {
                "query":           query,
                "results":         [],
                "relevance_notes": "No search results found.",
            }

        formatted = "\n".join(
            f"{i+1}. [{r['title']}] {r.get('snippet', '')} (URL: {r['url']})"
            for i, r in enumerate(results)
        )

        relevance_notes = self.chat(
            user_message=(
                f"Research query: {query}\n\n"
                f"Search results:\n{formatted}\n\n"
                "Which of these are most relevant and why?"
            )
        )

        print(f"[SearchAgent] Found {len(results)} results for: '{query}'")
        return {
            "query":           query,
            "results":         results,
            "relevance_notes": relevance_notes,
        }
