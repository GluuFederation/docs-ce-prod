# Here is how you can check which version of the Gluu Server you are using:

```
1. SSH into VM
2. Log into Gluu-Server container
3. oxTrust version: cat /opt/tomcat/webapps/identity/META-INF/MANIFEST.MF
4. oxAuth version: cat /opt/tomcat/webapps/oxauth/META-INF/MANIFEST.MF
```
