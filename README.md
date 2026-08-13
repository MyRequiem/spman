---
# spman
>###### Spman is a powerful Slackware package manager implemented in Python 3 and licensed under the MIT license.
>###### This program is available on [SlackBuilds.org][26]
---
##### Main features:
* Check installed packages for available upgrades
* Download binary packages or source code from enabled repositories
* Download, build, and install queued packages from the SBo repository
* Remove or upgrade packages in the current directory
* View the installation, update, and removal history of packages
* Show a list of all dependencies for a package from the SBo repository
* View the contents of files inside a SlackBuild archive from the SBo repository
* Search for packages across all enabled repositories and view their info
* Show a complete list of packages available in a repository
* Scan for dependency issues in system packages using the Slackware binary dependency checker ([sbbdep][32]) tool or ldd
* Search for broken links to nonexistent files or directories in a specified path
* Check the health of installed system packages
* Search for *.new configuration files on the system
* Support command autocompletion

Available repositories: [[Slackware.com]][1] [[SlackBuilds.org]][2] [[Alien Bob's]][3] [[Alien Bob's multilib]][4]

##### Requirements:
* Slackware Linux

##### Optional dependencies:
* bash-completion - Provides autocompletion for CLI input parameters (available in the [standard Slackware repository][1], extra group)
* sbbdep - Slackware binary dependency checker required for dependency issue scanning functionality (available on [SlackBuilds.org][32])
* tqdm - Provides a progress bar for specific operations (available on [SlackBuilds.org][33])

##### Build and install:
1. `~# wget https://github.com/MyRequiem/spman/archive/2.2.3/spman-2.2.3.tar.gz`
2. `~# tar -xvzf spman-2.2.3.tar.gz`
3. `~# cd spman-2.2.3/slackbuild`
4. `~# ./spman.SlackBuild`
5. `~# upgradepkg --install-new --reinstall /tmp/spman-2.2.3-*.t?z`

##### Usage: spman \<param> [param[, param ...]]
##### -h, --help

Print the help message and exit:

![help][5]

##### -v, --check-version

Check the program version for available updates:

![check-version][6]

##### -l, --repolist

Print a list of all repositories configured in /etc/spman/repo-list
Unavailable repositories are highlighted in red:

![repolist][7]

##### -r, --repoinfo

Show detailed information about all active repositories:

![repoinfo][8]

##### -b, --blacklist

Show blacklisted packages from /etc/spman/blacklist

![blacklist][9]

##### -u, --update

Update local metadata for all repositories. The paths to the log files and
package lists are specified in /etc/spman/spman.conf

By default:
* `/var/log/spman/repo_name/ChangeLog.txt`
* `/var/lib/spman/repo_name/PACKAGES.TXT (or SLACKBUILDS.TXT)`

where repo_name is slack, sbo, alienbob, or multilib

**NOTE**: You must run the command `'spman --update'` immediately after
installing spman and configuring /etc/spman/spman.conf

![update][10]

##### -t, --health

Check the health of all installed system packages and display
detailed information:

![health][11]

##### -w, --new-config
Search for *.new configuration files on the system:

![new-config][12]

##### -g, --check-upgrade
Check all installed packages for available upgrades:

![check-upgrade][13]

##### -d, --download --pkg|--src \<reponame> \<pkg>[ \<pkg> ...]
Download binary packages or source code from a specified repository. Binary
packages will be saved to the directory specified in the BUILD_PATH
parameter of /etc/spman/spman.conf (default: /root/spman/build/). Source
code and build scripts will be downloaded to the BUILD_PATH/pkg_name/ directory.

**NOTE**:
Only `'--pkg'` is allowed for the 'multilib' repository; only '--src' is allowed for the 'sbo' repository.

![download][14]

##### -m, --upgrade-pkgs [--only-new]
Install or upgrade packages found in the current directory.

* `--only-new`<br>Packages already installed on the system with the exact same name,
    version, build number, and tag will not be reinstalled.

![upgrade-pkgs][28]

##### -e, --remove-pkgs
Remove packages from the system if corresponding *.t?z files in the current directory are already installed.

![remove-pkgs][27]

##### -q, --queue --add|--remove|--clear|--show|--install
Download, build, and install queued packages from SlackBuilds.org (sbo)

* `--add <pkg>[ <pkg> ...]`<br>Add package(s) to the queue
* `--remove <pkg>[ <pkg> ...]`<br>Remove package(s) from the queue
* `--clear`<br>Clear the queue
* `--show`<br>Print the queue contents
* `--install`<br>Download, build, and install queued packages

![queue][15]

##### -y, --history [--update]
View the package installation, update, and removal history.
* `--update`<br>Update the installed packages database (reset history)

![history][29]

#####  -p, --find-deps \<pkg>
Show a list of all dependencies for a package from the SlackBuilds.org (sbo) repository.
Packages already installed in the system are highlighted in green:

![find-deps][16]

##### -s, --view-slackbuild \<pkg>
View the contents of files included in a SlackBuild archive using a pager:

![view-slackbuild1][17]

![view-slackbuild2][18]

##### -f, --find-pkg [--strict] \<pattern>
Search for a package (case-insensitive) across all enabled repositories and view its information.
* `--strict`<br>Perform a strict exact-match search by package name

![find-pkg1][19]

![find-pkg2][20]

![find-pkg3][21]

##### -i, --pkglist \<reponame> [--only-installed]
Show a complete list of packages available in a repository. Packages already
installed in the system are highlighted in green.
* `--only-installed`<br>Show only installed packages

![pkglist][22]

##### -k, --check-deps --sbbdep|--ldd
Search for dependency issues in the system packages.
* `--sbbdep`<br>Use the '[sbbdep][32]' tool
* `--ldd`<br>Use the 'ldd' tool

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
