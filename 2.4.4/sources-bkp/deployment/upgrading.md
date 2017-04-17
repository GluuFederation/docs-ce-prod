# Upgrading Gluu Server CE

Upgrading a Gluu Server is NOT a simple `apt-get upgrade`. The admin needs to explicitly install the version of the Gluu Server. It generally involves the following steps:

!!! Warning
    As a precautionary measure, Please make sure to back up the Gluu container or LDAP Ldif before proceeding to upgrading.

* Install new version
* Export the data from your current version
* Stop the current Gluu Server
* Start the new version of Gluu Server
* Import data into the new server

Gluu provides the necessary [scripts](https://github.com/GluuFederation/community-edition-setup/tree/master/static/scripts) to perform the import and export of the data in and out of the servers.

> NOTE: In this documentation, '2.4.x' is referred to existing installed version of Gluu CE Server. 

## Export the data from the current installation

```
# service gluu-server-2.4.x login

# wget https://raw.githubusercontent.com/GluuFederation/community-edition-setup/master/static/scripts/export24.py

# chmod +x export24.py

# ./export24.py
```

The export script will generate a directory called `backup_24` which will have all the data backed up from the current installation.
Check the log file generated in the directory for any errors.

## Install the latest version of the Gluu server

Stop the current version of the gluu-server.

```
# service gluu-server-2.4.x stop
```

Consult the [docs](https://www.gluu.org/docs/deployment/) of the respective distribution about how to install the Gluu Server using the package manager.
Once the package manager has installed the version `2.4.y`, then:

```
# cp -r /opt/gluu-server-2.4.x/root/backup_24/ /opt/gluu-server-2.4.y/root/

# service gluu-server-2.4.y start

# service gluu-server-2.4.y login

# cp backup_24/setup.properties /install/community-edition-setup/

# cd /install/community-edition-setup/

# ./setup.py
```

Enter the required information for the setup and complete the installation.

## Import your old data

Go to the folder where you have the `backup_24` folder (if the above commands were followed, it is in /root/) and  get the necessary scripts.

```

# wget -c https://raw.githubusercontent.com/GluuFederation/community-edition-setup/master/static/scripts/import244.py

# wget -c https://raw.githubusercontent.com/GluuFederation/community-edition-setup/master/ldif.py
```

Install the `python-pip` package using your package manager.

```
# apt-get install python-pip

or

# yum -y install python-pip
```

Install the `json-merge` Python package and run the import script.

```
# pip install jsonmerge

# chmod +x import244.py

# ./import244.py backup_24
```

Any error or warning will be displayed in the terminal or can be seen in the import log generated. Now the admin should be able to log into the oxTrust web-UI with the old admin credentials and see all previous data in place. After the completion of import, stop/start 2.4.4 container one more time. 
