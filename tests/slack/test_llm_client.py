"""Tests for the model-agnostic LLM client factory and provider selection."""

import os
from unittest.mock import MagicMock, patch

import pytest

from slack_bot.llm.client import AnthropicClient, OpenAIClient, build_client


class TestBuildClient:
    def test_prefers_anthropic_when_both_set(self, monkeypatch):
        monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-test")
        monkeypatch.setenv("OPENAI_API_KEY", "sk-openai-test")
        # We can't fully instantiate without the real SDK, so just check routing
        # by mocking the constructors
        import slack_bot.llm.client as mod
        calls = []

        class FakeAnthropic:
            def __init__(self, api_key):
                calls.append(("anthropic", api_key))

        monkeypatch.setattr("anthropic.Anthropic", FakeAnthropic)
        client = build_client()
        assert isinstance(client, AnthropicClient)
        assert client.provider == "anthropic"

    def test_falls_back_to_openai(self, monkeypatch):
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        monkeypatch.setenv("OPENAI_API_KEY", "sk-openai-test")

        import openai as openai_mod
        import slack_bot.llm.client as mod

        class FakeOpenAI:
            def __init__(self, api_key):
                pass

        monkeypatch.setattr(openai_mod, "OpenAI", FakeOpenAI)
        client = build_client()
        assert isinstance(client, OpenAIClient)
        assert client.provider == "openai"

    def test_raises_when_no_key(self, monkeypatch):
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        with pytest.raises(RuntimeError, match="No LLM API key"):
            build_client()


class TestAnthropicClientComplete:
    def _make_client(self, monkeypatch):
        import anthropic as anthropic_mod
        fake_sdk = MagicMock()
        monkeypatch.setattr(anthropic_mod, "Anthropic", lambda api_key: fake_sdk)
        return AnthropicClient("sk-test"), fake_sdk

    def test_empty_content_raises(self, monkeypatch):
        client, sdk = self._make_client(monkeypatch)
        response = MagicMock()
        response.content = []
        response.stop_reason = "max_tokens"
        sdk.messages.create.return_value = response
        with pytest.raises(RuntimeError, match="empty content"):
            client.complete([{"role": "user", "content": "hello"}])

    def test_returns_text_on_success(self, monkeypatch):
        client, sdk = self._make_client(monkeypatch)
        block = MagicMock()
        block.text = "Here is your PRD."
        sdk.messages.create.return_value = MagicMock(content=[block])
        result = client.complete([{"role": "user", "content": "hello"}])
        assert result == "Here is your PRD."


class TestOpenAIClientComplete:
    def _make_client(self, monkeypatch):
        import openai as openai_mod
        fake_sdk = MagicMock()
        monkeypatch.setattr(openai_mod, "OpenAI", lambda api_key: fake_sdk)
        return OpenAIClient("sk-test"), fake_sdk

    def test_null_content_raises(self, monkeypatch):
        client, sdk = self._make_client(monkeypatch)
        choice = MagicMock()
        choice.message.content = None
        choice.finish_reason = "content_filter"
        sdk.chat.completions.create.return_value = MagicMock(choices=[choice])
        with pytest.raises(RuntimeError, match="null content"):
            client.complete([{"role": "user", "content": "hello"}])

    def test_returns_content_on_success(self, monkeypatch):
        client, sdk = self._make_client(monkeypatch)
        choice = MagicMock()
        choice.message.content = "Here is your PRD."
        sdk.chat.completions.create.return_value = MagicMock(choices=[choice])
        result = client.complete([{"role": "user", "content": "hello"}])
        assert result == "Here is your PRD."


class TestSystemPromptLoaded:
    def test_system_prompt_contains_core_workflow(self):
        from slack_bot.llm.client import SYSTEM_PROMPT
        assert "Product Ready" in SYSTEM_PROMPT
        assert "Testability" in SYSTEM_PROMPT or "testable" in SYSTEM_PROMPT

    def test_system_prompt_contains_guardrails(self):
        from slack_bot.llm.client import SYSTEM_PROMPT
        assert "No Missing Decisions" in SYSTEM_PROMPT
        assert "Metric Integrity" in SYSTEM_PROMPT

    def test_system_prompt_contains_mpd_instruction(self):
        from slack_bot.llm.client import SYSTEM_PROMPT
        assert "[MPD]" in SYSTEM_PROMPT
