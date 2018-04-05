# User Authentication Introduction
The Gluu Server was designed to be very flexible in handling user authentication. Username / password is the default form of authentication ("basic"). Stronger forms of authentication, like One-Time Passcodes (OTP), U2F Security Keys, and Gluu's free U2F mobile app, Super Gluu, can be implemented to increase account security. 

## Authentication Interception Scripts
The Gluu Server leverages [interception scripts](../admin-guide/custom-script.md) to facilitate the user authentication process. Interception scripts specify how an authentication mechanism should be applied, and what pages should be presented during sign-in. 

The Gluu Server includes interception scripts for a number of authentication mechanisms, such as:

- [FIDO U2F](./U2F.md)
- [TOTP/HOTP](./otp.md)
- [Super Gluu](./supergluu.md)  (Gluu's free 2FA mobile push app)   
- [Duo Security](./duo.md)
- [Social Login](./passport.md) 

Default authentication mechanisms can be set [as described below](#default-authentication-mechanism), and OpenID Connect clients can request any enabled authentication mechanism using the OpenID Connect `acr_value`. The name of the script in Gluu == acr_value, so for example, if an OpenID Connect client wanted users to get U2F authentication from Gluu, the client would pass the following request: `"acr_values": ["u2f"]`. 

Interception scripts included in Gluu's default distribution can be customized and extended, or new scripts can be written to support unique business requirements for authentication. For example, a script could be extendeded to implement extra authentication steps based on contextual information such as fraud scores, location, or browser profiling. 

Follow the [custom authentication script tutorial](./customauthn.md) to better understand how interception scripts work. 

!!! Note
    All pre-written authentication scripts can be found in the [oxAuth integration folder on GitHub](https://github.com/GluuFederation/oxAuth/tree/master/Server/integrations). 

## Basic Authentication

By default, usernames and passwords are stored and authenticated against the local Gluu LDAP. If [LDAP synchronization](../user-management/ldap-sync.md) has been configured, an existing backend LDAP server can be used for authentication.

Learn how to [configure basic authentication](./basic.md).

## Two-Factor Authentication (2FA)

Gluu includes interception scripts for the following forms of 2FA:

- [U2F](./U2F.md)
- [Super Gluu](./supergluu.md)  
- [OTP apps](./otp.md)
- [SMS OTP](./sms-otp.md)
- [Duo Security](./duo.md)
- [Certificate Authentication](./cert-auth.md)

Follow each link to learn how to implement that specific type of 2FA with Gluu. 

### 2FA Credential Management	
	
Once 2FA is enforced, people need a good way to enroll, delete and manage their strong credentials (that doesn't involve calling the support desk!). In an effort to make the 2FA experience better for people and organizations, the Gluu Server now supports a new open source application called [Credential Manager](https://gluu.org/docs/creds). 

Credential Manager is a simple, user-facing applications people can use to manage a variety of free or low-cost 2FA credentials in the Gluu Server. 


## Social Login

During deployment of the Gluu Server you are presented with an option to include Passport.js in your installation. If you want to support social login, include Passport.js in your Gluu Server deployment. 

Passport.js provides a crowd-sourced approach to supporting social login at many popular consumer IDPs, including Facebook, LinkedIn, and GitHub. In addition to normalizing social login, Passport.js provides a standard mapping for user claims, allowing you to dynamically enroll new users into your Gluu Server that have authenticated elsewhere.

Learn how to [configure social login](./passport.md). 

## Default Authentication Mechanism
In oxTrust, navigate to `Configuration` > `Manage Authentication` > `Default Authentication` to specify the default authentication mechanism for two use cases: 

1. Default acr: this is the default authentication mechanism exposed to all applications that sends users to your Gluu Server for sign-in. Unless an app specifically requests a different form of authentication using the OpenID Connect `acr_value` (as specified [below](#multiple-authentication-mechanisms)), users will receive the form of authentication specified in this field. 

2. oxTrust acr: this form of authentication will be presented to anyone specifically trying to access the oxTrust admin GUI.

Depending on your requirements, you can set both fields to the same authentication mechanism, or choose a different mechanism for each use case. 

## Multiple Authentication Mechanisms
The Gluu Server can concurrently support multiple authentication mechanisms, enabling Web and mobile apps ("clients") to request a specific type of authentication using the standard OpenID Connect request parameter: `acr_value`. 

In oxTrust, navigate to `Configuration` > `Manage Custom Scripts` > `Person Authentication` and check the `Enabled` box for each applicable authentication interception script. Click the `Update` button at the bottom of the page to save the changes. 

By default, users will get the default authentication mechanism as specified [above](#default-authentication-mechanism). However, using the OpenID Connect `acr_value`, web and mobile clients can request any *enabled* authentication mechanism. 

Enabled scripts can be confirmed by checking oxTrust or the Gluu OP configuration URL, `https://<hostname>/.well-known/openid-configuration`, and finding the `"acr_values_supported"`. 

Learn more about `acr_values` in the [OpenID Connect core spec](http://openid.net/specs/openid-connect-core-1_0.html#acrSemantics) and in the Gluu Server [OpenID Connect docs](../admin-guide/openid-connect/#authentication).

!!! Note
    All Gluu Server authentications are routed through oxAuth (the OP). You can take incoming SAML or CAS assertions from a 3rd party IDP, for example ADFS, and use that as the basis for an OpenID Connect session in Gluu. This enables seamless SSO across all your apps.

## Account Lockout Policy

The default Gluu Server distribution includes an interception script to implement a basic account lockout policy, which will deactivate a user's account after a set number of consecutive failed login attempts.

Learn how to [configure account lockout](./lockout.md). 

## Customizing the Login Page 

Learn how to customize the look and feel of Gluu Server login pages in the [Design Customizations](../operation/custom-design.md) section of the Operations Guide.

## Revert Authentication 

New authentication flows and methods should **always** be tested in a different browser to reduce the chance of lockout. However, in case you find yourself locked out of the GUI, refer to the [revert authentication mechanism docs](../operation/faq.md#revert-an-authentication-method). 
