# User Registration 

## Overview
The Gluu Server includes two custom scripts to support a self-service user registration process:

- user_registration: This script implements a very basic user registration process *without* email activation. 

- user_confirm_registration: This script adds an email activation sequence. This feature requires a working SMTP server, which can be configured by following [this doc](https://gluu.org/docs/ce/3.1.6/admin-guide/oxtrust-ui/#smtp-server-configuration). 

!!! Note
    To implement a custom registraton workflow (*recommended!*), follow the tutorial in our [SCIM 2.0 docs](./scim2.md#supporting-a-user-registration-process-with-scim).

## Enable User Registration  
To enable user registration via the Gluu Server, follow these steps:  

1. Navigate to `Manage Custom Scripts` and select the `User Registration` tab   
1. Enable the script: `user_registration`   
1. To add an email activation sequence, also enable the script: `user_confirm_registration`   
1. Click the `Update` button at the bottom of the page   
1. New users will now be able to register for accounts at: `https://<hostname>/identity/register`   

!!! Note  
    When user registration is handled via oxTrust, users **cannot** be added to a backend LDAP or Active Directory server. This means that self-registration via oxTrust is only effective if users are authenticated by Gluu's LDAP (and not a backend LDAP or AD server).  

## Adding Attributes to Registration  
A limited number of attributes are present in the default registration form. If more attributes are needed, they can be added via the GUI by navigating to `Organization Configuration` > `Manage Registration`. Learn how to [add attributes](../admin-guide/oxtrust-ui.md#manage-registration) to the default registration form.  

## Manual Approval of New Users
By default, the `Custom property (key/value)` field will include the values: `enable_user` and `true`. This enables new users to sign in as soon as registration is complete. If new users should be manually reviewed and approved, set this value to `false`.

![image](../img/admin-guide/user/config-manage-script_enable.png)  

## Enforcing Unique Email Addresses
Administrators can choose whether all email addresses should be unique. By default, uniqueness is enforced. To turn email uniqueness off, make the below changes in oxTrust and the LDAP.

!!! Warning
    If this feature is disabled, more than one user can register with the same email address. 

### oxTrust
1. Log in to the Gluu Admin UI
1. Navigate to `Configuration` > `JSON Configuration`
1. Select the `oxTrust Configuration` tab
1. Select the appropriate option in the `enforceEmailUniqueness` field
1. Save

### OpenDJ
1. Log in to the Gluu container with `service gluu-server-3.1.6 login`
1. Run this command to list all plugins:  
    `/opt/opendj/bin/dsconfig -h hostname -p 4444 -D "cn=directory manager" -w yourPassword -n list-plugins`
1. To disable the email uniqueness plugin, run this command:  
    `/opt/opendj/bin/dsconfig -h hostname -p 4444 -D "cn=directory manager" -w yourPassword -n set-plugin-prop --plugin-name "Unique mail address" --set enabled:false`
1. If you want to re-enable the email uniqueness plugin, run this command:  
    `/opt/opendj/bin/dsconfig -h hostname -p 4444 -D "cn=directory manager" -w yourPassword -n set-plugin-prop --plugin-name "Unique mail address" --set enabled:true`
1. Restart OpenDJ: service opendj restart
