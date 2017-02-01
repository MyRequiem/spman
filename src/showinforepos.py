#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# showinforepos.py file is part of spman

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
Show information about all repositories.
"""

from .getrepodata import GetRepoData
from .maindata import MainData
from .utils import get_indent


class ShowInfoRepos:
    """
    Show information about all repositories.
    """
    def __init__(self):
        self.meta = MainData()

    def start(self) -> None:
        """
        init show information
        """
        repos = self.meta.get_repo_dict()
        for repo in sorted(repos):
            rdata = GetRepoData(repo).start()
            print('\nRepository: {0}{1}{2}'.format(self.meta.clrs['lyellow'],
                                                   repo,
                                                   self.meta.clrs['reset']))

            self.print_option('URL:', self.meta.get_repo_dict()[repo])
            self.print_option('Last update:', rdata['lupd'])
            self.print_option('Total packages:', rdata['numpkgs'])
            if rdata['comp']:
                self.print_option('Compressed packages:', rdata['comp'])
                self.print_option('Uncompressed packages:', rdata['uncomp'])

        print()

    def print_option(self, optname: str, val: str) -> None:
        """
        print option
        """
        print('{0}{1}{2}{3}{4}{5}'.format(self.meta.clrs['yellow'],
                                          optname,
                                          self.meta.clrs['cyan'],
                                          get_indent(len(optname), 23),
                                          val,
                                          self.meta.clrs['reset']))