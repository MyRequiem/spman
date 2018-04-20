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
    """{0}Version: {1}{6}
Usage: spman command [param[, param ...]]

{2} -h|--help{3}            Print this help message and exit
{2} -v|--check-version{3}   Check program version
{2} -l|--repolist{3}        Print a list of all the repositories
{2} -r|--repoinfo{3}        Show information about all active repositories
{2} -b|--blacklist{3}       Show blacklist
{2} -u|--update{3}          Update local data for all repositories
{2} -t|--health{3}          Check health installed packages
{2} -w|--new-config{3}      Find all '*.new' files from /etc/ and /usr/share/
                        folders and subfolders
{2} -g|--check-upgrade{3}   Check packages for upgrade
{2} -d|--download{3}        Download binary package or source code + SlackBuild
{2}     --pkg|--src{3}          for reposytory 'multilib' only --pkg
                          for reposytory 'sbo' only --src
{2}     reponame{3}             name of repository
{2}     pkg1[ pkg2...]{3}       list of packages name
{2} -q|--queue{3}           Download, build and install package(s) in the queue
                        from 'sbo' repository
{2}     --add|--remove{3}       add or remove package(s) from the queue
{2}     --clear{3}              clear queue
{2}     --show{3}               print queue
{2}     --install{3}            download, build and install package(s)
{2} -p|--find-deps pkg{3}   Show list all dependencies for package from 'sbo'
                        repository
{2} -s|--view-slackbuild{3} View the contents of files included in SlackBuild
                        archive using pager
{2}         pkg{3}              package name
{2} -f|--find-pkg pkg{3}    Find package from each enabled repository and
                        view info
{2} -i|--pkglist{3}         Show complete list of the packages in the repository
{2}     reponame{3}             name of repository
{2}     --only-installed{3}     output only installed packages
{2} -k|--check-deps{3}      Search dependency problems in the system packages
{2}     --sbbdep{3}             using \'sbbdep\' tool
{2}     --ldd{3}                using \'ldd\' tool
{2} -a|--bad-links{3}       Find links to non-existent files/directories
{2}     /path/to/dir{3}         directory for searching

{0}Home page: {5}
{4}{6}"""

    meta = MainData()

    if repo == 'error':
        # parameter input error
        print(('{0}Wrong parameters. '
               '{2}Type {1}spman --help{2}').format(meta.clrs['red'],
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
                                             meta.clrs['yellow'],
                                             meta.clrs['cyan'],
                                             meta.mail,
                                             meta.home_page,
                                             meta.clrs['reset']))
