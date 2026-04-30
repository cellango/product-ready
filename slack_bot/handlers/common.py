"""
Shared logic used by both slash command and @mention handlers.
"""

from __future__ import annotations

import logging
import re

from slack_bot.blocks.renderer import render_response
from slack_bot.context.thread import ThreadContext
from slack_bot.llm.client import LLMClient
from slack_bot.rate_limiter import RateLimiter
from slack_bot.workflows.router import route

logger = logging.getLogger(__name__)


def _strip_mention(text: str) -> str:
    """Remove <@BOTID> prefix from @mention messages."""
    return re.sub(r"^<@[A-Z0-9]+>\s*", "", text).strip()


def handle_message(
    *,
    text: str,
    channel: str,
    thread_ts: str,
    user: str,
    client,           # slack_sdk WebClient
    llm: LLMClient,
    ctx: ThreadContext,
    rl: RateLimiter,
    is_mention: bool = False,
) -> None:
    """
    Core message handler shared by slash commands and @mentions.

    1. Strips bot mention if needed
    2. Routes to the correct workflow intent (three-tier)
    3. Appends the routing hint + user message to thread history
    4. Calls the LLM
    5. Appends LLM reply to thread history
    6. Posts Block Kit response back to the thread
    """
    clean = _strip_mention(text) if is_mention else text.strip()
    if not clean:
        return

    if user and not rl.is_allowed(user):
        client.chat_postMessage(
            channel=channel,
            thread_ts=thread_ts,
            text=":no_entry: You're sending requests too quickly. Please wait a moment and try again.",
        )
        return

    route_result = route(clean)
    logger.info("channel=%s thread=%s tier=%d intent=%s", channel, thread_ts, route_result.tier, route_result.intent)

    history = ctx.get(channel, thread_ts)

    # prepend routing hint so the LLM knows which workflow step to apply
    user_content = f"{route_result.hint}\n\nUser: {clean}"
    history.append({"role": "user", "content": user_content})

    try:
        reply = llm.complete(history)
    except Exception as exc:
        logger.exception("LLM call failed: %s", exc)
        client.chat_postMessage(
            channel=channel,
            thread_ts=thread_ts,
            text=":warning: Something went wrong calling the LLM. Check the bot logs.",
        )
        return

    ctx.append(channel, thread_ts, "user", user_content)
    ctx.append(channel, thread_ts, "assistant", reply)

    blocks = render_response(reply, intent=route_result.intent, channel=channel, thread_ts=thread_ts)
    client.chat_postMessage(
        channel=channel,
        thread_ts=thread_ts,
        text=reply,        # fallback for notifications
        blocks=blocks,
    )
