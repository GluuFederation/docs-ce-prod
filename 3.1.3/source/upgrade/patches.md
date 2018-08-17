# Gluu Server Patches

## Code White Patch
### August 16, 2018

### Affected versions
- All Gluu versions (1.x, 2.x, 3.x)

### Description
We have discovered a critical vulnerability in the Jboss Richfaces library. All versions of the component Richfaces (including the latest v4.5.17.Final) are affected by the vulnerability, which is an EL injection leading to Remote Code Execution. The CVE assignment to MITRE for it is CVE-2018-12532. The CVE can be seen on the [MITRE](http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-12532) site as well as [NIST](https://nvd.nist.gov/vuln/detail/CVE-2018-12532). 

This vulnerability is basically a bypass of CVE-2015-0279. CVE-2015-0279 hardens the `org.richfaces.resource.MediaOutputResource` class by blocking expressions containing [parantheses](https://github.com/richfaces/richfaces/blob/4.5.17.Final/components/a4j/src/main/java/org/richfaces/resource/MediaOutputResource.java#L67-L69). The new vulnerability lies in the fact that EL additionally made use of custom variable mappers internally to resolve the variable name in case it's not found in the main expression, but variable mappers themselves can contain EL code just the same. Variable mappers are implemented through the `varMapper` field of `org.apache.el.MethodExpressionImpl` in Tomcat EL API, which Jetty is also using.

The general flow looks like this: the application deserializes the "do" parameter (the 'source') at `org.richfaces.resource.ResourceUtils#decodeBytesData`, passes the object through some other calls, and eventually calls a `MethodExpression.invoke` on a field in the object (the 'sink') at `org.richfaces.resource.MediaOutputResource#encode`. There is however a protection in place restricting deserialization to [certain classes](https://github.com/richfaces/richfaces/blob/4.5.17.Final/core/src/main/java/org/richfaces/util/LookAheadObjectInputStream.java#L133), but as the `VariableMapperImpl` class is also whitelisted there, we then have full control over the `varMapper` field in the `MethodExpressionImpl` instance, which essentially means arbitrary EL injection.

As oxTrust/Identity utilizes Jboss Richfaces, this allows an unauthorized user to perform unauthorized Remote Code Execution. Knowing this, we have created a richfaces updater script that removes the affected class from the `identity.war` file, negating the impact of this vulnerability. That being said, we strongly recommend that **oxTrust should not be internet facing.**

### Steps to Fix
1. Login to the Gluu Server chroot
1. Download the security patch from https://repo.gluu.org/upd/richfaces_updater.sh
1. Grant `richfaces_updater.sh` executable privileges
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

1. Restart oxTrust/identity

        [root@localhost ~]# service identity restart

### Explanation of Fix

By following the above instructions, you will replace the old richfaces library in `identity.war` with a custom fixed version for the Gluu Server. The fix is accomplished by removing the affected (and unused) classes from the vulnerable library, negating the impact of the vulnerabiity.

A backup of your `identity.war`, before changes, is in the `/opt/update/$TIME_STAMP` directory in case you need it.
