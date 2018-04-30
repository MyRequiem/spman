---
# spman
>###### Spman is a powerful Slackware package manager implemented on Python3 and licensed under the MIT license.
>###### This program is available on [SlackBuilds.org][26]
---
##### Main features:
* check packages for upgrade
* download package or source code from allowed repositories
* download, build and install package(s) in the queue from SBo repository
* show list all dependencies for package from SBo repository
* view the contents of files included in SlackBuild archive
* search package from each enabled repository and view info
* show complete list of the packages in the repository
* search dependency problems in the system packages using Slackware binary dependency checker (sbbdep) tool or ldd
* search for links to nonexistent files/dir in the specified directory
* check health installed packages
* search for *.new config files on the system
* autocompletion of input parameters

Available repositories: [[Slackware.com]][1] [[SlackBuilds.org]][2] [[Alien's]][3] [[Alien's multilib]][4]

##### Requirements:
* Slackware Linux
* GNU coreutils
* GNU diffutils
* GNU wget
* pkgtools
* Python 3.0+ (available on SlackBuilds.org)

##### Optional dependencies:
* bash-completion - for autocomplete the input parameters (from standard Slackware repository, group extra)
* sbbdep - Slackware binary dependency checker for search dependency problems functionality (available on SlackBuilds.org)

##### Build and install:
1. `~# wget https://github.com/MyRequiem/spman/archive/1.5.0/spman-1.5.0.tar.gz
2. `~# tar -xvzf spman-1.5.0.tar.gz`
3. `~# cd spman-1.5.0/slackbuild`
4. `~# ./spman.SlackBuild`
5. `~# upgradepkg --install-new --reinstall /tmp/spman-1.5.0-*.t?z`

##### Usage:
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

Show blacklisted packages in /etc/spman/blacklist

![blacklist][9]

##### -u, --update

Update local data for all repositories specified in /etc/spman/spman.conf

By default:
* `/var/lib/spman/repository_name`  - PACKAGES.TXT or SLACKBUILDS.TXT
* `/var/log/spman/repository_name`  - ChangeLog.txt

**NOTE**: You must run this command immediately after installing spman and
configuring /etc/spman/spman.conf

![update][10]

##### -t, --health

Check health installed packages. Displayed detailed information about
installed packages:

![health][11]

##### -w, --new-config
Search for *.new config files on the system:

![new-config][12]

##### -g, --check-upgrade
Check all installed packages for upgrade:

![check-upgrade][13]

##### -d, --download --pkg|--src reponame pkg1[ pkg2...]
Download binary package(s) or source code from specified repository.

**NOTE**:
for reposytory 'multilib' only `--pkg`, for reposytory 'sbo' only `--src`

**Examples:**

* ###### download flashplayer-plugin package from alienbob repository:
    `~# spman --download --pkg alienbob flashplayer-plugin`

* ###### download 'emacs' and 'kdelibs' source code with SlackBuild scripts from standard Slackware repository:
    `~# spman --download --src slack emacs kdelibs`

![download][14]

##### -q, --queue --add pkglist|--remove pkglist|--clear|--show|--install
Download, build and install package(s) in the queue from SlackBuilds.org

**NOTE**: pkglist - list of names of packages

* `--add pkglist` - add package(s) to the queue
* `--remove pkglist` - remove package(s) from the queue
* `--clear` - clear queue
* `--show` - print queue
* `--install` - download, build and install package(s)

![queue][15]

#####  -p, --find-deps pkgname
Show list all dependencies for package from 'sbo' repository. Installed packages are highlighted in green:

![find-deps][16]

##### -s, --view-slackbuild pkgname
View the contents of files included in SlackBuild archive using pager:

![view-slackbuild1][17]

![view-slackbuild2][18]

##### -f, --find-pkg [--strict] pkgname
Search package from each enabled repository and view info (case-insensitive)
* `--strict` - strict match by package name

![find-pkg1][19]

![find-pkg2][20]

![find-pkg3][21]

##### -i, --pkglist reponame [--only-installed]
Show complete list of the packages on repository. Installed packages are
highlighted in green.
* `--only-installed` - output only installed packages

![pkglist][22]

##### -k, --check-deps --sbbdep|--ldd
Search dependency problems in the system packages
* `--sbbdep` - using 'sbbdep' tool
* `--ldd` - using 'ldd' tool

![check-deps-sbbdep][23]
![check-deps-ldd][24]

##### -a, --bad-links /path/to/dir
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
[26]: https://slackbuilds.org/repository/14.2/system/spman/
