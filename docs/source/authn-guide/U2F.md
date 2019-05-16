# FIDO U2F

## Overview
FIDO Universal 2nd Factor (U2F) is an open authentication standard that strengthens and simplifies two-factor authentication using specialized USB or NFC devices based on similar security technology found in smart cards. 

> Learn more about the U2F standard [on Gluu's website](https://www.gluu.org/resources/documents/standards/fido-u2f/).

This document will explain how to use Gluu's [U2F interception script](https://raw.githubusercontent.com/GluuFederation/oxAuth/master/Server/integrations/u2f/U2fExternalAuthenticator.py) 
to configure the Gluu Server for a two-step authentication process with username and password as the first step, 
and any U2F device as the second step.

Some well known U2F devices and manufacturers include:           
- [Vasco DIGIPASS SecureClick](https://www.vasco.com/products/two-factor-authenticators/hardware/one-button/digipass-secureclick.html)      
- [Yubico](https://www.yubico.com/)      
- [HyperFIDO](http://hyperfido.com/)       
- [Feitian Technologies](http://www.ftsafe.com/)      

Check [FIDO's certified products](https://fidoalliance.org/certification/fido-certified-products/) for a comprehensive list of U2F devices (sort by `Specification` == `U2F`).

## Properties
The script has the following properties

|	Property	|	Description		|	Example	|
|-----------------------|-------------------------------|---------------|
|u2f_application_id		|URL of the application		|`https://idp.gluu.info`|
|u2f_server_uri		|DNS/URL of the oxauth/u2f server|`https://idp.gluu.info`|
|u2f_server_metadata_uri|URL of the u2f server metadata|`https://idp.gluu.info`|

## Configure U2F

Follow the steps below to configure the U2F module in the oxTrust Admin GUI.

1. Navigate to `Configuration` > `Manage Custom Scripts`.    

2. Click on the `Person Authentication` tab       
![person-auth](../img/admin-guide/multi-factor/person-auth.png)

3. Select the U2F script       
![u2f-script](../img/admin-guide/multi-factor/u2f-script.png)

4. Enable the script by ticking the check box       
![enable](../img/admin-guide/enable.png)

5. Click `Update`

6. Change the `Default Authentication Method` to `u2f`       
![u2f](../img/admin-guide/multi-factor/u2f.png)
