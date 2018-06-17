#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# getrepodata.py file is part of spman
#
# spman - Slackware package manager
# Home page: https://github.com/MyRequiem/spman
#
# Copyright (c) 2018 Vladimir MyRequiem Astrakhan, Russia
# <mrvladislavovich@gmail.com>
# All rights reserved
# See LICENSE for details.


"""
Get data from the repository
"""

from .maindata import MainData
from .pkgs import Pkgs


class GetRepoData:
    """
    get data from the repository
    """
    def __init__(self, reponame: str):
        self.reponame = reponame
        self.meta = MainData()
        self.pkgs = Pkgs()
        self.spman_conf = self.meta.get_spman_conf()
        # compressed and uncompressed total packages size
        self.comp = [0, 0]
        self.pkgname = ''
        self.rdata = {
            # date and time of the last update on the server
            'lupd': '',
            # number of pkgs
            'numpkgs': 0,
            # total compressed size
            'comp': '',
            # total uncompressed size
            'uncomp': '',
            # list data for packages
            'pkgs': {
                # 'pkg_name': [
                #   [0] - list parts of package name (for sbo - only version)
                #   [1] - location package (development, audio, system etc.)
                #   [2] - size compressed package (only for NON sbo repo)
                #   [3] - size uncompressed package (only for NON sbo repo)
                #   [4] - list of dependencies for package
                #   [5] - package description
                #   [6] - list of SlackBuild files (only for sbo repo)
                #   [7] - list of urls for download (only for sbo repo)
                #   [8] - extention package
                # ]
            }
        }

    def start(self) -> dict:
        """
        start grab data from PACKAGES.TXT (SLACKBUILDS.TXT)
        """
        if self.reponame == 'sbo':
            # if repository name is 'sbo', last date update
            # is only available in the log file
            dfile = '{0}{1}/ChangeLog.txt'.format(self.spman_conf['LOGS_PATH'],
                                                  self.reponame)
            with open(dfile) as datafile:
                for line in datafile:
                    # first line of the file contains
                    # the date of the last update
                    if line != '\n':
                        self.rdata['lupd'] = line.strip()
                    break

            if not datafile.closed:
                datafile.close()

        fname = 'SLACKBUILDS.TXT' if self.reponame == 'sbo' else 'PACKAGES.TXT'
        dfile = '{0}{1}/{2}'.format(self.spman_conf['REPOS_PATH'],
                                    self.reponame,
                                    fname)

        with open(dfile) as datafile:
            for line in datafile:
                # last update
                if (not self.rdata['lupd'] and
                        line.startswith('PACKAGES.TXT; ')):
                    self.rdata['lupd'] = self.get_line_value(line, '; ')
                    continue

                if self.reponame != 'sbo':
                    self.get_non_sbo_data(line)
                else:
                    self.get_sbo_data(line)

        if not datafile.closed:
            datafile.close()

        # read ALL-PACKAGES.TXT
        if self.reponame == 'slack':
            parts = dfile.split('/')
            dfile = '{0}/ALL-{1}'.format('/'.join(parts[:-1]), parts[-1])
            with open(dfile) as datafile:
                for line in datafile:
                    self.get_non_sbo_data(line)

        if not datafile.closed:
            datafile.close()

        self.rdata['numpkgs'] = len(self.rdata['pkgs'])
        if self.comp[0]:
            self.rdata['comp'] = self.get_human_readable_size(self.comp[0])
            self.rdata['uncomp'] = self.get_human_readable_size(self.comp[1])

        return self.rdata

    def get_non_sbo_data(self, line: str) -> None:
        """
        get non sbo data
        """
        rdata = self.rdata['pkgs']
        if line.startswith('PACKAGE NAME: '):
            pkg = self.get_line_value(line, ': ')
            parts = self.pkgs.get_parts_pkg_name(pkg)
            if parts[0] not in self.rdata['pkgs']:
                self.pkgname = parts[0]
                rdata[self.pkgname] = self.get_list_new_pkg()
                # list parts of package name
                rdata[self.pkgname][0] = parts
                # package extention
                rdata[self.pkgname][8] = pkg.split('.')[-1]
            else:
                self.pkgname = ''
        elif self.pkgname:
            if line.startswith('PACKAGE LOCATION: '):
                val = self.get_line_value(line, ': ')
                rdata[self.pkgname][1] = '/'.join(val.split('/')[1:])
            elif line.startswith('PACKAGE SIZE (compressed): '):
                self.process_size_pkg(line, 0)
            elif line.startswith('PACKAGE SIZE (uncompressed): '):
                self.process_size_pkg(line, 1)
            elif line.startswith('PACKAGE REQUIRED: '):
                self.get_req_pkg(line, ',')
            elif line.startswith('{0}:'.format(self.pkgname)):
                val = self.get_line_desc(line, '{0}:'.format(self.pkgname))
                # only not empty strings
                if val:
                    rdata[self.pkgname][5].append(val)

    def get_sbo_data(self, line: str) -> None:
        """
        get sbo data
        """
        if line.startswith('SLACKBUILD NAME: '):
            self.pkgname = self.get_line_value(line, ': ')
            self.rdata['pkgs'][self.pkgname] = self.get_list_new_pkg()
        elif line.startswith('SLACKBUILD VERSION: '):
            val = self.get_line_value(line, ': ')
            self.rdata['pkgs'][self.pkgname][0] = val
        elif line.startswith('SLACKBUILD LOCATION: '):
            val = self.get_line_value(line, ': ').split('/')[1]
            self.rdata['pkgs'][self.pkgname][1] = val
        elif line.startswith('SLACKBUILD REQUIRES: '):
            self.get_req_pkg(line)
        elif line.startswith('SLACKBUILD SHORT DESCRIPTION: '):
            val = self.get_line_desc(line, ': ')
            self.rdata['pkgs'][self.pkgname][5].append(val)
        elif line.startswith('SLACKBUILD FILES: '):
            val = self.get_line_value(line, ': ')
            for sfile in val.split():
                self.rdata['pkgs'][self.pkgname][6].append(sfile.strip())
        elif line.startswith('SLACKBUILD DOWNLOAD: '):
            self.get_dwnld_urls(line)
        elif (self.meta.arch == 'x86_64' and
              line.startswith('SLACKBUILD DOWNLOAD_x86_64: ')):
            self.get_dwnld_urls(line)

    def get_dwnld_urls(self, line: str) -> None:
        """
        get download urls
        """
        val = self.get_line_value(line, ': ')
        if val and val != 'UNSUPPORTED' and val != 'UNTESTED':
            urls = []
            for url in val.split():
                urls.append(url.strip())

            self.rdata['pkgs'][self.pkgname][7] = urls

    @staticmethod
    def get_line_desc(line: str, sep: str) -> str:
        """
        get description line value
        """
        return sep.join(line.split(sep)[1:]).strip()

    def get_req_pkg(self, line: str, sep: str = None) -> None:
        """
        get list dependencies for package
        """
        str_req = self.get_line_value(line, ': ').split(sep)
        for req in str_req:
            if req and req != '%README%':
                self.rdata['pkgs'][self.pkgname][4].append(req.strip())

    def process_size_pkg(self, line: str, ind: int) -> None:
        """
        process size package
        """
        # if ind == 0 then compressed size, else uncompressed
        val = int(self.get_line_value(line, ': ').split()[0].strip())
        self.comp[ind] += val
        hval = self.get_human_readable_size(val)
        self.rdata['pkgs'][self.pkgname][ind + 2] = hval

    @staticmethod
    def get_list_new_pkg() -> list:
        """
        return list data for new package
        """
        return ['', '', '', '', [], [], [], [], '']

    @staticmethod
    def get_line_value(line: str, sep: str) -> str:
        """
        return value of line parameter
        """
        return line.split(sep)[1].strip()

    @staticmethod
    def get_human_readable_size(val: int) -> str:
        """
        return human readable size package
        """
        if val < 1024:
            return '{0} Kb'.format(val)

        hval = val / 1024
        if hval < 1024:
            return '{0:.2f} Mb'.format(hval)

        return '{0:.2f} Gb'.format(hval / 1024)
