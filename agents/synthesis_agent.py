"""
agents/synthesis_agent.py — Produces the final structured research report
"""

from agents.base_agent import BaseAgent


INSTRUCTIONS = """
You are a Research Synthesis Agent. You produce the final, structured
research report by combining all findings from other agents.

Your report must follow this exact format:

# Research Report: [Topic]

## Executive Summary
[2-3 sentence overview of the key answer]

## Key Findings
[Numbered list of the most important findings with confidence scores]
Each finding: "Finding text [Confidence: XX%] — supported by N sources"

## Evidence Trail
[For each key finding, list which sources support it]

## Contradictions & Uncertainties
[Any areas where sources disagree — be transparent]

## Final Verdict
[A direct, honest answer to the research query with an overall confidence score]

## Sources
[Numbered list of all sources used]

---
Be rigorous, honest, and clear. If something is uncertain, say so explicitly.
Your confidence scores must reflect the actual evidence quality.
"""


class SynthesisAgent(BaseAgent):

    def __init__(self):
        super().__init__(name="SynthesisAgent", instructions=INSTRUCTIONS)

    def run(self, input_data: dict) -> dict:
        """
        Args:
            input_data: {
                "query":             str,
                "extracted_info":    list[dict],
                "fact_check_report": str,
                "has_contradictions": bool,
            }

        Returns:
            {
                "query":         str,
                "final_report":  str,
                "sources_count": int,
            }
        """
        query             = input_data["query"]
        extracted_info    = input_data.get("extracted_info", [])
        fact_check_report = input_data.get("fact_check_report", "")

        sources_list = "\n".join(
            f"{i+1}. {info['title']} — {info['url']}"
            for i, info in enumerate(extracted_info)
        )

        extractions_summary = "\n\n".join(
            f"Source {i+1} ({info['title']}):\n{info['extraction']}"
            for i, info in enumerate(extracted_info)
        )

        final_report = self.chat(
            user_message=(
                f"Research query: {query}\n\n"
                f"Extracted information from sources:\n{extractions_summary}\n\n"
                f"Fact-check report:\n{fact_check_report}\n\n"
                f"Sources:\n{sources_list}\n\n"
                "Produce the final structured research report."
            )
        )

        print(f"\n[SynthesisAgent] Final report generated ({len(final_report)} chars)")
        return {
            "query":         query,
            "final_report":  final_report,
            "sources_count": len(extracted_info),
        }
