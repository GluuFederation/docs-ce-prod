# Debian Installation 
## Overview
Single-node Gluu Server Linux packages are available for Ubuntu, CentOS, RHEL and Debian operating systems. The installation procedure is similar across all distributions: 

1. [Install the Linux package](#install-the-package)
2. [Start the Server and log in to the container](#start-the-server-and-log-in)
3. [Run `setup.py`](#run-setuppy)
4. [Sign in via browser](#sign-in-via-browser)
5. [Disable Gluu repositories](#disable-gluu-repositories)

## Prerequisites

- Make sure the target server or VM meets **all minimum requirements** specified in the [VM Preparation Guide](../installation-guide/index.md).   

- Make sure the `apt-transport-https` Debian package is already installed on the target system before the `gluu-repo.list` is added. Otherwise the installation might be hindered.

## Instructions

### Install the package

Installation of the Gluu server will be done under `/root`. 
The Gluu Server will create its file system under `/root/` and will be installed under `/opt`. File size and [minimum requirements](../installation-guide/index.md) remain the same as the host.

Gluu Server CE 4.0 supports **Debian 9 (Stretch)**. Enter these commands to install:

```
echo "deb https://repo.gluu.org/debian/ stretch-testing main" > /etc/apt/sources.list.d/gluu-repo.list
```

```
# curl https://repo.gluu.org/debian/gluu-apt.key | apt-key add -
```

```
apt-get update
```

```
apt-get install gluu-server-4.0
```

### Start the server and log in

The Gluu Server is a chroot container, which must be started to proceed. 

Run the following commands: 

```
/sbin/gluu-serverd-4.0 enable
```

```
/sbin/gluu-serverd-4.0 start
```

```
/sbin/gluu-serverd-4.0 login
```

!!! Note
    Only use `enable` the first time you start the Gluu Server.

### Run `setup.py`

Configuration is completed by running `setup.py` from inside the chroot container. This generates certificates, salt values, and renders configuration files.

```
cd /install/community-edition-setup
```

```
./setup.py
```   

See the [Setup Script Documentation](./setup_py.md#setup-prompt) for more detail on setup script options.

### Sign in via browser

Wait about 10 minutes in total for the server to restart and finalize its configuration. After that period, sign in via a web browser. The username will be `admin` and your password will be the `ldap_password` you provided during installation. 

!!! Note   
    If the Gluu Server login page does not appear, confirm that port 443 is open in the VM. If it is not open, open port 443 and try to reach the host in the browser again.   

### Disable Gluu Repositories

To prevent involuntary overwrites of the currently deployed instance (in case a newer version of the same package is found during regular OS updates), disable the previously added Gluu repositories after initial installation.

Edit `/etc/apt/sources.list.d/gluu-repo.list` to comment out all Gluu-related repos.     

!!! Note
    The Gluu Server does **not** support package updates/upgrades via Linux package management (i.e. using commands like `# yum update` or `# apt-get update`). For upgrade instructions, see the [upgrade docs](../upgrade/index.md).

## Backups
Sometimes things go wrong! It can be difficult to troubleshoot issues if the steps to reproduce the issue are not clearly documented. This is why we **always** recommend creating [backups of your Gluu Server](../operation/backup.md). 

## Uninstallation

Run the following commands:

```
service gluu-server-4.0 stop
```

```
apt-get remove gluu-server-4.0
```

```
rm -rf /opt/gluu-server-4.0.save
```

!!! Note
    `apt-get purge gluu-server-4.0` or `apt-get remove --purge gluu-server-4.0` can also be used to uninstall and remove all the folders and services of the Gluu Server. Make sure to back up ALL directories of `/opt` into other direction (tmp or root directory itself) before running the purge command.

## Support
Please review the [Gluu support portal](https://support.gluu.org). There are many existing tickets about troubleshooting installation issues. If there is no similar existing public issue, register for an account and open a new ticket. 

If your organization needs guaranteed responses, SLAs, and priority access to the Gluu support and development team, consider purchasing one of our [VIP support contracts](https://gluu.org/pricing).  
