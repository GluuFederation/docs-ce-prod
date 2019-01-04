## Notice

This document, also known as the Gluu Release Note, 
relates to the Gluu Server Release versioned 3.1.5. The work is licensed under “The MIT License” 
allowing the use, copy, modify, merge, publish, distribute, sub-license and sale without 
limitation and liability. This document extends only to the aforementioned release version 
in the heading.

UNLESS IT HAS BEEN EXPRESSLY AGREED UPON BY ANY WRITTEN AGREEMENT BEFOREHAND, 
THE WORK/RELEASE IS PROVIDED “AS IS”, WITHOUT ANY WARRANTY OR GUARANTEE OF ANY KIND 
EXPRESS OR IMPLIED. UNDER NO CIRCUMSTANCE, THE AUTHOR, OR GLUU SHALL BE LIABLE FOR ANY 
CLAIMS OR DAMAGES CAUSED DIRECTLY OR INDIRECTLY TO ANY PROPERTY OR LIFE WHILE INSTALLING 
OR USING THE RELEASE.

## Purpose

The document is released with the Version 3.1.5 of the Gluu Software. The purpose of this document is to provide the changes made/new features included in this release of the Gluu Software. The list is not exhaustive and there might be some omission of negligible issues, but the noteworthy features, enhancements and fixes are covered. 

## Background

The Gluu Server is a free open source identity and access management (IAM) platform. The Gluu Server is a container distribution composed of software written by Gluu and incorporated from other open source projects. 

The most common use cases for the Gluu Server include single sign-on (SSO), mobile authentication, API access management, two-factor authentication, customer identity and access management (CIAM) and identity federation.

## Documentation

