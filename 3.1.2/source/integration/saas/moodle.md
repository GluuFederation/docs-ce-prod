# SSO To Moodle
​
The doc is going to describe the process of doing SSO to Moodle based site with Gluu server as Identity Provider.
For the process we've used OpenID Connect(oidc) plugin from Office 365.

### Installing OIDC in Moodle

Before moving forward we require moole-auth_oidc package. We can clone the source code from git repo of Microsoft as below:

```
# git clone https://github.com/Microsoft/moodle-auth_oidc.git
```

Let's assume that the moodle is installed at the location: /var/www/html/moodle.yoursite.com/public_html/, then you need to move above code to auth as follows:

```
# mv  moodle-auth_oidc   /var/www/html/moodle.yoursite.com/public_html/auth/oidc

```
Login as admin to your moodle site and tehn follow the path: 

Site administration ===> Plugins ===> Authentication 

and follow rest of the on-screen instructions about database update.

Create a new client under OpenID Connect with the following specifications:

| Attribute Name     |              Values       |
|-------------------------|---------------------------------------|
| Client Name     | Your desired value|| Application Type        | Web |
| Pre-Authorization        |Enabled                        |
| Authentication method for the Token Endpoint     |   client_secret_post    |
| Redirect Login URIs   | https://<hostname>/auth/oidc/ |
| Scopes | address, email, openid, permission, phone, profile, user_name |
| Response Types | code, token, id_token |
| Grant Types | authorization_code, implicit, refresh_token |
| Logout Session Required | True |

### Configure Gluu Server as IdP in Moodle

![image](../../img/integration/Moodles_OIDC_Values.png)

The values in above image as shown are:

| OIDC Form Field Name     |              Values       |
|-------------------------|---------------------------------------|
| Provider Name | Gluu OpenID Connect |
| Client ID | Take the value from the newly created client |
| Client Secret | This too is to be taken from client created at Gluu server|| Authorization Endpoint | Take the value from https://<hostname>/.well-known/openid-configuration |
| Token Endpoint |Take the value from https://<idp-hostname>/.well-known/openid-configuration |
| Redirect URI auth_oidc | https://<hostname>/auth/oidc/ |
