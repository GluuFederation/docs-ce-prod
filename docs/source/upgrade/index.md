# Upgrade to Gluu Server 3.1.5

## Overview
The Gluu Server **cannot** be upgraded with a simple `apt-get upgrade`. You will need to either use our in-place upgrade script or explicitly install the new version and export/import your data. Find your existing version below for upgrade instructions to Gluu Server 3.1.5. 

### Pre-requisites

- Before upgrading, make sure to [back up](../operation/backup.md) the Gluu container or LDAP LDIF. 
- Upgrades should always be thoroughly scoped and tested on a development environment *first*.

## Upgrade from 3.1.x to 3.1.5

To perform an in place upgrade to Gluu Server 3.1.5, download and run our in-place upgrade script following these instructions:

1. Log into your server with `service gluu-server-3.1.x login`

1. Download the upgrade script with `wget https://repo.gluu.org/upd/3-1-5-upg.sh`

1. Run the script with `sh 3-1-5-upg.sh`

1. When the script has finished, restart your server:

```
logout
service gluu-server-3.1.x restart
```

!!! Note
    Scripts and directories outside the Chroot will still reflect the version from which you upgraded. For example, if you started with version 3.1.3, the directory will still be gluu-server-3.1.3 even after upgrading to 3.1.5.

## Upgrade from 3.0.x to 3.1.5


Upgrading generally involves the following steps:

- Install the new version

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

# wget -c https://raw.githubusercontent.com/GluuFederation/community-edition-setup/version_3.1.6/ldif.py
```

Install the `python-pip` package.

```
# curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"

# python get-pip.py
```

Install the `json-merge` Python package and run the import script.

```
# pip install jsonmerge

# python export3031.py
```

!!! Note
    Choose OpenLDAP if your current LDAP Server is OpenLDAP when you are asked to choose a target LDAP Server.

The export script will generate a directory called `backup_3031` which will have all the data from the current installation. Check the log file generated in the directory for any errors.

### Install the Latest Version of the Gluu Server

Stop the current version of the Gluu Server.

```
# service gluu-server-3.0.x stop
```

Review the [installation docs](../installation-guide/install.md) to install the Gluu Server using the package manager. Once the package manager has installed version `3.1.5`, execute the following commands:

```
# cp -r /opt/gluu-server-3.0.x/root/backup_3031/ /opt/gluu-server-3.1.5/root/

# service gluu-server-3.1.5 start

# service gluu-server-3.1.5 login

# cd

# cp backup_3031/setup.properties /install/community-edition-setup/

# cd /install/community-edition-setup/

# ./setup.py
```

Enter the required information to complete the installation.

### Import your Old Data

Navigate to where you have the `backup_3031` folder (if the above commands were followed, it is in `/root/`) and execute the following commands to get the necessary scripts:

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
```

Install the python-ldap package. 
For Debian and Ubuntu:

```
# apt-get update

# apt-get install python-ldap
```

For CentOS and RHEL:

```
# yum install python-ldap
```

Now run the import script:

```
# python import3031.py backup_3031
```

!!! Note
    The import script will enable the default admin user and will disable all custom authentication scripts. You should manually enable them if any were configured.
    
    After completion of import, stop/start gluu-server container one final time.

Any errors or warnings will be displayed in the terminal and can be reviewed in the import log. Now you should be able to log into the oxTrust web UI using the old admin credentials and you should see all previous data in place. 

## Upgrade from 2.x.x to 3.1.5

!!! Warning
    Before proceeding with an upgrade, make sure to [back up](../operation/backup.md) the Gluu container or LDAP LDIF before proceeding with the upgrade. 

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

Architectural differences are significant between 2.x and 3.x packages. Among other compatibility issues, custom authentication scripts written for 2.x most likely will fail to initialize in 3.x instances. This becomes a problem if your old setup is using such a script to authenticate admin users accessing oxTrust web UI - in such case after migration you risk getting locked out from the easiest way to manage your instance, and will have to resort to directly changing settings in LDAP.

