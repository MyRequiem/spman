#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# main.py file is part of spman
#
# spman - Slackware package manager
# Home page: https://github.com/MyRequiem/spman
#
# Copyright (c) 2018 Vladimir MyRequiem Astrakhan, Russia
# <mrvladislavovich@gmail.com>
# All rights reserved
# See LICENSE for details.


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
            '-m': self.upgrade_pkgs,
            '--upgrade-pkgs': self.upgrade_pkgs,
            '-e': self.remove_pkgs,
            '--remove-pkgs': self.remove_pkgs,
            '-q': self.processing_queue,
            '--queue': self.processing_queue,
            '-y': self.history,
            '--history': self.history,
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
                    '-m',
                    '--upgrade-pkgs',
                    '-e',
                    '--remove-pkgs',
                    '-k',
                    '--checkdeps',
                    '-a',
                    '--bad-links']

            if self.args[0] not in args:
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

        # checking internet connection
        import socket
        """
        $ nmap 8.8.8.8
        ...
        Nmap scan report for google-public-dns-a.google.com (8.8.8.8)
        53/tcp  open  domain
        ...
        """
        host = '8.8.8.8'
        port = 53
        try:
            socket.setdefaulttimeout(3)
            socket.socket(socket.AF_INET,
                          socket.SOCK_STREAM).connect((host, port))

            from .update import Update
            Update().start()
        except Exception:
            print(('{0}No internet '
                   'connection !{1}').format(self.meta.clrs['red'],
                                             self.meta.clrs['reset']))

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

    def upgrade_pkgs(self) -> None:
        """
        upgrade packages in the current directory
        """
        num_args = len(self.args)
        if num_args > 2:
            show_help_mess('error')

        from .upgradepkgs import Upgradepkgs
        if num_args == 2:
            if self.args[1] != '--only-new':
                show_help_mess('error')
            else:
                Upgradepkgs(True).start()
        else:
            Upgradepkgs(False).start()

    def remove_pkgs(self) -> None:
        """
        remove packages in the current directory
        """
        if len(self.args) > 1:
            show_help_mess('error')

        from .removepkgs import Removepkgs
        Removepkgs().start()

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

    def history(self) -> None:
        """
        show/update package history
        """
        num_args = len(self.args)
        if num_args > 2:
            show_help_mess('error')

        from .history import History
        if num_args == 2:
            if self.args[1] != '--update':
                show_help_mess('error')
            else:
                History(True).start()
        else:
            History(False).start()

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
        num_args = len(self.args)
        if num_args < 2 or num_args > 3:
            show_help_mess('error')

        strict = False
        pkgname = self.args[1]
        if len(self.args) == 3:
            if self.args[1] != '--strict':
                show_help_mess('error')
            else:
                pkgname = self.args[2]
                strict = True

        from .findpkg import FindPkg
        FindPkg(strict, pkgname).start()

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
