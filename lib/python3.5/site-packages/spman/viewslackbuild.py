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


class ViewSlackBuild(object):
    """
    View README, slack-desc, doinst.sh and .SlackBuild
    files from sbo repository.
    """
    def __init__(self, pkgname):
        self.meta = MainData()
        self.pkgname = pkgname
        self.sbodata = GetRepoData('sbo').start()
        self.pkgdata = []
        self.filelist = []

    def start(self):
        """
        start show slackbuilds files
        """
        if self.pkgname not in self.sbodata['pkgs']:
            from .utils import pkg_not_found_mess
            pkg_not_found_mess(self.pkgname, 'sbo')
            raise SystemExit

        self.pkgdata = self.sbodata['pkgs'][self.pkgname]
        self.filelist = self.pkgdata[6]
        self.create_interface()

        while True:
            choice = input('Your choice: ')
            if choice == 'q' or choice == 'Q':
                raise SystemExit

            url = self.meta.get_repo_dict()['sbo'].replace('http://',
                                                           'https://')
            url = '{0}{1}/{2}/{3}/'.format(url,
                                           self.meta.get_os_version(),
                                           self.pkgdata[1],
                                           self.pkgname)

            if choice == 'r' or choice == 'R' and 'README' in self.filelist:
                self.show_file('{0}README'.format(url))
            if choice == 's' or choice == 'S':
                self.show_file('{0}slack-desc'.format(url))
            if choice == 'd' or choice == 'D' and 'doinst.sh' in self.filelist:
                self.show_file('{0}doinst.sh'.format(url))
            if choice == 'b' or choice == 'B':
                self.show_file('{0}{1}.SlackBuild'.format(url, self.pkgname))

    def create_interface(self):
        """
        create interface of choice for the user
        """
        location = self.pkgdata[1]
        print('\n{0}{1} > {2}{3}'.format(self.meta.clrs['lcyan'],
                                         location[0].upper() + location[1:],
                                         self.pkgname,
                                         self.meta.clrs['reset']),
              end='\n\n')

        if 'README' in self.filelist:
            print('View {0}R{1}EADME'.format(self.meta.clrs['red'],
                                             self.meta.clrs['reset']))
        if 'slack-desc' in self.filelist:
            print('View {0}s{1}lack-desc'.format(self.meta.clrs['red'],
                                                 self.meta.clrs['reset']))
        if 'doinst.sh' in self.filelist:
            print('View {0}d{1}oinst.sh'.format(self.meta.clrs['red'],
                                                self.meta.clrs['reset']))
        if self.pkgname + '.SlackBuild' in self.filelist:
            print('View {0}.Slack{1}B{2}uild'.format(self.pkgname,
                                                     self.meta.clrs['red'],
                                                     self.meta.clrs['reset']))
        print('{0}Q{1}uit'.format(self.meta.clrs['red'],
                                  self.meta.clrs['reset']), end='\n\n')

    @staticmethod
    def show_file(url):
        """
        show file
        """
        _context = _create_unverified_context()
        content = urlopen(url, context=_context)
        pydoc.pager(str(content.read(),
                        encoding=(sys.stdout.encoding or sys.stderr.encoding)))
