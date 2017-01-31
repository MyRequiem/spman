#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# majortests.py file is part of spman

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
check exists dirs and files from /etc/spman/spman.conf
"""

from os import (
    path,
    makedirs
)

from .maindata import MainData


class MajorTests(object):
    """
    check exists dirs and files from /etc/spman/spman.conf
    """
    def __init__(self):
        self.meta = MainData()
        self.repos = self.meta.get_repo_dict()
        self.spman_conf = self.meta.get_spman_conf()

    def start(self):
        """
        start checks
        """
        self.check_exists_dirs()
        self.check_exists_libs()

    def check_exists_dirs(self):
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

    def check_exists_libs(self):
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
