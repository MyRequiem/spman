#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# finddeps.py file is part of spman

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
Show list all dependencies for package from 'sbo' repository
"""

from sys import setrecursionlimit

from .getrepodata import GetRepoData
from .maindata import MainData


class FindDeps(object):
    """
    Show list all dependencies for package from 'sbo' repository
    """
    def __init__(self):
        self.meta = MainData()
        self.sbodata = GetRepoData('sbo').start()
        self.alldeps = []

    def start(self, pkgname):
        """
        find all deps for package
        """
        if pkgname not in self.sbodata['pkgs']:
            from .utils import pkg_not_found_mess
            pkg_not_found_mess(pkgname, 'sbo')
            raise SystemExit

        self.get_all_deps(pkgname)
        if not self.alldeps:
            print(('Package {0}\'{1}\'{2} has no '
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

    def get_deps(self, pkgname):
        """
        return list of dependencies for package
        """
        return self.sbodata['pkgs'][pkgname][4]

    def get_all_deps(self, pkgname):
        """
        create list of the dependencies list for each package
        """
        setrecursionlimit(7000)
        deps = self.get_deps(pkgname)
        if deps:
            self.alldeps.append(deps)
            for dep in deps:
                self.get_all_deps(dep)

    def print_deps_list(self, deps):
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
