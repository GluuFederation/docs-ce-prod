# Certificate Authentication

## Overview
Certificate authentication enables you to enforce the use of a browser certificate for access to a website or application. 

This document will explain how to use Gluu's certificate authentication interception script to configure the Gluu Server for a two-step authentication process where a valid browser certificate is checked for as the first step, and username and password is presented as the second step.

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

## Configure oxTrust

Follow the steps below to configure certificate authentication in the oxTrust Admin GUI.

1. Navigate to `Configuration` > `Manage Custom Scripts`.
2. Click on the `Person Authentication` tab.
3. Click on the `Add Custom Scritp` button.
![add-script-button](../img/admin-guide/multi-factor/add-script-button.png)
4. Fill up the from and add the [Certificate Authentication Script](https://raw.githubusercontent.com/GluuFederation/oxAuth/master/Server/integrations/cert/UserCertExternalAuthenticator.py)
5. Enable the script by ticking the check box
![enable](../img/admin-guide/enable.png)
6. Change the `Default Authentication Method` to `Cert`
![cert](../img/admin-guide/multi-factor/cert.png)
