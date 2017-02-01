#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# downloadpkg.py file is part of spman

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
Download packages or sources (SlackBuilds)
"""

from os import (
    path,
    rename,
    remove
)
from shutil import rmtree
from subprocess import call

from .getrepodata import GetRepoData
from .maindata import MainData
from .utils import download


class DownloadPkg:
    """
    Download packages or sources (SlackBuilds)
    """
    def __init__(self, mode: str, repo: str, pkglist: list):
        self.meta = MainData()
        self.os_ver = self.meta.get_os_version()
        # download src or pkg
        self.mode = mode
        # repo name
        self.repo = repo
        # packages list for download
        self.pkglist = pkglist
        self.repo_url = self.meta.get_repo_dict()[self.repo]
        self.repodata = GetRepoData(self.repo).start()
        self.wgetprefix = self.meta.get_spman_conf()['BUILD_PATH']
        self.wgetdir = ('--no-check-certificate -r -nH -ct 0 -w 2 -l 10 '
                        '--cut-dirs={0} --no-parent -R *.meta4,*.mirrorlist,'
                        'index.html*')

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
        arch = 'x86_64' if self.meta.arch == 'x86_64' else 'x86'

        if self.mode == '--pkg':
            # download binary package
            fname = self.get_fname(pkgdata)
            url = '{0}{1}/{2}/{3}/{4}'.format(self.repo_url,
                                              self.os_ver,
                                              arch,
                                              pkg,
                                              fname)
            download(url, self.wgetprefix)
        else:
            # download directory with source code and SlackBuild script
            url = '{0}{1}/build/'.format(
                self.repo_url.replace('sbrepos', 'slackbuilds'), pkg)
            download(url, self.wgetprefix,
                     self.wgetdir.format(self.get_cut_dirs(url)))

            # if dir downloaded, rename to pkgname
            downdir = '{0}build'.format(self.wgetprefix)
            if path.isdir(downdir):
                new_dir_name = '{0}{1}'.format(self.wgetprefix, pkg)
                # if this directory already exists remove it
                if path.isdir(new_dir_name):
                    rmtree(new_dir_name)
                rename(downdir, new_dir_name)
                self.set_chmod(new_dir_name)

    def download_multilib(self, pkgdata: list) -> None:
        """
        download binary package(s) from multilib repository
        """
        fname = self.get_fname(pkgdata)
        location = '{0}/'.format(pkgdata[1]) if pkgdata[1] else ''
        url = '{0}{1}/{2}{3}'.format(self.repo_url,
                                     self.os_ver,
                                     location,
                                     fname)
        download(url, self.wgetprefix)

    def download_slack(self, pkg: str, pkgdata: list) -> None:
        """
        download from slackware repository (directory 'patches')
        """
        arch = '64' if self.meta.arch == 'x86_64' else ''
        repo_url = '{0}slackware{1}-{2}/patches/'.format(self.repo_url,
                                                         arch,
                                                         self.os_ver)

        # kernel packages and kernel source are located in the
        # directory /patches/packages/linux-x.x.x/
        kernel_packages = [
            'kernel-firmware',
            'kernel-generic',
            'kernel-headers',
            'kernel-huge',
            'kernel-modules',
            'kernel-source'
        ]

        # download kernel package or kernel source
        if pkg in kernel_packages:
            kernel_ver = self.get_pkg_data('kernel-source')[0][1]
            fname = self.get_fname(pkgdata)
            url = '{0}packages/linux-{1}/{2}'.format(repo_url,
                                                     kernel_ver,
                                                     fname)
            download(url, self.wgetprefix)
        else:
            if self.mode == '--pkg':
                # download binary package
                fname = self.get_fname(pkgdata)
                url = '{0}packages/{1}'.format(repo_url, fname)
                download(url, self.wgetprefix)
            else:
                # download directory with source code and SlackBuild script
                url = '{0}source/{1}/'.format(repo_url, pkg)
                download(url, self.wgetprefix,
                         self.wgetdir.format(self.get_cut_dirs(url)))

                downdir = '{0}{1}'.format(self.wgetprefix, pkg)
                if path.isdir(downdir):
                    self.set_chmod(downdir)

    def download_sbo(self, pkg: str, pkgdata: list) -> None:
        """
        download SlackBuild script and sources from 'sbo' repository
        """
        fname = '{0}.tar.gz'.format(pkg)
        url = '{0}{1}/{2}/{3}'.format(self.repo_url,
                                      self.os_ver,
                                      pkgdata[1],
                                      fname)
        # downloading SlackBuild script
        download(url, self.wgetprefix)

        # before unpack archive:
        # if dir with name pkg already exists remove it
        slackbuil_dir = '{0}{1}/'.format(self.wgetprefix, pkg)
        if path.isdir(slackbuil_dir):
            rmtree(slackbuil_dir)

        # unpack SlackBuild archive
        import tarfile
        archive = '{0}{1}'.format(self.wgetprefix, fname)
        tar = tarfile.open(archive)
        tar.extractall(self.wgetprefix)
        # remove archive
        remove(archive)
        self.set_chmod(slackbuil_dir)

        # download sources
        for url in pkgdata[7]:
            download(url, slackbuil_dir)

    @staticmethod
    def set_chmod(path_to_dir: str) -> None:
        """
        chmod 744 for *.SlackBuild and *.sh into dir
        """
        call(('find {0} -type f -a \\( '
              '-name "*.SlackBuild" -o '
              '-name "*.sh" -o '
              '-name "*.build" \\) -a '
              '! -name "doinst.sh" '
              '-exec chmod 744 {{}} \\;').format(path_to_dir),
             shell=True)

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
            from .utils import pkg_not_found_mess
            pkg_not_found_mess(pkg, self.repo)
            return False

        return True

    @staticmethod
    def get_cut_dirs(url: str) -> int:
        """
        return count cut dirs from url for wget, when download directory
        """
        if not url.endswith('/'):
            url += '/'

        return len(url.split('/')[3:-2])