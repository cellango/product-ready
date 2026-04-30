"""
Jira export handler.

Entry point:
  block_actions jira_export — "Send to Jira" button on PRD/spec responses.

Flow:
  1. Deduplicate: if this thread was already exported, tell the user and stop.
  2. Retrieve thread conversation history.
  3. Call the LLM extractor to get structured PRD/story data.
  4. Create Epic + Stories in Jira.
  5. Post a confirmation block with links to created issues.
  6. Replace the original button with a static "✓ Sent to Jira" indicator.
"""

from __future__ import annotations

import logging
import os
from threading import Lock

from slack_bot.blocks.jira import (
    jira_confirmation_blocks,
    jira_error_block,
    jira_insufficient_data_block,
    jira_progress_block,
    replace_jira_button_with_sent,
)
from slack_bot.context.thread import ThreadContext
from slack_bot.jira.client import ExportResult, JiraClient, JiraError, build_jira_client
from slack_bot.jira.extractor import extract_from_conversation
from slack_bot.llm.client import LLMClient
from slack_bot.rate_limiter import RateLimiter

logger = logging.getLogger(__name__)

_JIRA_ENABLED = all(
    os.getenv(k) for k in ("JIRA_BASE_URL", "JIRA_EMAIL", "JIRA_API_TOKEN", "JIRA_PROJECT_KEY")
)

# (channel, thread_ts) pairs that have already been exported this session.
_exported: set[tuple[str, str]] = set()
_exported_lock = Lock()


def _mark_exported(channel: str, thread_ts: str) -> None:
    with _exported_lock:
        _exported.add((channel, thread_ts))


def _already_exported(channel: str, thread_ts: str) -> bool:
    with _exported_lock:
        return (channel, thread_ts) in _exported


def _export(
    *,
    channel: str,
    thread_ts: str,
    client,
    llm: LLMClient,
    ctx: ThreadContext,
    button_channel: str = "",
    button_msg_ts: str = "",
    button_blocks: list[dict] | None = None,
) -> None:
    """Core export logic — called by the button action handler."""

    if _already_exported(channel, thread_ts):
        client.chat_postMessage(
            channel=channel,
            thread_ts=thread_ts,
            text=":information_source: This thread has already been exported to Jira.",
        )
        return

    if not _JIRA_ENABLED:
        client.chat_postMessage(
            channel=channel,
            thread_ts=thread_ts,
            text=(
                ":warning: Jira is not configured. "
                "Set `JIRA_BASE_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN`, and `JIRA_PROJECT_KEY` "
                "in the bot environment."
            ),
        )
        return

    progress_msg = client.chat_postMessage(
        channel=channel,
        thread_ts=thread_ts,
        text=":hourglass_flowing_sand: Extracting product data…",
        blocks=jira_progress_block("Extracting product data from conversation…"),
    )
    progress_ts = progress_msg["ts"]

    history = ctx.get(channel, thread_ts)
    if not history:
        client.chat_update(
            channel=channel,
            ts=progress_ts,
            text="Nothing to export yet.",
            blocks=jira_insufficient_data_block(
                "This thread has no product-ready conversation yet. Run a workflow first."
            ),
        )
        return

    prd = extract_from_conversation(history, llm)
    if prd is None:
        client.chat_update(
            channel=channel,
            ts=progress_ts,
            text="Not enough product data to export.",
            blocks=jira_insufficient_data_block(
                "The conversation doesn't have a complete PRD or story list yet. "
                "Try `/prd` or `/product-ready` to generate one first."
            ),
        )
        return

    client.chat_update(
        channel=channel,
        ts=progress_ts,
        text=":hourglass_flowing_sand: Creating Jira issues…",
        blocks=jira_progress_block(f"Creating Jira issues for *{prd.title}*…"),
    )

    try:
        jira = build_jira_client()
        result = _create_issues(jira, prd)
    except JiraError as exc:
        logger.exception("Jira API error during export: %s", exc)
        client.chat_update(
            channel=channel,
            ts=progress_ts,
            text="Jira export failed.",
            blocks=jira_error_block(
                f"Jira returned an error ({exc.status}). Check bot logs for details."
            ),
        )
        return
    except Exception as exc:
        logger.exception("Unexpected error during Jira export: %s", exc)
        client.chat_update(
            channel=channel,
            ts=progress_ts,
            text="Jira export failed.",
            blocks=jira_error_block("An unexpected error occurred. Check bot logs."),
        )
        return

    _mark_exported(channel, thread_ts)

    client.chat_update(
        channel=channel,
        ts=progress_ts,
        text=f"Exported to Jira: {prd.title}",
        blocks=jira_confirmation_blocks(prd.title, result),
    )

    # Replace the "Send to Jira" button in the original LLM message with a
    # static "✓ Sent to Jira" indicator so it cannot be clicked again.
    if button_channel and button_msg_ts and button_blocks:
        try:
            client.chat_update(
                channel=button_channel,
                ts=button_msg_ts,
                blocks=replace_jira_button_with_sent(button_blocks),
                text="",
            )
        except Exception as exc:
            logger.warning("Could not update button message after export: %s", exc)


def _create_issues(jira: JiraClient, prd) -> ExportResult:
    result = ExportResult()

    epic = jira.create_epic(
        summary=prd.title,
        description=prd.summary + (
            "\n\nRequirements:\n" + "\n".join(prd.requirements)
            if prd.requirements else ""
        ),
        metrics=prd.metrics,
    )
    result.epic = epic

    for story_data in prd.stories:
        story = jira.create_story(
            summary=story_data.get("title", "Untitled Story"),
            description=story_data.get("description", ""),
            acceptance_criteria=story_data.get("acceptance_criteria", ""),
            epic_key=epic.key,
        )
        result.stories.append(story)

    return result


def register(app, llm: LLMClient, ctx: ThreadContext, rl: RateLimiter) -> None:
    """Register the Jira export button action handler."""

    @app.action("jira_export")
    def on_jira_button(ack, body, client):
        ack()

        user = body.get("user", {}).get("id", "")
        if user and not rl.is_allowed(user):
            channel = body.get("channel", {}).get("id", "")
            client.chat_postMessage(
                channel=channel,
                text=":no_entry: You're sending requests too quickly. Please wait a moment.",
            )
            return

        value = body["actions"][0].get("value", "")
        parts = value.split("|", 1)
        if len(parts) != 2:
            return
        channel, thread_ts = parts

        # Capture the button's own message so we can disable it after export.
        button_channel = body.get("channel", {}).get("id", "")
        button_msg_ts = body.get("message", {}).get("ts", "")
        button_blocks = body.get("message", {}).get("blocks", [])

        _export(
            channel=channel,
            thread_ts=thread_ts,
            client=client,
            llm=llm,
            ctx=ctx,
            button_channel=button_channel,
            button_msg_ts=button_msg_ts,
            button_blocks=button_blocks,
        )
