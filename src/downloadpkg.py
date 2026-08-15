# downloadpkg.py file is part of spman
#
# spman - Slackware package manager
# Home page: https://github.com/MyRequiem/spman
#
# Copyright (c) 2018 Vladimir MyRequiem Astrakhan, Russia
# <mrvladislavovich@gmail.com>
# All rights reserved
# See LICENSE for details.

"""Download ready-made binary packages or source code and build scripts."""

from pathlib import Path # noqa: I001
from tarfile import open as taropen
from typing import Any

from .download import Download
from .getrepodata import GetRepoData
from .maindata import MainData
from .utils import get_all_files, url_is_alive


class DownloadPkg:
    """Download ready-made binary packages or source files with SlackBuilds."""

    def __init__(self, mode: str, repo: str, pkglist: list[str]) -> None:
        """Initialize the package downloader.

        Initialize the package downloader with repository and configuration
        metadata.
        """
        self.meta: MainData = MainData()
        self.spman_conf: dict[str, str] = self.meta.get_spman_conf()
        self.os_ver: str = self.spman_conf["OS_VERSION"]
        self.mode: str = mode             # download src or pkg
        self.repo: str = repo             # repo name
        self.pkglist: list[str] = pkglist # packages list for download

        # May raise ValueError if all repositories are disabled
        self.repo_url: str = self.meta.get_repo_dict()[self.repo]
        self.repodata: dict[str, Any] = GetRepoData(self.repo).start()
        self.dest: str = self.spman_conf["BUILD_PATH"]

    def start(self) -> None:
        """Execute the package downloading process.

        Execute the package downloading process for all items in the list.
        """
        for pkg in self.pkglist:
            # This method will raise a ValueError if the package does not exist
            # in the repository metadata; otherwise, execution continues
            # normally.
            self.check_exist_pkg(pkg)

            pkgdata = self.get_pkg_data(pkg)

            if self.repo == "sbo":
                self.download_sbo(pkg, pkgdata)

            if self.repo == "multilib":
                self.download_multilib(pkgdata)

            if self.repo == "alienbob":
                self.download_alienbob(pkg, pkgdata)

            if self.repo == "slack":
                self.download_slack(pkg, pkgdata)

    def download_sbo(self, pkg: str, pkgdata: list[str]) -> None:
        """Download the SlackBuild script from SBo (slackbuilds.org).

        Download the SlackBuild script and source code from the 'sbo'
        repository.
        """
        # SBo does not support the Slackware 'current' branch. Fall back to the
        # latest stable release specified in /etc/spman/spman.conf.
        if (os_ver := self.os_ver) == "current":
            os_ver = self.spman_conf["OS_LAST_RELEASE"]

        fname = f"{pkg}.tar.gz"
        url = f"{self.repo_url}{os_ver}/{pkgdata[1]}/{fname}"

        # Download the SlackBuild script archive.
        Download(url, self.dest).start()

        # Unpack the SlackBuild archive safely using a context manager.
        base_path = Path(self.dest)
        archive_path = base_path / fname

        with taropen(archive_path) as tar:
            tar.extractall(self.dest, filter="data")

        # Remove the source archive after extraction using pathlib syntax.
        archive_path.unlink()

        # Download all required source files into the package directory.
        pkg_dir = f"{self.dest}{pkg}/"
        for src_url in pkgdata[7]:
            Download(src_url, pkg_dir).start()

    def download_multilib(self, pkgdata: list[str]) -> None:
        """Download binary package(s) from the 'multilib' repository."""
        fname = self.get_fname(pkgdata)
        location = self.get_pkg_location(pkgdata[1])

        url = f"{self.repo_url}{self.os_ver}/{location}{fname}"
        Download(url, self.dest).start()

    def download_alienbob(self, pkg: str, pkgdata: list[str]) -> None:
        """Download from the alienbob repository.

        Download binary packages or source directories from the alienbob
        repository.
        """
        arch = "x86_64" if self.meta.arch == "x86_64" else "x86"

        if self.mode == "--pkg":
            # Download a ready-made binary package.
            fname = self.get_fname(pkgdata)
            url = f"{self.repo_url}{self.os_ver}/{arch}/{pkg}/{fname}"
            Download(url, self.dest).start()
        else:
            # Download a directory containing source code and the SlackBuild
            # script.
            clean_repo_url = self.repo_url.replace("sbrepos", "slackbuilds")
            url = f"{clean_repo_url}{pkg}/build/"
            dest_dir = f"{self.dest}{pkg}/"

            Download(url, dest_dir).start()

            if Path(dest_dir).is_dir():
                self.set_chmod(dest_dir)

    # ruff: noqa: C901,PLR0912,PLR0915
    def download_slack(self, pkg: str, pkgdata: list[str]) -> None:
        """Download from the standard Slackware repository.

        Download binary packages or source patches from the standard Slackware
        repository.
        """
        arch = "64" if self.meta.arch == "x86_64" else ""
        repo_url = f"{self.repo_url}slackware{arch}-{self.os_ver}"

        # Patched kernel packages and sources for stable releases are
        # historically located in patches/packages/linux-x.x.x/
        kernel_packages = {
            "kernel-firmware",
            "kernel-generic",
            "kernel-headers",
            "kernel-huge",
            "kernel-modules",
            "kernel-source",
        }

        location = self.get_pkg_location(pkgdata[1])
        if self.mode == "--pkg" or pkg in kernel_packages:
            # Download a standard binary package.
            fname = self.get_fname(pkgdata)
            url = f"{repo_url}/{location}{fname}"
            Download(url, self.dest).start()
            return

        # Download a directory containing source code and the SlackBuild
        # script.
        replace_str = "packages"
        if self.os_ver == "current" or not location.startswith("patches/"):
            replace_str = f"slackware{arch}"

        location = location.replace(replace_str, "source")
        url = f"{repo_url}/{location}{pkg}/"
        dest_dir = f"{self.dest}{pkg}"

        # Processes complex layouts for X11 packages inside source/x/x11
        if location.endswith("/x/"):
            if not url_is_alive(url):
                location = f"{location}x11/"
                url = f"{repo_url}/{location}"

                for xdir in ("build", "configure", "doinst.sh", "makepkg"):
                    print(
                        f"{self.meta.clrs['grey']}Search for file: "
                        f"{location}{xdir}/{pkg}{self.meta.clrs['reset']}" # noqa: COM812
                    )
                    xurl = f"{url}{xdir}/{pkg}"
                    if url_is_alive(xurl):
                        Download(xurl, f"{dest_dir}/{xdir}").start()
                    elif xdir == "configure":
                        Download(
                            xurl.replace(pkg, xdir),
                            f"{dest_dir}/{xdir}",
                        ).start()

                for xdir in ("patch", "post-install"):
                    print(
                        f"{self.meta.clrs['grey']}Search for directory: "
                        f"{location}{xdir}/{pkg}/{self.meta.clrs['reset']}" # noqa: COM812
                    )
                    xurl = f"{url}{xdir}/{pkg}"
                    if url_is_alive(xurl):
                        Download(xurl, f"{dest_dir}/{xdir}/{pkg}").start()

                    print(
                        f"{self.meta.clrs['grey']}Search for file: "
                        f"{location}{xdir}/{pkg}.{xdir}{self.meta.clrs['reset']}" # noqa: COM812
                    )
                    xurl = f"{url}{xdir}/{pkg}.{xdir}"
                    if url_is_alive(xurl):
                        Download(xurl, f"{dest_dir}/{xdir}").start()

                xdir = "slack-desc"
                print(
                    f"{self.meta.clrs['grey']}Search for file: "
                    f"{location}{xdir}/{pkg}{self.meta.clrs['reset']}" # noqa: COM812
                )
                xurl = f"{url}{xdir}/{pkg}"
                Download(xurl, f"{dest_dir}/{xdir}").start()

                # Source code tarball
                source = f"{pkg}-{pkgdata[0][1]}.tar.xz"
                print(
                    f"{self.meta.clrs['grey']}Search for source code: "
                    f"{source}{self.meta.clrs['reset']}" # noqa: COM812
                )

                # Vertical sorting for X11 source subdirectories mapping
                x11_src_dirs = (
                    "src/app",
                    "src/data",
                    "src/doc",
                    "src/driver",
                    "src/font",
                    "src/lib",
                    "src/proto",
                    "src/util",
                    "src/xcb",
                    "src/xserver",
                )
                for src_dir in x11_src_dirs:
                    print(
                        f"{self.meta.clrs['grey']}Scan directory: "
                        f"{location}{src_dir}/{self.meta.clrs['reset']}" # noqa: COM812
                    )
                    xurl = f"{url}{src_dir}/{source}"
                    if url_is_alive(xurl):
                        Download(xurl, f"{dest_dir}/{src_dir}").start()
                        break

                scripts = (
                    "arch.use.flags",
                    "modularize",
                    "noarch",
                    "package-blacklist",
                    "x11.SlackBuild",
                )
                for script in scripts:
                    Download(f"{url}{script}", dest_dir).start()

                if Path(dest_dir).is_dir():
                    self.set_chmod(dest_dir)
                return
        elif location.endswith("/kde/"):
            url = f"{repo_url}/{location}"

            for kdir in ("build", "cmake", "docs", "doinst.sh", "makepkg"):
                print(
                    f"{self.meta.clrs['grey']}Search for file: "
                    f"{location}{kdir}/{pkg}{self.meta.clrs['reset']}" # noqa: COM812
                )
                xurl = f"{url}{kdir}/{pkg}"

                if url_is_alive(xurl):
                    Download(xurl, f"{dest_dir}/{kdir}").start()
                elif kdir == "cmake":
                    # If cmake script isn't package-specific, fetch standard
                    # SBo/Slack core components.
                    cmake_files = (
                        kdir,
                        "kdeaccessibility",
                        "kdeadmin",
                        "kdebase",
                        "kdebindings",
                    )
                    for file_ in cmake_files:
                        xurl = f"{url}{kdir}/{file_}"
                        Download(xurl, f"{dest_dir}/{kdir}").start()

            kdir = "modules"
            xurl = f"{url}{kdir}"
            Download(xurl, f"{dest_dir}/{kdir}").start()

            for kdir in ("patch", "post-install", "pre-install"):
                print(
                    f"{self.meta.clrs['grey']}Search for directory: "
                    f"{location}{kdir}/{pkg}/{self.meta.clrs['reset']}" # noqa: COM812
                )
                xurl = f"{url}{kdir}/{pkg}"
                if url_is_alive(xurl):
                    Download(xurl, f"{dest_dir}/{kdir}/{pkg}").start()

                print(
                    f"{self.meta.clrs['grey']}Search for file: "
                    f"{location}{kdir}/{pkg}.{kdir}{self.meta.clrs['reset']}" # noqa: COM812
                )
                xurl = f"{url}{kdir}/{pkg}.{kdir}"
                if url_is_alive(xurl):
                    Download(xurl, f"{dest_dir}/{kdir}").start()

            kdir = "slack-desc"
            print(
                f"{self.meta.clrs['grey']}Search for file: "
                f"{location}{kdir}/{pkg}{self.meta.clrs['reset']}" # noqa: COM812
            )
            xurl = f"{url}{kdir}/{pkg}"
            Download(xurl, f"{dest_dir}/{kdir}").start()

            # Source code tarball
            source = f"{pkg}-{pkgdata[0][1]}.tar.xz"
            print(
                f"{self.meta.clrs['grey']}Search for source code: "
                f"{source}{self.meta.clrs['reset']}" # noqa: COM812
            )

            for kdir in ("src", "src/extragear"):
                print(
                    f"{self.meta.clrs['grey']}Scan directory: "
                    f"{location}{kdir}/{self.meta.clrs['reset']}" # noqa: COM812
                )
                xurl = f"{url}{kdir}/{source}"
                if url_is_alive(xurl):
                    Download(xurl, f"{dest_dir}/{kdir}").start()
                    break

            kde_scripts = (
                "KDE.SlackBuild",
                "KDE.options",
                "modularize",
                "noarch",
                "package-blacklist",
            )
            for script in kde_scripts:
                Download(f"{url}{script}", dest_dir).start()

            if Path(dest_dir).is_dir():
                self.set_chmod(dest_dir)
            return

        elif location.endswith("/kdei/"):
            # Extract core package name without language tag
            # (e.g., kde-l10n-ru -> kde-l10n)
            short_pkg_name = pkg.rsplit("-", 1)[0]
            url = f"{repo_url}/{location}{short_pkg_name}"

            kdir = "slack-desc"
            print(
                f"{self.meta.clrs['grey']}Search for file: "
                f"{location}{kdir}/{kdir}.{pkg}{self.meta.clrs['reset']}" # noqa: COM812
            )
            Download(
                f"{url}/{kdir}/{kdir}.{pkg}",
                f"{dest_dir}/{kdir}",
            ).start()

            Download(
                f"{url}/{short_pkg_name}.SlackBuild",
                dest_dir,
            ).start()

            lang_path = f"{dest_dir}/languages"
            print(
                f"{self.meta.clrs['grey']}Creating "
                f"{lang_path}{self.meta.clrs['reset']}" # noqa: COM812
            )

            # Atomic file write operation using pathlib context
            lang_tag = pkg.rsplit("-", 1)[-1]
            Path(lang_path).write_text(f"{lang_tag}\n", encoding="utf-8")

            source = f"{pkg}-{pkgdata}.tar.xz"
            print(
                f"{self.meta.clrs['grey']}Source code: "
                f"{source}{self.meta.clrs['reset']}" # noqa: COM812
            )
            Download(f"{url}/{source}", dest_dir).start()

            if short_pkg_name == "kde-l10n":
                for addon_dir in ("kdepim-l10n", "local.options"):
                    Download(
                        f"{url}/{addon_dir}",
                        f"{dest_dir}/{addon_dir}",
                    ).start()

            if Path(dest_dir).is_dir():
                self.set_chmod(dest_dir)
            return

        # Default fallback branch: downloads any standard non-X11/KDE Slackware
        # package sources.
        Download(url, dest_dir).start()
        if Path(dest_dir).is_dir():
            self.set_chmod(dest_dir)

    @staticmethod
    def set_chmod(dir_path: str, mode: int = 0o755) -> None:
        """Set execution permissions.

        Set execution permissions for scripts and initialization files in the
        directory.
        """
        # Use an elegant tuple inside endswith to flatten the compound if
        # statement.
        target_extensions = (".sh", ".csh", ".SlackBuild")

        for script in get_all_files(dir_path):
            if script.endswith(target_extensions) or "/rc.d/rc." in script:
                Path(script).chmod(mode)

    def get_pkg_data(self, pkg: str) -> list[Any]:
        """Return structured database registry metadata.

        Return structured database registry metadata for a specific package.
        """
        return self.repodata["pkgs"][pkg]

    @staticmethod
    def get_fname(pkgdata: list[Any]) -> str:
        """Construct the full target filename with extension for downloading.

        Construct the full target filename with extension for downloading.
        """
        pkg_base_name = "-".join(pkgdata[0])
        extension = pkgdata[8]

        return f"{pkg_base_name}.{extension}"

    def check_exist_pkg(self, pkg: str) -> None:
        """Validate if the package exists in the repository metadata.

        Raises:
            ValueError: If the package is missing from the database.

        """
        if pkg not in self.repodata["pkgs"]:
            err = (
                f"{self.meta.clrs['lred']}Package {self.meta.clrs['lcyan']}"
                f"{pkg}{self.meta.clrs['lred']} not found in "
                f"{self.meta.clrs['cyan']}'{self.repo}' "
                f"{self.meta.clrs['lred']}repository.{self.meta.clrs['reset']}"
            )
            raise ValueError(err)

    @staticmethod
    def get_pkg_location(location: str) -> str:
        """Append a trailing slash.

        Append a trailing slash to the repository location path if it exists.
        """
        return f"{location}/" if location else ""
