#!/usr/bin/env python3

import sys
from setuptools import setup, find_packages, os

module_name = "test_versiongit"

# Place the directory containing _version_git on the path
for path, _, filenames in os.walk(os.path.dirname(os.path.abspath(__file__))):
    if "_version_git.py" in filenames:
        sys.path.append(path)
        break

from _version_git import __version__, get_cmdclass  # noqa

install_reqs = [

]

develop_reqs = [
    "pytest",
    "mock",
    "black"

]

with open("README.rst", "rb") as f:
    long_description = f.read().decode("utf-8")

# packages = [x for x in find_packages() if not x.startswith("test")]
packages = find_packages()

setup(
    name=module_name,
    cmdclass=get_cmdclass(),
    version=__version__,
    python_requires=">=3.6",
    license="Apache",
    platforms=["Linux", "Windows", "Mac"],
    description="test versioingit versioning under Travis pypi deploy",
    packages=packages,
    entry_points={
        "console_scripts": ["hello = versiongit_test.main:main"]
        },
    long_description=long_description,
    install_requires=install_reqs,
    extras_require={"dev": develop_reqs},
    author="Giles Knap",
    author_email="giles.knap@diamond.ac.uk",
    url="https://github.com/dls-controls/test_versiongit",
)
