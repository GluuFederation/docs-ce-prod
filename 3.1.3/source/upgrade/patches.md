# Gluu Server Patches

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

A backup of your `identity.war`, before changes, is in the `/opt/upd/backup_$TIME_STAMP` directory in case you need it.\

## Patching image/files uploading for Gluu 3.1.3
 
 There is a [known issue](https://github.com/GluuFederation/oxTrust/issues/1007) in Gluu 3.1.3 that affects file upload feature like **Person Import**, **Organization logo upload**.
 
 Below are steps to fix that issue by patching the oxtrust war file.
 
 1. Login into Gluu container
 1. Save a copy of you actual `/opt/gluu/jetty/identity/webapps/identity.war`
 1. Move to home directory: `#cd` 
 1. Copy identity.war in the current directory: `#cp /opt/gluu/jetty/identity/webapps/identity.war .`
 1. Run : ``` #zip -d identity.war WEB-INF/lib/jsf-api-2.2.17.jar```
 1. Run : ``` #zip -d identity.war WEB-INF/lib/jsf-impl-2.2.17.jar```
 1. Make directory: `#mkdir -p WEB-INF/lib`
 1. Change directory: `#cd WEB-INF/lib`
 1. Run: `#wget http://repository.jboss.org/nexus/content/groups/public-jboss/com/sun/faces/jsf-api/2.2.16/jsf-api-2.2.16.jar`
 1. Run: `#wget http://repository.jboss.org/nexus/content/groups/public-jboss/com/sun/faces/jsf-impl/2.2.16/jsf-impl-2.2.16.jar`
 1. Run: `#jar -uf identity.war WEB-INF/lib/jsf-api-2.2.16.jar`
 1. Run: `#jar -uf identity.war WEB-INF/lib/jsf-impl-2.2.16.jar`
 1. Move back the war file: `#cp identity.war /opt/gluu/jetty/identity/webapps/identity.war`
 1. Restart identity service: `#service identity restart`
