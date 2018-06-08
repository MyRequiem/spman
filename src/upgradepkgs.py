#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# upgradepkgs.py file is part of spman
#
# spman - Slackware package manager
# Home page: https://github.com/MyRequiem/spman
#
# Copyright (c) 2018 Vladimir MyRequiem Astrakhan, Russia
# <mrvladislavovich@gmail.com>
# All rights reserved
# See LICENSE for details.


"""
upgrade packages in the current directory
"""

import os

from .maindata import MainData
from .utils import get_packages_in_current_dir


class Upgradepkgs:
    """
    upgrade packages in the current directory
    """
    def __init__(self, only_new: bool):
        self.only_new = only_new
        self.meta = MainData()
        self.pkgs_in_dir = get_packages_in_current_dir()

    def start(self) -> None:
        """
        start upgrade
        """
        if not self.pkgs_in_dir:
            print(('{0}Directory {1}{2}{0} does not contain a Slackware '
                   'packages for upgrade.{3}').format(self.meta.clrs['lred'],
                                                      self.meta.clrs['cyan'],
                                                      os.getcwd(),
                                                      self.meta.clrs['reset']))
        else:
            self.upgradepkgs()

    def upgradepkgs(self) -> None:
        """
        upgrade packages
        """
        from subprocess import call

        for pkg in self.pkgs_in_dir:
            install_mod = '--install-new --reinstall'
            if self.only_new:
                install_mod = '--install-new'

            call('/sbin/upgradepkg {0} {1}'.format(install_mod, pkg),
                 shell=True)
