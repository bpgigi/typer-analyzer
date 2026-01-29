import json
import pickle
from typing import Any, Optional
from pathlib import Path
import shutil


class Cache:
    def __init__(self, cache_dir: str = "data"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    def save_json(self, data: Any, filename: str) -> Path:
        path = self.cache_dir / filename
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return path

    def load_json(self, filename: str) -> Optional[Any]:
        path = self.cache_dir / filename
        if not path.exists():
            return None
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_pickle(self, data: Any, filename: str) -> Path:
        path = self.cache_dir / filename
        with open(path, "wb") as f:
            pickle.dump(data, f)
        return path

    def load_pickle(self, filename: str) -> Optional[Any]:
        path = self.cache_dir / filename
        if not path.exists():
            return None
        with open(path, "rb") as f:
            return pickle.load(f)

    def clear(self):
        for f in self.cache_dir.iterdir():
            if f.is_file():
                f.unlink()

    def delete(self, filename: str):
        path = self.cache_dir / filename
        if path.exists():
            path.unlink()

    def exists(self, filename: str) -> bool:
        return (self.cache_dir / filename).exists()
