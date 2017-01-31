#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# update.py file is part of spman

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
Update PACKAGES.TXT, SLACKBUILDS.TXT and
ChangeLog.txt for each repository
"""

from os import (
    path,
    remove,
    rename
)
from ssl import _create_unverified_context
from subprocess import call
from urllib.request import urlopen

from .maindata import MainData
from .utils import (
    get_line,
    download
)


class Update(object):
    """
    Update PACKAGES.TXT, SLACKBUILDS.TXT and
    ChangeLog.txt for each repository
    """
    def __init__(self):
        self.meta = MainData()
        self.spman_conf = self.meta.get_spman_conf()

    def start(self):
        """
        start update all local repository
        """
        # dict {'repo_name': 'url', ...}
        repos = self.meta.get_repo_dict()
        # slackware version
        os_version = self.meta.get_os_version()
        # machine architecture
        arch = 'x86_64' if self.meta.arch == 'x86_64' else 'x86'

        for repo in sorted(repos):
            print(('\n{0}{4}\n+ Update repository:{1} '
                   '{2}{3}\n{0}{4}{3}').format(self.meta.clrs['yellow'],
                                               self.meta.clrs['cyan'],
                                               repo,
                                               self.meta.clrs['reset'],
                                               get_line('+', 80)))
            # repo file name
            repo_txt = 'SLACKBUILDS.TXT' if repo == 'sbo' else 'PACKAGES.TXT'
            # full path to local repo file
            repo_file = '{0}{1}/{2}'.format(self.spman_conf['REPOS_PATH'],
                                            repo,
                                            repo_txt)
            # log file name
            log_txt = 'ChangeLog.txt'
            # full path to local log file
            log_file = '{0}{1}/{2}'.format(self.spman_conf['LOGS_PATH'],
                                           repo,
                                           log_txt)

            # URL's for remote logs and repo files
            if repo == 'alienbob':
                log_url = '{0}{1}'.format(repos[repo], log_txt)
                repo_url = '{0}{1}/{2}/{3}'.format(repos[repo],
                                                   os_version,
                                                   arch,
                                                   repo_txt)
            elif repo == 'multilib':
                log_url = '{0}{1}'.format(repos[repo], log_txt)
                repo_url = '{0}{1}/{2}'.format(repos[repo],
                                               os_version,
                                               repo_txt)
            elif repo == 'sbo':
                log_url = '{0}{1}/{2}'.format(repos[repo],
                                              os_version,
                                              log_txt)
                repo_url = '{0}{1}/{2}'.format(repos[repo],
                                               os_version,
                                               repo_txt)
            else:
                arch_sl = '64' if self.meta.arch == 'x86_64' else ''
                rep = '{0}slackware{1}-{2}'.format(repos[repo],
                                                   arch_sl,
                                                   os_version)
                log_url = '{0}/{1}'.format(rep, log_txt)
                repo_url = '{0}/patches/{1}'.format(rep, repo_txt)

            print('{0}Wait...{1}'.format(self.meta.clrs['grey'],
                                         self.meta.clrs['reset']))

            template = '{0}{1}/'

            # download PACKAGES.TXT/SLACKBUILDS.TXT if not exist,
            repo_downloaded = False
            prefix_repo = template.format(self.spman_conf['REPOS_PATH'], repo)
            if not path.isfile(repo_file):
                download(repo_url, prefix_repo)
                repo_downloaded = True

            # download ChangeLog.txt if not exist
            log_downloaded = False
            prefix_log = template.format(self.spman_conf['LOGS_PATH'], repo)
            if not path.isfile(log_file):
                download(log_url, prefix_log)
                log_downloaded = True

            if not repo_downloaded or not log_downloaded:
                if (not self.check_file_size(repo_file, repo_url) or
                        not self.check_file_size(log_file, log_url)):
                    # if repository multilib show diff PACKAGES.TXT
                    # otherwise show diff ChangeLog.txt
                    if repo == 'multilib':
                        download(log_url, prefix_log)
                        self.upd_and_show_diff(repo_file, repo_url, prefix_repo)
                    else:
                        self.upd_and_show_diff(log_file, log_url, prefix_log)
                        download(repo_url, prefix_repo)

            print('{0}Done{1}'.format(self.meta.clrs['grey'],
                                      self.meta.clrs['reset']))
        print()

    def upd_and_show_diff(self, local_file, file_url, prefix):
        """
        update file and show diff with old file
        """
        # rename local_file --> local_file_old
        old_file = '{0}_old'.format(local_file)
        rename(local_file, old_file)
        # download new file
        download(file_url, prefix)
        # show diff
        print('\n{0}Diff:{1}{2}'.format(self.meta.clrs['lmagenta'],
                                        self.meta.clrs['reset'],
                                        self.meta.clrs['green']))
        call(('diff -U 0 {0}_old {0} | grep -v @@ | '
              'grep -vE "\\-\\-\\-" | '
              'grep -vE "\\+\\+\\+"').format(local_file),
             shell=True)
        # delete odl file
        remove(old_file)
        print()

    def check_file_size(self, local, remote):
        """
        check size local and remote ChangeLog.txt
        """
        equal = self.get_remote_file_size(remote) == path.getsize(local)
        return equal

    @staticmethod
    def get_remote_file_size(remote):
        """
        get remote file size
        """
        filelen = 0
        _context = _create_unverified_context()
        c_length = urlopen(remote, context=_context).getheader('Content-Length')
        if c_length:
            filelen = int(c_length)

        return filelen
