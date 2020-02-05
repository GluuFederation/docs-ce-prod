# Release Notes

## Notice

This document, also known as the Gluu Release Note, 
relates to the Gluu Server Release versioned 4.1. The work is licensed under “The MIT License” 
allowing the use, copy, modify, merge, publish, distribute, sub-license and sale without 
limitation and liability. This document extends only to the aforementioned release version 
in the heading.

UNLESS IT HAS BEEN EXPRESSLY AGREED UPON BY ANY WRITTEN AGREEMENT BEFOREHAND, 
THE WORK/RELEASE IS PROVIDED “AS IS”, WITHOUT ANY WARRANTY OR GUARANTEE OF ANY KIND 
EXPRESS OR IMPLIED. UNDER NO CIRCUMSTANCE, THE AUTHOR, OR GLUU SHALL BE LIABLE FOR ANY 
CLAIMS OR DAMAGES CAUSED DIRECTLY OR INDIRECTLY TO ANY PROPERTY OR LIFE WHILE INSTALLING 
OR USING THE RELEASE.

## Lifecycle

Status: In Development

| Released | Community EOL | Enterprise EOL |
| --- | --- | --- |
| Upcoming | TBD | TBD |

## Purpose

The document is released with the Version 4.1 of the Gluu Software. The purpose of this document is to provide the changes made/new features included in this release of the Gluu Software. The list is not exhaustive and there might be some omission of negligible issues, but the noteworthy features, enhancements and fixes are covered. 

## Background

The Gluu Server is a free open source identity and access management (IAM) platform. The Gluu Server is a container distribution composed of software written by Gluu and incorporated from other open source projects. 

The most common use cases for the Gluu Server include single sign-on (SSO), mobile authentication, API access management, two-factor authentication, customer identity and access management (CIAM) and identity federation.

## Documentation

