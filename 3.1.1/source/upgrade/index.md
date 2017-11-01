# Upgrade to Gluu Server 3.1.1

## Overview
The Gluu Server can **not** be upgraded with a simple `apt-get upgrade`. You need to explicitly install the new version and export/import your data. Find your existing version below for upgrade instructions to Gluu Server 3.1.1. 

## Upgrade from 3.1.0 to 3.1.1

Upgrading from 3.1.0 to 3.1.1 involves the following steps:

- Stop oxTrust and oxAuth services

- Backup existing oxTrust and oxAuth .war files

- Download 3.1.1 oxTrust and oxAuth from repo

- Copy oxTrust and oxAuth .war in path

- Update Gluu schema files

- Start oxTrust and oxAuth services

### Updating .war and schema manually

To upgrade from 3.1.0 to 3.1.1, you have to manually update your .war files as outlined below:

1. Login to chroot container:  

    `# service gluu-server-3.1.1 login`
    
#### Update Identity .war

2. Stop the identity service:  

    `# service identity stop`
        
3. Navigate to the `/opt/gluu/jetty` directory and backup the current app in the 
root's home directory (just in case you need to restore!): 

    `# cd /opt/gluu/jetty/`
    
    `# tar -czf ~/identity.tar.gz identity`
    
4. Download and install the latest .war 

    `# cd /opt/gluu/jetty/identity/webapps/`
    
    `# rm identity.war`
    
    `# wget https://ox.gluu.org/maven/org/xdi/oxtrust-server/3.1.1.Final/oxtrust-server-3.1.1.Final.war -O identity.war`

6. Start the identity service  
    
    `# service identity start`
 
#### Update oxAuth .war

7. Stop oxAuth Service

    `# service oxauth stop`
    
8. Navigate to the `/opt/gluu/jetty` directory and back up the current app in the 
root's home directory (just in case you need to restore!): 

    `# cd /opt/gluu/jetty/`
    
    `# tar -czf ~/oxauth.tar.gz oxauth`
    
9. Download and install the latest WAR (assuming the URL was in the $WAR_URL environment variable): 

    `# cd /opt/gluu/jetty/oxauth/webapps/`
    
    `# rm oxauth.war`
    
    `# wget https://ox.gluu.org/maven/org/xdi/oxauth-server/3.1.1.Final/oxauth-server-3.1.1.Final.war -O oxauth.war`
    
10. Start the oxAuth service

    `# service oxauth start`

