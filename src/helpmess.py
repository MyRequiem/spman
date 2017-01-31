#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# helpmess.py file is part of spman

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
Help messages and usage
"""

from .maindata import MainData
from .repolist import show_repo_list


def show_help_mess(repo=''):
    """
{0}Version: {1}{6}
Usage: spman command [param[, param ...]]

{2} -h|--help{3}            Print this help message and exit.
{2} -v|--check-version{3}   Check program version.
{2} -l|--repolist{3}        Print a list of all the repositories.
{2} -r|--repoinfo{3}        Show information about all active repositories.
{2} -b|--blacklist{3}       Show blacklist.
{2} -u|--update{3}          Update local data for all repositories.
{2} -t|--health{3}          Check health installed packages.
{2} -w|--new-config{3}      Find all '*.new' files from /etc/ and /usr/share/
                        folders and subfolders.
{2} -g|--check-upgrade{3}   Check packages for upgrade.
{2} -d|--download{3}        Download binary package or source code + SlackBuild
{2}     --pkg|--src{3}          for reposytory 'multilib' only --pkg
                          for reposytory 'sbo' only --src
{2}     reponame{3}             name of repository
{2}     pkg1[ pkg2...]{3}       list of packages name
{2} -q|--queue{3}           Download, build and install package(s) in the queue
                        from 'sbo' repository.
{2}     --add|--remove{3}       add or remove package(s) from the queue
{2}     --clear{3}              clear queue
{2}     --show{3}               print queue
{2}     --install{3}            download, build and install package(s)
{2} -p|--find-deps pkg{3}   Show list all dependencies for package from 'sbo'
                        repository.
{2} -s|--view-slackbuild{3} View README, slack-desc, doinst.sh and .SlackBuild
                        files from sbo repository.
{2}         pkg{3}              package name
{2} -f|--find-pkg pkg{3}    Find package from each enabled repository and
                        view info.
{2} -k|--check-deps{3}      Search dependency problems in the system packages.
{2}     --sbbdep{3}             using \'sbbdep\' tool
{2}     --ldd{3}                using \'ldd\' tool
{2} -a|--bad-links{3}       Find links to non-existent files/directories.
{2}     /path/to/dir{3}         directory for searching


{4}Home page: {7}
{0}{5}{6}
"""

    meta = MainData()

    if repo == 'error':
        # parameter input error
        print(('{0}Wrong parameters:{1} \'spman -h\' or '
               '\'spman --help\' for help{2}').format(meta.clrs['red'],
                                                      meta.clrs['cyan'],
                                                      meta.clrs['reset']))
        raise SystemExit
    elif repo:
        # repository does not exist
        print(('\n{0}Repository{3} {1}\'{2}\'{0} is not '
               'available:{3}\n').format(meta.clrs['lred'],
                                         meta.clrs['cyan'],
                                         repo,
                                         meta.clrs['reset']))
        show_repo_list()
        print('\n{0}config file: '
              '{1}repo-list{2}'.format(meta.clrs['grey'],
                                       meta.configs_path,
                                       meta.clrs['reset']), end='\n\n')
        raise SystemExit()

    # show usage
    print(str(show_help_mess.__doc__).format(meta.clrs['grey'],
                                             meta.prog_version,
                                             meta.clrs['yellow'],
                                             meta.clrs['cyan'],
                                             meta.clrs['green'],
                                             meta.mail,
                                             meta.clrs['reset'],
                                             meta.home_page))
