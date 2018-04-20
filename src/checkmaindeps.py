#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# checkmaindeps.py file is part of spman
#
# spman - Slackware package manager
# Home page: https://github.com/MyRequiem/spman
#
# Copyright (c) 2018 Vladimir MyRequiem Astrakhan, Russia
# <mrvladislavovich@gmail.com>
# All rights reserved
# See LICENSE for details.


"""
Checking dependencies for program
"""

from .maindata import MainData
from .pkgs import Pkgs


def check_main_deps() -> None:
    """
    Checking dependencies for program:
        - GNU coreutils
        - GNU diffutils
        - GNU wget
        - pkgtools
    """
    deps = {
        'coreutils': 'a/',
        'diffutils': 'ap/',
        'wget': 'n/',
        'pkgtools': 'a/'
    }

    pkgs = Pkgs()
    meta = MainData()
    for dep in deps:
        if not pkgs.find_pkgs_on_system(dep):
            print(('{0}You need to install the package '
                   '{1}{2}{3}').format(meta.clrs['lred'],
                                       meta.clrs['lcyan'],
                                       dep,
                                       meta.clrs['reset']))

            # if repository 'slack' ON, show url for download package
            repo_dict = meta.get_repo_dict()
            if 'slack' in repo_dict:
                arch = '64' if meta.arch == 'x86_64' else ''
                os_version = meta.get_spman_conf()['OS_VERSION']
                print(('{0}{1}slackware{2}-{3}/'
                       'slackware{2}/{4}{5}').format(meta.clrs['grey'],
                                                     repo_dict['slack'],
                                                     arch,
                                                     os_version,
                                                     deps[dep],
                                                     meta.clrs['reset']))
            raise SystemExit
