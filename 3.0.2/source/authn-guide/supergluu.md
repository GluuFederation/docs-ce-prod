# Super Gluu
## Overview
[Super Gluu](https://super.gluu.org) is a free and secure two-factor authentication mobile application developed by Gluu. 

This section of the docs explains how to enable and configure your Gluu Server to use Super Gluu for user authentication. Complete docs for Super Gluu, including a User Guide and Developer Guide, can be found on the [Super Gluu docs site](https://gluu.org/docs/supergluu). 

### FIDO U2F
During device enrollment, Super Gluu uses the Gluu Server's FIDO U2F endpoints to enroll a public key. When authentication happens, there is a challenge response to ensure that the device has the respective private key. 

Learn more about where Super Gluu entries are stored in LDAP, the Gluu Server FIDO discovery endpoint, and managing FIDO devices using SCIM in the Gluu Server [FIDO U2F docs](./U2F.md). 

### Open source 
Super Gluu is based on the free open source [oxPush 3](https://github.com/GluuFederation/oxPush3) source code. 

## Prerequisites 
- A Gluu Server ([installation instructions](../installation-guide/index.md));
- [Super Gluu interception script](https://github.com/GluuFederation/oxAuth/blob/master/Server/integrations/super_gluu/SuperGluuExternalAuthenticator.py) (included in the default Gluu Server distribution);
- An Android or iOS device with Super Gluu installed.

### Download Super Gluu
Super Gluu is available on the iOS and Android marketplaces:

- [Super Gluu for iOS](https://itunes.apple.com/us/app/super-gluu/id1093479646?mt=8)     
- [Super Gluu for Android](https://play.google.com/store/apps/details?id=gluu.org.super.gluu)     

## Properties
The Super Gluu authentication script has the following properties

|	Property	|	Description		|	Example	|
|-----------------------|-------------------------------|---------------|
|application_id		|URL of the identity server	|https://idp.example.info|
|authentication_mode	|Determine factor of authentication|two_step|
|credentials_file	|JSON file for SuperGluu 		|/etc/certs/super_gluu_creds.json| 

## Enable Super Gluu

To get started, log into the Gluu Server dashboard (a.k.a. oxTrust) and do the following: 

1. Navigate to `Configuration` > `Manage Custom Scripts`.
2. In the `Person Authentication` tab find the `super_gluu` authentication module.  
3. Scroll down and find the `Enable` check box. 
4. Enable the script by clicking the check box.
5. Scroll to the bottom of the page and click `Update`. 

Now Super Gluu is an available authentication mechanism for your Gluu Server. This means that, using OpenID Connect `acr_values`, applications can now request Super Gluu authentication for users. 

!!! Note 
    To make sure Super Gluu has been enabled successfully, you can check your Gluu Server's OpenID Connect configuration by navigating to the following URL: `https://<hostname>/.well-known/openid-configuration`. Find `"acr_values_supported":` and you should see `"super_gluu"`. 

## Make Super Gluu the Default Authentication Mechanism

Now applications can request Super Gluu authentication, but what if you want to make Super Gluu your default authentication mechanism? You can follow these instructions: 

1. Navigate to `Configuration` > `Manage Authentication`. 
2. Select the `Default Authentication Method` tab. 
3. In the Default Authentication Method window you will see two options: `Default acr` and `oxTrust acr`. 

- The `oxTrust acr` field controls the authentication mechanism that is presented to access the oxTrust dashboard GUI (the application you are in).    
- The `Default acr` field controls the default authentication mechanism that is presented to users from all applications that leverage your Gluu Server for authentication.    

You can change one or both fields to Super Gluu authentication as you see fit. If you want Super Gluu to be the default authentication mechanism for access to oxTrust and all other applications that leverage your Gluu Server, change both fields to Super Gluu.  
 
## How to register a new device? 

After Super Gluu is enabled and configured you can initiate the standard login sequence to enroll your device. After successfully entering your username and passsword you will be presented with a Super Gluu QR code. If you haven't already downloaded Super Gluu, you will now need to download the app. Once downloaded, open the app and scan the QR code.

You will be presented with an approve / deny screen. Approve the authentication, and now your device has been associated with your account in the Gluu Server. For all future authentications, you will receive a push notification to approve or deny the request. 

For more information about using Super Gluu, check the [Super Gluu User Guide](https://gluu.org/docs/supergluu/user-guide/).

## What to do about lost devices? 

In the case that someone loses their device, they will need to inform the Gluu system administrator who can do the following: 
    
  - Find the ‘DN’ of this user from ldap. 
    
  - Find the oxID ‘DN’ associated with the user
    
  - Remove the oxID DN. 

For example, let's say user ‘abc’ lost his device and wants to enroll a new device to use Super Gluu. The Gluu Server admin will do the following: 

(a) Get the DN of user ‘abc’ which will be something like this:   
`dn: inum=@!ABCD.1234.XXX.XXX.YYYY.8770,ou=people,o=@!DEFG.5678.XXX.XXX.ZZZ,o=gluu”`
 
(b) Now find the ‘oxID’ DN which is associated with this user’s DN. It might be something like: 

```
dn: oxId=1487683146561,ou=fido,inum=@!ABCD.1234.XXX.XXX.YYYY.8770,ou=people,o=@!DEFG.5678.XXX.XXX.ZZZ,o=gluu
objectClass: oxDeviceRegistration
objectClass: top
oxDeviceData: {"uuid":"b82abc-a1b2-3abc-bcccc-2222222222222","type":"normal","platform":"android","name":"zico","os_name":"kitkat","os_version":"4.4.4","push_token":"dddddddddd:aaaaaa_58_cccccc_4t_bbbbbbbbbbbbb_aaaaaaaaaaaaaa_ggggggggg"}
oxDeviceKeyHandle: fyyyyyyyyyyyyy_jaaaaaaaaaaaa_mKJw
oxStatus: active
oxApplication: https://test.gluu.org/identity/authentication/authcode
oxCounter: 2
creationDate: 20170221131906.559Z
oxId: 11111111111111111
oxDeviceRegistrationConf: {"publicKey":"BIGbwF…………….","attestationCert":"MIICJjCCAcygAwIBAgKBgQDzLA-......L5ztE"}
oxLastAccessTime: 20170
```

(c ) Delete the oxID DN. 

Now the old device is gone and the user can enroll a new device following the instructions above regarding registering a new device. 
 

