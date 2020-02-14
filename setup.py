#!/usr/bin/env python3

import sys
from setuptools import setup, find_packages
from pathlib import Path


module_name = "test_versiongit"

# Place the directory containing _version_git on the path
# for path, _, filenames in os.walk(os.path.dirname(os.path.abspath(__file__))):
#     if "_version_git.py" in filenames:
#         sys.path.append(path)
#         break
package_path = Path(__file__).parent / 'versiongit_test'

print("*******  Setup.py Checks *********")
print(f"adding {package_path} to sys.path")
file_list = package_path.parent.glob('**/*')
for f in file_list:
    print(" - {f}")


sys.path.append(str(package_path))

from _version_git import get_cmdclass, __version__  # noqa: E402

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
