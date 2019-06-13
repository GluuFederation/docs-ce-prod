# Gluu Server Patches

## Patching image/files uploading for Gluu 3.1.3
 
 There is a [known issue](https://github.com/GluuFederation/oxTrust/issues/1007) in Gluu 3.1.3 that affects file upload feature like **Person Import**, **Organization logo upload**.
 
 Below are steps to fix that issue by patching the oxtrust war file.
 
 1. Log in to Gluu container
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
