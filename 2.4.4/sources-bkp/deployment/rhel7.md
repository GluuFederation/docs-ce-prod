# RHEL 7 Installation Guide
## Installing Gluu Server 
Download and install Gluu Server by the following commands. Use the
`.rpm` installation to perform a base chroot installation with the
following Gluu Server Base CentOS requirements.

As an alternative, use our Gluu repository for RHEL 7:

```
# wget https://repo.gluu.org/rhel/Gluu-rhel7.repo -O /etc/yum.repos.d/Gluu.repo
# wget https://repo.gluu.org/rhel/RPM-GPG-KEY-GLUU -O /etc/pki/rpm-gpg/RPM-GPG-KEY-GLUU
# rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-GLUU
# yum clean all
# yum install gluu-server-2.4.4.2
```

**Note:It is recommended to copy and paste the commands to avoid errors and issue**

## Configuring Gluu Server
After both the retrieval, and the installation of the Gluu Server
software package start the Gluu Server, and login into the local chroot
environment to configure the Gluu Server. 

Below are the steps to configure Gluu Server:

1.  Start the Gluu Server.
2.  Login into local chroot environment toconfigure Gluu Server.
3.  Navigate or change to community-edition-setup directory where setup.py script is located.
4.  Run setup.py to configure the Gluu Server

```
# /sbin/gluu-serverd-2.4.4.2 start
# /sbin/gluu-serverd-2.4.4.2 enable
# /sbin/gluu-serverd-2.4.4.2 login
# cd /install/community-edition-setup/
#./setup.py
```

The `setup.py` script will bring up a prompt to provide information for certificate. It is recommened to use
`hostname.domain` structure for hostname and refrain from using `127.x.x.x`
for IP address. After the successful execution of `setup.py` script, login to oxTrust,
the policy administration point for Gluu. Access the oxtrust UI from the local browser using `https://hostname.domain`, which was provided during the configuration. And the uri will be mentioned at the end of successful configuration.

For both help and the latest installation options see either [setup.py help](./setup_py.md), or run `./setup.py -h`.

If resolvable DNS host is not used, add the hostname to your hosts file on the server or the system where the oxtrust UI is accessed.
Login with the default user name “admin” and the password used in
the confirmation (also contained in `setup.properties.last` use the
Unix command `grep --color -i pass` to find the according line quickly)
and look for the LDAP password which is the same as the admin password.

Make sure to remove or encrypt `setup.properties.last` It has the clear 
text passwords for everything: LDAP, admin user, keystores, and 3DES salt.
Logs can be analyzed for installation error, check `setup.log` for a detailed step-by-step
analysis of the installation. As an alternative, check the file
`setup_errors.log` to just see the errors (or stderr output from the
scripts).

## Removing/disabling Gluu repo

After initial installation is completed, it's recommended to remove Gluu
repos from sources list, to avoid accidental upgrade of the Gluu package by conducting regular system's update procedures (like, by running `# yum update`)

Either remove `/etc/yum.repos.d/Gluu.repo` file, or modify it setting
"enabled" property to "0" for Gluu CE repos there.

## Starting and Stopping the Gluu Server

To start the Gluu Server use the below command:

```
# /sbin/gluu-serverd-2.4.4.2 start
```

To start the Gluu Server use the below command:

```
# /sbin/gluu-serverd-2.4.4.2 stop
```

To check the status of Gluu Server use the below command:

```
#/sbin/gluu-serverd-2.4.4.2 status
```

## Login to the chroot environment

```
# /sbin/gluu-serverd-2.4.4.2 login
```

### Scripted Installation

Below are the steps to script the installation of the Gluu Server:

* Save and backup your existing file `setup.properties.last`.
* Uninstall existing Gluu Server installation.
* For a new installation you can either grab a new VM, or just use the
  existing one.
* Run all the commands until `service gluu-server24 login`.
* Copy your file `setup.properties.last` into the new server's
  `/install/community-edition-setup/` location.
* Rename the file `setup.properties.last` to `setup.properties`.
* Run the setup script with `./setup.py` command.

## Uninstallation

1.  Exit from the chroot environment to main linux, by entering Logout command.  
2.  Stop the Gluu Server chroot environment which will unmount allchroot directories. 
3.  Delete both the Gluu Server packages that are installed, and the home directory of the Gluu Server user.

The following commands illustrate the steps:

```
# /sbin/gluu-serverd-2.4.4.2 stop
# yum remove gluu-server-2.4.4.2
# rm -rf /opt/gluu-server-2.4.4.2*
```
## Support

Gluu offers both community and VIP support. Anyone can browse and open
tickets on our [support portal](http://support.gluu.org). For private
support, expedited assistance, and strategic consultations, please view
[our pricing](http://gluu.org/pricing) and [schedule a meeting with
us](http://gluu.org/booking) to discuss VIP support options.
