"""
Per-user rate limiter using a sliding window counter.

Prevents any single Slack user from triggering excessive LLM API calls.
Default: 10 requests per 60-second window per user.
Override with the RATE_LIMIT_PER_MINUTE environment variable.
"""

from __future__ import annotations

import os
from collections import deque
from datetime import datetime, timedelta, timezone
from threading import Lock

_DEFAULT_PER_MINUTE = 10


class RateLimiter:
    def __init__(self, per_minute: int = _DEFAULT_PER_MINUTE) -> None:
        self._per_minute = per_minute
        self._window = timedelta(minutes=1)
        self._lock = Lock()
        self._log: dict[str, deque[datetime]] = {}

    def is_allowed(self, user_id: str) -> bool:
        """Return True and record the request, or False if the user is over-limit."""
        now = datetime.now(tz=timezone.utc)
        cutoff = now - self._window
        with self._lock:
            dq = self._log.setdefault(user_id, deque())
            while dq and dq[0] < cutoff:
                dq.popleft()
            if len(dq) >= self._per_minute:
                return False
            dq.append(now)
            return True

    def remaining(self, user_id: str) -> int:
        """How many requests the user can still make in the current window."""
        now = datetime.now(tz=timezone.utc)
        cutoff = now - self._window
        with self._lock:
            dq = self._log.get(user_id, deque())
            recent = sum(1 for t in dq if t >= cutoff)
            return max(0, self._per_minute - recent)


def build_rate_limiter() -> RateLimiter:
    try:
        per_minute = int(os.getenv("RATE_LIMIT_PER_MINUTE", str(_DEFAULT_PER_MINUTE)))
    except ValueError:
        per_minute = _DEFAULT_PER_MINUTE
    return RateLimiter(per_minute=per_minute)
