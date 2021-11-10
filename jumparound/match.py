import re
from typing import List


def match_items(needle: str, haystack: List) -> List:
    r = ".*" + ".*".join(map(re.escape, needle.split())) + ".*"
    rf = re.IGNORECASE | re.UNICODE

    def search_func(x: str):
        return re.search(r, x, flags=rf)

    return list(filter(search_func, haystack))
