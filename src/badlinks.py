#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# badlinks.py file is part of spman

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
Find links to non-existent files/directories
"""

from os import (
    path,
    chdir,
    getcwd,
    readlink
)

from .maindata import MainData


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

        from .utils import get_all_files

        err_count = 0
        allfiles = get_all_files(self.pathdir)
        for lnk in allfiles:
            # if file is link
            if path.islink(lnk):
                # path to directory where the link
                dirlink = path.dirname(lnk)
                # go to directory with a link
                if dirlink != getcwd():
                    chdir(dirlink)

                dest = readlink(lnk)
                if not path.isfile(dest) and not path.isdir(dest):
                    err_count += 1
                    print('{0}{1}{2}'.format(self.meta.clrs['red'],
                                             lnk,
                                             self.meta.clrs['reset']))

        self.print_rezult(err_count)

    def print_rezult(self, err_count: int) -> None:
        """
        print rezult
        """
        if err_count:
            print('\nIncorrect references in {0}: {1}'.format(self.pathdir,
                                                              err_count),
                  end='\n\n')
        else:
            print(('{0}Congratulations !!!\nNot found invalid '
                   'links in {1}{2}').format(self.meta.clrs['green'],
                                             self.pathdir,
                                             self.meta.clrs['reset']))
