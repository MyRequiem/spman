# helpmess.py file is part of spman
#
# spman - Slackware package manager
# Home page: https://github.com/MyRequiem/spman
#
# Copyright (c) 2018 Vladimir MyRequiem Astrakhan, Russia
# <mrvladislavovich@gmail.com>
# All rights reserved
# See LICENSE for details.

"""Help messages and usage information for spman."""

from .maindata import MainData


def show_help_mess(repo: str = "") -> None:
    """Print the program usage help message or specific repository errors."""
    meta = MainData()

    if repo == "error":
        error_msg = (
            f"{meta.clrs['lred']}Wrong parameters "
            f"{meta.clrs['reset']}({meta.clrs['cyan']}spman --help"
            f"{meta.clrs['reset']} for help)"
        )
        raise ValueError(error_msg)

    if repo:
        error_msg = (
            f"{meta.clrs['lred']}Repository {meta.clrs['cyan']}{repo} "
            f"{meta.clrs['lred']}is not available\n"
            f"{meta.clrs['reset']}For more info: "
            f"{meta.clrs['cyan']}spman --repolist{meta.clrs['reset']}"
        )
        raise ValueError(error_msg)

    # ruff: noqa: E501
    help_text = f"""{meta.clrs['grey']}Version: {meta.prog_version}
Home page: {meta.home_page}
{meta.mail}{meta.clrs['reset']}

Usage: spman <param> [param[, param ...]]

{meta.clrs['cyan']} -h, --help{meta.clrs['reset']}
    Print this help message and exit.

{meta.clrs['cyan']} -v, --check-version{meta.clrs['reset']}
    Check program version for updates.

{meta.clrs['cyan']} -l, --repolist{meta.clrs['reset']}
    Print a list of all repositories.

{meta.clrs['cyan']} -r, --repoinfo{meta.clrs['reset']}
    Show information about all active repositories.

{meta.clrs['cyan']} -b, --blacklist{meta.clrs['reset']}
    Show blacklisted packages from /etc/spman/blacklist

{meta.clrs['cyan']} -u, --update{meta.clrs['reset']}
    Update local data for all repositories.

{meta.clrs['cyan']} -t, --health{meta.clrs['reset']}
    Check the health of all installed packages on the system.

{meta.clrs['cyan']} -w, --new-config{meta.clrs['reset']}
    Search for *.new config files on the system.

{meta.clrs['cyan']} -g, --check-upgrade{meta.clrs['reset']}
    Check all installed packages for upgrades.

{meta.clrs['cyan']} -d, --download --pkg|--src <reponame> <pkg>[ <pkg> ...]{meta.clrs['reset']}
    Download binary package(s) or source code from a specified repository.
    {meta.clrs['yellow']}Note:{meta.clrs['reset']}
      only '--pkg' for repository 'multilib'
      only '--src' for repository 'sbo'

{meta.clrs['cyan']} -m, --upgrade-pkgs [--only-new]{meta.clrs['reset']}
    Install or upgrade packages in the current directory.
      {meta.clrs['cyan']}--only-new{meta.clrs['reset']}
          Packages already installed on the system with the same name,
          version, build number, and tag will not be reinstalled.

{meta.clrs['cyan']} -e, --remove-pkgs{meta.clrs['reset']}
    Remove packages from the system if corresponding *.t?z files
    in the current directory are already installed.

{meta.clrs['cyan']} -q, --queue --add|--remove|--clear|--show|--install{meta.clrs['reset']}
    Download, build, and install package(s) in the queue from SlackBuilds.org.
      {meta.clrs['cyan']}--add{meta.clrs['reset']}    <pkg>[ <pkg> ...] - add package(s) to the queue
      {meta.clrs['cyan']}--remove{meta.clrs['reset']} <pkg>[ <pkg> ...] - remove package(s) from the queue
      {meta.clrs['cyan']}--clear{meta.clrs['reset']}                    - clear queue
      {meta.clrs['cyan']}--show{meta.clrs['reset']}                     - print queue
      {meta.clrs['cyan']}--install{meta.clrs['reset']}                  - download, build, and install packages

{meta.clrs['cyan']} -y, --history [--update]{meta.clrs['reset']}
    View the package installation, update, and removal history.
      {meta.clrs['cyan']}--update{meta.clrs['reset']}
          Update the installed packages database (reset history).

{meta.clrs['cyan']} -p, --find-deps <pkg>{meta.clrs['reset']}
    Show a list of all dependencies for a package from the SlackBuilds.org (sbo)
    repository. Packages already installed in the system are highlighted in green.

{meta.clrs['cyan']} -s, --view-slackbuild <pkg>{meta.clrs['reset']}
    View the contents of files included in a SlackBuild archive using a
    pager (e.g., README, doinst.sh, patches, slack-desc, .info, .SlackBuild).

{meta.clrs['cyan']} -f, --find-pkg [--strict] <pattern>{meta.clrs['reset']}
    Search for a package (case-insensitive) across all enabled repositories.
      {meta.clrs['cyan']}--strict{meta.clrs['reset']}    - strict match by package name

{meta.clrs['cyan']} -i, --pkglist <reponame> [--only-installed]{meta.clrs['reset']}
    Show a complete list of packages in a repository. Packages already
    installed in the system are highlighted in green.
      {meta.clrs['cyan']}--only-installed{meta.clrs['reset']}    - show only installed packages

{meta.clrs['cyan']} -k, --check-deps --sbbdep|--ldd{meta.clrs['reset']}
    Search for dependency issues in system packages.
      {meta.clrs['cyan']}--sbbdep{meta.clrs['reset']}   - use the 'sbbdep' tool
      {meta.clrs['cyan']}--ldd{meta.clrs['reset']}      - use 'ldd'

{meta.clrs['cyan']} -a, --bad-links <path_to_dir>{meta.clrs['reset']}
    Search for broken links to nonexistent files or directories in the specified path.
"""
    print(help_text)
