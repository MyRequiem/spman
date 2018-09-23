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

from difflib import unified_diff
from os import path, remove, rename

from .download import Download
from .maindata import MainData
from .utils import check_md5sum, get_line


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

            # download PACKAGES.TXT/SLACKBUILDS.TXT if not exist,
            repo_downloaded = False
            dest_repo = '{0}{1}/'.format(self.spman_conf['REPOS_PATH'], repo)
            if not path.isfile(repo_file):
                self.show_download_mess(repo_txt)
                Download(repo_url, dest_repo).start()
                repo_downloaded = True

            # download ChangeLog.txt if not exist
            log_downloaded = False
            dest_log = '{0}{1}/'.format(self.spman_conf['LOGS_PATH'], repo)
            if not path.isfile(log_file):
                self.show_download_mess(log_txt)
                Download(log_url, dest_log).start()
                log_downloaded = True

            if not repo_downloaded or not log_downloaded:
                print(('{0}Comparison of remote and '
                       'local log{1}').format(self.meta.clrs['grey'],
                                              self.meta.clrs['reset']))

                if (not check_md5sum(repo_file, repo_url) or
                        not check_md5sum(log_file, log_url)):
                    # if repository == 'multilib' show diff PACKAGES.TXT
                    # otherwise show diff ChangeLog.txt
                    if repo == 'multilib':
                        self.show_download_mess(log_txt)
                        Download(log_url, dest_log, True).start()
                        self.download_and_show_diff(repo_file,
                                                    repo_url,
                                                    dest_repo)
                    else:
                        self.show_download_mess(repo_txt)
                        Download(repo_url, dest_repo, True).start()
                        self.download_and_show_diff(log_file,
                                                    log_url,
                                                    dest_log)
                else:
                    print('{0}No updates{1}'.format(self.meta.clrs['grey'],
                                                    self.meta.clrs['reset']))

            # ALL-PACKAGES.TXT for repository 'slack'
            if repo == 'slack':
                all_repo_txt = 'ALL-' + repo_txt
                repo_file = repo_file.replace(repo_txt, all_repo_txt)
                repo_url = '{0}/{1}'.format(rep, repo_txt)
                if (not path.isfile(repo_file) or
                        not check_md5sum(repo_file, repo_url)):
                    print(('{0}Downloading {1} for all '
                           'repository{2}').format(self.meta.clrs['grey'],
                                                   repo_txt,
                                                   self.meta.clrs['reset']))
                    Download(repo_url, dest_repo, True, all_repo_txt).start()

        print()

    def download_and_show_diff(self,
                               file_path: str,
                               remote_url: str,
                               dest: str) -> None:
        """
        update file and show diff with old file
        """
        # rename old file
        old_file = '{0}_old'.format(file_path)
        try:
            rename(file_path, old_file)
        except FileNotFoundError:
            return

        # download new file
        self.show_download_mess(path.basename(file_path))
        Download(remote_url, dest, True).start()
        if not path.isfile(file_path):
            remove(old_file)
            return

        # show diff
        print('\n{0}Diff:{1}'.format(self.meta.clrs['lmagenta'],
                                     self.meta.clrs['reset']))

        with open(old_file, 'r', errors='replace') as file_old:
            with open(file_path, 'r', errors='replace') as file_new:
                diff = unified_diff(file_old.readlines(),
                                    file_new.readlines(),
                                    fromfile='file_old',
                                    tofile='file_new',
                                    n=0)
                for line in diff:
                    if line.startswith('+++') or line.startswith('---'):
                        continue

                    color = 'green'
                    if '/multilib/' in file_path:
                        if 'PACKAGE NAME:' in line:
                            if line.startswith('-'):
                                color = 'red'
                            print('{0}{1}{2}'.format(self.meta.clrs[color],
                                                     line,
                                                     self.meta.clrs['reset']),
                                  end='')
                    elif line.startswith('+'):
                        print('{0}{1}{2}'.format(self.meta.clrs[color],
                                                 line,
                                                 self.meta.clrs['reset']),
                              end='')

        if not file_old.closed:
            file_old.close()
        if not file_new.closed:
            file_new.close()

        remove(old_file)

    def show_download_mess(self, mess: str) -> None:
        print(('{0}Downloading {1}{2}').format(self.meta.clrs['grey'],
                                               mess,
                                               self.meta.clrs['reset']))
