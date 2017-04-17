#FAQ

## How do I change hostname and/or IP address and/or listening port of my Gluu Server?

There is no easy way to change any of those once your instance is already deployed. At very least it would require to modify a lot of settings stored in LDAP configuration entries, in Apache/Tomcat configuration, and perhaps in custom authentication scripts' sources too (if you plan to use one). If you need to change an IP address, we recommend doing a fresh install on a new VM.

Aside from using static public ip address, you could opt to use some static ip address from private range of your internal network, and to employ some sort of reverse proxy, or load balancer, or simple port forwarding on another internet-facing device that will forward connections to your instance in that network. When it's set up this way you can freely change your public ip address on this internet-facing intermediary device (just will need to make sure your DNS records will be updated accordingly each time).

## How do I set my port to something other than 443?

Ports other then 443 are not really supported. Port 443 is the Apache Web Server. But you'd have to update all the metadata too, like the config data in `https://hostname/.well-known/openid-configuration` and also the SAML metadata. And even then you still might face bugs.

Recommendation: use a virtual ethernet interface and a different IP address on your server rather than trying to update the port to a different port.

## How do I customize the IDP to ask for Email instead of Username for login? 

In oxTrust navigate to the Manage Authentication tab within the Configuration section. By default the Primary Key and Local Key are set to `uid`. Set those values to `mail` and now your Gluu Server will expect email as the identifier instead of username.

![Screenshot](../img/oxTrustConfiguration/Configuration/Authentication/Manage_Authentication_Primary_key_change.png)

Now you will want to update your IDP login page to display `Email Address` as the requested identifier. In order to do that you need to modify the `login.xhtml` file, which is located in `/opt/tomcat/webapps/oxauth/`. Insert `Email Address` as the value for `outputLabel`; this snippet is under the `dialog` class. See the screenshot below. 

![Screenshot](../img/oxTrustConfiguration/Configuration/Authentication/Email_Address.png)

## How do I add additional roles to oxTrust (Gluu's web UI) and/or change permissions set for existing ones?

To accomplish something like that, you would need to implement new dynamic rules in Jboss Seam, and then implement those rules in the UI, as current "manager" and "user" roles are defined within `security.drl` and hard-coded in OxTrust. During login, it checks for the manager group's membership, and adds the role to the web context. If you'll still opt to change this framework, we won't be able to provide you any help regarding this currently.

oxTrust was designed to be a tool for administrators. There are some basic user features, but we don't really encourage usage of oxTrust as a user facing application.

A better approach might be to write a standalone application that calls the SCIM API's or even the LDAP API's with just the data that you want to expose, then make that new application an [Openid Connect](http://openid.net/connect/) Relying Party (so authentication of users attempting to use it could be handled by your Gluu instance).

## How do I properly reboot my Gluu Server?
Follow these instructions to properly reboot your Gluu Server:

1. Stop Gluu Server container first:    
   a) For CentOS 6.x / RHEL6.x / Ubuntu 14.04: `service gluu-server-2.x.x stop`        
   b) For CentOS 7.x / RHEL7.x: `/sbin/gluu-server-2.x.x stop`       
2. Reboot the server    
3. After return, check if Gluu Server container started or not:     
   a) For CentOS 6.x / RHEL6.x / Ubuntu 14.04: `gluu-server-2.x.x status`    
   b) For CentOS 7.x / RHEL7.x: `/sbin/gluu-server-2.x.x status`     
4. If the Gluu Server didn't start, start it:     
   a) For CentOS 6.x / RHEL6.x / Ubuntu 14.04: `service gluu-server-2.x.x start`     
   b) For CentOS 7.x / RHEL7.x: `/sbin/gluu-server-2.x.x start`           
5. Wait 10 mins while the server is prepared. Check the login from your web browser.     

## How do I perform matinenace on my Gluu Server?

Sometimes it's required to push system updates (not an OS upgrade) in your Gluu Server VM. Here are a few steps to get you started:  
   - Backup your whole VM.   
   - Login to your Gluu Server VM.     
   - Become root.     
   - Login to the Gluu Server container using the following command: `service gluu-server-x.x.x login` (for RHEL/CentOS 7 users:     `/sbin/gluu-server-x.x.x login`)    
   - Push updates inside the container using the following command: `yum update` (for RPM based systems) or `apt-get update` (for DEB based systems).    
   - Exit the container.    
   - Stop Gluu-Server container using the following command: `service gluu-server-x.x.x stop` (for RHEL/CentOS 7users:     `/sbin/gluu-server-x.x.x stop`).   
   - Perform `yum update` or `apt-get update` in the host system.   
   - Do a soft reboot.   
   - After the VM returns from a succesful reboot, check the system status:    
     - See if your Gluu Server container started by running the following command: `service gluu-server-x.x.x status`.    
     - Login to the container.     
     - See if there is any issue in the `wrapper.log` file or in the `idp-process.log` file (if you are using SAML).    
     - Wait for 10 minutes.    
     - Check Gluu Server Web UI.     
