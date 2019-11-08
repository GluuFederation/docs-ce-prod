## Notice

This document, also known as the Gluu Release Note, 
relates to the Gluu Server Release versioned 3.1.7. The work is licensed under “The MIT License” 
allowing the use, copy, modify, merge, publish, distribute, sub-license and sale without 
limitation and liability. This document extends only to the aforementioned release version 
in the heading.

UNLESS IT HAS BEEN EXPRESSLY AGREED UPON BY ANY WRITTEN AGREEMENT BEFOREHAND, 
THE WORK/RELEASE IS PROVIDED “AS IS”, WITHOUT ANY WARRANTY OR GUARANTEE OF ANY KIND 
EXPRESS OR IMPLIED. UNDER NO CIRCUMSTANCE, THE AUTHOR, OR GLUU SHALL BE LIABLE FOR ANY 
CLAIMS OR DAMAGES CAUSED DIRECTLY OR INDIRECTLY TO ANY PROPERTY OR LIFE WHILE INSTALLING 
OR USING THE RELEASE.

## Purpose

The document is released with the Version 3.1.7 of the Gluu Software. The purpose of this document is to provide the changes made/new features included in this release of the Gluu Software. The list is not exhaustive and there might be some omission of negligible issues, but the noteworthy features, enhancements and fixes are covered. 

## Background

The Gluu Server is a free open source identity and access management (IAM) platform. The Gluu Server is a container distribution composed of software written by Gluu and incorporated from other open source projects. 

The most common use cases for the Gluu Server include single sign-on (SSO), mobile authentication, API access management, two-factor authentication, customer identity and access management (CIAM) and identity federation.

## Documentation

Please visit the [Gluu Documentation Page](http://www.gluu.org/docs/ce) for the complete 
documentation and administrative guide. 

## Available components in Gluu Server 3.1.7
- oxAuth, oxTrust, oxCore v3.1.7
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

## 3.1.7 Changes

### [GluuFederation/oxAuth](https://github.com/GluuFederation/oxAuth/issues?utf8=?&q=is%3Aissue+milestone%3A3.1.7+)

- [#1184](https://github.com/GluuFederation/oxAuth/issues/1184) Added proper validation of access token on /clientinfo endpoint

- [#1177](https://github.com/GluuFederation/oxAuth/issues/1177) Backport session script changes

- [#1153](https://github.com/GluuFederation/oxAuth/issues/1153) allowPostLogoutRedirectWithoutValidation oxAuth feature doesn't work

-  [#1109](https://github.com/GluuFederation/oxAuth/issues/1109) oxauth does not take care requested scopes while creating client dynamically

-  [#1088](https://github.com/GluuFederation/oxAuth/issues/1088) id_token contains wrong hash of access_token for RS512 (and possibly other algorithms)

- [#1083](https://github.com/GluuFederation/oxAuth/issues/1083) `invalidateSessionCookiesAfterAuthorizationFlow=true` leads to authorization failure

- [#1063](https://github.com/GluuFederation/oxAuth/issues/1063) Add a config value to allow to share the same subject identifier between two Clients with the same sector identifier

- [#1078](https://github.com/GluuFederation/oxAuth/issues/1078) Check expiration of JWT encoded profile used in passport flows

- [#1052](https://github.com/GluuFederation/oxAuth/issues/1052) Resource Owner Password Credential Grant Interception Script Buggy Logic

- [#1003](https://github.com/GluuFederation/oxAuth/issues/1003) Allow to refresh 'ID Token' with grant_type refresh_token

- Update jackson-databind library

- Backported ROPC flow update from CE 4.0

- Added secure flag to `org.gluu.i18n.Locale` cookie

- Disabled request host redirect to authorization page

- Set unauthenticated session state when applicaiton session script returns false

### [GluuFederation/oxTrust](https://github.com/GluuFederation/oxTrust/issues?utf8=?&q=is%3Aissue+milestone%3A3.1.7+)

- [#1646](https://github.com/GluuFederation/oxTrust/pull/1646) Add a config value to allow to share the same subject identifier between two Clients with the same sector identifier

- [#1061](https://github.com/GluuFederation/oxTrust/issues/1061) Add search box to attribute inventory

- Update jackson-databind library

- Fixed metadata validation

### [GluuFederation/oxShibboleth](https://github.com/GluuFederation/oxShibboleth/issues?utf8=?&q=is%3Aissue+milestone%3A3.1.7+)

- Update Shibboleth from 3.3.3 to 3.4.4

### [GluuFederation/community-edition-setup](https://github.com/GluuFederation/community-edition-setup/issues?utf8=?&q=is%3Aissue+milestone%3A3.1.7+)

- [#534](https://github.com/GluuFederation/community-edition-setup/pull/534) Add a config value to allow to share the same subject identifier between two Clients with the same sector identifier

- Migrate to amazon-corretto

- Update keystore creation for latest Shibboleth

