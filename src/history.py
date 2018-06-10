#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# history.py file is part of spman
#
# spman - Slackware package manager
# Home page: https://github.com/MyRequiem/spman
#
# Copyright (c) 2018 Vladimir MyRequiem Astrakhan, Russia
# <mrvladislavovich@gmail.com>
# All rights reserved
# See LICENSE for details.


"""
show/update package history
"""

from os import listdir

from .maindata import MainData
from .pkgs import Pkgs
from .utils import get_indent


class History:
    """
    show/update package history
    """
    def __init__(self, update: bool):
        self.update = update
        self.pkglist_now = []
        self.pkglist_db = []
        self.meta = MainData()
        self.get_parts_pkg_name = Pkgs().get_parts_pkg_name

    def start(self) -> None:
        """
        start
        """
        if self.update:
            from .utils import update_pkg_db
            update_pkg_db()
            print('The database of local packages has been updated.')
        else:
            self.show_history()

    def show_history(self) -> None:
        """
        show package history
        """
        # list of installed packages divided into parts
        for pkg in sorted(listdir(self.meta.pkgs_installed_path)):
            self.append_parts_pkd(pkg, self.pkglist_now)

        # list of packages in the database divided into parts
        last_update = ''
        db_path = '{0}{1}'.format(self.meta.get_spman_conf()['REPOS_PATH'],
                                  self.meta.pkg_db_name)
        with open(db_path, 'r') as pkgdb:
            for pkg in pkgdb:
                pkg = pkg.rstrip()
                if pkg.startswith('Last database update:'):
                    last_update = pkg
                else:
                    self.append_parts_pkd(pkg, self.pkglist_db)

        if not pkgdb.closed:
            pkgdb.close()

        removed_pkgs = []
        updated_pkgs = []
        for ind1 in range(0, len(self.pkglist_db), 4):
            pkg_db_name = self.pkglist_db[ind1]
            part2db = self.pkglist_db[ind1 + 1]
            part3db = self.pkglist_db[ind1 + 2]
            part4db = self.pkglist_db[ind1 + 3]
            full_name_db = '-'.join([pkg_db_name, part2db, part3db, part4db])
            try:
                ind2 = self.pkglist_now.index(pkg_db_name)
                part2now = self.pkglist_now[ind2 + 1]
                part3now = self.pkglist_now[ind2 + 2]
                part4now = self.pkglist_now[ind2 + 3]

                if (part2db != part2now or part3db != part3now or
                        part4db != part4now):
                    full_name_now = '-'.join([self.pkglist_now[ind2],
                                              part2now,
                                              part3now,
                                              part4now]
                                             )

                    updated_pkgs.append((full_name_db, full_name_now))
            except ValueError:
                removed_pkgs.append(full_name_db)

        new_pkgs = []
        for ind in range(0, len(self.pkglist_now), 4):
            if not self.pkglist_now[ind] in self.pkglist_db:
                new_pkgs.append('-'.join([self.pkglist_now[ind],
                                          self.pkglist_now[ind + 1],
                                          self.pkglist_now[ind + 2],
                                          self.pkglist_now[ind + 3]]
                                         )
                                )
        print(('{0}\n{1}Update database of local packages: # '
               'spman --history --update{2}').format(last_update,
                                                     self.meta.clrs['grey'],
                                                     self.meta.clrs['reset']),
              end='\n\n')

        print('New packages:     {0}'.format(len(new_pkgs)))
        for pkg in new_pkgs:
            print('{0}{1}{2}'.format(self.meta.clrs['green'],
                                     pkg,
                                     self.meta.clrs['reset'],))

        new_line = '\n' if new_pkgs else ''
        print('{0}Updated packages: {1}'.format(new_line, len(updated_pkgs)))
        for pkg in updated_pkgs:
            print('{0}{3}{2}{5}--> '
                  '{1}{4}{2}'.format(self.meta.clrs['yellow'],
                                     self.meta.clrs['cyan'],
                                     self.meta.clrs['reset'],
                                     pkg[0],
                                     pkg[1],
                                     get_indent(len(pkg[0]), 37)))

        new_line = '\n' if updated_pkgs else ''
        print('{0}Removed packages: {1}'.format(new_line, len(removed_pkgs)))
        for pkg in removed_pkgs:
            print('{0}{1}{2}'.format(self.meta.clrs['red'],
                                     pkg,
                                     self.meta.clrs['reset'],))

        print()

    def append_parts_pkd(self, pkg: str, pkglist: list) -> None:
        """
        append parts of package name into list
        """
        parts = self.get_parts_pkg_name(pkg)
        for ind in range(4):
            pkglist.append(parts[ind])
