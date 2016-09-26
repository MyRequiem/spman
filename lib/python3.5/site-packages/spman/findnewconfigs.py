#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# findnewconfigs.py file is part of spman

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
Find all '*.new' files from /etc/ and /usr/share/ folders and subfolders
"""

from .maindata import MainData
from .utils import get_all_files


class FindNewConfigs(object):
    """
    Find all '*.new' files from /etc/ and /usr/share/ folders and subfolders
    """
    def __init__(self):
        self.meta = MainData()
        self.newconfigs = []

    def start(self):
        """
        start find *.new files
        """
        for configpath in ['/etc/', '/usr/share/']:
            configfiles = get_all_files(configpath)
            for configname in configfiles:
                if (configname.endswith('.new') and
                        not configname.endswith('/titletoc.new')):
                    self.newconfigs.append(configname)

        self.print_new_configs()

    def print_new_configs(self):
        """
        Print *.new files
        """
        if not self.newconfigs:
            print('{0}No *.new configuration '
                  'files found.{1}'.format(self.meta.clrs['green'],
                                           self.meta.clrs['reset']))
        else:
            print('\n{0}Found *.new configuration '
                  'files:{1}'.format(self.meta.clrs['yellow'],
                                     self.meta.clrs['reset']))
            for newconfig in self.newconfigs:
                print('\t{0}'.format(newconfig))

            print()
