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

from .maindata import MainData


class PkgList:
    """
    Show complete list of the packages in the repository
    """
    def __init__(self, repo: str, only_installed: bool):
        self.meta = MainData()
        self.repo = repo
        self.only_installed = only_installed

    def start(self):
        """
        start show packages list
        """
        print(self.only_installed)

    def xxx(self):
        """
        xxx
        """
        print(self)
