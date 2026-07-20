"""Redis cache helper with graceful degradation."""
import json
import logging
from typing import Any, Optional

import redis

logger = logging.getLogger(__name__)


class Cache:
    def __init__(self):
        self._client: Optional[redis.Redis] = None
        self._url: Optional[str] = None
        self._ttl: int = 60

    def init_app(self, app):
        self._url = app.config["REDIS_URL"]
        self._ttl = int(app.config.get("REDIS_CACHE_TTL_SECONDS", 60))
        try:
            self._client = redis.Redis.from_url(self._url, decode_responses=True,
                                                socket_connect_timeout=2, socket_timeout=2)
            self._client.ping()
            logger.info("redis_connected", extra={"url": self._url})
        except Exception as exc:  # pragma: no cover
            logger.warning("redis_unavailable", extra={"error": str(exc)})
            self._client = None

    @property
    def client(self) -> Optional[redis.Redis]:
        return self._client

    def is_available(self) -> bool:
        if not self._client:
            return False
        try:
            return bool(self._client.ping())
        except Exception:
            return False

    def get(self, key: str) -> Any:
        if not self._client:
            return None
        try:
            v = self._client.get(key)
            return json.loads(v) if v else None
        except Exception as exc:
            logger.warning("cache_get_error", extra={"key": key, "error": str(exc)})
            return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        if not self._client:
            return
        try:
            self._client.setex(key, ttl or self._ttl, json.dumps(value, default=str))
        except Exception as exc:
            logger.warning("cache_set_error", extra={"key": key, "error": str(exc)})

    def delete(self, *keys: str) -> None:
        if not self._client or not keys:
            return
        try:
            self._client.delete(*keys)
        except Exception as exc:
            logger.warning("cache_delete_error", extra={"keys": keys, "error": str(exc)})

    def delete_pattern(self, pattern: str) -> None:
        if not self._client:
            return
        try:
            for key in self._client.scan_iter(match=pattern, count=200):
                self._client.delete(key)
        except Exception as exc:
            logger.warning("cache_delete_pattern_error", extra={"pattern": pattern, "error": str(exc)})


cache = Cache()
