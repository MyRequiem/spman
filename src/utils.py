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
    """
    Displaying the error message
    """
    meta = MainData()
    print(('{0}Can not open URL: {1} {2}{3}').format(meta.clrs['red'],
                                                     meta.clrs['lblue'],
                                                     url,
                                                     meta.clrs['reset']))


def url_is_alive(url: str) -> object:
    """
    Checks that a given URL is reachable
    """
    from ssl import _create_unverified_context
    from urllib.error import HTTPError, URLError
    from urllib.request import urlopen

    try:
        return urlopen(url, context=_create_unverified_context())
    except HTTPError:
        return False
    except URLError:
        return False


def get_remote_file_size(url: str = '', httpresponse: object = False) -> int:
    """
    Get the size of the remote file
    """
    need_to_close = False
    if not httpresponse:
        httpresponse = url_is_alive(url)
        if not httpresponse:
            error_open_mess(url)
            return 0
        need_to_close = True

    content_length = httpresponse.getheader('Content-Length')
    if need_to_close:
        httpresponse.close()

    return int(content_length) if content_length else 0


def get_md5_hash(file_path: str) -> str:
    """
    get md5sum of remote or local file
    """
    from hashlib import md5

    # local file
    if file_path.startswith('/'):
        return md5(open(file_path, 'rb').read()).hexdigest()

    # remote file
    httpresponse = url_is_alive(file_path)
    if not httpresponse:
        error_open_mess(file_path)
        return ''

    md5hash = md5()
    max_file_size = 100 * 1024 * 1024
    total_read = 0
    while True:
        data = httpresponse.read(4096)
        total_read += 4096

        if not data or total_read > max_file_size:
            break

        md5hash.update(data)

    httpresponse.close()
    return md5hash.hexdigest()


def check_md5sum(file1: str, file2: str) -> bool:
    """
    check md5sum of two files
    """
    return get_md5_hash(file1) == get_md5_hash(file2)


def check_internet_connection() -> bool:
    """
    checking Internet connection
    """
    meta = MainData()
    spman_conf = meta.get_spman_conf()
    host = spman_conf['TEST_CONNECTION_HOST']
    port = spman_conf['TEST_CONNECTION_PORT']

    try:
        port = int(port)
    except ValueError:
        print(('{0}{4}{5}.conf{3}: {1}port is not valid{2}\n'
               'TEST_CONNECTION_PORT={6}{3}').format(meta.clrs['cyan'],
                                                     meta.clrs['red'],
                                                     meta.clrs['grey'],
                                                     meta.clrs['reset'],
                                                     meta.configs_path,
                                                     meta.prog_name,
                                                     port))
        return False

    try:
        import socket
        sockt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sockt.settimeout(7)
        sockt.connect((host, port))
        sockt.shutdown(1)
        sockt.close()
        return True
    except socket.error:
        print(('{0}No internet connection!{1}\nIP address and port '
               'for verification: {3}{4}:{5}{1}\nCheck your internet '
               'connection and see parameters\n{2}TEST_CONNECTION_HOST{1} '
               'and {2}TEST_CONNECTION_PORT {1}in '
               '{6}{7}.conf{3}').format(meta.clrs['red'],
                                        meta.clrs['grey'],
                                        meta.clrs['cyan'],
                                        meta.clrs['reset'],
                                        host,
                                        port,
                                        meta.configs_path,
                                        meta.prog_name))
        return False
