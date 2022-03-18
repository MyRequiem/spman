---
# spman
>###### Spman is a powerful Slackware package manager implemented on Python3 and licensed under the MIT license.
>###### This program is available on [SlackBuilds.org][26]
---
##### Main features:
* check packages for upgrade
* download package or source code from allowed repositories
* download, build and install packages in the queue from SBo repository
* remove/upgrade packages in the current directory
* view the history of installing/updating/removing packages
* show list all dependencies for package from SBo repository
* view the contents of files included in SlackBuild archive from SBo repository
* search package from each enabled repository and view info
* show complete list of the packages in the repository
* search for problems with dependencies in the system packages using Slackware binary dependency checker ([sbbdep][32]) tool or ldd
* search for links to nonexistent files/dir in the specified directory
* check health installed packages
* search for *.new config files on the system
* commands autocompletion

Available repositories: [[Slackware.com]][1] [[SlackBuilds.org]][2] [[Alien's]][3] [[Alien's multilib]][4]

##### Requirements:
* Slackware Linux

##### Optional dependencies:
* bash-completion - for autocomplete the input parameters (from [standard Slackware repository][1], group extra)
* sbbdep - Slackware binary dependency checker for search dependency problems functionality (available on [SlackBuilds.org][32])
* tqdm - show progress bar for some parameters (available on [SlackBuilds.org][33])

##### Build and install:
1. `~# wget https://github.com/MyRequiem/spman/archive/2.2.3/spman-2.2.3.tar.gz
2. `~# tar -xvzf spman-2.2.3.tar.gz`
3. `~# cd spman-2.2.3/slackbuild`
4. `~# ./spman.SlackBuild`
5. `~# upgradepkg --install-new --reinstall /tmp/spman-2.2.3-*.t?z`

##### Usage: spman \<param> [param[, param ...]]
##### -h, --help

Print help message and exit:

![help][5]

##### -v, --check-version

Check program version for update:

![check-version][6]

##### -l, --repolist

Print a list of all the repositories allowed in /etc/spman/repo-list
Disconnected repositories are highlighted in red:

![repolist][7]

##### -r, --repoinfo

Show information about all active repositories:

![repoinfo][8]

##### -b, --blacklist

Show blacklisted packages from /etc/spman/blacklist

![blacklist][9]

##### -u, --update

Update local data for all repositories. The paths to the log files and
lists of packages are specified in /etc/spman/spman.conf

By default:
* `/var/log/spman/repo_name/ChangeLog.txt`
* `/var/lib/spman/repo_name/PACKAGES.TXT (or SLACKBUILDS.TXT)`

where repo_name: slack, sbo, alienbob or multilib

**NOTE**: You must run command `'spman --update'` immediately after
installing spman and configuring /etc/spman/spman.conf

![update][10]

##### -t, --health

Check the health of all installed packages on the system and display
detailed information:

![health][11]

##### -w, --new-config
Search for *.new config files on the system:

![new-config][12]

##### -g, --check-upgrade
Check all installed packages for upgrade:

![check-upgrade][13]

##### -d, --download --pkg|--src \<reponame> \<pkg>[ \<pkg> ...]
Download binary package(s) or source code from specified repository. Binary
packages will be downloaded to the directory specified in the BUILD_PATH
parameter from /etc/spman/spman.conf (default: /root/spman/build/). Source
code and build scripts will be downloaded to BUILD_PATH/pkg_name/ directory.

**NOTE**:
only `'--pkg'` for reposytory 'multilib', only '--src' for reposytory 'sbo'

![download][14]

##### -m, --upgrade-pkgs [--only-new]
Install/Upgrade packages in the current directory.

* `--only-new`<br>packages already installed on the system with the same name,
    version, build number and tag will not be reinstalled.

![upgrade-pkgs][28]

##### -e, --remove-pkgs
If there are *.t?z packages in the current directory and they are installed,
then these packages will be removed from the system.

![remove-pkgs][27]

##### -q, --queue --add|--remove|--clear|--show|--install
Download, build and install packages in the queue from SlackBuilds.org (sbo)

* `--add <pkg>[ <pkg> ...]`<br>add package(s) to the queue
* `--remove <pkg>[ <pkg> ...]`<br>remove package(s) from the queue
* `--clear`<br>clear queue
* `--show`<br>print queue
* `--install`<br>download, build and install package(s)

