#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# queue.py file is part of spman
#
# spman - Slackware package manager
# Home page: https://github.com/MyRequiem/spman
#
# Copyright (c) 2018 Vladimir MyRequiem Astrakhan, Russia
# <mrvladislavovich@gmail.com>
# All rights reserved
# See LICENSE for details.


"""
Manage queue for 'sbo' repository
"""

from .getrepodata import GetRepoData
from .maindata import MainData
from .utils import get_indent, get_line


class Queue:
    """
    Manage queue for 'sbo' repository
    """
    def __init__(self):
        self.meta = MainData()
        self.spman_conf = self.meta.get_spman_conf()
        self.queue_file = '{0}queue'.format(self.spman_conf['QUEUE_PATH'])
        self.queue_list = self.get_queue_list()

    def clear(self) -> None:
        """
        clear queue
        """
        open(self.queue_file, 'w').close()
        self.queue_is_empty_message()

    def show(self) -> None:
        """
        print queue
        """
        if not self.queue_list:
            self.queue_is_empty_message()
        else:
            for pkg in self.queue_list:
                print('{0}{1}{2}'.format(self.meta.clrs['green'],
                                         pkg,
                                         self.meta.clrs['reset']))

    def add(self, pkgs: list) -> None:
        """
        add package(s) in the queue
        """
        # if one of the packages not found in the 'sbo'
        # repository - nothing to add to the queue
        self.check_exists_pkgs(pkgs)

        fqueue = open(self.queue_file, 'a')
        for pkg in pkgs:
            if pkg not in self.queue_list:
                fqueue.write('{0}\n'.format(pkg))
                self.print_message(
                    pkg, pkgs, 'added in the queue', ('grey', 'green'))
            else:
                self.print_message(
                    pkg, pkgs, 'is already in the queue', ('grey', 'red'))

        fqueue.close()

    def remove(self, pkgs: list) -> None:
        """
        remove package(s) from the queue
        """
        if not self.queue_list:
            self.queue_is_empty_message()
        else:
            for pkg in pkgs:
                if pkg not in self.queue_list:
                    self.print_message(
                        pkg, pkgs, 'is not in the queue', ('red', 'lcyan'))
                else:
                    self.queue_list.remove(pkg)
                    fqueue = open(self.queue_file, 'w')
                    for package in self.queue_list:
                        fqueue.write('{0}\n'.format(package))
                    fqueue.close()

                    self.print_message(
                        pkg, pkgs, 'removed from the queue', ('grey', 'lcyan'))

    def install(self) -> None:
        """
        download, build and install package(s) on the queue
        """
        if not self.queue_list:
            self.queue_is_empty_message()
        else:
            import os
            from subprocess import call

            from .downloadpkg import DownloadPkg

            pkg_type = self.spman_conf['PKGTYPE']
            os.environ['PKGTYPE'] = pkg_type
            output = self.spman_conf['OUTPUT_PATH']
            os.environ['OUTPUT'] = output

            build_path = self.spman_conf['BUILD_PATH']
            for pkg in self.queue_list:
                DownloadPkg('--src', 'sbo', [pkg]).start()

                slackbuild_dir = '{0}{1}'.format(build_path, pkg)
                if os.path.isdir(slackbuild_dir):
                    os.chdir(slackbuild_dir)
                    ret_code = call('sh {0}.SlackBuild'.format(pkg), shell=True)
                    if ret_code != 0:
                        resp = input(('\n{0}\nPackage {1}: build error. '
                                      'Continue? '
                                      '(y/n): ').format(get_line('!', 80), pkg))
                        if resp not in ['y', 'Y']:
                            raise SystemExit
                    else:
                        call(('/sbin/upgradepkg --install-new --reinstall '
                              '{0}{1}-*.{2}'.format(output,
                                                    pkg,
                                                    pkg_type)),
                             shell=True)

    def get_queue_list(self) -> list:
        """
        return list queue from queue file
        """
        queue_list = []
        with open(self.queue_file) as qfile:
            for line in qfile:
                if line != '\n':
                    queue_list.append(line.strip())

        if not qfile.closed:
            qfile.close()

        return queue_list

    def queue_is_empty_message(self) -> None:
        """
        print message if queue is empty
        """
        print('{0}Queue is empty{1}'.format(self.meta.clrs['grey'],
                                            self.meta.clrs['reset']))

    @staticmethod
    def check_exists_pkgs(pkgs: list) -> None:
        """
        check exists packages on 'sbo' repository
        """
        repodata = GetRepoData('sbo').start()
        for pkg in pkgs:
            if pkg not in repodata['pkgs']:
                from .utils import pkg_not_found_mess
                pkg_not_found_mess(pkg, 'sbo')
                raise SystemExit

    @staticmethod
    def get_max_length_pkg_name(pkgs: list) -> int:
        """
        return max length package name
        """
        max_length = 0
        for pkg in pkgs:
            len_pkg = len(pkg)
            if len_pkg > max_length:
                max_length = len_pkg

        return max_length

    def print_message(self, pkg: str, pkgs: list,
                      mess: str, colors: tuple) -> None:
        """
        print message
        """
        str_pkg = 'Package '
        len_str_pkg = len(str_pkg)
        max_indent = self.get_max_length_pkg_name(pkgs) + len_str_pkg + 1
        indent = get_indent(len(pkg) + len_str_pkg, max_indent)
        print('{0}{1}{2}{3}{4}{0}{5}{6}'.format(self.meta.clrs[colors[0]],
                                                str_pkg,
                                                self.meta.clrs[colors[1]],
                                                pkg,
                                                indent,
                                                mess,
                                                self.meta.clrs['reset']))
