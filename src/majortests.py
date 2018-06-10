#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# majortests.py file is part of spman
#
# spman - Slackware package manager
# Home page: https://github.com/MyRequiem/spman
#
# Copyright (c) 2018 Vladimir MyRequiem Astrakhan, Russia
# <mrvladislavovich@gmail.com>
# All rights reserved
# See LICENSE for details.


"""
check exists dirs and files from /etc/spman/spman.conf
"""

from os import makedirs, path

from .maindata import MainData


class MajorTests:
    """
    check exists dirs and files from /etc/spman/spman.conf
    """
    def __init__(self):
        self.meta = MainData()
        self.repos = self.meta.get_repo_dict()
        self.spman_conf = self.meta.get_spman_conf()

    def start(self) -> None:
        """
        start checks
        """
        self.check_exists_dirs()
        self.check_exists_libs()
        self.check_exists_db()

    def check_exists_dirs(self) -> None:
        """
        check exists dirs
        """
        repo_logs = ['REPOS_PATH', 'LOGS_PATH']
        for opt_name in self.spman_conf:
            pth = self.spman_conf[opt_name]
            # if option is the path
            if pth.startswith('/'):
                # if path not exist
                if not path.exists(pth):
                    makedirs(pth)

                if opt_name in repo_logs:
                    for repo in self.repos:
                        repo_dir = pth + repo
                        if not path.exists(repo_dir):
                            makedirs(repo_dir)

                # queue file in queue dir
                if opt_name == 'QUEUE_PATH':
                    queue_file = pth + 'queue'
                    if not path.isfile(queue_file):
                        open(queue_file, 'w').close()

    def check_exists_libs(self) -> None:
        """
        check exists files
        """
        # if not exists PACKAGES.TXT, SLACKBUILDS.TXT or
        # ChangeLog.txt for one of the repositories
        repo_path = self.spman_conf['REPOS_PATH']
        logs_path = self.spman_conf['LOGS_PATH']
        for repo in self.repos:
            pkg_file = 'SLACKBUILDS.TXT' if repo == 'sbo' else 'PACKAGES.TXT'
            log_file = 'ChangeLog.txt'
            pkg_exist = path.isfile('{0}{1}/{2}'.format(repo_path,
                                                        repo,
                                                        pkg_file))
            log_exist = path.isfile('{0}{1}/{2}'.format(logs_path,
                                                        repo,
                                                        log_file))
            if not pkg_exist or not log_exist:
                print(('{0}For some repositories missing files PACKAGES.TXT, '
                       'SLACKBUILDS.txt or ChangeLog.txt\n{1}\'spman -u\' or '
                       '\'spman --update\' for update '
                       'libraries.{2}').format(self.meta.clrs['red'],
                                               self.meta.clrs['grey'],
                                               self.meta.clrs['reset']))
                raise SystemExit

    def check_exists_db(self) -> None:
        db_path = '{0}{1}'.format(self.spman_conf['REPOS_PATH'],
                                  self.meta.pkg_db_name)
        if not path.isfile(db_path):
            from .utils import update_pkg_db
            update_pkg_db(db_path)
