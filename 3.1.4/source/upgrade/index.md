# Upgrade to Gluu Server 3.1.4

## Overview
The Gluu Server **cannot** be upgraded with a simple `apt-get upgrade`. You will need to either use our in-place upgrade script or explicitly install the new version and export/import your data. Find your existing version below for upgrade instructions to Gluu Server 3.1.4. 

!!! Warning
    Before upgrading, make sure to [back up](../operation/backup.md) the Gluu container or LDAP LDIF. 

## Upgrade from 3.1.x to 3.1.4

New to version 3.1.4, it is now possible to perform an in-place upgrade from 3.1.x to 3.1.4, rather than requiring manual configuration. To do so, follow these directions to download and run our new in-place upgrade script:

1. Log into your server with `service gluu-server-3.1.x login`

1. Download the upgrade script with `wget http://c1.gluu.org:8999/3-1-4-sp1.sh`

1. Run the script with `sh 3-1-4-sp1.sh`

1. When the script has finished, restart your server:

```
logout
service gluu-server-3.1.x restart
```

!!! Note:
    Scripts and directories outside the Chroot will still reflect the version from which you upgraded. For example, if you started with version 3.1.3, the directory will still be gluu-server-3.1.3 even after upgrading to 3.1.4.

### Updating .war and Schema Manually

To upgrade from 3.1.x to 3.1.4, you have to manually update your .war files as outlined below:

1. Log into chroot container:  

    `# service gluu-server-3.1.x login`

### Update Jetty

1. Create all the necessary directories for the upgrade.

    `# mkdir -p /opt/jetty-9.4/`  
    `# mkdir -p /opt/jetty-9.4/temp`  
    `# chown jetty:jetty -R /opt/jetty-9.4/*`  
   
1. Download and extract the Jetty .tgz from eclipse to /opt/jetty-9.4/:
 
    `# wget http://central.maven.org/maven2/org/eclipse/jetty/jetty-distribution/9.4.9.v20180320/jetty-distribution-9.4.9.v20180320.tar.gz \`  
    `-O /opt/jetty-9.4/jetty-distribution-9.4.9.v20180320.tar.gz`  
    `# tar -xvf /opt/jetty-9.4/jetty-distribution-9.4.9.v20180320.tar.gz -C /opt/jetty-9.4/`  
    `# rm /opt/jetty-9.4/jetty-distribution-9.4.9.v20180320.tar.gz`
   
1. Unlink the jetty-9.3 directory and link jetty-9.4 to jetty

    ```
    # unlink /opt/jetty
    # ln -sf /opt/jetty-9.4/jetty-distribution-9.4.9.v20180320 /opt/jetty
    # chown -h jetty:jetty /opt/jetty
    ```
1. Now change the `/etc/default/<service>` files `TMPDIR` from:

    `TMPDIR=/opt/jetty-9.3/temp`  
   
    To:  

    `TMPDIR=/opt/jetty-9.4/temp`  
 
1. Last we need to make a minor adjustment to the initialization process in `/opt/gluu/jetty/<service>/start.ini`:

    `# Module: logging`  
    `--module=logging`
  
    Becomes:

    `# Module: logging`  
    `--module=console-capture`
  
#### Update oxAuth .war

1. Stop oxAuth Service:

    `# service oxauth stop`
    
1. Navigate to the `/opt/gluu/jetty` directory and back up the current app in the root's home directory (just in case you need to restore it later): 

    `# cd /opt/gluu/jetty/`
    
    `# tar -czf ~/oxauth.tar.gz oxauth`
    
1. Download and install the latest WAR: 

    `# cd /opt/gluu/jetty/oxauth/webapps/`
    
    `# rm oxauth.war`
    
    `# wget https://ox.gluu.org/maven/org/xdi/oxauth-server/3.1.4.Final/oxauth-server-3.1.4.Final.war -O oxauth.war`
    
