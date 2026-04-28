"""
Model-agnostic LLM client.

Reads ANTHROPIC_API_KEY or OPENAI_API_KEY from the environment and routes
to the appropriate provider. The caller never needs to know which model is
running underneath.
"""

from __future__ import annotations

import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Iterator

ROOT = Path(__file__).parent.parent.parent


def _read_core() -> str:
    core = (ROOT / "core/product-ready-core.md").read_text()
    guardrails = (ROOT / "core/guardrails.md").read_text()
    return (
        f"{core}\n\n{guardrails}\n\n"
        "# Response Format\n"
        "Be concise. Use plain text with minimal markdown. "
        "Ask questions before generating artifacts. "
        "Do not generate full PRDs or behavior specs unless explicitly asked. "
        "When flagging a Missing Product Decision, prefix the line with [MPD]."
    )


SYSTEM_PROMPT: str = _read_core()

Message = dict[str, str]  # {"role": "user"|"assistant", "content": str}


class LLMClient(ABC):
    @abstractmethod
    def complete(self, messages: list[Message]) -> str:
        """Return the assistant reply for the given conversation history."""

    @abstractmethod
    def stream(self, messages: list[Message]) -> Iterator[str]:
        """Yield text chunks as they arrive (for streaming responses)."""

    @property
    @abstractmethod
    def provider(self) -> str:
        """Human-readable provider name."""


class AnthropicClient(LLMClient):
    MODEL = "claude-sonnet-4-6"

    def __init__(self, api_key: str) -> None:
        try:
            import anthropic
        except ImportError:
            raise RuntimeError("anthropic package not installed. Run: pip install anthropic")
        self._client = anthropic.Anthropic(api_key=api_key)

    @property
    def provider(self) -> str:
        return "anthropic"

    def complete(self, messages: list[Message]) -> str:
        response = self._client.messages.create(
            model=self.MODEL,
            max_tokens=2048,
            system=SYSTEM_PROMPT,
            messages=messages,
        )
        return response.content[0].text

    def stream(self, messages: list[Message]) -> Iterator[str]:
        with self._client.messages.stream(
            model=self.MODEL,
            max_tokens=2048,
            system=SYSTEM_PROMPT,
            messages=messages,
        ) as stream:
            yield from stream.text_stream


class OpenAIClient(LLMClient):
    MODEL = "gpt-4o"

    def __init__(self, api_key: str) -> None:
        try:
            import openai
        except ImportError:
            raise RuntimeError("openai package not installed. Run: pip install openai")
        self._client = openai.OpenAI(api_key=api_key)

    @property
    def provider(self) -> str:
        return "openai"

    def complete(self, messages: list[Message]) -> str:
        payload = [{"role": "system", "content": SYSTEM_PROMPT}] + messages
        response = self._client.chat.completions.create(
            model=self.MODEL,
            messages=payload,
            max_tokens=2048,
        )
        return response.choices[0].message.content

    def stream(self, messages: list[Message]) -> Iterator[str]:
        payload = [{"role": "system", "content": SYSTEM_PROMPT}] + messages
        for chunk in self._client.chat.completions.create(
            model=self.MODEL,
            messages=payload,
            max_tokens=2048,
            stream=True,
        ):
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta


def build_client() -> LLMClient:
    """Instantiate the right client based on available environment variables."""
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")

    if anthropic_key:
        return AnthropicClient(anthropic_key)
    if openai_key:
        return OpenAIClient(openai_key)

    raise RuntimeError(
        "No LLM API key found. Set ANTHROPIC_API_KEY or OPENAI_API_KEY."
    )
