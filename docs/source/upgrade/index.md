# Upgrade to Gluu Server 4.1

## Overview
The Gluu Server **cannot** be upgraded with a simple `apt-get upgrade`. You will need to either use our in-place upgrade script or explicitly install the new version and export/import your data. Find the existing version below for upgrade instructions to Gluu Server 4.1. 

### Pre-requisites

- Before upgrading, make sure to [back up](../operation/backup.md) the Gluu container or LDAP LDIF. 
- Upgrades should always be thoroughly scoped and tested on a development environment *first*.

### Upgrading from 3.1.x to 4.1

At this time, only Gluu Server version 3.1.x can be upgraded to version 4.1. The upgrade script works on CentOS 7, Ubuntu 16, and RedHat 7. Upgrade script performs the following steps:

- Upgrades Java to Amazon Corretto. Extracts certificates from the existing Java keystore to `hostname_service.crt` in the upgrade directory. After upgrading Java, imports to keystore
- Upgrades all Gluu WAR files, NodeJS, and Passport components
- Transfers all data from LDAP to `gluu.ldif` in the upgrade directory
- Upgrades to [WrenDS](https://github.com/WrenSecurity/wrends) (a community maintained fork of OpenDJ). If you are currently running OpenLDAP, it will be backed up and migrated to WrenDS
- Processes `gluu.ldif` to convert the existing data set to the new model. Removes all inums. Depending on the data
size, this step will take some time. Writes resulting data to `gluu_noinum.ldif`. Your current passport configuration
will be moved to `gluuPassportConfiguration.json` for future reference
- Imports `gluu_noinum.ldif` to newly installed WrenDS. Rejected and Skipped entries will be written to 
`opendj_rejects.txt` and `opendj_skips.txt` to the upgrade directory
- Upgrade script uses setup.py to updated the configuration. All activities will be logged to `setup/update.log` and
`update_error.log`
- All files will be backed up with `file_name.gluu-version-#~` where # is a consecutive number, unless backup is specified in
another way.
- Sets the OpenID Connect `claimsParameterSupported` property to `false` by default to ensure clients are unable to gather unwanted claims. If a client in use depends on this property, it can be set back to `true` in the JSON configuration.

!!! Note
    If you are using custom schema:  
    (a) OpenDJ Users: Back up the schema file  
    (b) OpenLDAP users: Convert the schema according to [this guide](https://backstage.forgerock.com/docs/opendj/3.5/admin-guide/#chap-schema)  
    
    When the upgrade script prompts:  
    
    ```
    If you have custom ldap schema, add them now and press c  
    If you don't have any custom schema you can continue with pressing c
    ```
    
    Put the schema file in `/opt/opendj/config/schema/`


There are two options to perform the upgrade (both methods work inside the container):

#### Upgrade with Scripts
There are two steps upgrading 3.1.x to 4.1: first upgrade from 3.1.x to 4.0 and then upgrade to 4.1
We need two scripts:

##### 1) Upgrade 3.1.x to 4.0 
The upgrade script can download all needed software and applications from the internet. You can perform an online upgrade by following these steps:

* Download the upgrade script

```
wget https://raw.githubusercontent.com/GluuFederation/community-edition-package/master/update/4.0/update.py
```

* Execute the script with `-o` argument

```
python update.py -o
```

Your upgrade directory will be the current directory. The script will create these directories: `app`, `war`, `temp`, `setup`

##### 2) Upgrade 4.0 to 4.1

* Download the upgrade script

```
wget https://raw.githubusercontent.com/GluuFederation/community-edition-package/master/update/4.1.0/upg40to410.py
```

* Execute the script:

```
python upg40to410.py
```

