## Notice

This document, also known as the Gluu Release Note, 
relates to the Gluu Server Release versioned 3.1.4. The work is licensed under “The MIT License” 
allowing the use, copy, modify, merge, publish, distribute, sub-license and sale without 
limitation and liability. This document extends only to the aforementioned release version 
in the heading.

UNLESS IT HAS BEEN EXPRESSLY AGREED UPON BY ANY WRITTEN AGREEMENT BEFOREHAND, 
THE WORK/RELEASE IS PROVIDED “AS IS”, WITHOUT ANY WARRANTY OR GUARANTEE OF ANY KIND 
EXPRESS OR IMPLIED. UNDER NO CIRCUMSTANCE, THE AUTHOR, OR GLUU SHALL BE LIABLE FOR ANY 
CLAIMS OR DAMAGES CAUSED DIRECTLY OR INDIRECTLY TO ANY PROPERTY OR LIFE WHILE INSTALLING 
OR USING THE RELEASE.

## Purpose

The document is released with the Version 3.1.4 of the Gluu Software. The purpose of this document is to provide the changes made/new features included in this release of the Gluu Software. The list is not exhaustive and there might be some omission of negligible issues, but the noteworthy features, enhancements and fixes are covered. 

## Background

The Gluu Server is a free open source identity and access management (IAM) platform. The Gluu Server is a container distribution composed of software written by Gluu and incorporated from other open source projects. 

The most common use cases for the Gluu Server include single sign-on (SSO), mobile authentication, API access management, two-factor authentication, customer identity and access management (CIAM) and identity federation.

## Documentation

