#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# checkhealth.py file is part of spman

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
Check health installed packages
"""

from os import path

from .maindata import MainData
from .pkgs import Pkgs
from .utils import (
    get_indent,
    get_line
)


class CheckHealth(object):
    """
    Check health installed packages
    """
    def __init__(self):
        self.meta = MainData()
        self.pkgs = Pkgs()
        self.list_pkg_installed = self.pkgs.find_pkgs_on_system()
        self.blacklist = self.meta.get_blacklist()
        self.not_exist_files = 0
        self.count_files = 0
        self.count_broken_packages = 0
        self.pkgname = ''

    def start(self):
        """
        start check health installed packages
        """
        print()
        for pkgname in self.list_pkg_installed:
            if (self.pkgs.get_parts_pkg_name(pkgname)[0] not in
                    self.blacklist):
                with open('{0}{1}'.format(self.meta.pkgs_installed_path,
                                          pkgname)) as pkgfile:
                    count_lines = 1
                    for line in pkgfile:
                        if count_lines > 19:
                            self.check_exists_files(line.strip(), pkgname)
                        count_lines += 1

        self.show_rezult()

    def check_exists_files(self, line, pkgname):
        """
        check exists file
        """
        starts = ('FILE LIST', 'dev/', 'install/')
        ends = ('/', '.new')
        if (not line.startswith(starts) and
                not line.endswith(ends) and
                '/incoming/' not in line):

            self.count_files += 1
            check_file = '/' + line
            if not path.isfile(check_file):
                self.not_exist_files += 1
                if self.pkgname != pkgname:
                    print('Package: {0}'.format(pkgname))
                    self.pkgname = pkgname
                    self.count_broken_packages += 1
                print('\t{0}{1}{2}'.format(self.meta.clrs['red'],
                                           check_file,
                                           self.meta.clrs['reset']))

    def show_rezult(self):
        """
        Display general statistics
        """
        percent = 100 - self.not_exist_files * 100 / self.count_files
        if percent > 95:
            color = 'green'
        elif percent > 70:
            color = 'yellow'
        else:
            color = 'red'

        str1 = 'Total packages:'
        str2 = 'Broken packages:'
        str3 = 'Checked files:'
        str4 = 'Missing files:'
        str5 = 'Total health:'

        print('\n|' + get_line('-', 79))
        print(('| {0} {1}{2}\n'
               '| {3} {4}{5}\n'
               '| {6} {7}{8}\n'
               '| {9} {10}{11}\n'
               '| {12} {13}{14}{15}%'
               '{16}').format(str1,
                              get_indent(len(str1), 20),
                              len(self.list_pkg_installed),
                              str2,
                              get_indent(len(str2), 20),
                              self.count_broken_packages,
                              str3,
                              get_indent(len(str3), 20),
                              '{0:,d}'.format(self.count_files),
                              str4,
                              get_indent(len(str4), 20),
                              self.not_exist_files,
                              str5,
                              get_indent(len(str5), 20),
                              self.meta.clrs[color],
                              '{0:.4f}'.format(percent)[:-2],
                              self.meta.clrs['reset']))

        print('|' + get_line('-', 79), end='\n\n')
