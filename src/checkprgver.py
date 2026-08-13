# checkprgver.py file is part of spman
#
# spman - Slackware package manager
# Home page: https://github.com/MyRequiem/spman
#
# Copyright (c) 2018 Vladimir MyRequiem Astrakhan, Russia
# <mrvladislavovich@gmail.com>
# All rights reserved
# See LICENSE for details.

"""Check program version."""

import re
from urllib.parse import urlparse

import requests

from .maindata import MainData


def check_prg_ver() -> None:
    """Check program version using requests and raw file parsing."""
    meta = MainData()
    local_ver = meta.prog_version

    print(
        f"Installed version: {local_ver}\n"
        f"{meta.clrs['grey']}Checking latest release version..."
        f"{meta.clrs['reset']}",
    )

    """
    Safely extract owner and repository name (e.g., 'MyRequiem/spman'). Works
    correctly even if home_page has a trailing slash:

    >>> home_page = "https://github.com/MyRequiem/spman"
    >>> urlparse(home_page)
    ParseResult(..., path='/MyRequiem/spman', ...)
    >>> urlparse(home_page).path
    '/MyRequiem/spman'
    >>> urlparse(home_page).path.strip("/")
    'MyRequiem/spman'
    """
    repo_path = urlparse(meta.home_page).path.strip("/")

    raw_url = (
        f"https://raw.githubusercontent.com/{repo_path}"
        f"/refs/heads/master/src/maindata.py"
    )

    try:
        response = requests.get(raw_url, timeout=10)
        # Raises an exception on 404, 500, or other HTTP errors.
        response.raise_for_status()
        remote_text = response.text
    except requests.RequestException as e:
        print(
            f"{meta.clrs['lred']}Error checking version: "
            f"{e}{meta.clrs['reset']}",
        )
        return

    match = re.search(
        r"self\.prog_version\s*=\s*['\"]([^'\"]+)['\"]",
        remote_text,
    )

    if not match:
        print(
            f"{meta.clrs['lred']}Error checking version: "
            f"self.prog_version not found in remote file{meta.clrs['reset']}",
        )

        return

    version = match.group(1)

    if version != local_ver:
        print(
            f"{meta.clrs['lred']}New version is available:"
            f"{meta.clrs['reset']} {version}\n"
            f"Visit: {meta.home_page}/releases\n"
            f"Or download new version source code:\n"
            f"{meta.home_page}/archive/"
            f"{version}/{meta.prog_name}-{version}.tar.gz",
        )
    else:
        print(
            f"{meta.clrs['green']}You are using the latest program version."
            f"{meta.clrs['reset']}",
        )
