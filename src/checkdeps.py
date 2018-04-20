#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# sbbcheck.py file is part of spman
#
# spman - Slackware package manager
# Home page: https://github.com/MyRequiem/spman
#
# Copyright (c) 2018 Vladimir MyRequiem Astrakhan, Russia
# <mrvladislavovich@gmail.com>
# All rights reserved
# See LICENSE for details.


"""
Search dependency problems in the system packages using 'sbbdep' or 'ldd' tool.
"""

import os
import subprocess

from .maindata import MainData
from .pkgs import Pkgs
from .utils import (
    get_line,
    get_indent
)


class CheckDeps:
    """
    Search dependency problems in the system packages
    using 'sbbdep' or 'ldd' tool.
    """
    def __init__(self, tool: str):
        self.tool = tool
        self.meta = MainData()
        self.pkgs = Pkgs()

    def start(self) -> None:
        """
        start search dependency problems
        """
        if self.tool == '--sbbdep':
            # if sbbdep package not installed
            if not self.pkgs.find_pkgs_on_system('sbbdep'):
                print(('You need to install {0}\'sbbdep\'{1} package '
                       'from \'sbo\' repository:\n'
                       '  # spman --update\n'
                       '  # spman --queue --clear\n'
                       '  # spman --queue --add sbbdep\n'
                       '  # spman --queue --install').format(
                           self.meta.clrs['lcyan'], self.meta.clrs['reset']))
                raise SystemExit

            self.sbbdep()
        else:
            self.ldd()

    def sbbdep(self) -> None:
        """
        check using 'sbbdep' tool
        """
        # updata sbbdep database
        subprocess.call('sbbdep', shell=True)

        sbblog = '/tmp/sbbcheck.log'
        # create/clear log file
        open(sbblog, 'w').close()
        logfile = open(sbblog, 'a')

        numpkg = 1
        brokenpkg = 0
        for pkg in self.pkgs.find_pkgs_on_system():
            pkgname = self.pkgs.get_parts_pkg_name(pkg)[0]
            print('{0}.{1}{2}Checking {3}'
                  '{4}'.format(numpkg,
                               get_indent(len(str(numpkg)), 5),
                               self.meta.clrs['yellow'],
                               self.meta.clrs['lmagenta'],
                               pkgname),
                  end='')

            errors = self.get_error_lines(
                'sbbdep --ldd {0}{1}; exit 0'.format(
                    self.meta.pkgs_installed_path, pkg))

            if errors:
                brokenpkg += 1
                self.print_rezult('Error', 'red', pkgname)
                logfile.write('{0}\n{1}\n'.format(
                    pkgname, get_line('-', len(pkgname) + 1)))

                for line in errors:
                    self.print_error_string(line)
                    logfile.write('{0}\n'.format(line))
                logfile.write('\n')
            else:
                self.print_rezult('Ok', 'green', pkgname)

            numpkg += 1

        logfile.close()

        if brokenpkg:
            self.print_rezult(('\n{0} packages have '
                               'problems.').format(brokenpkg), 'red')
            print('Log file: {0}{1}{2}'.format(self.meta.clrs['grey'],
                                               sbblog,
                                               self.meta.clrs['reset']),
                  end='\n\n')
        else:
            self.print_rezult(('\nCongratulations !!! sbbdep not found '
                               'problems with dependencies.'), 'green')
            print()

    def ldd(self) -> None:
        """
        check using 'ldd' tool
        """
        from .utils import get_all_files

        directories = [
            '/bin/',
            '/sbin/',
            '/lib/',
            '/lib64/',
            '/usr/bin/',
            '/usr/sbin/',
            '/usr/lib/',
            '/usr/lib64/',
            '/usr/local/bin/',
            '/usr/local/sbin/',
            '/usr/local/lib/',
            '/usr/local/lib64/',
            '/usr/X11R6/bin/',
            '/usr/X11R6/lib/',
            '/usr/X11R6/lib64/',
            '/opt/',
            '/usr/games/',
            '/usr/share/texmf/bin/'
        ]

        lddlog = '/tmp/ldd.log'
        # create/clear log file
        open(lddlog, 'w').close()
        logfile = open(lddlog, 'a')

        numstr = 1
        brokenfiles = 0
        for directory in directories:
            if not os.path.isdir(directory):
                continue

            for fls in get_all_files(directory):
                if self.is_binary(fls):
                    errors = self.get_error_lines('ldd {0}; exit 0'.format(fls))
                    color = 'reset' if not errors else 'red'
                    print('{0}.{1}{2}{3}'
                          '{4}'.format(numstr,
                                       get_indent(len(str(numstr)), 8),
                                       self.meta.clrs[color],
                                       fls,
                                       self.meta.clrs['reset']))
                    if errors:
                        brokenfiles += 1
                        logfile.write('{0}\n{1}\n'.format(
                            fls, get_line('-', len(fls) + 1)))

                        for line in errors:
                            self.print_error_string(line)
                            logfile.write('{0}\n'.format(line))
                        logfile.write('\n')

                    numstr += 1

        logfile.close()

        if brokenfiles:
            self.print_rezult(('\n{0} file(s) have '
                               'problems.').format(brokenfiles), 'red')
            print('Log file: {0}{1}{2}'.format(self.meta.clrs['grey'],
                                               lddlog,
                                               self.meta.clrs['reset']),
                  end='\n\n')
        else:
            self.print_rezult(('\nCongratulations !!! ldd not found '
                               'problems with dependencies.'), 'green')
            print()

    def get_error_lines(self, command: str) -> list:
        """
        return list lines with errors
        """
        proc = subprocess.check_output(command,
                                       stderr=subprocess.STDOUT,
                                       shell=True)

        errors = []
        for line in proc.decode('utf-8').split('\n'):
            line = line.strip()
            nover = 'no version information'
            if self.tool == '--sbbdep':
                if ('can not read file:' in line or
                        nover in line or
                        line.startswith('for /')):
                    errors.append(line)
            else:
                if 'not found' in line or nover in line:
                    errors.append(line)

        return errors

    def print_error_string(self, line: str) -> None:
        """
        print error string
        """
        print('{0}{1}{2}{3}'.format(get_line(' ', 8),
                                    self.meta.clrs['red'],
                                    line,
                                    self.meta.clrs['reset']))

    def print_rezult(self, string: str, color: str, pkgname: str = '') -> None:
        """
        print rezult string
        """
        print('{0}{1}{2}{3}'.format(get_indent(len(pkgname) + 15, 50),
                                    self.meta.clrs[color],
                                    string,
                                    self.meta.clrs['reset']))

    @staticmethod
    def is_binary(filepath: str) -> bool:
        """
        return True, if file is binary
        """
        filename = filepath.split('/')[-1]
        ext = ('.txt', '.py', '.la', '.sh', '.bash', '.js')
        # if file is executable or library
        if (not filename.endswith(ext) and not os.path.islink(filepath) and
                (os.access(filepath, os.X_OK) or '.so' in filename)):
            return True

        return False
