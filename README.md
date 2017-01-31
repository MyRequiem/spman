# spman
####Slackware package manager

######Available repositories:
[alienbob](http://taper.alienbase.nl/mirrors/people/alien/sbrepos/)<br>
[multilib](http://www.slackware.com/~alien/multilib/)<br>
[sbo](http://slackbuilds.org/slackbuilds/)<br>
[slack](http://ftp.osuosl.org/.2/slackware/)
<br><br>
![help](https://github.com/MyRequiem/spman/raw/master/imgs/help.png)

######Requirements:
* Slackware Linux
* Python 3.0+
* GNU coreutils
* GNU diffutils
* GNU wget
* pkgtools
* Optional: sbbdep (Slackware binary dependency checker)
<br><br>

######Build and install spman:
1) Download source code:<br>
   wget https://github.com/MyRequiem/spman/archive/1.2.2.tar.gz<br>
2) tar -xvzf 1.2.2.tar.gz<br>
3) cd spman-1.2.2/slackbuild<br>
4) ./spman.SlackBuild<br>
    The package will be created in the /tmp directory<br>
5) upgradepkg --install-new --reinstall /tmp/spman-1.2.2-noarch-1_myreq.txz
<br>
