"""
@mention handler.

Fires when the bot is mentioned in any channel it has been added to.
Replies in the same thread, maintaining conversation context.
"""

from __future__ import annotations

from slack_bolt import App

from slack_bot.context.thread import ThreadContext
from slack_bot.handlers.common import handle_message
from slack_bot.llm.client import LLMClient
from slack_bot.rate_limiter import RateLimiter


def register(app: App, llm: LLMClient, ctx: ThreadContext, rl: RateLimiter) -> None:
    """Register the app_mention handler on the given Bolt app."""

    @app.event("app_mention")
    def on_mention(event, client):
        text = event.get("text", "")
        channel = event["channel"]
        # Use thread_ts if in a thread, else the event ts (starts a new thread)
        thread_ts = event.get("thread_ts") or event["ts"]
        user = event.get("user", "")

        handle_message(
            text=text,
            channel=channel,
            thread_ts=thread_ts,
            user=user,
            client=client,
            llm=llm,
            ctx=ctx,
            rl=rl,
            is_mention=True,
        )