Please visit the [Gluu Documentation Page](http://www.gluu.org/docs/ce) for the complete 
documentation and administrative guide. 

## Available components in Gluu Server 3.1.5
- oxAuth, oxTrust, oxCore v3.1.5
- Gluu OpenLDAP v2.4.44-5
- Gluu OpenDJ v3.0
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

## Changes

### [GluuFederation/oxAuth](https://github.com/GluuFederation/oxAuth/issues?utf8=?&q=is%3Aissue+milestone%3A3.1.5+)
 
- [#954](https://github.com/GluuFederation/oxAuth/issues/954) oxauth-client now rethrows connection exceptions, so client app can handle it
- [#952](https://github.com/GluuFederation/oxAuth/issues/952) OP session is now invalidated after consent flow is completed
- [#951](https://github.com/GluuFederation/oxAuth/issues/951) Introspect endpoint now returns 200 OK with active=false if invalid token is provided
- [#948](https://github.com/GluuFederation/oxAuth/issues/948) Simplified Passport custom scripts
- [#941](https://github.com/GluuFederation/oxAuth/issues/941) Removed useless JS dependency on Super Gluu QA Page
- [#939](https://github.com/GluuFederation/oxAuth/issues/939) Improved error message and string in Twilio SMS page
- [#938](https://github.com/GluuFederation/oxAuth/issues/938) Fixed issue where a NullPointerException is often thrown during logout for some users
- [#934](https://github.com/GluuFederation/oxAuth/issues/934) Metric records are now stored in a separate backend o=metric
- [#933](https://github.com/GluuFederation/oxAuth/issues/933) Removed JCE Requirement From Gluu Server CE
- [#932](https://github.com/GluuFederation/oxAuth/issues/932) Added missing `Remember me` checkbox to some login screens
- [#930](https://github.com/GluuFederation/oxAuth/issues/930) Added support to return RPT as JWT
- [#929](https://github.com/GluuFederation/oxAuth/issues/929) Introspection endpoint now returns 200 http status code with active=false if token is not found on AS instead of 400, per spec
- [#927](https://github.com/GluuFederation/oxAuth/issues/927) oxAuth can be configured to enforce registered `post_logout_redirect_uri`
- [#925](https://github.com/GluuFederation/oxAuth/issues/925) oxAuth client log is clearer when oxAuth is not available
- [#924](https://github.com/GluuFederation/oxAuth/issues/924) ClientAuthorizations are now serializable so Redis can save them into cache.
- [#917](https://github.com/GluuFederation/oxAuth/issues/917) Added dynamic scopes and claims to discovery
- [#914](https://github.com/GluuFederation/oxAuth/issues/914) Fixed bug where all calls to oxAuth fail when httpLoggingEnabled is set to true
- [#913](https://github.com/GluuFederation/oxAuth/issues/913) RP iframe message is now handled differently than the OP iframe message, more closely aligning with spec
- [#912](https://github.com/GluuFederation/oxAuth/issues/912) Added ability to customized authentication pages logos
- [#911](https://github.com/GluuFederation/oxAuth/issues/911) Deprecated `access_token` parameter in Authorization Request
- [#906](https://github.com/GluuFederation/oxAuth/issues/906) Improved handling for session_expired, authentication_error, and user_account_disabled error codes
- [#896](https://github.com/GluuFederation/oxAuth/issues/896) Removed loginPage and authorizationPage properties
- [#883](https://github.com/GluuFederation/oxAuth/issues/883) Client expiration turned off by default, and removed ability to update expiration via endpoint
- [#876](https://github.com/GluuFederation/oxAuth/issues/876) Fixed error when providing JSON when calling .well-known/openid-configuration
- [#849](https://github.com/GluuFederation/oxAuth/issues/849) Fixed bug where if the session_id is not passed in a logout request, oxAuth incorrectly responds as if session termination succeeded
- [#830](https://github.com/GluuFederation/oxAuth/issues/830) Added client-specific access token expiration
- [#781](https://github.com/GluuFederation/oxAuth/issues/781) Added new endpoints for FIDO 2 / W3C web authentication
- [#566](https://github.com/GluuFederation/oxAuth/issues/566) Introspection endpoint now supports basic authentication
- [#230](https://github.com/GluuFederation/oxAuth/issues/230) Added Resource Owner Password Credential Grant Interception Script

### [GluuFederation/oxTrust](https://github.com/GluuFederation/oxTrust/issues?utf8=?&q=is%3Aissue+milestone%3A3.1.5+)

- [#1372](https://github.com/GluuFederation/oxTrust/issues/1372) Fixed SCIM group patch bug that occurs when member list ends up empty
- [#1371](https://github.com/GluuFederation/oxTrust/issues/1371) Email uniqueness enforcement in oxTrust is now optional
- [#1368](https://github.com/GluuFederation/oxTrust/issues/1368) Added an ID to improve UI view for QA
- [#1364](https://github.com/GluuFederation/oxTrust/issues/1364) Added a log for clean up services.
- [#1359](https://github.com/GluuFederation/oxTrust/issues/1359) Replaced list of authentication methods in oxTrust profile, when viewed by admin
- [#1356](https://github.com/GluuFederation/oxTrust/issues/1356) Require Auth Time is now False by default
- [#1348](https://github.com/GluuFederation/oxTrust/issues/1348) The OIDC `Client's Registration Expires` field is now able to be cleared
- [#1347](https://github.com/GluuFederation/oxTrust/issues/1347) The password reset email only sends to registered email address
- [#1345](https://github.com/GluuFederation/oxTrust/issues/1345) Disabling Recaptchas on Password Reminder Form now also disables them on the reset password form
- [#1344](https://github.com/GluuFederation/oxTrust/issues/1344) All user email templates are now uniform
- [#1340](https://github.com/GluuFederation/oxTrust/issues/1340) Added a `password` field for Redis cache configuration
- [#1339](https://github.com/GluuFederation/oxTrust/issues/1339) Added 'Test LDAP Connection' in Cache Refresh page
- [#1338](https://github.com/GluuFederation/oxTrust/issues/1338) Improved text Forgot Password page
- [#1329](https://github.com/GluuFederation/oxTrust/issues/1329) The correct error message now displays when a password reset token is expired 
- [#1322](https://github.com/GluuFederation/oxTrust/issues/1322) It's no longer possible to use duplicate UMA scope names
- [#1312](https://github.com/GluuFederation/oxTrust/issues/1312) Updated the 'attribute-filter.xml.vm' template
- [#1311](https://github.com/GluuFederation/oxTrust/issues/1311) Changing the oxTrust ACR to "default" in "Default Authentication Method" no longer deletes oxTrustAuthenticationMode entry
- [#1308](https://github.com/GluuFederation/oxTrust/issues/1308) Fixed a minor label error in oxTrust configuration
- [#1305](https://github.com/GluuFederation/oxTrust/issues/1305) Added a front channel logout URI
- [#1304](https://github.com/GluuFederation/oxTrust/issues/1304) oxTrust now displays available ACR options in client UI
- [#1295](https://github.com/GluuFederation/oxTrust/issues/1295) Fixed bug where OxTrust occasionally throws an error a few seconds after the first login in Docker Edition.
- [#1294](https://github.com/GluuFederation/oxTrust/issues/1294) Added a dedicated logger for Velocity's logs
- [#1293](https://github.com/GluuFederation/oxTrust/issues/1293) Long fields are now shortened by default, but expandable
- [#1292](https://github.com/GluuFederation/oxTrust/issues/1292) Redesigned OpenID Scope selection screen
- [#1286](https://github.com/GluuFederation/oxTrust/issues/1286) Fixed Cache Refresh metrics to be more accurate
- [#1285](https://github.com/GluuFederation/oxTrust/issues/1285) Fixed error where properties set via the "Configure Relying Party" control don't affect TRs based on a federation's TR
- [#1284](https://github.com/GluuFederation/oxTrust/issues/1284) Fixed client registration expiration
- [#1283](https://github.com/GluuFederation/oxTrust/issues/1283) Fixed invalid drop-down menu for the authenticationRecaptchaEnabled property in oxTrust configuration
- [#1273](https://github.com/GluuFederation/oxTrust/issues/1273) Fixed incorrect error message when accessing an incorrect URL
- [#1269](https://github.com/GluuFederation/oxTrust/issues/1269) Clarified registration result pop-up
- [#1264](https://github.com/GluuFederation/oxTrust/issues/1264) Improved design of public facing pages
- [#1262](https://github.com/GluuFederation/oxTrust/issues/1262) Improved layout of "Add/Update OIDC client" page
- [#1258](https://github.com/GluuFederation/oxTrust/issues/1258) Users can now `tab` between fields in the profile page fields
- [#1219](https://github.com/GluuFederation/oxTrust/issues/1219) Fixed issue where updating JSON Configuration switches the active tab
- [#1196](https://github.com/GluuFederation/oxTrust/issues/1196) Improved metric labels on authentication graph 
- [#1176](https://github.com/GluuFederation/oxTrust/issues/1176) You can now export client configuration as Markdown
- [#1149](https://github.com/GluuFederation/oxTrust/issues/1149) Added "uma grant" option to oxTrust OIDC client
- [#1093](https://github.com/GluuFederation/oxTrust/issues/1093) Improved oxTrust layout and element design
- [#1034](https://github.com/GluuFederation/oxTrust/issues/1034) 'Authentication Requests' graph only includes oxAuth authentication
- [#1029](https://github.com/GluuFederation/oxTrust/issues/1029) Fixed conversation_error occurring after 30 minutes of inactivity
- [#356](https://github.com/GluuFederation/oxTrust/issues/356) Improved default password reset email contents

### [GluuFederation/gluu-passport](https://github.com/GluuFederation/gluu-passport/issues?utf8=?&q=is%3Aissue+milestone%3A3.1.5+)

- [#53](https://github.com/GluuFederation/gluu-passport/issues/53) Adjusted IDP-linking URL to work with Casa social plugin
- [#49](https://github.com/GluuFederation/gluu-passport/issues/49) Removed Start.log requirement from Passport startup
- [#48](https://github.com/GluuFederation/gluu-passport/issues/48) Passport log name in archives now contains the date
- [#47](https://github.com/GluuFederation/gluu-passport/issues/47) Added logging transport for stdout
- [#29](https://github.com/GluuFederation/gluu-passport/issues/29) Implemented custom script for Passport authorization requests for Inbound SAML flow
- [#28](https://github.com/GluuFederation/gluu-passport/issues/28) AuthZ request and signed user profile are now sent as signed JWTs for Inbound SAML flow
- [#27](https://github.com/GluuFederation/gluu-passport/issues/27) Implemented SP to OIDC client mapping for Inbound SAML
- [#26](https://github.com/GluuFederation/gluu-passport/issues/26) Added endpoint to trigger Inbound SAML flow

### [GluuFederation/community-edition-setup](https://github.com/GluuFederation/community-edition-setup/issues?utf8=?&q=is%3Aissue+milestone%3A3.1.5+)

- [#498](https://github.com/GluuFederation/community-edition-setup/issues/498) The Hostname inside the chroot is no longer changed during setup
- [#497](https://github.com/GluuFederation/community-edition-setup/issues/497) Fixed init script headers for OpenDJ
- [#496](https://github.com/GluuFederation/community-edition-setup/issues/496) Casa client registration script renamed for clarity
- [#495](https://github.com/GluuFederation/community-edition-setup/issues/495) Obsolete JCE jurisdiction files are no longer downloaded
- [#492](https://github.com/GluuFederation/community-edition-setup/issues/492) SCIM UMA Resource ID is no longer hard coded
- [#488](https://github.com/GluuFederation/community-edition-setup/issues/488) Gluu Server now exports JAVA_HOME, NODE_HOME and OPENDJ_HOME and modify PATH
- [#486](https://github.com/GluuFederation/community-edition-setup/issues/486) Apache configuration formatting cleaned up
- [#485](https://github.com/GluuFederation/community-edition-setup/issues/485) setup.py now aborts if file descriptor is less than 64k

### [GluuFederation/oxCore](https://github.com/GluuFederation/oxCore/issues?utf8=?&q=is%3Aissue+milestone%3A3.1.5+)

- [#93](https://github.com/GluuFederation/oxCore/issues/93) Clarified an exception throw in oxCore
- [#91](https://github.com/GluuFederation/oxCore/issues/91) Improved the Custom script error message

### [GluuFederation/SCIM-Client](https://github.com/GluuFederation/SCIM-Client/issues?utf8=?&q=is%3Aissue+milestone%3A3.1.5+)

- [#71](https://github.com/GluuFederation/SCIM-Client/issues/71) Added parameter to revalidate after a set period of inactivity
