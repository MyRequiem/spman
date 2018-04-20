#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# checkuser.py file is part of spman
#
# spman - Slackware package manager
# Home page: https://github.com/MyRequiem/spman
#
# Copyright (c) 2018 Vladimir MyRequiem Astrakhan, Russia
# <mrvladislavovich@gmail.com>
# All rights reserved
# See LICENSE for details.


"""
Check super user
"""

import getpass


def check_root_user() -> None:
    """
    Check super user
    """
    if getpass.getuser() != 'root':
        print('spman can only be run as root')
        raise SystemExit