#### Update Gluu Schema Files
    
    To upgrade gluu server 3.1.0 to 3.1.1, Gluu schema files needs to be updated. 
    Gluu Schema files can be found [here](https://github.com/GluuFederation/community-edition-setup/tree/master/schema) to update.

11. Navigate to `/opt/gluu/schema/openldap` directory 

    `# cd /opt/gluu/schema/openldap/`

12. Stop LDAP service.

    `# Service solserver stop`
    
13. Take a back up of the current schema files, which will be `gluu.schema`.

    `# mv gluu.schema gluu.schema.old`
    
12. Download the Schema files to `/opt/gluu/schema/openldap`

    `#wget https://raw.githubusercontent.com/GluuFederation/community-edition-setup/version_3.1.1/static/openldap/gluu.schema -O gluu.schema`

13. Start LDAP service.
     
    `# service solserver start`

!!!Warning
    If you are using a customized schema, make sure not to change `gluu.schema`.

!!! Note
    Above procedure can be utilized to update other components of Gluu CE server 3.1.1, mentioned below.

### Latest .war files

The latest release of .war files can be downloaded from the following locations:

- [oxTrust](https://ox.gluu.org/maven/org/xdi/oxtrust-server/)
- [oxAuth](https://ox.gluu.org/maven/org/xdi/oxauth-server/)
- [Shibboleth IdP](https://ox.gluu.org/maven/org/xdi/oxshibbolethIdp/)
- [Asimba SAML proxy](https://ox.gluu.org/maven/org/asimba/asimba-wa/)
- [oxAuth RP](https://ox.gluu.org/maven/org/xdi/oxauth-rp/)

### Location of Gluu 3.1.1 Components

Gluu 3.1.x components which can be updated in this way inside the container can be found at the following locations:

- oxTrust: `/opt/gluu/jetty/identity/webapps/identity.war`
- oxAuth: `/opt/gluu/jetty/oxauth/webapps/oxauth.war`
- Shibboleth IdP: `/opt/gluu/jetty/idp/webapps/idp.war`
- Asimba SAML proxy: `/opt/gluu/jetty/asimba/webapps/asimba.war`
- oxAuth RP: `/opt/gluu/jetty/oxauth-rp/webapps/oxauth-rp.war`


## Upgrade from 3.0.x to 3.1.1

!!! Warning
    Before proceeding with an upgrade, make sure to [backup](../operation/backup.md) the Gluu container or LDAP Ldif before proceeding with the upgrade. 

Upgrading generally involves the following steps:

- Install new version

- Export the data from your current version

- Stop the current Gluu Server

- Start the new version of Gluu Server

- Import data into the new server

Gluu provides the necessary [scripts](https://github.com/GluuFederation/community-edition-setup/tree/master/static/scripts) to import and export data in and out of the servers.

### Export the data from the current installation

```
# service gluu-server-3.0.x login

# wget https://raw.githubusercontent.com/GluuFederation/community-edition-setup/master/static/scripts/export3031.py

# wget -c https://raw.githubusercontent.com/GluuFederation/community-edition-setup/master/ldif.py

```

Install the `python-pip` package using your package manager.

```
# apt-get update
# apt-get install python-pip

or

# yum -y install python-pip

or, for CentOS/RHEL 7x series

# curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
# python get-pip.py
```

Install the `json-merge` Python package and run the import script.

```
# pip install jsonmerge

# chmod +x export3031.py

# ./export3031.py
```

The export script will generate a directory called `backup_3031` which will have all the data from the current installation. Check the log file generated in the directory for any errors.

### Install the latest version of the Gluu server

Stop the current version of the gluu-server.

```
# service gluu-server-3.0.x stop
```

Review the [installation docs](../installation-guide/install.md) to install the Gluu Server using the package manager. Once the package manager has installed version `3.0.2`, then execute the following commands:

```
# cp -r /opt/gluu-server-3.0.x/root/backup_3031/ /opt/gluu-server-3.1.0/root/

# service gluu-server-3.1.1 start

# service gluu-server-3.1.1 login

# cp backup_3031/setup.properties /install/community-edition-setup/

# cd /install/community-edition-setup/

# ./setup.py
```

Enter the required information to complete the installation.

### Import your old data

Navigate to where you have the `backup_3031` folder (if the above commands were followed, it is in `/root/`) and execute the following commands to get the necessary scripts.

```

# wget -c https://raw.githubusercontent.com/GluuFederation/community-edition-setup/master/static/scripts/import3031.py

# wget -c https://raw.githubusercontent.com/GluuFederation/community-edition-setup/master/ldif.py
```

Install the `python-pip` package using your package manager.

```
# apt-get update
# apt-get install python-pip

or

# yum -y install python-pip

or, for CentOS/RHEL 7x series

# curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
# python get-pip.py
```

Install the `json-merge` Python package and run the import script.

```
# pip install jsonmerge

# chmod +x import3031.py

# ./import3031.py backup_3031
```

!!! Note
    After completion of import, stop/start gluu-server container one final time

Any errors or warnings will be displayed in the terminal and can be reviewed in the import log. Now you should be able to log into the oxTrust web UI using the old admin credentials and you should see all previous data in place. 

## Upgrade from 2.x.x to 3.1.1

!!! Note
    This guide assumes that you are upgrading from version 2.x.x to 3.1.1 and are **OK with changing persistence from OpenDJ to OpenLDAP**. If you prefer to keep OpenDJ in Gluu Server 3.x, follow the separate documentation for [upgrading with OpenDJ](../upgrade/manual-update.md).

!!! Warning
    Before proceeding with an upgrade, make sure to [backup](../operation/backup.md) the Gluu container or LDAP Ldif before proceeding with the upgrade. 

Upgrading generally involves the following steps:   

* Install new version
* Export the data from your current version
* Stop the current Gluu Server
* Start the new version of Gluu Server
* Import data into the new server

Gluu provides the necessary [scripts](https://github.com/GluuFederation/community-edition-setup/tree/master/static/scripts) to import and export data in and out of the servers.

### Export the data from the current installation

```
# service gluu-server-2.x.x login

# wget https://raw.githubusercontent.com/GluuFederation/community-edition-setup/master/static/scripts/export2431.py

# wget -c https://raw.githubusercontent.com/GluuFederation/community-edition-setup/master/ldif.py

```

Install the `python-pip` package using your package manager.

```
# apt-get update
# apt-get install python-pip

or

# yum -y install python-pip

or, for CentOS/RHEL 7x series

# curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
# python get-pip.py
```

Install the `json-merge` Python package and run the import script.

```
# pip install jsonmerge

# chmod +x export2431.py

# python export2431.py
```

The export script will generate a directory called `backup_2431` which will have all the data from the current installation. Check the log file generated in the directory for any errors.

### Install the latest version of the Gluu server

Stop the current version of the gluu-server.

```
# service gluu-server-2.4.x stop
```

Review the [installation docs](../installation-guide/install.md) to install the Gluu Server using the package manager. Once the package manager has installed version `3.1.1`, then execute the following commands:

```
# cp -r /opt/gluu-server-2.4.x/root/backup_2431/ /opt/gluu-server-3.1.1/root/

# service gluu-server-3.1.1 start

# service gluu-server-3.1.1 login

# cp backup_2431/setup.properties /install/community-edition-setup/

# cd /install/community-edition-setup/

# ./setup.py
```

Enter the required information to complete the installation.

### Import your old data

Navigate to where you have the `backup_2431` folder (if the above commands were followed, it is in `/root/`) and execute the following commands to get the necessary scripts.

```

# wget -c https://raw.githubusercontent.com/GluuFederation/community-edition-setup/master/static/scripts/import2431.py

# wget -c https://raw.githubusercontent.com/GluuFederation/community-edition-setup/master/ldif.py
```

Install the `python-pip` package using your package manager.

```
# apt-get update
# apt-get install python-pip

or

# yum -y install python-pip

or, for CentOS/RHEL 7x series

# curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
# python get-pip.py
```

Install the `json-merge` Python package and run the import script.

```
# pip install jsonmerge

# chmod +x import2431.py

# ./import2431.py backup_2431
```

!!! Note
    After completion of import, stop/start gluu-server container one final time

Any errors or warnings will be displayed in the terminal and can be reviewed in the import log. 
Now you should be able to log into the oxTrust web UI using the old admin credentials and 
you should see all previous data in place. 
