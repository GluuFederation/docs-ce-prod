# Cluster with Gluu CE
It is possible to setup a cluster of servers with Gluu Server CE. This page outlines the setup process of a cluster with two (2) nodes. It is possible to add more nodes, but it is recommened to contact Gluu for higher level solutions.
##Design
The following diagram outlines the design of the cluster.
![image](https://cloud.githubusercontent.com/assets/7156097/13850591/9a553fde-ec28-11e5-8fa7-675f96743a10.png)

## Requirements

For complete deployment requirements and instructions, please see the [Deployment Page](../installation-guide/index.md).
The requirements for Clusters vary only in the RAM requirement. Clusters require at least 8GB RAM for smooth performance. The requirements below are specific for Cluster Installation VMs. Please remember that the requirements from the deployment page will apply as well.


|	Number of VMs	|CPU Units	|	RAM	|Root Partion	|	Port Requirements	|
|-----------------------|---------------|---------------|---------------|-------------------------------|
|	2		|	2 CPU ea.	|	8 GB	|	40 GB	|	4444 and 8989 (LDAP replication), 30865 (file system syncing)|

!!! Note
    For convenience, the nodes are identified as `host-1` and `host-1`

### Csync2 Installation
#### CentOS 6.x

1. Log into Gluu-Server container

2. Install epel-release-latest by running `rpm -ivh https://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm`

3. Install `csync2` package by running `yum install csync2`


#### CentOS 7.x

On the moment of writing csync2 can't be found in public repositories. The only option is to compile from sources. 

Below are the steps:

1. Log into Gluu-Server container

2. Enable epel-release repo: `# yum install epel-release`

3. Install compiler and development environment: `# yum group install "Development Tools"`

4. Install csync2's dependencies:

    1. `# yum install librsync-devel`

    2. `# yum install gnutls-devel`

    3. `# yum install sqlite-devel`

5. `# mkdir building_csync && cd building_csync/`

6. Download the latest version of the tool from [here](http://oss.linbit.com/csync2/): `# wget http://oss.linbit.com/csync2/csync2-2.0.tar.gz`

7. Unpack: `# tar -xz -f ./csync2-2.0.tar.gz && cd csync2-2.0/`

8. Build & install, while directing it to use `/usr/local/etc/csync2/` directory for storing configuration (for convenience): `# ./configure --sysconfdir /usr/local/etc/csync2/ && make && make install`. Don't forget to update paths to csync's binaries and configuration files later on, as they are different from the ones used in examples in the main article!

#### Ubuntu 14.x (compiling from sources)

1. Log into Gluu-Server container

2. Run `apt-get update`

3. Install csync2's dependencies:

    1. `# apt-get install pkg-config`
    
    2. `# apt-get install libsqlite-dev`
    
    3. `# apt-get install libsqlite3-dev`

    4. `# apt-get install librsync-dev`

4. Download the latest version of the tool from [here](http://oss.linbit.com/csync2/): `# wget http://oss.linbit.com/csync2/csync2-2.0.tar.gz`

5. Unpack: `# tar -xz -f ./csync2-2.0.tar.gz && cd csync2-2.0/`

6. Build & install, while directing it to use `/etc/csync2/` directory for storing configuration and `/usr/sbin` directory for executables (for convenience): `./configure --sysconfdir /etc/csync2/ --prefix /usr/ && make && make install`

#### Ubuntu 14.x (from repo)

1. Log into Gluu-Server container

2. Run `apt-get update`

3. Run `apt-get install csync2`

## Preparing VMs

* Install Gluu CE following the [Deployment Page](../installation-guide/index.md) in `host-1`

!!! Note
    The following step must be done right after initial installation of the Gluu CE Package but before finalizing the setup by running the `setup.py` script.

* Copy the `setup.properties.last` file that is generated afther finalizing the installation of Gluu CE on `host-1` and paste it in the `/install/community-edition-setup/` folder inside the `host-2` chroot. Please remember that the interactive setup mode will not run with this command, so add keywords such as `-a` to include asimba, shibboleth or any other component that was installed. Read [this section](#optional-actions-in-case-setuppropertieslast-method-of-installation-didnt-work-for-you) in case you failed to setup Gluu CE in `host-2`.

* Finalize the installation by running the setup script with any additional components that was installed in `host-1`.

## LDAP Replication

|	host-1			|	host-2		   |
|-------------------------------|--------------------------|
|IP Address eg. 192.168.6.1	|Ip Address eg. 192.168.6.2|
|	LDAP admin pass		|	LDAP admin pass	   |
|ldapGeneralConfigInstall.py	|
|replicationSetup.py		|

* Run [ldapGeneralConfigInstall.py](./ldapGeneralConfigInstall.py) in `host-1`. This script will prepare the `host-1` LDAP server to accept various configurations such as `allow-pre-encoded-passwords` or applyting the host and port for LDAP Server.

* Run [replicationSetup.py](./replicationSetup.py) in `host-1` and it will give a similar output as below:

```
[ldap@]$ python replicationSetup.py 
Create a password for the replication admin: 
Enter number of OpenDJ servers: 2
Enter the hostname of server 1: 192.168.6.1
Enter the Directory Manager password for 192.168.6.1: xxxxx
Enter the hostname of server 2: 192.168.6.2
Enter the Directory Manager password for 192.168.6.2: yyyyy

Establishing connections ..... Done.
Checking registration information ..... Done.
Configuring Replication port on server 192.168.6.1:4444 ..... Done.
Configuring Replication port on server 192.168.6.2:4444 ..... Done.
Updating replication configuration for baseDN o=gluu on server 192.168.6.1:4444 ..... Done.
Updating replication configuration for baseDN o=gluu on server 192.168.6.2:4444 ..... Done.
Updating registration configuration on server 192.168.6.1:4444 ..... Done.
Updating registration configuration on server 192.168.6.2:4444 ..... Done.
Updating replication configuration for baseDN cn=schema on server 192.168.6.1:4444 ..... Done.
Updating replication configuration for baseDN cn=schema on server 192.168.6.2:4444 ..... Done.
Initializing registration information on server 192.168.6.2:4444 with the contents of server 192.168.6.1:4444 ..... Done.
Initializing schema on server 192.168.6.2:4444 with the contents of server 192.168.6.1:4444 ..... Done.

Replication has been successfully enabled.  Note that for replication to work you must initialize the contents of the base DNs that are being replicated (use dsreplication initialize to do so).

See /tmp/opendj-replication-8140652343601372868.log for a detailed log of this
operation.

Enabling Replication Complete.
[ldap@...]$
```

* Initialize directory server replication with this command `/opt/opendj/bin/dsreplication initialize` and it will give the following output:

```
[ldap@...]$ /opt/opendj/bin/dsreplication initialize


Specify server administration connection parameters for the source server

Directory server hostname or IP address [idp.gluu.org]: 192.168.6.1

Directory server administration port number [4444]: 

How do you want to trust the server certificate?

    1)  Automatically trust
    2)  Use a truststore
    3)  Manually validate

Enter choice [3]: 1

Global Administrator User ID [admin]: 

Password for user 'admin': #!0^GluU(sWoWSm)


>>>> Specify server administration connection parameters for the destination
server

Directory server hostname or IP address [idp.gluu.org]: 192.168.6.2

Directory server administration port number [4444]: 

How do you want to trust the server certificate?

    1)  Automatically trust
    2)  Use a truststore
    3)  Manually validate

Enter choice [3]: 1

You must choose at least one base DN to be initialized.
Initialize base DN o=gluu? (yes / no) [yes]: 


Initializing the contents of a base DN removes all the existing contents of
that base DN.  Do you want to remove the contents of the selected base DNs on
server 192.168.6.2:4444 and replace them with the contents of server
192.168.6.1:4444? (yes / no) [yes]: 


Initializing base DN o=gluu with the contents from 192.168.6.1:4444:
0 entries processed (0 % complete).
36336 entries processed (99 % complete).
Base DN initialized successfully.

See /tmp/opendj-replication-808135637744675184.log for a detailed log of this
operation.
```

!!! Note
    OpenDJ may become picky about certificates used for SSL connections during replication in certain linux distros. Make sure you've added certificates of each OpenDJ instance to default java key storage of each node; an alternative is to use the same OpenDJ certificate/key pair for both nodes

## File System Replication

!!! Advice
    The backup feature is broken in some of earlier versions of csync2. In that case it msut either be disabled by commenting out `backup-*` clauses in tool's configuration file, or build csync2 version 2.0+ from sources and use key `-l` in your xinetd.d's config (like `server_args     = -i -l -N idp1.gluu.org`) on both nodes.

!!! Warning
    Please verify all pathes (for executables, keys etc) in configuration files' examples before using them in your production instance, as they may differ in different linux distributions.

`csync2` is used for file system syncing between `host-1` and `host-2`. The following locations are synced in between the two VMs.

1. /opt/idp/conf
2. /opt/idp/metadata
3. /opt/idp/ssl
4. /opt/tomcat/conf
5. /etc/csync2/csync2.cfg

### Csync2 configuration for host-1

1. Log into Gluu-Server container

2. Generate `csync2` private key by running `csync2 -k csync2.key` and put it into `/etc/csync2/csync2.key` file

3. Copy the private key to `host-2` and put it into the same file there

4. Generate certificate/key pair that will be used to establish SSL protection layer for incoming connections by running next commands on `host-1` (location of the files and their names are hardcoded into executable). Don't fill any fields, just hit `Enter` accepting default values:

```
openssl genrsa -out /etc/csync2_ssl_key.pem 1024
openssl req -new -key /etc/csync2_ssl_key.pem -out /etc/csync2_ssl_cert.csr
openssl x509 -req -days 600 -in /etc/csync2_ssl_cert.csr -signkey /etc/csync 2_ssl_key.pem \
-out /etc/csync2_ssl_cert.pem
```
In case you've compiled csync from sources you may opt to just run `# make cert` while in the sources' directory, it will do everything for you.

<ol start ="5">
<li> Add IP and hostnames in the <code>hosts</code> file. In the hosts file example below <code>host-1</code> is called <code>idp1.gluu.org</code> and <code>host-2</code> is called <code>idp2.gluu.org</code></li>
</ol>
```
127.0.0.1       localhost
::1             ip6-localhost ip6-loopback
ff02::1         ip6-allnodes
ff02::2         ip6-allrouters
192.168.6.1     idp1.gluu.org
192.168.6.2     idp2.gluu.org  
```
<ol start ="6">
<li> Modify <code>csync2</code> in the <code>/etc/xinetd.d/</code> folder (some packages may reqire you to install it first; run <code># yum install xinetd</code>, followed by <code># chkconfig xinetd on</code></li>
</ol>

```
# default: off
# description: csync2
service csync2
{
        flags           = REUSE
        socket_type     = stream
        wait            = no
        user            = root
        group           = root
        server          = /usr/sbin/csync2
        server_args     = -i -N idp1.gluu.org
        port            = 30865
        type            = UNLISTED
        #log_on_failure += USERID
        disable         = no
        # only_from     = 192.168.199.3 192.168.199.4
}
```

<ol start ="7">
<li> Run the following commands</li>
</ol>
```
service xinetd restart
chkconfig xinetd on
```
!!! Note
    The status can be checked by running `chkconfig xinetd –list` and `iptables -L -nv | grep 30865`. For confirmation, telnet 30865 port from the VMs.

<ol start="8">
<li> Configure <code>csync2.cfg</code> to reflect the configuration below (Please note that csync2 doesn't allow to use symlinks in this file; you'll may need to correct full paths to certain directories as they may change in future Gluu's CE packages)</li>
</ol>
```
#nossl * *;
group cluster_group
{

        host idp1.gluu.org;
        host idp2.gluu.org;

        key /etc/csync2/csync2.key;
        include /etc/csync2/csync2.cfg;
        include /opt/idp/conf;
        include /opt/idp/metadata;
        include /opt/idp/ssl;
        include /opt/apache-tomcat-7.0.65/conf;

        exclude *~ .*;


        action
        {

                logfile "/var/log/csync2_action.log";
                do-local;
        }

        action
        {
                pattern /opt/apache-tomcat-7.0.65/conf/*;

                exec "/sbin/service tomcat restart";
                logfile "/var/log/csync2_action.log";
                do-local;
        }

        backup-directory /var/backups/csync2;
        backup-generations 3;

        auto younger;
} 
```
<ol start ="9">
<li> Start <code>csync2</code> by running <code>csync2 -cvvv -N idp2.gluu.org</code></li>
</ol>

<ol start ="10"> 
<li>Run `mkdir -p /var/backups/csync2`</li>
</ol>

<ol start ="11">
<li> Add cronjob to automate csync2 run. The cronjob example is given below:</li>
</ol>
```
1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,37,39,41,43,45,47,49,51,53,55,57,59 * * * *    /usr/sbin/csync2 -N idp1.gluu.org -xv 2>/var/log/csync2.log 
```

### Csync2 configuration for host-2

1. Log into Gluu-Server container

2. Please copy the private key generated on `host-1` to `host-2` and put it into `/etc/csync2/csync2.key` file 

3. Generate certificate/key pair that will be used to establish SSL protection layer for incoming connections by running next commands on `host-2` (location of the files and their names are hardcoded into executable). Don't fill any fields, just hit "Enter" accepting default values:
```
openssl genrsa -out /etc/csync2_ssl_key.pem 1024
openssl req -new -key /etc/csync2_ssl_key.pem -out /etc/csync2_ssl_cert.csr
openssl x509 -req -days 600 -in /etc/csync2_ssl_cert.csr -signkey /etc/csync2_ssl_key.pem \
-out /etc/csync2_ssl_cert.pem
```
In case you've compiled csync from sources you may opt to just run `# make cert` while in the sources' directory, it will do everything for you.

<ol start ="4">
<li>Add IP and hostnames in the <code>hosts</code> file. In the hosts file example below <code>host-1</code> is called <code>idp1.gluu.org</code> and <code>host-2</code> is called <code>idp2.gluu.org</code></li>
</ol>
```
127.0.0.1       localhost
::1             ip6-localhost ip6-loopback
ff02::1         ip6-allnodes
ff02::2         ip6-allrouters
192.168.6.1     idp1.gluu.org
192.168.6.2     idp2.gluu.org
```

<ol start ="5">
<li> Modify <code>csync2</code> in the <code>/etc/xinetd.d/</code> folder (some packages may reqire you to install it first; run <code># yum install xinetd</code>, then <code># chkconfig xinetd on</code>):</li>
</ol>
```
# default: off
# description: csync2
service csync2
{
        flags           = REUSE
        socket_type     = stream
        wait            = no
        user            = root
        group           = root
        server          = /usr/sbin/csync2
        server_args     = -i -N idp2.gluu.org
        port            = 30865
        type            = UNLISTED
        #log_on_failure += USERID
        disable         = no
        # only_from     = 192.168.199.3 192.168.199.4
}
```

<ol start ="6">
<li> Run the following commands</li>
</ol>
```
service xinetd restart
chkconfig xinetd on
```
**Note:** The status can be checked by running `chkconfig xinetd –list` and `iptables -L -nv | grep 30865`. For confirmation, telnet 30865 port from the VMs.

<ol start ="7">
<li> Configure `csync2.cfg` to reflect the configuration below (Please note that csync2 doesn't allow to use symlinks in this file; you'll may need to correct full paths to certain directories as they may change in future Gluu's CE packages):</li>
</ol>
```
#nossl * *;
group cluster_group
{

        host idp1.gluu.org;
        host idp2.gluu.org;

        key /etc/csync2/csync2.key;
        include /etc/csync2/csync2.cfg;
        include /opt/idp/conf;
        include /opt/idp/metadata;
        include /opt/idp/ssl;
        include /opt/apache-tomcat-7.0.65/conf;

        exclude *~ .*;


        action
        {

                logfile "/var/log/csync2_action.log";
                do-local;
        }

        action
        {
                pattern /opt/apache-tomcat-7.0.65/conf/*;

                exec "/sbin/service tomcat restart";
                logfile "/var/log/csync2_action.log";
                do-local;
        }

        backup-directory /var/backups/csync2;
        backup-generations 3;

        auto younger;
} 
```

<ol start ="8">
<li> Start <code>csync2</code> by running <code>csync2 -cvvv -N idp2.gluu.org</code></li>
</ol>

<ol start ="9"><li> Run <code>mkdir -p /var/backups/csync2</code></li></ol>

<ol start ="10">
<li> Add cronjob to automate csync2 run. The cronjob example is given below:</li></ol>
```
1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,37,39,41,43,45,47,49,51,53,55,57,59 * * * *    /usr/sbin/csync2 -N idp2.gluu.org -xv 2>/var/log/csync2.log 
```

## Certificate Management

The certificates do not vary in the manual cluster configuration. The certificates should be updated manually 
in each host, when required. Move to `/etc/certs/` on the 1st node (inside the container). Copy all keys, certs and key storages conforming to these masks: `httpd.*`, `asimba.*`, `asimbaIDP.*` and `shibIDP.*` to the same directory on the 2nd node (overwriting files that exist there; you may opt to backup them first, just in case).

After that's done you still will need to update default system storage (`cacerts` file) at the 2nd node with these newly copied certificates.

##[Optional] Actions in case setup.properties.last method of installation didn't work for you

In this case jks keystores you'll be moving to the 2nd node will be protected by passwords hardcoded into different configuration files on the 1st node, which are different from the similar passwords hardcoded into the same files on the 2nd node.

Thus you MUST ensure that the 1st node will be the one that will initialize the 2nd node during first csync's run (i.e., that it will win any conflicts due to changes in files that csync may detect during its very first run), as otherwise different components won't be able to decrypt these keystores and will fail.

To achieve this you should run initial sync manualy after completing configuring it, but before you install cron jobs:

1. Comment out `auto younger;` string in `csync2.cfg` on both nodes to disable autoresolution of conflicts

2. Run `# csync2 -crvvv -N idp1.gluu.org` on the 1st node

3. Run `# csync2 -crvvv -N idp2.gluu.org` on the 2nd node

4. Previous commands did initial scan and filled metadata database. Now run `# csync2 -xrvvv -N idp1.gluu.org` on the 1st node. That will try to sync files with the 2nd node, and most likely will fail to replicate all files due to some conflicts.

5. You should be now in a state of conflict, as certain files in directories to be synced differ between nodes and tool can't decide which to prefer. Run this `# csync2 -frvvv -N idp1.gluu.org /` on the 1st node to mark its files that still in dirty state as the ones that will win any conflict next time.

6. Run `# csync2 -xrvvv -N idp1.gluu.org` on the 1st node to complete your initial sync. Now all your 2nd node's directories covered by csync should be identical to the 1st node's.

7. Uncomment `auto younger;` string and proceed to installing cron jobs
