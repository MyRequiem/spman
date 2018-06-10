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

from os import listdir

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
        pkgs = []
        # list containing the names of the files
        # in the directory /var/log/packages/
        installed_pkgs = listdir(self.meta.pkgs_installed_path)
        for pkg in sorted(installed_pkgs):
            if pkg_name and self.get_parts_pkg_name(pkg)[0] == pkg_name:
                    return [pkg]
            else:
                if len(self.get_parts_pkg_name(pkg)) == 4:
                    pkgs.append(pkg)

        if pkg_name:
            return []

        return pkgs

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
        # broken package name
        if len(parts) < 4:
            return ['']

        build = parts[-1]
        arch = parts[-2]
        ver = parts[-3]
        name = '-'.join(parts[:-3])

        return [name, ver, arch, build]
