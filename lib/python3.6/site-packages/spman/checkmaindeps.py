#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# checkmaindeps.py file is part of spman

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
Checking dependencies for program
"""

from .maindata import MainData
from .pkgs import Pkgs


def check_main_deps():
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
                print(('{0}{1}slackware{2}-{3}/'
                       'slackware{2}/{4}{5}').format(meta.clrs['grey'],
                                                     repo_dict['slack'],
                                                     arch,
                                                     meta.get_os_version(),
                                                     deps[dep],
                                                     meta.clrs['reset']))
            raise SystemExit
