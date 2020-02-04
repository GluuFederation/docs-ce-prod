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

## Lifecycle

Status: Active Release

| Released | Community EOL | Enterprise EOL |
| --- | --- | --- |
| January 2019 | July 2020 | July 2021 |

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

- [#975](https://github.com/GluuFederation/oxAuth/issues/975) Implemented Fido2 authenticator script which based on Fido2 API

- [#969](https://github.com/GluuFederation/oxAuth/issues/969) Fix expired entries clean up

- [#968](https://github.com/GluuFederation/oxAuth/issues/968) Store missing IDP name for passport inbound

- [#966](https://github.com/GluuFederation/oxAuth/issues/966) The OTP finish button should be centered

- [#959](https://github.com/GluuFederation/oxAuth/issues/959) Authenticator should not depend on any ACR methods

- [#956](https://github.com/GluuFederation/oxAuth/issues/956) JWT(Access token as JWT) returning empty scope

- [#955](https://github.com/GluuFederation/oxAuth/issues/955) Empty scope should throw proper error ( while registering client ) instead of NPE

- [#954](https://github.com/GluuFederation/oxAuth/issues/954) oxauth-client should re-throw connection exception, so client app can handle it

- [#952](https://github.com/GluuFederation/oxAuth/issues/952) Invalidate OP session after consent flow is completed

- [#951](https://github.com/GluuFederation/oxAuth/issues/951) Introspect endpoint should return 200 OK with active=false if invalid token is provided

- [#948](https://github.com/GluuFederation/oxAuth/issues/948) Simplify passport cust scripts where possible

- [#941](https://github.com/GluuFederation/oxAuth/issues/941) Remove useless  js dependency on Super Gluu QA Page

- [#938](https://github.com/GluuFederation/oxAuth/issues/938) A NullPointerException is often throw during logout for some users

- [#934](https://github.com/GluuFederation/oxAuth/issues/934) Store metric records in separate backed o=metric

- [#933](https://github.com/GluuFederation/oxAuth/issues/933) Remove JCE Requirement From Gluu Server CE

- [#932](https://github.com/GluuFederation/oxAuth/issues/932) `Remember me` checkbox missing from login screen

- [#930](https://github.com/GluuFederation/oxAuth/issues/930) Add support to return RPT as JWT

- [#929](https://github.com/GluuFederation/oxAuth/issues/929) Introspection endpoint must return 200 http status code with active=false if token is not found on AS instead of 400

- [#927](https://github.com/GluuFederation/oxAuth/issues/927) oxAuth Does Not Enforce Registered `post_logout_redirect_uri`

- [#925](https://github.com/GluuFederation/oxAuth/issues/925) oxAuth client should log more self explanatory erorr message if oxAuth is not available

- [#924](https://github.com/GluuFederation/oxAuth/issues/924) Make ClientAuthorizations serializable otherwise redis will fail to save it into cache.

- [#917](https://github.com/GluuFederation/oxAuth/issues/917) Add dynamic scopes and claims to discovery

- [#914](https://github.com/GluuFederation/oxAuth/issues/914) All calls to oxauth fails when httpLoggingEnabled is set to true

- [#913](https://github.com/GluuFederation/oxAuth/issues/913) RP iframe Message Should Not Be Created In The Same Way As OP iframe Message

- [#912](https://github.com/GluuFederation/oxAuth/issues/912) Customized Authentication pages's logo

- [#911](https://github.com/GluuFederation/oxAuth/issues/911) Authorization Endpoint : revisit `access_token` parameter in Authorization Request

- [#906](https://github.com/GluuFederation/oxAuth/issues/906) On authentication session expiration and other errors, oxAuth should redirect user to intended RP

- [#896](https://github.com/GluuFederation/oxAuth/issues/896) Remove loginPage and authorizationPage properties

- [#883](https://github.com/GluuFederation/oxAuth/issues/883) Turn off client expiration by default and remove ability to update expiration via endpoint

- [#876](https://github.com/GluuFederation/oxAuth/issues/876) 406 from .well-known/openid-configuration

- [#868](https://github.com/GluuFederation/oxAuth/issues/868) token introspection interception script

- [#849](https://github.com/GluuFederation/oxAuth/issues/849) If session_id is not passed in logout request, oxAuth responds as if session termination succeed, while it didn't

- [#830](https://github.com/GluuFederation/oxAuth/issues/830) Client-specific access token expiration

- [#781](https://github.com/GluuFederation/oxAuth/issues/781) Add new endpoints for FIDO 2 / W3C web authentication

- [#704](https://github.com/GluuFederation/oxAuth/issues/704) Add support for Client metadata: software_id, software_version, software_statement

- [#566](https://github.com/GluuFederation/oxAuth/issues/566) Introspection endpoint: Add support for basic authentication

- [#230](https://github.com/GluuFederation/oxAuth/issues/230) Resource Owner Password Credential Grant Interception Script

### [GluuFederation/oxTrust](https://github.com/GluuFederation/oxTrust/issues?utf8=?&q=is%3Aissue+milestone%3A3.1.5+)

- [#1451](https://github.com/GluuFederation/oxTrust/issues/1451) Error in client registration form

- [#1448](https://github.com/GluuFederation/oxTrust/issues/1448) Enhancement for some views

- [#1435](https://github.com/GluuFederation/oxTrust/issues/1435) add claims - better search / pagination

- [#1434](https://github.com/GluuFederation/oxTrust/issues/1434) Regex validation of attribute leads to Error Page

- [#1428](https://github.com/GluuFederation/oxTrust/issues/1428) Password length validation not working

- [#1425](https://github.com/GluuFederation/oxTrust/issues/1425) Improve registration confirmation page

- [#1424](https://github.com/GluuFederation/oxTrust/issues/1424) Improve social  login strategy list

- [#1421](https://github.com/GluuFederation/oxTrust/issues/1421) Add ability to download a certificate from the list of cert

- [#1417](https://github.com/GluuFederation/oxTrust/issues/1417) Add more space between elements in Certificates view

- [#1412](https://github.com/GluuFederation/oxTrust/issues/1412) Error removing sector identifier when the client associated  has been deleted

- [#1409](https://github.com/GluuFederation/oxTrust/issues/1409) Typo in oxTrust Error

- [#1400](https://github.com/GluuFederation/oxTrust/issues/1400) Reorder oxTrust log level

- [#1396](https://github.com/GluuFederation/oxTrust/issues/1396) improper log level for some log lines

- [#1395](https://github.com/GluuFederation/oxTrust/issues/1395) Some error related to recaptcha.

- [#1389](https://github.com/GluuFederation/oxTrust/issues/1389) oopw while view Oxtrust Admin client details

- [#1387](https://github.com/GluuFederation/oxTrust/issues/1387) Oops when uploading ldif

- [#1386](https://github.com/GluuFederation/oxTrust/issues/1386) Errors with User addition/edition

- [#1385](https://github.com/GluuFederation/oxTrust/issues/1385) Remove "Select" from Allow for dynamic registration dropdown in Add Scope

- [#1384](https://github.com/GluuFederation/oxTrust/issues/1384) Remove "Visibility type" from Type dropdown in Add Group

- [#1382](https://github.com/GluuFederation/oxTrust/issues/1382) Add interface in user view to manage Pairwise IDs

- [#1378](https://github.com/GluuFederation/oxTrust/issues/1378) Oxtrust Admin Ui Client is delete from Clients list few hour after installation

- [#1376](https://github.com/GluuFederation/oxTrust/issues/1376) SCIM service not clearing custom attribute in LDAP using PUT or PATCH

- [#1374](https://github.com/GluuFederation/oxTrust/issues/1374) Typo in oxtrust.properties

- [#1372](https://github.com/GluuFederation/oxTrust/issues/1372) SCIM group patch anomaly when member list ends up empty

- [#1371](https://github.com/GluuFederation/oxTrust/issues/1371) Make email's uniqueness enforcement by oxTrust optional

- [#1364](https://github.com/GluuFederation/oxTrust/issues/1364) Add visibility log for clean up services.

- [#1359](https://github.com/GluuFederation/oxTrust/issues/1359) CE3.1.4: Missing Authentication Methods

- [#1347](https://github.com/GluuFederation/oxTrust/issues/1347) The password reset message should be neutral

- [#1340](https://github.com/GluuFederation/oxTrust/issues/1340) Add `password` field for Redis cache configuration

- [#1339](https://github.com/GluuFederation/oxTrust/issues/1339) 'Test LDAP Connection' in Cache Refresh page

- [#1338](https://github.com/GluuFederation/oxTrust/issues/1338) Ubuntu14+CE3.1.4: change string in Forgot Password Flow

- [#1334](https://github.com/GluuFederation/oxTrust/issues/1334) Ubuntu18+CE3.1.4: Missing Dashboard values

- [#1329](https://github.com/GluuFederation/oxTrust/issues/1329) Wrong error message when password reset token was expired

- [#1328](https://github.com/GluuFederation/oxTrust/issues/1328) Configuration > Certificates enhancements

- [#1327](https://github.com/GluuFederation/oxTrust/issues/1327) `Remember me` checkbox missing from login screens

- [#1323](https://github.com/GluuFederation/oxTrust/issues/1323) It's possible to create OIDC scopes with duplicated names in oxTrust

- [#1322](https://github.com/GluuFederation/oxTrust/issues/1322) Prevent duplicate scopes

- [#1312](https://github.com/GluuFederation/oxTrust/issues/1312) 'attribute-filter.xml.vm' template not 100% compatible in 3.1.4

- [#1311](https://github.com/GluuFederation/oxTrust/issues/1311) Changing "oxTrust acr" to "default" in "Default Authentication Method" Deletes oxTrustAuthenticationMode Entry

- [#1308](https://github.com/GluuFederation/oxTrust/issues/1308) Extra syntax / remove '222' thing

- [#1305](https://github.com/GluuFederation/oxTrust/issues/1305) oxTrust Needs To Register A Front Channel Logout URI

- [#1304](https://github.com/GluuFederation/oxTrust/issues/1304) Display available ACR options in client UI

- [#1303](https://github.com/GluuFederation/oxTrust/issues/1303) Toggle Pairwise Subject type: algorithmic | peristent

- [#1295](https://github.com/GluuFederation/oxTrust/issues/1295) OxTrust throws error few seconds after the first login.

- [#1294](https://github.com/GluuFederation/oxTrust/issues/1294) Add a dedicated logger for Velocity's logs

- [#1293](https://github.com/GluuFederation/oxTrust/issues/1293) Shorten long fields for brevity

- [#1292](https://github.com/GluuFederation/oxTrust/issues/1292) Improve OpenID Scope selection UX

- [#1286](https://github.com/GluuFederation/oxTrust/issues/1286) Cache Refresh metrics don't work as expected

- [#1285](https://github.com/GluuFederation/oxTrust/issues/1285) Properties set via "Configure Relying Party" control don't have effect on TRs based on a federation's TR

- [#1284](https://github.com/GluuFederation/oxTrust/issues/1284) Issues with "Client's registration expires" control of OIDC client's properties page

- [#1283](https://github.com/GluuFederation/oxTrust/issues/1283) authenticationRecaptchaEnabled property in oxTrust configuration has invalid drop down menu action

- [#1282](https://github.com/GluuFederation/oxTrust/issues/1282) Improve error messages when cust scripts have errors

- [#1273](https://github.com/GluuFederation/oxTrust/issues/1273) "Failed to execute registration script" when hitting a non-existing /restv1 URL

- [#1264](https://github.com/GluuFederation/oxTrust/issues/1264) Improve some public facing pages to match Gluu design

- [#1262](https://github.com/GluuFederation/oxTrust/issues/1262) Suggestion for further re-work of "Add/Update OIDC client" page

- [#1219](https://github.com/GluuFederation/oxTrust/issues/1219) Improvement : oxTrust automatically switch to another tab on update action.

- [#1196](https://github.com/GluuFederation/oxTrust/issues/1196) Authentication graph improvement

- [#1176](https://github.com/GluuFederation/oxTrust/issues/1176) Export Client Config

- [#1149](https://github.com/GluuFederation/oxTrust/issues/1149) "uma grant" option not available in oxtrust OIDC client

- [#1112](https://github.com/GluuFederation/oxTrust/issues/1112) Change menu item lbael "JSON Configuration" to "Base Configuration"

- [#1034](https://github.com/GluuFederation/oxTrust/issues/1034) 'Authentication Requests' graph should only include oxAuth authentication

- [#356](https://github.com/GluuFederation/oxTrust/issues/356) Default password reset email contents

### [GluuFederation/community-edition-setup](https://github.com/GluuFederation/community-edition-setup/issues?utf8=?&q=is%3Aissue+milestone%3A3.1.5+)

- [#503](https://github.com/GluuFederation/community-edition-setup/issues/503) Enhance oxtrus/oxAuth log level

- [#499](https://github.com/GluuFederation/community-edition-setup/issues/499) Fix Init Script Headers For Service Startup Order

- [#498](https://github.com/GluuFederation/community-edition-setup/issues/498) Why Do We Change The Hostname Inside The Chroot?

- [#497](https://github.com/GluuFederation/community-edition-setup/issues/497) OpenDJ init Script Fixes

- [#496](https://github.com/GluuFederation/community-edition-setup/issues/496) Change display name of casa client registration script

- [#495](https://github.com/GluuFederation/community-edition-setup/issues/495) Can we remove downloading oracle JCE in the installer?

- [#491](https://github.com/GluuFederation/community-edition-setup/issues/491) Enable jetty threadlimit mod if needed

- [#488](https://github.com/GluuFederation/community-edition-setup/issues/488) Gluu-server should export JAVA_HOME, NODE_HOME and OPENDJ_HOME and modify PATH

- [#486](https://github.com/GluuFederation/community-edition-setup/issues/486) Clean Up Apache Config

- [#485](https://github.com/GluuFederation/community-edition-setup/issues/485) Abort setup.py if file descriptor is less than 64k

### [GluuFederation/oxcore](https://github.com/GluuFederation/oxcore/issues?utf8=?&q=is%3Aissue+milestone%3A3.1.5+)

- [#105](https://github.com/GluuFederation/oxCore/issues/105) Increase custom script name length to 60 characters

- [#104](https://github.com/GluuFederation/oxCore/issues/104) redis with password does not work

- [#102](https://github.com/GluuFederation/oxCore/issues/102) Update UptimeConverter

- [#99](https://github.com/GluuFederation/oxCore/issues/99) Add two methods to Person type custom script

- [#96](https://github.com/GluuFederation/oxCore/issues/96) Add the field enforceEmailUniqueness to oxtrustjson configuration

- [#95](https://github.com/GluuFederation/oxCore/issues/95) Decrypt redisConfiguration password before using it for authentication

- [#93](https://github.com/GluuFederation/oxCore/issues/93) Misleading Exception throw  in oxCore

- [#91](https://github.com/GluuFederation/oxCore/issues/91) Improve Custom script error message

### [GluuFederation/SCIM-Client](https://github.com/GluuFederation/SCIM-Client/issues?utf8=?&q=is%3Aissue+milestone%3A3.1.5+)

- [#71](https://github.com/GluuFederation/SCIM-Client/issues/71) NoHttpResponseException: <server> failed to respond

### [GluuFederation/oxShibboleth](https://github.com/GluuFederation/oxShibboleth/issues?utf8=?&q=is%3Aissue+milestone%3A3.1.5+)

- [#50](https://github.com/GluuFederation/oxShibboleth/issues/50) 'SAML2Logout' Relying party configuration availability

- [#49](https://github.com/GluuFederation/oxShibboleth/issues/49) Restore previous configuration for nameid generation

### [GluuFederation/gluu-passport](https://github.com/GluuFederation/gluu-passport/issues?utf8=?&q=is%3Aissue+milestone%3A3.1.5+)

- [#55](https://github.com/GluuFederation/gluu-passport/issues/55) Passport social show empty page when the email is already register

- [#54](https://github.com/GluuFederation/gluu-passport/issues/54) Review some potential problems in passport-saml-config.json

- [#53](https://github.com/GluuFederation/gluu-passport/issues/53) Adjust IDP linking URL for casa social plugin

- [#51](https://github.com/GluuFederation/gluu-passport/issues/51) Passport service doesn't perform restart properly / Error: Received unexpected HTTP status code of 503

- [#49](https://github.com/GluuFederation/gluu-passport/issues/49) Remove Start.log Requirement From Passport Startup

- [#48](https://github.com/GluuFederation/gluu-passport/issues/48) Passport Log Should Read "passport.log" and archive as "passport-$DATE.log"

- [#47](https://github.com/GluuFederation/gluu-passport/issues/47) Add logging transport for stdout

- [#33](https://github.com/GluuFederation/gluu-passport/issues/33) Overall logging enhancements

- [#29](https://github.com/GluuFederation/gluu-passport/issues/29) IDP-inited flow for inbound identity - write custom script

- [#28](https://github.com/GluuFederation/gluu-passport/issues/28) IDP-inited flow for inbound identity - AuthZ request + signed user profile

- [#27](https://github.com/GluuFederation/gluu-passport/issues/27) IDP-inited flow for inbound identity - SP to OIDC client

- [#26](https://github.com/GluuFederation/gluu-passport/issues/26) IDP-inited flow for inbound identity - Add enpoint to trigger flow

- [#24](https://github.com/GluuFederation/gluu-passport/issues/24) Passport-Saml: IDP initiated flow fail
