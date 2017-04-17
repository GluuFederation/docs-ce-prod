# Updating a war file

A [WAR](https://en.wikipedia.org/wiki/WAR_(file_format)) file is a 
zipped up java web application. Because they make deployment a breeze,
even if you hate violence you can learn to love .war's!

When you install a new version of Gluu it always comes with the latest
WAR files. However, sometimes you might make a customization, or 
Gluu might send you a WAR file as a temporary fix between a
service pack or version release. 

These instructions walk you through how to put it to use. 

Keep in mind that a new version of code may also require updates to
the LDAP schema or to the application JSON properties. Make sure 
you are aware of the requirements before you start, because missing
data can cause the Gluu Server to malfunction.

In the following example we assume the service is oxTrust (which
uses the WAR file `identity.war`). However this process can be utilized  
to update the WAR file for any other Gluu Server module, like oxAuth, Asimba, 
Shibboleth IDP or oxAuth-RP, by simply changing the name of the WAR file in
the provided commands (you can find exact locations of
corresponding archives at the [end of this page](#latest-war-files).

1. Login to chroot container:  

    `# service gluu-server-3.0.1 login`
    
2. Stop the respective service:  

    `# service identity stop`
    
3. Navigate to the `/opt/gluu/jetty` folder and back up the current app in the root's home directory (just in case you need to restore!): 

    `# cd /opt/gluu/jetty/`
    
    `# tar -czf ~/identity.tar.gz identity`
    
4. Download and install the latest WAR (assuming the URL was in the $WAR_URL environment variable): 

    `# cd /opt/gluu/jetty/identity/webapps/`
    
    `# rm identity.war`
    
    `# wget $WAR_URL`
    
5. Start the service (for example oxTrust): 
    
    `# service identity start`

## Latest WAR files

The latest release of WAR files can be downloaded from the following locations:

- [oxTrust](https://ox.gluu.org/maven/org/xdi/oxtrust-server/)
- [oxAuth](https://ox.gluu.org/maven/org/xdi/oxauth-server/)
- [Shibboleth IdP](https://ox.gluu.org/maven/org/xdi/oxshibbolethIdp/)
- [Asimba SAML proxy](https://ox.gluu.org/maven/org/xdi/oxasimba-proxy/)
- [oxAuth RP](https://ox.gluu.org/maven/org/xdi/oxauth-rp/)

## Location of Gluu 3.x Components

Gluu 3.x components which can be updated in this way inside the container can be found at the following locations:

- oxTrust: `/opt/gluu/jetty/identity/webapps/identity.war`
- oxAuth: `/opt/gluu/jetty/oxauth/webapps/oxauth.war`
- Shibboleth IdP: `/opt/gluu/jetty/idp/webapps/idp.war`
- Asimba SAML proxy: `/opt/gluu/jetty/asimba/webapps/asimba.war`
- oxAuth RP: `/opt/gluu/jetty/oxauth-rp/webapps/oxauth-rp.war`
