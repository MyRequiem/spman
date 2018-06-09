#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# removepkgs.py file is part of spman
#
# spman - Slackware package manager
# Home page: https://github.com/MyRequiem/spman
#
# Copyright (c) 2018 Vladimir MyRequiem Astrakhan, Russia
# <mrvladislavovich@gmail.com>
# All rights reserved
# See LICENSE for details.


"""
delete packages in the current directory
"""

import os

from .maindata import MainData
from .utils import get_packages_in_current_dir


class Removepkgs:
    """
    delete packages in the current directory
    """
    def __init__(self):
        self.meta = MainData()
        self.pkgs_in_dir = get_packages_in_current_dir()

    def start(self) -> None:
        """
        start remove
        """
        if not self.pkgs_in_dir:
            print(('{0}Directory {1}{2}{0} does not contain a Slackware '
                   'packages for remove.{3}').format(self.meta.clrs['lred'],
                                                     self.meta.clrs['cyan'],
                                                     os.getcwd(),
                                                     self.meta.clrs['reset']))
        else:
            self.removepkgs()

    def removepkgs(self) -> None:
        """
        remove packages
        """
        from subprocess import call

        removed = 0
        not_removed = []
        for pkg in self.pkgs_in_dir:
            # name of package without extention
            pkg_full_name = '.'.join(pkg.split('.')[:-1])
            pkg_path = '{0}{1}'.format(self.meta.pkgs_installed_path,
                                       pkg_full_name)

            if os.path.isfile(pkg_path):
                call('/sbin/removepkg {0}'.format(pkg_path), shell=True)
                removed += 1
            else:
                not_removed.append(pkg_full_name)

        print(('\n{0}Packages for deletion: {3}{1}\n'
               '{0}Removed:               '
               '{3}{2}').format(self.meta.clrs['lgreen'],
                                len(self.pkgs_in_dir),
                                removed,
                                self.meta.clrs['reset']))

        if not_removed:
            print('Packages not found in the system:')
            for pkg in not_removed:
                print('{0}{1}{2}'.format(self.meta.clrs['lred'],
                                         pkg,
                                         self.meta.clrs['reset']))
