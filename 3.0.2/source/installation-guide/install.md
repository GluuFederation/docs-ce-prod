# Installation 
## Overview
Gluu publishes packages for Ubuntu, CentOS, RHEL and Debian. The 
installation procedure is similar across all the distributions: 

1. [Install the Linux package](#install-gluu-server-package)
2. [Start the Gluu Server and login to the container](#start-the-gluu-server-and-login)
3. [Run `setup.py`](#run-setuppy)

!!! Note
    The Gluu Server needs to be installed on a VM or physical server with at least 4GB of RAM and 2CPU units. Containers are not supported. Make sure your box meets the [minimum requirements](../installation-guide/index.md) to deploy the Gluu Server. 
    
!!! Warning
    You must use a fully qualified domain name (FQDN) to install the Gluu Server. You **can not** use localhost to install the Gluu Server. If you want to run Gluu locally, you can make up a hostname. Just make sure it is in the host file of your VM and the host file of the local windows machine.

## Install Gluu Server Package

Installation of the Gluu server will be done under `/root`. 
The Gluu Server will create its file system under `/root/` and will be 
installed under `/opt`. File size and [minimum requirements](../installation-guide/index.md) 
remain the same as the host.

### Ubuntu Server 14.04.x

| Command Description     |               Trusty Commands         |
|-------------------------|---------------------------------------|
| Add Gluu Repository     | `# echo "deb https://repo.gluu.org/ubuntu/ trusty main" > /etc/apt/sources.list.d/gluu-repo.list` |
| Add Gluu GPG Key        | `# curl https://repo.gluu.org/ubuntu/gluu-apt.key | apt-key add -` |
| Update/Clean Repo       | `# apt-get update`                         |
| Install Gluu Server     | `# apt-get install gluu-server-3.0.2`      |
    
### Ubuntu Server 16.04.x

|  Command Description    |               Xenial Commands         |
|-------------------------|---------------------------------------|
| Add Gluu Repository     | `# echo "deb https://repo.gluu.org/ubuntu/ xenial main" > /etc/apt/sources.list.d/gluu-repo.list` |
| Add Gluu GPG Key        | `# curl https://repo.gluu.org/ubuntu/gluu-apt.key | apt-key add -` |
| Update/Clean Repo       | `# apt-get update`                         |
| Install Gluu Server     | `# apt-get install gluu-server-3.0.2`      |

### CentOS 6.x

| Command Description     |               CentOS 6.x              |
|-------------------------|---------------------------------------|
| Add Gluu Repository     | `# wget https://repo.gluu.org/centos/Gluu-centos6.repo -O /etc/yum.repos.d/Gluu.repo`|
| Add Gluu GPG Key        | `# wget https://repo.gluu.org/centos/RPM-GPG-KEY-GLUU -O /etc/pki/rpm-gpg/RPM-GPG-KEY-GLUU`|
| Import GPG Key          | `# rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-GLUU`|
| Update/Clean Repo       | `# yum clean all`                          |
| Install Gluu Server     | `# yum install gluu-server-3.0.2`          |

### CentOS 7.x

| Command Description     |               CentOS 7.2              |
|-------------------------|---------------------------------------|
| Add Gluu Repository     | `# wget https://repo.gluu.org/centos/Gluu-centos7.repo -O /etc/yum.repos.d/Gluu.repo` |
| Add Gluu GPG Key        | `# wget https://repo.gluu.org/centos/RPM-GPG-KEY-GLUU -O /etc/pki/rpm-gpg/RPM-GPG-KEY-GLUU`|
| Import GPG Key          | `# rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-GLUU` |
| Update/Clean Repo       | `# yum clean all`                          |
| Install Gluu Server     | `# yum install gluu-server-3.0.2`          |

### RHEL 6.x

| Command Description     |               RHEL 6.x              |
|-------------------------------|---------------------------------------|
| Add Gluu Repository     | `# wget https://repo.gluu.org/centos/Gluu-centos6.repo -O /etc/yum.repos.d/Gluu.repo` |
| Add Gluu GPG Key        | `# wget https://repo.gluu.org/centos/RPM-GPG-KEY-GLUU -O /etc/pki/rpm-gpg/RPM-GPG-KEY-GLUU`|
| Import GPG Key          | `# rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-GLUU` |
| Update/Clean Repo       | `# yum clean all`                          |
| Install Gluu Server     | `# yum install gluu-server-3.0.2`          |

### RHEL 7.x

| Command Description     |               RHEL 7                  |
|-------------------------|---------------------------------------|
| Add Gluu Repository     | `# wget https://repo.gluu.org/rhel/Gluu-rhel7.repo -O /etc/yum.repos.d/Gluu.repo` |
| Add Gluu GPG Key        | `# wget https://repo.gluu.org/rhel/RPM-GPG-KEY-GLUU -O /etc/pki/rpm-gpg/RPM-GPG-KEY-GLUU`|
| Import GPG Key          | `# rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-GLUU` |
| Update/Clean Repo       | `# yum clean all`                          |
| Install Gluu Server     | `# yum install gluu-server-3.0.2`          |

### Debian 8 (Jessie)

| Command Description     |               Jessie Commands         |
|-------------------------|---------------------------------------|
| Add Gluu Repository     | `# echo "deb https://repo.gluu.org/debian/ stable main" > /etc/apt/sources.list.d/gluu-repo.list`|
| Add Gluu GPG Key        | `# curl https://repo.gluu.org/debian/gluu-apt.key | apt-key add -` |
| Update/Clean Repo       | `# apt-get update`                         |
| Install Gluu Server     | `# apt-get install gluu-server-3.0.2`      |

## Start the Gluu Server and Login

The Gluu Server is a chroot container, which you must start to proceed. 

For Centos 6.x, Red Hat 6.x, Ubuntu 14/16, and Debian 8:

```
# service gluu-server-3.0.2 start
# service gluu-server-3.0.2 login
```

For Centos 7.x and Red Hat 7.x: 

```
# /sbin/gluu-serverd-3.0.2 enable
# /sbin/gluu-serverd-3.0.2 start
# /sbin/gluu-serverd-3.0.2 login
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
| Enter IP Address | Used primarily by Apache HTTPD for the [Listen](https://httpd.apache.org/docs/2.4/bind.html) directive. **Use an IP address assigned to one of this server's network interfaces (usage of addresses assigned to loopback interfaces is not supported)**|
| Enter hostname | Internet-facing FQDN that is used to generate certificates and metadata. **Do not use an IP address or localhost.** |
| Enter your city or locality | Used to generate X.509 certificates. |
| Enter your state or province two letter code | Used to generate X.509 certificates. |
| Enter two letter Country Code | Used to generate X.509 certificates. |
| Enter Organization Name | Used to generate X.509 certificates. |
| Enter email address for support at your organization | Used to generate X.509 certificates. | 
| Optional: enter password for oxTrust and LDAP superuser | Used as the LDAP directory manager password, and for the default admin user for oxTrust. |
| Install oxAuth OAuth2 Authorization Server | Required. Includes Gluu's OpenID Connect provider (OP) and UMA authorization server (AS) implementations.|
| Install oxTrust Admin UI | Required. This is the Gluu server admin dashboard. |
| Install LDAP Server | Required. LDAP is used to store user info and configuration data. |
| Install Apache HTTPD Server | Required |
| Install Shibboleth SAML IDP | Optional: only install if you need to a SAML identity provider. |
| Install Asimba SAML Proxy | Optional: only install if you need to send users to external SAML IDPs for authentication. |
| Install oxAuth RP | OpenID Connect test client: recommended for test enviornments, for more details see [here](../admin-guide/openid-connect/#oxauth-rp) |
| Install Passport |  Install if you want to offer users social login. |

!!! Warning
	Changing the hostname after installation is not supported. 

After answering these questions, `setup.py` will show you your selections and ask you if you want to continue. If everything looks good, select Y to finish installation. 

Note: the easiest place to go wrong is with the first two questions:

1. Do not use `localhost` for either the IP address or hostname.  

2. Use a real hostname--you can always manage via host file entries even if you don't want to mess with DNS for testing. If you are deploying a cluster, use the hostname of the cluster--that is used by the clients connecting to the Gluu Server.

After 5-10 minutes you will see the following success message: Gluu Server installation successful! Point your browser to [hostname]. 

## Login via Browser

Wait about 10 minutes in total for the server to restart and finalize its configuration. After that period you are now ready to log into your Gluu Server via a web browser. 

Note: If the Gluu Server login page is still not appearing after you've received the success message and waited about 10 minutes, check if port 443 is open in the VM. If it is not open, open port 443 and try to reach the host in your browser again. 

## Clustering

If you need to support fail over and high availability, the Gluu Server can be clustered using the 
Gluu Cluster Manager product. After you have followed the instructions to deploy your single Gluu Server, you can follow the [Gluu Cluster Manager documentation](https://gluu.org/docs/cm/alpha) to replicate data and cluster your servers.

## Uninstallation

Something went wrong? No problem, just uninstall and reinstall.

For Ubuntu 14/16, and Debian 8:

```
# service gluu-server-3.0.2 stop
# apt-get remove gluu-server-3.0.2
# rm -rf /opt/gluu-server-3.0.2
```

For Centos 6.x, Red Hat 6.x, 

```
# service gluu-server-3.0.2 stop
# yum remove gluu-server-3.0.2
# rm -rf /opt/gluu-server-3.0.2
```

For Centos 7.x and Red Hat 7.x:

```
# /sbin/gluu-serverd-3.0.2 disable
# /sbin/gluu-serverd-3.0.2 stop
# yum remove gluu-server-3.0.2 
# rm -rf /opt/gluu-server-3.0.2
```


