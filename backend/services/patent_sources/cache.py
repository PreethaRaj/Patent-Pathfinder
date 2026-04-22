from __future__ import annotations

import hashlib
import json
from typing import Any

from cachetools import TTLCache

from backend.core.config import settings

_cache: TTLCache[str, Any] = TTLCache(maxsize=settings.patent_cache_maxsize, ttl=settings.patent_cache_ttl_seconds)


def make_cache_key(prefix: str, payload: dict) -> str:
    raw = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    return f'{prefix}:{hashlib.sha256(raw.encode("utf-8")).hexdigest()}'


def cache_get(key: str):
    return _cache.get(key)


def cache_set(key: str, value: Any):
    _cache[key] = value
