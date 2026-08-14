# getrepodata.py file is part of spman
#
# spman - Slackware package manager
# Home page: https://github.com/MyRequiem/spman
#
# Copyright (c) 2018 Vladimir MyRequiem Astrakhan, Russia
# <mrvladislavovich@gmail.com>
# All rights reserved
# See LICENSE for details.

"""Fetch, parse, and structure metadata from repositories."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .maindata import MainData
from .pkgs import Pkgs


class GetRepoData:
    """Fetch and organize package metadata from a specified repository."""

    def __init__(self, reponame: str) -> None:
        """Initialize repository parser with target names and size counters."""
        self.reponame: str = reponame
        self.meta: MainData = MainData()
        self.pkgs: Pkgs = Pkgs()
        self.spman_conf: dict[str, str] = self.meta.get_spman_conf()

        # Track raw byte sizes: [compressed, uncompressed].
        self.comp: list[int] = [0, 0]
        self.pkgname: str = ""

        self.rdata: dict[str, Any] = {
            # Timestamp of the last repository update on the remote server
            "lupd": "",
            # Total count of available packages in this repository
            "numpkgs": 0,
            # Total human-readable compressed size (e.g., '14M')
            "comp": "",
            # Total human-readable uncompressed size (e.g., '45M')
            "uncomp": "",
            # Structured package registry database mapping
            "pkgs": {
# ruff: noqa: ERA001
# 'pkg_name': [
#   [0] - List containing naming tokens (for SBo: holds only version string)
#   [1] - Target repository category path (e.g., development, audio, system)
#   [2] - Compressed package size in bytes (Omitted/empty for SBo repository)
#   [3] - Uncompressed package size in bytes (Omitted/empty for SBo repository)
#   [4] - List of tracked application dependencies
#   [5] - Multi-line formatted package summary and description
#   [6] - List of files included in the SlackBuild archive (SBo only)
#   [7] - List of source code download URLs (SBo only)
#   [8] - Package tarball file extension string (e.g., 'txz')
# ]
            },
        }

    def start(self) -> dict[str, Any]:
        """Parse and structured metadata.

        Parse and structured metadata from PACKAGES.TXT or SLACKBUILDS.TXT.
        """
        if self.reponame == "sbo":
            # For SBo, the last update timestamp is stored on the first line of
            # its ChangeLog.txt file.
            logs_path = Path(self.spman_conf["LOGS_PATH"])
            dfile = logs_path / self.reponame / "ChangeLog.txt"

            with dfile.open(encoding="utf-8") as datafile:
                for line in datafile:
                    if line != "\n":
                        self.rdata["lupd"] = line.strip()
                    break

        fname = "SLACKBUILDS.TXT" if self.reponame == "sbo" else "PACKAGES.TXT"
        repos_path = Path(self.spman_conf["REPOS_PATH"])
        dfile = repos_path / self.reponame / fname

        with dfile.open(encoding="utf-8") as datafile:
            for line in datafile:
                # Extract the last update timestamp if not already set (non-SBo
                # repos).
                if (
                    not self.rdata["lupd"]
                    and line.startswith("PACKAGES.TXT; ")
                ):
                    self.rdata["lupd"] = self.get_line_value(line, "; ")
                    continue

                if self.reponame != "sbo":
                    self.get_non_sbo_data(line)
                else:
                    self.get_sbo_data(line)

        # Process the comprehensive ALL-PACKAGES.TXT file for standard
        # Slackware repos.
        if self.reponame == "slack":
            all_pkgs_path = dfile.parent / f"ALL-{fname}"

            with all_pkgs_path.open(encoding="utf-8") as datafile:
                for line in datafile:
                    self.get_non_sbo_data(line)

        # Finalize repository statistics and convert byte sizes to
        # human-readable format.
        self.rdata["numpkgs"] = len(self.rdata["pkgs"])
        if self.comp[0]:
            self.rdata["comp"] = self.get_human_readable_size(self.comp[0])
            self.rdata["uncomp"] = self.get_human_readable_size(self.comp[1])

        return self.rdata

    def get_non_sbo_data(self, line: str) -> None:
        """Parse a single line from PACKAGES.TXT.

        Parse a single line from PACKAGES.TXT and extract package metadata.
        """
        rdata = self.rdata["pkgs"]

        if line.startswith("PACKAGE NAME: "):
            pkg = self.get_line_value(line, ": ")
            parts = self.pkgs.get_parts_pkg_name(pkg)

            # Ensure the package name structure is valid before processing.
            if parts and parts[0] not in rdata:
                self.pkgname = parts[0]
                rdata[self.pkgname] = self.get_list_new_pkg()
                rdata[self.pkgname][0] = parts
                # Extract package extension string safely from the right end.
                rdata[self.pkgname][8] = pkg.rsplit(".", 1)[-1]
            else:
                self.pkgname = ""

        elif self.pkgname:
            if line.startswith("PACKAGE LOCATION: "):
                val = self.get_line_value(line, ": ")
                rdata[self.pkgname][1] = "/".join(val.split("/")[1:])
            elif line.startswith("PACKAGE SIZE (compressed): "):
                self.process_size_pkg(line, 0)
            elif line.startswith("PACKAGE SIZE (uncompressed): "):
                self.process_size_pkg(line, 1)
            elif line.startswith("PACKAGE REQUIRED: "):
                self.get_req_pkg(line, ",")
            elif line.startswith(f"{self.pkgname}:"):
                val = self.get_line_desc(line, f"{self.pkgname}:")
                if val:
                    rdata[self.pkgname][5].append(val)

    def get_sbo_data(self, line: str) -> None:
        """Parse a single line from SLACKBUILDS.TXT.

        Parse a single line from SLACKBUILDS.TXT and extract SBo metadata.
        """
        pkgs_db = self.rdata["pkgs"]

        if line.startswith("SLACKBUILD NAME: "):
            self.pkgname = self.get_line_value(line, ": ")
            pkgs_db[self.pkgname] = self.get_list_new_pkg()
            return

        pkg_entry = pkgs_db[self.pkgname]

        if line.startswith("SLACKBUILD VERSION: "):
            pkg_entry[0] = self.get_line_value(line, ": ")
        elif line.startswith("SLACKBUILD LOCATION: "):
            pkg_entry[1] = self.get_line_value(line, ": ").split("/")[1]
        elif line.startswith("SLACKBUILD REQUIRES: "):
            self.get_req_pkg(line)
        elif line.startswith("SLACKBUILD SHORT DESCRIPTION: "):
            val = self.get_line_desc(line, ": ")
            pkg_entry[5].append(val)
        elif line.startswith("SLACKBUILD FILES: "):
            val = self.get_line_value(line, ": ")
            # Fast and clean list extension using compressed generator.
            pkg_entry[6].extend(sfile.strip() for sfile in val.split())
        elif line.startswith("SLACKBUILD DOWNLOAD: "): # noqa: SIM114
            self.get_dwnld_urls(line)
        elif (
            self.meta.arch == "x86_64"
            and line.startswith("SLACKBUILD DOWNLOAD_x86_64: ")
        ):
            self.get_dwnld_urls(line)

    def get_dwnld_urls(self, line: str) -> None:
        """Extract and store source download URLs from SBo metadata line."""
        val = self.get_line_value(line, ": ")
        if val and val not in {"UNSUPPORTED", "UNTESTED"}:
            urls = [url.strip() for url in val.split()]
            self.rdata["pkgs"][self.pkgname][7] = urls

    @staticmethod
    def get_line_desc(line: str, sep: str) -> str:
        """Extract and clean description values.

        Extract and clean description values using the specified separator.
        """
        return sep.join(line.split(sep)[1:]).strip()

    def get_req_pkg(self, line: str, sep: str | None = None) -> None:
        """Extract and parse clean application dependencies.

        Extract and parse clean application dependencies into the registry
        database.
        """
        str_req = self.get_line_value(line, ": ").split(sep)
        pkg_deps = self.rdata["pkgs"][self.pkgname][4]

        for req in str_req:
            if req and req != "%README%":
                pkg_deps.append(req.strip())

    def process_size_pkg(self, line: str, ind: int) -> None:
        """Parse and aggregate package sizes.

        Parse and aggregate package sizes, storing their human-readable format.
        """
        # if ind == 0: compressed size; if ind == 1: uncompressed size
        val = int(self.get_line_value(line, ": ").split()[0])
        self.comp[ind] += val
        hval = self.get_human_readable_size(val)
        self.rdata["pkgs"][self.pkgname][ind + 2] = hval

    @staticmethod
    def get_list_new_pkg() -> list[Any]:
        """Return a blank template list initialization.

        Return a blank template list initialization for a new package entry.
        """
        return ["", "", "", "", [], [], [], [], ""]

    @staticmethod
    def get_line_value(line: str, sep: str) -> str:
        """Extract and clean the value component.

        Extract and clean the value component from a separated line parameter.
        """
        return line.split(sep)[1].strip()

    @staticmethod
    def get_human_readable_size(val: int) -> str:
        """Convert a raw kilobyte size value.

        Convert a raw kilobyte size value into a stylized human-readable
        string.
        """
        if val < 1024:
            return f"{val} Kb"

        hval = val / 1024
        if hval < 1024:
            return f"{hval:.2f} Mb"

        return f"{hval / 1024:.2f} Gb"
