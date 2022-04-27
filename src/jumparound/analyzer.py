import os
import threading
from dataclasses import dataclass
from typing import List

from .cache import Cache, CacheRepo
from .config import Config


@dataclass
class Project:
    name: str
    dirname: str
    path: str

    @staticmethod
    def init_from_path(path: str):
        return Project(
            path=path,
            name=os.path.basename(path),
            dirname=os.path.dirname(path),
        )


class Analyzer:
    _found: List[Project] = []
    _config: Config
    _cache_repo: CacheRepo

    def __init__(self, config: Config) -> None:
        self._config = config
        self._cache_repo = CacheRepo(config)

    def run(self, callback=None, use_cache=True) -> None:
        if use_cache:
            cache = self._cache_repo.load()
            if not cache.is_stale():
                if callback:
                    callback(
                        list(
                            map(lambda x: Project.init_from_path(x), cache.directories)
                        )
                    )
                return

        self._found = []
        threads = []
        for p in self._config.search_include_paths():
            t = threading.Thread(target=self._walk_path, args=(p,))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
        self._cache_repo.store(Cache(directories=self._found_paths()))
        if callback:
            callback(self._found)
        self._found = []

    def _found_paths(self):
        return list(map(lambda x: x.path, self._found))

    def _walk_path(self, path: str) -> None:
        for root, dirs, files in os.walk(path, topdown=True):
            if root.endswith(tuple(self._config.search_excludes)):
                dirs[:] = []  # stop walking if in search_excludes path
            match_dirs = [d for d in dirs if d in self._config.path_stops]
            match_files = [f for f in files if f in self._config.path_stops]
            if match_dirs or match_files:
                self._found.append(Project.init_from_path(root))
                dirs[:] = []  # stop walking if we run into path stop
