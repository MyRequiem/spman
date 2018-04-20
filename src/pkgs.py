#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# pkgs.py file is part of spman
#
# spman - Slackware package manager
# Home page: https://github.com/MyRequiem/spman
#
# Copyright (c) 2018 Vladimir MyRequiem Astrakhan, Russia
# <mrvladislavovich@gmail.com>
# All rights reserved
# See LICENSE for details.


"""
Processing packages
"""

import os

from .maindata import MainData


class Pkgs:
    """
    Processing package
    """
    def __init__(self):
        self.meta = MainData()

    def find_pkgs_on_system(self, pkg_name: str = '') -> list:
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

            return []

        return sorted(installed_pkgs)

    @staticmethod
    def get_parts_pkg_name(pkg_name: str) -> list:
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
