# Manual upgrade from 2.4.4.2 or 2.4.4.3 to 3.0.1 with OpenDJ

## Overview
This guide explains how to upgrade the Gluu Server 2.4.4.2 (SP 2) or 2.4.4.3 (SP 3) to 3.0.1
and keep OpenDJ in the server. This guide assumes an Ubuntu operating system. 
For other operating systems some commands may change.

## Upgrade Process

> Note: "x" represents the version (sp2/sp3)

1\. Install 2.4.4 SP2/SP3

2\. Log into CE 2.4.4 SP2/SP3 and install it
```
service gluu-server-2.4.4.x start
service gluu-server-2.4.4.x login
cd /install/community-edition-setup/
./setup.py
```
3\. Exit and Stop 2.4.4.x SP2/SP3
```
exit
service gluu-server-2.4.4.x stop
```
4\. Disable 2.4.4 SP2/SP3 service auto startup
```
/usr/sbin/update-rc.d -f gluu-server-2.4.4.x disable
```
> For CentOS6.x: 
> - Disable 'gluuserver-2.4.4.x' from startup: `chkconfig gluu-server-2.4.4.x off`
> - Check the status of service in init: `chkconfig --list | grep gluu-server-2.4.4.x`

5\. Install 3.0.1 rpm/deb, do not run setup script. 

6\. Backup OpenDJ, ox-ldap.properties, salt from 2.4.4 SP2/SP3 and copy it into 3.0.1
```
cd /opt/gluu-server-2.4.4.x/opt
tar -czf opendj.tar.gz opendj
cp opendj.tar.gz /opt/gluu-server-3.0.1/opt/

cp /opt/gluu-server-2.4.4.x/opt/apache-tomcat-7.0.65/conf/ox-ldap.properties /opt/gluu-server-3.0.1/tmp
cp /opt/gluu-server-2.4.4.x/opt/apache-tomcat-7.0.65/conf/salt /opt/gluu-server-3.0.1/tmp
```
7\. Log into CE 3.0.1 and run setup script
```
service gluu-server-3.0.1 start
service gluu-server-3.0.1 login
cd /install/community-edition-setup/
./setup.py
```
8\. Verify if installed services are up

9\. Stop OpenLDAP and all installed services
```
service oxauth stop
service identity stop
...
service solserver stop
```
10\. Disable OpenLDAP
```
/usr/sbin/update-rc.d -f solserver disable
```

> For CentOS6.x
> - Disable in startup: `chkconfig solserver off`
> - Check the status in init: `chkconfig --list | grep solserver`

11\. Restore OpenDJ from 2.4.4 SP2/SP3
```
cd /opendj
rm -rf opendj
tar -xzf opendj.tar.gz
chown -R ldap:ldap opendj
```
12\. Update OpenDJ java settings
```
/bin/su ldap -c "export OPENDJ_JAVA_HOME=/opt/jre; /opt/opendj/bin/dsjavaproperties"
```

> For CentOS6.x: 
> Perform below operations are user 'ldap'

> - Add jre location in 'java.properties' ( location: /opt/opendj/config ): `default.java-home=/opt/jre`

> - Run command: `export OPENDJ_JAVA_HOME=/opt/jre`

> - Run command: `/opt/opendj/bin/dsjavaproperties`

13\. Create OpenDJ init script
```
export OPENDJ_JAVA_HOME=/opt/jre; /opt/opendj/bin/create-rc-script --outputFile /etc/init.d/opendj --userName ldap
/usr/sbin/update-rc.d -f opendj enable
```

> For CentOS6.x: 

> As root, run command: `export OPENDJ_JAVA_HOME=/opt/jre; /opt/opendj/bin/create-rc-script --outputFile /etc/init.d/opendj --userName ldap` 

> Add OpenDJ service in startup: `chkconfig opendj on`

> Check the status of OpenDJ service: `chkconfig --list | grep opendj`

14\. Update LDAP schema
```
cp -f /install/community-edition-setup/static/opendj/deprecated/101-ox.ldif /opt/opendj/config/schema/
```
15\. In 3.0.1 user custom attributes objectClass is `gluuCustomPerson`. It's defined in `/opt/opendj/config/schema/77-customAttributes.ldif` 

We need to add into it definition custom attributes from 2.4.4 SP2/SP3 `/opt/opendj/config/schema/100-user.ldif`. Old custom attributes `objectClass` is based on `orgInum`. Example: `ox-6657268F7461C8CE000150DA8011-oid`

16\. Start OpenDJ
```
service opendj start
```

17\. Verify startup messages in OpenDJ logs: `/opt/opendj/logs/server.out and /opt/opendj/logs/errors`

18\. Restore ox-ldap.properties and salt from CE 2.4.4 SP2/SP3
```
cd /etc/gluu/conf
mv ox-ldap.properties ox-ldap.properties.3.0.1
mv salt salt.3.0.1
mv /tmp/ox-ldap.properties .
mv /tmp/salt .
chown -R root:gluu /etc/gluu/conf
```
19\. Start CE servces
```
service oxauth start
service identity start
...
```

20\. Verify if installed services are up

21\. Update oxTrust JSON configuration
 - We need to update `personObjectClassTypes`, `personObjectClassDisplayNames` and  `personCustomObjectClass`.
 
   In  3.0.1 these properties have next default values:
   ```
   personObjectClassTypes = gluuCustomPerson, gluuPerson, eduPerson
   personObjectClassDisplayNames = gluuCustomPerson, gluuPerson, eduPerson
   personCustomObjectClass = gluuCustomPerson
   ```
 - We need to update `ldifStore`, `velocityLog`.
   In  3.0.1 these properties have next default values:
   `ldifStore` = `/var/ox/identity/removed`
   `velocityLog` = `/opt/gluu/jetty/identity/logs/velocity.log`
   
  - If you are using SAML, you have to modify couple of sections as well: 
    - Add Shibv3 Root Directory location: `"shibboleth3FederationRootDir":"/opt/shibboleth-federation",` [ This configuration goes in between of _"photoRepositoryCount..._ and _""velocityLog"..._ ]
    - Couple of other declarations: [ This configuration lies in between of _"scimTestModeAccessToken..."_ and _"clientWhiteList..."_ ] 
     ```
    "shibbolethVersion":"v3",
    "shibboleth3IdpRootDir":"/opt/shibboleth-idp",
    "shibboleth3SpConfDir":"/opt/shibboleth-idp/sp",
    "organizationName":"Gluu Inc.",
    "idp3SigningCert":"/etc/certs/idp-signing.crt",
    "idp3EncryptionCert":"/etc/certs/idp-encryption.crt",
      ```

22\. Update oxTrust CacheRefesh snapshotFolder.
   New snapshotFolder = `/var/ox/identity/cr-snapshots`

## Notes

1\. If in 2.4.4 SP2/SP3 environment SCIM was enabled we need to do the following:
 - Fill new properties: `scimUmaClientId`, `scimUmaClientKeyId`, `scimUmaResourceId`, `scimUmaScope`, `scimUmaClientKeyStoreFile`, `scimUmaClientKeyStorePassword` -- These properties have the same values as before, but in 3.0.1 we added prefix "scim" to all of them.
 - Copy `/etc/certs/scim-rs.jks` from 2.4.4 SP2/SP3 into 3.0.1
