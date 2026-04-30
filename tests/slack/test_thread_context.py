"""Tests for the thread context manager."""

import tempfile
from datetime import datetime, timedelta, timezone

import pytest

from slack_bot.context.thread import MAX_MESSAGES, ThreadContext, _Entry


# ── Helpers ───────────────────────────────────────────────────────────────── #

def _backdate(ctx, channel, thread_ts, minutes):
    """Move an in-memory entry back in time to simulate expiry."""
    key = (channel, thread_ts)
    old = ctx._store[key]
    ctx._store[key] = _Entry(
        messages=old.messages,
        last_active=datetime.now(tz=timezone.utc) - timedelta(minutes=minutes),
    )


def _mem():
    return ThreadContext()


def _db():
    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    return ThreadContext(db_path=tmp.name)


# ── Parametrise every behavioural test over both backends ─────────────────── #

@pytest.fixture(params=["memory", "sqlite"])
def ctx(request):
    if request.param == "memory":
        return _mem()
    return _db()


class TestGetAndAppend:
    def test_empty_thread_returns_empty_list(self, ctx):
        assert ctx.get("C123", "1234567890.000") == []

    def test_appended_message_is_retrievable(self, ctx):
        ctx.append("C123", "ts1", "user", "hello")
        msgs = ctx.get("C123", "ts1")
        assert len(msgs) == 1
        assert msgs[0] == {"role": "user", "content": "hello"}

    def test_multi_turn_order_preserved(self, ctx):
        ctx.append("C1", "ts1", "user", "first")
        ctx.append("C1", "ts1", "assistant", "second")
        ctx.append("C1", "ts1", "user", "third")
        msgs = ctx.get("C1", "ts1")
        assert [m["content"] for m in msgs] == ["first", "second", "third"]

    def test_different_threads_are_isolated(self, ctx):
        ctx.append("C1", "ts1", "user", "thread A")
        ctx.append("C1", "ts2", "user", "thread B")
        assert ctx.get("C1", "ts1")[0]["content"] == "thread A"
        assert ctx.get("C1", "ts2")[0]["content"] == "thread B"

    def test_different_channels_are_isolated(self, ctx):
        ctx.append("C1", "ts1", "user", "channel 1")
        ctx.append("C2", "ts1", "user", "channel 2")
        assert ctx.get("C1", "ts1")[0]["content"] == "channel 1"
        assert ctx.get("C2", "ts1")[0]["content"] == "channel 2"


class TestClear:
    def test_clear_removes_thread(self, ctx):
        ctx.append("C1", "ts1", "user", "hello")
        ctx.clear("C1", "ts1")
        assert ctx.get("C1", "ts1") == []

    def test_clear_nonexistent_thread_is_safe(self, ctx):
        ctx.clear("C1", "ts_nonexistent")  # must not raise


class TestExpiry:
    def test_expired_entries_are_removed(self):
        ctx = _mem()
        ctx.append("C1", "ts1", "user", "old message")
        _backdate(ctx, "C1", "ts1", minutes=31)
        assert ctx.get("C1", "ts1") == []

    def test_fresh_entries_survive_expiry(self, ctx):
        ctx.append("C1", "ts1", "user", "recent")
        assert len(ctx.get("C1", "ts1")) == 1

    def test_sqlite_expired_entries_are_removed(self):
        import sqlite3, time
        ctx = _db()
        ctx.append("C1", "ts1", "user", "old")
        # Backdate directly in the DB
        cutoff = (datetime.now(tz=timezone.utc) - timedelta(minutes=31)).timestamp()
        ctx._conn.execute(
            "UPDATE thread_context SET last_active=? WHERE channel='C1' AND thread_ts='ts1'",
            (cutoff,),
        )
        ctx._conn.commit()
        assert ctx.get("C1", "ts1") == []


class TestActiveCount:
    def test_count_reflects_active_threads(self, ctx):
        assert ctx.active_thread_count() == 0
        ctx.append("C1", "ts1", "user", "a")
        ctx.append("C1", "ts2", "user", "b")
        assert ctx.active_thread_count() == 2


class TestMessageCap:
    def test_memory_caps_at_max_messages(self):
        ctx = _mem()
        for i in range(MAX_MESSAGES + 10):
            ctx.append("C1", "ts1", "user", f"msg {i}")
        msgs = ctx.get("C1", "ts1")
        assert len(msgs) == MAX_MESSAGES
        assert msgs[-1]["content"] == f"msg {MAX_MESSAGES + 9}"

    def test_sqlite_caps_at_max_messages(self):
        ctx = _db()
        for i in range(MAX_MESSAGES + 10):
            ctx.append("C1", "ts1", "user", f"msg {i}")
        msgs = ctx.get("C1", "ts1")
        assert len(msgs) == MAX_MESSAGES
        assert msgs[-1]["content"] == f"msg {MAX_MESSAGES + 9}"


class TestSQLitePersistence:
    def test_context_survives_across_instances(self):
        tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        db_path = tmp.name
        tmp.close()

        ctx1 = ThreadContext(db_path=db_path)
        ctx1.append("C1", "ts1", "user", "persisted message")

        ctx2 = ThreadContext(db_path=db_path)
        msgs = ctx2.get("C1", "ts1")
        assert len(msgs) == 1
        assert msgs[0]["content"] == "persisted message"
