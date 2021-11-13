import os
from enum import Enum
from pathlib import Path
from typing import List

import yaml


class ViewMode(Enum):
    BASIC = 1
    FULL = 2
    COMBINED = 3


class Config:
    _default_cache_file_name: str = "cache"
    _default_search_includes: List[str] = [
        "development/",
        "dev/",
        "xcode-projects/",
        "repos/",
    ]
    _default_search_excludes: List[str] = [
        "/node_modules",
        "/bin",
        "/temp",
        "/tmp",
        "/vendor",
        "/venv",
        "/ios/Pods",
        "/.idea",
        "/go/pkg",
    ]
    _default_path_stops: List[str] = [
        ".git",
        "Gemfile",
        "package.json",
        "go.mod",
        "setup.py",
        "pyproject.toml",
        "requirements.txt",
    ]

    _config_name: str = "config.yaml"
    _jumper_dirname: str = ".jumparound"
    _user_home: str

    cache_file: str
    search_excludes: List[str]
    search_includes: List[str]
    path_stops: List[str]
    view_mode: ViewMode

    def __init__(self) -> None:
        self._user_home = os.path.expanduser("~")
        self.load()

    def load(self) -> None:
        if not os.path.exists(self.get_full_config_dirname()):
            os.makedirs(self.get_full_config_dirname())

        if not os.path.exists(self.get_full_config_file_path()):
            Path(self.get_full_config_file_path()).touch()

        with self.open() as f:
            data = yaml.load(f, Loader=yaml.SafeLoader) or {}

            self.cache_file = data.get("cache_file", self._default_cache_file_name)
            self.search_excludes = data.get(
                "search_excludes", self._default_search_excludes
            )
            self.search_includes = data.get(
                "search_includes", self._default_search_includes
            )
            self.path_stops = data.get("path_stops", self._default_path_stops)
            self.view_mode = data.get("view_mode", ViewMode.BASIC)

            self.write(f)

    def set_view_mode(self, view_mode: ViewMode):
        self.view_mode = view_mode

    def get_view_mode(self) -> ViewMode:
        return self.view_mode

    def open(self):
        return open(self.get_full_config_file_path(), "r+", newline="")

    def write(self, f):
        f.seek(0)
        f.write(self.dump())

    def dump(self):
        return yaml.dump(
            {
                "cache_file": self.cache_file,
                "search_excludes": self.search_excludes,
                "search_includes": self.search_includes,
                "path_stops": self.path_stops,
            },
            Dumper=yaml.SafeDumper,
        )

    def get_full_config_dirname(self) -> str:
        return os.path.join(self._user_home, self._jumper_dirname)

    def get_full_config_file_path(self) -> str:
        return os.path.join(self.get_full_config_dirname(), self._config_name)

    def cache_file_path(self) -> str:
        return os.path.join(self.get_full_config_dirname(), self.cache_file)

    def search_include_paths(self) -> map:
        return map(
            lambda p: os.path.join(self._user_home, p),
            self.search_includes,
        )
