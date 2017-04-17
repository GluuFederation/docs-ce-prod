# U2F
This script enables multi-factor authentication with any FIDO U2F device. Learn more about the U2F standard [here](https://www.gluu.org/resources/documents/standards/fido-u2f/). For a list of U2F compliant devices for sale, [check Amazon](http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=U2F). 

Some well known U2F device manufacturers include:  
- [Yubico](https://www.yubico.com/)   
- [HyperFIDO](http://hyperfido.com/)   
- [Feitian Technologies](http://www.ftsafe.com/)    

## Overview
The script has the following properties

|	Property	|	Description		|	Example	|
|-----------------------|-------------------------------|---------------|
|u2f_server_uri		|URL of the u2f server		|https://idp.gluu.info|
|u2f_server_metadata_uri|URL of the u2f server metadata|https://idp.gluu.info|

## Installation
### Configure oxTrust
Follow the steps below to configure the [DUO][duo] module in the oxTrust Admin GUI.

1. Go to Manage Custom Scripts
![image](../img/2.4/config-script_menu.png)

2. Click on the Person Authentication tab
![image](../img/2.4/config-script_person.png)

3. Select the [U2F script](https://raw.githubusercontent.com/GluuFederation/oxAuth/master/Server/integrations/u2f/U2fExternalAuthenticator.py)
![image](../img/2.4/config-script_u2f.png)

4. Enable the script by ticking the check box
![image](../img/2.4/config-script_enable.png)

5. Click Update 
![image](../img/2.4/config-script_update.png)

6. Change the Default authentication method to U2F
![image](../img/2.4/admin_auth_u2f.png)