1. Start the oxAuth service:

    `# service oxauth start`
    
#### Update Identity .war

1. Stop the identity service:  

    `# service identity stop`
        
1. Navigate to the `/opt/gluu/jetty` directory and back up the current app in the root's home directory (just in case you need to restore it later): 

    `# cd /opt/gluu/jetty/`
    
    `# tar -czf ~/identity.tar.gz identity`
    
1. Download and install the latest .war: 

    `# cd /opt/gluu/jetty/identity/webapps/`
    
    `# rm identity.war`
    
    `# wget https://ox.gluu.org/maven/org/xdi/oxtrust-server/3.1.4.Final/oxtrust-server-3.1.4.Final.war -O identity.war`

1. Start the identity service:  
    
    `# service identity start`
    
#### Update Gluu Schema Files

You will need to upgrade schema files to accommodate for new attributes added to some entries in Gluu 3.1.4. Follow the instructions below for OpenDJ or OpenLDAP, depending on which LDAP server you have installed with your Gluu Server. If upgrading from 2.x, follow the OpenDJ instructions below. 

##### OpenDJ

1. Navigate to the `/opt/opendj/config/schema/` directory

   `# cd /opt/opendj/config/schema/`

1. Stop LDAP service:

    `# service opendj stop`

1. Make a backup of the current schema files, which will be `gluu.schema`:

    `# mv 101-ox.ldif 101-ox.ldif.old`

1. Download the schema files to `/opt/opendj/config/schema/`:

    `# wget https://raw.githubusercontent.com/GluuFederation/community-edition-setup/version_3.1.4/static/opendj/101-ox.ldif -O 101-ox.ldif`
    
    `# chown ldap:ldap 101-ox.ldif`

1. Start LDAP service:
     
    `# service opendj start`

##### OpenLDAP

