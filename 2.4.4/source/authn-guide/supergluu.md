# oxPush2 - Super Gluu Authenticaion
## Overview
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