# User Authentication Introduction
The Gluu Server is very flexible in handling user authentication. By default, LDAP is used for username / password authentication ("basic"). However, you can change the default mechanism to a stronger form of authentication, like One-Time Passwords (OTP) or U2F. You can also support multiple mechanisms at the same time, enabling Web and mobile clients to request a certain authentication type by using standard OpenID Connect request parameters. 

## Authentication Interception Scripts
The Gluu Server uses [interception scripts](../admin-guide/custom-script.md) to facilitate the user authentication process. For each supported authentication mechanism--like username/password ("basic"), U2F or OTP--there is a corresponding interception script that specifies how the mechanism should be applied during user sign-in. 

The Gluu Server ships with interception scripts for a number of authentication mechanisms, including:

- [Social Login](./passport.md) 
- [Duo Security](./duo.md)
- [U2F](./U2F.md)
- [Super Gluu](./supergluu.md)  (Gluu's free 2FA mobile app)

You can review all pre-written authentication scripts in the [oxAuth integration folder on GitHub](https://github.com/GluuFederation/oxAuth/tree/master/Server/integrations). 

You can also write custom scripts to support your own unique requirements for authentication. For example, you can add extra authentication steps based on contextual information such as fraud scores, location, or browser profiling via a custom authentication script.   

Follow [this tutorial](./customauthn.md) to better understand the process of writing a custom authentication script. 

## Basic Authentication

By default, LDAP is used to authenticate usernames and passwords. Passwords can either be checked in your Gluu Server's local LDAP server, or in an existing backend LDAP server if you have configured [LDAP synchronization](../user-management/ldap-sync.md). Until additional authentication scripts are enabled, default authentication will always be username and password. 

Learn how to [configure basic authentication](./basic.md).

## Social Login

During deployment of the Gluu Server you are presented with an option to include Passport.js in your installation. If you want to support social login, include Passport.js in your Gluu Server deployment. 

Passport.js provides a crowd-sourced approach to supporting social login at many popular consumer IDPs, including Facebook, LinkedIn, and GitHub. In addition to normalizing social login, Passport.js provides a standard mapping for user claims, allowing you to dynamically enroll new users into your Gluu Server that have authenticated elsewhere.

Learn how to [configure social login](./passport.md). 

## Strong Authentication

The default Gluu Server distribution includes interception scripts to implement the following forms of strong authentication:

- [U2F](./U2F.md)
- [Super Gluu](./supergluu.md)  (Gluu's free 2FA mobile app)
- [Duo Security](./duo.md)
- [Certificate Authentication](./cert-auth.md)
- [OTP](./otp.md)

## Default Authentication Mechanism
In oxTrust, you can navigate to `Configuration` > `Manage Authentication` > `Default Authentication` to specify the default authentication mechanism for two use cases: 

1. Default acr: this is the default authentication mechanism exposed to all applications that sends users to your Gluu Server for sign-in. Unless an app specifically requests a different form of authentication using the OpenID Connect `acr_value` (as specified [below](#multiple-authentication-mechanisms)), users will receive the form of authentication specified in this field. 

2. oxTrust acr: this form of authentication will be presented to anyone specifically trying to access the oxTrust admin GUI.

Depending on your requirements, you can set both fields to the same authentication mechanism, or choose a different mechanism for each use case. 

## Multiple Authentication Mechanisms
As previously mentioned, your Gluu Server can support multiple authentication mechanisms. 

In oxTrust, navigate to `Configuration` > `Manage Custom Scripts` > `Person Authentication` and check the `Enabled` box for each applicable interception script and save the page. 

By default, users will get the default authentication mechanism you specified [above](#default-authentication-mechanism) in the `Default acr` field. However, using the OpenID Connect `acr_value`, web and mobile applications can request any *enabled* authentication mechanism. 

You can enable and disable scripts in the oxTrust interface. You can also see which scripts are enabled by checking your OP configuration URL: `https://<hostname>/.well-known/openid-configuration` and look for `"acr_values_supported"`. 

Learn more about `acr_values` in the [OpenID Connect core scpec](http://openid.net/specs/openid-connect-core-1_0.html#acrSemantics) and in the Gluu Server [OpenID Connect docs](../admin-guide/openid-connect.md/#multi-factor-authentication-for-clients).

!!! Note
    All Gluu Server authentications are routed through oxAuth (the OP). You can take incoming SAML or CAS assertions from a 3rd party IDP, for example ADFS, and use that as the basis for an OpenID Connect session. This eanbles seamless SSO across all your apps.

## Account Lockout

The default Gluu Server distribution includes an interception script to implement a basic account lockout policy which will deactivate a users account after a set number of consecutive failed login attempts.

Learn how to [configure account lockout](./lockout.md). 

## Customizing the Login Page 

Learn how to customize the look and feel of Gluu Server pages in the [Design Customizations](../operation/custom-design.md) section of the Operations Guide.
