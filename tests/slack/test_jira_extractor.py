"""Tests for the Jira extractor (LLM-based structured data extraction)."""

from __future__ import annotations

import json

import pytest

from slack_bot.jira.extractor import ExtractedPRD, extract_from_conversation


class _FakeLLM:
    def __init__(self, response: str):
        self._response = response

    def complete(self, messages):
        return self._response


class TestExtractFromConversation:
    def test_returns_none_for_empty_history(self):
        llm = _FakeLLM("{}")
        result = extract_from_conversation([], llm)
        assert result is None

    def test_returns_none_on_insufficient_data(self):
        payload = json.dumps({"error": "insufficient_data", "message": "No PRD found."})
        llm = _FakeLLM(payload)
        result = extract_from_conversation([{"role": "user", "content": "hello"}], llm)
        assert result is None

    def test_returns_none_on_invalid_json(self):
        llm = _FakeLLM("not json at all")
        result = extract_from_conversation([{"role": "user", "content": "x"}], llm)
        assert result is None

    def test_parses_valid_prd_response(self):
        payload = json.dumps({
            "title": "User Login",
            "summary": "Allow users to log in securely.",
            "requirements": ["REQ-001: Email/password login", "REQ-002: Session expiry"],
            "stories": [
                {
                    "title": "User logs in with email",
                    "description": "Standard login flow",
                    "acceptance_criteria": "Given valid credentials, user reaches dashboard",
                }
            ],
            "metrics": ["Login success rate > 95%"],
        })
        llm = _FakeLLM(payload)
        result = extract_from_conversation([{"role": "user", "content": "write a PRD"}], llm)
        assert result is not None
        assert result.title == "User Login"
        assert len(result.requirements) == 2
        assert len(result.stories) == 1
        assert result.has_stories is True

    def test_strips_markdown_code_fences(self):
        payload = "```json\n" + json.dumps({
            "title": "Feature",
            "summary": "A feature.",
            "requirements": [],
            "stories": [],
            "metrics": [],
        }) + "\n```"
        llm = _FakeLLM(payload)
        result = extract_from_conversation([{"role": "user", "content": "x"}], llm)
        assert result is not None
        assert result.title == "Feature"

    def test_empty_lists_are_valid(self):
        payload = json.dumps({
            "title": "Simple feature",
            "summary": "Does something.",
            "requirements": [],
            "stories": [],
            "metrics": [],
        })
        llm = _FakeLLM(payload)
        result = extract_from_conversation([{"role": "user", "content": "x"}], llm)
        assert result is not None
        assert result.has_stories is False

    def test_returns_none_on_llm_exception(self):
        class _FailLLM:
            def complete(self, _):
                raise RuntimeError("API down")

        result = extract_from_conversation([{"role": "user", "content": "x"}], _FailLLM())
        assert result is None


class TestExtractedPRD:
    def test_has_stories_false_when_empty(self):
        prd = ExtractedPRD(title="T", summary="S")
        assert prd.has_stories is False

    def test_has_stories_true_when_populated(self):
        prd = ExtractedPRD(title="T", summary="S", stories=[{"title": "s1"}])
        assert prd.has_stories is True
