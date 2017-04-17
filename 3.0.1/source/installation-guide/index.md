# Preparing VM for Gluu Server Installation
## Overview
Thank you for your interest in the Gluu Server! This document will provide instructions for preparing your VM for a standard Gluu Server deployment. Once your servers are ready you can move on to the [installation instructions](../installation-guide/install.md). Good luck with your deployment, and welcome to the community!

## Minimum Requirements

The Gluu Server Community Edition (CE) needs to be deployed on a 
server or VM with the following **minimum** requirements. 

|CPU Unit  |    RAM     |   Disk Space      | Processor Type |
|----------|------------|-------------------|----------------|
|       2  |    4GB     |   40GB            |  64 Bit        |

!!! note
    If you plan on installing more than the default components (i.e. oxAuth, oxTrust, and LDAP), we recommend that your server or VM have at least 8GB of RAM. 

!!! warning
    Please only post installation issues to [Gluu Support](https://support.gluu.org) if all the above requirements are met!

## Ports

The following ports are open to the Internet by default.

|       Port Number     |       Protocol        |   Notes          |
|-----------------------|-----------------------|------------------|
|       80              |       tcp             | Forwards to 443  |
|       443             |       tcp             | Apache HTTPD     |
|       22              |       tcp             | ssh              |


## File Descriptors

The Gluu Server **requires** setting the `file descriptors` to 65k. 
Follow these steps or research how to do this on your Linux platform.

* Add the following lines in the `/etc/security/limits.conf` file.

```
* soft nofile 65536
* hard nofile 262144
```

* Add the following lines to `/etc/pam.d/login`
```
session required pam_limits.so
```

* Increase the file descriptor limit to 65535. The system file limit 
is set in `/proc/sys/fs/file-max`.

It is recommended to check the file descriptor size before increasing, 
and if the file descriptor size more than the default and customized, 
it is the recommended to the use the higher file size.
File descriptor size can be found using the below command. 

```
# cat /proc/sys/fs/file-max
```
> Please note command may vary depending on the OS flavor used.

```
echo 65535 > /proc/sys/fs/file-max**
```
* Use the `ulimit` command to set the file descriptor limit to the hard limit specified in `/etc/security/limits.conf`.

```
** ulimit -n unlimited**
```

!!!Note:
    Centos by default will not accept more than the default maximum of 65535. You may get an error while performing the above command.

* Restart your system.     

## Amazon AWS      

Amazon AWS instances provide a public and private IP address. While
running the `/install/community-edition-setup/setup.py` script, use the
Private IP address. Also, use a hostname other then the long default
hostname that Amazon provides. Update your DNS or hosts files accordingly.

## Microsoft Azure      

Accessing the Gluu Server on Azure can be a little bit tricky because of
the Public/Private IP. Azure assigns a new Public/Private IP
addresses each time the server is started. 

### Setting up VM       
1. Log into Windows Azure Administrative Panel

2. Click on `Virtual Machines` tab, and click `Create a Virtual Machine` link

3. From the menu, choose `Compute` > `Virtual Machine` > `From Gallery` branch.

4. Choose Ubuntu Server 14.04 LTS or CentOS 6.7. Remember to set selinux
   to permissive if you choose CentOS.

5. Provide a name for the VM in the `Virtual Machine Name` field and use `Standard` for `Tier`.

6. Select a server with at least 4GB RAM in the `Size` dropdown menu.

7. Provide a username/password to connect via ssh and upload ssh certificate. Click `Next`.

8. Create a new cloud service and select `None` for the `Availability Set` option.
        * Endpoints Section: This is where port forwarding is set so
      that the internal IP address can be selectively reachable from
      the outside world. By default, only tcp /22 is there for ssh. The
      public ports for `http` and `https` (tcp ports 80 and 443) have to be
      added and mapped to the same private ports. If the cloud mappings
      are flagged conflicting, proceed without setting them. Remember to
      set them after the creation of the VM. Then, click `Next`.

9. Choose not to install `VM Agent` and click the `tick` button to
   finalize the VM.

10. Go to the `Dashboard` tab of VM Management Panel and copy the `DNS
    Name`. This is the name that is used to access the Gluu Server.

11. You should now be able to ssh to the server and proceed with the 
    installation.


## Linode VM

Linode Virtual Machines (VM) use a custom kernel which is not 
supported by the Gluu Server, therefore the kernel must be updated before 
the Gluu Server can be installed in a Linode VM. The following steps will 
guide you through kernel update in the Linode VM.

* Check for the current version of the kernel. If the output contains `-Linode`, then proceed
```
# uname -a
```

* Run the following command to update the kernel:
```
# apt-get install linux-image-virtual grub2
```

* Modify `grub` file in the `/etc/default/` folder:
```
# vim /etc/default/grub
```

  * Ensure that the following lines are present in the grub file
```
GRUB_TIMEOUT=10
GRUB_CMDLINE_LINUX="console=ttyS0,19200n8"
GRUB_DISABLE_LINUX_UUID=true
GRUB_SERIAL_COMMAND="serial --speed=19200 --unit=0 --word=8 --parity=no --stop=1"
```

* Finally run the following commands to update `grub` and reboot:
```
# update-grub
# reboot
```
