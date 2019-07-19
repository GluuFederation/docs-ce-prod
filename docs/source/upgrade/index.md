# Upgrade to Gluu Server 4.0 Beta

## Overview
The Gluu Server **cannot** be upgraded with a simple `apt-get upgrade`. You will need to either use our in-place upgrade script or explicitly install the new version and export/import your data. Find your existing version below for upgrade instructions to Gluu Server 4.0. 

### Pre-requisites

- Before upgrading, make sure to [back up](../operation/backup.md) the Gluu container or LDAP LDIF. 
- Upgrades should always be thoroughly scoped and tested on a development environment *first*.

### Upgrading from 3.1.6 to 4.0

At this time, only Gluu Server version 3.1.6 can be upgraded to version 4.0 Beta. This upgrade process is performed by downloading and running the following script inside the chroot:

```
wget https://raw.githubusercontent.com/GluuFederation/community-edition-package/master/update/4.0/update.py
```

```
python update.py
```

This script downloads and upgrades all components within the server.
