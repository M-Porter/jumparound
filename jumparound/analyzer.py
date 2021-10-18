import threading
import os
from typing import List
from jumparound.cache import Cache, CacheRepo
from jumparound.config import Config
from rich import print as rprint


class Analyzer:
    _found: List[str] = []
    _config: Config
    _cache_repo: CacheRepo

    def __init__(self, config: Config) -> None:
        self._config = config
        self._cache_repo = CacheRepo(config)

    def run(self, callback=None, debug=False, use_cache=True) -> None:
        if use_cache:
            cache = self._cache_repo.load()
            if not cache.is_stale():
                if callback:
                    callback(cache.directories)
                if debug:
                    rprint("loading from cache")
                    rprint(cache.directories)
                return

        self._found = []
        threads = []
        for p in self._config.search_include_paths():
            t = threading.Thread(target=self._walk_path, args=(p,))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
        self._cache_repo.store(Cache(directories=self._found))
        if callback:
            callback(self._found)
        if debug:
            rprint("not using cache")
            rprint(self._found)
        self._found = []

    def _walk_path(self, path: str) -> None:
        for root, dirs, files in os.walk(path, topdown=True):
            if root.endswith(tuple(self._config.search_excludes)):
                dirs[:] = []
            match_dirs = [d for d in dirs if d in self._config.path_stops]
            match_files = [f for f in files if f in self._config.path_stops]
            if match_dirs or match_files:
                self._found.append(root)
