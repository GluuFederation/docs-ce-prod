# Preparing VM for Gluu Server Installation
## Overview

Thank you for your interest in the Gluu Server! 

This document will provide instructions for preparing a VM  for a standard Gluu Server deployment (i.e. **not** Docker). Once the server is ready, move on to the [installation instructions](../installation-guide/install.md). 

Good luck and welcome to the community!

!!! Note
    To learn more about software licenses, use cases, and more, visit the [docs homepage](../index.md)    
    
## System Requirements

Set up a server or VM with the following **minimum** requirements: 

|CPU Unit  |    RAM     |   Disk Space      | Processor Type |
|----------|------------|-------------------|----------------|
|       2  |    4GB     |   40GB            |  64 Bit        |


A few additional notes about system requirements:

- When installing more than the default components (i.e. oxAuth, oxTrust, and LDAP), we recommend using a machine with **at least 8GB of RAM**. 

- Gluu must be deployed on a server or VM with a static IP Address. The static IP address should resolve to a computer hostname which can be achieved by adding an entry to the DNS server or in `/etc/hosts`.     

- If setting up a VM locally, we recommend using VM Player (**not** Virtual Box).

    
## Supported Operating Systems
Deploy Gluu on a server or VM with one of the following supported operating systems:

- Ubuntu 16, 18
- CentOS 7.x
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

To check the status of these ports in Ubuntu, use the following commands (other OS have similar commands):

```
ufw status verbose
```


The default for `ufw` is to `deny incoming` and `allow outgoing`. To reset your setting to default :

```
ufw default deny incoming
```

```
ufw default allow outgoing
```

reset `ufw`

```
ufw reset
```

If for any reason the ports are closed, allow connections by:

```
ufw allow <port>
```

Ports 443, 80, and 22 must be accessible. 

!!! Note
    For clustered deployments, [more ports must be configured](../installation-guide/cluster.md).
    
## File Descriptors (FD)

The Gluu Server requires setting the **`file descriptors` to 65k**.

Follow these steps or research how to do this on your Linux platform.

* Add the following lines in the `/etc/security/limits.conf` file.

```
* soft nofile 65535
* hard nofile 262144
```

* Add the following lines to `/etc/pam.d/login` if not already present.

```
session required pam_limits.so
```

* Increase the FD limit to 65535. The system file limit is set in `/proc/sys/fs/file-max`.

It is recommended to check the FD limit before increasing it. If this limit is customized and more than default, we recommend using the higher one. The FD limit can be found using the following command. 

```
# cat /proc/sys/fs/file-max
```

Please note, the command may vary depending on the OS in use.

```
echo 65535 > /proc/sys/fs/file-max**
```

* Use the `ulimit` command to set the FD limit to the hard limit specified in `/etc/security/limits.conf`.

```
ulimit -n 262144
```

!!! Note
    CentOS by default will not accept more than the default maximum of 65535. You may get an error while performing the above command.


If the above does not work, use the `ulimit` command to set the FD limit to the soft limit of the file `/etc/security/limits.conf`

```
ulimit -n 65535
```

* Restart the system. 

## IP Address
    
The Server or VM must be deployed on a static IP address. Cloud servers should already have that set. When installing the Gluu Server, make sure the server has a static IP.

In Linux, open the following using any editor:

```
vi /etc/network/interfaces
```

Below is the network configuration. Notice `iface ens33 inet` is set to `dhcp`.

```
#This file describes the network interfaces available on your system
#and how to activate them. For more information, see interfaces(5).

source /etc/network/interfaces.d/*

# The loopback network interface
auto lo
iface lo inet loopback

# The primary network interface
auto ens33
iface ens33 inet dhcp

```

Comment out the line that contains the `dhcp` by adding `#` in front of it and add the values for the `address`, `netmask`, `network`, `broadcast`, `gateway`, and `dns-nameservers` of the network, as seen in the example below:

```
#This file describes the network interfaces available on your system
#and how to activate them. For more information, see interfaces(5).

source /etc/network/interfaces.d/*

# The loopback network interface
auto lo
iface lo inet loopback

# The primary network interface
auto ens33
#iface ens33 inet dhcp
iface ens33 inet static
    # This value is an example
    address 192.168.1.10 
    # This value is an example
    netmask 255.255.255.0
    # This value is an example
    network 192.168.1.0 #
    # This value is an example
    broadcast 192.168.1.255
    # This value is an example
    gateway 192.168.1.1 
    
# This value is an example
dns-nameservers 8.8.8.8 8.8.4.4 # This value is an example
```

Restart the network service:

```
service networking restart
```
or

```
/etc/init.d/networking restart
```

Restart the server.

## Fully Qualified Domain Name (FQDN)

Gluu must be deployed on a fully qualified domain name (FQDN), e.g. `https://my-gluu.server.com`. Localhost is **not** supported. 

In Linux, edit the hosts file and add the appropriate IP Address and FQDN. For example:

```
vi /etc/hosts
```
If the IP was `192.168.1.1`, and the FQDN was `test.gluu.org`, add this to all hosts files:

```
192.168.1.1 test.gluu.org
```

!!! Note
     The Windows hosts file is located at `C:\Windows\System32\drivers\etc\hosts`

## Cloud-specific notes

### Amazon AWS      

Amazon AWS instances provide a public and private IP address. While running the `/install/community-edition-setup/setup.py` script, **use the Private IP address**. Also, use a hostname other than the long default hostname that Amazon provides as CN(Canonical Name). Update the DNS or hosts file accordingly.

### Google Cloud Platform

Gluu Server installation in GCP is pretty straight forward. We need to check a couple of points for this installation: 

 - Deployer must select supported operating system and required resources. 
 - Enable 'HTTPS' from 'Firewall'
 - Do not enter any IP during the installation of Gluu Server, the setup script will automatically 
gather appropriate IP information. 
 - When accessing the newly installed Gluu server from a browser, update the DNS or hosts file accordingly. 
 
 A video tutorial is also available in the [Gluu channel](https://www.youtube.com/watch?v=0RskrQG8km8)

### Microsoft Azure      

Accessing the Gluu Server on Azure can be a little tricky because of
the Public/Private IP. Azure assigns new Public/Private IP
addresses each time the server is started. 

Follow these steps to set up the VM on Azure:
    
1. Log into Windows Azure Administrative Panel

2. Navigate to `Virtual Machines` > `Create a Virtual Machine`

3. From the menu, choose `Compute` > `Virtual Machine` > `From Gallery` branch.

4. Choose the operating system. Remember to set selinux
   to permissive if you choose CentOS.

5. Provide a name for the VM in the `Virtual Machine Name` field and use `Standard` for `Tier`.

6. Select a server with at least 4GB RAM in the `Size` dropdown menu.

7. Provide a username/password to connect via SSH and upload an SSH certificate. Click `Next`.

8. Create a new cloud service and select `None` for the `Availability Set` option.
        * Endpoints Section: This is where port forwarding is set so
      that the internal IP address can be selectively reachable from
      the outside world. By default, only tcp /22 is there for SSH. The
      public ports for `http` and `https` (tcp ports 80 and 443) have to be
      added and mapped to the same private ports. If the cloud mappings
      are flagged as conflicting, proceed without setting them. Remember to
      set them after the creation of the VM. Then, click `Next`.

9. Choose not to install `VM Agent` and click the `tick` button to
   finalize the VM.

10. Go to the `Dashboard` tab of VM Management Panel and copy the `DNS
    Name`. This is the name that is used to access the Gluu Server.

11. SSH to the server and proceed with the 
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
