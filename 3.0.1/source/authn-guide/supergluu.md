# Super Gluu
## Overview
[Super Gluu](https://super.gluu.org) is a free and secure two-factor authentication mobile application developed by Gluu. It is based on the free open source [oxPush2](https://github.com/GluuFederation/oxPush2) two-factor authentication application. 

This document will explain how to use the [Super Gluu interception script](https://github.com/GluuFederation/oxAuth/blob/master/Server/integrations/super_gluu/SuperGluuExternalAuthenticator.py) to configure the Gluu Server for a two-step authentication process with username and password as the first step, and Super Gluu as the second step. 

In order to use this authentication mechanism users will need to download the Super Gluu mobile app from the [Android](https://play.google.com/store/apps/details?id=gluu.super.gluu) or [iOS](https://itunes.apple.com/us/app/super-gluu/id1093479646?ls=1&mt=8)  marketplace. 

## Properties
The script has the following properties

|	Property	|	Description		|	Example	|
|-----------------------|-------------------------------|---------------|
|application_id		|URL of the identity server	|https://idp.gluu.info|
|authentication_mode	|Determine factor of authentication|two_step|
|credentials_file	|JSON file for oxPush2 		|/etc/certs/oxpush2_creds.json|

## Configure oxTrust

1. Navigate to `Configuration` > `Manage Custom Scripts`.               

2. Click on the `Perosn Authentication` tab.              
![person-auth](../img/admin-guide/multi-factor/person-auth.png)

3. Select the oxPush2 Script                  
![oxpush2-script](../img/admin-guide/multi-factor/oxpush2-script.png)

4. Enable the script by ticking the check box          
![enable](../img/admin-guide/enable.png)
 
5. Click `Update`         

6. Change the `Authentication method` to oxPush2       
![oxpush2](../img/admin-guide/multi-factor/oxpush2.png)
