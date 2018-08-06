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

Usage: spman <param> [param[, param ...]]

{2} -h, --help{5}
    Print this help message and exit.

{2} -v, --check-version{5}
    Check program version for update.

{2} -l, --repolist{5}
    Print a list of all the repositories.

{2} -r, --repoinfo{5}
    Show information about all active repositories.

{2} -b, --blacklist{5}
    Show blacklisted packages from /etc/spman/blacklist

{2} -u, --update{5}
    Update local data for all repositories.

{2} -t, --health{5}
    Check the health of all installed packages on the system and
    display detailed information.

{2} -w, --new-config{5}
    Search for *.new config files on the system.

{2} -g, --check-upgrade{5}
    Check all installed packages for upgrade.

{2} -d, --download --pkg|--src <reponame> <pkg>[ <pkg> ...]{5}
    Download binary package(s) or source code from specified repository.
{6}    Note:{5}
      only '--pkg' for reposytory 'multilib'
      only '--src' for reposytory 'sbo'

{2} -m, --upgrade-pkgs [--only-new]{5}
    Install/Upgrade packages in the current directory.
      {2}--only-new{5}
          Packages already installed on the system with the same name,
          version, build number and tag will not be reinstalled.

{2} -e, --remove-pkgs{5}
    If there are *.t?z packages in the current directory and they
    are installed, then these packages will be removed from the
    system.

{2} -q, --queue --add|--remove|--clear|--show|--install{5}
    Download, build and install package(s) in the queue from SlackBuilds.org
      {2}--add{5} <pkg>[ <pkg> ...]    - add package(s) to the queue
      {2}--remove{5} <pkg>[ <pkg> ...] - remove package(s) from the queue
      {2}--clear{5}                    - clear queue
      {2}--show{5}                     - print queue
      {2}--install{5}                  - download, build and install packages

{2} -y, --history [--update]{5}
    View the history of installing/updating/removing packages.
      {2}--update{5}
          Update the installed packages database (reset history).

{2} -p, --find-deps <pkg>{5}
    Show list all dependencies for package from SlackBuilds.org (sbo)
    repository. The packages already installed in the system are
    highlighted in green.

{2} -s, --view-slackbuild <pkg>{5}
    View the contents of files included in SlackBuild archive using
    pager: README, doinst.sh, patches, slack-desc, <pkg>.SlackBuild,
    <pkg>.info, etc.

{2} -f, --find-pkg [--strict] <pattern>{5}
    Search for package (case-insensitive) from each enabled
    repository and view info.
      {2}--strict{5}    - strict match by package name

{2} -i, --pkglist <reponame> [--only-installed]{5}
    Show complete list of the packages on repository. The packages
    already installed in the system are highlighted in green.
      {2}--only-installed{5}    - show only installed packages

{2} -k, --check-deps --sbbdep|--ldd{5}
    Search for problems with dependencies in the system packages.
      {2}--sbbdep{5}      - using \'sbbdep\' tool
      {2}--ldd{5}         - using \'ldd\'

{2} -a, --bad-links <path_to_dir>{5}
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
