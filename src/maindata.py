# maindata.py file is part of spman
#
# spman - Slackware package manager
# Home page: https://github.com/MyRequiem/spman
#
# Copyright (c) 2018 Vladimir MyRequiem Astrakhan, Russia
# <mrvladislavovich@gmail.com>
# All rights reserved
# See LICENSE for details.

"""Main configuration and metadata for the program."""

from __future__ import annotations

from pathlib import Path
from platform import machine


class MainData:
    """Main data and configuration constants for spman."""

    def __init__(self) -> None:
        """Initialize MainData with program constants and color codes."""
        self.prog_name: str = "spman"
        self.prog_version: str = "2.2.3"
        self.home_page: str = f"https://github.com/MyRequiem/{self.prog_name}"
        self.mail: str = "<mrvladislavovich@gmail.com>"
        self.pkg_db_name: str = "pkg-db"
        self.pkgs_installed_path: str = "/var/log/packages/"
        self.configs_path: str = f"/etc/{self.prog_name}/"
        self.arch: str = machine()

        # Terminal ANSI color codes for stylized CLI output.
        self.clrs: dict[str, str] = {
            "red": "\x1b[0;31m",
            "lred": "\x1b[1;31m",
            "green": "\x1b[0;32m",
            "lgreen": "\x1b[1;32m",
            "yellow": "\x1b[0;33m",
            "lyellow": "\x1b[1;33m",
            "blue": "\x1b[0;34m",
            "lblue": "\x1b[1;34m",
            "magenta": "\x1b[0;35m",
            "lmagenta": "\x1b[1;35m",
            "cyan": "\x1b[0;36m",
            "lcyan": "\x1b[1;36m",
            "grey": "\x1b[38;5;247m",
            "reset": "\x1b[0m",
        }

    def get_repo_dict(self) -> dict[str, str]:
        """Return a dictionary of enabled repositories from repo-list config.

        Format: {'repo_name': 'url', ...}

        Raises:
            FileNotFoundError: If the repo-list file does not exist.
            ValueError: If all repositories in the config are disabled.

        """
        repo_dict: dict[str, str] = {}
        config_file = Path(self.configs_path) / "repo-list"

        with config_file.open(encoding="utf-8") as config:
            for line in config:
                clean_line = line.strip()
                if not clean_line or clean_line.startswith("#"):
                    continue

                parts = self.process_config_line(clean_line)
                repo_dict[parts[0]] = parts[1]

        if not repo_dict:
            # We raise a ValueError to keep this module decoupled from CLI
            # printing. The calling module will catch this and show a formatted
            # error message.
            error_msg = f"All repositories are disabled in {config_file}"
            raise ValueError(error_msg)

        return repo_dict

    def get_spman_conf(self) -> dict[str, str]:
        """Return a dictionary with all options from spman.conf.

        Fills missing options with default values.
        """
        spman_conf: dict[str, str] = {}
        config_file = Path(self.configs_path) / f"{self.prog_name}.conf"

        with config_file.open(encoding="utf-8") as config:
            for line in config:
                clean_line = line.strip()
                if not clean_line or clean_line.startswith("#"):
                    continue

                parts = self.process_config_line(clean_line, "=")
                spman_conf[parts[0]] = parts[1]

        # Default options used if not explicitly set in the config file.
        default_opt: dict[str, str] = {
            "OS_VERSION": "15.0",
            "OS_LAST_RELEASE": "15.0",
            "REPOS_PATH": f"/var/lib/{self.prog_name}/",
            "LOGS_PATH": f"/var/log/{self.prog_name}/",
            "QUEUE_PATH": f"/root/{self.prog_name}/queue/",
            "BUILD_PATH": f"/root/{self.prog_name}/build/",
            "OUTPUT_PATH": f"/root/{self.prog_name}/build/",
            "PKGTYPE": "txz",
            "USER_AGENT_TYPE": "curl",
        }

        # The `|` operator merges dicts (Python 3.9+). It populates missing
        # keys with values from default_opt and overrides others with
        # spman_conf.
        return default_opt | spman_conf

    def get_blacklist(self) -> list[str]:
        """Return a list of blacklisted packages from the blacklist config."""
        config_file = Path(self.configs_path) / "blacklist"

        with config_file.open(encoding="utf-8") as config:
            return [
                clean_line
                # The walrus operator (:=) strips the line, creates
                # `clean_line`, checks it for emptiness, and appends it to the
                # list if it's not a comment.
                for line in config
                if (clean_line := line.strip())
                and not clean_line.startswith("#")
            ]

    @staticmethod
    def process_config_line(
        line: str,
        sep: str | None = None,
    ) -> tuple[str, str]:
        """Parse a config line into a stripped (name, value) tuple."""
        parts = line.split(sep)

        name = parts[0].strip()
        value = parts[1].strip()

        # Add a trailing slash to URLs or directory paths if missing.
        if (
            (value.startswith("/") or "://" in value)
            and not value.endswith("/")
        ):
            value += "/"

        return name, value
