#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# maindata.py file is part of spman
#
# spman - Slackware package manager
# Home page: https://github.com/MyRequiem/spman
#
# Copyright (c) 2018 Vladimir MyRequiem Astrakhan, Russia
# <mrvladislavovich@gmail.com>
# All rights reserved
# See LICENSE for details.


"""
Main data for program
"""

from platform import machine


class MainData:
    """
    Main data for program
    """
    def __init__(self):
        self.prog_name = 'spman'
        self.prog_version = '2.2.2'
        self.home_page = ('https://github.com/MyRequiem'
                          '/{0}').format(self.prog_name)
        self.mail = '<mrvladislavovich@gmail.com>'
        self.pkg_db_name = 'pkg-db'
        self.pkgs_installed_path = '/var/log/packages/'
        self.configs_path = '/etc/{0}/'.format(self.prog_name)
        self.arch = machine()

        self.clrs = {
            'red': '\x1b[0;31m',
            'lred': '\x1b[1;31m',
            'green': '\x1b[0;32m',
            'lgreen': '\x1b[1;32m',
            'yellow': '\x1b[0;33m',
            'lyellow': '\x1b[1;33m',
            'blue': '\x1b[0;34m',
            'lblue': '\x1b[1;34m',
            'magenta': '\x1b[0;35m',
            'lmagenta': '\x1b[1;35m',
            'cyan': '\x1b[0;36m',
            'lcyan': '\x1b[1;36m',
            'grey': '\x1b[38;5;247m',
            'reset': '\x1b[0m'
        }

    def get_repo_dict(self) -> dict:
        """
        return dict: {'repo_name': 'url', ...} from /etc/spman/repo-list
        """
        repo_dict = {}
        with open('{0}repo-list'.format(self.configs_path)) as config:
            for line in config:
                if not line.startswith('#') and line != '\n':
                    parts = self.process_config_line(line)
                    repo_dict[parts[0]] = parts[1]

        if not config.closed:
            config.close()

        # all repositories are disabled
        if not repo_dict:
            print(('{0}All repositories are disabled\n{1}See config '
                   'file: {2}repo-list{3}').format(self.clrs['lred'],
                                                   self.clrs['grey'],
                                                   self.configs_path,
                                                   self.clrs['reset']))
            raise SystemExit

        return repo_dict

    def get_spman_conf(self) -> dict:
        """
        return dict all options from /etc/spman/spman.conf
        """
        spman_conf = {}
        with open('{0}{1}.conf'.format(self.configs_path,
                                       self.prog_name)) as config:
            for line in config:
                if not line.startswith('#') and line != '\n':
                    parts = self.process_config_line(line, '=')
                    spman_conf[parts[0]] = parts[1]

        if not config.closed:
            config.close()

        # if option is not set, write default
        default_opt = {
            'OS_VERSION': '14.2',
            'OS_LAST_RELEASE': '14.2',
            'REPOS_PATH': '/var/lib/{0}/'.format(self.prog_name),
            'LOGS_PATH': '/var/log/{0}/'.format(self.prog_name),
            'QUEUE_PATH': '/root/{0}/queue/'.format(self.prog_name),
            'BUILD_PATH': '/root/{0}/build/'.format(self.prog_name),
            'OUTPUT_PATH': '/root/{0}/build/'.format(self.prog_name),
            'PKGTYPE': 'txz',
            'TEST_CONNECTION_HOST': '8.8.8.8',
            'TEST_CONNECTION_PORT': '53'
        }

        for opt in default_opt:
            if opt not in spman_conf:
                spman_conf[opt] = default_opt[opt]

        return spman_conf

    def get_blacklist(self) -> list:
        """
        return list blacklisted packages from /etc/spman/blacklist
        """
        blacklist = []
        with open('{0}blacklist'.format(self.configs_path)) as config:
            for line in config:
                if not line.startswith('#') and line != '\n':
                    blacklist.append(line.strip())

        return blacklist

    @staticmethod
    def process_config_line(line: str, sep: str = None) -> list:
        """
        return list [name, value] from line of config file
        """
        parts = line.split(sep)
        parts[0] = parts[0].strip()
        parts[1] = parts[1].strip()
        # add slash at the end of URL or path to dir (if not exist)
        if parts[1].startswith('/') or '://' in parts[1]:
            if not parts[1].endswith('/'):
                parts[1] += '/'
        return [parts[0], parts[1]]
