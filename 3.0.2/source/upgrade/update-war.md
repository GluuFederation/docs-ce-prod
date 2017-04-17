# Updating a war file

A [war](https://en.wikipedia.org/wiki/WAR_(file_format)) file is a 
zipped up java web application. Because they make deployment a breeze,
even if you hate violence, you can learn to love .war's!

When you install a new version of Gluu, it always comes with the latest
war files. However, sometimes you might make a customization, or 
Gluu might send you a war file as a temporary fix between
service pack or version releases. These instructions walk you through
how to put it to use. 

Keep in mind that a new version of code may also require updates to
the LDAP schema or to the application JSON properties. Make sure 
you are aware of any requirements before you start, because missing
data can cause the Gluu Server to malfunction.

In the following example, we assume the service is oxTrust (which
uses the warfile "identity.war"). But you could switch this process 
for any of the Gluu Server war files like oxAuth, asimba, the 
Shibboleth IDP or oxauth-rp.

1. Login to chroot container 

    `# service gluu-server-3.0.2 login`
    
2. Stop the respective service. 

    `# service identity stop`
    
3. Navigate to the /opt/gluu/jetty folder and back up the current app
in root's home directory (just in case you need to restore!)

    `# cd /opt/gluu/jetty/`
    
    `# tar -czf ~/identity.tar.gz identity`
    

4. Download and install the latest release war (assuming the 
URL was in the $WAR_URL environment variable).

    `# cd /opt/gluu/jetty/identity/webapps/`
    
    `# rm identity.war`
    
    `# wget $WAR_URL`
    

5. Start the service (for example oxTrust)
    
    `# service identity start`
    
Latest release of war files can be downloaded from [here](https://ox.gluu.org/maven/org/xdi/oxtrust-server/)
