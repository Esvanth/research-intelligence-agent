from __future__ import annotations
from abc import ABC, abstractmethod
import re

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

import config


class BaseAgent(ABC):

    def __init__(self, name: str, instructions: str):
        self.name         = name
        self.instructions = instructions
        self._client      = self._build_client()

    def _build_client(self):
        if config.OPENAI_API_KEY:
            from openai import OpenAI
            return _OpenAIAdapter(OpenAI(api_key=config.OPENAI_API_KEY))

        # Azure AI Foundry IQ — primary path
        return ChatCompletionsClient(
            endpoint=config.FOUNDRY_INFERENCE_ENDPOINT,
            credential=AzureKeyCredential(config.AZURE_API_KEY),
        )

    def chat(self, user_message: str, extra_context: str = "") -> str:
        messages = [SystemMessage(content=self.instructions)]
        if extra_context:
            messages.append(SystemMessage(content=f"Additional context:\n{extra_context}"))
        messages.append(UserMessage(content=user_message))

        response = self._client.complete(
            model=config.MODEL_DEPLOYMENT,
            messages=messages,
            temperature=0.3,
            max_tokens=1500,
        )
        content = response.choices[0].message.content or ""
        content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL)
        return content.strip()

    @abstractmethod
    def run(self, input_data: dict) -> dict:
        ...


class _OpenAIAdapter:
    """Wraps openai.OpenAI to expose .complete() matching ChatCompletionsClient."""

    def __init__(self, client):
        self._c = client

    def complete(self, model, messages, temperature=0.3, max_tokens=1500, **_):
        oai_msgs = [{"role": m.role, "content": m.content} for m in messages]
        return self._c.chat.completions.create(
            model=model,
            messages=oai_msgs,
            temperature=temperature,
            max_tokens=max_tokens,
        )
