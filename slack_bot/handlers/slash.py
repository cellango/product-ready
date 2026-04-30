"""
Slash command handlers.

Supported commands:
  /product-ready [text]   generic — intent detected automatically
  /prd [text]             direct entry to PRD workflow
  /behavior [text]        direct entry to Behavior Spec workflow
  /backlog [text]         direct entry to Backlog Review workflow
"""

from __future__ import annotations

from slack_bolt import App

from slack_bot.context.thread import ThreadContext
from slack_bot.handlers.common import handle_message
from slack_bot.llm.client import LLMClient
from slack_bot.rate_limiter import RateLimiter

# Intent overrides for direct-entry commands
_INTENT_HINTS = {
    "/prd": "[Workflow: PRD] Start with clarifying questions before drafting.",
    "/behavior": "[Workflow: Behavior Spec] Ask which feature before generating scenarios.",
    "/backlog": "[Workflow: Backlog Review] Apply all 7 guardrails. Flag missing decisions with [MPD].",
}


def register(app: App, llm: LLMClient, ctx: ThreadContext, rl: RateLimiter) -> None:
    """Register all slash command handlers on the given Bolt app."""

    def _make_handler(command_name: str):
        def _handler(ack, respond, command, client):
            ack()
            text = command.get("text", "").strip()
            channel = command["channel_id"]
            # Slash commands start a new thread; use command ts as thread root
            thread_ts = command.get("thread_ts") or command["ts"]
            user = command["user_id"]

            if not text:
                respond(
                    text="What would you like to work on?\n"
                    "Examples:\n"
                    "• `/product-ready write a PRD for login`\n"
                    "• `/prd user registration`\n"
                    "• `/behavior checkout flow`\n"
                    "• `/backlog` (paste your stories in the thread)"
                )
                return

            # For direct commands, inject the intent hint into the text
            hint = _INTENT_HINTS.get(command_name, "")
            augmented = f"{hint}\n\n{text}" if hint else text

            handle_message(
                text=augmented,
                channel=channel,
                thread_ts=thread_ts,
                user=user,
                client=client,
                llm=llm,
                ctx=ctx,
                rl=rl,
            )

        return _handler

    app.command("/product-ready")(_make_handler("/product-ready"))
    app.command("/prd")(_make_handler("/prd"))
    app.command("/behavior")(_make_handler("/behavior"))
    app.command("/backlog")(_make_handler("/backlog"))
