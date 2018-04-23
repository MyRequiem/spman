#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# findpkg.py file is part of spman
#
# spman - Slackware package manager
# Home page: https://github.com/MyRequiem/spman
#
# Copyright (c) 2018 Vladimir MyRequiem Astrakhan, Russia
# <mrvladislavovich@gmail.com>
# All rights reserved
# See LICENSE for details.


"""
Find package from each enabled repository and view info.
"""

from .getrepodata import GetRepoData
from .maindata import MainData


class FindPkg:
    """
    Find package from each enabled repository and view info.
    """
    def __init__(self, strict: bool, pkgname: str):
        self.meta = MainData()
        self.repos = self.meta.get_repo_dict()
        self.strict = strict
        self.pkgname = pkgname
        if not self.strict:
            self.pkgname = self.pkgname.lower()
        self.repo = ''

    def start(self) -> None:
        """
        Find package from each enabled repository and view info.
        """
        pkg_is_found = False
        for repo in sorted(self.repos):
            repodata = GetRepoData(repo).start()
            self.repo = repo
            if self.strict:
                if self.pkgname in repodata['pkgs']:
                    self.print_info(repodata['pkgs'], self.pkgname)
                    pkg_is_found = True
            else:
                all_pkg_names = list(repodata['pkgs'].keys())
                for pkg_name in all_pkg_names:
                    if self.pkgname in pkg_name.lower():
                        self.print_info(repodata['pkgs'], pkg_name)
                        pkg_is_found = True

        if not pkg_is_found:
            print(('Package {0}\'{1}\'{2} not '
                   'found.').format(self.meta.clrs['lcyan'],
                                    self.pkgname,
                                    self.meta.clrs['reset']))

    def print_info(self, pkgdict: dict, pkgname: str) -> None:
        """
        print package info
        """
        pkgdata = pkgdict[pkgname]
        sbo = True if self.repo == 'sbo' else False
        self.print_data('Package name: ', pkgname, 'yellow')
        self.print_data('Repository: ', self.repo, 'lcyan')
        version = pkgdata[0] if sbo else pkgdata[0][1]
        self.print_data('Version: ', version)
        if sbo or self.repo == 'multilib' and pkgdata[1]:
            self.print_data('Location: ', pkgdata[1])
        if not sbo:
            self.print_data('Compressed size: ', pkgdata[2])
            self.print_data('Uncompressed size: ', pkgdata[3])
        if sbo or self.repo == 'alienbob':
            list_deps = ', '.join(pkgdata[4])
            if not list_deps:
                list_deps = '---'
            self.print_data('Package dependencies: ', list_deps, 'grey')
        print('Description:')
        for line in pkgdata[5]:
            print('{0}{1}{2}'.format(self.meta.clrs['green'],
                                     line,
                                     self.meta.clrs['reset']))
        print()

    def print_data(self, dataname: str, data: str,
                   color: str = 'reset') -> None:
        """
        print data string
        """
        from .utils import get_indent
        print('{0}{1}{2}{3}{4}'.format(dataname,
                                       get_indent(len(dataname), 23),
                                       self.meta.clrs[color],
                                       data,
                                       self.meta.clrs['reset']))
