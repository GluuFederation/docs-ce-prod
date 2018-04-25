# Upgrade to Gluu Server 3.1.3

## Overview
The Gluu Server **cannot** be upgraded with a simple `apt-get upgrade`. You need to explicitly install the new version and export/import your data. Find your existing version below for upgrade instructions to Gluu Server 3.1.3. 

## Upgrade from 3.1.x to 3.1.3

Upgrading from 3.1.x to 3.1.3 involves the following steps:

- Stop oxTrust and oxAuth services

- Backup existing oxTrust and oxAuth .war files

- Download 3.1.3 oxTrust and oxAuth from repo

- Copy oxTrust and oxAuth .war in path

- Update Gluu schema files

- Start oxTrust and oxAuth services

### Updating .war and Schema Manually

To upgrade from 3.1.x to 3.1.3, you have to manually update your .war files as outlined below:

1. Log into chroot container:  

    `# service gluu-server-3.1.x login`
    
#### Update Identity .war

2. Stop the identity service:  

    `# service identity stop`
        
3. Navigate to the `/opt/gluu/jetty` directory and back up the current app in the 
root's home directory (just in case you need to restore!): 

    `# cd /opt/gluu/jetty/`
    
    `# tar -czf ~/identity.tar.gz identity`
    
4. Download and install the latest .war 

    `# cd /opt/gluu/jetty/identity/webapps/`
    
    `# rm identity.war`
    
    `# wget https://ox.gluu.org/maven/org/xdi/oxtrust-server/3.1.3.Final/oxtrust-server-3.1.3.Final.war -O identity.war`

6. Start the identity service  
    
    `# service identity start`
 
#### Update oxAuth .war

7. Stop oxAuth Service

    `# service oxauth stop`
    
8. Navigate to the `/opt/gluu/jetty` directory and back up the current app in the 
root's home directory (just in case you need to restore!): 

    `# cd /opt/gluu/jetty/`
    
    `# tar -czf ~/oxauth.tar.gz oxauth`
    
9. Download and install the latest WAR: 

    `# cd /opt/gluu/jetty/oxauth/webapps/`
    
    `# rm oxauth.war`
    
    `# wget https://ox.gluu.org/maven/org/xdi/oxauth-server/3.1.3.Final/oxauth-server-3.1.3.Final.war -O oxauth.war`
    
10. Start the oxAuth service

    `# service oxauth start`

