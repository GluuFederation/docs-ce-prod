## User Registration 
The Gluu Server is shipped with a user registration script that implements a very basic user registration process. 

In most situations, we recommend writing a custom registraton app and then using Gluu's [SCIM 2.0 endpoints](./scim2.md#supporting-a-user-registration-process-with-scim) to send the identity data to Gluu. Using SCIM will give you more control and flexibility over the registration process. Also, since oxTrust is frequently not Internet facing, the registration page (`https://<hostname>/identity/register`) may not be available to a user on the web.        

Instructions for using Gluu's user registration functionality follows: 

### Enable User Registration
To enable user registration via the Gluu Server, follow these steps:

1. Navigate to `Custom Scripts` and select the `User Registration` tab;   
2. Find the `Enabled` field and check the box;     
3. Click the `Update` button at the bottom of the page;      
4. New users will now be able to register for accounts at: `https://<hostname>/identity/register`.  

!!! Note 
    When user registration is handled via oxTrust, users can **not** be added to a backend LDAP or Active Directory server. This means that self-registration via oxTrust is only effective if users are authenticated by GluuLDAP (and not a backend LDAP or AD server).

### Adding Attributes to Registration
A limited number of attributes are present in the default registration form. If more attributes are needed they can be added via the GUI by navigating to `Organization Configuration` > `Manage Registration`. Learn how to [add attributes](../admin-guide/oxtrust-ui.md#manage-registration) to the default registration form. 

### Manual Approval of New Users
By default the `Custom property (key/value)` field will include the value: `enable_user` and `true`. This enables new users to login as soon as registration is complete. If you want to manually review and approve new user registrations, you can set this value to `false` as shown in the screenshot below.

![image](../img/admin-guide/user/config-manage-script_enable.png)
