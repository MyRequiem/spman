#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# pkgs.py file is part of spman

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
Processing packages
"""

import os

from .maindata import MainData


class Pkgs(object):
    """
    Processing package
    """
    def __init__(self):
        self.meta = MainData()

    def find_pkgs_on_system(self, pkg_name=''):
        """
        return list full name installed package(s) on system
        """
        # list containing the names of the files
        # in the directory /var/log/packages/
        installed_pkgs = os.listdir(self.meta.pkgs_installed_path)
        if pkg_name:
            for pkg in installed_pkgs:
                if self.get_parts_pkg_name(pkg)[0] == pkg_name:
                    return [pkg]

        else:
            return sorted(installed_pkgs)

    @staticmethod
    def get_parts_pkg_name(pkg_name):
        """
        return list of parts package name:
            [name, version, architecture, build]
        """
        # remove extention if exist
        ext = ('.tgz', '.txz')
        if pkg_name.endswith(ext):
            pkg_name = '.'.join(pkg_name.split('.')[:-1])

        # example pkg name:
        # xorg-server-1.14.3-x86_64-3_slack14.1
        parts = pkg_name.split('-')
        build = parts[-1]
        arch = parts[-2]
        ver = parts[-3]
        name = '-'.join(parts[:-3])

        return [name, ver, arch, build]