Please visit the [Gluu Documentation Page](http://www.gluu.org/docs/ce) for the complete 
documentation and administrative guide. 

## Available components in Gluu Server 4.1
- oxAuth, oxTrust, oxCore v4.1
- Gluu OpenDJ v3.0.1
- Shibboleth v3.4.4
- Passport v4.1
- Java v1.8.0_112
- Node.js v9.9.0
- Jetty-distribution-9.4.12.v20180830
- Jython v2.7.2a
- Weld 3.0.0
- FluentD 3.5
- Redis

## New features

## Fixes / Enhancements
### [GluuFederation/oxAuth](https://github.com/GluuFederation/oxAuth/issues?utf8=?&q=is%3Aissue+milestone%3A4.1+)

- [#1237](https://github.com/GluuFederation/oxAuth/issues/1237) ~Overlap in QR code scanning for super gluu authentication~

- [#1233](https://github.com/GluuFederation/oxAuth/issues/1233) ~Don't insert ou=pairwiseIdentifiers tree node into DB which not supports tree model~

- [#1232](https://github.com/GluuFederation/oxAuth/issues/1232) ~Support localel with - instead of _ in the name~

- [#1231](https://github.com/GluuFederation/oxAuth/issues/1231) ~Cluster: CM rotates keys but oxauth is not aware of it. Keystore is loaded only at start up.~

- [#1229](https://github.com/GluuFederation/oxAuth/issues/1229) ~After some time oxauth running keys idToken can't be issued due to keys problem~

- [#1221](https://github.com/GluuFederation/oxAuth/issues/1221) ~During MTLS authentication session user is not re-configured which leads to infinite loop between authorization action and endpoint~

- [#1218](https://github.com/GluuFederation/oxAuth/issues/1218) ~Store extra parameters after final authnetication step~

- [#1217](https://github.com/GluuFederation/oxAuth/issues/1217) ~Front-channel logout breaks when cache type is set to redis or memcached.~

- [#1214](https://github.com/GluuFederation/oxAuth/issues/1214) ~Fix oidc session change detection~

- [#1210](https://github.com/GluuFederation/oxAuth/issues/1210) ~JWT signature fails when using algorithms other than RSA~

- [#1209](https://github.com/GluuFederation/oxAuth/issues/1209) ~Support domain cookie option in session cookies~

- [#1208](https://github.com/GluuFederation/oxAuth/issues/1208) ~Fix native cache random errors which led to 3% AuthZ flow failures~

- [#1207](https://github.com/GluuFederation/oxAuth/issues/1207) ~Failed to render updates in oxAuthRP~

- [#1201](https://github.com/GluuFederation/oxAuth/issues/1201) ~Allow to change cleaner interval without restarting oxAuth~

- [#1200](https://github.com/GluuFederation/oxAuth/issues/1200) ~"sub" claim is absent from id_token and userinfo response when certain attributes are used as source for it~

- [#1199](https://github.com/GluuFederation/oxAuth/issues/1199) ~Registered clients disappear one day after created regardless of client expiration value ?~

- [#1189](https://github.com/GluuFederation/oxAuth/issues/1189) ~Issued session_id claim in RO grant type~

- [#1188](https://github.com/GluuFederation/oxAuth/issues/1188) ~Add new method to ROPC scritp to allow modify token response~

- [#1147](https://github.com/GluuFederation/oxAuth/issues/1147) ~Use new delete method with filter in clean up jobs~

- [#1078](https://github.com/GluuFederation/oxAuth/issues/1078) ~Check expiration of JWT encoded profile used in passport flows~

### [GluuFederation/oxTrust](https://github.com/GluuFederation/oxTrust/issues?utf8=?&q=is%3Aissue+milestone%3A4.1+)

- [#1905](https://github.com/GluuFederation/oxTrust/issues/1905) ~Allow to specify inum in API calls~

- [#1904](https://github.com/GluuFederation/oxTrust/issues/1904) ~Few Fido2 JSON parameter are missing in GUI~

- [#1897](https://github.com/GluuFederation/oxTrust/issues/1897) ~Keeping client's 'change secret' blank removing existing clientSecret~

- [#1896](https://github.com/GluuFederation/oxTrust/issues/1896) ~redis password is not mandatory~

- [#1895](https://github.com/GluuFederation/oxTrust/issues/1895) ~Remove sentinelMasterGroupName in redisConfiguration~

- [#1893](https://github.com/GluuFederation/oxTrust/issues/1893) ~Name change: "Custom Attributes" to something else~

- [#1892](https://github.com/GluuFederation/oxTrust/issues/1892) ~Enforce https scheme for redirect_uri in web UI~

- [#1888](https://github.com/GluuFederation/oxTrust/issues/1888) ~Hide "Manage Saml Acrs" menu if SAML is not installed~

- [#1885](https://github.com/GluuFederation/oxTrust/issues/1885) ~Make username field readonly while editing person~

- [#1884](https://github.com/GluuFederation/oxTrust/issues/1884) ~Make inum field readonly while editing person~

- [#1882](https://github.com/GluuFederation/oxTrust/issues/1882) ~Inaccurate description of scim field in attribute form~

- [#1880](https://github.com/GluuFederation/oxTrust/issues/1880) ~Enable/Disable OpenDJ mail uniqueness~

- [#1878](https://github.com/GluuFederation/oxTrust/issues/1878) ~Unable to create unexpired client~

- [#1877](https://github.com/GluuFederation/oxTrust/issues/1877) ~Wrong time in client form~

- [#1876](https://github.com/GluuFederation/oxTrust/issues/1876) ~Test Cache Provider~

- [#1875](https://github.com/GluuFederation/oxTrust/issues/1875) ~Show warning when gluuCustomperson attributes list is empty on User Form~

- [#1874](https://github.com/GluuFederation/oxTrust/issues/1874) ~Store server stats in separate entry~

- [#1872](https://github.com/GluuFederation/oxTrust/issues/1872) ~Fix defaultScope checkbox in scope form~

- [#1871](https://github.com/GluuFederation/oxTrust/issues/1871) ~Client Attributes can't be persisted from web UI~

- [#1728](https://github.com/GluuFederation/oxTrust/issues/1728) ~Implement SCIM change log and expose API to get changes from certain date~

### [GluuFederation/oxShibboleth](https://github.com/GluuFederation/oxShibboleth/issues?utf8=?&q=is%3Aissue+milestone%3A4.1+)

### [GluuFederation/gluu-passport](https://github.com/GluuFederation/gluu-passport/issues?utf8=?&q=is%3Aissue+milestone%3A4.1+)

- [#73](https://github.com/GluuFederation/gluu-passport/issues/73) ~Encrypt profile data~

- [#66](https://github.com/GluuFederation/gluu-passport/issues/66) ~Sending data other than profile data from passport to custom script?~

- [#65](https://github.com/GluuFederation/gluu-passport/issues/65) ~Support logout for IDPs~

### [GluuFederation/community-edition-setup](https://github.com/GluuFederation/community-edition-setup/issues?utf8=?&q=is%3Aissue+milestone%3A4.1+)

- [#634](https://github.com/GluuFederation/community-edition-setup/issues/634) add oxd and casa for post setup installation

- [#629](https://github.com/GluuFederation/community-edition-setup/issues/629) ~Change ownership on oxauth.xml and identity.xml during setup~

- [#613](https://github.com/GluuFederation/community-edition-setup/issues/613) ~Preisntall memcached int ochroot~

### [GluuFederation/oxcore](https://github.com/GluuFederation/oxcore/issues?utf8=?&q=is%3Aissue+milestone%3A4.1+)

- [#177](https://github.com/GluuFederation/oxCore/issues/177) ~Cache should supports mehods hasKey and allow to put data without expiration~

- [#176](https://github.com/GluuFederation/oxCore/issues/176) ~findEntries defect~

- [#175](https://github.com/GluuFederation/oxCore/issues/175) ~Support LDAP configuration update via EntryManager API~

- [#173](https://github.com/GluuFederation/oxCore/issues/173) ~Fix random user authentication test failure after user auto-enrollment in oxAuth Person auth Script~

- [#172](https://github.com/GluuFederation/oxCore/issues/172) ~Fix Native cache clean up~

- [#171](https://github.com/GluuFederation/oxCore/issues/171) ~Add In Memory local cache to cache small data sets~

- [#168](https://github.com/GluuFederation/oxCore/issues/168) ~Server do wrong redirects when oxAuth/oxTrust is behind LB~

### [GluuFederation/SCIM-Client](https://github.com/GluuFederation/SCIM-Client/issues?utf8=?&q=is%3Aissue+milestone%3A4.1+)
