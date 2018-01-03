# Notice

This document, also known as the Gluu Release Note, 
relates to the Gluu Release versioned 3.1.2. The work is licensed under “The MIT License” 
allowing the use, copy, modify, merge, publish, distribute, sub-license and sale without 
limitation and liability. This document extends only to the aforementioned release version 
in the heading.

UNLESS IT HAS BEEN EXPRESSLY AGREED UPON BY ANY WRITTEN AGREEMENT BEFOREHAND, 
THE WORK/RELEASE IS PROVIDED “AS IS”, WITHOUT ANY WARRANTY OR GUARANTEE OF ANY KIND 
EXPRESS OR IMPLIED. UNDER NO CIRCUMSTANCE, THE AUTHOR, OR GLUU SHALL BE LIABLE FOR ANY 
CLAIMS OR DAMAGES CAUSED DIRECTLY OR INDIRECTLY TO ANY PROPERTY OR LIFE WHILE INSTALLING 
OR USING THE RELEASE.

## Overview

## Purpose

The document is released with the Version 3.1.2 of the Gluu Software. The purpose of this document is to provide the changes made/new features included in this release of the Gluu Software. The list is not exhaustive and there might be some omission of negligible issues, but the noteworthy features, enhancements and fixes are covered. 

## Background

The Gluu Server is a free open source identity and access management (IAM) platform. The Gluu Server is a container distribution composed of software written by Gluu and incorporated from other open source projects. 

The most common use cases for the Gluu Server include single sign-on (SSO), mobile authentication, API access management, two-factor authentication, customer identity and access management (CIAM) and identity federation.

## Documentation

