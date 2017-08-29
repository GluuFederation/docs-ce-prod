# Authentication against LDAP (AKA “Basic”, “Internal”)

## Overview
The [Basic authentication script](https://raw.githubusercontent.com/GluuFederation/oxAuth/master/Server/integrations/basic/BasicExternalAuthenticator.py) 
is used to implement username / password authentication. Basic authentication relies on a successful LDAP BIND operation against an LDAP directory--either the local LDAP included in the Gluu Server, or a backend LDAP server like Active Directory that has been configured for use with the Gluu Server via [Cache Refresh](../admin-guide/user-management.md/#ldap-synchronization). 

## Configuring Basic Authentication
Follow the steps below to configure the Basic authentication method:

1. Click on `Configuration` > `Manage authentication` 
![basic](../img/user-authn/basicauthn.png)

You can find more detailed description of each field in the
[Manage Authentication](../admin-guide/oxtrust-ui/#manage-authentication) 
section of the Gluu docs. 

Let’s only touch concepts of `primary key` and `local primary key` for now:

- Primary key: name of LDAP attribute used to look up user entries in backend LDAP directory. 

- Local primary key:  name of LDAP attribute used to look up user entries in Gluu’s 
internal LDAP directory.

!!! Note
    A primary key can also be considered a `uid` (short for: unique identifier).

## Basic Authentication Flow

Basic authentication flow can be divided into three phases:
 
1. String provided by user in the “Login” field of the login form is treated as a local key. 
It becomes a part of LDAP search filter similar to 
`&(..set of predefined filter clauses..)(local_primary_key=provided_login_name)`. 
If a user entry conforming to this filter is found in Gluu’s internal LDAP directory and 
its `gluuStatus` attribute is set to `active`, login flow continues, 
otherwise it’s deemed unsuccessful. That means that even when a backend 
directory is used for authentication, a mirrored user entry still must be present in 
Gluu’s internal directory.      

2. String provided by user in the “Login” field is now treated as a 
primary key. It becomes a part of LDAP search filter similar to 
`&(..set hardcoded clauses..)(primary_key=provided_login_name)`. 
If a user entry conforming to this filter is found in specified backend LDAP directory 
login flows continues, otherwise it’s deemed unsuccessful      

3. LDAP BIND operation is initiated against backend LDAP directory with DN 
of user entry found on step 2; for a password it will use string provided 
by user in the “Password” field of the login form. If bind results in success, 
login flow ends and user is treated as authenticated.     

## Basic Authentication Using Remote LDAP backend(s)

By default the Gluu Server is configured to use its own internal LDAP directory for authentication (as opposed to a remote LDAP backend). 

To use an external LDAP server like Active Directory instead, you need to provide the backend server's DNS name or IP address in the `Server` field. 

The login name provided by the user will be used as a search term against both the remote and internal directories, meaning there must be a strict relation between user entries in the two directories that ensures both searches will succeed. 

The simplest way to achieve this is to use the Gluu Server's Cache Refresh feature which allows the admin to set 
mappings for user attributes imported from a backend directory. Cache Refresh also allows you to customize default mapping behavior with Jython-based scripts. Learn more about [Cache Refresh](../user-management/#ldap-synchronization) in the user management portion of these docs.

