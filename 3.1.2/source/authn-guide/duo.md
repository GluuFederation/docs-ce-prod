# Duo Security
## Overview
[Duo Security](https://duosecurity.com) is a SaaS authentication provider. This document will explain how to use Gluu's [Duo interception script](https://github.com/GluuFederation/oxAuth/blob/master/Server/integrations/duo/DuoExternalAuthenticator.py) to configure the Gluu Server for a two-step authentication process with username and password as the first step, and Duo as the second step. 

In order to use this authentication mechanism your organization will need a Duo account and users will need to download the Duo mobile app. 

## Prerequisites
- A Gluu Server ([installation instructions](../installation-guide/index.md));
- [Duo interception script](https://github.com/GluuFederation/oxAuth/blob/master/Server/integrations/duo/DuoExternalAuthenticator.py) (included in the default Gluu Server distribution);
- An account with [Duo Security](https://duo.com/).   

## Properties
There are a few properties in the Duo Security authentication script:

|	Property	|Status		|	Description	|	Example		|
|-----------------------|---------------|-----------------------|-----------------------|
|duo_creds_file		|Mandatory     |Path to ikey, skey, akey|/etc/certs/duo_creds.json|
|duo_host		|Mandatory    |URL of the Duo API Server|api-random.duosecurity.com|
|audit_attribute	|Optional|Attribute to determine user group|memberOf		|
|duo_group		|Optional|Attribute to enable Duo for specific user|memberOf	|
|audit_group		|Optional|Notify administrator via email upon user login|memberOf|
|audit_group_email	|Optional|Administrator email		| admin@organization.com|

## Configure Duo Account

1. [Sign up](https://duo.com/) for a Duo account.

2. Log in to the Duo Admin Panel and navigate to Applications.

3. Click Protect an Application and locate Web SDK in the applications list. Click Protect this Application to get your integration key, secret key, and API hostname.

4. Generate an `akey` value for your instance. [Learn more](https://duo.com/docs/duoweb#1.-generate-an-akey).

For additional info on Duo's Web SDK, check [this article](https://duo.com/docs/duoweb). 

## Configure CE Chroot
1. Prepare the Duo credential file `/etc/certs/duo_creds.json` with **ikey, akey & skey**

## Configure oxTrust 

Follow the steps below to configure the Duo module in the oxTrust Admin GUI.

1. Navigate to `Configuration` > `Manage Custom Scripts`.
2. Click on the `Person Authentication` tab.
3. Scroll down to the Duo authentication script   
![duo-script](../img/admin-guide/multi-factor/duo-script.png)

4. Change the value of `duo_host` to your API    

5. Enable the script by ticking the check box    
![enable](../img/admin-guide/enable.png)

Now Duo is an available authentication mechanism for your Gluu Server. This means that, using OpenID Connect `acr_values`, applications can now request Duo authentication for users. 

!!! Note 
    To make sure Duo has been enabled successfully, you can check your Gluu Server's OpenID Connect configuration by navigating to the following URL: `https://<hostname>/.well-known/openid-configuration`. Find `"acr_values_supported":` and you should see `"duo"`. 

## Make Duo the Default Authentication Mechanism

Now applications can request Duo authentication, but what if you want to make Duo your default authentication mechanism? You can follow these instructions: 

1. Navigate to `Configuration` > `Manage Authentication`. 
2. Select the `Default Authentication Method` tab. 
3. In the Default Authentication Method window you will see two options: `Default acr` and `oxTrust acr`. 

    - The `oxTrust acr` field controls the authentication mechanism that is presented to access the oxTrust dashboard GUI (the application you are in).    
    - The `Default acr` field controls the default authentication mechanism that is presented to users from all applications that leverage your Gluu Server for authentication.    

You can change one or both fields to Duo authentication as you see fit. If you want Duo to be the default authentication mechanism for access to oxTrust and all other applications that leverage your Gluu Server, change both fields to Duo.  
 
![duo](../img/admin-guide/multi-factor/duo.png)
