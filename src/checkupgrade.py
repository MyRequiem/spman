#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# checkupgrade.py file is part of spman

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
Check packages for upgrade
"""

from .getrepodata import GetRepoData
from .maindata import MainData
from .pkgs import Pkgs
from .utils import get_indent


class CheckUpgrade:
    """
    Check packages for upgrade
    """
    def __init__(self):
        self.meta = MainData()
        self.pkgs = Pkgs()
        self.blacklist = self.meta.get_blacklist()
        self.repos = ['alienbob', 'sbo', 'multilib', 'slack']
        self.reposdata = [{}, {}, {}, {}]
        self.upgrpkgs = [[], [], [], []]

    def start(self) -> None:
        """
        start check packages for upgrade
        """
        self.get_repos_data()

        for pkg in self.pkgs.find_pkgs_on_system():
            parts = self.pkgs.get_parts_pkg_name(pkg)
            if parts[0] not in self.blacklist:
                # gcc-5.3.0_multilib-x86_64-3alien --> multilib
                # compat32-tools-3.7-noarch-1alien --> multilib
                # mozilla-firefox-l10n-ru-45.2.0-x86_64-1alien

                # alienbob
                if (self.reposdata[0] and
                        'alien' in parts[3] and
                        'multilib' not in parts[1] and
                        parts[0] != 'compat32-tools'):
                    self.check_pkg(parts, 0)
                # sbo
                elif self.reposdata[1] and 'SBo' in parts[3]:
                    self.check_pkg(parts, 1)
                # multilib
                elif self.reposdata[2] and ('compat32' in parts[3] or
                                            parts[0] == 'compat32-tools' or
                                            'multilib' in parts[1]):
                    self.check_pkg(parts, 2)
                # slack
                elif self.reposdata[3]:
                    self.check_pkg(parts, 3)

        self.show_rezult()

    def get_repos_data(self) -> None:
        """
        get data from PACKAGES.TXT (SLACKBUILDS.TXT)
        """
        repos = self.meta.get_repo_dict()
        ind = 0
        for repo in self.repos:
            if repo in repos:
                self.reposdata[ind] = GetRepoData(repo).start()
            ind += 1

    def check_pkg(self, parts: list, ind: int) -> None:
        """
        check pkg for upgrade
        """
        data = self.reposdata[ind]

        pkgdata = ''
        if parts[0] in data['pkgs']:
            pkgdata = data['pkgs'][parts[0]]

        if pkgdata:
            newpkg = ''
            # alienbob, multilib, slack
            if ind != 1:
                if (parts[1] != pkgdata[0][1] or
                        parts[2] != pkgdata[0][2] or
                        parts[3] != pkgdata[0][3]):
                    newpkg = '-'.join(pkgdata[0])
            # sbo
            else:
                # fix check version for virtualbox-kernel* packages
                #   virtualbox-kernel*-${VERSION}_${KERNEL_VERSION}-... -->
                #   virtualbox-kernel*-${VERSION}-...
                # fix check version for nvidia-kernel packages
                #   nvidia-...-kernel-${VERSION}_${KERNEL_VERSION}-... -->
                #   nvidia-...-kernel-${VERSION}-...
                if (parts[0].startswith('virtualbox-kernel') or
                        (parts[0].startswith('nvidia-') and
                         parts[0].endswith('-kernel'))):
                    if '_' in parts[1]:
                        parts[1] = parts[1].split('_')[0]

                if parts[1] != pkgdata[0]:
                    newpkg = '-'.join(
                        [parts[0], pkgdata[0], parts[2], parts[3]])

            if newpkg:
                oldpkg = '-'.join(parts)
                self.upgrpkgs[ind].append(
                    ('{0}{1}{2}{3} --> '
                     '{4}{5}{2}').format(self.meta.clrs['yellow'],
                                         oldpkg,
                                         self.meta.clrs['reset'],
                                         get_indent(len(oldpkg), 37),
                                         self.meta.clrs['green'],
                                         newpkg))

    def show_rezult(self) -> None:
        """
        show pkgs for upgrade
        """
        new_pkgs = False
        for ind in range(len(self.repos)):
            if self.upgrpkgs[ind]:
                new_pkgs = True
                print('\nRepository: {0}{1}{2}'.format(self.meta.clrs['lcyan'],
                                                       self.repos[ind],
                                                       self.meta.clrs['reset']))
                for pkg in self.upgrpkgs[ind]:
                    print(pkg)

        if not new_pkgs:
            print(('{0}Packages for upgrade not '
                   'found.{1}').format(self.meta.clrs['green'],
                                       self.meta.clrs['reset']))
