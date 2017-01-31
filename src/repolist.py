#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# repolist.py file is part of spman

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
show repo list
"""

from .maindata import MainData


def show_repo_list() -> None:
    """
    show repo list
    """
    maindata = MainData()
    with open(maindata.configs_path + 'repo-list') as config:
        for line in config:
            if '://' in line:
                color = 'green' if not line.startswith('#') else 'red'
                if color == 'red':
                    line = line.split('#')[1].lstrip()
                print('{0}{1}{2}'.format(maindata.clrs[color],
                                         line,
                                         maindata.clrs['reset']),
                      end='')
