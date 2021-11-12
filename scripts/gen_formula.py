#!/usr/bin/env python3

import re
import subprocess
from string import Template

import requests
from bs4 import BeautifulSoup

resource_template = Template(
    """resource \"$name\" do
  url "$url"
  sha256 "$sha256"
end
"""
)


def gen_formula():
    requirements = subprocess.check_output(
        ["poetry", "export", "--without-hashes"]
    ).decode("utf-8")

    for line in requirements.splitlines():
        requirements = str(line).split(";", 1)[0]
        [name, version] = requirements.split("==", 1)
        pkg_url = f"https://pypi.org/project/{name}/{version}/"
        r = requests.get(f"{pkg_url}#files")

        soup = BeautifulSoup(r.text, features="html.parser")
        s = soup.body.find(text=re.compile(re.escape(f"{name}-{version}.tar.gz")))
        if not s:
            continue
        dep_url = s.parent["href"]

        dep_hash = None
        for link in s.parent.parent.parent.findAll("a"):
            if "hash" in link["href"]:
                rr = requests.get(pkg_url + link["href"])
                good_soup = BeautifulSoup(rr.text, features="html.parser")
                ss = good_soup.body.find(text=re.compile(re.escape("SHA256")))
                dep_hash = ss.parent.parent.find("code").text

        if dep_hash and dep_url:
            d = {
                "name": name,
                "url": dep_url,
                "sha256": dep_hash,
            }
            print(resource_template.substitute(d))


if __name__ == "__main__":
    gen_formula()
