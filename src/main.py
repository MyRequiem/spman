# main.py file is part of spman
#
# spman - Slackware package manager
# Home page: https://github.com/MyRequiem/spman
#
# Copyright (c) 2018 Vladimir MyRequiem Astrakhan, Russia
# <mrvladislavovich@gmail.com>
# All rights reserved
# See LICENSE for details.

"""Main application controller for spman."""

import collections.abc
import sys

from .helpmess import show_help_mess
from .maindata import MainData


class Main:
    """Main application dispatcher handling CLI arguments and commands."""

    def __init__(self) -> None:
        """Initialize the main application loop.

        (metadata, and command routing)
        """
        # Slice sys.argv to skip the script name, leaving only CLI arguments.
        self.args: list[str] = sys.argv[1:]
        self.meta: MainData = MainData()

        self.repos: dict[str, str] = self.meta.get_repo_dict()

        # Command dispatcher routing CLI flags to specific class methods.
        self.commands: dict[str, collections.abc.Callable[[], None]] = {
            "-h": self.show_help,
            "--help": self.show_help,
            "-v": self.check_version,
            "--check-version": self.check_version,
            "-l": self.show_repo_list,
            "--repolist": self.show_repo_list,
            "-r": self.show_info_repos,
            "--repoinfo": self.show_info_repos,
            "-b": self.show_blacklist,
            "--blacklist": self.show_blacklist,
            "-u": self.update,
            "--update": self.update,
            "-t": self.check_health,
            "--health": self.check_health,
            "-w": self.find_new_configs,
            "--new-config": self.find_new_configs,
            "-g": self.check_upgrade,
            "--check-upgrade": self.check_upgrade,
            "-d": self.download_pkg,
            "--download": self.download_pkg,
            "-m": self.upgrade_pkgs,
            "--upgrade-pkgs": self.upgrade_pkgs,
            "-e": self.remove_pkgs,
            "--remove-pkgs": self.remove_pkgs,
            "-q": self.processing_queue,
            "--queue": self.processing_queue,
            "-y": self.history,
            "--history": self.history,
            "-p": self.find_deps,
            "--find-deps": self.find_deps,
            "-s": self.view_slackbuild,
            "--view-slackbuild": self.view_slackbuild,
            "-f": self.find_pkg,
            "--find-pkg": self.find_pkg,
            "-k": self.checkdeps,
            "--check-deps": self.checkdeps,
            "-a": self.bad_links,
            "--bad-links": self.bad_links,
            "-i": self.pkglist,
            "--pkglist": self.pkglist,
        }

    def start(self) -> None:
        """Parse arguments and launch the relevant application options."""
        # Show error and exit if the program is run without any CLI arguments.
        if not self.args:
            show_help_mess("error")

        current_flag = self.args[0]

        if current_flag not in self.commands:
            show_help_mess("error")

        # Light flags that do not require running intensive environment/config
        # validation.
        light_flags = {
            "-h", "--help",
            "-v", "--check-version",
            "-l", "--repolist",
            "-b", "--blacklist",
            "-u", "--update",
            "-t", "--health",
            "-w", "--new-config",
            "-m", "--upgrade-pkgs",
            "-e", "--remove-pkgs",
            "-k", "--checkdeps",
            "-a", "--bad-links",
        }

        # Run major system tests for heavy operations (install, download,
        # queue, etc.).
        if current_flag not in light_flags:
            from .majortests import MajorTests
            MajorTests().start()

        # Execute the routed command from the dispatcher dictionary.
        self.commands[current_flag]()

    def show_help(self) -> None:
        """Show the program help message."""
        show_help_mess()

    def show_repo_list(self) -> None:
        """Show the repository list from the configuration file."""
        from .repolist import show_repo_list
        show_repo_list()

    def update(self) -> None:
        """Update local repository metadata.

        Fetches PACKAGES.TXT, SLACKBUILDS.TXT, and ChangeLog.txt for each
        enabled repository.
        """
        from .update import Update
        Update().start()

    def show_info_repos(self) -> None:
        """Show detailed information about all active repositories."""
        if len(self.args) > 1:
            show_help_mess("error")

        from .showinforepos import ShowInfoRepos
        ShowInfoRepos().start()

    def check_version(self) -> None:
        """Check the program version for available updates."""
        from .checkprgver import check_prg_ver
        check_prg_ver()

    def check_health(self) -> None:
        """Check the health of all installed packages on the system."""
        from .checkhealth import CheckHealth
        CheckHealth().start()

    def find_new_configs(self) -> None:
        """Find all '*.new' configuration files on the system.

        Scans the /etc/ and /usr/share/ directories and their subfolders.
        """
        from .findnewconfigs import FindNewConfigs
        FindNewConfigs().start()

    def check_upgrade(self) -> None:
        """Check all installed packages for available upgrades."""
        from .checkupgrade import CheckUpgrade
        CheckUpgrade().start()

    def show_blacklist(self) -> None:
        """Show blacklisted packages in stylized terminal output."""
        for pkg in self.meta.get_blacklist():
            print(f"{self.meta.clrs['lred']}{pkg}{self.meta.clrs['reset']}")

    def download_pkg(self) -> None:
        """Download binary packages or source code with SlackBuild scripts.

        Validates the download mode (--pkg or --src) against specific
        repository constraints.
        """
        # We need at least:
        # spman <flag> <mode> <repo> <pkg1> (minimum 4 arguments).
        if len(self.args) < 4:
            show_help_mess("error")

        # Extract parameters using human-readable names.
        mode = self.args[1]
        repo = self.args[2]
        pkglist = self.args[3:]

        if repo not in self.repos:
            show_help_mess(repo)

        if mode not in {"--src", "--pkg"}:
            show_help_mess("error")

        # Validate repository-specific constraints.
        if mode == "--pkg" and repo == "sbo":
            error_msg = (
                f"{self.meta.clrs['lred']}"
                f"Only SlackBuild scripts with source code can be downloaded "
                f"from the 'sbo' repository.{self.meta.clrs['reset']}"
            )
            raise ValueError(error_msg)

        if mode == "--src" and repo == "multilib":
            error_msg = (
                f"{self.meta.clrs['lred']}Only binary packages can be "
                f"downloaded from the 'multilib' repository."
                f"{self.meta.clrs['reset']}"
            )
            raise ValueError(error_msg)

        from .downloadpkg import DownloadPkg
        DownloadPkg(mode, repo, pkglist).start()

    def upgrade_pkgs(self) -> None:
        """Install or upgrade packages found in the current directory."""
        # If an argument is provided but it's not the allowed flag, it's an
        # error.
        if len(self.args) > 1 and self.args[1] != "--only-new":
            show_help_mess("error")

        # True if '--only-new' flag is present, False otherwise.
        only_new = len(self.args) > 1 and self.args[1] == "--only-new"

        from .upgradepkgs import Upgradepkgs
        Upgradepkgs(only_new).start()

    def remove_pkgs(self) -> None:
        """Remove installed packages.

        (that match files in the current directory)
        """
        from .removepkgs import Removepkgs
        Removepkgs().start()

    def processing_queue(self) -> None:
        """Process the package queue specifically for the 'sbo' repository."""
        repo = "sbo"
        if repo not in self.repos:
            show_help_mess(repo)

        if len(self.args) < 2:
            show_help_mess("error")

        action = self.args[1]
        pkgs = self.args[2:]

        from .queue import Queue
        queue = Queue()

        # Dispatcher for simple queue commands that do not accept package
        # arguments.
        simple_actions = {
            "--clear": queue.clear,
            "--show": queue.show,
            "--install": queue.install,
        }

        if action in simple_actions:
            simple_actions[action]()
            return

        # Handle commands that strictly REQUIRE package arguments.
        if not pkgs:
            show_help_mess("error")

        if action == "--add":
            queue.add(pkgs)
        elif action == "--remove":
            queue.remove(pkgs)
        else:
            show_help_mess("error")

    def history(self) -> None:
        """Show or update the package installation and removal history."""
        # True if the explicit '--update' flag is passed, False otherwise
        # (Any other trailing garbage for a command is ignored).
        is_update = len(self.args) > 1 and self.args[1] == "--update"

        if len(self.args) > 1 and self.args[1] != "--update":
            show_help_mess("error")

        from .history import History
        History(is_update).start()

    def find_deps(self) -> None:
        """Show a list of all dependencies for a package.

        (from the 'sbo' repository).
        """
        repo = "sbo"
        if repo not in self.repos:
            show_help_mess(repo)

        if len(self.args) < 2:
            show_help_mess("error")

        target_pkg = self.args[1]

        from .finddeps import FindDeps
        FindDeps().start(target_pkg)

    def view_slackbuild(self) -> None:
        """View text files inside a SlackBuild archive (only 'sbo' repository).

        Provides an interactive menu to view files like README, doinst.sh,
        slack-desc, and the actual .SlackBuild build script.
        """
        repo = "sbo"
        if repo not in self.repos:
            show_help_mess(repo)

        if len(self.args) < 2:
            show_help_mess("error")

        target_pkg = self.args[1]

        from .viewslackbuild import ViewSlackBuild
        ViewSlackBuild(target_pkg).start()

    def find_pkg(self) -> None:
        """Globally search for a package and display its information.

        Scans all enabled repositories using case-insensitive pattern
        matching or strict exact name matching.
        """
        # Minimum required: spman --find-pkg <pattern> (at least 2 arguments).
        if len(self.args) < 2:
            show_help_mess("error")

        strict = "--strict" in self.args

        if strict:
            # For exact match, syntax must be:
            # spman --find-pkg --strict <pkgname>
            if self.args[1] != "--strict" or len(self.args) < 3:
                show_help_mess("error")
            pkgname = self.args[2]
        else:
            # Standard pattern match: spman --find-pkg <pattern>
            pkgname = self.args[1]

        from .findpkg import FindPkg
        FindPkg(strict, pkgname).start()

    def checkdeps(self) -> None:
        """Search for dependency issues.

        Search for dependency issues in system packages using 'sbbdep' or
        'ldd'.
        """
        if len(self.args) < 2 or self.args[1] not in {"--sbbdep", "--ldd"}:
            show_help_mess("error")

        mode = self.args[1]

        from .checkdeps import CheckDeps
        CheckDeps(mode).start()

    def bad_links(self) -> None:
        """Find broken symbolic links to nonexistent files or directories."""
        if len(self.args) < 2:
            show_help_mess("error")

        target_path = self.args[1]

        from .badlinks import BadLinks
        BadLinks(target_path).start()

    def pkglist(self) -> None:
        """Show a complete list of packages in a given repository."""
        # Syntax required: spman --pkglist <reponame> [--only-installed]
        if len(self.args) < 2:
            show_help_mess("error")

        repo = self.args[1]
        if repo not in self.repos:
            show_help_mess(repo)

        # True if the optional third argument is strictly '--only-installed'.
        only_installed = (
            len(self.args) > 2 and self.args[2] == "--only-installed"
        )

        # If a third argument is passed but it's not the allowed flag, trigger
        # an error.
        if len(self.args) > 2 and not only_installed:
            show_help_mess("error")

        from .pkglist import PkgList
        PkgList(repo, only_installed).start()
