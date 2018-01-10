# Authentication against LDAP (a.k.a “Basic” or “Internal”)

## Overview
The 'Basic' or 'Internal' method is used to implement username / password authentication.

Basic authentication relies on a successful LDAP BIND operation against an LDAP directory--either the
local LDAP included in the Gluu Server, or a backend LDAP server like Active Directory that has been configured for
use with the Gluu Server via [Cache Refresh](../user-management/ldap-sync.md).

## Prerequisites

 - Installed Gluu Server
 - [Basic authentication script](https://raw.githubusercontent.com/GluuFederation/oxAuth/master/Server/integrations/basic/BasicExternalAuthenticator.py)
 - If remote LDAP / AD server then
   - Network connectivity between Gluu Server and backend AD/LDAP
   - Remote Active Directory / LDAP bind information. 
   - Successful completion of Cache Refresh
   
## Properties
The script has the following properties: 

|	Property	|	Description		|	Example	|
|-----------------------|-------------------------------|---------------|
|Name		|Name of the authentication module		|basic|
|Description		|Description of the purpose of this script|Basic AuthN Script|
|Programming Language|Script Developed with Python|Python|
|Location type|Where this script is located inside Gluu Server|Ldap|
|Usage type|Purpose of usage|Native|
|Custom property|Customization properties|Not required by default|
|Script|The main python script|No change required by default|


## Enable 'Basic' Authentication

Basic authentication should be enabled out-of-the-box. In case it needs to be re-enabled, follow these steps: 

 1. Navitage to `Configuration` > `Manage Custom Scripts`
 1. Expand `basic` ![toolbox](../tmp/img/second_basic_authN.png)
 1. `Enabled` it
   - You can tail `oxauth_script.log` to check successful initialization of this script
```
GLUU.[root@gluu logs]# tail -f oxauth_script.log
2018-01-10 10:39:16,847 INFO  [oxAuthScheduler_Worker-5] [org.xdi.service.PythonService$PythonLoggerOutputStream] (PythonService.java:209) - Basic. Initialization
2018-01-10 10:39:16,853 INFO  [oxAuthScheduler_Worker-5] [org.xdi.service.PythonService$PythonLoggerOutputStream] (PythonService.java:209) - Basic. Initialized successfully
```
 4. Click on `Configuration` > `Manage authentication` > `Manage LDAP Authentication` tab
![basic](../tmp/img/basicauthn.png)

We can keep it as it is if we use Gluu Server as user's data source. 
For remote data source ( remote LDAP / AD ); we have to provide sufficient info such as bindDN, bindDN user password, Primary Key ( don't change local primary_key ), Server Name / IP along with port and BaseDN/s accordingly. 

!!! Note You can find more detailed description of each field in the
[Manage Authentication](../admin-guide/oxtrust-ui/#manage-authentication) 
section of the Gluu docs.


## Make 'Basic' the Default

By default, basic authentication is the default authentication method for the Gluu Server. In case it needs to be reset, follow these steps:
 
 1. Go to `Configuration` > `Manage Authentication` >  `Default Authentication Method` tab
 2. Select 'basic' for 'Default acr' and / or 'oxTrust acr' ![image](../tmp/img/second_basic_authN.png)

## Using Basic Authentication

Open up a new browser or incognito window, try to login into your Gluu Server or perform SSOn with an SP or RP. 

### Password reset in local Gluu LDAP

If passwords are stored locally, Gluu admins can reset a user's password in two ways: 

1. Using oxTrust:    
   - Navigate to `Users`> `Manage People`
   - Find the target user
   - Click the `Update Password` button at the bottom of the user record
   - Set the new password      

1. Using LDAP:    
   - Access the local LDAP following [these instructions](https://gluu.org/docs/ce/3.1.2/user-management/local-user-management/#manage-users-in-gluu-openldap)     
   - Search for user with 'uid' or 'mail' attribute    
   - Password attribute ( userPassword ) can be changed using ldapmodify commands      

### Password reset in Remote Backend Server

It's possible to reset a user's password in a Remote Backend Server, but requires configuration of a [different Authentication module](https://raw.githubusercontent.com/GluuFederation/oxAuth/master/Server/integrations/basic.change_password/BasicPassowrdUpdateExternalAuthenticator.py). 




