# User Authentication Introduction
The Gluu Server is very flexible in handling user authentication. By default, either the Gluu Server's local LDAP, or an organization's backend LDAP (depending on where passwords are stored), is used for username / password authentication ("basic"). 

Stronger forms of authentication like One-Time Passwords (OTP), U2F Security Keys, and Gluu's free U2F mobile app, Super Gluu, can be implemented to increase the security of logins. In addition, the Gluu Server can support multiple mechanisms at the same time, enabling Web and mobile apps ("clients") to request a specific authentication type by using standard OpenID Connect request parameters. 

## Authentication Interception Scripts
The Gluu Server leverages [interception scripts](../admin-guide/custom-script.md) to facilitate the user authentication process. For each supported authentication mechanism--like username/password ("basic"), U2F or OTP--there is a corresponding interception script that specifies how the mechanism should be applied during user sign-in. 

The Gluu Server ships with interception scripts for a number of authentication mechanisms, such as:

- [FIDO U2F](./U2F.md)
- [Super Gluu](./supergluu.md)  (Gluu's free 2FA mobile app)
- [Social Login](./passport.md) 
- [Duo Security](./duo.md)

All pre-written authentication scripts can be viewed in the [oxAuth integration folder on GitHub](https://github.com/GluuFederation/oxAuth/tree/master/Server/integrations). 

Custom scripts can also be written to support unique requirements for authentication. For example, a custom script could be written to implement extra authentication steps based on contextual information such as fraud scores, location, or browser profiling. 

Follow the [custom authentication script tutorial](./customauthn.md) to better understand the process of writing your own interception scripts. 

## Basic Authentication

By default, LDAP is used to authenticate usernames and passwords. Passwords can either be authenticated in the Gluu Server's local LDAP server, or, if [LDAP synchronization](../user-management/ldap-sync.md) has been configured, in an existing backend LDAP server. Until additional authentication scripts are enabled, default authentication will always be username and password. 

Learn how to [configure basic authentication](./basic.md).

## Two-Factor Authentication (2FA)

The default Gluu Server distribution includes interception scripts that implement the following forms of two-factor authentication:

- [U2F](./U2F.md)
- [Super Gluu](./supergluu.md)  (Gluu's free 2FA mobile app)=
- [OTP apps](./otp.md)
- [SMS OTP](./sms-otp.md)
- [Duo Security](./duo.md)
- [Certificate Authentication](./cert-auth.md)

Follow each link to learn how to implement that specific type of 2FA with Gluu. 

### 2FA Credential Management

Enabling users to manage and enroll 2FA credentials without undermining the security model is one of the most important things to consider when rolling out 2FA. 

Regardless of 2FA type or vendor, users need a secure way to enroll and delete their 2FA credentials.

By default, the Gluu Server allows each user to enroll just one (1) strong credential per 2FA credential type. For instance, if authentication is set to U2F, by default the user can only enroll one U2F security key. Same for OTP, Super Gluu, etc. The credential is enrolled upon the first authentication attempt, and can be used to pass all subsequent prompts for 2FA. Behavior can be customized via interception scripts and custom development. 
 
Information about managing specific types of credentials can be found in the corresponding document in this Authentication Guide. 

## Social Login

During deployment of the Gluu Server you are presented with an option to include Passport.js in your installation. If you want to support social login, include Passport.js in your Gluu Server deployment. 

Passport.js provides a crowd-sourced approach to supporting social login at many popular consumer IDPs, including Facebook, LinkedIn, and GitHub. In addition to normalizing social login, Passport.js provides a standard mapping for user claims, allowing you to dynamically enroll new users into your Gluu Server that have authenticated elsewhere.

Learn how to [configure social login](./passport.md). 

## Default Authentication Mechanism
In oxTrust, you can navigate to `Configuration` > `Manage Authentication` > `Default Authentication` to specify the default authentication mechanism for two use cases: 

1. Default acr: this is the default authentication mechanism exposed to all applications that sends users to your Gluu Server for sign-in. Unless an app specifically requests a different form of authentication using the OpenID Connect `acr_value` (as specified [below](#multiple-authentication-mechanisms)), users will receive the form of authentication specified in this field. 

2. oxTrust acr: this form of authentication will be presented to anyone specifically trying to access the oxTrust admin GUI.

Depending on your requirements, you can set both fields to the same authentication mechanism, or choose a different mechanism for each use case. 

## Multiple Authentication Mechanisms
As previously mentioned, the Gluu Server can concurrently support multiple authentication mechanisms. 

In oxTrust, navigate to `Configuration` > `Manage Custom Scripts` > `Person Authentication` and check the `Enabled` box for each applicable interception script. Click the update button at the bottom of the page to save your changes. 

By default, users will get the default authentication mechanism as specified [above](#default-authentication-mechanism). However, using the OpenID Connect `acr_value`, web and mobile clients can request any *enabled* authentication mechanism. 

Authentication scripts can be enabled and disabled in the oxTrust interface. Enabled scripts can also be confirmed by checking the OP configuration URL, `https://<hostname>/.well-known/openid-configuration`, and finding the `"acr_values_supported"`. 

Learn more about `acr_values` in the [OpenID Connect core scpec](http://openid.net/specs/openid-connect-core-1_0.html#acrSemantics) and in the Gluu Server [OpenID Connect docs](../admin-guide/openid-connect.md/#multi-factor-authentication-for-clients).

!!! Note
    All Gluu Server authentications are routed through oxAuth (the OP). You can take incoming SAML or CAS assertions from a 3rd party IDP, for example ADFS, and use that as the basis for an OpenID Connect session in Gluu. This enables seamless SSO across all your apps.

## Account Lockout Policy

The default Gluu Server distribution includes an interception script to implement a basic account lockout policy which will deactivate a users account after a set number of consecutive failed login attempts.

Learn how to [configure account lockout](./lockout.md). 

## Customizing the Login Page 

Learn how to customize the look and feel of Gluu Server login pages in the [Design Customizations](../operation/custom-design.md) section of the Operations Guide.

## Revert authentication 

You should always test new authentication flows and methods in a different browser to reduce the chance of lockout. However, in case you find yourself locked out, refer to the [revert authentication mechanism docs](../operation/faq.md#revert-an-authentication-method). 
