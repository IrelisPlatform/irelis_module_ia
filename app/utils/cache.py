from __future__ import annotations

import hashlib
import json
import threading
import time
from datetime import date, datetime
from enum import Enum
from typing import Any
from uuid import UUID


class TTLCache:
    """Simple in-memory cache with time-based eviction."""

    def __init__(self, default_ttl_seconds: int = 60, max_entries: int = 1024):
        self.default_ttl_seconds = default_ttl_seconds
        self.max_entries = max_entries
        self._store: dict[str, tuple[float, Any]] = {}
        self._lock = threading.Lock()

    def get(self, key: str) -> tuple[bool, Any]:
        now = time.time()
        with self._lock:
            entry = self._store.get(key)
            if entry is None:
                return False, None
            expires_at, value = entry
            if expires_at < now:
                self._store.pop(key, None)
                return False, None
            return True, value

    def set(self, key: str, value: Any, ttl_seconds: int | None = None) -> None:
        ttl = self.default_ttl_seconds if ttl_seconds is None else ttl_seconds
        expires_at = time.time() + max(ttl, 0)
        with self._lock:
            if len(self._store) >= self.max_entries:
                self._prune()
            self._store[key] = (expires_at, value)

    def _prune(self) -> None:
        now = time.time()
        expired = [key for key, (exp, _) in self._store.items() if exp < now]
        for key in expired:
            self._store.pop(key, None)
        while len(self._store) >= self.max_entries and self._store:
            self._store.pop(next(iter(self._store)))


def _serialize_cache_value(value: Any) -> Any:
    if value is None:
        return None
    if hasattr(value, "model_dump"):
        return value.model_dump()
    if isinstance(value, (list, tuple, set)):
        return [_serialize_cache_value(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _serialize_cache_value(val) for key, val in value.items()}
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, UUID):
        return str(value)
    if isinstance(value, Enum):
        return value.value
    return value


def make_cache_key(prefix: str, *parts: Any, **kwargs: Any) -> str:
    payload = {
        "parts": [_serialize_cache_value(part) for part in parts],
        "kwargs": {key: _serialize_cache_value(val) for key, val in sorted(kwargs.items())},
    }
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    return f"{prefix}:{digest}"


APP_CACHE = TTLCache(default_ttl_seconds=60, max_entries=1024)
