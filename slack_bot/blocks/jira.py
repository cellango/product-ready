"""
Block Kit blocks for Jira integration UI.
"""

from __future__ import annotations

from slack_bot.jira.client import ExportResult


def replace_jira_button_with_sent(blocks: list[dict]) -> list[dict]:
    """Swap the Send-to-Jira actions block for a static 'sent' indicator."""
    filtered = [
        b for b in blocks
        if not (
            b.get("type") == "actions"
            and any(e.get("action_id") == "jira_export" for e in b.get("elements", []))
        )
    ]
    filtered.append({
        "type": "context",
        "elements": [{"type": "mrkdwn", "text": ":white_check_mark: Sent to Jira"}],
    })
    return filtered


def send_to_jira_button(channel: str, thread_ts: str) -> dict:
    """Action button appended to PRD and issues responses."""
    return {
        "type": "actions",
        "elements": [
            {
                "type": "button",
                "text": {"type": "plain_text", "text": ":jira: Send to Jira", "emoji": True},
                "style": "primary",
                "action_id": "jira_export",
                "value": f"{channel}|{thread_ts}",
            }
        ],
    }


def jira_progress_block(message: str) -> list[dict]:
    return [
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": f":hourglass_flowing_sand: {message}"},
        }
    ]


def jira_insufficient_data_block(message: str) -> list[dict]:
    return [
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": f":information_source: *Nothing to export yet*\n{message}"},
        }
    ]


def jira_error_block(message: str) -> list[dict]:
    return [
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": f":x: *Jira export failed*\n{message}"},
        }
    ]


def jira_confirmation_blocks(title: str, result: ExportResult) -> list[dict]:
    blocks: list[dict] = [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": ":white_check_mark: Exported to Jira", "emoji": True},
        },
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"*{title}*"},
        },
        {"type": "divider"},
    ]

    if result.epic:
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f":large_purple_circle: *Epic* — <{result.epic.url}|{result.epic.key}>: {result.epic.summary}",
            },
        })

    if result.stories:
        story_lines = "\n".join(
            f"• <{s.url}|{s.key}>: {s.summary}" for s in result.stories
        )
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f":large_blue_circle: *Stories ({len(result.stories)})*\n{story_lines}",
            },
        })

    total = len(result.all_issues)
    blocks.append({
        "type": "context",
        "elements": [
            {"type": "mrkdwn", "text": f"{total} issue{'s' if total != 1 else ''} created in Jira."}
        ],
    })

    return blocks