Please visit the [Gluu Documentation Page](http://www.gluu.org/docs/ce) for the complete 
documentation and administrative guide. 

## Components included in Gluu Server CE 3.1.2
- oxAuth, oxTrust,oxCore v3.1.2
- OpenLDAP v2.4.44-5
- Shibboleth v3.2.1
- Asimba forked from v1.3.0 + v1.3.1 snapshot changes (v1.3.1 was never released)
- Passport v0.3.2
- Java v1.8.0_112
- Node.js v6.9.1
- Jetty-distribution-9.3.15.v20161220
- Jython v2.7.0
- Weld 3.0.0
- FluentD 3.5
- Redis

## What's new in version 3.1.2

### New features

- [Make implicit flow configurable and persist all related objects into cache (no ldap at all)](https://github.com/GluuFederation/oxAuth/issues/658)

- [Dynamic OpenID Authz script](https://github.com/GluuFederation/oxAuth/issues/679) 

- [Updated default Super Gluu web pages](https://github.com/GluuFederation/oxTrust/issues/717)   

- [Inbound SAML SSO via passport.js](https://github.com/GluuFederation/Inbound-SAML-Demo/wiki/Readme_single)   

- [UMA 2 : Allow access token for authentication at UMA token endpoint](https://github.com/GluuFederation/oxAuth/issues/686)

- [UMA 2 : support "and", "or" logical operations for scopes (including nested)](https://github.com/GluuFederation/oxAuth/issues/688)

### Fixes

#### [oxAuth](https://github.com/GluuFederation/oxAuth/issues?q=is%3Aopen+is%3Aissue+milestone%3A3.1.2)

- [Create new JWK for use=enc for Client and Server tests #699](https://github.com/GluuFederation/oxAuth/issues/699)

- [Invalid "scopes" field in Dynamic Client Registration request and response #700](https://github.com/GluuFederation/oxAuth/issues/700#issuecomment-346950251)

- [Encode/decode client_id/secret separately in basic auth](https://github.com/GluuFederation/oxAuth/issues/677)

- [Fix Password Expiration authentication script](https://github.com/GluuFederation/oxAuth/issues/661)

- [Introspection API Docs: Missing Response](https://github.com/GluuFederation/oxAuth/issues/391)

- [Add support for encrypting Request Objects sent to the OP #91](https://github.com/GluuFederation/oxAuth/issues/91)

- [No support for "popup" value of "display" request parameter #574](https://github.com/GluuFederation/oxAuth/issues/574)

- [Performance improvements #691](https://github.com/GluuFederation/oxAuth/issues/691)

- [OIDC returning arrays incorrectly](https://github.com/GluuFederation/oxAuth/issues/600)

- [Introspection response `exp` field must return value in seconds](https://github.com/GluuFederation/oxAuth/issues/696)

- [Introspection : add `sub` field value to introspection response](https://github.com/GluuFederation/oxAuth/issues/695)

- [UMA 2 : requested scope is not returned in permissions of RPT introspection](https://github.com/GluuFederation/oxAuth/issues/689)

- [Failed to update oxLastLogonTime of user X" error message #685](https://github.com/GluuFederation/oxAuth/issues/685)

- [Multi-Step OpenID Connect AuthZ Script](https://github.com/GluuFederation/oxAuth/issues/679)

- [Don't override OC specified in custom script](https://github.com/GluuFederation/oxAuth/issues/681)

- [Restore parameters from session automatically](https://github.com/GluuFederation/oxAuth/issues/675)

- [OIDC authorization page throws an error](https://github.com/GluuFederation/oxAuth/issues/672)

- [Only first value of multi-valued claim is returned in id_token](https://github.com/GluuFederation/oxAuth/issues/670)

- [Log denied Dynamic Client Registration Requests at INFO level](https://github.com/GluuFederation/oxAuth/issues/668)

- [Improve oxAuth authz checking mechanism](https://github.com/GluuFederation/oxAuth/issues/662)

- [External authN not working in 3.1.1beta2](https://github.com/GluuFederation/oxAuth/issues/659)

- [NPE when requesting authorization with acr param](https://github.com/GluuFederation/oxAuth/issues/653)

- [Support Custom Params](https://github.com/GluuFederation/oxAuth/issues/647)

- [basic_multi_auth not working](https://github.com/GluuFederation/oxAuth/issues/632)

- [Call instance<T>.destroy on manually created object on destroy](https://github.com/GluuFederation/oxAuth/issues/584)

- [SuperGluu Script: add link to download app](https://github.com/GluuFederation/oxAuth/issues/479)

- [UMA RPT policy script for SCIM crashes](https://github.com/GluuFederation/oxAuth/issues/692)

- [UMA 2 : requested scope must be validated per client (not system wide)](https://github.com/GluuFederation/oxAuth/issues/690)

- [UMA 2 : Allow access token for authentication at UMA token endpoint](https://github.com/GluuFederation/oxAuth/issues/686)

- [Test coverage for multi-step authz flows](https://github.com/GluuFederation/oxAuth/issues/684)

- [Make implicit flow configurable and persist all related objects into cache (no ldap at all)](https://github.com/GluuFederation/oxAuth/issues/658)

#### [oxTrust](https://github.com/GluuFederation/oxTrust/issues?q=is%3Aopen+is%3Aissue+milestone%3A3.1.2)
- [Activate/Deactive LDAP server feature of "Manage authentication" page is broken](https://github.com/GluuFederation/oxTrust/issues/789)

- [On profile update applciation should call update person custom script](https://github.com/GluuFederation/oxTrust/issues/780)

- [Add post add/update/delete methods to update user script](https://github.com/GluuFederation/oxTrust/issues/779)

- [oxTrust cannot create "userCertificate"](https://github.com/GluuFederation/oxTrust/issues/751)

- [UMA Scope is not editable after image upload](https://github.com/GluuFederation/oxTrust/issues/770)

- [Add new default designs for U2F, OTP, and SMS OTP auth pages](https://github.com/GluuFederation/oxTrust/issues/767)

- [Errors thrown before redirected to oxAuth login page #737](https://github.com/GluuFederation/oxTrust/issues/737)

- [VTL identifier wrong in Shibboleth velocity templates](https://github.com/GluuFederation/oxTrust/issues/761)

- ["JSON configuration -> oxTrust" page/tab contains field no longer being used](https://github.com/GluuFederation/oxTrust/issues/759)

- [Fix User status value when using User Import with xls file](https://github.com/GluuFederation/oxTrust/issues/757)

- [Fix Incorrect Label on email address field in Manage People screen](https://github.com/GluuFederation/oxTrust/issues/756)

- [Remote IDP's certificate (Asimba flows' settings) is not being imported](https://github.com/GluuFederation/oxTrust/issues/755)

- [Unable to add attributes via Attributes Filter](https://github.com/GluuFederation/oxTrust/issues/754)

- [Fix screen display for large attributes in "Update Users" screen](https://github.com/GluuFederation/oxTrust/issues/753)

- [Unable to delete created attributes](https://github.com/GluuFederation/oxTrust/issues/750)

- [Mail Sent from Gluu Server is in text format](https://github.com/GluuFederation/oxTrust/issues/746)

- [No option to clear an OIDC client's setting if it was already set to some value explicitly using a drop-down list](https://github.com/GluuFederation/oxTrust/issues/745)

- [Submenus do not open and close](https://github.com/GluuFederation/oxTrust/issues/744)

- [no build date and number](https://github.com/GluuFederation/oxTrust/issues/743)

- [Extend Authentication Script to support GUI representation](https://github.com/GluuFederation/oxTrust/issues/741)

- [Cache Provider Configuration settings fix](https://github.com/GluuFederation/oxTrust/issues/723)

- [Add option to mail configuration to enable implicit trust to host mail server](https://github.com/GluuFederation/oxTrust/issues/629)

- [show u2f creds in user page](https://github.com/GluuFederation/oxTrust/issues/604)

- [Register page is not working](https://github.com/GluuFederation/oxTrust/issues/599)

- [MAX_COUNT in SCIM Client negative test cases](https://github.com/GluuFederation/oxTrust/issues/536)

- [SCIM 2.0 Missing access token in test mode causes unhandled exception](https://github.com/GluuFederation/oxTrust/issues/404)

- [Question on error / oxTrust - "Can't perform redirect to viewId: /error"](https://github.com/GluuFederation/oxTrust/issues/765)

- [Super Gluu Enroll + Subsequent Auths page](https://github.com/GluuFederation/oxTrust/issues/717)

- [Images in developer setup are too small](https://github.com/GluuFederation/oxTrust/issues/633)

#### [Community Edition Setup](https://github.com/GluuFederation/community-edition-setup/issues?q=is%3Aopen+is%3Aissue+milestone%3A3.1.2)

- In setup.py allow selection of LDAP server #[393](https://github.com/GluuFederation/community-edition-setup/issues/393)

- [Don't allow to run setup.py after installation #30](https://github.com/GluuFederation/community-edition-setup/issues/30)

- [#367 | Upgrade: `openIdClientPassword` changing in 'oxidp' configuration bug](https://github.com/GluuFederation/community-edition-setup/issues/367)

- [#366 | Upgrade: permission of Shibboleth configuration bug](https://github.com/GluuFederation/community-edition-setup/issues/366)

- [#350 | Wrong directory in gluu-server uninstall notification](https://github.com/GluuFederation/community-edition-setup/issues/350)

- [Setup.py re-prompt for IP address upon invalid entry](https://github.com/GluuFederation/community-edition-setup/issues/352)

- [Stopping Gluu Server does not stop memcached in 3.1](https://github.com/GluuFederation/community-edition-setup/issues/345)

- [Failed to start rsyslog in RHEL 7.2](https://github.com/GluuFederation/community-edition-setup/issues/273)

- [IdP starts prior to OpenLDAP in Xenial](https://github.com/GluuFederation/community-edition-setup/issues/371)

- [Upgrade: 2.4.4 export script not working](https://github.com/GluuFederation/community-edition-setup/issues/363)

- [Cron jobs don't start inside of the container of 2.4.3 CE deb packages](https://github.com/GluuFederation/community-edition-setup/issues/134)

#### [gluu-Asimba](https://github.com/GluuFederation/gluu-asimba/issues?q=is%3Aopen+is%3Aissue+milestone%3A3.1.2)

- [An Asimba setting which controls the number of seconds after which Asimba refuses authentication based on AuthInstant](https://github.com/GluuFederation/gluu-Asimba/issues/44)

- [Asimba Script's reaction for AuthnFailed message from Asimba](https://github.com/GluuFederation/gluu-Asimba/issues/43)

#### [Gluu Passport](https://github.com/GluuFederation/gluu-passport/issues?q=is%3Aopen+is%3Aissue+milestone%3A3.1.2)

- [Support other SAML params #6](https://github.com/GluuFederation/gluu-passport/issues/6)

- [Support SAML response encryption #5](https://github.com/GluuFederation/gluu-passport/issues/5)

- [Controls the number of seconds after which Passport refuses authentication #7](https://github.com/GluuFederation/gluu-passport/issues/7)

#### [oxCore](https://github.com/GluuFederation/oxCore/issues?q=is%3Aopen+is%3Aissue+milestone%3A3.1.2)

- [Redis : avoid NPE if key is null](https://github.com/GluuFederation/oxCore/issues/56)

- [Use same connection in count method](https://github.com/GluuFederation/oxCore/issues/59)

#### [SCIM Client](https://github.com/GluuFederation/SCIM-client/issues?q=is%3Aopen+is%3Aissue+milestone%3A3.1.2)

- [Deserialization of custom attributes not taking place in client-side](https://github.com/GluuFederation/SCIM-Client/issues/55)
