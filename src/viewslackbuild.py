#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# viewslackbuild.py file is part of spman

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
View README, slack-desc, doinst.sh and .SlackBuild files from sbo repository.
"""

import pydoc
import sys
from ssl import _create_unverified_context
from urllib.request import urlopen

from .getrepodata import GetRepoData
from .maindata import MainData


class ViewSlackBuild:
    """
    View README, slack-desc, doinst.sh and .SlackBuild
    files from sbo repository.
    """
    def __init__(self, pkgname: str):
        self.meta = MainData()
        self.pkgname = pkgname

    def start(self) -> None:
        """
        start show slackbuilds files
        """
        sbodata = GetRepoData('sbo').start()
        if self.pkgname not in sbodata['pkgs']:
            from .utils import pkg_not_found_mess
            pkg_not_found_mess(self.pkgname, 'sbo')
            raise SystemExit

        pkgdata = sbodata['pkgs'][self.pkgname]
        filelist = pkgdata[6]
        url = '{0}{1}/{2}/{3}/'.format(self.meta.get_repo_dict()['sbo'],
                                       self.meta.get_os_version(),
                                       pkgdata[1],
                                       self.pkgname).replace('http://',
                                                             'https://')
        print(('{0}{1} > {2}\n'
               '{3}URL: {4}{5}{6}').format(self.meta.clrs['lcyan'],
                                           pkgdata[1].capitalize(),
                                           self.pkgname,
                                           self.meta.clrs['yellow'],
                                           self.meta.clrs['grey'],
                                           url,
                                           self.meta.clrs['reset']))

        num = 1
        for sl_file in filelist:
            print('  {0} {1}{2}{3}'.format(num,
                                           self.meta.clrs['cyan'],
                                           sl_file,
                                           self.meta.clrs['reset']))
            num += 1

        while True:
            choice = input(('{0}Your choice {1}({2}q{1}uit){3}'
                            ': ').format(self.meta.clrs['lyellow'],
                                         self.meta.clrs['grey'],
                                         self.meta.clrs['lred'],
                                         self.meta.clrs['reset']))

            if choice == 'q':
                raise SystemExit

            if choice.isdigit():
                choice = int(choice)
                if 0 < choice <= len(filelist):
                    self.show_file('{0}{1}'.format(url, filelist[choice - 1]))

    @staticmethod
    def show_file(url: str) -> None:
        """
        show file
        """
        _context = _create_unverified_context()
        content = urlopen(url, context=_context)
        pydoc.pager(str(content.read(),
                        encoding=(sys.stdout.encoding or sys.stderr.encoding)))
