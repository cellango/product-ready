"""
Thread context manager.

Keeps conversation history keyed by (channel_id, thread_ts) so multi-turn
product-ready workflows work naturally within Slack threads. Entries expire
after TTL_MINUTES of inactivity to avoid unbounded memory growth.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from threading import Lock
from typing import NamedTuple

from slack_bot.llm.client import Message

TTL_MINUTES = 30


class _Entry(NamedTuple):
    messages: list[Message]
    last_active: datetime


class ThreadContext:
    def __init__(self, ttl_minutes: int = TTL_MINUTES) -> None:
        self._ttl = timedelta(minutes=ttl_minutes)
        self._store: dict[tuple[str, str], _Entry] = {}
        self._lock = Lock()

    def _key(self, channel: str, thread_ts: str) -> tuple[str, str]:
        return (channel, thread_ts)

    def _now(self) -> datetime:
        return datetime.now(tz=timezone.utc)

    def _expire(self) -> None:
        cutoff = self._now() - self._ttl
        expired = [k for k, e in self._store.items() if e.last_active < cutoff]
        for k in expired:
            del self._store[k]

    def get(self, channel: str, thread_ts: str) -> list[Message]:
        with self._lock:
            self._expire()
            entry = self._store.get(self._key(channel, thread_ts))
            return list(entry.messages) if entry else []

    def append(self, channel: str, thread_ts: str, role: str, content: str) -> None:
        key = self._key(channel, thread_ts)
        with self._lock:
            entry = self._store.get(key)
            messages = list(entry.messages) if entry else []
            messages.append({"role": role, "content": content})
            self._store[key] = _Entry(messages=messages, last_active=self._now())

    def clear(self, channel: str, thread_ts: str) -> None:
        with self._lock:
            self._store.pop(self._key(channel, thread_ts), None)

    def active_thread_count(self) -> int:
        with self._lock:
            self._expire()
            return len(self._store)
