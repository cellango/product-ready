"""
Product Ready Slack bot entry point.

Supports both HTTP mode (SLACK_SIGNING_SECRET) and Socket Mode
(SLACK_APP_TOKEN) — determined by which env vars are present at startup.

Environment variables:
  Required:
    SLACK_BOT_TOKEN       xoxb-... token from your Slack app
    ANTHROPIC_API_KEY     OR
    OPENAI_API_KEY        at least one LLM key required

  HTTP mode (production):
    SLACK_SIGNING_SECRET  from your Slack app Basic Information page
    PORT                  port to listen on (default: 3000)

  Socket Mode (local dev, no public URL needed):
    SLACK_APP_TOKEN       xapp-... token (requires connections:write scope)
"""

from __future__ import annotations

import logging
import os

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from slack_bot.context.thread import ThreadContext
from slack_bot.handlers import jira_export, mention, slash
from slack_bot.llm.client import build_client

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def create_app() -> tuple[App, LLMClient, ThreadContext]:  # type: ignore[name-defined]
    from slack_bot.llm.client import LLMClient  # local to avoid circular at module level

    bot_token = os.environ["SLACK_BOT_TOKEN"]
    signing_secret = os.getenv("SLACK_SIGNING_SECRET", "")

    app = App(token=bot_token, signing_secret=signing_secret or None)
    llm = build_client()
    ctx = ThreadContext()

    slash.register(app, llm, ctx)
    mention.register(app, llm, ctx)
    jira_export.register(app, llm, ctx)

    logger.info("Product Ready bot started — LLM provider: %s", llm.provider)
    return app, llm, ctx


def main() -> None:
    app, llm, ctx = create_app()

    app_token = os.getenv("SLACK_APP_TOKEN")
    if app_token:
        logger.info("Starting in Socket Mode")
        SocketModeHandler(app, app_token).start()
    else:
        port = int(os.getenv("PORT", "3000"))
        logger.info("Starting HTTP server on port %d", port)
        app.start(port=port)


if __name__ == "__main__":
    main()
