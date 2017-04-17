# oxPush2
This script enables use of the free open source [oxPush2 multi-factor authentication](https://github.com/GluuFederation/oxPush2) mechanism.
## Overview
The script has the following properties

|	Property	|	Description		|	Example	|
|-----------------------|-------------------------------|---------------|
|application_id		|URL of the identity server	|https://idp.gluu.info|
|authentication_mode	|Determine factor of authentication|two_step|
|credentials_file	|JSON file for oxPush2 		|/etc/certs/oxpush2_creds.json|

## Installation
### Configure oxTrust
Follow the steps below to configure the oxPush2 module in the oxTrust Admin GUI.

1. Go to Manager Custom Scripts
![image](../img/2.4/config-script_menu.png)

2. Click on the Person Authentication tab
![image](../img/2.4/config-script_person.png)

3. Select the [oxPush2 script](://raw.githubusercontent.com/GluuFederation/oxAuth/master/Server/integrations/oxpush2/oxPush2ExternalAuthenticator.py)
![image](../img/2.4/config-script_oxpush2.png)

4. Enable the script by ticking the check box
![image](../img/2.4/config-script_enable.png)

5. Click Update 
![image](../img/2.4/config-script_update.png)

6. Change the oxTrust  authentication method to oxPush2
![image](https://cloud.githubusercontent.com/assets/5271048/13883127/1aeba3b8-ecf6-11e5-8e69-798f2f26f827.png)

