# download.py file is part of spman
#
# spman - Slackware package manager
# Home page: https://github.com/MyRequiem/spman
#
# Copyright (c) 2018 Vladimir MyRequiem Astrakhan, Russia
# <mrvladislavovich@gmail.com>
# All rights reserved
# See LICENSE for details.

"""Downloading files or directories from remote repositories."""

from __future__ import annotations # noqa: I001

import shutil

from html.parser import HTMLParser
from pathlib import Path

import requests

from .maindata import MainData
from .utils import error_open_mess, get_remote_file_size, url_is_alive


# Safe polyfill for tqdm if the package is missing in the Slackware system.
try:
    from tqdm import tqdm
except ImportError:
    from collections.abc import Iterable
    from typing import TypeVar

    T = TypeVar("T")

    def tqdm(
            iterable: Iterable[T] | None = None,
            *args: object,    # noqa: ARG001
            **kwargs: object, # noqa: ARG001
        ) -> Iterable[T]:
        """Return the iterable directly if tqdm is not installed."""
        return iterable

class ListingParser(HTMLParser):
    """Parse an HTML directory listing page to extract all hyperlinks.

    Extracted URLs are stored in the 'links' list attribute.
    """

    def __init__(self, url: str) -> None:
        """Initialize the HTML parser with a target repository URL."""
        super().__init__()
        self._url: str = url
        self.links: list[str] = []

    def handle_starttag(
            self,
            tag: str,
            attrs: list[tuple[str, str | None]],
        ) -> None:
        """Process HTML start tags.

        Process HTML start tags to extract and resolve 'href' link values.
        """
        if tag == "a":
            for key, value in attrs:
                if key == "href" and value:
                    if resolved := self.resolve_link(value):
                        self.links.append(resolved)
                    break

    def resolve_link(self, link: str) -> str | None:
        """Discard unnecessary links.

        Return absolute URLs for repository contents.
        """
        # Clean query strings, absolute external URLs, or absolute root paths.
        if link == "" or "?" in link or link.startswith(
                ("..", "/", "http://", "https://", "ftp://"),
            ) or link.endswith(".mirrorlist"):
            return None

        return f"{self._url}{link}"

