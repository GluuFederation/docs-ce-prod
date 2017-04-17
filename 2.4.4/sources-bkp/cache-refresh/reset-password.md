# Reset User Password
Gluu Server Community Edition comes with a password reset feature, but it is disabled by default.
This feature is available for those setups which use Gluu Server's internal LDAP as the user data source.
Any organization using their own backend LDAP/AD server will require advanced configuration using scritps and
the password reset feature.

This document shows how to setup password reset feature.

1. Enable `Self-Service Password Reset` from oxTrust `Organization Configuration` menu
![image](../img/2.4/admin_menu_configuration.png)
![image](../img/2.4/password-reset.png)

2. Configure SMTP Server from oxTrust `Organization Configuration` menu
![image](../img/2.4/admin_menu_configuration.png)
![image](../img/2.4/admin_config_smtp.png)

3. Now the password reset link will be available at `https://<hostname>/identity/person/passwordReminder.htm`
![image](../img/2.4/pass-reset.png)

4. Enter the email address and Gluu Server will send the passsword reset link via email.
![image](../img/2.4/pass-reset-email.png)

5. The email link will allow the user to set a new password.
![image](../img/2.4/new-pass.png)



