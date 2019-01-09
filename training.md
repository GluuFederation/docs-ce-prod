# Gluu Training Curriculum 
The following is a five-day Gluu Server training curriculum. Each day's activities should take roughly four hours.  

## Day 1

 - Install Gluu Server ( latest version ) in any preferred distro. - 1 hour
 - Install OpenID Connect Resource Provider (RP) using oxd or the mod_auth_openidc web filter- 2 hours
 - Connect with Gluu Server - 30 mins
 - Test Single Sign On - 30 mins
   - You should be able to perform SSO operation for your RP which you just configured; authentication will be performed at the Gluu Server you installed. 

## Day 2

`Task completed in Day 1: A Gluu Server is ready with one RP` 

 - Configure and test one Multi factor AuthN script ( i.e. SuperGluu ) - 30 mins
 - SSO with RP through SuperGluu - 30 mins
 - Configure Cache Refresh: 3 hours
   - Set up backend LDAP server ( OpenDJ / OpenLDAP ) - 1 hour
   - Configure Cache Refresh - 2 hours

## Day 3

`Task completed in previous two days: A Gluu Server is ready with one RP + Cache Refresh working + MFA enabled`

 - Install one SAML Service Provider by Shibboleth SP - 1 hour
 - Configure Shib SP with Gluu Server for SAML SSO - 1 hour
 - Test SSO - 30 mins
 - Test Basic multi_auth script - 30 mins

## Day 4

`Task completed in previous three days: A Gluu Server is ready with OpenID + SAML protocols, Cache Refresh working, MFA enabled, user can login with multi attributes`

 - Free test drive / whatever you want to do with Gluu Server - 2 hours
 - Try to play with jython interception script to configure and map ePSA mapping - 2 hours

## Day 5

`Task completed in previous four days: A Gluu Server is ready with OpenID + SAML protocols, Cache Refresh working, MFA enabled, user can login with multi attributes. eduPersonScopedAffiliation attribute is populated`

 - Cluster - 2-4 hours. 

# Educational Resources

## Gluu Links

Gluu Docs:
http://gluu.org/docs/ce

Application integration guide:
https://gluu.org/docs/ce/integration/

Authentication guide:
https://gluu.org/docs/ce/authn-guide/intro/

Gluu Support (Register and ask here if you have any questions!):
https://support.gluu.org

Super Gluu - Free Mobile two factor authentication:
http://super.gluu.org

Gluu Github:
https://github.com/GluuFederation/


## OpenID Connect


OpenID Connect v. SAML v. OAuth 2.0
http://www.gluu.co/oauth-saml-openid

Slides from Microsoft:
http://wiki.openid.net/w/file/fetch/80030063/OpenID_Connect_Overview_May_5_2014.pdf

When to use Implicit Flow
http://www.gluu.co/implicit-flow

OpenID Connect Audiences
http://www.gluu.co/know-your-audience

New Standards Emerging for HoK Tokens:
http://gluu.co/hok-standards

Minimalist blog from Nat Sakimura:
http://nat.sakimura.org/2012/03/31/openid-connect-stripped-down-to-just-authentication

OpenID Connect Certifications:
http://oixnet.org/openid-certifications

Overview from Travis Spencer (former Ping CTO):
http://gluu.co/connect-deep-dive

OAuth 2.0 Authentication
https://oauth.net/articles/authentication/

Stop using JWT for sessions
http://gluu.co/stop-using-jwt-for-sessions

Client Software Development Slides
http://gluu.co/client-is-not-always-right

## Client Software


OXD - Client software for php, python, node, java, ruby, c#
http://oxd.gluu.org

mod_auth_openidc Apache Filter
https://github.com/zmartzone/mod_auth_openidc

NGINX OpenID plugin
https://github.com/zmartzone/lua-resty-openidc

OpenID Connect implict flow Javascript client
https://github.com/openid/AppAuth-JS
or
https://github.com/GluuFederation/openid-implicit-client
or 
https://github.com/IdentityModel/oidc-client-js

SAML SP - Apache / IIS filters
http://shibboleth.net/products/service-provider.html

## Mobile


Overview
http://gluu.co/appauth-blog

IETF Draft, Best practices for mobile SSO
https://tools.ietf.org/html/draft-wdenniss-oauth-native-apps

AppAuth: Best Practices for Native OAuth Apps
http://gluu.co/best-practices-native-oauth-slides

AppAuth iOS
https://github.com/openid/AppAuth-iOS

AppAuth Android
https://github.com/openid/AppAuth-Android

## UMA

UMA Grant Spec (for client developers)
https://docs.kantarainitiative.org/uma/wg/oauth-uma-grant-2.0-09.html

UMA Federated Authz Spec (for RS / AS developers)
https://docs.kantarainitiative.org/uma/wg/oauth-uma-federated-authz-2.0-09.html

UMA 2.0 Overview:
http:///gluu.co/uma-2-intro

Google OAuth2 Scopes
http://gluu.co/google-scopes

Gluu UMA Kong Plugin
http://getkong.org
https://github.com/GluuFederation/kong-plugins/tree/master/kong-uma-rs

