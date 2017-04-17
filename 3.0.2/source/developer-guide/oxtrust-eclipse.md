# How to Build oxTrust with Eclipse

## Overview

This section of the document discusses how to build oxTrust using Eclipse. This guide can be followed by developers and architects to code and customize oxTrust.

## Building oxTrust With Eclipse
!!! Note 
    this installation procedure assumes you have a local VM running an instance of the Gluu Server CE. 

Gluu CE installation is discussed in the [Installation Guide](../installation-guide/install/#install-gluu-server-package).

Testing and Beta release can be found here: [Beta Release](https://ox.gluu.org/doku.php?id=qa:platforms )

### Summary
Here is a quick summary: 

We will be building latest branch 

```
# wget https://repo.gluu.org/centos/Gluu-centos7.repo -O /etc/yum.repos.d/Gluu.repo 

# wget https://repo.gluu.org/centos/RPM-GPG-KEY-GLUU -O /etc/pki/rpm-gpg/RPM-GPG-KEY-GLUU 

# rpm –import /etc/pki/rpm-gpg/RPM-GPG-KEY-GLUU 

# yum clean all 

# yum install gluu-server-3.0.2 

# /sbin/gluu-serverd-3.0.2 start 

# /sbin/gluu-serverd-3.0.2 enable 

# /sbin/gluu-serverd-3.0.2 login 
```
!!! Note: 
    This documentation is prepared based on CentOS, follow the appropriate installation guide based on your OS.
    
Gluu Server will run in chroot

```
# cd /install/community-edition-setup/ 

# ./setup.py 
```
You can mostly go with default values, however I suggest you make sure that oxTrust and LDAP servers 
are installed, and oxAuth is not. 

Install oxAuth OAuth2 Authorization Server? [Yes] : no 

Install oxTrust Admin UI? [Yes] : 

Install LDAP Server? [Yes] : 

Install Apache HTTPD Server [Yes] : no 

Now we need to collect critical configuration files and test data need for development environment: 
```
# mkdir /root/configs/ 

# /opt/opendj/bin/ldapsearch -h localhost -p 1636 -D “cn=directory manager,o=gluu” -w “<LDAP superuser password>” -ZXT -b “o=gluu” “objectclass=*” > /root/configs/everything.ldif 

# cp /etc/gluu/conf/ox-ldap.properties /root/configs/ 

# cp /etc/gluu/conf/salt /root/configs/ 

# cp /opt/gluu/*.schema /root/configs/ 

# tar -czf /root/configs.tgz /root/configs 
```
Now leave chroot 
```
# logout 
```

root directory of gluu chroot jail is `/opt/gluu-server-3.0.2/` 

download `/opt/gluu-server-3.0.2/root/configs.tgz` to your machine. 

## Download Software
Download below mentioned required softwares. And this assumes you're using Windows 64-bit operating sytsem. 
If you're using Mac or 32-bit Windows, adjust accordingly. 

### Java
Download [Java 1.8](http://www.oracle.com/technetwork/java/javase/downloads/jdk7-downloads-1880260.html),
When you install it, make sure you install both the JDK and the JRE in `c:\java` (not Program Files). 
Each of these software distributions should just be unzipped under `C:\java\jdk1.8.0_112` on my system. 

Updates your JAVA_HOME environment variable to point to the folder of your jdk, for example 

### Eclipse
Download [Eclipse IDE](http://www.eclipse.org/downloads/packages/eclipse-ide-java-ee-developers/mars1) 
for Java EE Developers 

### Maven
Download the latest [Maven](https://maven.apache.org/download.cgi)binary zip 

### Jetty
Download latest zip of [Jetty 9](http://www.eclipse.org/jetty/download.html) 

### Jython
Download [Jython](http://www.jython.org/downloads.html) and install in `c:\jython2.7.0` 

### Keystore Explorer
This is optional, but convenient. You can find it on [SorceForge](http://keystore-explorer.sourceforge.net/). 

## Configure Eclipse
### Install JBoss Tools Plugin

In the Help / Eclipse Marketplace menu add “JBoss Tools” 

  ![eclipse](../img/developer/oxtrust/eclipse.png)

### Set Perspective to Web Development

In the upper right hand corner, select the Web Development perspective from the pop-up menu. 
  ![Webdev](../img/developer/oxtrust/eclipse-webdev.png)

### Set Java 1.8 as JDK

From the Window / Preferences menu, just check the Java / Installed JRE's tab and 
make sure you see your 1.8 JDK (not JRE). 

  ![java](../img/developer/oxtrust/java-jdk.png)

### Add External Maven

Use the external maven you installed, not the built in maven. 
In Window / Preferences, there is a section for Maven. 
Under the Installations section, add the Maven folder you installed in `c:\java`

   ![maven](../img/developer/oxtrust/externalmaven.png)

### Install Eclipse Jetty Launcher

You should be able to install Jetty Launcher using either of the methods

If You want to run jetty in Eclipse, you can download and install 
Jetty Launcher from [eclipse marketplace](https://marketplace.eclipse.org/content/eclipse-jetty)

Or Jetty Launcher can be installed directly from eclipse marketplace 

  ![marketplace](../img/developer/oxtrust/jettylauncher.png)

### Turn off Validation
Document validation throws a lot of errors, and its better to see these as Warnings. 

   ![validationoff](../img/developer/oxtrust/validationoff.png)
 
### Import Projects
For each of these sections, you will have to use File / Import and then 
provide the Github URL 

   ![importproj](../img/developer/oxtrust/importprojs.png)

And then specify the github url 

   ![specifyurl](../img/developer/oxtrust/specifyurl-target.png)

You can find this URL on github 

![findurl](../img/developer/oxtrust/githubpage.png) 

- [oxTrust](https://github.com/GluuFederation/oxTrust.git)
- [oxAuth](https://github.com/GluuFederation/oxAuth.git)
- [oxCore](https://github.com/GluuFederation/oxCore.git)
- [SCIM Client](https://github.com/GluuFederation/SCIM-Client.git)

After importing all the projects, it will take some time to download and compile all the code. 
When everything is done building, you can set up run configuration for oxTrust to launch using Jetty:

   ![runconfiguration](../img/developer/oxtrust/runconfiguration.png)

Select m2e-wtp webapp folder for deployment in Jetty 

   ![deploy](../img/developer/oxtrust/deployinjetty.png)

Add VM arguments to jetty to specify location of oxTrust configuration. 
You can just create two empty directories for now. 

Those directories will contain gluu configuration and logs: 

   ![VMarguments](../img/developer/oxtrust/vmarguments.png)
 
Change jetty version in eclipse plugin to the one you downloaded earlier: 

   ![verchange](../img/developer/oxtrust/jettyverchng.png)

Add configuration listener to oxtrust-server/src/main/webapp/WEB-INF/web.xml: 

   ![conflistener](../img/developer/oxtrust/configurationlistener.png)

> ** OxTrust styles are packaged in a separate project oxtrust-static. 
In order for jetty to correcty serve those styles close the oxtrust-static 
project in eclipse and by updating the project under `Maven` >` Update Project` on `oxtrust` > `server project`. **  

## Configuration

To get your oxTrust running, you'll need to copy some file from your Gluu 
Server Community Edition (CE) installation. 

This assumes you've deployed CE, and run `setup.py`, and that its working. 
Add conf subdirectory to the one you referenced in gluu.base VM argument (e.g. `C:\home\gluu\conf\`) 

From the configs.tgz you downloaded earlier extract these files: 

 - configs/ox-ldap.properties
 - configs/salt

into the conf subdirectory you created (e.g. C:\home\gluu\conf\ox-ldap.properties) 

## Install OpenLDAP
We use this distribution of [OpenLdap]()http://www.userbooster.de/en/download/openldap-for-windows.aspx) for windows in this document: 

Any other build should work as well though. 

During the installation the only change required is to update ports to 1389 and 1636. 
If ports are changed to some other values - corresponding changes should 
be made in ox-ldap.properties and in everything.ldif before data import (or in database after import) 

   ![install](../img/developer/oxtrust/instalopenldap.png)

### Configure OpenLDAP
Extract these files from the configs.tgz we created earlier: 

- configs/slapd.conf
- configs/everything.ldif
- configs/user.schema
- configs/custom.schema
- configs/gluu.schema

put schema files into some easy-reachable location (e.g. `c:\home\gluu\`) 

Now update slapd.conf to resemble the `configs/slapd.conf`


1. Add ppolicy.schema to the include section 

2. Add user.schema, custom.schema and gluu.schema to the include section 

    ![policyschema](../img/developer/oxtrust/policyschema.png)

3. Load back_mdb.la, back_monitor.la and ppolicy.la modules 

    ![load modules](../img/developer/oxtrust/loadmdb.png)

4. Define access policy 

    ![accesspolicy](../img/developer/oxtrust/accesspolicy.png)

5. Define `o=gluu` database  

    ![GluuDB](../img/developer/oxtrust/gluudatabase.png)

6. Also create a data directory somewhere and update the location in `slapd.conf`
   
    ![datadir](../img/developer/oxtrust/datadir.png)

7. Define config database 

    ![configdb](../img/developer/oxtrust/configdb.png)

8. Remove memberOf mentions from gluu.schema (temporary) 

    ![remove](../img/developer/oxtrust/7.png)
  
    ![remove](../img/developer/oxtrust/22memberof.png)
  
    ![memberof](../img/developer/oxtrust/23memberof.png)
    
9. Change passwords in slapd.conf to the LDAP Admin password configured at gluu CE deployment. 

    !!! Note 
        You can use cleartext passwords in dev environment.

    ![changepswd](../img/developer/oxtrust/24chngpass.png)
    
    ![chngepswd2](../img/developer/oxtrust/25changepass.png)

10. Verify that slapd.conf is correct with `slaptest.exe`. Run slaptest exe installer using the paramater `-u`
   
    `# cd C:\OpenLDAP`
    
    `# slaptest.exe -u`
        
    ![slaptest](../img/developer/oxtrust/slaptest.png)

11. Import everything.ldif into the database using `slapadd.exe`

    ![importldif](../img/developer/oxtrust/importldif.png)
    
12. Restart database.

13. You can use Ldap Admin `http://www.ldapadmin.org/`
to verify that database is running and has been populated. 

14. If `http://www.userbooster.de/en/download/openldap-for-windows.aspx` doesn't allow  
OpenLDAP service to run on port 1636 instead of default 636 and if you are having difficulties 
with service you can stop windows service by using the command to run OpenLdap from commandline: 

    ![openldapcmd](../img/developer/oxtrust/openldapcmd.png)
    
15. Update oxtrust configuration in LDAP to use basic auth. You can use any ldap client, 
we recommend ldap admin.
    
    ![updateoxtrust](../img/developer/oxtrust/updateoxtrust.png)

!!! Note: 
    Your inum may vary. You have to change “authMode”:“” to “authMode”:“basic” 
    within ou=oxtrust,ou=configuration,inum=…,ou=applicanes,o=gluu in oxTrustConfApplication attribute 

## Test

Start your server.. and point your browser at http://localhost:8080/ 
