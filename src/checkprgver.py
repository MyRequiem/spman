#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# checkprgver.py file is part of spman

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
Check program version
"""

from ssl import _create_unverified_context
from sys import (
    stdout,
    stderr
)
from urllib.request import urlopen

from .maindata import MainData


def check_prg_ver() -> None:
    """
    check program version
    """
    meta = MainData()
    local_ver = meta.prog_version
    print(('Installed version: {0}\n{1}Checking '
           'latest release...{2}').format(local_ver,
                                          meta.clrs['grey'],
                                          meta.clrs['reset']))

    # search latest release on https://github.com/MyRequiem/spman/releases
    url = '{0}/releases'.format(meta.home_page)
    _context = _create_unverified_context()
    bytes_content = urlopen(url, context=_context).read()
    # bytes --> str
    html = str(bytes_content, encoding=(stdout.encoding or stderr.encoding))

    # <a href="/MyRequiem/spman/archive/1.1.1.zip" rel="nofollow">
    # split('/MyRequiem/spman/archive/')
    spl = '/{0}/archive/'.format('/'.join(meta.home_page.split('/')[3:]))
    version = '.'.join(html.split(spl)[1].split('.')[:3])

    if version != local_ver:
        print(('{0}New version are available:{2} {4}\nVisit: '
               '{1}{3}/releases{2}\nor download new version '
               'source code:\n{1}{3}/archive/'
               '{4}.tar.gz{2}').format(meta.clrs['lred'],
                                       meta.clrs['cyan'],
                                       meta.clrs['reset'],
                                       meta.home_page,
                                       version))
    else:
        print(('{0}You are using the latest program '
               'version{1}').format(meta.clrs['green'],
                                    meta.clrs['reset']))
