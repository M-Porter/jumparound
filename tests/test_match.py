from jumparound.analyzer import Project
from jumparound.match import match_items
from os.path import dirname, basename


def test_match():
    projects = list(
        map(
            lambda p: Project(path=p, name=basename(p), dirname=dirname(p)),
            [
                "/foo/bar/biz/baz",
                "/some/python/project",
                "/jumparound/project/path",
                "/a/b/c/d/f/g/e",
            ],
        )
    )

    matches = match_items("baz", projects)

    assert len(matches) == 1