The latest schema files can be found [here](https://github.com/GluuFederation/community-edition-setup/tree/master/schema). Following the next step will upgrade the schema:

1. Navigate to the `/opt/gluu/schema/openldap` directory 

    `# cd /opt/gluu/schema/openldap/`

1. Stop LDAP service:

    `# service solserver stop`
    
1. Make a backup of the current schema files, which will be `gluu.schema`:

    `# mv gluu.schema gluu.schema.old`
    
1. Download the schema files to `/opt/gluu/schema/openldap`:

    `# wget https://raw.githubusercontent.com/GluuFederation/community-edition-setup/version_3.1.4/static/openldap/gluu.schema -O gluu.schema`

1. Start LDAP service:
     
    `# service solserver start`

!!! Warning
    If the schema of your old instance was customized, such as through the addition of custom attributes and/or object classes, you'll need to manually migrate your changes (if any) to the newest `gluu.schema` file.

!!! Note
    The above procedure can be utilized to update other components of Gluu CE server 3.1.4, mentioned below.

### Update Passport.js installation.

#### Upgrading from 3.1.3 to 3.1.4

1. Ensure you have updated the [war files and schema](#updating-war-and-schema-manually) before proceeding.

1. Create a temporary directory inside container and move into it: `# mkdir ~/passport_update; cd ~/passport_update`

1. Download and extract the recent Passport package: `# wget https://ox.gluu.org/npm/passport/passport-3.1.4.tgz; tar -xzvf passport-3.1.4.tgz`

1. Backup current Passport's files: `# tar -cvpzf ./passport-package-v313-backup.tar.gz /opt/gluu/node/passport/`

1. Stop the service: `# service passport stop`

1. Remove the previous package and deploy the new one: `# cd /opt/gluu/node/passport; rm -rf ./*; cp -R ~/passport_update/package/* ./`

1. Restore proper permissions on the files: `# chown -R node:node /opt/gluu/node/passport`

1. Update the custom script: 
    - Login to oxTrust and locate the interception script labelled `passport_social` (on "Manage custom scripts -> Person authentication").
    - Replace the contents with those of the file found [here](https://github.com/GluuFederation/community-edition-setup/blob/version_3.1.4/static/extension/person_authentication/PassportExternalAuthenticator.py).
    - Add new property to script `behaviour` with value `social`
    - Add this couple of properties too: `key_store_file=/etc/certs/passport-rp.jks`, `key_store_password=secret`
    - If you are employing Passport - Inbound SAML flow, substitute the `passport_saml` script as well. [Here](https://github.com/GluuFederation/community-edition-setup/blob/version_3.1.4/static/extension/person_authentication/SamlPassportAuthenticator.py) is the updated version.
    - Add the `behaviour` property to your `passport_saml` script with value `saml`
    - Add `key_store_file` and `key_store_password` as in social script

1. Edit `/etc/gluu/conf/passport-config.json` by changing "applicationEndpoint" property to "`https://<host-name>/oxauth/postlogin`"

1. (Optional) In /etc/gluu/conf/passport-config.json add a property "logLevel", example: `"logLevel": "info",`

1. Restart passport: `# service passport start`

1. Clean the temporary files: `# cd ~/; rm -rf ~/passport_update`

#### Upgrading to 3.1.3

1. Have the Client ID and Client Secrets of your already registered strategies at hand. Due to an standardization process performed on how configuration properties are stored, you may need to re-enter those again via oxTrust.

1. Ensure you have updated the [war files and schema](#updating-war-and-schema-manually) before proceeding.

1. Create a temporary directory inside container and move into it: `# mkdir ~/passport_update; cd ~/passport_update`

1. Download and extract the recent Passport package: `# wget https://ox.gluu.org/npm/passport/passport-3.1.3.tgz; tar -xzvf passport-3.1.3.tgz`

1. Backup current Passport's files: `# tar -cvpzf ./passport-package-v312-backup.tar.gz /opt/gluu/node/passport/`

1. Stop the service: `# service passport stop`

1. Remove the previous package and deploy the new one: `# cd /opt/gluu/node/passport; rm -rf ./*; cp -R ~/passport_update/package/* ./`

1. Restore proper permissions on the files: `# chown -R node:node /opt/gluu/node/passport`

1. Initialize Passport framework:
    - `# su - node`
    - `$ cd /opt/gluu/node/passport`
    - `$ mkdir server/logs`
    - `$ export PATH=$PATH:/opt/node/bin`
    - Before proceeding, ensure the host has internet connection, then run `$ npm install -P`
    - `$ exit`

1. Patch known vulnerability in the code:

    - Update the corresponding custom script: Login to oxTrust and locate the interception script labelled `passport_social` (on "Manage custom scripts -> Person authentication"). Replace the contents with those of the file found [here](https://raw.githubusercontent.com/GluuFederation/gluu-passport/version_3.1.3_securitypatch_issue30/scripts/PassportExternalAuthenticator.py).
    - Add new properties to the `passport_social` authentication script (do not use quotes):
        - "key_store_file" = "/etc/certs/passport-rp.jks"
        - "key_store_password" = "secret"
    - If you are employing Passport - Inbound SAML flow, substitute the `passport_saml` script as well. [Here](https://raw.githubusercontent.com/GluuFederation/gluu-passport/version_3.1.3_securitypatch_issue30/scripts/SamlPassportAuthenticator.py) is the updated version.
    - Add the same two properties you just added to `passport_social` to Inbound SAML script (`passport_saml`)
    - Edit `/etc/gluu/conf/passport-config.json` by changing "applicationEndpoint" property to "`https://<host-name>/oxauth/postlogin`"
    - Acquire patched `index.js` file from [here](https://raw.githubusercontent.com/GluuFederation/gluu-passport/version_3.1.3_securitypatch_issue30/server/routes/index.js) and overwrite `/opt/gluu/node/passport/server/routes/index.js` with it. Make sure its ownership is still set as "node:node": `# chown node:node /opt/gluu/node/passport/server/routes/index.js`

!!! Note:
    If you are upgrading from 3.1.0 or 3.1.1, please account for the following 3 additional steps:
    
1. Download [passport-saml-config.json](https://github.com/GluuFederation/community-edition-setup/raw/version_3.1.3/templates/passport-saml-config.json) and place it in directory `/etc/gluu/conf/`.

1. Add this line `NODE_LOGS=$NODE_BASE/logs` to file `/etc/default/passport`

1. Run this [script](mod_ldap.py) inside chroot container. This requires installing `python-ldap` beforehand:

    - For CentOS/RHEL/Fedora run: `yum install python-ldap`, for Ubunutu/Debian do: `apt-get install python-ldap`
    - Run `# python mod_ldap.py`

To finish please do:

1. In the oxTrust admin console, go to `Configuration` > `Manage authentication` > `Passport authn method`, double check your strategies are listed and the client ID/secrets are properly shown, otherwise make any adjustment before proceeding.

1. Move to the "Configuration -> Manage Custom scripts -> UMA RPT Policies" page and make sure "uma_client_authz_rpt_policy" script is enabled there.

1. Start passport service: `# service passport start`

1. Clean the temporary files: `# cd ~/; rm -rf ~/passport_update`

### Latest .war Files

The latest release of .war files can be downloaded from the locations provided below. Select the subdirectory corresponding to 
your package version.

!!! Note
    Subdirectories marked as "-SNAPSHOT" are not safe for general public's use and should be avoided unless you were specifically instructed by Gluu staff to use one.

- [oxTrust](https://ox.gluu.org/maven/org/xdi/oxtrust-server/)
- [oxAuth](https://ox.gluu.org/maven/org/xdi/oxauth-server/)
- [Shibboleth IdP](https://ox.gluu.org/maven/org/xdi/oxshibbolethIdp/)
- [Asimba SAML proxy](https://ox.gluu.org/maven/org/asimba/asimba-wa/)
- [oxAuth RP](https://ox.gluu.org/maven/org/xdi/oxauth-rp/)

### Location of Gluu 3.1.4 Components

Gluu 3.1.x components that can be updated in this way inside the container can be found at the following locations:

- oxTrust: `/opt/gluu/jetty/identity/webapps/identity.war`
- oxAuth: `/opt/gluu/jetty/oxauth/webapps/oxauth.war`
- Shibboleth IdP: `/opt/gluu/jetty/idp/webapps/idp.war`
- Asimba SAML proxy: `/opt/gluu/jetty/asimba/webapps/asimba.war`
- oxAuth RP: `/opt/gluu/jetty/oxauth-rp/webapps/oxauth-rp.war`


## Upgrade from 3.0.x to 3.1.4


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

Review the [installation docs](../installation-guide/install.md) to install the Gluu Server using the package manager. Once the package manager has installed version `3.1.4`, execute the following commands:

```
# cp -r /opt/gluu-server-3.0.x/root/backup_3031/ /opt/gluu-server-3.1.4/root/

# service gluu-server-3.1.4 start

# service gluu-server-3.1.4 login

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

## Upgrade from 2.x.x to 3.1.4

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

# python export2431.py
```

The export script will generate a directory called `backup_2431` which will have all the data from the current installation. Check the log file generated in the directory for any errors.

### Install the Latest Version of the Gluu Server

Stop the current version of the Gluu Server.

```
# service gluu-server-2.4.x stop
```

Review the [installation docs](../installation-guide/install.md) to install the Gluu Server using the package manager. Once the package manager has installed version `3.1.4`, then follow the next steps to prepare :

```
# cp -r /opt/gluu-server-2.4.x/root/backup_2431/ /opt/gluu-server-3.1.4/root/

# service gluu-server-3.1.4 start

# service gluu-server-3.1.4 login

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
