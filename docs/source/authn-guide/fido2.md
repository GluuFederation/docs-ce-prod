# FIDO2

## Overview
FIDO 2.0 Universal 2nd Factor (FIDO2 U2F) is an open authentication standard that strengthens and simplifies two-factor authentication using specialized USB or NFC devices. 

This document explains how to use the Gluu Server's included 
[FIDO2 U2F interception script](https://github.com/GluuFederation/oxAuth/blob/master/Server/integrations/fido2/Fido2ExternalAuthenticator.py) 
to implement a two-step, two-factor authentication (2FA) process with username / password as the first step, and any U2F device as the second step. 

!!! Note 
    For more background on U2F, including a discussion of its security advantages, visit the [Yubico blog](https://www.yubico.com/solutions/fido-u2f/). 

## Prerequisites
- A Gluu Server ([installation instructions](../installation-guide/index.md));      
- [FIDO2 U2F interception script](https://github.com/GluuFederation/oxAuth/blob/master/Server/integrations/fido2/Fido2ExternalAuthenticator.py) (included in the default Gluu Server distribution);     
- At least one U2F device for testing, like one of the devices [listed below](#u2f-devices). 
- For Linux-based operating systems, a little modification required in udev rule, that is stated [below](#u2f-linux).

### U2F Devices
Some well known U2F devices and manufacturers include:           

- [Yubico](https://www.yubico.com/)      
- [Vasco DIGIPASS SecureClick](https://www.vasco.com/products/two-factor-authenticators/hardware/one-button/digipass-secureclick.html)   
- [HyperFIDO](http://hyperfido.com/)       
- [Feitian Technologies](http://www.ftsafe.com/)      

[Purchase U2F devices on Amazon](https://www.amazon.com/s/ref=nb_sb_noss/146-0120855-4781335?url=search-alias%3Daps&field-keywords=u2f). Or, check [FIDO's certified products](https://fidoalliance.org/certification/fido-certified-products/) for a comprehensive list of U2F devices (sort by `Specification` == `U2F`). 

## Properties
The script has the following properties

|	Property	|	Description		|	Example	|
|-----------------------|-------------------------------|---------------|
|u2f_server_uri		|URL of the oxAuth U2F server|`https://idp.mycompany.com`|

## Enable U2F

Follow the steps below to enable U2F authentication:

1. Navigate to `Configuration` > `Manage Custom Scripts`.    

1. Click on the `Person Authentication` tab       
![person-auth](../img/admin-guide/multi-factor/person-auth.png)

1. Find the fido2 script       
![fido2-script](../img/admin-guide/multi-factor/fido2-script.png)

1. Enable the script by checking the box       
![enable](../img/admin-guide/enable.png)

1. Scroll to the bottom of the page and click `Update`

Now FIDO2 U2F is an available authentication mechanism for your Gluu Server. This means that, using OpenID Connect `acr_values`, applications can now request FIDO2 U2F authentication for users. 

!!! Note 
    To make sure FIDO2 U2F has been enabled successfully, you can check your Gluu Server's OpenID Connect 
    configuration by navigating to the following URL: `https://<hostname>/.well-known/openid-configuration`. 
    Find `"acr_values_supported":` and you should see `"fido2"`. 

## Enable FIDO2 U2F Endpoints

By default, the FIDO2 endpoints are disabled in the Gluu Server for compatibility with older versions. To activate the endpoints, follow these steps:

1. Navigate to `Configuration` > `JSON Configuration`

1. Click on the `oxAuth Configuration` tab

1. Scroll down to the Fido2 Specification

1. Set the `disable` field to `False`

1. Click the `Save Configuration` button at the bottom of the page.

## Make U2F the Default

If U2F should be the default authentication mechanism, follow these instructions: 

1. Navigate to `Configuration` > `Manage Authentication`. 

1. Select the `Default Authentication Method` tab. 

1. In the Default Authentication Method window you will see two options: `Default acr` and `oxTrust acr`. 

![u2f](../img/admin-guide/multi-factor/u2f.png)

 - `oxTrust acr` sets the authentication mechanism for accessing the oxTrust dashboard GUI (only managers should have acccess to oxTrust).    

 - `Default acr` sets the default authentication mechanism for accessing all applications that leverage your Gluu Server for authentication (unless otherwise specified).    

If FIDO2 U2F should be the default authentication mechanism for all access, change both fields to `fido2`.  

!!! Note
    If FIDO2 U2F is set as a default authentication mechanism users will **not** be able to access the protected resource(s) while using a mobile device or a browser that does not support U2F (e.g. Internet Explorer).  

## U2F Login Page
Below is an illustration of the Gluu Server's default U2F login page:

![u2f](../img/user-authn/fido2.png)

The design is being rendered from the [U2F xhtml page](https://github.com/GluuFederation/oxAuth/blob/master/Server/src/main/webapp/auth/fido2/login.xhtml). To customize the look and feel of this page, follow the [customization guide](../operation/custom-design.md). 

## Using U2F Tokens 

### Credential Enrollment
U2F device enrollment happens during the first authentication attempt. 

### Subsequent Authentications
All subsequent U2F authentications for that user account will require the enrolled U2F key. 

### U2F Credential Management
A user's FIDO2 U2F devices can be removed by a Gluu administrator in LDAP under the user entry as shown in the below screenshot. 

![fidoldap](../img/admin-guide/multi-factor/fido2-ldap-entry.png)

## U2F Discovery Endpoint
A discovery document for U2F is published by the Gluu Server at: `https://<hostname>/.well-known/fido2-configuration` This document specifies the URL of the registration and authentication endpoints.

## U2F in Linux 

From your terminal run the below commands and reboot your computer. 

  - `sudo curl https://hypersecu.com/downloads/files/configurations/70-u2f.rules > /etc/udev/rules.d/70-u2f.rules`
  - `chmod +x /etc/udev/rules.d/70-u2f.rules`
