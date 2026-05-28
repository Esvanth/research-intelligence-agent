from __future__ import annotations
from abc import ABC, abstractmethod
import re
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
import config

class BaseAgent(ABC):

    def __init__(self, name: str, instructions: str):
        self.name         = name
        self.instructions = instructions
        self._client      = self._build_client()

    def _build_client(self):
        if config.AZURE_API_KEY:
            # API key auth for deployed environments (Render, etc.)
            from openai import OpenAI
            base_url = config.FOUNDRY_PROJECT_ENDPOINT.rstrip('/') + '/openai/v1'
            return OpenAI(api_key=config.AZURE_API_KEY, base_url=base_url)
        else:
            # Local dev — requires az login
            project_client = AIProjectClient(
                endpoint=config.FOUNDRY_PROJECT_ENDPOINT,
                credential=DefaultAzureCredential(),
            )
            return project_client.get_openai_client()

    def chat(self, user_message: str, extra_context: str = "") -> str:
        messages = [{"role": "system", "content": self.instructions}]
        if extra_context:
            messages.append({
                "role": "system",
                "content": f"Additional context:\n{extra_context}",
            })
        messages.append({"role": "user", "content": user_message})
        response = self._client.chat.completions.create(
            model=config.MODEL_DEPLOYMENT,
            messages=messages,
            temperature=0.3,
            max_tokens=1500,
        )
        content = response.choices[0].message.content or ""
        # Strip reasoning blocks emitted by thinking models (Phi-4-*-reasoning)
        content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL)
        # If the model wrote "I'll produce..." style deliberation lines, keep only
        # content after the last occurrence of a separator the model tends to use
        for marker in ("Thus,", "Therefore,", "In summary,", "To summarize,"):
            if marker in content:
                content = content[content.rfind(marker):]
                break
        return content.strip()

    @abstractmethod
    def run(self, input_data: dict) -> dict:
        ...