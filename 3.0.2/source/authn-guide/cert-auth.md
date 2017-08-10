# Certificate Authentication

## Overview
Certificate authentication enables you to enforce the use of a browser certificate for access to a website or application. 

This document will explain how to use Gluu's certificate authentication interception script to configure the Gluu Server for a two-step authentication process where a valid browser certificate is checked for as the first step, and username and password is presented as the second step.

## Prerequisites 
- A Gluu Server ([installation instructions](../installation-guide/index.md));
- Browser certificates or a smart card with a middleware service that bridges the browser and your smart card.

## Architecture 
The image below contains the design diagram for this module.

![cert-design](../img/admin-guide/multi-factor/cert-design.jpg)

## Properties 

The script has a few properties:

|       Property        |Description|   Allowed Values                  |example|
|-------|--------------|------------|-----------------|
|chain_cert_file_path   |mandatory property pointing to certificate chains in [pem][pem] format |file path| /etc/certs/chain_cert.pem   |
|map_user_cert          |specifies if the script should map new user to local account           |true/false| true|
|use_generic_validator  |enable/disable specific certificate validation                         |true/false| false|
|use_path_validator     |enable/disable specific certificate validation                         |true/false| true|
|use_oscp_validator|enable/disable specific certificate validation                              |true/false| false|
|use_crl_validator|enable/disable specific certificate validation                               |true/false| false|
|crl_max_response_size  |specifies the maximum allowed size of [CRL][crl] response              | Integer > 0| 2|

## Enable Certificate Authentication

To get started, log into the Gluu Server dashboard (a.k.a. oxTrust) and do the following: 

1. Navigate to `Configuration` > `Manage Custom Scripts`.
2. In the `Person Authentication` tab find the `cert` authentication module.  
3. Scroll down and find the `Enable` check box. 
4. Enable the script by clicking the check box.
5. Scroll to the bottom of the page and click `Update`. 

Now Certificate authentication is an available mechanism for your Gluu Server. This means that, using OpenID Connect `acr_values`, your applications can now request Certificate authentication for users. 

!!! Note 
    To make sure Certificate authentication has been enabled successfully, you can check your Gluu Server's OpenID Connect configuration by navigating to the following URL: `https://<hostname>/.well-known/openid-configuration`. Find `"acr_values_supported":` and you should see `"cert"`. 

## Make Certificat Authentication the Default Authentication Mechanism

Now applications can request Cert authentication, but what if you want to make Cert authentication your default mechanism? You can follow these instructions: 

1. Navigate to `Configuration` > `Manage Authentication`. 
2. Select the `Default Authentication Method` tab. 
3. In the Default Authentication Method window you will see two options: `Default acr` and `oxTrust acr`. 

- The `oxTrust acr` field controls the authentication mechanism that is presented to access the oxTrust dashboard GUI (the application you are in).    
- The `Default acr` field controls the default authentication mechanism that is presented to users from all applications that leverage your Gluu Server for authentication.    

You can change one or both fields to cert authentication as you see fit. If you want cert authentication to be the default mechanism for access to oxTrust and all other applications that leverage your Gluu Server, change both fields to cert.  

![cert](../img/admin-guide/multi-factor/cert.png)
