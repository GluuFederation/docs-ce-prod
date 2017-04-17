# How to install csync2 in different Gluu CE containers


## CentOS 6.x

1. Log into Gluu-Server container

2. Install epel-release-latest by running `rpm -ivh https://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm`

3. Install `csync2` package by running `yum install csync2`


## CentOS 7.x

On the moment of writing csync2 can't be found in public repositories. The only option is to compile from sources.

1. Log into Gluu-Server container

2. Enable epel-release repo: `# yum install epel-release`

3. Install compiler and development environment: `# yum groupinstall "Development Tools"`

4. Install csync2's dependencies:

    1. `# yum install librsync-devel`

    2. `# yum install gnutls-devel`

    3. `# yum install sqlite-devel`

5. `# mkdir building_csync && cd building_csync/`

6. Download the latest version of the tool from [here](http://oss.linbit.com/csync2/): `# wget http://oss.linbit.com/csync2/csync2-2.0.tar.gz`

7. Unpack: `# tar -xz -f ./csync2-2.0.tar.gz && cd csync2-2.0/`

8. Build & install, while directing it to use `/usr/local/etc/csync2/` directory for storing configuration (for convenience): `# ./configure --sysconfdir /usr/local/etc/csync2/ && make && make install`. Don't forget to update paths to csync's binaries and configuration files later on, as they are different from the ones used in examples in the main article!

## Ubuntu 14.x (compiling from sources)

1. Log into Gluu-Server container

2. Run `apt-get update`

3. Install csync2's dependencies:

    1. `# apt-get install pkg-config`
    
    2. `# apt-get install libsqlite-dev`
    
    3. `# apt-get install libsqlite3-dev`

    4. `# apt-get install librsync-dev`

4. Download the latest version of the tool from [here](http://oss.linbit.com/csync2/): `# wget http://oss.linbit.com/csync2/csync2-2.0.tar.gz`

5. Unpack: `# tar -xz -f ./csync2-2.0.tar.gz && cd csync2-2.0/`

6. Build & install, while directing it to use `/etc/csync2/` directory for storing configuration and `/usr/sbin` directory for executables (for convenience): `./configure --sysconfdir /etc/csync2/ --prefix /usr/ && make && make install`

## Ubuntu 14.x (from repo)

1. Log into Gluu-Server container

2. Run `apt-get update`

3. Run `apt-get install csync2`
