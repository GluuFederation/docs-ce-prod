# Release Notes

## Notice

This document, also known as the Gluu Release Note, 
relates to the Gluu Release versioned 3.1.1. The work is licensed under “The MIT License” 
allowing the use, copy, modify, merge, publish, distribute, sub-license and sale without 
limitation and liability. This document extends only to the aforementioned release version 
in the heading.

UNLESS IT HAS BEEN EXPRESSLY AGREED UPON BY ANY WRITTEN AGREEMENT BEFOREHAND, 
THE WORK/RELEASE IS PROVIDED “AS IS”, WITHOUT ANY WARRANTY OR GUARANTEE OF ANY KIND 
EXPRESS OR IMPLIED. UNDER NO CIRCUMSTANCE, THE AUTHOR, OR GLUU SHALL BE LIABLE FOR ANY 
CLAIMS OR DAMAGES CAUSED DIRECTLY OR INDIRECTLY TO ANY PROPERTY OR LIFE WHILE INSTALLING 
OR USING THE RELEASE.

## Overview

### Lifecycle

Status: Active Release

| Released | EOL |
| --- | --- |
|October 2017 | April 2020 |

### Purpose

The document is released with the Version 3.1.1 of the Gluu Software. The purpose of this document is to provide the changes made/new features included in this release of the Gluu Software. The list is not exhaustive and there might be some omission of negligible issues, but the noteworthy features, enhancements and fixes are covered. 

### Background

The Gluu Server is a free open source identity and access management (IAM) platform. The Gluu Server is a container distribution composed of software written by Gluu and incorporated from other open source projects. 

The most common use cases for the Gluu Server include single sign-on (SSO), mobile authentication, API access management, two-factor authentication, customer identity and access management (CIAM) and identity federation.

### Documentation

Please visit the [Gluu Documentation Page](http://www.gluu.org/docs/ce) for the complete 
documentation and administrative guide. 

## Components included in Gluu Server CE 3.1.1
- oxAuth, oxTrust,oxCore v3.1.1
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

## What's new in version 3.1.1

### Enhancements
#### oxAuth
- [#649](https://github.com/GluuFederation/oxauth/issues/649) UMA 2 : Authorization Context - add user attribute fetching
- [#644](https://github.com/GluuFederation/oxauth/issues/644) UMA 2 : `id_token` validation configurable against local idp
- [#612](https://github.com/GluuFederation/oxauth/issues/612) Add attribute to Disable OpenID Client
- [#642](https://github.com/GluuFederation/oxAuth/issues/642) Redis : provide ability to specify multiple servers in configuration

#### oxTrust
- [#33](https://github.com/GluuFederation/oxTrust/issues/33) Set ACR / Level for LDAP Password Authentication
- [#69](https://github.com/GluuFederation/oxTrust/issues/69) Force oxAuth to generate new Keys
- [#714](https://github.com/GluuFederation/oxTrust/issues/714) Show hide value based on SimpleExtendedCustomProperty hideValue field
- [#717](https://github.com/GluuFederation/oxTrust/issues/717) Added Super Gluu Enroll page
- [#729](https://github.com/GluuFederation/oxTrust/issues/729) Add new redisProviderType configuration property
- [#722](https://github.com/GluuFederation/oxTrust/pull/722) OpenID Connect Provider Certification

#### Community Edition
- [#332](https://github.com/GluuFederation/community-edition-setup/pull/332)New export/import scripts
- Add property to allow disable clients

### Fixes
#### oxAuth
- [#247](https://github.com/GluuFederation/oxauth/issues/247) Update "Super Gluu" script and configuration to use Gluu push notification service
- [#646](https://github.com/GluuFederation/oxauth/issues/646) Issues with memcached session persistence

#### oxTrust
- [#724](https://github.com/GluuFederation/oxTrust/issues/724) Error on clicking INACTIVE attributes in Oxtrust UI 
- [#716](https://github.com/GluuFederation/oxTrust/issues/716) UMA 2 : resource added via api exists in ldap but is not visible on GUI

#### Community Edition
- [#331](https://github.com/GluuFederation/community-edition-setup/issues/331) Update LDAP schema to confirm UMA 2.0 code
- Update UMA 2.0 scripts
- Update "Super Gluu" and "Twilio"
