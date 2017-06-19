# User Authentication Introduction
The Gluu Server is very flexible in handling authentication. By default, the Gluu Server uses username and password authentication. However, using the Gluu Server's [interception script infrastructure](../admin-guide/custom-script.md), you can define multiple authentication methods and custom business logic for complex multi-step authentication workflows. You can have multiple authentication mechanisms active at the same time--Web or mobile clients can request a certain authentication type by using standard OpenID Connect request parameters. 

Interception scripts allow you to configure authentication processes and customize how they are applied. Sophisticated authentication logic can implement adaptive authentication. For example, you can add extra authentication steps based on contextual information such as fraud scores, location, or browser profiling. You can also customize the look and feel of a web authentication: html, css, images and javascript can be externalized and managed by your organization.

## Basic Authentication

By default, LDAP is used to authenticate usernames and passwords. 
You can set a default authentication method for access to external applications, 
as well as access to the Gluu Server UI. Until additional authentication mechanisms 
are enabled via custom scripts, default authentication will always be some 
variation of username and password. 

Learn how to [configure basic authentication](./basic.md).

## Configure Social Authentication

During deployment of the Gluu Server you are presented with an option to deploy Passport.js. With over 300 existing "strategies", Passport.js provides a crowd-sourced approach to supporting social login at many popular consumer IDPs. Passport not only normalizes authentication, it also provides a standard mapping for user claims.

Learn how to [configure social login](./passport.md). 

## Configure Multi-Factor Authentication

Interception scripts are used by the Gluu Server to implement multi-factor authentication. A number of scripts are included out-of-the-box, including scripts to support FIDO U2F tokens (like Vasco and Yubikey), Gluu's free Android and iOS two-factor authentication application called Super Gluu, certificate authentication, Duo Security, One-Time Passwords, and more. 

View all pre-written Gluu Server [custom authentication scripts](https://github.com/GluuFederation/oxAuth/tree/master/Server/integrations). Implementation guides can be found in the pages that follow in this User Authentication Guide.

Organizations frequently have custom requirements for authentication. For instance, an organization may want to implement a policy that enforces two-factor authentication only for users from certain a group; or only when a user tries to access a protected resource from an unknown IP address. Custom interception scripts enable enforcement of these types of policies, as well as any other business driven policy that can be scripted. 

Review our [custom authentication script tutorial](./customauthn.md), where we demonstrate how to write a script to implement OTP authentication using Twilio to send an SMS code for a two-step out-of-band authentication mechanism. 

##  Support Multiple Authentication Mechanisms

All authentications that happen at the Gluu Server are routed through oxAuth, the software that includes Gluu's OpenID Connect Provider (OP) implementation. Using the OpenID Connect `acr_value`, an application can request a certain type of authentication at the Gluu Server. This allows you to support multiple authetication mechanisms, and allow applications to request a specific mechanism on a case-by-case basis. Learn more about the `acr_values` that are supported out-of-the-box by the Gluu Server in the [OpenID Connect docs](../admin-guide/openid-connect.md/#multi-factor-authentication-for-clients).

!!! Note
    Since all authentications are routed through oxAuth, your Gluu Server can take an incoming SAML or CAS assertion from a 3rd party IDP, for example ADFS, and use that as the basis for an OIDC session, providing seamless SSO across all your apps regardless of protocol.

## Configuring Account Lockout

The Gluu Server is shipped with a custom authentication script that implements a 
basic account lockout policy which will deactivate a users account 
after a set number of consecutive failed login attempts.

The script uses authentication settings provided in the `Manage LDAP Authentication` tab within `Configuration` > `Manage Authentication`. In case the set threshold of failed logins is reached, the “gluuStatus” attribute of the user in question will be set to `inactive` and login counter is reset to zero. The login counter will also be reset to zero if several unsuccessful login attempts are finally followed by a successful one (before exceeding the limit). You can re-enable a locked account by settings 
its `gluuStatus` attribute back to `active` via web UI.

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
