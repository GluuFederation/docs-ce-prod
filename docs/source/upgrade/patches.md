# Gluu Server Patches

## OPENDJ-2969 
### February 15, 2019

### Affected versions
- All Gluu versions (2.x - 3.x), any installation using Gluu OpenDJ

### Description

OpenDJ 3.0 is affected by bug preventing replication server component from successfully starting if its DB's certain changelog (binary) files are of size of multiply of 256. More info on the [OpenDJ jira](https://bugster.forgerock.org/jira/browse/OPENDJ-2969).

Upgrading to a fixed 3.5 package version isn't yet possible at the time of writting due to licensing. The only possible workaround is to rename/remove the `changeDBlog/` dir before starting OpenDJ's JVM. Thus a workaround was developed by the Gluu Team in attempt to mitigate its impact, which automates the process and does it transparenlty to an user.

If the bug presents itself, when starting the Gluu Server you will see errors like: `changeLogDB doesn't have enough space so replication can't be performed.`

### Steps to Fix

!!! Note
    Only if the bug is observed should the workaround documented below be implemented.

#### Patching steps

Follow next steps to apply the patch:

1. All work should be done inside Gluu-Server container. 

1. Put patching script at `/usr/local/sbin/check_changelog.sh` (see source code of it below)   

1. Edit `/opt/opendj/bin/start-ds` script by adding section calling the patch script to the beginning of it (see diff below for clues)    
1. Set proper permissions for the patch script: `# chmod +x /usr/local/sbin/check_changelog.sh; chown ldap:ldap /usr/local/sbin/check_changelog.sh`

When service is started/restarted, if unsafe condition is detected, script will rename the current `changeDBlog/` dir to `changeDBlog.TIMESTAMP/` and then will allow `start-ds` script to proceed with starting OpenDJ, expecting it to re-create the directory.

#### Patch script's source

```
#!/bin/bash

base=`basename $PWD`
TODAY=`date +%Y%m%d_%H%M`
changeDBlog="/opt/opendj/changelogDb"

date=`date "+%y%m%d-%H%M%S"`

files=`find $changeDBlog -name "head.log" -print` 
for file in $files; do
	size=`ls -l $file | awk '{print $5}'`
	check1=`expr ${size} / 256`
	check2=`expr 256 \* ${check1}`
	if [ "${size}" = "${check2}" -a "${check1}" != "0" ]; then
		echo "ALERT! $file has size as multiple of 256..."
		echo "Renaming $changeDBlog as ${changeDBlog}.$TODAY"
		mv $changeDBlog ${changeDBlog}.$TODAY
		break
	fi
done
echo "Moving towards normal opendj start now..."
```

#### Diff between the modified and original `start-ds` files

```
# diff -c /opt/opendj/bin/start-ds-new /opt/opendj/bin/start-ds
*** /opt/opendj/bin/start-ds-new	2018-02-12 12:17:38.534685038 -0500
--- /opt/opendj/bin/start-ds	2016-04-20 07:16:29.000000000 -0400
***************
*** 19,33 ****
  # Capture the current working directory so that we can change to it later.
  # Then capture the location of this script and the Directory Server instance
  # root so that we can use them to create appropriate paths.
- 
- ### This is custom procedure implemented by Ganesh/Zico/Alex
- test_changelog () {
-   /usr/local/sbin/check_changelog.sh
- }
- 
- test_changelog
- ####################################
- 
  WORKING_DIR=`pwd`
  
  cd "`dirname "${0}"`"
--- 19,24 ----

```
