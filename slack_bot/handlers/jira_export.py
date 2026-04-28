"""
Jira export handler.

Two entry points:
  1. /product-ready export  — slash command, exports current thread
  2. block_actions jira_export_<channel>_<thread_ts> — "Send to Jira" button

Both paths:
  1. Retrieve thread conversation history
  2. Call the LLM extractor to get structured PRD/story data
  3. Create Epic + Stories in Jira
  4. Post a confirmation block with links to created issues
"""

from __future__ import annotations

import logging
import os

from slack_bot.blocks.jira import (
    jira_confirmation_blocks,
    jira_error_block,
    jira_insufficient_data_block,
    jira_progress_block,
)
from slack_bot.context.thread import ThreadContext
from slack_bot.jira.client import ExportResult, JiraClient, JiraError, build_jira_client
from slack_bot.jira.extractor import extract_from_conversation
from slack_bot.llm.client import LLMClient

logger = logging.getLogger(__name__)

_JIRA_ENABLED = all(
    os.getenv(k) for k in ("JIRA_BASE_URL", "JIRA_EMAIL", "JIRA_API_TOKEN", "JIRA_PROJECT_KEY")
)


def _export(
    *,
    channel: str,
    thread_ts: str,
    client,
    llm: LLMClient,
    ctx: ThreadContext,
    respond_fn=None,
) -> None:
    """Core export logic used by both slash command and button handler."""

    if not _JIRA_ENABLED:
        msg = (
            ":warning: Jira is not configured. "
            "Set `JIRA_BASE_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN`, and `JIRA_PROJECT_KEY` "
            "in the bot environment."
        )
        if respond_fn:
            respond_fn(text=msg)
        else:
            client.chat_postMessage(channel=channel, thread_ts=thread_ts, text=msg)
        return

    # Show progress immediately so the user knows something is happening
    progress_msg = client.chat_postMessage(
        channel=channel,
        thread_ts=thread_ts,
        text=":jira: Extracting product data…",
        blocks=jira_progress_block("Extracting product data from conversation…"),
    )
    progress_ts = progress_msg["ts"]

    history = ctx.get(channel, thread_ts)
    if not history:
        client.chat_update(
            channel=channel,
            ts=progress_ts,
            text="Nothing to export yet.",
            blocks=jira_insufficient_data_block("This thread has no product-ready conversation yet. Run a workflow first."),
        )
        return

    # Extract structured data from the conversation
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

    # Update progress
    client.chat_update(
        channel=channel,
        ts=progress_ts,
        text=":jira: Creating Jira issues…",
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
            blocks=jira_error_block(f"Jira returned an error ({exc.status}). Check bot logs for details."),
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

    client.chat_update(
        channel=channel,
        ts=progress_ts,
        text=f"Exported to Jira: {prd.title}",
        blocks=jira_confirmation_blocks(prd.title, result),
    )


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


def register(app, llm: LLMClient, ctx: ThreadContext) -> None:
    """Register Jira export as a slash sub-command and button action."""

    @app.action("jira_export")
    def on_jira_button(ack, body, client):
        ack()
        value = body["actions"][0].get("value", "")
        # value is encoded as "channel|thread_ts"
        parts = value.split("|", 1)
        if len(parts) != 2:
            return
        channel, thread_ts = parts
        _export(channel=channel, thread_ts=thread_ts, client=client, llm=llm, ctx=ctx)
