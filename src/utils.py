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
    print(('{0}Package {1}{2} {0}not found in \'{3}\' '
           'repository.{4}').format(meta.clrs['red'],
                                    meta.clrs['lcyan'],
                                    pkgname,
                                    reponame,
                                    meta.clrs['reset']))


def download(url: str, prefix: str, wgetparam: str = '',
             show_process: bool = True) -> None:
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

    try:
        from tqdm import tqdm
    except ImportError:
        def tqdm(*args):
            return args[0]

    for root, dirs, files in tqdm(walk(pathdir)):
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
