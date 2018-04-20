#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# showinforepos.py file is part of spman
#
# spman - Slackware package manager
# Home page: https://github.com/MyRequiem/spman
#
# Copyright (c) 2018 Vladimir MyRequiem Astrakhan, Russia
# <mrvladislavovich@gmail.com>
# All rights reserved
# See LICENSE for details.


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
