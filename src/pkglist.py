#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# pkglist.py file is part of spman

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
pkglist.py
"""

from .getrepodata import GetRepoData
from .maindata import MainData
from .pkgs import Pkgs


class PkgList:
    """
    Show complete list of the packages in the repository
    """
    def __init__(self, repo: str, only_installed: bool):
        self.repo = repo
        self.only_installed = only_installed
        self.pkgs = Pkgs()

    def start(self) -> None:
        """
        start show packages list
        """
        meta = MainData()
        rdata = GetRepoData(self.repo).start()

        for pkg in sorted(rdata['pkgs']):
            full_pkg_name = self.get_full_pkg_name(pkg)
            if full_pkg_name:
                print(('{0}{1}{2}-{3}'
                       '{4}').format(meta.clrs['lgreen'],
                                     pkg,
                                     meta.clrs['grey'],
                                     '-'.join(full_pkg_name.split('-')[-3:]),
                                     meta.clrs['reset']))
            elif not self.only_installed:
                print(pkg)

        print(('{0}Total packages in '
               'the repository:{2} {1}').format(meta.clrs['lyellow'],
                                                rdata['numpkgs'],
                                                meta.clrs['reset']))

    def get_full_pkg_name(self, pkg: str) -> str:
        """
        if package installed on the system return full
        name package, otherwise return blank string
        """
        return ''.join(self.pkgs.find_pkgs_on_system(pkg))
