## User Registration 
The Gluu Server is shipped with a user registration script that implements a very basic user registration process. 

In most situations, we recommend writing a custom registraton app and then using Gluu's [SCIM 2.0 endpoints](./scim2.md#supporting-a-user-registration-process-with-scim) to send the identity data to Gluu. Using SCIM will give you more control and flexibility over the registration process. Also, since oxTrust is frequently not Internet facing, the registration page (`https://<hostname>/identity/register`) may not be available to a user on the web.  

Instructions for using Gluu's user registration functionality follows:  

### Enable User Registration  
To enable user registration via the Gluu Server, follow these steps:  

1. Navigate to `Custom Scripts` and select the `User Registration` tab;  
1. Find the `Enabled` field and check the box;  
1. Click the `Update` button at the bottom of the page;  
1. New users will now be able to register for accounts at: `https://<hostname>/identity/register`.  

!!! Note  
    When user registration is handled via oxTrust, users **cannot** be added to a backend LDAP or Active Directory server. This means that self-registration via oxTrust is only effective if users are authenticated by Gluu's LDAP (and not a backend LDAP or AD server).  

### Adding Attributes to Registration  
A limited number of attributes are present in the default registration form. If more attributes are needed, they can be added via the GUI by navigating to `Organization Configuration` > `Manage Registration`. Learn how to [add attributes](../admin-guide/oxtrust-ui.md#manage-registration) to the default registration form.  

### Manual Approval of New Users
By default, the `Custom property (key/value)` field will include the value: `enable_user` and `true`. This enables new users to log in as soon as registration is complete. If you want to manually review and approve new user registrations, you can set this value to `false` as shown in the screenshot below.  

![image](../img/admin-guide/user/config-manage-script_enable.png)  

## Enforcing Unique Email Addresses
Administrators can choose whether they want to require all users to have unique email addresses. Uniqueness **is** enforced by default. If this feature is disabled, more than one user can register the same email address. If a password reset is requested using a shared email address, the first matching user listed in LDAP will receive the reset email.

To change this setting, you need to make the following changes in both oxTrust and the LDAP:

### oxTrust
1. Log in to the Gluu Admin UI
1. Navigate to `Configuration` > `JSON Configuration`
1. Select the `oxTrust Configuration` tab
1. Select the appropriate option in the `enforceEmailUniqueness` field
1. Save

### OpenDJ
1. Log in to the Gluu container with `service gluu-server-3.1.7 login`
1. Run this command to list all plugins:  
    `/opt/opendj/bin/dsconfig -h hostname -p 4444 -D "cn=directory manager" -w yourPassword -n list-plugins`
1. To disable the email uniqueness plugin, run this command:  
    `/opt/opendj/bin/dsconfig -h hostname -p 4444 -D "cn=directory manager" -w yourPassword -n set-plugin-prop --plugin-name "Unique mail address" --set enabled:false`
1. If you want to re-enable the email uniqueness plugin, run this command:  
    `/opt/opendj/bin/dsconfig -h hostname -p 4444 -D "cn=directory manager" -w yourPassword -n set-plugin-prop --plugin-name "Unique mail address" --set enabled:true`
1. Restart OpenDJ: service opendj restart

### OpenLDAP
1. Log in to the Gluu container with `service gluu-server-3.1.7 login`
1. Open `/opt/symas/etc/openldap/slapd.conf` in a text editor
1. To disable email uniqueness, comment out the following line:  
    `unique_uri    ldap:///?mail?sub?(objectClass=gluuPerson)`
1. If you want to re-enable email uniqueness, uncomment the above line
1. Restart the SOL Server with `service solserver restart`
