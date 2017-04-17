# Upgrading Gluu Server CE
## Overview
Gluu Server cannot be upgraded with simple `apt-get upgrade`. The admin needs to explicitly install the new version of the Gluu Server and export and import the required data using scripts. 

!!! Warning
    Make sure to [backup](../operation/backup.md/) the Gluu container or LDAP Ldif before proceeding with the upgrade. 

Upgrading generally involves the following steps:   

* Install new version
* Export the data from your current version
* Stop the current Gluu Server
* Start the new version of Gluu Server
* Import data into the new server

Gluu provides the necessary [scripts](https://github.com/GluuFederation/community-edition-setup/tree/master/static/scripts) to import and export data in and out of the servers.

> NOTE: In this documentation, we assume the existing installed Gluu Server version is 2.x.x. 

## Export the data from the current installation

```
# service gluu-server-2.x.x login

# wget https://raw.githubusercontent.com/GluuFederation/community-edition-setup/master/static/scripts/export24.py

# chmod +x export24.py

# ./export24.py
```

The export script will generate a directory called `backup_24` which will have all the data from the current installation. Check the log file generated in the directory for any errors.

## Install the latest version of the Gluu server

Stop the current version of the gluu-server.

```
# service gluu-server-2.4.x stop
```

Review the [installation docs](../installation-guide/install.md) to install the Gluu Server using the package manager. Once the package manager has installed version `3.0.0`, then execute the following commands:

```
# cp -r /opt/gluu-server-2.4.x/root/backup_24/ /opt/gluu-server-3.0.0/root/

# service gluu-server-3.0.0 start

# service gluu-server-3.0.0 login

# cp backup_24/setup.properties /install/community-edition-setup/

# cd /install/community-edition-setup/

# ./setup.py
```

Enter the required information to complete the installation.

## Import your old data

Navigate to where you have the `backup_24` folder (if the above commands were followed, it is in `/root/`) and execute the following commands to get the necessary scripts.

```

# wget -c https://raw.githubusercontent.com/GluuFederation/community-edition-setup/master/static/scripts/import30.py

# wget -c https://raw.githubusercontent.com/GluuFederation/community-edition-setup/master/ldif.py
```

Install the `python-pip` package using your package manager.

```
# apt-get update
# apt-get install python-pip

or

# yum -y install python-pip
```

Install the `json-merge` Python package and run the import script.

```
# pip install jsonmerge

# chmod +x import30.py

# ./import30.py backup_24
```

Any errors or warnings will be displayed in the terminal and can be reviewed in the import log. Now you should be able to log into the oxTrust web UI using the old admin credentials. You should see all previous data in place. After completion of import, stop/start 2.4.4 container one final time. 
