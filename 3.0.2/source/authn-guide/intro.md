# User Authentication Introduction
The Gluu Server is very flexible in handling authentication. By default, the Gluu Server uses username and password authentication. However, you can can change the default authentication mechanism to a stronger mechanism, like OTP or U2F. You can also support multiple authentication mechanisms at the same time, enabling Web and mobile clients to request a certain authentication type by using standard OpenID Connect request parameters. 

## Authentication Interception Scripts
Using the Gluu Server's [interception script infrastructure](../admin-guide/custom-script.md), you can define multiple authentication methods and customize how they are applied. Sophisticated authentication logic can implement adaptive authentication. For example, you can add extra authentication steps based on contextual information such as fraud scores, location, or browser profiling. You can also customize the look and feel of a web authentication: html, css, images and javascript can be externalized and managed by your organization.

The Gluu Server ships with interception scripts for a number of authentication mechanisms, including:

- [Social Login](./passport.md) 
- [Duo Security](./duo.md)
- [U2F](./U2F.md)
- [Super Gluu](./supergluu.md)  (Gluu's free 2FA mobile app)

To review all existing authentication scripts, check the [oxAuth integration folder on GitHub](https://github.com/GluuFederation/oxAuth/tree/master/Server/integrations). The scripts can be used as is, or can be customized to implement custom functionality. 

Review our [custom authentication script tutorial](./customauthn.md), where we demonstrate how to write a script to implement OTP authentication using Twilio to send an SMS code for a two-step out-of-band authentication mechanism. 

## Basic Authentication

By default, LDAP is used to authenticate usernames and passwords. 
You can set a default authentication method for access to external applications, 
as well as access to the Gluu Server UI. Until additional authentication mechanisms 
are enabled via custom scripts, default authentication will always be some 
variation of username and password. 

Learn how to [configure basic authentication](./basic.md).

## Social Login

During deployment of the Gluu Server you are presented with an option to deploy Passport.js. With over 300 existing "strategies", Passport.js provides a crowd-sourced approach to supporting social login at many popular consumer IDPs. Passport not only normalizes authentication, it also provides a standard mapping for user claims.

Learn how to [configure social login](./passport.md). 

## Strong Authentication

The default Gluu Server distribution includes interception scripts to implement the following forms of strong authentication:

- [U2F](./U2F.md)
- [Super Gluu](./supergluu.md)  (Gluu's free 2FA mobile app)
- [Duo Security](./duo.md)
- [Certificate Authentication](./cert-auth.md)
- [OTP](./otp.md)

##  Support Multiple Authentication Mechanisms

In `Configuration` > `Manage Custom Scripts` > `Person Authentication` you can view and manage all your authentication interception scripts. To support multiple authentication mechanisms, simply check the `Enabled` box for each applicable interception script and save the page. Now, using the OpenID Connect `acr_value`, web and mobile applications can request any enabled authentication mechanisms. 

To view which authentication mechanisms are enabled at your Gluu Server, you can always check your OP URL: `https://<hostname>/.well-known/openid-configuration`. Find `"acr_values_supported"` to see a list of which `acr_values` applications can use to request a specific type of authentication. 

Learn more about `acr_values` in the [OpenID Connect core scpec](http://openid.net/specs/openid-connect-core-1_0.html#acrSemantics) and in the Gluu Server [OpenID Connect docs](../admin-guide/openid-connect.md/#multi-factor-authentication-for-clients).

!!! Note
    Since all authentications at the Gluu Server are routed through oxAuth, you can take incoming SAML or CAS assertions from a 3rd party IDP, for example ADFS, and use that as the basis for an OIDC session. This eanbles seamless SSO across all your apps regardless of protocol.

## Configuring Account Lockout

The Gluu Server is shipped with an interception script that implements a basic account lockout policy which will deactivate a users account after a set number of consecutive failed login attempts.

The script uses authentication settings provided in the `Manage LDAP Authentication` tab within `Configuration` > `Manage Authentication`. In case the set threshold of failed logins is reached, the “gluuStatus” attribute of the user in question will be set to `inactive` and login counter is reset to zero. The login counter will also be reset to zero if several unsuccessful login attempts are finally followed by a successful one (before exceeding the limit). 

You can re-enable a locked account by settings its `gluuStatus` attribute back to `active` via the web UI.

To configure this feature navigate to `Configuration` > `Manage custom scripts` and find `basic_lock` script on the `Person Authentication` tab. There are 2 configurable properties:

- `Invalid_login_count_attribute` sets the name of the attribute used to store the current amount of failed login attempts. It assumes your schema already allows such an attribute to appear in user entries. The default attribute is `oxCountInvalidLogin` and it’s already supported by Gluu’s LDAP schema.

- `Maximum_invalid_login_attemps` sets the threshold for number of failed login attempts before the user gets locked out.

![acct-update](../img/admin-guide/user/acct-lockout-config.png)

2. After script is configured tick the `Enabled` checkbox 
3. Click the `Update` button 
4. Click on `Configuration` > `Manage Authentication` on the left menu and select `Default Authentication Method` tab. 
5. Select `basic_lock` authentication method for oxAuth and/or oxTrust.
6. Click the `Update` button there.
![acct-update](../img/admin-guide/user/acct-lockout-update.png)


## Customizing the Login Page 

Learn how to customize the look and feel of Gluu Server pages in the [Design Customizations](../operation/custom-loginpage.md) section of the Operations Guide.
