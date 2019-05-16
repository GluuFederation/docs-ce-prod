# Here is how you can check which version of the Gluu Server you are using:

1. SSH into VM
2. Log into Gluu-Server container. 

    a. Using below command
    
     `# service gluu-server-3.0.0 login`
     
3. To find oxTrust version

      `# cat /opt/jetty-9.3/temp/jetty-localhost-8082-identity.war-_identity-any-8734901518752897483.dir/webapp/META-INF/MANIFEST.MF`

4. oxAuth version can be found using below command 

    `# cat /opt/jetty-9.3/temp/jetty-localhost-8081-oxauth.war-_oxauth-any-6134601069165491713.dir/webapp/META-INF/MANIFEST.MF`

Another simplest way to find out the Gluu Server installed or upgraded 
version can be found on the top the oxTrust Admin UI.

![Gluu Version](../img/oxtrust/welcome-page.png)

Versions of other apps like idp, asimba and oxauth-rp,
can be found or viewed in the same directory. These app can be 
identified with the [port number](./ports.md) after the localhost.