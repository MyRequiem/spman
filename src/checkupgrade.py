# checkupgrade.py file is part of spman
#
# spman - Slackware package manager
# Home page: https://github.com/MyRequiem/spman
#
# Copyright (c) 2018 Vladimir MyRequiem Astrakhan, Russia
# <mrvladislavovich@gmail.com>
# All rights reserved
# See LICENSE for details.

"""Check installed Slackware packages for available upgrades."""

from typing import Any

from .getrepodata import GetRepoData
from .maindata import MainData
from .pkgs import Pkgs


class CheckUpgrade:
    """Analyze system packages.

    Analyze system packages and match them against repository metadata for
    upgrades.
    """

    def __init__(self) -> None:
        """Initialize upgrade checker.

        Initialize upgrade checker with system specifications and database
        tracks.
        """
        self.meta: MainData = MainData()
        self.pkgs: Pkgs = Pkgs()
        self.blacklist: list[str] = self.meta.get_blacklist()
        self.repos: list[str] = ["alienbob", "sbo", "multilib", "slack"]
        self.reposdata: list[dict[str, Any]] = [{}, {}, {}, {}]
        self.upgrpkgs: list[list[tuple[str, str]]] = [[], [], [], []]

    def start(self) -> None:
        """Execute the upgrade.

        Execute the upgrade verification loop against all tracked
        repositories.
        """
        self.get_repos_data()

        for pkg in self.pkgs.find_pkgs_on_system():
            parts = self.pkgs.get_parts_pkg_name(pkg)
            if not parts or parts[0] in self.blacklist:
                continue

            pkg_name, pkg_ver, _, pkg_build = parts

            # alienbob repository match rules
            if (
                self.reposdata[0]
                and "alien" in pkg_build
                and "multilib" not in pkg_ver
                and pkg_name != "compat32-tools"
            ):
                self.check_pkg(parts, 0)

            # sbo (SlackBuilds.org) repository match rules
            elif self.reposdata[1] and "SBo" in pkg_build:
                self.check_pkg(parts, 1)

            # multilib repository match rules
            elif self.reposdata[2] and (
                "compat32" in pkg_build
                or pkg_name == "compat32-tools"
                or "multilib" in pkg_ver
            ):
                self.check_pkg(parts, 2)

            # slack (Official core Slackware) repository fallback match rules
            elif self.reposdata[3]:
                self.check_pkg(parts, 3)

        self.show_rezult()

    def get_repos_data(self) -> None:
        """Get data from PACKAGES.TXT or SLACKBUILDS.TXT."""
        repos = self.meta.get_repo_dict()

        # Elegant unpacking using enumerate() to track indices automatically.
        for ind, repo in enumerate(self.repos):
            if repo in repos:
                self.reposdata[ind] = GetRepoData(repo).start()

    def check_pkg(self, parts: list[str], ind: int) -> None:
        """Compare the installed package version.

        Compare the installed package version against repository metadata for
        updates.
        """
        data = self.reposdata[ind]
        pkg_name = parts[0]

        if pkg_name not in data["pkgs"]:
            return

        pkgdata = data["pkgs"][pkg_name]
        newpkg = ""

        # Repositories: alienbob, multilib, slack.
        if ind != 1:
            repo_parts = pkgdata[0]
            if (
                parts[1] != repo_parts[1]
                or parts[2] != repo_parts[2]
                or parts[3] != repo_parts[3]
            ):
                newpkg = "-".join(repo_parts)

        # SBo repository.
        else:
            # Clean composite kernel versions for virtualbox/nvidia modules
            if (
                pkg_name.startswith("virtualbox-kernel")
                or (
                    pkg_name.startswith("nvidia-") and
                    pkg_name.endswith("-kernel")
                )
            ) and "_" in parts[1]:
                parts[1] = parts[1].split("_", 1)[0]

            if parts[1] != pkgdata[0]:
                newpkg = "-".join([pkg_name, pkgdata[0], parts[2], parts[3]])

        if newpkg:
            oldpkg = "-".join(parts)

            self.upgrpkgs[ind].append((oldpkg, newpkg))

    def show_rezult(self) -> None:
        """Display colorized information.

        Display colorized information about packages available for upgrade.
        """
        new_pkgs = False

        for ind, repo_name in enumerate(self.repos):
            if self.upgrpkgs[ind]:
                new_pkgs = True
                print(
                    f"\nRepository: {self.meta.clrs['lcyan']}{repo_name}"
                    f"{self.meta.clrs['reset']}" # noqa: COM812
                )

                max_len = max(
                    (
                        len(pair[0])
                        for pair in self.upgrpkgs[ind]
                    ),
                    default=0,
                )

                for oldpkg, newpkg in self.upgrpkgs[ind]:
                    padded_old = f"{oldpkg:<{max_len}}"

                    print(
                        f"{self.meta.clrs['yellow']}{padded_old}"
                        f"{self.meta.clrs['reset']} --> "
                        f"{self.meta.clrs['green']}{newpkg}"
                        f"{self.meta.clrs['reset']}" # noqa: COM812
                    )

        if not new_pkgs:
            print(
                f"{self.meta.clrs['green']}Packages for upgrade not found."
                f"{self.meta.clrs['reset']}" # noqa: COM812
            )
