# Installation 
## Overview
Gluu publishes packages for Ubuntu, CentOS, RHEL and Debian. The 
installation procedure is similar across all the distributions: 

1. [Install the Linux package](#install-gluu-server-package)
2. [Start the Gluu Server and login to the container](#start-the-gluu-server-and-login)
3. [Run `setup.py`](#run-setuppy)

!!! Note
    Make sure your VM or server meets the [minimum requirements](../installation-guide/index.md) to deploy the Gluu Server.  

## Install Gluu Server Package

!!! Note
    Installation of the Gluu server will be done under `/root`. The Gluu Server will create its file system under `/root/` and will be installed under `/opt`. File size and [minimum requirements](../installation-guide/index.md) remain the same as the host.
   
### Ubuntu Server 14.04.x

| Command Description     |               Trusty Commands         |
|-------------------------|---------------------------------------|
| Add Gluu Repository     | `# echo "deb https://repo.gluu.org/ubuntu/ trusty main" > /etc/apt/sources.list.d/gluu-repo.list` |
| Add Gluu GPG Key        | `# curl https://repo.gluu.org/ubuntu/gluu-apt.key | apt-key add -` |
| Update/Clean Repo       | `# apt-get update`                         |
| Install Gluu Server     | `# apt-get install gluu-server-3.0.1`      |
    
### Ubuntu Server 16.04.x

|  Command Description    |               Xenial Commands         |
|-------------------------|---------------------------------------|
| Add Gluu Repository     | `# echo "deb https://repo.gluu.org/ubuntu/ xenial main" > /etc/apt/sources.list.d/gluu-repo.list` |
| Add Gluu GPG Key        | `# curl https://repo.gluu.org/ubuntu/gluu-apt.key | apt-key add -` |
| Update/Clean Repo       | `# apt-get update`                         |
| Install Gluu Server     | `# apt-get install gluu-server-3.0.1`      |

### CentOS 6.x

| Command Description     |               CentOS 6.x              |
|-------------------------|---------------------------------------|
| Add Gluu Repository     | `# wget https://repo.gluu.org/centos/Gluu-centos6.repo -O /etc/yum.repos.d/Gluu.repo`|
| Add Gluu GPG Key        | `# wget https://repo.gluu.org/centos/RPM-GPG-KEY-GLUU -O /etc/pki/rpm-gpg/RPM-GPG-KEY-GLUU`|
| Import GPG Key          | `# rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-GLUU`|
| Update/Clean Repo       | `# yum clean all`                          |
| Install Gluu Server     | `# yum install gluu-server-3.0.1`          |

### CentOS 7.2

| Command Description     |               CentOS 7.2              |
|-------------------------|---------------------------------------|
| Add Gluu Repository     | `# wget https://repo.gluu.org/centos/Gluu-centos7.repo -O /etc/yum.repos.d/Gluu.repo` |
| Add Gluu GPG Key        | `# wget https://repo.gluu.org/centos/RPM-GPG-KEY-GLUU -O /etc/pki/rpm-gpg/RPM-GPG-KEY-GLUU`|
| Import GPG Key          | `# rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-GLUU` |
| Update/Clean Repo       | `# yum clean all`                          |
| Install Gluu Server     | `# yum install gluu-server-3.0.1`          |

### RHEL 6.x

| Command Description     |               RHEL 6.x              |
|-------------------------------|---------------------------------------|
| Add Gluu Repository     | `# wget https://repo.gluu.org/centos/Gluu-centos6.repo -O /etc/yum.repos.d/Gluu.repo` |
| Add Gluu GPG Key        | `# wget https://repo.gluu.org/centos/RPM-GPG-KEY-GLUU -O /etc/pki/rpm-gpg/RPM-GPG-KEY-GLUU`|
| Import GPG Key          | `# rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-GLUU` |
| Update/Clean Repo       | `# yum clean all`                          |
| Install Gluu Server     | `# yum install gluu-server-3.0.1`          |

### RHEL 7.2

| Command Description     |               RHEL 7                  |
|-------------------------|---------------------------------------|
| Add Gluu Repository     | `# wget https://repo.gluu.org/rhel/Gluu-rhel7.repo -O /etc/yum.repos.d/Gluu.repo` |
| Add Gluu GPG Key        | `# wget https://repo.gluu.org/rhel/RPM-GPG-KEY-GLUU -O /etc/pki/rpm-gpg/RPM-GPG-KEY-GLUU`|
| Import GPG Key          | `# rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-GLUU` |
| Update/Clean Repo       | `# yum clean all`                          |
| Install Gluu Server     | `# yum install gluu-server-3.0.1`          |

### Debian 8 (Jessie)

| Command Description     |               Jessie Commands         |
|-------------------------|---------------------------------------|
| Add Gluu Repository     | `# echo "deb https://repo.gluu.org/debian/ stable main" > /etc/apt/sources.list.d/gluu-repo.list`|
| Add Gluu GPG Key        | `# curl https://repo.gluu.org/debian/gluu-apt.key | apt-key add -` |
| Update/Clean Repo       | `# apt-get update`                         |
| Install Gluu Server     | `# apt-get install gluu-server-3.0.1`      |

## Start the Gluu Server and Login

The Gluu Server is a chroot container, which you must start to proceed. 

For Centos 6.x, Red Hat 6.x, Ubuntu 14/16, and Debian 8:

```
# service gluu-server-3.0.1 start
# service gluu-server-3.0.1 login
```

For Centos 7.2 and Red Hat 7.2: 

```
# /sbin/gluu-serverd-3.0.1 enable
# /sbin/gluu-serverd-3.0.1 start
# /sbin/gluu-serverd-3.0.1 login
```

 * Use `enable` just the first time you start the Gluu Server.

## Run `setup.py`

Configuration is completed by running the `setup.py` script. This generates 
certificates, salt values, and renders configuration files. After
completion, you're done! Note: you must be logged into the Gluu Server 
chroot container to run `setup.py` (see Step 2 above). 

```
# cd /install/community-edition-setup
# ./setup.py
```

You will be prompted to answer some questions. Just hit `Enter` to
accept the default value specified in square brackets. The following
table should help you answer the questions correctly.

| Question                |  Explanation                               |
|-------------------------|--------------------------------------------|
| Enter IP Address | Used primarily by Apache HTTPD for the [Listen](https://httpd.apache.org/docs/2.4/bind.html) directive|
| Enter hostname | Internet-facing hostname, FQDN or CNAME whichever your organization follows to be used to generate certificates and metadata. **Don't use an IP address or localhost here** |
| Enter your city or locality | Used to generate X.509 certificates |
| Enter your state or province two letter code | Used to generate X.509 certificates |
| Enter two letter Country Code | Used to generate X.509 certificates |
| Enter Organization Name | Used to generate X.509 certificates |
| Enter email address for support at your organization | Used to generate X.509 certificates | 
| Optional: enter password for oxTrust and LDAP superuser | Used as the LDAP directory manager password, and for the default admin user for oxTrust |
| Install oxAuth OAuth2 Authorization Server | Required|
| Install oxTrust Admin UI | Required |
| Install LDAP Server | Required |
| Install Apache HTTPD Server | Required |
| Install Shibboleth SAML IDP | Optional: install only if you want outbound SAML |
| Install Asimba SAML Proxy | Optional: install only if you are supporting SAML from other domains' IDPs. |
| Install CAS | Deprecated: install only if you have existing CAS apps |
| Install oxAuth RP | OpenID Connect test client: recommended for test enviornments, for more details see [here](../admin-guide/openid-connect/#oxauth-rp) |
| Install Passport | Component used for social login |

After answering these questions, `setup.py` will show you your 
selections, and ask you if you want to continue. 

The easiest place to go wrong is with the first two questions. Don't 
use `localhost` for either the IP address or hostname. And use a real
hostname--you can always manage via host file entries even if you don't 
want to mess with DNS for testing. If you are deploying a cluster, use
the hostname of the cluster--that is used by the clients connecting
to the Gluu Server.

!!! Warning
	Changing of hostname after installation is not supported. 

## Uninstallation

Something went wrong? No problem, just uninstall and reinstall.

For Ubuntu 14/16, and Debian 8:

```
# service gluu-server-3.0.1 stop
# apt-get remove gluu-server-3.0.1
# rm -rf /opt/gluu-server-3.0.1
```

For Centos 6.x, Red Hat 6.x, 

```
# service gluu-server-3.0.1 stop
# yum remove gluu-server-3.0.1
# rm -rf /opt/gluu-server-3.0.1
```

For Centos 7.2 and Red Hat 7.2:

```
# /sbin/gluu-serverd-3.0.1 disable
# /sbin/gluu-serverd-3.0.1 stop
# yum remove gluu-server-3.0.1 
# rm -rf /opt/gluu-server-3.0.1
```
