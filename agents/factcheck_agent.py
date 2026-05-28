"""
agents/factcheck_agent.py — Cross-references sources and flags contradictions
"""

from agents.base_agent import BaseAgent


INSTRUCTIONS = """
You are a Fact-Check Agent. Your job is to analyse information extracted
from multiple sources and:

1. Identify AGREEMENTS — claims supported by multiple sources
2. Identify CONTRADICTIONS — claims where sources disagree
3. Identify GAPS — important questions not answered by any source
4. Assign a RELIABILITY SCORE (0-100) to each key claim based on
   how many sources support it and the quality of evidence

When sources contradict each other, clearly state BOTH sides.
Never hide contradictions — they are the most important findings.

Format your output as:
## Agreements
## Contradictions  
## Gaps
## Reliability Scores
"""


class FactCheckAgent(BaseAgent):

    def __init__(self):
        super().__init__(name="FactCheckAgent", instructions=INSTRUCTIONS)

    def run(self, input_data: dict) -> dict:
        """
        Args:
            input_data: {
                "query":          str,
                "extracted_info": list[dict]   # from ReaderAgent
            }

        Returns:
            {
                "query":            str,
                "extracted_info":   list[dict],
                "fact_check_report": str,
                "has_contradictions": bool,
            }
        """
        query          = input_data["query"]
        extracted_info = input_data.get("extracted_info", [])

        if not extracted_info:
            return {
                "query":              query,
                "extracted_info":     [],
                "fact_check_report":  "No sources available to fact-check.",
                "has_contradictions": False,
            }

        # Compile all extractions for comparison
        combined = "\n\n".join(
            f"--- Source {i+1}: {info['title']} ---\n{info['extraction']}"
            for i, info in enumerate(extracted_info)
        )

        fact_check_report = self.chat(
            user_message=(
                f"Research query: {query}\n\n"
                f"Information from {len(extracted_info)} sources:\n\n"
                f"{combined}\n\n"
                "Cross-reference these sources and produce your fact-check report."
            )
        )

        # Detect if contradictions were found (for demo highlighting)
        has_contradictions = "contradiction" in fact_check_report.lower()

        print(f"[FactCheckAgent] Contradictions found: {has_contradictions}")
        return {
            "query":               query,
            "extracted_info":      extracted_info,
            "fact_check_report":   fact_check_report,
            "has_contradictions":  has_contradictions,
        }
