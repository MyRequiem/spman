#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# utils.py file is part of spman

# Copyright 2016 MyRequiem <mrvladislavovich@gmail.com>
# All rights reserved

# spman - Slackware package manager
# Home page: https://github.com/MyRequiem/spman

# Spman is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""
Utils
"""

from shutil import rmtree

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
    print(('{0}Error!!! Package {1}\'{2}\' {0}not found in \'{3}\' '
           'repository.{4}').format(meta.clrs['red'],
                                    meta.clrs['cyan'],
                                    pkgname,
                                    reponame,
                                    meta.clrs['reset']))


def download(url: str, prefix: str, wgetparam: str='',
             show_process: bool=True) -> None:
    """
    download file/dir
    """
    from os import (
        path,
        remove
    )

    # download dir, not file
    downdir = True if wgetparam else False
    if downdir and not url.endswith('/'):
        url += '/'

    # name of download file or dir
    fname = url.split('/')[-2] if downdir else url.split('/')[-1]
    # full path to file or dir
    fpath = '{0}{1}'.format(prefix, fname)

    # remove file/dir if already exists
    if not downdir and path.isfile(fpath):
        remove(fpath)
    elif downdir and path.isdir(fpath):
        rmtree(fpath)

    meta = MainData()
    if show_process:
        string = 'directory' if downdir else 'file'
        print('{0}Downloading {1}:{2} {3}'.format(meta.clrs['lyellow'],
                                                  string,
                                                  meta.clrs['reset'],
                                                  url))
        print('{0}in {1}{2}'.format(meta.clrs['grey'],
                                    prefix,
                                    meta.clrs['reset']))

    from subprocess import call
    wgetprm = meta.get_spman_conf()['WGET_OPT'] if not downdir else wgetparam
    call('wget {0} --directory-prefix={1} {2}'.format(wgetprm,
                                                      prefix,
                                                      url),
         shell=True)

    if ((not downdir and not path.isfile(fpath)) or
            (downdir and not path.isdir(fpath))):
        print('{0}Failed download !!!{1}'.format(meta.clrs['red'],
                                                 meta.clrs['reset']))


def get_all_files(pathdir: str) -> list:
    """
    return list of all files in directory and subdirectories
    """
    from os import (
        path,
        walk
    )

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
    for root, dirs, files in walk(pathdir):
        del dirs
        for fls in files:
            allfiles.append(path.join(root, fls))

    return allfiles
