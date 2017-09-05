# FIDO U2F

## Overview
FIDO Universal 2nd Factor (U2F) is an open authentication standard that strengthens and simplifies two-factor authentication using specialized USB or NFC devices based on similar security technology found in smart cards. 

> Learn more about the U2F standard [on Gluu's website](https://www.gluu.org/resources/documents/standards/fido-u2f/).

This document will explain how to use Gluu's [U2F interception script](https://raw.githubusercontent.com/GluuFederation/oxAuth/master/Server/integrations/u2f/U2fExternalAuthenticator.py) 
to configure the Gluu Server for a two-step authentication process with username and password as the first step, 
and any U2F device as the second step.

## U2F Devices
Some well known U2F devices and manufacturers include:           
- [Vasco DIGIPASS SecureClick](https://www.vasco.com/products/two-factor-authenticators/hardware/one-button/digipass-secureclick.html)      
- [Yubico](https://www.yubico.com/)      
- [HyperFIDO](http://hyperfido.com/)       
- [Feitian Technologies](http://www.ftsafe.com/)      

Check [FIDO's certified products](https://fidoalliance.org/certification/fido-certified-products/) for a comprehensive list of U2F devices (sort by `Specification` == `U2F`).

## Prerequisites
- A Gluu Server ([installation instructions](../installation-guide/index.md));
- At least one U2F device for testing, like one of the devices [listed above](#u2f-devices);
- [U2F interception script](https://github.com/GluuFederation/oxAuth/blob/master/Server/integrations/u2f/U2fExternalAuthenticator.py) (included in the default Gluu Server distribution).

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

3. Find the U2F script       
![u2f-script](../img/admin-guide/multi-factor/u2f-script.png)

4. Enable the script by ticking the check box       
![enable](../img/admin-guide/enable.png)

5. Click `Update`

Now U2F is an available authentication mechanism for your Gluu Server. This means that, using OpenID Connect `acr_values`, applications can now request U2F authentication for users. 

!!! Note 
    To make sure U2F has been enabled successfully, you can check your Gluu Server's OpenID Connect configuration by navigating to the following URL: `https://<hostname>/.well-known/openid-configuration`. Find `"acr_values_supported":` and you should see `"u2f"`. 
    

## Make U2F the Default Authentication Mechanism

Now applications can request U2F authentication, but what if you want to make U2F your default authentication mechanism? You can follow these instructions: 

1. Navigate to `Configuration` > `Manage Authentication`. 
2. Select the `Default Authentication Method` tab. 
3. In the Default Authentication Method window you will see two options: `Default acr` and `oxTrust acr`. 

![u2f](../img/admin-guide/multi-factor/u2f.png)

- The `oxTrust acr` field controls the authentication mechanism that is presented to access the oxTrust dashboard GUI (the application you are in).    
- The `Default acr` field controls the default authentication mechanism that is presented to users from all applications that leverage your Gluu Server for authentication.    

You can change one or both fields to U2F authentication as you see fit. If you want U2F to be the default authentication mechanism for access to oxTrust (the admin portal) and all other applications that leverage your Gluu Server, change both fields to U2F.  

     

