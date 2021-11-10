from jumparound.match import match_items


def test_match():
    list = [
        "/foo/bar/biz/baz",
        "/some/python/project",
        "/jumparound/project/path",
        "/a/b/c/d/f/g/e",
    ]

    matches = match_items("biz baz", list)

    assert len(matches) == 1
