#!/hint/python3

import re
import subprocess
from typing import Any, List
from os import getenv
import subprocess

from .gitutil import git_check_clean as git_check_clean  # Stop mypy complaining about implicit reexport
from .uiutil import run_txtcapture
from .gitutil import git_add as git_add # Stop mypy complaining about implicit reexport

# These are some regular expressions to validate and parse
# X.Y.Z[-rc.N] versions.
re_rc = re.compile(r'^([0-9]+)\.([0-9]+)\.([0-9]+)-rc\.([0-9]+)$')
re_ga = re.compile(r'^([0-9]+)\.([0-9]+)\.([0-9]+)$')
re_ea = re.compile(r'^([0-9]+)\.([0-9]+)\.([0-9]+)-ea$')
vX = 1
vY = 2
vZ = 3
vN = 4

DEFAULT_REPO = "emissary-ingress/emissary"


def base_version(release_version: str) -> str:
    """Given 'X.Y.Z[-rc.N]', return 'X.Y'."""
    return build_version(release_version).rsplit(sep='.', maxsplit=1)[0]


def build_version(release_version: str) -> str:
    """Given 'X.Y.Z[-rc.N]', return 'X.Y.Z'."""
    return release_version.split('-')[0]


def assert_eq(actual: Any, expected: Any) -> None:
    """`assert_eq(a, b)` is like `assert a == b`, but has a useful error
    message when they're not equal.
    """
    if actual != expected:
        raise AssertionError(f"wanted '{expected}', got '{actual}'")


def get_is_private() -> bool:
    """Return whether we're in a "private" Git checkout, for doing
    embargoed work.
    """
    remote_names = run_txtcapture(['git', 'remote']).split()
    remote_urls: List[str] = []
    for remote_name in remote_names:
        remote_urls += run_txtcapture(['git', 'remote', 'get-url', '--all', remote_name]).split()
    return 'private' in "\n".join(remote_urls)


def get_gh_repo() -> str:
    remote_url = run_txtcapture(['git', 'remote', 'get-url', 'origin']).strip()
    re_repo = re.compile(r'github\.com[:\/]([a-z\d-]+\/[a-z]+)(\.git)?$')
    m = re_repo.search(remote_url)
    if not m:
        raise Exception(f"Could not find repo from {remote_url}")
    return m[1]
