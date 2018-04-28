#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# finddeps.py file is part of spman
#
# spman - Slackware package manager
# Home page: https://github.com/MyRequiem/spman
#
# Copyright (c) 2018 Vladimir MyRequiem Astrakhan, Russia
# <mrvladislavovich@gmail.com>
# All rights reserved
# See LICENSE for details.


"""
Show list all dependencies for package from 'sbo' repository
"""

from sys import setrecursionlimit

from .getrepodata import GetRepoData
from .maindata import MainData


class FindDeps:
    """
    Show list all dependencies for package from 'sbo' repository
    """
    def __init__(self):
        self.meta = MainData()
        self.sbodata = GetRepoData('sbo').start()
        self.alldeps = []

    def start(self, pkgname: str) -> None:
        """
        find all deps for package
        """
        if pkgname not in self.sbodata['pkgs']:
            from .utils import pkg_not_found_mess
            pkg_not_found_mess(pkgname, 'sbo')
            raise SystemExit

        self.get_all_deps(pkgname)
        if not self.alldeps:
            print(('Package {0}{1}{2} has no '
                   'dependencies.').format(self.meta.clrs['cyan'],
                                           pkgname,
                                           self.meta.clrs['reset']))
            raise SystemExit

        self.alldeps.reverse()
        # create a single list
        # >>> l = []
        # >>> l1 = [[1, 2], [3, 4], [5, 6]]
        # >>> for lst in l1:
        #       l += lst
        # >>> l
        # [1, 2, 3, 4, 5, 6]
        single_list = []
        for lst in self.alldeps:
            single_list += lst

        # remove duplicate packages from list
        no_dupl = []
        for pkg in single_list:
            if pkg not in no_dupl:
                no_dupl.append(pkg)

        self.print_deps_list(no_dupl)

    def get_deps(self, pkgname: str) -> list:
        """
        return list of dependencies for package
        """
        return self.sbodata['pkgs'][pkgname][4]

    def get_all_deps(self, pkgname: str) -> None:
        """
        create list of the dependencies list for each package
        """
        setrecursionlimit(7000)
        deps = self.get_deps(pkgname)
        if deps:
            self.alldeps.append(deps)
            for dep in deps:
                self.get_all_deps(dep)

    def print_deps_list(self, deps: list) -> None:
        """
        print dependencies list
        """
        from .pkgs import Pkgs
        from .utils import get_indent

        num = 1
        pkgs = Pkgs()
        for dep in deps:
            color = 'lred'
            if pkgs.find_pkgs_on_system(dep):
                color = 'lgreen'
            print('{0}.{1}{2}{3}{4}'.format(num,
                                            get_indent(len(str(num)) + 1, 4),
                                            self.meta.clrs[color],
                                            dep,
                                            self.meta.clrs['reset']))
            num += 1
