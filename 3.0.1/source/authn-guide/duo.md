# Duo Security
## Overview
[Duo Security](https://duosecurity.com) is a SaaS authentication provider. This document will explain how to use Gluu's [Duo interception script](./DuoExternalAuthenticator.py) to configure the Gluu Server for a two-step authentication process with username and password as the first step, and Duo as the second step. 

In order to use this authentication mechanism your organization will need a Duo account and users will need to download the Duo mobile app. 

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

**Configure oxTrust**

Follow the steps below to configure the Duo module in the oxTrust Admin GUI.

1. Navigate to `Configuration` > `Manage Custom Scripts`.
2. Click on the `Person Authentication` tab.
3. Scroll down to the Duo authentication script   
![duo-script](../img/admin-guide/multi-factor/duo-script.png)

4. Change the value of `duo_host` to your API    

5. Enable the script by ticking the check box    
![enable](../img/admin-guide/enable.png)

6. Change the `Default authentication method` to Duo   
![duo](../img/admin-guide/multi-factor/duo.png)
