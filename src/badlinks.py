#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# badlinks.py file is part of spman
#
# spman - Slackware package manager
# Home page: https://github.com/MyRequiem/spman
#
# Copyright (c) 2018 Vladimir MyRequiem Astrakhan, Russia
# <mrvladislavovich@gmail.com>
# All rights reserved
# See LICENSE for details.


"""
Find links to non-existent files/directories
"""

from os import getcwd, path, readlink, stat

from .maindata import MainData
from .utils import get_all_files


class BadLinks:
    """
    Find links to non-existent files/directories
    """
    def __init__(self, pathdir: str):
        self.meta = MainData()
        self.pathdir = pathdir
        if not self.pathdir.endswith('/'):
            self.pathdir += '/'
        if self.pathdir.startswith('./'):
            self.pathdir = self.pathdir[2:]
        if not self.pathdir.startswith('/'):
            self.pathdir = '{0}/{1}'.format(getcwd(), self.pathdir)

    def start(self) -> None:
        """
        start find bad links
        """
        if not path.isdir(self.pathdir):
            print(('Directory {0}{1}{2} does '
                   'not exist.').format(self.meta.clrs['lcyan'],
                                        self.pathdir,
                                        self.meta.clrs['reset']))
            raise SystemExit

        try:
            from tqdm import tqdm
        except ImportError:
            def tqdm(*args, **kwargs):
                if args:
                    return args[0]
                return kwargs.get('iterable', None)

        bad_links = []
        for lnk in tqdm(get_all_files(self.pathdir), leave=False,
                        ncols=80, unit=''):
            if path.islink(lnk):
                try:
                    stat(lnk)
                except FileNotFoundError:
                    bad_links.append((lnk, readlink(lnk)))

        self.print_rezult(bad_links)

    def print_rezult(self, bad_links: list) -> None:
        """
        print rezult
        """
        err_count = len(bad_links)
        if err_count:
            print(('{0}Incorrect references in {1}: '
                   '{2}{3}{4}').format(self.meta.clrs['yellow'],
                                       self.pathdir,
                                       self.meta.clrs['lred'],
                                       err_count,
                                       self.meta.clrs['reset']))

            for bad_link in bad_links:
                print(('{0}{1}{4} -> '
                       '{3}{2}{4}').format(self.meta.clrs['lcyan'],
                                           bad_link[0],
                                           bad_link[1],
                                           self.meta.clrs['red'],
                                           self.meta.clrs['reset']))
        else:
            print(('{0}Congratulations !!!\nNot found invalid '
                   'links in {1}{2}').format(self.meta.clrs['green'],
                                             self.pathdir,
                                             self.meta.clrs['reset']))
