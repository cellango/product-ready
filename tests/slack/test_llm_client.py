"""Tests for the model-agnostic LLM client factory and provider selection."""

import os

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
