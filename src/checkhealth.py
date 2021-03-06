#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# checkhealth.py file is part of spman
#
# spman - Slackware package manager
# Home page: https://github.com/MyRequiem/spman
#
# Copyright (c) 2018 Vladimir MyRequiem Astrakhan, Russia
# <mrvladislavovich@gmail.com>
# All rights reserved
# See LICENSE for details.


"""
Check health installed packages
"""

from os import path

from .maindata import MainData
from .pkgs import Pkgs
from .utils import get_indent, get_line


class CheckHealth:
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

    def start(self) -> None:
        """
        start check health installed packages
        """
        try:
            from tqdm import tqdm
        except ImportError:
            def tqdm(*args, **kwargs):
                if args:
                    return args[0]
                return kwargs.get('iterable', None)

        for pkgname in tqdm(self.list_pkg_installed, leave=False,
                            ncols=80, unit=''):
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

    def check_exists_files(self, line: str, pkgname: str) -> None:
        """
        check exists file
        """
        starts = ('FILE LIST', 'dev/', 'install/')
        ends = ('/', '.new')
        if (not line.startswith(starts) and
                not line.endswith(ends) and
                '/incoming/' not in line and
                '/autostart/' not in line and
                '/ca-certificates/mozilla/' not in line):

            self.count_files += 1
            check_file = '/' + line
            if not path.isfile(check_file):
                self.not_exist_files += 1
                if self.pkgname != pkgname:
                    print(('\n{0}Package: '
                           '{1}{2}{3}').format(self.meta.clrs['yellow'],
                                               self.meta.clrs['cyan'],
                                               pkgname,
                                               self.meta.clrs['reset']))
                    self.pkgname = pkgname
                    self.count_broken_packages += 1
                print('\t{0}{1}{2}'.format(self.meta.clrs['red'],
                                           check_file,
                                           self.meta.clrs['reset']))

    def show_rezult(self) -> None:
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

        print('|' + get_line('-', 79))
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

        print('|' + get_line('-', 79))