class Download:
    """Handle downloading of files.

    Handle downloading of files or entire directories from remote locations.
    """

    def __init__(
        self,
        url: str,
        dest: str,
        *, # All arguments below must be passed as keyword-only arguments.
        remove_dest: bool = False,
        new_file_name: str = "",
    ) -> None:
        """Initialize the downloader.

        Initialize the downloader with target URLs, destinations, and paths.
        """
        self.meta: MainData = MainData()
        self.url: str = url
        self.dest: str = dest
        self.downdir: bool = False
        self.remove_dest: bool = remove_dest
        self.new_file_name: str = new_file_name
        self.links: list[str] = []
        self.dirs: list[str] = []

    def start(self) -> None:
        """Verify the target URL and dispatch file or directory downloading."""
        print(
            f"{self.meta.clrs['grey']}URL verification..."
            f"{self.meta.clrs['reset']}" # noqa: COM812
        )

        # url_is_alive should return a requests.Response object or None/False.
        response = url_is_alive(self.url)
        if not response:
            error_open_mess(self.url)
            raise SystemExit(1)

        # Check if the URL points to an HTML directory listing or a raw file.
        content_type = response.headers.get("Content-Type", "")
        if "text/html" in content_type:
            self.downdir = True
            if not self.url.endswith("/"):
                self.url = f"{self.url}/"

        if not self.dest.endswith("/"):
            self.dest = f"{self.dest}/"

        if self.downdir:
            print(
                f"{self.meta.clrs['grey']}Creating a list of "
                f"links...{self.meta.clrs['reset']}" # noqa: COM812
            )
            # Pass the modern requests response object.
            self.get_links_in_remote_dir(response=response)

            if self.remove_dest and Path(self.dest).is_dir():
                shutil.rmtree(self.dest)

            for link in self.links:
                self.download(link)
        else:
            self.download(self.url)

    def get_links_in_remote_dir(
        self,
        url: str = "",
        response: requests.Response | None = None,
    ) -> None:
        """Recursively extract.

        Recursively extract all file and directory links from a remote path.
        """
        # If no active response is provided, try to establish a connection.
        if response is None:
            response = url_is_alive(url)
            if not response:
                error_open_mess(url)
                raise SystemExit(1)
        else:
            url = self.url

        # Now we can safely read the clean HTML text using requests.
        content = response.text

        parser = ListingParser(url)
        parser.feed(content)

        # Separate links into files and subdirectories.
        for found_link in parser.links:
            if not found_link.endswith("/"):
                self.links.append(found_link)
            elif found_link not in self.dirs:
                self.dirs.append(found_link)

        # Recursively process remaining directories in the stack.
        if self.dirs:
            self.get_links_in_remote_dir(url=self.dirs.pop())

    def download(self, url: str) -> None: # noqa: C901,PLR0912,PLR0915
        """Download a specific file.

        Download a specific file supporting chunked streaming and resume.
        """
        response = url_is_alive(url)
        if not response:
            error_open_mess(url)
            raise SystemExit(1)

        file_name = self.new_file_name or url.rsplit("/", 1)[-1]
        file_size = get_remote_file_size(response=response)

        if self.downdir:
            clean_path = Path(url.replace(self.url, "")).parent
            clean_path = "" if str(clean_path) == "." else clean_path
            local_dir = f"{self.dest}{clean_path}"
            if not local_dir.endswith("/"):
                local_dir = f"{local_dir}/"
        else:
            local_dir = self.dest

        local_file = f"{local_dir}{file_name}"

        path_file = Path(local_file)
        path_dir = Path(local_dir)

        if self.remove_dest and path_file.is_file():
            path_file.unlink()

        path_dir.mkdir(parents=True, exist_ok=True)

        first_byte = path_file.stat().st_size if path_file.exists() else 0

        new_name = (
            f" (renamed to: {self.new_file_name})"
            if self.new_file_name
            else ""
        )

        print(
            f"{self.meta.clrs['lyellow']}Downloading: "
            f"{self.meta.clrs['lblue']}{Path(url).name}{new_name}"
            f"{self.meta.clrs['reset']}\n"
            f"URL: {self.meta.clrs['grey']}{url}{self.meta.clrs['reset']}\n"
            f"to: {self.meta.clrs['grey']}{local_dir}"
            f"{self.meta.clrs['reset']}" # noqa: COM812
        )

        if not file_size and path_file.is_file():
            path_file.unlink()

        if file_size and first_byte >= file_size:
            print(
                f"{self.meta.clrs['cyan']}{local_file} "
                f"{self.meta.clrs['green']}is already fully downloaded"
                f"{self.meta.clrs['reset']}" # noqa: COM812
            )
            return

        try:
            import time
            time.sleep(0.5)

            user_agent_type = self.meta.get_spman_conf()["USER_AGENT_TYPE"]

            if user_agent_type == "curl":
                agent = "curl/8.17.0"
                accept = "*/*"
            elif user_agent_type == "wget":
                agent = "Wget/1.25.0 (linux-gnu)"
                accept = "*/*"
            else:  # browser
                agent = (
                    "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) "
                    "Gecko/20100101 Firefox/153.0"
                )
                accept = (
                    "text/html,application/xhtml+xml,"
                    "application/xml;q=0.9,*/*;q=0.8"
                )

            headers = {
                "User-Agent": agent,
                "Accept": accept,
            }
            if user_agent_type == "browser":
                headers["Accept-Language"] = "en-US,en;q=0.5"

            req = requests.get(
                url,
                headers=headers,
                stream=True,
                timeout=(5, 30),
            )
            req.raise_for_status()
        except requests.RequestException:
            error_open_mess(url)
            raise SystemExit(1) from None

        pbar = tqdm(
            total=file_size,
            initial=first_byte,
            unit="B",
            unit_scale=True,
            ncols=80,
            ascii=True,
            leave=False,
        )

        # Check if pbar is a real tqdm instance object or our placeholder
        # function.
        has_pbar = hasattr(pbar, "update")
        size_chunk = 4096

        try:
            with path_file.open("ab") as dfile:
                for chunk in req.iter_content(chunk_size=size_chunk):
                    if chunk:
                        dfile.write(chunk)
                        if has_pbar:
                            pbar.update(len(chunk))

            if has_pbar:
                pbar.close()

            print(f"{self.meta.clrs['lgreen']}Done{self.meta.clrs['reset']}")
        except requests.RequestException:
            if has_pbar:
                pbar.close()

            error_open_mess(self.url)
            raise SystemExit(1) from None
