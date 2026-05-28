"""
agents/reader_agent.py — Reads and extracts key information from sources
"""

from agents.base_agent import BaseAgent
from tools.document_reader import read_url


INSTRUCTIONS = """
You are a Research Reader Agent. You read web page content and extract:
1. Key facts and claims relevant to the research query
2. The author's main argument or conclusion
3. Any data, statistics, or evidence provided
4. Any limitations or caveats mentioned

Be precise and factual. Do NOT add your own opinions.
Format your output clearly with these sections.
"""


class ReaderAgent(BaseAgent):

    def __init__(self):
        super().__init__(name="ReaderAgent", instructions=INSTRUCTIONS)

    def run(self, input_data: dict) -> dict:
        """
        Args:
            input_data: {
                "query":   str,
                "results": list[dict]   # from SearchAgent
            }

        Returns:
            {"query": str, "extracted_info": list[dict]}
        """
        query          = input_data["query"]
        search_results = input_data.get("results", [])
        extracted_info = []

        # Read top 3 sources to stay within time/token budget
        for result in search_results[:3]:
            url  = result["url"]
            page = read_url(url)

            if page["error"] or not page["content"]:
                print(f"[ReaderAgent] Skipping unreadable URL: {url}")
                continue

            extraction = self.chat(
                user_message=(
                    f"Research query: {query}\n\n"
                    f"Source title: {page['title']}\n"
                    f"Source content:\n{page['content']}\n\n"
                    "Extract the key information relevant to the query."
                )
            )

            extracted_info.append({
                "url":        url,
                "title":      page["title"],
                "extraction": extraction,
            })
            print(f"[ReaderAgent] Read: {page['title'][:60]}...")

        return {
            "query":          query,
            "extracted_info": extracted_info,
        }
