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
from tarfile import open as taropen

from .download import Download
from .getrepodata import GetRepoData
from .maindata import MainData
from .utils import get_all_files, pkg_not_found_mess, url_is_alive


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

            # packages from source/x/x11 (no patches)
            if location.endswith('/x/'):
                httpresponse = url_is_alive(url)
                if httpresponse:
                    httpresponse.close()
                else:
                    location = location + 'x11/'
                    url = '{0}/{1}'.format(repo_url, location)

                    for xdir in ['build', 'configure', 'doinst.sh', 'makepkg']:
                        print(('{0}Search for file: {1}{2}/{3}'
                               '{4}').format(self.meta.clrs['grey'],
                                             location,
                                             xdir,
                                             pkg,
                                             self.meta.clrs['reset']))
                        xurl = '{0}{1}/{2}'.format(url, xdir, pkg)
                        httpresponse = url_is_alive(xurl)
                        if httpresponse:
                            httpresponse.close()
                            Download(xurl, '{0}/{1}'.format(dest_dir,
                                                            xdir)).start()
                        else:
                            if xdir == 'configure':
                                print(('{0}Downloading: configure'
                                       '{1}').format(self.meta.clrs['grey'],
                                                     self.meta.clrs['reset']))
                                Download(xurl.replace(pkg, xdir),
                                         '{0}/{1}'.format(dest_dir,
                                                          xdir)).start()

                    for xdir in ['patch', 'post-install']:
                        print(('{0}Search for directory: {1}{2}/{3}/'
                               '{4}').format(self.meta.clrs['grey'],
                                             location,
                                             xdir,
                                             pkg,
                                             self.meta.clrs['reset']))
                        xurl = '{0}{1}/{2}'.format(url, xdir, pkg)
                        httpresponse = url_is_alive(xurl)
                        if httpresponse:
                            httpresponse.close()
                            Download(xurl, '{0}/{1}/{2}'.format(dest_dir,
                                                                xdir,
                                                                pkg)).start()

                        print(('{0}Search for file: {1}{2}/{3}.{2}'
                               '{4}').format(self.meta.clrs['grey'],
                                             location,
                                             xdir,
                                             pkg,
                                             self.meta.clrs['reset']))
                        xurl = '{0}{1}/{2}.{1}'.format(url, xdir, pkg)
                        httpresponse = url_is_alive(xurl)
                        if httpresponse:
                            httpresponse.close()
                            Download(xurl, '{0}/{1}'.format(dest_dir,
                                                            xdir)).start()

                    xdir = 'slack-desc'
                    print(('{0}Downloading: {1}'
                           '{2}').format(self.meta.clrs['grey'],
                                         xdir,
                                         self.meta.clrs['reset']))
                    xurl = '{0}{1}/{2}'.format(url, xdir, pkg)
                    Download(xurl, '{0}/{1}'.format(dest_dir, xdir)).start()

                    # source code
                    source = '{0}-{1}.tar.xz'.format(pkg, pkgdata[0][1])
                    print(('{0}Search for source code: '
                           '{1}{2}').format(self.meta.clrs['grey'],
                                            source,
                                            self.meta.clrs['reset']))
                    for xdir in ['src/app', 'src/data', 'src/doc',
                                 'src/driver', 'src/font', 'src/lib',
                                 'src/proto', 'src/util', 'src/xcb',
                                 'src/xserver']:
                        print(('{0}Scan directory: {1}{2}/'
                               '{3}').format(self.meta.clrs['grey'],
                                             location,
                                             xdir,
                                             self.meta.clrs['reset']))
                        xurl = '{0}{1}/{2}'.format(url, xdir, source)
                        httpresponse = url_is_alive(xurl)
                        if httpresponse:
                            httpresponse.close()
                            Download(xurl, '{0}/{1}'.format(dest_dir,
                                                            xdir)).start()
                            break

                    for script in ['arch.use.flags', 'modularize', 'noarch',
                                   'package-blacklist', 'x11.SlackBuild']:
                        print(('{0}Downloading: {1}{2}'
                               '{3}').format(self.meta.clrs['grey'],
                                             location,
                                             script,
                                             self.meta.clrs['reset']))
                        Download(url + script, dest_dir).start()

                    if path.isdir(dest_dir):
                        self.set_chmod(dest_dir)
                    return
            elif location.endswith('/kde/'):
                url = '{0}/{1}'.format(repo_url, location)
                for kdir in ['build', 'cmake', 'docs', 'doinst.sh', 'makepkg']:
                    print(('{0}Search for file: {1}{2}/{3}'
                           '{4}').format(self.meta.clrs['grey'],
                                         location,
                                         kdir,
                                         pkg,
                                         self.meta.clrs['reset']))
                    xurl = '{0}{1}/{2}'.format(url, kdir, pkg)
                    httpresponse = url_is_alive(xurl)
                    if httpresponse:
                        httpresponse.close()
                        Download(xurl, '{0}/{1}'.format(dest_dir,
                                                        kdir)).start()
                    else:
                        if kdir == 'cmake':
                            for file_ in [kdir, 'kdeaccessibility', 'kdeadmin',
                                          'kdebase', 'kdebindings']:
                                print(('{0}Downloading: {1}{2}/{3}'
                                       '{4}').format(self.meta.clrs['grey'],
                                                     location,
                                                     kdir,
                                                     file_,
                                                     self.meta.clrs['reset']))
                                xurl = '{0}{1}/{2}'.format(url, kdir, file_)
                                Download(xurl, '{0}/{1}'.format(dest_dir,
                                                                kdir)).start()

                kdir = 'modules'
                xurl = '{0}{1}'.format(url, kdir)
                print(('{0}Downloading directory: {1}{2}/'
                       '{3}').format(self.meta.clrs['grey'],
                                     location,
                                     kdir,
                                     self.meta.clrs['reset']))
                Download(xurl, '{0}/{1}'.format(dest_dir, kdir)).start()

                for kdir in ['patch', 'post-install', 'pre-install']:
                    print(('{0}Search for directory: {1}{2}/{3}/'
                           '{4}').format(self.meta.clrs['grey'],
                                         location,
                                         kdir,
                                         pkg,
                                         self.meta.clrs['reset']))
                    xurl = '{0}{1}/{2}'.format(url, kdir, pkg)
                    httpresponse = url_is_alive(xurl)
                    if httpresponse:
                        httpresponse.close()
                        Download(xurl, '{0}/{1}/{2}'.format(dest_dir,
                                                            kdir,
                                                            pkg)).start()

                    print(('{0}Search for file: {1}{2}/{3}.{2}'
                           '{4}').format(self.meta.clrs['grey'],
                                         location,
                                         kdir,
                                         pkg,
                                         self.meta.clrs['reset']))
                    xurl = '{0}{1}/{2}.{1}'.format(url, kdir, pkg)
                    httpresponse = url_is_alive(xurl)
                    if httpresponse:
                        httpresponse.close()
                        Download(xurl, '{0}/{1}'.format(dest_dir,
                                                        kdir)).start()

                kdir = 'slack-desc'
                print(('{0}Downloading: {1}'
                       '{2}').format(self.meta.clrs['grey'],
                                     kdir,
                                     self.meta.clrs['reset']))
                xurl = '{0}{1}/{2}'.format(url, kdir, pkg)
                Download(xurl, '{0}/{1}'.format(dest_dir, kdir)).start()

                # source code
                source = '{0}-{1}.tar.xz'.format(pkg, pkgdata[0][1])
                print(('{0}Search for source code: '
                       '{1}{2}').format(self.meta.clrs['grey'],
                                        source,
                                        self.meta.clrs['reset']))
                for kdir in ['src', 'src/extragear']:
                    print(('{0}Scan directory: {1}{2}/'
                           '{3}').format(self.meta.clrs['grey'],
                                         location,
                                         kdir,
                                         self.meta.clrs['reset']))
                    xurl = '{0}{1}/{2}'.format(url, kdir, source)
                    httpresponse = url_is_alive(xurl)
                    if httpresponse:
                        httpresponse.close()
                        Download(xurl, '{0}/{1}'.format(dest_dir,
                                                        kdir)).start()
                        break

                for script in ['KDE.SlackBuild', 'KDE.options', 'modularize',
                               'noarch', 'package-blacklist']:
                    print(('{0}Downloading: {1}{2}'
                           '{3}').format(self.meta.clrs['grey'],
                                         location,
                                         script,
                                         self.meta.clrs['reset']))
                    Download(url + script, dest_dir).start()

                if path.isdir(dest_dir):
                    self.set_chmod(dest_dir)
                return
            elif location.endswith('/kdei/'):
                short_pkg_name = '-'.join(pkg.split('-')[:-1])
                url = '{0}/{1}{2}'.format(repo_url, location, short_pkg_name)

                kdir = 'slack-desc'
                print(('{0}Downloading: {1}'
                       '{2}').format(self.meta.clrs['grey'],
                                     kdir,
                                     self.meta.clrs['reset']))
                Download('{0}/{1}/{1}.{2}'.format(url, kdir, pkg),
                         '{0}/{1}'.format(dest_dir, kdir)).start()

                for script in ['{0}.SlackBuild'.format(short_pkg_name),
                               'languages']:
                    print(('{0}Downloading file: {1}'
                           '{2}').format(self.meta.clrs['grey'],
                                         script,
                                         self.meta.clrs['reset']))
                    Download('{0}/{1}'.format(url, script), dest_dir).start()

                source = '{0}-{1}.tar.xz'.format(pkg, pkgdata[0][1])
                print(('{0}Download source code: {1}'
                       '{2}').format(self.meta.clrs['grey'],
                                     source,
                                     self.meta.clrs['reset']))
                Download('{0}/{1}'.format(url, source), dest_dir).start()

                if short_pkg_name == 'kde-l10n':
                    for kdir in ['kdepim-l10n', 'local.options']:
                        print(('{0}Download directory: {1}{2}/{3}/'
                               '{4}').format(self.meta.clrs['grey'],
                                             location,
                                             short_pkg_name,
                                             kdir,
                                             self.meta.clrs['reset']))
                        Download('{0}/{1}'.format(url, kdir),
                                 '{0}/{1}'.format(dest_dir, kdir)).start()

                if path.isdir(dest_dir):
                    self.set_chmod(dest_dir)
                return

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
        # unpack SlackBuild archive
        archive = '{0}{1}'.format(self.dest, fname)
        tar = taropen(archive)
        tar.extractall(self.dest)
        # remove archive
        remove(archive)
        # download sources
        for url in pkgdata[7]:
            Download(url, '{0}{1}/'.format(self.dest, pkg)).start()

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
