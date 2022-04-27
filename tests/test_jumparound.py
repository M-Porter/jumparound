import re

from src.jumparound import __version__


def test_version():
    with open("pyproject.toml", "r") as f:
        lines = f.read()
    matches = re.search('version = "([0-9]+\\.[0-9]+\\.[0-9]+)"', lines).groups()
    pyproject_version = matches[0]

    assert pyproject_version == "0.4.0"
    assert __version__ == "0.4.0"
