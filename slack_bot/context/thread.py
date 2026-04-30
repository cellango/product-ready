"""
Thread context manager.

Keeps conversation history keyed by (channel_id, thread_ts). Entries expire
after TTL_MINUTES of inactivity and are capped at MAX_MESSAGES per thread
to bound LLM context window size.

By default uses in-memory storage. Set CONTEXT_DB_PATH to a SQLite file path
to persist context across container restarts and deploys.
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timedelta, timezone
from threading import Lock
from typing import NamedTuple

from slack_bot.llm.client import Message

TTL_MINUTES = 30
MAX_MESSAGES = 50  # tail kept per thread; prevents unbounded LLM context growth


class _Entry(NamedTuple):
    messages: list[Message]
    last_active: datetime


class ThreadContext:
    def __init__(self, ttl_minutes: int = TTL_MINUTES, db_path: str | None = None) -> None:
        self._ttl = timedelta(minutes=ttl_minutes)
        self._lock = Lock()

        if db_path:
            self._conn = sqlite3.connect(db_path, check_same_thread=False)
            self._conn.execute("PRAGMA journal_mode=WAL")
            self._conn.execute("""
                CREATE TABLE IF NOT EXISTS thread_context (
                    channel   TEXT NOT NULL,
                    thread_ts TEXT NOT NULL,
                    messages  TEXT NOT NULL,
                    last_active REAL NOT NULL,
                    PRIMARY KEY (channel, thread_ts)
                )
            """)
            self._conn.commit()
            self._store: dict[tuple[str, str], _Entry] | None = None
        else:
            self._conn: sqlite3.Connection | None = None
            self._store = {}

    # ── Internal helpers ──────────────────────────────────────────────────── #

    def _now(self) -> datetime:
        return datetime.now(tz=timezone.utc)

    def _cutoff_ts(self) -> float:
        return (self._now() - self._ttl).timestamp()

    # ── SQLite backend ────────────────────────────────────────────────────── #

    def _db_get(self, channel: str, thread_ts: str) -> list[Message]:
        row = self._conn.execute(
            "SELECT messages FROM thread_context "
            "WHERE channel=? AND thread_ts=? AND last_active>=?",
            (channel, thread_ts, self._cutoff_ts()),
        ).fetchone()
        return json.loads(row[0]) if row else []

    def _db_append(self, channel: str, thread_ts: str, role: str, content: str) -> None:
        messages = self._db_get(channel, thread_ts)
        messages.append({"role": role, "content": content})
        self._conn.execute(
            """INSERT INTO thread_context (channel, thread_ts, messages, last_active)
               VALUES (?, ?, ?, ?)
               ON CONFLICT(channel, thread_ts)
               DO UPDATE SET messages=excluded.messages, last_active=excluded.last_active""",
            (channel, thread_ts, json.dumps(messages[-MAX_MESSAGES:]), self._now().timestamp()),
        )
        self._conn.commit()

    def _db_clear(self, channel: str, thread_ts: str) -> None:
        self._conn.execute(
            "DELETE FROM thread_context WHERE channel=? AND thread_ts=?",
            (channel, thread_ts),
        )
        self._conn.commit()

    def _db_expire(self) -> None:
        self._conn.execute(
            "DELETE FROM thread_context WHERE last_active<?", (self._cutoff_ts(),)
        )
        self._conn.commit()

    def _db_count(self) -> int:
        self._db_expire()
        return self._conn.execute("SELECT COUNT(*) FROM thread_context").fetchone()[0]

    # ── In-memory backend ─────────────────────────────────────────────────── #

    def _mem_expire(self) -> None:
        cutoff = self._now() - self._ttl
        for k in [k for k, e in self._store.items() if e.last_active < cutoff]:
            del self._store[k]

    # ── Public API ────────────────────────────────────────────────────────── #

    def get(self, channel: str, thread_ts: str) -> list[Message]:
        with self._lock:
            if self._conn is not None:
                return self._db_get(channel, thread_ts)
            self._mem_expire()
            entry = self._store.get((channel, thread_ts))
            return list(entry.messages) if entry else []

    def append(self, channel: str, thread_ts: str, role: str, content: str) -> None:
        with self._lock:
            if self._conn is not None:
                self._db_append(channel, thread_ts, role, content)
                return
            key = (channel, thread_ts)
            entry = self._store.get(key)
            messages = list(entry.messages) if entry else []
            messages.append({"role": role, "content": content})
            self._store[key] = _Entry(messages=messages[-MAX_MESSAGES:], last_active=self._now())

    def clear(self, channel: str, thread_ts: str) -> None:
        with self._lock:
            if self._conn is not None:
                self._db_clear(channel, thread_ts)
                return
            self._store.pop((channel, thread_ts), None)

    def active_thread_count(self) -> int:
        with self._lock:
            if self._conn is not None:
                return self._db_count()
            self._mem_expire()
            return len(self._store)
