import os
from pathlib import Path
from typing import Dict, List, TextIO, Union
from enum import IntEnum
import yaml


DEFAULT_CACHE_FILE_NAME: str = "cache"
DEFAULT_SEARCH_INCLUDES: List[str] = [
    "development/",
    "dev/",
    "xcode-projects/",
    "repos/",
]
DEFAULT_SEARCH_EXCLUDES: List[str] = [
    "/node_modules",
    "/bin",
    "/temp",
    "/tmp",
    "/vendor",
    "/venv",
    "/ios/Pods",
]
DEFAULT_PATH_STOPS: List[str] = [
    ".git",
    "Gemfile",
    "package.json",
    "go.mod",
    "setup.py",
    "pyproject.toml",
    "requirements.txt",
]
JUMPAROUND_DIRNAME = ".jumparound"
JUMPAROUND_CONFIG_NAME = "config.yaml"


class ViewMode(IntEnum):
    BASIC = 1
    FULL = 2
    COMBINED = 3

    def next(self):
        if self.value == max(ViewMode):
            return ViewMode(min(ViewMode))
        return ViewMode(self.value + 1)


class Config:
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

            self.cache_file = data.get("cache_file", DEFAULT_CACHE_FILE_NAME)
            self.search_excludes = data.get("search_excludes", DEFAULT_SEARCH_EXCLUDES)
            self.search_includes = data.get("search_includes", DEFAULT_SEARCH_INCLUDES)
            self.path_stops = data.get("path_stops", DEFAULT_PATH_STOPS)
            self.view_mode = ViewMode(data.get("view_mode", ViewMode.BASIC))

            self.write(f)

    def next_view_mode(self) -> None:
        self.view_mode = self.view_mode.next()
        with self.open() as f:
            self.write(f)

    def get_view_mode(self) -> ViewMode:
        return self.view_mode

    def open(self) -> TextIO:
        return open(self.get_full_config_file_path(), "r+", newline="")

    def write(self, f) -> None:
        f.seek(0)
        f.write(self.dump())

    def values(self) -> Dict[str, any]:
        return {
            "cache_file": self.cache_file,
            "search_excludes": self.search_excludes,
            "search_includes": self.search_includes,
            "path_stops": self.path_stops,
            "view_mode": self.view_mode.value,
        }

    def dump(self) -> Union[str, bytes]:
        return yaml.dump(self.values(), Dumper=yaml.SafeDumper)

    def get_full_config_dirname(self) -> str:
        return os.path.join(self._user_home, JUMPAROUND_DIRNAME)

    def get_full_config_file_path(self) -> str:
        return os.path.join(self.get_full_config_dirname(), JUMPAROUND_CONFIG_NAME)

    def cache_file_path(self) -> str:
        return os.path.join(self.get_full_config_dirname(), self.cache_file)

    def search_include_paths(self) -> map:
        return map(
            lambda p: os.path.join(self._user_home, p),
            self.search_includes,
        )
