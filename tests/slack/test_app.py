"""Tests for slack_bot.app.create_app startup validation."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest


def _base_env(monkeypatch, **overrides):
    """Set the minimum env vars needed and apply any overrides/deletions."""
    defaults = {
        "SLACK_BOT_TOKEN": "xoxb-test",
        "ANTHROPIC_API_KEY": "sk-test",
    }
    defaults.update({k: v for k, v in overrides.items() if v is not None})
    for k, v in defaults.items():
        monkeypatch.setenv(k, v)
    for k, v in overrides.items():
        if v is None:
            monkeypatch.delenv(k, raising=False)


def _patched_create_app():
    """Context manager that patches App, build_client, and ThreadContext."""
    return patch.multiple(
        "slack_bot.app",
        App=MagicMock(return_value=MagicMock()),
        build_client=MagicMock(return_value=MagicMock(provider="anthropic")),
        ThreadContext=MagicMock(return_value=MagicMock()),
    )


class TestCreateAppSigningSecretGuard:
    def test_http_mode_without_signing_secret_raises(self, monkeypatch):
        _base_env(monkeypatch, SLACK_APP_TOKEN=None, SLACK_SIGNING_SECRET=None)
        with _patched_create_app():
            from slack_bot.app import create_app
            with pytest.raises(RuntimeError, match="SLACK_SIGNING_SECRET is required"):
                create_app()

    def test_socket_mode_without_signing_secret_is_allowed(self, monkeypatch):
        _base_env(monkeypatch, SLACK_APP_TOKEN="xapp-test", SLACK_SIGNING_SECRET=None)
        with _patched_create_app():
            from slack_bot.app import create_app
            app, llm, ctx = create_app()  # must not raise
        assert app is not None

    def test_http_mode_with_signing_secret_succeeds(self, monkeypatch):
        _base_env(monkeypatch, SLACK_APP_TOKEN=None, SLACK_SIGNING_SECRET="secret123")
        with _patched_create_app():
            from slack_bot.app import create_app
            app, llm, ctx = create_app()  # must not raise
        assert app is not None
