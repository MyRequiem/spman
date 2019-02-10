#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# download.py file is part of spman
#
# spman - Slackware package manager
# Home page: https://github.com/MyRequiem/spman
#
# Copyright (c) 2018 Vladimir MyRequiem Astrakhan, Russia
# <mrvladislavovich@gmail.com>
# All rights reserved
# See LICENSE for details.


"""
Downloading file or directory
"""

from html.parser import HTMLParser
from os import makedirs, path, remove
from shutil import rmtree
from ssl import _create_unverified_context
from sys import stderr, stdout

import requests

from .maindata import MainData
from .utils import error_open_mess, get_remote_file_size, url_is_alive

try:
    from tqdm import tqdm
except ImportError:
    def tqdm(*args, **kwargs):
        if args:
            return args[0]
        return kwargs.get('iterable', None)


class ListingParser(HTMLParser):
    """
    Parses an HTML page and build a list of links in the directory.
    Links are stored into the 'links' list.
    """
    def __init__(self, url: str):
        HTMLParser.__init__(self)
        self.__url = url
        self.links = []

    def handle_starttag(self, tag: str, attrs: list) -> None:
        """
        HTMLParser.handle_starttag method redefinition
        """
        if tag == 'a':
            for key, value in attrs:
                if key == 'href' and value:
                    value = self.resolve_link(value)
                    if value:
                        self.links.append(value)
                    break

    def resolve_link(self, link: str) -> str:
        """
        discard unnecessary links
        """
        if (not link.startswith('/') and
                '?' not in link and
                'http://' not in link and
                'https://' not in link and
                'ftp://' not in link):
            return '{0}{1}'.format(self.__url, link)


class Download:
    """
    Downloading file or directory
    """
    def __init__(self,
                 url: str,
                 dest: str,
                 remove_dest: bool = False,
                 new_file_name: str = ''):

        self.meta = MainData()
        self.url = url
        self.dest = dest
        self.downdir = False
        self.remove_dest = remove_dest
        self.new_file_name = new_file_name
        self.links = []
        self.dirs = []
        self.context = _create_unverified_context()

    def start(self) -> None:
        """
        start
        """
        print(('{0}URL verification...{1}').format(self.meta.clrs['grey'],
                                                   self.meta.clrs['reset']))
        httpresponse = url_is_alive(self.url)
        if not httpresponse:
            error_open_mess(self.url)
            return

        # if content type of url == 'text/html'
        # then download the entire directory, else download file
        if httpresponse.info().get_content_type() == 'text/html':
            self.downdir = True
            # add a trailing slash to the URL if it does not exist
            if not self.url.endswith('/'):
                self.url = '{0}/'.format(self.url)

        # add a trailing slash to the destination
        # directory if it does not exist
        if not self.dest.endswith('/'):
            self.dest = '{0}/'.format(self.dest)

        if self.downdir:
            print(('{0}Creating a list of '
                   'links...{1}').format(self.meta.clrs['grey'],
                                         self.meta.clrs['reset']))
            self.get_links_in_remote_dir(response=httpresponse)

            if self.remove_dest and path.isdir(self.dest):
                rmtree(self.dest)

            for link in self.links:
                self.download(link)
        else:
            self.download(self.url)

    def get_links_in_remote_dir(self,
                                url: str = '',
                                response: object = False) -> None:
        """
        get links in the remote directory
        """
        if not response:
            response = url_is_alive(url)
            if not response:
                error_open_mess(url)
        else:
            url = self.url

        if response:
            # byte --> str
            content = str(response.read(),
                          encoding=(stdout.encoding or stderr.encoding))
            parser = ListingParser(url)
            parser.feed(content)
            response.close()

            for found_link in parser.links:
                if not found_link.endswith('/'):
                    self.links.append(found_link)
                elif found_link not in self.dirs:
                    self.dirs.append(found_link)

        if self.dirs:
            self.get_links_in_remote_dir(self.dirs.pop())

    def download(self, url: str) -> None:
        """
        download the file
        """
        response = url_is_alive(url)
        if not response:
            error_open_mess(url)
            return

        file_name = (self.new_file_name
                     if self.new_file_name else url.split('/')[-1])
        file_size = get_remote_file_size(httpresponse=response)

        if self.downdir:
            local_dir = ('{0}'
                         '{1}').format(self.dest,
                                       path.dirname(url.replace(self.url, '')))
            if not local_dir.endswith('/'):
                local_dir = '{0}/'.format(local_dir)
        else:
            local_dir = self.dest

        local_file = '{0}{1}'.format(local_dir, file_name)

        if self.remove_dest and path.isfile(local_file):
            remove(local_file)

        if not path.isdir(local_dir):
            makedirs(local_dir)

        first_byte = 0
        if path.exists(local_file):
            first_byte = path.getsize(local_file)

        new_name = (' (renamed to: {0})'.format(self.new_file_name)
                    if self.new_file_name else '')
        print(('{0}Downloading: {1}{2}{7}\nURL: {4}{3}{7}\nto: '
               '{4}{5}{6}{7}').format(self.meta.clrs['lyellow'],
                                      self.meta.clrs['lblue'],
                                      path.basename(url),
                                      url,
                                      self.meta.clrs['grey'],
                                      local_dir,
                                      new_name,
                                      self.meta.clrs['reset']))

        if not file_size and path.isfile(local_file):
            remove(local_file)

        if file_size and first_byte >= file_size:
            print(('{0}{1} {2}is already fully '
                   'downloaded{3}').format(self.meta.clrs['cyan'],
                                           local_file,
                                           self.meta.clrs['green'],
                                           self.meta.clrs['reset']))
            return

        header = {'Range': 'bytes={0}-{1}'.format(first_byte, file_size)}
        try:
            req = requests.get(url, headers=header, stream=True, timeout=10)
        except requests.exceptions.Timeout:
            error_open_mess(url)
            return
        except requests.exceptions.RequestException:
            error_open_mess(url)
            return

        pbar = tqdm(total=file_size,
                    initial=first_byte,
                    unit='B',
                    unit_scale=True,
                    ncols=80,
                    ascii=True,
                    leave=False)

        is_tqdm = type(pbar) is tqdm
        size_chunk = 4096
        with open(local_file, 'ab') as dfile:
            for chunk in req.iter_content(chunk_size=size_chunk):
                if chunk:
                    dfile.write(chunk)
                    if is_tqdm:
                        pbar.update(size_chunk)

        if is_tqdm:
            pbar.close()
        req.close()
        if not dfile.closed:
            dfile.close()
        if not response.closed:
            response.close()

        print('{0}Done{1}'.format(self.meta.clrs['lgreen'],
                                  self.meta.clrs['reset']))
