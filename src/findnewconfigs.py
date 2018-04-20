#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# findnewconfigs.py file is part of spman
#
# spman - Slackware package manager
# Home page: https://github.com/MyRequiem/spman
#
# Copyright (c) 2018 Vladimir MyRequiem Astrakhan, Russia
# <mrvladislavovich@gmail.com>
# All rights reserved
# See LICENSE for details.


"""
Find all '*.new' files from /etc/ and /usr/share/ folders and subfolders
"""

from .maindata import MainData
from .utils import get_all_files


class FindNewConfigs:
    """
    Find all '*.new' files from /etc/ and /usr/share/ folders and subfolders
    """
    def __init__(self):
        self.meta = MainData()
        self.newconfigs = []

    def start(self) -> None:
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

    def print_new_configs(self) -> None:
        """
        Print *.new files
        """
        if not self.newconfigs:
            print('{0}No *.new configuration '
                  'files found.{1}'.format(self.meta.clrs['green'],
                                           self.meta.clrs['reset']))
        else:
            print('{0}Found *.new configuration '
                  'files:{1}'.format(self.meta.clrs['yellow'],
                                     self.meta.clrs['reset']))
            for newconfig in self.newconfigs:
                print('{0}{1}{2}'.format(self.meta.clrs['grey'],
                                         newconfig,
                                         self.meta.clrs['reset']))
