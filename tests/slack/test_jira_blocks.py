"""Tests for Jira Block Kit components."""

from __future__ import annotations

import pytest

from slack_bot.blocks.jira import (
    jira_confirmation_blocks,
    jira_error_block,
    jira_insufficient_data_block,
    jira_progress_block,
    send_to_jira_button,
)
from slack_bot.jira.client import CreatedIssue, ExportResult


class TestSendToJiraButton:
    def test_is_actions_block(self):
        block = send_to_jira_button("C123", "ts456")
        assert block["type"] == "actions"

    def test_value_encodes_channel_and_thread(self):
        block = send_to_jira_button("C123", "ts456")
        value = block["elements"][0]["value"]
        assert value == "C123|ts456"

    def test_action_id_is_jira_export(self):
        block = send_to_jira_button("C1", "ts1")
        assert block["elements"][0]["action_id"] == "jira_export"


class TestProgressBlock:
    def test_returns_list(self):
        blocks = jira_progress_block("Working…")
        assert isinstance(blocks, list)
        assert len(blocks) == 1

    def test_contains_message(self):
        blocks = jira_progress_block("Extracting data")
        assert "Extracting data" in blocks[0]["text"]["text"]


class TestConfirmationBlocks:
    def _result_with_epic_and_stories(self):
        result = ExportResult(
            epic=CreatedIssue("PROD-1", "https://co.atlassian.net/browse/PROD-1", "Login Feature")
        )
        result.stories = [
            CreatedIssue("PROD-2", "https://co.atlassian.net/browse/PROD-2", "User logs in"),
            CreatedIssue("PROD-3", "https://co.atlassian.net/browse/PROD-3", "Session expires"),
        ]
        return result

    def test_contains_epic_key(self):
        result = self._result_with_epic_and_stories()
        blocks = jira_confirmation_blocks("Login Feature", result)
        all_text = " ".join(
            b.get("text", {}).get("text", "") for b in blocks
        )
        assert "PROD-1" in all_text

    def test_contains_all_story_keys(self):
        result = self._result_with_epic_and_stories()
        blocks = jira_confirmation_blocks("Login Feature", result)
        all_text = " ".join(
            b.get("text", {}).get("text", "") for b in blocks
        )
        assert "PROD-2" in all_text
        assert "PROD-3" in all_text

    def test_issue_count_in_context(self):
        result = self._result_with_epic_and_stories()
        blocks = jira_confirmation_blocks("Login Feature", result)
        context = next(b for b in blocks if b["type"] == "context")
        assert "3" in context["elements"][0]["text"]

    def test_epic_only_result(self):
        result = ExportResult(
            epic=CreatedIssue("PROD-10", "https://x/PROD-10", "Feature")
        )
        blocks = jira_confirmation_blocks("Feature", result)
        all_text = " ".join(b.get("text", {}).get("text", "") for b in blocks)
        assert "PROD-10" in all_text


class TestRendererJiraButton:
    def test_prd_intent_gets_jira_button(self):
        from slack_bot.blocks.renderer import render_response
        from slack_bot.workflows.router import Intent
        blocks = render_response("Here are your requirements.", intent=Intent.PRD, channel="C1", thread_ts="ts1")
        action_blocks = [b for b in blocks if b.get("type") == "actions"]
        assert len(action_blocks) == 1
        assert action_blocks[0]["elements"][0]["action_id"] == "jira_export"

    def test_no_button_without_channel(self):
        from slack_bot.blocks.renderer import render_response
        from slack_bot.workflows.router import Intent
        blocks = render_response("Here are your requirements.", intent=Intent.PRD)
        action_blocks = [b for b in blocks if b.get("type") == "actions"]
        assert len(action_blocks) == 0

    def test_discovery_intent_no_jira_button(self):
        from slack_bot.blocks.renderer import render_response
        from slack_bot.workflows.router import Intent
        blocks = render_response("What data?", intent=Intent.DISCOVERY, channel="C1", thread_ts="ts1")
        action_blocks = [b for b in blocks if b.get("type") == "actions"]
        assert len(action_blocks) == 0
