"""Tests for Jira export idempotency and deduplication."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

import slack_bot.handlers.jira_export as export_mod


@pytest.fixture(autouse=True)
def reset_exported():
    """Clear the module-level exported set before each test."""
    export_mod._exported.clear()
    yield
    export_mod._exported.clear()


def _make_client():
    client = MagicMock()
    client.chat_postMessage.return_value = {"ts": "progress.ts"}
    return client


class TestAlreadyExportedGuard:
    def test_second_export_posts_already_exported_message(self):
        export_mod._mark_exported("C1", "ts1")

        client = _make_client()
        export_mod._export(
            channel="C1",
            thread_ts="ts1",
            client=client,
            llm=MagicMock(),
            ctx=MagicMock(),
        )

        client.chat_postMessage.assert_called_once()
        text = client.chat_postMessage.call_args.kwargs["text"]
        assert "already been exported" in text

    def test_first_export_not_blocked(self):
        assert not export_mod._already_exported("C1", "ts1")

    def test_mark_exported_persists(self):
        export_mod._mark_exported("C1", "ts1")
        assert export_mod._already_exported("C1", "ts1")

    def test_different_threads_are_independent(self):
        export_mod._mark_exported("C1", "ts1")
        assert not export_mod._already_exported("C1", "ts2")
        assert not export_mod._already_exported("C2", "ts1")


class TestJiraDisabled:
    def test_posts_config_warning_when_jira_not_enabled(self):
        client = _make_client()
        with patch.object(export_mod, "_JIRA_ENABLED", False):
            export_mod._export(
                channel="C1",
                thread_ts="ts1",
                client=client,
                llm=MagicMock(),
                ctx=MagicMock(),
            )
        client.chat_postMessage.assert_called_once()
        assert "not configured" in client.chat_postMessage.call_args.kwargs["text"]


class TestButtonReplacement:
    def test_button_message_updated_after_successful_export(self):
        from slack_bot.blocks.jira import send_to_jira_button

        button_blocks = [send_to_jira_button("C1", "ts1")]
        client = _make_client()

        mock_prd = MagicMock()
        mock_prd.title = "Login Feature"
        mock_prd.summary = "Users can log in."
        mock_prd.requirements = []
        mock_prd.metrics = []
        mock_prd.stories = []

        with patch.object(export_mod, "_JIRA_ENABLED", True), \
             patch("slack_bot.handlers.jira_export.extract_from_conversation", return_value=mock_prd), \
             patch("slack_bot.handlers.jira_export.build_jira_client") as mock_jira:
            mock_jira.return_value.create_epic.return_value = MagicMock(key="PROD-1", url="https://x/PROD-1", summary="Login Feature")

            ctx = MagicMock()
            ctx.get.return_value = [{"role": "user", "content": "write a PRD"}]

            export_mod._export(
                channel="C1",
                thread_ts="ts1",
                client=client,
                llm=MagicMock(),
                ctx=ctx,
                button_channel="C1",
                button_msg_ts="button.ts",
                button_blocks=button_blocks,
            )

        # chat_update calls: progress → creating → confirmation (ts=progress.ts)
        #                    + button replacement (ts=button.ts)
        update_calls = client.chat_update.call_args_list
        button_update = next(
            (c for c in update_calls if c.kwargs.get("ts") == "button.ts"), None
        )
        assert button_update is not None
        # The updated blocks must not contain the actions block
        updated_blocks = button_update.kwargs["blocks"]
        assert not any(b.get("type") == "actions" for b in updated_blocks)
