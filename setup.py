#!/usr/bin/env python3

import sys
from setuptools import setup, find_packages, os

# Place the directory containing _version_git on the path
for path, _, filenames in os.walk(os.path.dirname(os.path.abspath(__file__))):
    if "_version_git.py" in filenames:
        sys.path.append(path)
        break

from _version_git import get_cmdclass, __version__

setup(
    cmdclass=get_cmdclass(),
    version=__version__
)

module_name = "test_versiongit"

install_reqs = [

]

develop_reqs = [
    "pytest",
    "mock",
    "black"
]

with open("README.rst", "rb") as f:
    long_description = f.read().decode("utf-8")

setup(
    name=module_name,
    version="0.1b1",
    python_requires=">=3.6",
    license="Apache",
    platforms=["Linux", "Windows", "Mac"],
    description="test versioingit versioning under Travis pypi deploy",
    packages=find_packages(exclude=("tests.*", "tests", "etc.*", "etc")),
    entry_points={
        "console_scripts": ["test versioingit = test_versioingit.main:main"]
        },
    long_description=long_description,
    install_requires=install_reqs,
    extras_require={"dev": develop_reqs},
    author="Giles Knap",
    author_email="giles.knap@diamond.ac.uk",
    url="https://github.com/dls-controls/test_versiongit",
)
