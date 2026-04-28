"""
Block Kit renderer.

Converts plain LLM text responses into structured Slack Block Kit payloads.
Handles four response shapes:
  - Questions (numbered lists → question blocks)
  - Missing Product Decision flags ([MPD] prefix)
  - Structured artifacts (PRD sections, behavior specs)
  - Plain text fallback
"""

from __future__ import annotations

import re

from slack_bot.workflows.router import Intent

# Intents that warrant a "Send to Jira" button
_JIRA_ELIGIBLE_INTENTS = {Intent.PRD, Intent.BACKLOG, Intent.BEHAVIOR}

_MPD_RE = re.compile(r"^\[MPD\]\s*(.+)$", re.M)
_NUMBERED_Q_RE = re.compile(r"^\s*\d+\.\s+(.+)$", re.M)
_SECTION_HEADER_RE = re.compile(r"^#{1,3}\s+(.+)$", re.M)
_REQ_RE = re.compile(r"\b(REQ|BR|BS|TS)-\d+\b")

MAX_BLOCK_TEXT = 3000  # Slack's per-block character limit


def _truncate(text: str, limit: int = MAX_BLOCK_TEXT) -> str:
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."


def _divider() -> dict:
    return {"type": "divider"}


def _section(text: str) -> dict:
    return {
        "type": "section",
        "text": {"type": "mrkdwn", "text": _truncate(text)},
    }


def _header(text: str) -> dict:
    return {
        "type": "header",
        "text": {"type": "plain_text", "text": text[:150], "emoji": True},
    }


def _mpd_block(decisions: list[str]) -> dict:
    bullet_list = "\n".join(f":red_circle: *[MPD]* {d}" for d in decisions)
    return {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"*Missing Product Decisions — must be resolved before this is ready:*\n{bullet_list}",
        },
    }


def _questions_block(questions: list[str]) -> list[dict]:
    lines = "\n".join(f"*{i + 1}.* {q}" for i, q in enumerate(questions))
    return [_section(lines)]


def render_response(
    text: str,
    intent: Intent = Intent.UNKNOWN,
    channel: str = "",
    thread_ts: str = "",
) -> list[dict]:
    """
    Convert an LLM response string into a list of Slack Block Kit blocks.
    Falls back to a plain section block if no structure is detected.
    """
    blocks: list[dict] = []

    # --- Missing Product Decisions ---------------------------------------- #
    mpd_matches = _MPD_RE.findall(text)
    if mpd_matches:
        blocks.append(_mpd_block(mpd_matches))
        blocks.append(_divider())
        # Remove MPD lines from text before further processing
        text = _MPD_RE.sub("", text).strip()

    # --- Numbered questions ----------------------------------------------- #
    question_matches = _NUMBERED_Q_RE.findall(text)
    if question_matches and len(question_matches) <= 6 and len(text) < 800:
        # Looks like a short question list — render as a clean question block
        preamble = _NUMBERED_Q_RE.sub("", text).strip()
        if preamble:
            blocks.append(_section(preamble))
        blocks.extend(_questions_block(question_matches))
        return blocks

    # --- Structured artifact (has markdown headers or REQ/BR/BS/TS refs) --- #
    has_headers = bool(_SECTION_HEADER_RE.search(text))
    has_refs = bool(_REQ_RE.search(text))

    if has_headers or has_refs:
        parts = _SECTION_HEADER_RE.split(text)
        headers = _SECTION_HEADER_RE.findall(text)

        # parts[0] is text before the first header
        if parts[0].strip():
            blocks.append(_section(parts[0].strip()))

        for i, header_text in enumerate(headers):
            blocks.append(_divider())
            blocks.append(_header(header_text))
            body = parts[i + 1].strip() if i + 1 < len(parts) else ""
            if body:
                # Split large bodies into multiple section blocks
                for chunk in _chunk(body, MAX_BLOCK_TEXT):
                    blocks.append(_section(chunk))

        return _append_jira_button(blocks, intent, channel, thread_ts)

    # --- Plain text fallback --------------------------------------------- #
    for chunk in _chunk(text, MAX_BLOCK_TEXT):
        blocks.append(_section(chunk))

    return _append_jira_button(blocks, intent, channel, thread_ts)


def _append_jira_button(
    blocks: list[dict],
    intent: Intent,
    channel: str,
    thread_ts: str,
) -> list[dict]:
    """Add a Send to Jira button when the response is a Jira-eligible artifact."""
    if intent in _JIRA_ELIGIBLE_INTENTS and channel and thread_ts:
        from slack_bot.blocks.jira import send_to_jira_button
        blocks.append({"type": "divider"})
        blocks.append(send_to_jira_button(channel, thread_ts))
    return blocks


def _chunk(text: str, size: int) -> list[str]:
    """Split text into chunks of at most `size` characters at paragraph boundaries."""
    if len(text) <= size:
        return [text]

    chunks = []
    while text:
        if len(text) <= size:
            chunks.append(text)
            break
        split_at = text.rfind("\n\n", 0, size)
        if split_at == -1:
            split_at = text.rfind("\n", 0, size)
        if split_at == -1:
            split_at = size
        chunks.append(text[:split_at].strip())
        text = text[split_at:].strip()

    return [c for c in chunks if c]
