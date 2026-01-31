from typing import Any, Optional
import json
from pathlib import Path
import logging
import hashlib
import time

logger = logging.getLogger(__name__)


class Cache:
    def __init__(self, cache_dir: str = ".cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    def get(self, key: str) -> Optional[Any]:
        cache_file = self._get_cache_path(key)
        if cache_file.exists():
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if data.get("expires_at") and data["expires_at"] < time.time():
                        return None
                    return data["value"]
            except Exception as e:
                logger.warning(f"Failed to read cache {key}: {e}")
        return None

    def set(self, key: str, value: Any, ttl: int = 3600):
        cache_file = self._get_cache_path(key)
        try:
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump({"value": value, "expires_at": time.time() + ttl}, f)
        except Exception as e:
            logger.warning(f"Failed to write cache {key}: {e}")

    def _get_cache_path(self, key: str) -> Path:
        hashed = hashlib.md5(key.encode()).hexdigest()
        return self.cache_dir / f"{hashed}.json"

    def clear(self):
        for f in self.cache_dir.glob("*.json"):
            f.unlink()
