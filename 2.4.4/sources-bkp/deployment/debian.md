# Debian 8 Installation Guide
## Installing Gluu Server 
Download and install Gluu Server by the following commands. Use the
`.deb` installation to perform a base chroot installation with the
following Gluu Server Base Ubuntu requirements.

As an alternative, use our Gluu repository for Debian Jessie (8):

```
# echo "deb https://repo.gluu.org/debian/ stable main" > /etc/apt/sources.list.d/gluu-repo.list

# curl https://repo.gluu.org/debian/gluu-apt.key.new-xenial | apt-key add -

# apt-get update

# apt-get install gluu-server-2.4.4.2
```
**Note: While entering the "deb" command manually, make sure to enter an extra space between "/debian/" and "stable main".**

## Configuring Gluu Server
After both the retrieval, and the installation of the Gluu Server
software package start the Gluu Server, and login into the local chroot
environment to configure the Gluu Server. 

Below are the steps to configure Gluu Server:

1. Start the Gluu Server
2. Login into local chroot environment to configure Gluu Server.
3. Navigate or change to community-edition-setup directory where setup.py script is located.
4. Run setup.py to configure the Gluu Server

```
# /etc/init.d/gluu-server-2.4.4.2 start
# /etc/init.d/gluu-server-2.4.4.2 login
# cd /install/community-edition-setup/
#./setup.py
```

The `setup.py` script will bring up a prompt to provide information for certificate. It is recommened to use
`hostname.domain` structure for hostname and refrain from using `127.x.x.x`
for IP address. After the successful execution of `setup.py` script, login to oxTrust,
the policy administration point for Gluu. 

Access the oxtrust UI from the local browser using `https://hostname.domain`, which was provided during the configuration. And the uri will be mentioned at the end of successful configuration.

For both help and the latest installation options see either [setup.py help](./setup_py.md), or run `./setup.py -h`.

If resolvable DNS host is not used, add the hostname to your hosts file on the server or the system where the oxtrust UI is accessed.
Login with the default user name “admin” and the password used in
the configuration (also contained in `setup.properties.last` use the
Unix command `grep --color -i pass` to find the according line quickly)
and look for the LDAP password which is the same as the admin password.

Make sure to remove or encrypt `setup.properties.last` It has the clear 
text passwords for everything: LDAP, admin user, keystores, and 3DES salt.
If something goes wrong, check `setup.log` for a detailed step-by-step
analysis of the installation. As an alternative,check the file
`setup_errors.log` to just see the errors (or stderr output from the
scripts).

## Removing/disabling Gluu repo


After initial installation is completed, it is recommended to remove Gluu
repos from sources list, to avoid accidental upgrade of the Gluu package by conducting regular system's update procedures (like, by running `# apt-get update`)

Either remove `/etc/apt/sources.list.d/gluu-repo.list` file, or modify it
commenting out lines declaring Gluu CE's repos there.

## Starting and Stopping the Gluu Server

To start the Gluu Server use the below command:

```
# /etc/init.d/gluu-server-2.4.4.2 start

```

To stop the Gluu Server use the below command:

```
# /etc/init.d/gluu-server-2.4.4.2 stop

```
To check the status of Gluu Server use the below command:

```
# /etc/init.d/glu-server-2.4.4.2 status
```

## Login to the chroot environment

```
# /etc/init.d/gluu-server-2.4.4.2 login

```

alternatively sudo can be used as below

```
# chroot /home/gluu-server24/ su -

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

Below are the steps to script the installation of the Gluu Server: 

Step by Step instructions to uninstall Gluu Server:

1.  Exit from the chroot environment to main linux, by entering Logout command.
2.  Stop the Gluu Server chroot environment which will unmount allchroot directories.
3.  Delete both the Gluu Server packages that are installed, and the home directory of the Gluu Server user.

The following commands illustrate the steps:

```
# service gluu-server-2.4.4.2 stop
# apt-get remove gluu-server-2.4.4.2
# rm -rf /opt/gluu-server-2.4.4.2*
```

During an installation, any modified files are saved in the directory
`/home/gluu-server-2.4.4.2.save`. If required to remove all the remnants of the
installation, delete these files with the command `rm -rf /home/gluu-server-2.4.4.2.save'.

In some circumstances, the installation can be broken. In that case
please try the following to force to uninstall the package.

```
# dpkg --purge --force-all gluu-server-2.4.4.2

```

## Support

Gluu offers both community and VIP support. Anyone can browse and open
tickets on our [support portal](http://support.gluu.org). For private
support, expedited assistance, and strategic consultations, please view
[our pricing](http://gluu.org/pricing) and [schedule a meeting with
us](http://gluu.org/booking) to discuss VIP support options.
