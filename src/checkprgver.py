#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# checkprgver.py file is part of spman
#
# spman - Slackware package manager
# Home page: https://github.com/MyRequiem/spman
#
# Copyright (c) 2018 Vladimir MyRequiem Astrakhan, Russia
# <mrvladislavovich@gmail.com>
# All rights reserved
# See LICENSE for details.


"""
Check program version
"""

from ssl import _create_unverified_context
from sys import stderr, stdout
from urllib.request import urlopen

from .maindata import MainData


def check_prg_ver() -> None:
    """
    check program version
    """
    meta = MainData()
    local_ver = meta.prog_version
    print(('Installed version: {0}\n{1}Checking '
           'latest release version...{2}').format(local_ver,
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
        # https://github.com/MyRequiem/spman/archive/1.5.4/spman-1.5.4.tar.gz
        print(('{0}New version are available:{1} {3}\n' +
               'Visit: {2}/releases\nor download new version source code:\n' +
               '{2}/archive/{3}/{4}-{3}.tar.gz').format(meta.clrs['lred'],
                                                        meta.clrs['reset'],
                                                        meta.home_page,
                                                        version,
                                                        meta.prog_name))
    else:
        print(('{0}You are using the latest program '
               'version{1}').format(meta.clrs['green'],
                                    meta.clrs['reset']))