![queue][15]

##### -y, --history [--update]
View the history of installing/updating/removing packages.
* `--update`<br>update the installed packages database (reset history)

![history][29]

#####  -p, --find-deps \<pkg>
Show list all dependencies for package from SlackBuilds.org (sbo) repository.
The packages already installed in the system are highlighted in green:

![find-deps][16]

##### -s, --view-slackbuild \<pkg>
View the contents of files included in SlackBuild archive using pager:

![view-slackbuild1][17]

![view-slackbuild2][18]

##### -f, --find-pkg [--strict] \<pattern>
Search for package (case-insensitive) from each enabled repository and view info.
* `--strict`<br>strict match by package name

![find-pkg1][19]

![find-pkg2][20]

![find-pkg3][21]

##### -i, --pkglist \<reponame> [--only-installed]
Show complete list of the packages on repository. The packages already
installed in the system are highlighted in green.
* `--only-installed`<br>show only installed packages

![pkglist][22]

##### -k, --check-deps --sbbdep|--ldd
Search for problems with dependencies in the system packages.
* `--sbbdep`<br>using '[sbbdep][32]' tool
* `--ldd`<br>using 'ldd' tool

![check-deps-sbbdep][23]
![check-deps-ldd][24]

##### -a, --bad-links \<path_to_dir>
Search for links to nonexistent files/dirs in the specified directory.

![bad-links][25]

[1]: http://ftp.osuosl.org/.2/slackware/
[2]: http://slackbuilds.org/slackbuilds/
[3]: http://bear.alienbase.nl/mirrors/people/alien/sbrepos/
[4]: http://www.slackware.com/~alien/multilib/
[5]: https://github.com/MyRequiem/spman/raw/master/imgs/help.png
[6]: https://github.com/MyRequiem/spman/raw/master/imgs/check-version.png
[7]: https://github.com/MyRequiem/spman/raw/master/imgs/repolist.png
[8]: https://github.com/MyRequiem/spman/raw/master/imgs/repoinfo.png
[9]: https://github.com/MyRequiem/spman/raw/master/imgs/blacklist.png
[10]: https://github.com/MyRequiem/spman/raw/master/imgs/update.png
[11]: https://github.com/MyRequiem/spman/raw/master/imgs/health.png
[12]: https://github.com/MyRequiem/spman/raw/master/imgs/new-config.png
[13]: https://github.com/MyRequiem/spman/raw/master/imgs/check-upgrade.png
[14]: https://github.com/MyRequiem/spman/raw/master/imgs/download.png
[15]: https://github.com/MyRequiem/spman/raw/master/imgs/queue.png
[16]: https://github.com/MyRequiem/spman/raw/master/imgs/find-deps.png
[17]: https://github.com/MyRequiem/spman/raw/master/imgs/view-slackbuild1.png
[18]: https://github.com/MyRequiem/spman/raw/master/imgs/view-slackbuild2.png
[19]: https://github.com/MyRequiem/spman/raw/master/imgs/find-pkg1.png
[20]: https://github.com/MyRequiem/spman/raw/master/imgs/find-pkg2.png
[21]: https://github.com/MyRequiem/spman/raw/master/imgs/find-pkg3.png
[22]: https://github.com/MyRequiem/spman/raw/master/imgs/pkglist.png
[23]: https://github.com/MyRequiem/spman/raw/master/imgs/check-deps-sbbdep.png
[24]: https://github.com/MyRequiem/spman/raw/master/imgs/check-deps-ldd.png
[25]: https://github.com/MyRequiem/spman/raw/master/imgs/bad-links.png
[26]: https://slackbuilds.org/repository/15.0/system/spman/
[27]: https://github.com/MyRequiem/spman/raw/master/imgs/remove-pkgs.png
[28]: https://github.com/MyRequiem/spman/raw/master/imgs/upgrade-pkgs.png
[29]: https://github.com/MyRequiem/spman/raw/master/imgs/history.png
[32]: https://slackbuilds.org/repository/15.0/system/sbbdep/
[33]: http://slackbuilds.org/repository/15.0/python/tqdm/