#### Update Gluu Schema Files
    
  For the OpenLDAP to be able to accomodate new attributes added to some entries in 3.1.3, its schema files need to be updated. The recent schema files can be found [here](https://github.com/GluuFederation/community-edition-setup/tree/master/schema). Following the next step will upgrade the schema:

11. Navigate to `/opt/gluu/schema/openldap` directory 

    `# cd /opt/gluu/schema/openldap/`

12. Stop LDAP service

    `# service solserver stop`
    
13. Make a backup of the current schema files, which will be `gluu.schema`

    `# mv gluu.schema gluu.schema.old`
    
12. Download the schema files to `/opt/gluu/schema/openldap`

    `# wget https://raw.githubusercontent.com/GluuFederation/community-edition-setup/version_3.1.3/static/openldap/gluu.schema -O gluu.schema`

13. Start LDAP service
     
    `# service solserver start`

!!! Warning
    If the schema of your old instance was customized, such as through the addition of custom attributes and/or object classes, you'll need to resort to manual migration of your changes (if any) to the newest `gluu.schema` file.

!!! Note
    The above procedure can be utilized to update other components of Gluu CE server 3.1.3, mentioned below.

### Latest .war files

The latest release of .war files can be downloaded from locations provided below. Select the subdirectory corresponding to 
version of your package.

!!! Note
    Subdirectories marked as "-SNAPSHOT" are not safe for general public's use and should be avoided unless you were specifically 
    instructed by Gluu stuff to use one.

- [oxTrust](https://ox.gluu.org/maven/org/xdi/oxtrust-server/)
- [oxAuth](https://ox.gluu.org/maven/org/xdi/oxauth-server/)
- [Shibboleth IdP](https://ox.gluu.org/maven/org/xdi/oxshibbolethIdp/)
- [Asimba SAML proxy](https://ox.gluu.org/maven/org/asimba/asimba-wa/)
- [oxAuth RP](https://ox.gluu.org/maven/org/xdi/oxauth-rp/)

### Location of Gluu 3.1.3 Components

Gluu 3.1.x components which can be updated in this way inside the container can be found at the following locations:

- oxTrust: `/opt/gluu/jetty/identity/webapps/identity.war`
- oxAuth: `/opt/gluu/jetty/oxauth/webapps/oxauth.war`
- Shibboleth IdP: `/opt/gluu/jetty/idp/webapps/idp.war`
- Asimba SAML proxy: `/opt/gluu/jetty/asimba/webapps/asimba.war`
- oxAuth RP: `/opt/gluu/jetty/oxauth-rp/webapps/oxauth-rp.war`


## Upgrade from 3.0.x to 3.1.3

!!! Warning
    Before proceeding with an upgrade, make sure to [backup](../operation/backup.md) the Gluu container or LDAP LDIF before proceeding with the upgrade. 

Upgrading generally involves the following steps:

- Install new version

- Export the data from your current version

- Stop the current Gluu Server

- Start the new version of Gluu Server

- Import data into the new server

Gluu provides the necessary [scripts](https://github.com/GluuFederation/community-edition-setup/tree/master/static/scripts) to import and export data in and out of the servers.

### Export the Data from the Current Installation

```
# service gluu-server-3.0.x login

# cd

# wget https://raw.githubusercontent.com/GluuFederation/community-edition-setup/master/static/scripts/export3031.py

# wget -c https://raw.githubusercontent.com/GluuFederation/community-edition-setup/master/ldif.py
```

Install the `python-pip` package.

```
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

### Install the Latest Version of the Gluu Server

Stop the current version of the Gluu Server.

```
# service gluu-server-3.0.x stop
```

Review the [installation docs](../installation-guide/install.md) to install the Gluu Server using the package manager. Once the package manager has installed version `3.1.3`, then execute the following commands:

```
# cp -r /opt/gluu-server-3.0.x/root/backup_3031/ /opt/gluu-server-3.1.3/root/

# service gluu-server-3.1.3 start

# service gluu-server-3.1.3 login

# cd

# cp backup_3031/setup.properties /install/community-edition-setup/

# cd /install/community-edition-setup/

# ./setup.py
```

Enter the required information to complete the installation.

### Import your Old Data

Navigate to where you have the `backup_3031` folder (if the above commands were followed, it is in `/root/`) and execute the following commands to get the necessary scripts.

```
# cd

# wget -c https://raw.githubusercontent.com/GluuFederation/community-edition-setup/master/static/scripts/import3031.py

# wget https://raw.githubusercontent.com/GluuFederation/cluster-mgr/master/testing/ldifschema_utils.py
```

Install the `python-pip` package using your package manager.

```
# curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"

# python get-pip.py
```

Install the `json-merge` Python package and run the import script.

```
# pip install jsonmerge

# chmod +x import3031.py
```

Install python-ldap package. 
For Debian and Ubuntu:

```
# apt-get update

# apt-get install python-ldap

```

For CentOS and RHEL:

```
# yum install python-ldap

```

Now run import script:

```
# ./import3031.py backup_3031
```

!!! Note
    Import script will enable default admin user and will disable all custom authentcation scrpts. You should manually enable if you had configured one.
    After completion of import, stop/start gluu-server container one final time

Any errors or warnings will be displayed in the terminal and can be reviewed in the import log. Now you should be able to log into the oxTrust web UI using the old admin credentials and you should see all previous data in place. 

## Upgrade from 2.x.x to 3.1.3

!!! Warning
    Before proceeding with an upgrade, make sure to [backup](../operation/backup.md) the Gluu container or LDAP LDIF before proceeding with the upgrade. 

Upgrading generally involves the following steps:   

* Install the recent Gluu CE package
* Prepare the old Gluu Server instance for migration
* Export the data from your old instance
* Stop the old instance
* Start the new instance you installed
* Import data into the new server

Gluu provides the necessary [scripts](https://github.com/GluuFederation/community-edition-setup/tree/master/static/scripts) to import and export data in and out of the servers.

### Prepare your Old Instance

!!! Note
    The following steps are only mandatory if you are using a custom authentication script as one of your default authentication methods. The upgrade scripts support migration of the basic authentication settings configured in the "Manage LDAP Authentication" tab, including use cases where a remote LDAP server is used to authenticate user credentials. During the import phase of the upgrade, you will be prompted to import and apply your old LDAP settings from the previous instance. If you are using both LDAP authentication and custom scripts, disable your scripts as explained in steps 4-5 below, and make sure one of users you import from your LDAP backend can still log in and has administrator's level of access
    
Scripts cover most of tedious tasks of migrating your settings, but certain transitions are too tricky to automate and still need to be handled manually.

Architectural differences are significant between 2.x and 3.x packages. Among other compatibility issues is the fact that custom authentication scripts written for 2.x most likely will fail to initialize in 3.x instances. This becomes a problem if your old setup is using such script to authenticate administrator users accessing oxTrust web UI - in such case after migration you risk getting locked out from the easiest way to manage your instance, and will have to resort to directly changing settings in LDAP.

To prevent this, we recommend to temporarily reset your authentication methods to the most basic mode available - authentication against internal LDAP server. Please follow next steps to ensure you'll be able to acess web UI after the migration is done:

1. If "Cache Refresh" is used in your old instance, please proceed to "Configuration" > "Cache Refresh" page and disable it. Also make sure "Keep external persons" checkbox is set there (these changes can be reverted after migration is done, they are simply to prevent the user that will be added next to be removed by CR)
1. Move to "Users" > "Manage People" page and click "Add person" button. Create a new temporary administrator user providing basic set of mandatory attributes it requirese (don't forget to set a password for it)
1. Move to "Users" > "Manage People" and add the new user to "Gluu Manager Group" group
1. Move to "Configuration" > "Manage Authentication" > "Default Authentication Method" and make sure both settings there are set to "Default" (they must not contain the name of your (or any other) script)
1. Move to "Configuration" > "Manage Custom Scripts" > "Person Authentication" and make sure that for **all** scripts there "Enabled" checkbox is not checked
1. Don't log out from your current session which you used to apply recent changes so that you'll be able to revert them if something goes wrong. In a **separate** browser application (i.e. not in the different tab of the same browser you've been using so far) try to access old instance's web UI as the new admin user you've just created, to make sure it has full access to its controls
1. Log out from both your sessions and procceed with exporting your data (see the next chapter)

After migration is done you should be able to log in as the temporary admin user you created. After resolving compatibility issues with your custom scripts (in case you're using one of our standard scripts, you can simply fetch the most recent source for it from [the repos](https://github.com/GluuFederation/oxAuth/tree/master/Server/integrations); if your script is written from scratch or is a some modified verson of the standard one, you may need to manually resolve any conflicts; please see [this doc](https://github.com/GluuFederation/oxAuth/blob/master/Server/integrations/Migration_stepts_to_3.1.x.txt) for useful hints) and restoring your regular setup, you can remove the temporary user entry from "Managers" group and delete/disable it.

### Export the Data from the Current Installation

```
# service gluu-server-2.x.x login

# cd

# wget https://raw.githubusercontent.com/GluuFederation/community-edition-setup/master/static/scripts/export2431.py

# wget -c https://raw.githubusercontent.com/GluuFederation/community-edition-setup/master/ldif.py

```

Install the `python-pip` package.

```
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

### Install the Latest Version of the Gluu Server

Stop the current version of the Gluu Server.

```
# service gluu-server-2.4.x stop
```

Review the [installation docs](../installation-guide/install.md) to install the Gluu Server using the package manager. Once the package manager has installed version `3.1.3`, then follow next steps to prepare :

```
# cp -r /opt/gluu-server-2.4.x/root/backup_2431/ /opt/gluu-server-3.1.3/root/

# service gluu-server-3.1.3 start

# service gluu-server-3.1.3 login

# cd

# cp backup_2431/setup.properties /install/community-edition-setup/

# cd /install/community-edition-setup/

# ./setup.py
```
Enter the required information to complete the installation.

### Import your Old Data

Navigate to where you have the `backup_2431` folder (if the above commands were followed, it is in `/root/`) and execute the following commands to get the necessary scripts.

```
# cd

# wget -c https://raw.githubusercontent.com/GluuFederation/community-edition-setup/master/static/scripts/export2431.py

# wget https://raw.githubusercontent.com/GluuFederation/cluster-mgr/master/testing/ldifschema_utils.py
```

Install the `python-pip` package.

```
# curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"

# python get-pip.py
```

Install the `json-merge` Python package and run the import script.

```
# pip install jsonmerge

# python import2431.py backup_2431
```

You'll be asked whether or not you want to import your LDAP server settings from the old instance (the ones specified on "Manage Authentication" > "Manage LDAP Authentication" page/tab). If authentication against some remote backend LDAP server was used in the old instance and you expect to be able to log in with your old credentials after import is done, choose `[1]("yes")`. Choosing `[2]("no")` will keep default settings of the new instance (will verify user's credentials against Gluu's internal LDAP server).


!!! Note
    Import script will enable default admin user and will disable all custom authentcation scrpts. You should manually enable if you had configured one.
    After completion of import, stop/start gluu-server container one final time.

Any errors or warnings will be displayed in the terminal and can be reviewed in the import log. 
Now you should be able to log into the oxTrust web UI using the old admin credentials and 
you should see all previous data in place. 
