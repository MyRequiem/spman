#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# downloadpkg.py file is part of spman
#
# spman - Slackware package manager
# Home page: https://github.com/MyRequiem/spman
#
# Copyright (c) 2018 Vladimir MyRequiem Astrakhan, Russia
# <mrvladislavovich@gmail.com>
# All rights reserved
# See LICENSE for details.


"""
Download packages or sources (SlackBuilds)
"""

from os import chmod, path, remove
from shutil import rmtree
from tarfile import open as taropen

from .download import Download
from .getrepodata import GetRepoData
from .maindata import MainData
from .utils import get_all_files, pkg_not_found_mess


class DownloadPkg:
    """
    Download packages or sources (SlackBuilds)
    """
    def __init__(self, mode: str, repo: str, pkglist: list):
        self.meta = MainData()
        self.spman_conf = self.meta.get_spman_conf()
        self.os_ver = self.spman_conf['OS_VERSION']
        # download src or pkg
        self.mode = mode
        # repo name
        self.repo = repo
        # packages list for download
        self.pkglist = pkglist
        self.repo_url = self.meta.get_repo_dict()[self.repo]
        self.repodata = GetRepoData(self.repo).start()
        self.dest = self.spman_conf['BUILD_PATH']

    def start(self) -> None:
        """
        start download
        """
        for pkg in self.pkglist:
            if self.check_exist_pkg(pkg):
                pkgdata = self.get_pkg_data(pkg)

                if self.repo == 'alienbob':
                    self.download_alienbob(pkg, pkgdata)

                if self.repo == 'multilib':
                    self.download_multilib(pkgdata)

                if self.repo == 'slack':
                    self.download_slack(pkg, pkgdata)

                if self.repo == 'sbo':
                    self.download_sbo(pkg, pkgdata)

    def download_alienbob(self, pkg: str, pkgdata: list) -> None:
        """
        download from alienbob repository
        """
        arch = self.meta.arch if self.meta.arch == 'x86_64' else 'x86'

        if self.mode == '--pkg':
            # download binary package
            fname = self.get_fname(pkgdata)
            url = '{0}{1}/{2}/{3}/{4}'.format(self.repo_url,
                                              self.os_ver,
                                              arch,
                                              pkg,
                                              fname)
            Download(url, self.dest).start()
        else:
            # download directory with source code and SlackBuild script
            url = '{0}{1}/build/'.format(
                self.repo_url.replace('sbrepos', 'slackbuilds'), pkg)
            dest_dir = '{0}{1}/'.format(self.dest, pkg)
            Download(url, dest_dir).start()

            if path.isdir(dest_dir):
                self.set_chmod(dest_dir)

    def download_multilib(self, pkgdata: list) -> None:
        """
        download binary package(s) from multilib repository
        """
        fname = self.get_fname(pkgdata)
        url = '{0}{1}/{2}{3}'.format(self.repo_url,
                                     self.os_ver,
                                     self.get_pkg_location(pkgdata[1]),
                                     fname)
        Download(url, self.dest).start()

    def download_slack(self, pkg: str, pkgdata: list) -> None:
        """
        download from slackware repository
        """
        arch = '64' if self.meta.arch == 'x86_64' else ''
        repo_url = '{0}slackware{1}-{2}'.format(self.repo_url,
                                                arch,
                                                self.os_ver)

        # patched kernel packages and kernel source (for stable Slackware
        # versions) are located in the directory patches/packages/linux-x.x.x/
        kernel_packages = [
            'kernel-firmware',
            'kernel-generic',
            'kernel-headers',
            'kernel-huge',
            'kernel-modules',
            'kernel-source'
        ]

        location = self.get_pkg_location(pkgdata[1])
        if self.mode == '--pkg' or pkg in kernel_packages:
            # download binary package
            fname = self.get_fname(pkgdata)
            url = '{0}/{1}{2}'.format(repo_url, location, fname)
            Download(url, self.dest).start()
        else:
            # download directory with source code and SlackBuild script
            replace_str = 'packages'
            if self.os_ver == 'current' or not location.startswith('patches/'):
                replace_str = 'slackware{0}'.format(arch)

            location = location.replace(replace_str, 'source')
            url = '{0}/{1}{2}/'.format(repo_url, location, pkg)

            dest_dir = '{0}{1}'.format(self.dest, pkg)
            Download(url, dest_dir).start()

            if path.isdir(dest_dir):
                self.set_chmod(dest_dir)

    def download_sbo(self, pkg: str, pkgdata: list) -> None:
        """
        download SlackBuild script and sources from 'sbo' repository
        """
        if self.os_ver == 'current':
            self.os_ver = self.spman_conf['OS_LAST_RELEASE']

        fname = '{0}.tar.gz'.format(pkg)
        url = '{0}{1}/{2}/{3}'.format(self.repo_url,
                                      self.os_ver,
                                      pkgdata[1],
                                      fname)
        # downloading SlackBuild script
        Download(url, self.dest).start()

        # before unpack archive:
        # if dir with name pkg already exists remove it
        slackbuil_dir = '{0}{1}/'.format(self.dest, pkg)
        if path.isdir(slackbuil_dir):
            rmtree(slackbuil_dir)

        # unpack SlackBuild archive
        archive = '{0}{1}'.format(self.dest, fname)
        tar = taropen(archive)
        tar.extractall(self.dest)
        # remove archive
        remove(archive)

        # download sources
        for url in pkgdata[7]:
            Download(url, slackbuil_dir).start()

    @staticmethod
    def set_chmod(dir_path: str, mode: int = 0o755) -> None:
        """
        chmod (default: 0755) for *.SlackBuild, *.sh, *.csh, rc.d/rc.* into dir
        """
        for script in get_all_files(dir_path):
            if (script.endswith('.sh') or
                    script.endswith('.csh') or
                    script.endswith('.SlackBuild') or
                    '/rc.d/rc.' in script):
                chmod(script, 0o755)

    def get_pkg_data(self, pkg: str) -> list:
        """
        return list data of package
        """
        return self.repodata['pkgs'][pkg]

    @staticmethod
    def get_fname(pkgdata: list) -> str:
        """
        return file name for download
        """
        return '{0}.{1}'.format('-'.join(pkgdata[0]),
                                pkgdata[8])

    def check_exist_pkg(self, pkg: str) -> bool:
        """
        check exist package on repository
        """
        if pkg not in self.repodata['pkgs']:
            pkg_not_found_mess(pkg, self.repo)
            return False

        return True

    @staticmethod
    def get_pkg_location(location: str) -> str:
        """
        return location package in repository
        """
        return '{0}/'.format(location) if location else ''
