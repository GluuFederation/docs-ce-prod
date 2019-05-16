# Here is how you can check which version of the Gluu Server you are using:

!!! Attention
    The official support end-of-life (EOL) date for Gluu Server 2.4.4 is December 31, 2018. Starting January 1, 2019, no further security updates or bug-fixes will be provided for Gluu Server 2.X. We strongly recommend [upgrading](https://gluu.org/docs/ce/upgrade/) to the newest version.


```
1. SSH into VM
2. Log into Gluu-Server container
3. oxTrust version: cat /opt/tomcat/webapps/identity/META-INF/MANIFEST.MF
4. oxAuth version: cat /opt/tomcat/webapps/oxauth/META-INF/MANIFEST.MF
```