Please visit the [Gluu Documentation Page](http://www.gluu.org/docs/ce) for the complete 
documentation and administrative guide. 

## Available components in Gluu Server 3.1.4
- oxAuth, oxTrust, oxCore v3.1.4
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

## New features

## Fixes / Enhancements

### [GluuFederation/oxAuth](https://github.com/GluuFederation/oxAuth/issues?utf8=?&q=is%3Aissue+milestone%3A3.1.4+)

- [#824](https://github.com/GluuFederation/oxAuth/issues/824) UMA : Introduce separate ticket lifetime configuration
 
- [#821](https://github.com/GluuFederation/oxAuth/issues/821) Remove hardcoded code from passport page
 
- [#820](https://github.com/GluuFederation/oxAuth/issues/820) Stack trace on 'Failed to load session from LDAP'
 
- [#819](https://github.com/GluuFederation/oxAuth/issues/819) UMA 2 : restrict access to resource by associated client (make it configurable)
 
- [#817](https://github.com/GluuFederation/oxAuth/issues/817) startSession and endSession to manage application_session
 
- [#816](https://github.com/GluuFederation/oxAuth/issues/816) Review the prepareForStep method of passport social script
 
- [#812](https://github.com/GluuFederation/oxAuth/issues/812) Restrict requesting claims individually
 
- [#807](https://github.com/GluuFederation/oxAuth/issues/807) OTP 2FA / enrollment page + login page
 
- [#803](https://github.com/GluuFederation/oxAuth/issues/803) "acr_values" contains "null" in introspection endpoint's response
 
- [#802](https://github.com/GluuFederation/oxAuth/issues/802) NPE during end_session if client is expired and does not exist in LDAP anymore
 
- [#801](https://github.com/GluuFederation/oxAuth/issues/801) Getting NullPointerException whlie authorizing user
 
- [#799](https://github.com/GluuFederation/oxAuth/issues/799) If custom script getPageForStep throws error Authenticator should redirect to error page
 
- [#798](https://github.com/GluuFederation/oxAuth/issues/798) Relax log level when claims gathering script name is blank
 
- [#797](https://github.com/GluuFederation/oxAuth/issues/797) Implemented migration password script from BCRYPT to SSHA
 
- [#796](https://github.com/GluuFederation/oxAuth/issues/796) User should be redirect to error page instead of login when an exception occurs during external authentication
 
- [#791](https://github.com/GluuFederation/oxAuth/issues/791) Dynamic Registration: Minor request - add new info logger

- [#764](https://github.com/GluuFederation/oxAuth/issues/764) Create oxAuth JSON property to disable fido u2f endpoints
 
- [#753](https://github.com/GluuFederation/oxAuth/issues/753) Create Authorization Script to check BCrypt Hash
 
- [#638](https://github.com/GluuFederation/oxAuth/issues/638) Allow configuration of JWT for access token on a per client basis
 
- [#230](https://github.com/GluuFederation/oxAuth/issues/230) Resource Owner Password Credential Grant Interception Script

### [GluuFederation/oxTrust](https://github.com/GluuFederation/oxTrust/issues?utf8=?&q=is%3Aissue+milestone%3A3.1.4+)

- [#1014](https://github.com/GluuFederation/oxTrust/issues/1014) Ability to Disable Gathering Of Metrics
 
- [#1012](https://github.com/GluuFederation/oxTrust/issues/1012) The notification bubble that appears after updating the manage authentication seems a little off
 
- [#1011](https://github.com/GluuFederation/oxTrust/issues/1011) Better Button Locations in OpenID Connect Client Configuration
 
- [#1009](https://github.com/GluuFederation/oxTrust/issues/1009) The person import feature thrown error when the excel file upload has been created via a recent Excel version
 
- [#1007](https://github.com/GluuFederation/oxTrust/issues/1007) All file upload features in Gluu 3.1.3 don't works
 
- [#1002](https://github.com/GluuFederation/oxTrust/issues/1002) Adding organization logo throw an exception
 
- [#996](https://github.com/GluuFederation/oxTrust/issues/996) Log login initator exception with TRACE level only
 
- [#953](https://github.com/GluuFederation/oxTrust/issues/953) Auto-generate client secret
 
- [#952](https://github.com/GluuFederation/oxTrust/issues/952) log statements of level lower than INFO not shown after start
 
- [#703](https://github.com/GluuFederation/oxTrust/issues/703) Update OpenID Client page to support JWT access tokens
 
- [#557](https://github.com/GluuFederation/oxTrust/issues/557) Improve Passport.js user experience

### [GluuFederation/oxShibboleth](https://github.com/GluuFederation/oxShibboleth/issues?utf8=?&q=is%3Aissue+milestone%3A3.1.4+)

- [#44](https://github.com/GluuFederation/oxShibboleth/issues/44) Update Idp to V3.3.3

- [#43](https://github.com/GluuFederation/oxShibboleth/issues/43) eduPerson schema update

### [GluuFederation/gluu-passport](https://github.com/GluuFederation/gluu-passport/issues?utf8=?&q=is%3Aissue+milestone%3A3.1.4+)


- [#37](https://github.com/GluuFederation/gluu-passport/issues/37) Bundle passport with openid connect support

- [#35](https://github.com/GluuFederation/gluu-passport/issues/35) `Error in parsing JSON in getJSON` in passport log at startup

- [#33](https://github.com/GluuFederation/gluu-passport/issues/33) Overall logging enhancements

- [#32](https://github.com/GluuFederation/gluu-passport/issues/32) Make logging level a parameter in config file

- [#31](https://github.com/GluuFederation/gluu-passport/issues/31) NPE upon start when no strategies are defined

- [#18](https://github.com/GluuFederation/gluu-passport/issues/18) Passport should POST user data to /oxauth/postlogin

- [#14](https://github.com/GluuFederation/gluu-passport/issues/14) Updating certain inbound attributes showing errors in log

- [#12](https://github.com/GluuFederation/gluu-passport/issues/12) Re-attempt to get oxAuth metadata and token

- [#11](https://github.com/GluuFederation/gluu-passport/issues/11) Passport should return non zero exit code on startup errors

- [#10](https://github.com/GluuFederation/gluu-passport/issues/10) Readability of passport log

### [GluuFederation/community-edition-setup](https://github.com/GluuFederation/community-edition-setup/issues?utf8=?&q=is%3Aissue+milestone%3A3.1.4+)

- [#440](https://github.com/GluuFederation/community-edition-setup/issues/440) 2.4.x to 3.1.3 upgrade ( OpenDJ --> OpenDJ ): don't export `100-user.ldif` schema

- [#439](https://github.com/GluuFederation/community-edition-setup/issues/439) OpenLDAP enabled Gluu to OpenDJ-Gluu upgrade: ldap search filter not updating

- [#437](https://github.com/GluuFederation/community-edition-setup/issues/437) Remove '99-user.ldif' schema related calling

- [#436](https://github.com/GluuFederation/community-edition-setup/issues/436) 3.0.x to 3.1.x upgrade: metadata-provider template broken
 
- [#427](https://github.com/GluuFederation/community-edition-setup/issues/427) Asimba should be available in 3.1.4 as deprecated commmonent only

- [#425](https://github.com/GluuFederation/community-edition-setup/issues/425) Setup should prepare CE to work with dynamic IP correctly

- [#420](https://github.com/GluuFederation/community-edition-setup/issues/420) Update node passport init.d script

- [#100](https://github.com/GluuFederation/community-edition-setup/issues/100) Ensure 'hostname' is not 'localhost' by default

### [GluuFederation/SCIM-Client](https://github.com/GluuFederation/SCIM-Client/issues?utf8=?&q=is%3Aissue+milestone%3A3.1.4+)

- [#70](https://github.com/GluuFederation/SCIM-Client/issues/70) Add test cases for special chars handling

- [#69](https://github.com/GluuFederation/SCIM-Client/issues/69) Search results count isn't accurate when startindex > 1

### [GluuFederation/gluu-asimba](https://github.com/GluuFederation/gluu-asimba/issues?utf8=?&q=is%3Aissue+milestone%3A3.1.4+)
