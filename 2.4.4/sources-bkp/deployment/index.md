# Hardware Requirements
The Gluu Server is very flexible, and can be used for a wide array of
access management requirements. Depending on the size of data, and
the number of concurrent transactions to be supported, memory and CPU capacity requirements may vary.

If Gluu Server services are running on the same server (i.e.
SAML, OAuth2, LDAP), server will need at least:

|CPU Unit	|	RAM	|	Disk Space	|
|---------------|---------------|-----------------------|
|	2	| 	4GB 	| 	40GB		|

**Note:** *Not enough memory may produce some issues or errors, which may require few adjustments on the resources based on environment's specific requirements.*

## Operating System Requirement
Gluu Server Community Edition is available for the following Operating Systems.
Click on the desired operating system for deployment guide.

|	Operating System	|	Supported Versions	|	Architecture|	
|-------------------------------|-------------------------------|-------------------|
|[Ubuntu Server](./ubuntu.md)	|**14.04.2**			|	64 Bit|
|[CentOS 6.x](./centos.md)	|**6.5**, **6.6**, **6.7**	|	64 Bit|
|[CentOS 7.2](./centos7.md)	|**7.1**			|	64 Bit|
|[RHEL 6.x](./rhel.md)		|**6.5**, **6.6**, **6.7**	|	64 Bit|
|[RHEL 7](./rhel7.md)		|**7**				|	64 Bit|
	
## Memory allocated for Tomcat's heap.
Tomcat's heap  will require at least 3GB of RAM to spin up a test instance of Gluu CE 2.4.3 (and later). For production setups it is recommended to allocate at least 4-6GB of RAM to spin up a test instance of Gluu CE 2.4.3 and later.

Tomcat configuration will allow to enter the allocation of RAM amount during `setup.py` script's phase of installation. Allocation of RAM could also be modified after the installation has completed, by editing `/opt/tomcat/conf/gluuTomcatWrapper.conf` file inside of the container and setting `wrapper.java.initmemory` and `wrapper.java.maxmemory` properties to desired values.

## File Descriptor
Set `file descriptors`
to 65k. Following steps will help set the `file descriptor` limit.

* Edit the `/etc/security/limits.conf` file.
* By adding following lines to the file you can set default limits which will apply to any user for whom they weren't specified explicitly:
	
```
* soft nofile 65536
* hard nofile 262144
```

* If set limits are set per-user basis for "tomcat", "ldap" and "apache" users, next directives can be used (please note, that users under which different Gluu services run within container may be named differently in different linux distros; need to edit provided examples accordingly):

```
    ldap soft nofile 131072
    ldap hard nofile 262144

    apache soft nofile 131072
    apache hard nofile 262144

    tomcat soft nofile 131072
    tomcat hard nofile 262144
```

* Edit the `/etc/pam.d/login` by adding the line:
```
session required pam_limits.so
```
* Use the system file limit to increase the file descriptor limit to 262144. The system file limit is set in `/proc/sys/fs/file-max`.
```
echo 262144 > /proc/sys/fs/file-max
```

* Use the `ulimit` command to set the file descriptor limit to the hard limit specified in `/etc/security/limits.conf`.
```
ulimit -n unlimited
```
* Restart the server.

## Port
The following ports need to stay open for the Gluu Server to run. Please keep the ports open before installing Gluu Server.

|	Port Number	|	Protocol	|
|-----------------------|-----------------------|
|	80		|	tcp		|
|	443		|	tcp		|

## Disable SELinux
* Make sure there is "SELINUX=disabled" directive in the /etc/selinux/config file.
* Reboot your system. After reboot, confirm that the __getenforce__ command returns __Disabled__.

## Cloud Specific Requirements
## Amazon AWS
Amazon AWS provides a public and private IP address to its clouds. While
running the `/install/community-edition-setup/setup.py` script, use the
Private IP address.

## Microsoft Azure
Accessing the Gluu Server on Azure can be a little bit tricky because of
the Public/Private IP. Azure assigns a new Public/Private IP
addresses each time the server is started. Please see the [Azure Guide](./azure.md) for more info.

## Linode
The Linode Virtual Machines (VM) use a custom kernel which is not supported by Gluu Server, therefore the kernel must be updated before Gluu Server can be installed in Linode VM. Please see the [Linode Guide](./linode.md) to update your Linode VM Kernel.

## Available Components

When deploying the Gluu Server, installer will prompt on the following softwares to be installed along with Gluu Server:

|Software/Component| Feature and Functionality of the component |
|------------------|--------------------------------------------|
|  __oxAuth*__| oxAuth provides endpoints for an OpenID Connect Identity Provider (IdP) and an UMA Authorization Server (AS). Both OpenID Connect and UMA are standard profiles of OAuth 2.0, used for single sign-on (SSO) and web and API access management, respectively.|
|  __oxTrust*__| oxTrust is the graphical user interface that is used for server management.|
|  __LDAP*__ |The Gluu Server ships with a fork of the OpenDJ LDAP server.It is used to store attributes and server configurations locally.|
|  __Apache 2 web server:*__| Apache 2 serves the web server for the Gluu Server. Without Apache 2, it is not possible to see the hostname from a browser.|
|  **Shibboleth 2 SAML IDP:**| The Shibboleth server provides endpoints for a SAML Identity Provider (IdP). If the requirement requires to create single  sign-on (SSO) to a SAML SP, you will need a SAML IdP.|
|  **Asimba SAML Proxy:**| The Asimba SAML proxy should be deployed on if organization needs to consolidate inbound SAML authentication from the IdPs of partners to a single website or app.|
|  **CAS:**| CAS is legacy at this point and should only be deployed if organization has existing apps that can only support CAS for single sign-on.|
|  **oxAuth RP:**| The oxAuth RP is a web UI to enable OpenID Connect discovery, dynamic client registration, and authentication testing.|
|  **oxEleven:**| Web Application providing REST API's for a PKCS #11 interface using SoftHSMv2 as cryptographic store.|

*__Note:__* * implies that the software should *always* be deployed. And recommended to use defaults where ever required.

## Support
Gluu offers both community and VIP support. Anyone can browse and open
tickets on our [support portal](http://support.gluu.org). For private
support, expedited assistance, and strategic consultations, please view
[our pricing](http://gluu.org/pricing) and [schedule a meeting with
us](http://gluu.org/booking) to discuss VIP support options.


