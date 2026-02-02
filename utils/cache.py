"""
缓存工具模块
提供基于文件的缓存功能，支持过期时间设置
"""

from typing import Any, Optional
import json
from pathlib import Path
import logging
import hashlib
import time

logger = logging.getLogger(__name__)


class Cache:
    """
    文件缓存类
    使用 JSON 文件存储缓存数据，支持 TTL 过期机制
    """

    def __init__(self, cache_dir: str = ".cache"):
        """
        初始化缓存

        参数:
            cache_dir: 缓存目录路径
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    def get(self, key: str) -> Optional[Any]:
        """
        获取缓存值

        参数:
            key: 缓存键

        返回:
            缓存值，如果不存在或已过期则返回 None
        """
        cache_file = self._get_cache_path(key)
        if cache_file.exists():
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # 检查是否过期
                    if data.get("expires_at") and data["expires_at"] < time.time():
                        return None
                    return data["value"]
            except Exception as e:
                logger.warning(f"读取缓存失败 {key}: {e}")
        return None

    def set(self, key: str, value: Any, ttl: int = 3600):
        """
        设置缓存值

        参数:
            key: 缓存键
            value: 缓存值
            ttl: 过期时间（秒），默认 3600 秒
        """
        cache_file = self._get_cache_path(key)
        try:
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump({"value": value, "expires_at": time.time() + ttl}, f)
        except Exception as e:
            logger.warning(f"写入缓存失败 {key}: {e}")

    def _get_cache_path(self, key: str) -> Path:
        """
        获取缓存文件路径

        参数:
            key: 缓存键

        返回:
            缓存文件路径
        """
        hashed = hashlib.md5(key.encode()).hexdigest()
        return self.cache_dir / f"{hashed}.json"

    def clear(self):
        """清除所有缓存"""
        for f in self.cache_dir.glob("*.json"):
            f.unlink()

    def load_json(self, key: str) -> Optional[Any]:
        """
        加载 JSON 缓存（别名方法）

        参数:
            key: 缓存键

        返回:
            缓存值
        """
        return self.get(key)

    def save_json(self, key: str, value: Any, ttl: int = 3600):
        """
        保存 JSON 缓存（别名方法）

        参数:
            key: 缓存键
            value: 缓存值
            ttl: 过期时间（秒）
        """
        self.set(key, value, ttl)