To prevent this, we recommend to temporarily reset your authentication methods to the most basic mode available - authentication against the internal LDAP server. Please follow next steps to ensure you'll be able to access the web UI after the migration is done:

1. If "Cache Refresh" is used in your old instance, navigate to "Configuration" > "Cache Refresh" and disable it. Also make sure "Keep external persons" checkbox is set there (these changes can be reverted after migration is done, they are simply to prevent the user that will be added next to be removed by CR)
1. Move to "Users" > "Manage People" and click "Add person" button. Create a new temporary admin user providing a basic set of mandatory attributes (don't forget to set a password for it)
1. Move to "Users" > "Manage People" and add the new user to "Gluu Manager Group" group
1. Move to "Configuration" > "Manage Authentication" > "Default Authentication Method" and make sure both settings there are set to "Default" (they must not contain the name of your (or any other) script)
1. Move to "Configuration" > "Manage Custom Scripts" > "Person Authentication" and make sure that for **all** scripts there "Enabled" checkbox is not checked
1. Don't log out from your current session which you used to apply recent changes so that you'll be able to revert them if something goes wrong. In a **separate** browser application (i.e. not in the different tab of the same browser you've been using so far) try to access old instance's web UI as the new admin user you've just created, to make sure it has full access to its controls
1. Log out from both your sessions and procceed with exporting your data (see the next chapter)

After migration is done you should be able to log in as the temporary admin user you created. After resolving compatibility issues with your custom scripts (in case you're using one of our standard scripts, you can simply fetch the most recent source for it from [the repos](https://github.com/GluuFederation/oxAuth/tree/master/Server/integrations); if your script is written from scratch or is a modified verson of the standard one, you may need to manually resolve any conflicts; please see [this doc](https://github.com/GluuFederation/oxAuth/blob/master/Server/integrations/Migration_stepts_to_3.1.x.txt) for useful hints) and when you restore your regular setup, you can remove the temporary user entry from "Managers" group and delete/disable it.

### Export the Data from the Current Installation

```
# service gluu-server-2.x.x login

# cd

# wget https://raw.githubusercontent.com/GluuFederation/community-edition-setup/master/static/scripts/export2431.py

# wget -c https://raw.githubusercontent.com/GluuFederation/community-edition-setup/version_3.1.6/ldif.py

```

Install the `python-pip` package.

```
# curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"

# python get-pip.py
```

Install the `json-merge` Python package and run the import script.

```
# pip install jsonmerge

# python export2431.py
```

The export script will generate a directory called `backup_2431` which will have all the data from the current installation. Check the log file generated in the directory for any errors.

### Install the Latest Version of the Gluu Server

Stop the current version of the Gluu Server.

```
# service gluu-server-2.4.x stop
```

Review the [installation docs](../installation-guide/install.md) to install the Gluu Server using the package manager. Once the package manager has installed version `3.1.5`, then follow the next steps to prepare :

```
# cp -r /opt/gluu-server-2.4.x/root/backup_2431/ /opt/gluu-server-3.1.5/root/

# service gluu-server-3.1.5 start

# service gluu-server-3.1.5 login

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

# wget -c https://raw.githubusercontent.com/GluuFederation/community-edition-setup/master/static/scripts/import2431.py

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

You'll be asked whether you want to import your LDAP server settings from the old instance (the ones specified on the "Manage Authentication" > "Manage LDAP Authentication" page/tab). If authentication against some remote backend LDAP server was used in the old instance and you expect to be able to log in with your old credentials after import is done, choose `[1]("yes")`. Choosing `[2]("no")` will keep default settings of the new instance (will verify user's credentials against Gluu's internal LDAP server).


!!! Note
    The import script will enable a default admin user and will disable all custom authentication scripts. You should manually enable them if previously configured.
    After import is finished, stop/start the gluu-server container one final time.

Any errors or warnings will be displayed in the terminal and can be reviewed in the import log. 
Now you should be able to log into the oxTrust web UI using the old admin credentials and 
you should see all previous data in place. 
