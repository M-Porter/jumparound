import os
from dataclasses import dataclass, field
from time import time
from typing import Dict, List

import yaml

from src.jumparound.config import Config

# stale cache time in seconds
STALE_CACHE_TIME = 86400


@dataclass
class Cache:
    updated_at: float = 0
    directories: List[str] = field(default_factory=List)

    @staticmethod
    def from_source(data: Dict):
        updated_at = data["updated_at"] if "updated_at" in data else 0
        directories = data["directories"] if "directories" in data else []
        return Cache(updated_at=updated_at, directories=directories)

    def to_dict(self) -> Dict:
        return {
            "updated_at": self.updated_at,
            "directories": self.directories,
        }

    def is_stale(self) -> bool:
        return time() - self.updated_at >= STALE_CACHE_TIME


class CacheRepo:
    _config: Config

    def __init__(self, config: Config) -> None:
        self._config = config

    def load(self) -> Cache:
        if not os.path.exists(self._config.cache_file_path()):
            return Cache(directories=[])
        with open(self._config.cache_file_path(), "r+", newline="") as f:
            return Cache.from_source(yaml.load(f, Loader=yaml.SafeLoader))

    def store(self, cache: Cache):
        with open(self._config.cache_file_path(), "w+", newline="") as f:
            cache.updated_at = time()
            f.seek(0)
            f.write(yaml.dump(cache.to_dict(), Dumper=yaml.SafeDumper))
