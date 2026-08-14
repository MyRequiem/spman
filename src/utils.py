#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# utils.py file is part of spman
#
# spman - Slackware package manager
# Home page: https://github.com/MyRequiem/spman
#
# Copyright (c) 2018 Vladimir MyRequiem Astrakhan, Russia
# <mrvladislavovich@gmail.com>
# All rights reserved
# See LICENSE for details.


"""
Utils
"""

from __future__ import annotations

import requests

from .maindata import MainData


def get_line(char: str, length: int) -> str:
    """
    return string
    """
    return char * length


def get_indent(width1: int, width2: int) -> str:
    """
    get space indent for format print
    """
    return ' ' * (width2 - width1)


def pkg_not_found_mess(pkgname: str, reponame: str) -> None:
    """
    print message if package not found in repository
    """
    meta = MainData()
    print(('{0}Package {1}{2} {0}not found in \'{3}\' '
           'repository.{4}').format(meta.clrs['lred'],
                                    meta.clrs['lcyan'],
                                    pkgname,
                                    reponame,
                                    meta.clrs['reset']))


def get_all_files(pathdir: str) -> list:
    """
    return list of all files in directory and subdirectories
    """
    from os import path, walk

    '''
    os.walk(root_path) - directory tree generator.
    For each directory on root_path return a tuple:
    (path_for_dir, list_dirs_on_the_dir, list_files_on_the_dir)

    trash
    ├── dir1
    │   ├── dir2
    │   │   ├── dir3
    │   │   └── file3
    │   ├── file1
    │   └── file2
    └── dir4
        ├── dir5
        │   ├── file5
        │   └── file6
        └── file4

    >>> import os
    >>> list(os.walk('/home/myrequiem/trash'))
    [
        ('trash', ['dir1', 'dir4'], []),
        ('trash/dir1', ['dir2'], ['file2', 'file1']),
        ('trash/dir1/dir2', ['dir3'], ['file3']),
        ('trash/dir1/dir2/dir3', [], []),
        ('trash/dir4', ['dir5'], ['file4']),
        ('trash/dir4/dir5', [], ['file5', 'file6'])
    ]
    '''

    allfiles = []

    try:
        from tqdm import tqdm
    except ImportError:
        def tqdm(*args, **kwargs):
            if args:
                return args[0]
            return kwargs.get('iterable', None)

    for root, dirs, files in tqdm(walk(pathdir), leave=False,
                                  ncols=80, unit=''):
        del dirs
        for fls in files:
            allfiles.append(path.join(root, fls))

    return allfiles


def get_packages_in_current_dir() -> list:
    """
    return list of packages in the current directory
    """
    from os import listdir

    pkgs = []
    ext = ('.tgz', '.txz')
    for file_in_current_dir in sorted(listdir()):
        if file_in_current_dir.endswith(ext):
            pkgs.append(file_in_current_dir)

    return pkgs


def update_pkg_db(db_path: str = '') -> None:
    """
    update package database
    """
    meta = MainData()
    spman_conf = meta.get_spman_conf()
    db_path_exists = db_path
    if not db_path_exists:
        db_path = '{0}{1}'.format(spman_conf['REPOS_PATH'], meta.pkg_db_name)

    # create a backup of the database
    if not db_path_exists:
        from shutil import copy2
        db_path_backup = '{0}~'.format(db_path)
        copy2(db_path, db_path_backup)
        print('A backup was created: {0}'.format(db_path_backup))

    # write current time in db file
    from datetime import datetime
    date_now = datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S")
    pkgdb = open(db_path, 'w')
    pkgdb.write('Last database update: {0} UTC\n'.format(date_now))
    pkgdb.close()

    from .pkgs import Pkgs
    pkgdb = open(db_path, 'a')
    for pkg in Pkgs().find_pkgs_on_system():
        pkgdb.write('{0}\n'.format(pkg.strip()))
    pkgdb.close()


def error_open_mess(url: str) -> None:
    """Display an error message when a URL cannot be opened."""
    meta = MainData()
    print(
        f"{meta.clrs['lred']}Can not open URL: "
        f"{meta.clrs['lblue']}{url}{meta.clrs['reset']}" # noqa: COM812
    )


def url_is_alive(url: str) -> requests.Response | bool:
    """Check if the given URL is reachable and returns the response object."""
    try:
        # Use stream=True
        # to only fetch headers first without downloading the body.
        response = requests.get(url, stream=True, timeout=10)
        # Raise an exception for HTTP errors (4xx or 5xx status codes).
        response.raise_for_status()
    except requests.RequestException:
        return False

    return response


def get_remote_file_size(
    url: str = "",
    response: requests.Response | None = None,
) -> int:
    """Retrieve the content length of a remote file in bytes."""
    # If no active response is provided, check if the URL is reachable.
    if response is None:
        active_resp = url_is_alive(url)
        if not active_resp:
            error_open_mess(url)
            return 0
    else:
        active_resp = response

    # Extract Content-Length safely from requests headers dict.
    content_length = active_resp.headers.get("Content-Length")

    return int(content_length) if content_length else 0


def get_remote_md5(url: str) -> str:
    """Calculate the MD5 hash of a remote file using chunked streaming."""
    from hashlib import md5

    response = url_is_alive(url)
    if not response or not isinstance(response, requests.Response):
        error_open_mess(url)
        return ""

    md5hash = md5() # noqa: S324
    max_file_size = 100 * 1024 * 1024
    total_read = 0
    size_chunk = 4096

    # Iterate over stream chunks safely using requests.
    for chunk in response.iter_content(chunk_size=size_chunk):
        if not chunk:
            break

        md5hash.update(chunk)
        total_read += len(chunk)

        if total_read > max_file_size:
            break

    return md5hash.hexdigest()


def get_md5_hash(file_path: str) -> str:
    """Calculate the MD5 hash of a local or remote file."""
    from hashlib import md5
    from pathlib import Path

    # Local file handling using clean pathlib syntax.
    if file_path.startswith("/"):
        path_obj = Path(file_path)
        if not path_obj.is_file():
            return ""
        return md5(path_obj.read_bytes()).hexdigest() # noqa: S324

    # Remote file handling delegated to a specialized helper
    return get_remote_md5(file_path)


def check_md5sum(file1: str, file2: str) -> bool:
    """
    check md5sum of two files
    """
    return get_md5_hash(file1) == get_md5_hash(file2)
