# pkgs.py file is part of spman
#
# spman - Slackware package manager
# Home page: https://github.com/MyRequiem/spman
#
# Copyright (c) 2018 Vladimir MyRequiem Astrakhan, Russia
# <mrvladislavovich@gmail.com>
# All rights reserved
# See LICENSE for details.

"""Module for processing and analyzing installed Slackware packages."""

from pathlib import Path

from .maindata import MainData


class Pkgs:
    """Process and analyze installed system packages."""

    def __init__(self) -> None:
        """Initialize the package processor with system metadata."""
        self.meta: MainData = MainData()

    def find_pkgs_on_system(self, pkg_name: str = "") -> list[str]:
        """Return a sorted list of full names for installed system packages.

        If pkg_name is provided, returns a single-item list containing the
        exact match, or an empty list if not found.
        """
        base_path = Path(self.meta.pkgs_installed_path)
        if not base_path.is_dir():
            return []

        # Extract, filter out hidden/system files, and sort package names.
        installed_pkgs = sorted(
            p.name
            for p in base_path.iterdir()
            if p.is_file() and not p.name.startswith(".")
        )

        # Fast path for searching a specific package name.
        if pkg_name:
            for pkg in installed_pkgs:
                parts = self.get_parts_pkg_name(pkg)
                if parts and parts[0] == pkg_name:
                    return [pkg]
            return []

        # Collect all valid system packages (exactly 4 name tokens).
        return [
            pkg for pkg in installed_pkgs
            if len(self.get_parts_pkg_name(pkg)) == 4
        ]

    @staticmethod
    def get_parts_pkg_name(pkg_name: str) -> list[str]:
        """Split a Slackware package name into its four standard components.

        Returns:
            A list containing [name, version, architecture, build], or an empty
            list if the package name structure is invalid.

        """
        # Safely strip the extension from the end of the string if present:
        # <pkgname>-15.0-x86_64-1.txz -> <pkgname>-15.0-x86_64-1
        if pkg_name.lower().endswith((".tgz", ".txz", ".tbz", ".tlz")):
            pkg_name = pkg_name.rsplit(".", 1)[0]

        parts = pkg_name.split("-")

        # Guard clause for broken or malformed package names.
        if len(parts) < 4:
            return []

        # Slackware naming convention parses from right to left.
        build = parts[-1]
        arch = parts[-2]
        ver = parts[-3]
        name = "-".join(parts[:-3])

        return [name, ver, arch, build]
