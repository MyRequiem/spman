#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# main.py file is part of spman

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
main.py
"""

import sys

from .helpmess import show_help_mess
from .maindata import MainData


class Main:
    """
    class Main
    """
    def __init__(self):
        # list of arguments
        # delete argument[0] (path and name of the script)
        self.args = sys.argv[1:]
        self.meta = MainData()
        self.repos = self.meta.get_repo_dict()
        self.commands = {
            '-h': self.show_help,
            '--help': self.show_help,
            '-v': self.check_version,
            '--check-version': self.check_version,
            '-l': self.show_repo_list,
            '--repolist': self.show_repo_list,
            '-r': self.show_info_repos,
            '--repoinfo': self.show_info_repos,
            '-b': self.show_blacklist,
            '--blacklist': self.show_blacklist,
            '-u': self.update,
            '--update': self.update,
            '-t': self.check_health,
            '--health': self.check_health,
            '-w': self.find_new_configs,
            '--new-config': self.find_new_configs,
            '-g': self.check_upgrade,
            '--check-upgrade': self.check_upgrade,
            '-d': self.download_pkg,
            '--download': self.download_pkg,
            '-q': self.processing_queue,
            '--queue': self.processing_queue,
            '-p': self.find_deps,
            '--find-deps': self.find_deps,
            '-s': self.view_slackbuild,
            '--view-slackbuild': self.view_slackbuild,
            '-f': self.find_pkg,
            '--find-pkg': self.find_pkg,
            '-k': self.checkdeps,
            '--check-deps': self.checkdeps,
            '-a': self.bad_links,
            '--bad-links': self.bad_links,
            '-i': self.pkglist,
            '--pkglist': self.pkglist
        }

    def start(self) -> None:
        """
        parse arguments and launch of the relevant options
        """
        # program is run without arguments
        if not self.args:
            show_help_mess('error')

        if self.args[0] in self.commands:
            # check exists dirs and files from /etc/spman/spman.conf
            args = ['-h',
                    '--help',
                    '-v',
                    '--check-version',
                    '-l',
                    '--repolist',
                    '-b',
                    '--blacklist',
                    '-u',
                    '--update',
                    '-t',
                    '--health',
                    '-w',
                    '--new-config',
                    '-k',
                    '--checkdeps',
                    '-a',
                    '--bad-links']
            if len(self.args) > 1 or self.args[0] not in args:
                from .majortests import MajorTests
                MajorTests().start()

            # run command
            self.commands[self.args[0]]()
        else:
            show_help_mess('error')

    def show_help(self) -> None:
        """
        show help message
        """
        if len(self.args) == 1:
            show_help_mess()
        else:
            show_help_mess('error')

    def show_repo_list(self) -> None:
        """
        show repo list from /etc/spman/repo-list
        """
        if len(self.args) > 1:
            show_help_mess('error')

        from .repolist import show_repo_list
        show_repo_list()

    def update(self) -> None:
        """
        Update PACKAGES.TXT, SLACKBUILDS.TXT and
        ChangeLog.txt for each repository
        """
        if len(self.args) > 1:
            show_help_mess('error')

        from .update import Update
        Update().start()

    def show_info_repos(self) -> None:
        """
        show information about all repositories.
        """
        if len(self.args) > 1:
            show_help_mess('error')

        from .showinforepos import ShowInfoRepos
        ShowInfoRepos().start()

    def check_version(self) -> None:
        """
        check program version
        """
        if len(self.args) > 1:
            show_help_mess('error')

        from .checkprgver import check_prg_ver
        check_prg_ver()

    def check_health(self) -> None:
        """
        Check health installed packages
        """
        if len(self.args) > 1:
            show_help_mess('error')

        from .checkhealth import CheckHealth
        CheckHealth().start()

    def find_new_configs(self) -> None:
        """
        Find all '*.new' files from /etc/ and /usr/share/ folders and subfolders
        """
        if len(self.args) > 1:
            show_help_mess('error')

        from .findnewconfigs import FindNewConfigs
        FindNewConfigs().start()

    def check_upgrade(self) -> None:
        """
        Check packages for upgrade
        """
        if len(self.args) > 1:
            show_help_mess('error')

        from .checkupgrade import CheckUpgrade
        CheckUpgrade().start()

    def show_blacklist(self) -> None:
        """
        Show blacklist
        """
        if len(self.args) > 1:
            show_help_mess('error')

        print(('Blacklisted packages in '
               '{0}{1}blacklist{2}:').format(self.meta.clrs['grey'],
                                             self.meta.configs_path,
                                             self.meta.clrs['reset']))
        for pkg in self.meta.get_blacklist():
            print('{0}{1}{2}'.format(self.meta.clrs['lred'],
                                     pkg,
                                     self.meta.clrs['reset']))

    def download_pkg(self) -> None:
        """
        Download package or source + SlackBuild script
        """
        if len(self.args) < 4:
            show_help_mess('error')

        # Examples:
        # spman --download --src sbo pkg1 pkg2 pkg3
        # spman -d --pkg alienbob pkg1 pkg2 pkg3
        mode = self.args[1]
        repo = self.args[2]
        pkglist = self.args[3:]

        if repo not in self.repos:
            show_help_mess(repo)

        if mode not in ['--src', '--pkg']:
            show_help_mess('error')

        if mode == '--pkg' and repo == 'sbo':
            print('Only SlackBuild script with source code\n'
                  'can be downloaded from \'sbo\' repository')
            show_help_mess('error')

        if mode == '--src' and repo == 'multilib':
            print('Only binary packages can be\ndownloaded '
                  'from \'multilib\' repository')
            show_help_mess('error')

        from .downloadpkg import DownloadPkg
        DownloadPkg(mode, repo, pkglist).start()

    def processing_queue(self) -> None:
        """
        processing queue for 'sbo' repository
        """
        repo = 'sbo'
        if repo not in self.repos:
            show_help_mess(repo)

        if len(self.args) < 2:
            show_help_mess('error')

        from .queue import Queue
        if len(self.args) == 2:
            if self.args[1] == '--clear':
                Queue().clear()
            elif self.args[1] == '--show':
                Queue().show()
            elif self.args[1] == '--install':
                Queue().install()
            else:
                show_help_mess('error')

        if len(self.args) > 2:
            pkgs = self.args[2:]
            if self.args[1] == '--add':
                Queue().add(pkgs)
            elif self.args[1] == '--remove':
                Queue().remove(pkgs)
            else:
                show_help_mess('error')

    def find_deps(self) -> None:
        """
        show list all dependencies for package from 'sbo' repository
        """
        repo = 'sbo'
        if repo not in self.repos:
            show_help_mess(repo)

        if len(self.args) != 2:
            show_help_mess('error')

        from .finddeps import FindDeps
        FindDeps().start(self.args[1])

    def view_slackbuild(self) -> None:
        """
        View README, slack-desc, doinst.sh and .SlackBuild
        files from sbo repository.
        """
        repo = 'sbo'
        if repo not in self.repos:
            show_help_mess(repo)

        if len(self.args) != 2:
            show_help_mess('error')

        from .viewslackbuild import ViewSlackBuild
        ViewSlackBuild(self.args[1]).start()

    def find_pkg(self) -> None:
        """
        Find package from each enabled repository and view info.
        """
        if len(self.args) != 2:
            show_help_mess('error')

        from .findpkg import FindPkg
        FindPkg(self.args[1]).start()

    def checkdeps(self) -> None:
        """
        Search dependency problems in the system packages
        using 'sbbdep' or 'ldd' tool.
        """

        if len(self.args) != 2 or self.args[1] not in ['--sbbdep', '--ldd']:
            show_help_mess('error')

        from .checkdeps import CheckDeps
        CheckDeps(self.args[1]).start()

    def bad_links(self) -> None:
        """
        find links to non-existent files/directories
        """
        if len(self.args) != 2:
            show_help_mess('error')

        from .badlinks import BadLinks
        BadLinks(self.args[1]).start()

    def pkglist(self) -> None:
        """
        Show complete list of the packages in the repository
        """
        arglen = len(self.args)
        if arglen != 2 and arglen != 3:
            show_help_mess('error')

        repo = self.args[1]
        if repo not in self.repos:
            show_help_mess(repo)

        only_installed = False
        if arglen == 3:
            if self.args[2] != '--only-installed':
                show_help_mess('error')

            only_installed = True

        from .pkglist import PkgList
        PkgList(repo, only_installed).start()
