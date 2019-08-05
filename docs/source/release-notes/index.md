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

- [#1063](https://github.com/GluuFederation/oxAuth/issues/1063) Add a config value to allow to share the same subject identifier between two Clients with the same sector identifier
- [#1047](https://github.com/GluuFederation/oxAuth/issues/1047) Add option to KeyGenerator to specify `expiration_hours`
- [#1076](https://github.com/GluuFederation/oxAuth/issues/1076) authorization.xhtml page no longer requires session

### [GluuFederation/oxTrust](https://github.com/GluuFederation/oxTrust/issues?utf8=?&q=is%3Aissue+milestone%3A3.1.7+)

- [#1646](https://github.com/GluuFederation/oxTrust/pull/1646) Add a config value to allow to share the same subject identifier between two Clients with the same sector identifier
- Removed finishlogin.xhtml

### [GluuFederation/community-edition-setup](https://github.com/GluuFederation/community-edition-setup/issues?utf8=?&q=is%3Aissue+milestone%3A3.1.7+)

- [#534](https://github.com/GluuFederation/community-edition-setup/pull/534) Add a config value to allow to share the same subject identifier between two Clients with the same sector identifier

## 3.1.7 Changes

### [GluuFederation/oxAuth](https://github.com/GluuFederation/oxAuth/issues?utf8=?&q=is%3Aissue+milestone%3A3.1.7+)

- [#1030](https://github.com/GluuFederation/oxAuth/issues/1030) Server does not track clients that take part in SSO if ACR is changed

- [#1027](https://github.com/GluuFederation/oxAuth/issues/1027) Regular expression validation should work on password expiration script

- [#1006](https://github.com/GluuFederation/oxAuth/issues/1006) oxauth-client introspection fails if it meets unknown field

- [#1005](https://github.com/GluuFederation/oxAuth/issues/1005) Issue new token if branch is not available, 2nd attempt

- [#1002](https://github.com/GluuFederation/oxAuth/issues/1002) Admin login after logging out a second time in same browser

- [#1000](https://github.com/GluuFederation/oxAuth/issues/1000) End session : enable access_token in id_token_hint

- [#998](https://github.com/GluuFederation/oxAuth/issues/998) Introspection interception script response is not returned by WS

- [#997](https://github.com/GluuFederation/oxAuth/issues/997) Support JWT token algs PS256, PS384, PS512

- [#993](https://github.com/GluuFederation/oxAuth/issues/993) Adjust passport cust script and pages to remove unnecessary endpoints

- [#992](https://github.com/GluuFederation/oxAuth/issues/992) Second logout request from another RP returns error

- [#991](https://github.com/GluuFederation/oxAuth/issues/991) Cache native objects clean up not working properly

- [#990](https://github.com/GluuFederation/oxAuth/issues/990) Protect RP initiated logout flow against top-level browsing context changing from iframe

- [#989](https://github.com/GluuFederation/oxAuth/issues/989) IdTokenFacotry has to fetch public key base on JWE algorithm

- [#988](https://github.com/GluuFederation/oxAuth/issues/988) Don't show error message about missing consent cookie at Authorization flow start

- [#987](https://github.com/GluuFederation/oxAuth/issues/987) Adjust passport script to parameterize whether updates should be applied to user profile or not

- [#986](https://github.com/GluuFederation/oxAuth/issues/986) Consent form not shown when second client starts authorization

- [#985](https://github.com/GluuFederation/oxAuth/issues/985) Load Fido2 protected device metadata

- [#984](https://github.com/GluuFederation/oxAuth/issues/984) Update session AuthZ parameters on ACR change

- [#977](https://github.com/GluuFederation/oxAuth/issues/977) Typo in otp_configuration.json

- [#901](https://github.com/GluuFederation/oxAuth/issues/901) Super Gluu created time needs time zone support

- [#589](https://github.com/GluuFederation/oxAuth/issues/589) Phone number verification message for Twilio

### [GluuFederation/oxTrust](https://github.com/GluuFederation/oxTrust/issues?utf8=?&q=is%3Aissue+milestone%3A3.1.7+)

- [#1567](https://github.com/GluuFederation/oxTrust/issues/1567) Fix system information issue on CentOS 6 and Rhel 6

- [#1566](https://github.com/GluuFederation/oxTrust/issues/1566) Use new CR method to specify if run user sync process or not on specific node

- [#1555](https://github.com/GluuFederation/oxTrust/issues/1555) Remove Generate method from SAML TR

- [#1553](https://github.com/GluuFederation/oxTrust/issues/1553) Minor UX changes for the add new client form

- [#1549](https://github.com/GluuFederation/oxTrust/issues/1549) Secret field is now editable while adding client

- [#1545](https://github.com/GluuFederation/oxTrust/issues/1545) Change Client Secret deletes client secret

- [#1543](https://github.com/GluuFederation/oxTrust/issues/1543) Adjust order and behavior of client auth settings

- [#1539](https://github.com/GluuFederation/oxTrust/issues/1539) Inactive attributes available to add in User profile page

- [#1535](https://github.com/GluuFederation/oxTrust/issues/1535) Once set, lock client ID, client name, client secret fields

- [#1529](https://github.com/GluuFederation/oxTrust/issues/1529) Create User via SCIM not returning user extended attributes

- [#1527](https://github.com/GluuFederation/oxTrust/issues/1527) Changing OpenID Client doesn't work

- [#1523](https://github.com/GluuFederation/oxTrust/issues/1523) Error during password reset

- [#1513](https://github.com/GluuFederation/oxTrust/issues/1513) 'Import people' feature can't import multiple values of single attribute

- [#1503](https://github.com/GluuFederation/oxTrust/issues/1503) Uma Scope returns "Oops" if associated OpenID client does not exist

- [#1502](https://github.com/GluuFederation/oxTrust/issues/1502) Add OP-initiated endport support

- [#1501](https://github.com/GluuFederation/oxTrust/issues/1501) Add SAML TR logout profile

- [#1496](https://github.com/GluuFederation/oxTrust/issues/1496) Fields crashing when adding new user with 'outside' attributes

- [#1495](https://github.com/GluuFederation/oxTrust/issues/1495) Add 'persistent' type NameID in oxTrust

- [#1494](https://github.com/GluuFederation/oxTrust/issues/1494) Protected Gluu endpoints

- [#1493](https://github.com/GluuFederation/oxTrust/issues/1493) Optimize users/group daily statistic calculation

- [#1491](https://github.com/GluuFederation/oxTrust/issues/1491) Wrong free memory status in Ubuntu 18

- [#1486](https://github.com/GluuFederation/oxTrust/issues/1486) Problem to add users at the first time of login

- [#1485](https://github.com/GluuFederation/oxTrust/issues/1485) NPE when removing devices in user's profile

- [#1484](https://github.com/GluuFederation/oxTrust/issues/1484) Enhance how U2F devices are displayed in user's profile

- [#1478](https://github.com/GluuFederation/oxTrust/issues/1478) Oops page when deleting user

- [#1476](https://github.com/GluuFederation/oxTrust/issues/1476) Exception when oxOTPDevices is set. Prevents user edits

- [#1474](https://github.com/GluuFederation/oxTrust/issues/1474) Issues after two successive logoffs take place

- [#1473](https://github.com/GluuFederation/oxTrust/issues/1473) Logout triggers OP unauthenticated session creation

- [#1465](https://github.com/GluuFederation/oxTrust/issues/1465) Determine factor version in order to prepare correct command option

- [#1456](https://github.com/GluuFederation/oxTrust/issues/1456) Force required permissions in jsf pages

### [GluuFederation/community-edition-setup](https://github.com/GluuFederation/community-edition-setup/issues?utf8=?&q=is%3Aissue+milestone%3A3.1.7+)

No changes

### [GluuFederation/oxshibboleth](https://github.com/GluuFederation/oxShibboleth/issues?utf8=?&3Aissue+milestone%3A3.1.7+)

- [#10](https://github.com/GluuFederation/oxShibboleth/issues/10) Support ForceAuth = true

### [GluuFederation/oxcore](https://github.com/GluuFederation/oxcore/issues?utf8=?&q=is%3Aissue+milestone%3A3.1.7+)

- [#107](https://github.com/GluuFederation/oxCore/issues/107) Log all LDAP operation times to a separate log

### [GluuFederation/gluu-passport](https://github.com/GluuFederation/gluu-passport/issues?utf8=?&q=is%3Aissue+milestone%3A3.1.7+)

No changes
