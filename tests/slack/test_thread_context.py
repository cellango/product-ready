"""Tests for the thread context manager."""

from datetime import datetime, timedelta, timezone

import pytest

from slack_bot.context.thread import ThreadContext


class TestGetAndAppend:
    def test_empty_thread_returns_empty_list(self):
        ctx = ThreadContext()
        assert ctx.get("C123", "1234567890.000") == []

    def test_appended_message_is_retrievable(self):
        ctx = ThreadContext()
        ctx.append("C123", "ts1", "user", "hello")
        msgs = ctx.get("C123", "ts1")
        assert len(msgs) == 1
        assert msgs[0] == {"role": "user", "content": "hello"}

    def test_multi_turn_order_preserved(self):
        ctx = ThreadContext()
        ctx.append("C1", "ts1", "user", "first")
        ctx.append("C1", "ts1", "assistant", "second")
        ctx.append("C1", "ts1", "user", "third")
        msgs = ctx.get("C1", "ts1")
        assert [m["content"] for m in msgs] == ["first", "second", "third"]

    def test_different_threads_are_isolated(self):
        ctx = ThreadContext()
        ctx.append("C1", "ts1", "user", "thread A")
        ctx.append("C1", "ts2", "user", "thread B")
        assert ctx.get("C1", "ts1")[0]["content"] == "thread A"
        assert ctx.get("C1", "ts2")[0]["content"] == "thread B"

    def test_different_channels_are_isolated(self):
        ctx = ThreadContext()
        ctx.append("C1", "ts1", "user", "channel 1")
        ctx.append("C2", "ts1", "user", "channel 2")
        assert ctx.get("C1", "ts1")[0]["content"] == "channel 1"
        assert ctx.get("C2", "ts1")[0]["content"] == "channel 2"


class TestClear:
    def test_clear_removes_thread(self):
        ctx = ThreadContext()
        ctx.append("C1", "ts1", "user", "hello")
        ctx.clear("C1", "ts1")
        assert ctx.get("C1", "ts1") == []

    def test_clear_nonexistent_thread_is_safe(self):
        ctx = ThreadContext()
        ctx.clear("C1", "ts_nonexistent")  # should not raise


class TestExpiry:
    def test_expired_entries_are_removed(self):
        ctx = ThreadContext(ttl_minutes=30)
        ctx.append("C1", "ts1", "user", "old message")

        # Manually backdate the entry
        key = ("C1", "ts1")
        old_entry = ctx._store[key]
        from slack_bot.context.thread import _Entry
        ctx._store[key] = _Entry(
            messages=old_entry.messages,
            last_active=datetime.now(tz=timezone.utc) - timedelta(minutes=31),
        )

        assert ctx.get("C1", "ts1") == []

    def test_fresh_entries_survive_expiry(self):
        ctx = ThreadContext(ttl_minutes=30)
        ctx.append("C1", "ts1", "user", "recent")
        assert len(ctx.get("C1", "ts1")) == 1


class TestActiveCount:
    def test_count_reflects_active_threads(self):
        ctx = ThreadContext()
        assert ctx.active_thread_count() == 0
        ctx.append("C1", "ts1", "user", "a")
        ctx.append("C1", "ts2", "user", "b")
        assert ctx.active_thread_count() == 2
