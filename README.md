# spman
#### Slackware package manager

Available repositories:
[[alienbob]](http://taper.alienbase.nl/mirrors/people/alien/sbrepos/)
 [[multilib]](http://www.slackware.com/~alien/multilib/)
 [[sbo]](http://slackbuilds.org/slackbuilds/)
 [[slack]](http://ftp.osuosl.org/.2/slackware/)


![help](https://github.com/MyRequiem/spman/raw/master/imgs/help.png)


##### Requirements:
* Slackware Linux
* Python 3.0+
* GNU coreutils
* GNU diffutils
* GNU wget
* pkgtools
* Optional: sbbdep (Slackware binary dependency checker)

##### Build and install spman:
1) Download source code: https://github.com/MyRequiem/spman/archive/1.4.1.tar.gz
2) tar -xvzf 1.4.1.tar.gz
3) cd spman-1.4.1/slackbuild
4) ./spman.SlackBuild
5) upgradepkg --install-new --reinstall /tmp/spman-1.4.1-*-1_myreq.txz

