# Gluu Server Patches

!!! Attention
    The official support end-of-life (EOL) date for Gluu Server 2.4.4 is December 31, 2018. Starting January 1, 2019, no further security updates or bug-fixes will be provided for Gluu Server 2.X. We strongly recommend [upgrading](https://gluu.org/docs/ce/upgrade/) to the newest version.
    
## OPENDJ-2969 
### February 15, 2019

### Affected versions
- All Gluu versions (2.x - 3.x), any installation using Gluu OpenDJ

### Description

OpenDJ 3.0 is affected by bug preventing replication server component from successfully starting if its DB's certain changelog (binary) files are of size of multiply of 256. More info on the [OpenDJ jira](https://bugster.forgerock.org/jira/browse/OPENDJ-2969).

Upgrading to a fixed 3.5 package version isn't yet possible at the time of writting due to licensing. The only possible workaround is to rename/remove the `changeDBlog/` dir before starting OpenDJ's JVM. Thus a workaround was developed by the Gluu Team in attempt to mitigate its impact, which automates the process and does it transparenlty to an user.

### Steps to Fix

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


## Code White Patch
### August 21, 2018

### Affected versions
- All currently supported Gluu versions (2.4.4, 3.x)

### Description
We have discovered a critical vulnerability in the Jboss Richfaces library. All versions of the component Richfaces (including the latest v4.5.17.Final) are affected by the vulnerability, which is an EL injection leading to Remote Code Execution. The CVE assignment to MITRE for it is CVE-2018-12532. The CVE can be seen on the [MITRE](http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-12532) site as well as [NIST](https://nvd.nist.gov/vuln/detail/CVE-2018-12532). 

This vulnerability is basically a bypass of CVE-2015-0279. CVE-2015-0279 hardens the `org.richfaces.resource.MediaOutputResource` class by blocking expressions containing [parantheses](https://github.com/richfaces/richfaces/blob/4.5.17.Final/components/a4j/src/main/java/org/richfaces/resource/MediaOutputResource.java#L67-L69). The new vulnerability lies in the fact that EL additionally made use of custom variable mappers internally to resolve the variable name in case it's not found in the main expression, but variable mappers themselves can contain EL code just the same. Variable mappers are implemented through the `varMapper` field of `org.apache.el.MethodExpressionImpl` in Tomcat EL API, which Jetty is also using.

The general flow looks like this: the application deserializes the "do" parameter (the 'source') at `org.richfaces.resource.ResourceUtils#decodeBytesData`, passes the object through some other calls, and eventually calls a `MethodExpression.invoke` on a field in the object (the 'sink') at `org.richfaces.resource.MediaOutputResource#encode`. There is however a protection in place restricting deserialization to [certain classes](https://github.com/richfaces/richfaces/blob/4.5.17.Final/core/src/main/java/org/richfaces/util/LookAheadObjectInputStream.java#L133), but as the `VariableMapperImpl` class is also whitelisted there, we then have full control over the `varMapper` field in the `MethodExpressionImpl` instance, which essentially means arbitrary EL injection.

As oxTrust/Identity utilizes Jboss Richfaces, this allows an unauthorized user to perform unauthorized Remote Code Execution. Knowing this, we have created a richfaces updater script that removes the affected class from the `identity.war` file, negating the impact of this vulnerability. That being said, we strongly recommend that **oxTrust should not be internet facing.**

### Steps to Fix

!!! Note
    We **strongly** recommend [backing up your environment](../operation/backup.md) before proceeding. 

!!! Note
    The script will suggest you to restart container after the patching is done. This step can be omitted if steps below were followed to the letter, as stopping and starting particular service ("tomcat" for 2.x and "identity" for 3.x) is enough to apply the changes.
    
1. Login to the Gluu Server chroot
1. Download the security patch from [https://repo.gluu.org/upd/richfaces_updater.sh](https://repo.gluu.org/upd/richfaces_updater.sh)
1. Grant `richfaces_updater.sh` executable privileges
1. Stop "tomcat"/"identity" services:

        Gluu Server 3.x: [root@localhost ~]# service identity stop
        Gluu Server 2.x: [root@localhost ~]# service tomcat stop

1. Run `richfaces_updater.sh`

        [root@example ~]# service gluu-server-x.x.x Login
        Welcome to the Gluu Server!
        [root@localhost ~]# chmod +x richfaces_updater.sh 
        [root@localhost ~]# ./richfaces_updater.sh 
        Creating directory /opt/upd
        Verifying archive integrity...  100%   MD5 checksums are OK. All good.
        Uncompressing Gluu Richfaces Updater  100%  

        Backing up /opt/gluu/jetty/identity/webapps/identity.war to /opt/upd/Thu_Aug_16_20:21:50_2018
        Updating /opt/gluu/jetty/identity/webapps/identity.war
        Deleting old richfaces from identity.war
        deleting: WEB-INF/lib/richfaces-4.5.17.Final.jar
        deleting: WEB-INF/lib/richfaces-core-4.5.17.Final.jar
        deleting: WEB-INF/lib/richfaces-a4j-4.5.17.Final.jar
        Adding latest richfaces to identity.war
        adding: WEB-INF/lib/richfaces-4.5.17-gluu.Final.jar (deflated 20%)
        adding: WEB-INF/lib/richfaces-a4j-4.5.17-gluu.Final.jar (deflated 10%)
        adding: WEB-INF/lib/richfaces-core-4.5.17-gluu.Final.jar (deflated 9%)

1. Start "tomcat"/"identity" services:

        Gluu Server 3.x: [root@localhost ~]# service identity start
        Gluu Server 2.x: [root@localhost ~]# service tomcat start

### Explanation of Fix

By following the above instructions, you will replace the old richfaces library in `identity.war` with a custom fixed version for the Gluu Server. The fix is accomplished by removing the affected (and unused) classes from the vulnerable library, negating the impact of the vulnerabiity.

A backup of your `identity.war`, before changes, is in the `/opt/upd/backup_$TIME_STAMP` directory in case you need it.
