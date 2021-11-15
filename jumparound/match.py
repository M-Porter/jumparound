import re
from typing import List

from .analyzer import Project


def match_items(needle: str, haystack: List[Project]) -> List:
    r = ".*" + ".*".join(map(re.escape, needle.split())) + ".*"
    rf = re.IGNORECASE | re.UNICODE

    def search_func(p: Project):
        return re.search(r, p.name, flags=rf)

    return list(filter(search_func, haystack))
