# Installation 
## Overview
There are Gluu Server Linux packages for Ubuntu, CentOS, RHEL and Debian operating systems. The 
installation procedure is similar across all the distributions: 

1. [Install the Linux package](#1-install-gluu-server-package)
2. [Start the Gluu Server and login to the container](#2-start-the-gluu-server-and-login)
3. [Run `setup.py`](#3-run-setuppy)
4. [Login via a browser](#4-login-via-browser)
5. [Disable Gluu repositories](#5-disable-gluu-repositories)

!!! Note
    The below instructions are intended for single server Gluu deployments. If you intend to cluster your Gluu Server to achieve fail-over and high availability, please refer to the [cluster documentation](./cluster.md)

## Prerequisites

- The Gluu Server needs to be installed on a VM or physical server with at least 4GB of RAM and 2CPU units.  
- Gluu must be deployed on a fully qualified domain name (FQDN). Localhost is not supported. 
- Make sure your server or VM meets the [minimum requirements](../installation-guide/index.md) to deploy the Gluu Server.

!!! Warning
    Docker containers are **not** supported.     

## Instructions

### 1. Install Gluu Server package

Installation of the Gluu server will be done under `/root`. 
The Gluu Server will create its file system under `/root/` and will be 
installed under `/opt`. File size and [minimum requirements](../installation-guide/index.md) 
remain the same as the host.

#### Ubuntu Server 14.04.x

| Command Description     |               Trusty Commands         |
|-------------------------|---------------------------------------|
| Add Gluu Repository     | `# echo "deb https://repo.gluu.org/ubuntu/ trusty main" > /etc/apt/sources.list.d/gluu-repo.list` |
| Add Gluu GPG Key        | `# curl https://repo.gluu.org/ubuntu/gluu-apt.key | apt-key add -` |
| Update/Clean Repo       | `# apt-get update`                         |
| Install Gluu Server     | `# apt-get install gluu-server-3.1.2`      |
    
#### Ubuntu Server 16.04.x

|  Command Description    |               Xenial Commands         |
|-------------------------|---------------------------------------|
| Add Gluu Repository     | `# echo "deb https://repo.gluu.org/ubuntu/ xenial main" > /etc/apt/sources.list.d/gluu-repo.list` |
| Add Gluu GPG Key        | `# curl https://repo.gluu.org/ubuntu/gluu-apt.key | apt-key add -` |
| Update/Clean Repo       | `# apt-get update`                         |
| Install Gluu Server     | `# apt-get install gluu-server-3.1.2`      |

#### CentOS 6.x

| Command Description     |               CentOS 6.x              |
|-------------------------|---------------------------------------|
| Add Gluu Repository     | `# wget https://repo.gluu.org/centos/Gluu-centos6.repo -O /etc/yum.repos.d/Gluu.repo`|
| Add Gluu GPG Key        | `# wget https://repo.gluu.org/centos/RPM-GPG-KEY-GLUU -O /etc/pki/rpm-gpg/RPM-GPG-KEY-GLUU`|
| Import GPG Key          | `# rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-GLUU`|
| Update/Clean Repo       | `# yum clean all`                          |
| Install Gluu Server     | `# yum install gluu-server-3.1.2`          |

#### CentOS 7.x

| Command Description     |               CentOS 7.2              |
|-------------------------|---------------------------------------|
| Add Gluu Repository     | `# wget https://repo.gluu.org/centos/Gluu-centos7.repo -O /etc/yum.repos.d/Gluu.repo` |
| Add Gluu GPG Key        | `# wget https://repo.gluu.org/centos/RPM-GPG-KEY-GLUU -O /etc/pki/rpm-gpg/RPM-GPG-KEY-GLUU`|
| Import GPG Key          | `# rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-GLUU` |
| Update/Clean Repo       | `# yum clean all`                          |
| Install Gluu Server     | `# yum install gluu-server-3.1.2`          |

#### RHEL 6.x

| Command Description     |               RHEL 6.x              |
|-------------------------------|---------------------------------------|
| Add Gluu Repository     | `# wget https://repo.gluu.org/rhel/Gluu-rhel6.repo -O /etc/yum.repos.d/Gluu.repo` |
| Add Gluu GPG Key        | `# wget https://repo.gluu.org/centos/RPM-GPG-KEY-GLUU -O /etc/pki/rpm-gpg/RPM-GPG-KEY-GLUU`|
| Import GPG Key          | `# rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-GLUU` |
| Update/Clean Repo       | `# yum clean all`                          |
| Install Gluu Server     | `# yum install gluu-server-3.1.2`          |

#### RHEL 7.x

| Command Description     |               RHEL 7                  |
|-------------------------|---------------------------------------|
| Add Gluu Repository     | `# wget https://repo.gluu.org/rhel/Gluu-rhel7.repo -O /etc/yum.repos.d/Gluu.repo` |
| Add Gluu GPG Key        | `# wget https://repo.gluu.org/rhel/RPM-GPG-KEY-GLUU -O /etc/pki/rpm-gpg/RPM-GPG-KEY-GLUU`|
| Import GPG Key          | `# rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-GLUU` |
| Update/Clean Repo       | `# yum clean all`                          |
| Install Gluu Server     | `# yum install gluu-server-3.1.2`          |

#### Debian 8 (Jessie)

| Command Description     |               Jessie Commands         |
|-------------------------|---------------------------------------|
| Add Gluu Repository     | `# echo "deb https://repo.gluu.org/debian/ stable main" > /etc/apt/sources.list.d/gluu-repo.list`|
| Add Gluu GPG Key        | `# curl https://repo.gluu.org/debian/gluu-apt.key | apt-key add -` |
| Update/Clean Repo       | `# apt-get update`                         |
| Install Gluu Server     | `# apt-get install gluu-server-3.1.2`      |


### 2. Start the Gluu Server and login

The Gluu Server is a chroot container, which you must start to proceed. 

For Centos 6.x, Red Hat 6.x, Ubuntu 14/16, and Debian 8, run the following commands:

```
# service gluu-server-3.1.2 start
# service gluu-server-3.1.2 login
```

For Centos 7.x and Red Hat 7.x, run the following commands: 

```
# /sbin/gluu-serverd-3.1.2 enable
# /sbin/gluu-serverd-3.1.2 start
# /sbin/gluu-serverd-3.1.2 login
```

!!! Note
    Only use `enable` the first time you start the Gluu Server.

### 3. Run `setup.py`

Configuration is completed by running the `setup.py` script. This generates certificates, salt values, and renders configuration files. 

```
# cd /install/community-edition-setup
# ./setup.py
```

!!! Note
    You must be logged into the Gluu Server chroot container to run `setup.py`.

!!! Warning
    Only run setup.py **one time**. Running the above command twice will break the instance.

You will be prompted to answer some questions about your deployment. Hit `Enter` to accept the default values.

Refer to the following table for details about the available setup options:

| Setup Option                |  Explanation                               |
|-------------------------|--------------------------------------------|
| Enter IP Address | Used primarily by Apache HTTPD for the [Listen](https://httpd.apache.org/docs/2.4/bind.html) directive. **Use an IP address assigned to one of this server's network interfaces (usage of addresses assigned to loopback interfaces is not supported)**|
| Enter hostname | Internet-facing hostname, FQDN, or CNAME whichever your organization follows to be used to generate certificates and metadata. **Do not use an IP address or localhost.** |
| Enter your city or locality | Used to generate X.509 certificates. |
| Enter your state or province two letter code | Used to generate X.509 certificates. |
| Enter two letter Country Code | Used to generate X.509 certificates. |
| Enter Organization Name | Used to generate X.509 certificates. |
| Enter email address for support at your organization | Used to generate X.509 certificates. | 
| Optional: enter password for oxTrust and LDAP superuser | Used as the LDAP directory manager password, and for the default admin user for oxTrust. |
| Install oxAuth OAuth2 Authorization Server | Required. Includes Gluu's OpenID Connect provider (OP) and UMA authorization server (AS) implementations.|
| Install oxTrust Admin UI | Required. This is the Gluu server admin dashboard. |
| Install LDAP Server | Required. LDAP is used to store user info and configuration data. |
| Install Passport |  Install if you want to support external IDP, for instance to offer users social login. |
| Install Apache HTTPD Server | Required |
| Install Shibboleth SAML IDP | Optional: only install if you need to a SAML identity provider. |
| Install oxAuth RP | OpenID Connect test client: recommended for test enviornments, for more details see [here](../admin-guide/openid-connect/#oxauth-rp) |
| Install Asimba SAML Proxy | **Not recommended**: previously used to achieve inbound SAML. We now recommend using passport.js (above) |


!!! Warning
	Changing the hostname after installation is not supported. 

After answering these questions, `setup.py` will show you your selections and ask you if you want to continue. If everything looks good, select Y to finish installation. 

After 5-10 minutes you should see the following success message: 

`Gluu Server installation successful! Point your browser to [hostname].`

!!! Note
    The easiest place to go wrong is with the first two questions:                 
        1. Enter IP Address: Do **not** use `localhost` for either the IP address or hostname.     
	2. Enter hostname: Use a real hostname--you can always manage via host file entries even if you don't want to mess with DNS for testing. If you are deploying a cluster, use the hostname of the cluster--that is used by the clients connecting to the Gluu Server.    

### 4. Login via browser
Wait about 10 minutes in total for the server to restart and finalize its configuration. After that period you can log into your Gluu Server via a web browser. 

Your username will be `admin` and your password will be the `ldap_password` you provided during installation. 

!!! Note
    If the Gluu Server login page is still not appearing after you've received the success message and waited about 10 minutes, check if port 443 is open in the VM. If it is not open, open port 443 and try to reach the host in your browser again. 

### 5. Disable Gluu repositories
To prevent involuntary overwrites of the currently deployed instance (in case a newer version of the same package is found during regular OS updates), disable the previously added Gluu repositories after initial installation.

For CentOS/RHEL: 

`/etc/yum.repos.d/Gluu.repo` needs to be edited so that the `enabled=1` clause is changed to `enabled=0`        

For Ubuntu/Debian: 

`/etc/apt/sources.list.d/gluu-repo.list` needs to be edited to comment out all Gluu-related repos.     

!!! Note
    The Gluu Server does **not** support package updates/upgrades via Linux package management (i.e. using commands like `# yum update` or `# apt-get update`). For upgrade instructions, see the [upgrade docs](../upgrade/index.md).


## Backups
Sometimes things go wrong! And it can be difficult to troubleshoot issues if the steps to reproduce the issue are not clearly documented. This is why we **always** recommend creating [backups of your Gluu Server](../operation/backup.md). 

## Uninstallation
For Ubuntu 14/16, and Debian 8:

```
# service gluu-server-3.1.2 stop
# apt-get remove gluu-server-3.1.2
# rm -rf /opt/gluu-server-3.1.2.save
```

For Centos 6.x, Red Hat 6.x: 

```
# service gluu-server-3.1.2 stop
# yum remove gluu-server-3.1.2
# rm -rf /opt/gluu-server-3.1.2.save
```

For Centos 7.x and Red Hat 7.x:

```
# /sbin/gluu-serverd-3.1.2 disable
# /sbin/gluu-serverd-3.1.2 stop
# yum remove gluu-server-3.1.2 
# rm -rf /opt/gluu-server-3.1.2.save
```

!!! Note
    You can also use `apt-get purge gluu-server-3.1.2` or `apt-get remove --purge gluu-server-3.1.2` to uninstall and remove all the folders and services of Gluu server.

## Support
If you run into issues please review the [Gluu support portal](https://support.gluu.org). If you can not find a similar existing public issue, register for an account and open a new ticket. 

If your organization needs guaranteed responses, SLAs, and priority access to the Gluu support and development team, consider purchasing one of our [VIP support contracts](https://gluu.org/pricing).  
