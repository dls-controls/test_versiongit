import os
import re
from subprocess import STDOUT, check_output

# These will be filled in if git archive is run
GIT_ARCHIVE_REF_NAMES = "$Format:%D$"
GIT_ARCHIVE_HASH = "$Format:%h$"

# This will be filled in by cmdclasses passed to setup.py
VERSION_STATIC = None


def get_version_from_git(path=None):
    """Try to parse version from git describe, fallback to git archive tags"""
    if path is None:
        # If no path to git repo, choose the directory this file is in
        path = os.path.dirname(os.path.abspath(__file__))
    tag, plus, sha1, dirty, error = "0", "unknown", "error", "", None
    if not GIT_ARCHIVE_HASH.startswith("$"):
        # git archive has written a sha1 for us to use
        sha1 = GIT_ARCHIVE_HASH
        for ref_name in GIT_ARCHIVE_REF_NAMES.split(", "):
            if ref_name.startswith("tag: "):
                # On a git archive tag
                tag, plus = ref_name[5:], "0"
    else:
        git_cmd = "git -C %s describe --tags --dirty --always --long" % path
        # output is TAG-NUM-gHEX[-dirty] or HEX[-dirty]
        try:
            out = check_output(git_cmd.split(), stderr=STDOUT).decode().strip()
        except Exception as e:
            error = e
        else:
            if out.endswith("-dirty"):
                out = out[:-6]
                dirty = ".dirty"
            if "-" in out:
                # There is a tag, extract it and the other pieces
                match = re.search(r"^(.+)-(\d+)-g([0-9a-f]+)$", out)
                tag, plus, sha1 = match.groups()
            else:
                # No tag, just sha1
                plus, sha1 = "untagged", out
    # Replace dashes in tag for dots
    # Remove this line when we stop supporting python 2.7
    tag = tag.replace("-", ".")
    if plus != "0" or dirty:
        # Not on a tag, add additional info
        tag = "%(tag)s+%(plus)s.%(sha1)s%(dirty)s" % locals()
    return tag, error, sha1


if VERSION_STATIC:
    __version__, git_error, git_sha1 = VERSION_STATIC, None, None
else:
    __version__, git_error, git_sha1 = get_version_from_git()


def get_cmdclass(build_py=None, sdist=None):
    """Create cmdclass dict to pass to setuptools.setup that will write a
    _version_static.py file in our resultant sdist, wheel or egg"""
    if build_py is None:
        from setuptools.command.build_py import build_py
    if sdist is None:
        from setuptools.command.sdist import sdist

    def make_version_static(base_dir, pkg):
        vg = os.path.join(base_dir, pkg.split(".")[0], "_version_git.py")
        # Replace VERSION_STATIC in _version_git.py
        if os.path.isfile(vg):
            text = open(vg).read()
            open(vg, "w").write(
                text.replace(
                    "\nVERSION_STATIC = None", "\nVERSION_STATIC = %r" % __version__
                )
            )

    class BuildPy(build_py):
        def run(self):
            build_py.run(self)
            for pkg in self.packages:
                make_version_static(self.build_lib, pkg)

    class Sdist(sdist):
        def make_release_tree(self, base_dir, files):
            sdist.make_release_tree(self, base_dir, files)
            for pkg in self.distribution.packages:
                make_version_static(base_dir, pkg)

    return dict(build_py=BuildPy, sdist=Sdist)
