from __future__ import annotations
from abc import ABC, abstractmethod
import re
from openai import AzureOpenAI
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
import config


class BaseAgent(ABC):

    def __init__(self, name: str, instructions: str):
        self.name         = name
        self.instructions = instructions
        self._client      = self._build_client()

    def _build_client(self) -> AzureOpenAI:
        if config.AZURE_API_KEY:
            # API key auth — works locally and on any host (Render, etc.)
            base_endpoint = config.FOUNDRY_PROJECT_ENDPOINT.split('/api/projects/')[0]
            return AzureOpenAI(
                api_key=config.AZURE_API_KEY,
                azure_endpoint=base_endpoint,
                api_version="2024-12-01-preview",
            )
        else:
            # Fallback — requires az login locally or Managed Identity on Azure
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
        # Strip <think> blocks from Phi reasoning models
        content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL)
        return content.strip()

    @abstractmethod
    def run(self, input_data: dict) -> dict:
        ...
