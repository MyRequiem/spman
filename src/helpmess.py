#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# helpmess.py file is part of spman
#
# spman - Slackware package manager
# Home page: https://github.com/MyRequiem/spman
#
# Copyright (c) 2018 Vladimir MyRequiem Astrakhan, Russia
# <mrvladislavovich@gmail.com>
# All rights reserved
# See LICENSE for details.


"""
Help messages and usage
"""

from .maindata import MainData


def show_help_mess(repo: str = '') -> None:
    """{0}Version: {1}
Home page: {4}
{3}{5}

Usage: spman command [param[, param ...]]

{2} -h, --help{5}
    Print this help message and exit
{2} -v, --check-version{5}
    Check program version for update
{2} -l, --repolist{5}
    Print a list of all the repositories
{2} -r, --repoinfo{5}
    Show information about all active repositories
{2} -b, --blacklist{5}
    Show blacklist
{2} -u, --update{5}
    Update local data for all repositories
{2} -t, --health{5}
    Check health installed packages
{2} -w, --new-config{5}
    Search for *.new config files on the system
{2} -g, --check-upgrade{5}
    Check all installed packages for upgrade
{2} -d, --download --pkg|--src reponame pkg1[ pkg2...]{5}
    Download binary package(s) or source code from specified repository
{6}    Note:{5} for reposytory 'multilib' only --pkg
          for reposytory 'sbo' only --src
{2} -m, --upgrade-pkgs [--only-new]{5}
    Upgrade packages in the current directory
      --only-new    - install only new packages
{2} -e, --remove-pkgs{5}
    Remove packages in the current directory
{2} -q, --queue --add pkglist|--remove pkglist|--clear|--show|--install{5}
    Download, build and install package(s) in the queue from SlackBuilds.org
{6}    Note:{5} pkglist - list of names of packages
      --add pkglist{5}      add package(s) to the queue
      --remove pkglist{5}   remove package(s) from the queue
      --clear{5}            clear queue
      --show{5}             print queue
      --install{5}          download, build and install package(s)
{2} -p, --find-deps pkgname{5}
    Show list all dependencies for package from 'sbo' repository. Installed
    packages are highlighted in green.
{2} -s, --view-slackbuild pkgname{5}
    View the contents of files included in SlackBuild archive using pager
{2} -f, --find-pkg [--strict] pkgname{5}
    Search package from each enabled repository and view info
    (case-insensitive)
      --strict    - strict match by package name
{2} -i, --pkglist reponame [--only-installed]{5}
    Show complete list of the packages on repository. Installed packages are
    highlighted in green.
      --only-installed      output only installed packages
{2} -k, --check-deps --sbbdep|--ldd{5}
    Search dependency problems in the system packages
      --sbbdep      using \'sbbdep\' tool
      --ldd         using \'ldd\' tool
{2} -a, --bad-links /path/to/dir{5}
    Search for links to nonexistent files/dir in the specified directory.
"""

    meta = MainData()

    if repo == 'error':
        # parameter input error
        print(('{0}Wrong parameters {2}({1}'
               'spman --help{2} for help)').format(meta.clrs['red'],
                                                   meta.clrs['cyan'],
                                                   meta.clrs['reset']))
        raise SystemExit
    elif repo:
        # repository does not exist or not available
        print(('{0}Repository {1}{2} {0}is not available\n{3}For more info: '
               '{1}spman --repolist{3}').format(meta.clrs['red'],
                                                meta.clrs['cyan'],
                                                repo,
                                                meta.clrs['reset']))
        raise SystemExit()

    # show usage
    print(str(show_help_mess.__doc__).format(meta.clrs['grey'],
                                             meta.prog_version,
                                             meta.clrs['cyan'],
                                             meta.mail,
                                             meta.home_page,
                                             meta.clrs['reset'],
                                             meta.clrs['yellow']))
