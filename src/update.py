#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# update.py file is part of spman
#
# spman - Slackware package manager
# Home page: https://github.com/MyRequiem/spman
#
# Copyright (c) 2018 Vladimir MyRequiem Astrakhan, Russia
# <mrvladislavovich@gmail.com>
# All rights reserved
# See LICENSE for details.


"""
Update PACKAGES.TXT, SLACKBUILDS.TXT and
ChangeLog.txt for each repository
"""

from os import (
    path,
    remove,
    rename
)
from subprocess import call
from urllib.request import urlopen
from ssl import _create_unverified_context

from .maindata import MainData
from .utils import (
    get_line,
    download
)


class Update:
    """
    Update PACKAGES.TXT, SLACKBUILDS.TXT and
    ChangeLog.txt for each repository
    """
    def __init__(self):
        self.meta = MainData()
        self.spman_conf = self.meta.get_spman_conf()

    def start(self) -> None:
        """
        start update all local repository
        """
        # dict {'repo_name': 'url', ...}
        repos = self.meta.get_repo_dict()
        # machine architecture
        arch = 'x86_64' if self.meta.arch == 'x86_64' else 'x86'

        for repo in sorted(repos):
            # slackware version
            os_version = self.spman_conf['OS_VERSION']

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
                if os_version == 'current':
                    os_version = self.spman_conf['OS_LAST_RELEASE']

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
                dep_dir = ('slackware{0}'.format(arch_sl)
                           if os_version == 'current' else 'patches')

                repo_url = '{0}/{1}/{2}'.format(rep, dep_dir, repo_txt)

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

    def upd_and_show_diff(self, local_file: str,
                          file_url: str, prefix: str) -> None:
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

    def check_file_size(self, local: str, remote: str) -> bool:
        """
        check size local and remote ChangeLog.txt
        """
        return self.get_remote_file_size(remote) == path.getsize(local)

    @staticmethod
    def get_remote_file_size(remote: str) -> int:
        """
        get remote file size
        """
        filelen = 0
        _context = _create_unverified_context()
        c_length = urlopen(remote, context=_context).getheader('Content-Length')
        if c_length:
            filelen = int(c_length)

        return filelen
