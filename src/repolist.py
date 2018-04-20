#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# repolist.py file is part of spman
#
# spman - Slackware package manager
# Home page: https://github.com/MyRequiem/spman
#
# Copyright (c) 2018 Vladimir MyRequiem Astrakhan, Russia
# <mrvladislavovich@gmail.com>
# All rights reserved
# See LICENSE for details.


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
