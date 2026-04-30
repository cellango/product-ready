"""Tests for the per-user sliding-window rate limiter."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from unittest.mock import patch

import pytest

from slack_bot.rate_limiter import RateLimiter, build_rate_limiter


class TestRateLimiter:
    def test_allows_requests_within_limit(self):
        rl = RateLimiter(per_minute=5)
        for _ in range(5):
            assert rl.is_allowed("U001") is True

    def test_blocks_request_over_limit(self):
        rl = RateLimiter(per_minute=3)
        for _ in range(3):
            rl.is_allowed("U001")
        assert rl.is_allowed("U001") is False

    def test_different_users_are_independent(self):
        rl = RateLimiter(per_minute=2)
        rl.is_allowed("U001")
        rl.is_allowed("U001")
        assert rl.is_allowed("U001") is False
        assert rl.is_allowed("U002") is True

    def test_old_requests_slide_out_of_window(self):
        rl = RateLimiter(per_minute=2)
        now = datetime.now(tz=timezone.utc)

        # Simulate two requests that are >60s old
        old = now - timedelta(seconds=61)
        with patch("slack_bot.rate_limiter.datetime") as mock_dt:
            mock_dt.now.return_value = old
            rl.is_allowed("U001")
            rl.is_allowed("U001")

        # Both old entries should have slid out; new request must be allowed
        assert rl.is_allowed("U001") is True

    def test_remaining_decrements_with_use(self):
        rl = RateLimiter(per_minute=5)
        assert rl.remaining("U001") == 5
        rl.is_allowed("U001")
        assert rl.remaining("U001") == 4
        rl.is_allowed("U001")
        assert rl.remaining("U001") == 3

    def test_remaining_never_goes_negative(self):
        rl = RateLimiter(per_minute=2)
        for _ in range(5):
            rl.is_allowed("U001")
        assert rl.remaining("U001") == 0


class TestBuildRateLimiter:
    def test_reads_env_var(self, monkeypatch):
        monkeypatch.setenv("RATE_LIMIT_PER_MINUTE", "25")
        rl = build_rate_limiter()
        assert rl._per_minute == 25

    def test_defaults_when_env_not_set(self, monkeypatch):
        monkeypatch.delenv("RATE_LIMIT_PER_MINUTE", raising=False)
        rl = build_rate_limiter()
        assert rl._per_minute == 10

    def test_invalid_env_var_falls_back_to_default(self, monkeypatch):
        monkeypatch.setenv("RATE_LIMIT_PER_MINUTE", "not-a-number")
        rl = build_rate_limiter()
        assert rl._per_minute == 10
