"""
WSGI entry point for production (gunicorn).

Used by:
  gunicorn slack_bot.wsgi:flask_app

Exposes:
  POST /slack/events      — Slack event subscriptions
  POST /slack/interactive — Slack interactive payloads (buttons, actions)
  GET  /health            — Health check (returns active thread count)

Socket Mode (local dev) still goes through slack_bot.app directly.
"""

from __future__ import annotations

from flask import Flask, jsonify
from flask import request as flask_request
from slack_bolt.adapter.flask import SlackRequestHandler

from slack_bot.app import create_app

_bolt_app, _llm, _ctx = create_app()

flask_app = Flask(__name__)
_handler = SlackRequestHandler(_bolt_app)


@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return _handler.handle(flask_request)


@flask_app.route("/slack/interactive", methods=["POST"])
def slack_interactive():
    return _handler.handle(flask_request)


@flask_app.route("/health")
def health():
    return jsonify(
        {
            "status": "ok",
            "active_threads": _ctx.active_thread_count(),
        }
    )
