# Preparing VM for Gluu Server Installation
## Overview
Thank you for your interest in the Gluu Server! This document will provide instructions for preparing a VM for a standard Gluu Server deployment. Once the server is ready, move on to the [installation instructions](../installation-guide/install.md). 

Good luck and welcome to the community!

## System Requirements

The Gluu Server needs to be deployed on a server or VM with the following **minimum** requirements: 

|CPU Unit  |    RAM     |   Disk Space      | Processor Type |
|----------|------------|-------------------|----------------|
|       2  |    4GB     |   40GB            |  64 Bit        |

!!! note
    If you plan on installing more than the default components (i.e. oxAuth, oxTrust, and LDAP), we recommend using a machine with at least 8GB of RAM. 

!!! warning
    Docker deployments are not currently supported! 

## Supported Operating Systems
Deploy Gluu on a server or VM with one of the following supported operating systems:

- Ubuntu 14.04, 16.04
- CentOS 6.x, 7.x
- RHEL 6.x, 7.x
- Debian 8

## Ports

The following ports are open to the Internet by default.

|       Port Number     |       Protocol        |   Notes          |
|-----------------------|-----------------------|------------------|
|       80              |       tcp             | Forwards to 443  |
|       443             |       tcp             | apache2/httpd    |
|       22              |       tcp             | ssh              |

!!! Note
    See the [operations guide](../operation/ports.md) for a list of internal ports used by Gluu Server components (e.g. oxAuth, oxTrust, etc.). 

## File Descriptors(FD)

The Gluu Server **requires** setting the `file descriptors` to 65k. 
Follow these steps or research how to do this on your Linux platform.

* Add the following lines in the `/etc/security/limits.conf` file.

```
* soft nofile 65536
* hard nofile 262144
```

* Add the following lines to `/etc/pam.d/login` if not already present.
```
session required pam_limits.so
```

* Increase the FD limit to 65535. The system file limit 
is set in `/proc/sys/fs/file-max`.

It is recommended to check the FD limit before increasing it, and if this limit is customized and more than default, we recommend to the use the higher one. 
    
File descriptors limit can be found using the below command. 

```
# cat /proc/sys/fs/file-max
```
Please note, the command may vary depending on the OS flavor used.

```
echo 65535 > /proc/sys/fs/file-max**
```
* Use the `ulimit` command to set the FD limit to the hard limit specified in `/etc/security/limits.conf`.

```
ulimit -n unlimited
```

!!!Note:
    Centos by default will not accept more than the default maximum. You may get an error while performing the above command. If you do get an error, set it to `ulimit -n 262144`, or `65535` if you get a second error.

* Restart your system.     

## Cloud-specific notes

### Amazon AWS      

Amazon AWS instances provide a public and private IP address. While
running the `/install/community-edition-setup/setup.py` script, **use the
Private IP address**. Also, use a hostname other than the long default
hostname that Amazon provides as CN(Canonical Name). Update your DNS or hosts file accordingly.

### Google Cloud Platform

Gluu Server installation in GCP is pretty straight forward. We need to check couple of 
points for this installation: 

 - Deployer must have to select supported operating system and required resources. 
 - Enable 'HTTPS' from 'Firewall'
 - Do not enter any IP during installation of Gluu Server, setup script will automatically 
gather appropriate IP information. 
 - When accessing newly installed Gluu server from browser, update your DNS or hosts file accordingly. 
 
 A video tutorial is also available in [Gluu channel](https://www.youtube.com/watch?v=0RskrQG8km8)

### Microsoft Azure      

Accessing the Gluu Server on Azure can be a little tricky because of
the Public/Private IP. Azure assigns a new Public/Private IP
addresses each time the server is started. 

Follow these steps to setup the VM on Azure:
    
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


### Linode VM

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
