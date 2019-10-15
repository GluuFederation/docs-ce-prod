# Upgrade to Gluu Server 4.0 Beta

## Overview
The Gluu Server **cannot** be upgraded with a simple `apt-get upgrade`. You will need to either use our in-place upgrade script or explicitly install the new version and export/import your data. Find your existing version below for upgrade instructions to Gluu Server 4.0. 

### Pre-requisites

- Before upgrading, make sure to [back up](../operation/backup.md) the Gluu container or LDAP LDIF. 
- Upgrades should always be thoroughly scoped and tested on a development environment *first*.

### Upgrading from 3.1.6 to 4.0

At this time, only Gluu Server version 3.1.6 can be upgraded to version 4.0 Beta. Upgrade script works on
CentOS 7, Ubuntu 16, and RedHat 7. Upgrade script performs the followings:
- Upgrade Java to recent Amazon-Corretto. Extracts certificates from existing java keystore to `hostname_service.crt` to the upgrade directory, after upgrading Java, imports to keystore
- Upgrades all Gluu war files, nodejs, passport components
- Dumps all data from ldap to `gluu.ldif` in upgrade directory
- Upgrade to WrenDS. If you are currently running OpenLDAP, it will be removed and migrated to WrenDS
- Process `gluu.ldif` to convert the existing data set to the new model.Remove all inums. Depending on your data
size, this step will take some time. Writes resulting data to `gluu_noinum.ldif`. Your current passport configuration
will be dumped to `gluuPassportConfiguration.json` for future reference
- Imports `gluu_noinum.ldif` to newly installed WrenDS. Rejected and Skipped entries will be written to 
`opendj_rejects.txt` and `opendj_skips.txt` to the upgrade directory
- Upgrade script uses setup.py to perform certain tasks. All activities will be logged to `setup/update.log` and
`update_error.log`
- All files will be backed up with `file_name.gluu-version-#~` where # is consecutive number unless backup is specified in
another way.

You have two options to perform upgrade (both method works inside container):

#### Online Upgrade
Upgrade script can download all neeeded sowftware/applications from net. You can perform online upgrade as follows:

* Download upgrade script
```
wget https://raw.githubusercontent.com/GluuFederation/community-edition-package/master/update/4.0/update.py
```
* Execute with `-o` argument
```
python update.py -o
```
Your upgrade directory will be current directory. So script will create these directories: `app`, `war`, `temp`, `setup`

#### Static Upgrade
The static self extracting upgrade package contains all components for upgrade. Though you still need internet connection to install libraries nedeed by upgrade script. To perform static upgrade

* Download self extracting package
```
wget http:// ...... /4-0-upg.sh
```

* Execute
```
sh 4-0-upg.sh
```
Your upgrade directory will be `/opt/upd/4.0-upg`
