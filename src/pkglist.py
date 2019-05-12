#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# pkglist.py file is part of spman
#
# spman - Slackware package manager
# Home page: https://github.com/MyRequiem/spman
#
# Copyright (c) 2018 Vladimir MyRequiem Astrakhan, Russia
# <mrvladislavovich@gmail.com>
# All rights reserved
# See LICENSE for details.


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
        self.num_installed_pkgs = 0

    def start(self) -> None:
        """
        start show packages list
        """
        meta = MainData()
        rdata = GetRepoData(self.repo).start()

        for pkg in sorted(rdata['pkgs']):
            full_pkg_name = self.get_full_pkg_name(pkg)
            if full_pkg_name:
                # the package is installed but not from the SBo repository
                if self.repo == 'sbo' and not full_pkg_name.endswith('_SBo'):
                    if not self.only_installed:
                        print(pkg)
                        continue
                    else:
                        continue

                # the package is installed but not from the alienbob repository
                if (self.repo == 'alienbob' and
                        not full_pkg_name.endswith('alien')):
                    if not self.only_installed:
                        print(pkg)
                        continue
                    else:
                        continue

                print(('{0}{1}{2}-{3}'
                       '{4}').format(meta.clrs['lgreen'],
                                     pkg,
                                     meta.clrs['grey'],
                                     '-'.join(full_pkg_name.split('-')[-3:]),
                                     meta.clrs['reset']))
                self.num_installed_pkgs += 1
            elif not self.only_installed:
                print(pkg)

        print(('{0}Total packages in '
               'the repository:{2} {1}').format(meta.clrs['lyellow'],
                                                rdata['numpkgs'],
                                                meta.clrs['reset']))
        print('{0}Installed:{1} {2}'.format(meta.clrs['lgreen'],
                                            meta.clrs['reset'],
                                            self.num_installed_pkgs))

    def get_full_pkg_name(self, pkg: str) -> str:
        """
        if package installed on the system return full
        name package, otherwise return blank string
        """
        return ''.join(self.pkgs.find_pkgs_on_system(pkg))
