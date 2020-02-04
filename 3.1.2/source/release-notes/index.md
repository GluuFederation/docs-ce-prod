# Release Notes

## Notice

This document, also known as the Gluu Release Note, 
relates to the Gluu Server Release versioned 3.1.2. The work is licensed under “The MIT License” 
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

| Released | EOL |
| --- | --- |
| January 2018 | April 2020 |


## Purpose

The document is released with the Version 3.1.2 of the Gluu Software. The purpose of this document is to provide the changes made/new features included in this release of the Gluu Software. The list is not exhaustive and there might be some omission of negligible issues, but the noteworthy features, enhancements and fixes are covered. 

## Background

The Gluu Server is a free open source identity and access management (IAM) platform. The Gluu Server is a container distribution composed of software written by Gluu and incorporated from other open source projects. 

The most common use cases for the Gluu Server include single sign-on (SSO), mobile authentication, API access management, two-factor authentication, customer identity and access management (CIAM) and identity federation.

## Documentation

Please visit the [Gluu Documentation Page](http://www.gluu.org/docs/ce) for the complete 
documentation and administrative guide. 

## Available components in Gluu Server 3.1.2
- oxAuth, oxTrust, oxCore v3.1.2
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

- [658](https://github.com/GluuFederation/oxAuth/issues/658) Make implicit flow configurable and persist all related objects into cache (no ldap at all)

- [679](https://github.com/GluuFederation/oxAuth/issues/679) Dynamic OpenID Authz script 

- [Docs](../authn-guide/inbound-saml-passport.md) Inbound SAML SSO via passport.js 

- [686](https://github.com/GluuFederation/oxAuth/issues/686) UMA 2: Allow access token for authentication at UMA token endpoint

- [688](https://github.com/GluuFederation/oxAuth/issues/688) UMA 2: support "and", "or" logical operations for scopes (including nested)

- [604](https://github.com/GluuFederation/oxTrust/issues/604) Show u2f creds in user page

- [13](https://github.com/GluuFederation/community-edition-package/issues/13) Add "clear-logs" option to gluu-server init script to clear logs 

## Fixes / Enhancements

### [oxAuth](https://github.com/GluuFederation/oxAuth/issues?q=is%3Aopen+is%3Aissue+milestone%3A3.1.2)

- [728](https://github.com/GluuFederation/oxAuth/issues/728) Username remember me feature in login page

- [724](https://github.com/GluuFederation/oxAuth/issues/724) Improve `JwtClaims.setClaim()` to support types `JSONObject` and `List<Object>`

- [699](https://github.com/GluuFederation/oxAuth/issues/699) Create new JWK for use=enc for Client and Server tests

- [700](https://github.com/GluuFederation/oxAuth/issues/700) Invalid "scopes" field in Dynamic Client Registration request and response

- [677](https://github.com/GluuFederation/oxAuth/issues/677) Encode/decode client_id/secret separately in basic auth

- [661](https://github.com/GluuFederation/oxAuth/issues/661) Fix Password Expiration authentication script

- [391](https://github.com/GluuFederation/oxAuth/issues/391) Introspection API Docs: Missing Response

- [91](https://github.com/GluuFederation/oxAuth/issues/91) Add support for encrypting Request Objects sent to the OP

- [574](https://github.com/GluuFederation/oxAuth/issues/574) No support for "popup" value of "display" request parameter

- [691](https://github.com/GluuFederation/oxAuth/issues/691) Performance improvements

- [600](https://github.com/GluuFederation/oxAuth/issues/600) OIDC returning arrays incorrectly

- [696](https://github.com/GluuFederation/oxAuth/issues/696) Introspection response `exp` field must return value in seconds

- [695](https://github.com/GluuFederation/oxAuth/issues/695) Introspection : add `sub` field value to introspection response

- [689](https://github.com/GluuFederation/oxAuth/issues/689) UMA 2 : requested scope is not returned in permissions of RPT introspection

- [685](https://github.com/GluuFederation/oxAuth/issues/685) Failed to update oxLastLogonTime of user X" error message

- [679](https://github.com/GluuFederation/oxAuth/issues/679) Multi-Step OpenID Connect AuthZ Script

- [681](https://github.com/GluuFederation/oxAuth/issues/681) Don't override OC specified in custom script

- [675](https://github.com/GluuFederation/oxAuth/issues/675) Restore parameters from session automatically

- [672](https://github.com/GluuFederation/oxAuth/issues/672) OIDC authorization page throws an error

- [670](https://github.com/GluuFederation/oxAuth/issues/670) Only first value of multi-valued claim is returned in id_token

- [668](https://github.com/GluuFederation/oxAuth/issues/668) Log denied Dynamic Client Registration Requests at INFO level

- [662](https://github.com/GluuFederation/oxAuth/issues/662) Improve oxAuth authz checking mechanism

- [653](https://github.com/GluuFederation/oxAuth/issues/653) NPE when requesting authorization with acr param

- [647](https://github.com/GluuFederation/oxAuth/issues/647) Support Custom Params

- [632](https://github.com/GluuFederation/oxAuth/issues/632) basic_multi_auth not working

- [584](https://github.com/GluuFederation/oxAuth/issues/584) Call instance<T>.destroy on manually created object on destroy

- [479](https://github.com/GluuFederation/oxAuth/issues/479) SuperGluu Script: add link to download app

- [692](https://github.com/GluuFederation/oxAuth/issues/692) UMA RPT policy script for SCIM crashes

- [690](https://github.com/GluuFederation/oxAuth/issues/690) UMA 2 : requested scope must be validated per client (not system wide)

- [686](https://github.com/GluuFederation/oxAuth/issues/686) UMA 2 : Allow access token for authentication at UMA token endpoint

- [684](https://github.com/GluuFederation/oxAuth/issues/684) Test coverage for multi-step authz flows

### [oxTrust](https://github.com/GluuFederation/oxTrust/issues?q=is%3Aopen+is%3Aissue+milestone%3A3.1.2)

- [717](https://github.com/GluuFederation/oxTrust/issues/717) Updated default Super Gluu web pages   

- [789](https://github.com/GluuFederation/oxTrust/issues/789) Activate/Deactive LDAP server feature of "Manage authentication" page is broken

- [780](https://github.com/GluuFederation/oxTrust/issues/780) On profile update applciation should call update person custom script

- [779](https://github.com/GluuFederation/oxTrust/issues/779) Add post add/update/delete methods to update user script

- [751](https://github.com/GluuFederation/oxTrust/issues/751) oxTrust cannot create "userCertificate"

- [770](https://github.com/GluuFederation/oxTrust/issues/770) UMA Scope is not editable after image upload

- [767](https://github.com/GluuFederation/oxTrust/issues/767) Add new default designs for U2F, OTP, and SMS OTP auth pages

- [737](https://github.com/GluuFederation/oxTrust/issues/737) Errors thrown before redirected to oxAuth login page #737

- [761](https://github.com/GluuFederation/oxTrust/issues/761) VTL identifier wrong in Shibboleth velocity templates

- [759](https://github.com/GluuFederation/oxTrust/issues/759) "JSON configuration -> oxTrust" page/tab contains field no longer being used

- [757](https://github.com/GluuFederation/oxTrust/issues/757) Fix User status value when using User Import with xls file

- [756](https://github.com/GluuFederation/oxTrust/issues/756) Fix Incorrect Label on email address field in Manage People screen

- [755](https://github.com/GluuFederation/oxTrust/issues/755) Remote IDP's certificate (Asimba flows' settings) is not being imported

- [754](https://github.com/GluuFederation/oxTrust/issues/754) Unable to add attributes via Attributes Filter

- [753](https://github.com/GluuFederation/oxTrust/issues/753) Fix screen display for large attributes in "Update Users" screen

- [750](https://github.com/GluuFederation/oxTrust/issues/750) Unable to delete created attributes

- [746](https://github.com/GluuFederation/oxTrust/issues/746) Mail Sent from Gluu Server is in text format

- [745](https://github.com/GluuFederation/oxTrust/issues/745) No option to clear an OIDC client's setting if it was already set to some value explicitly using a drop-down list

- [744](https://github.com/GluuFederation/oxTrust/issues/744) Submenus do not open and close

- [743](https://github.com/GluuFederation/oxTrust/issues/743) No build date and number

- [741](https://github.com/GluuFederation/oxTrust/issues/741) Extend Authentication Script to support GUI representation]

- [723](https://github.com/GluuFederation/oxTrust/issues/723) Cache Provider Configuration settings fix

- [629](https://github.com/GluuFederation/oxTrust/issues/629) Add option to mail configuration to enable implicit trust to host mail server

- [599](https://github.com/GluuFederation/oxTrust/issues/599) Register page is not working

- [536](https://github.com/GluuFederation/oxTrust/issues/536) MAX_COUNT in SCIM Client negative test cases

- [404](https://github.com/GluuFederation/oxTrust/issues/404) SCIM 2.0 Missing access token in test mode causes unhandled exception

- [765](https://github.com/GluuFederation/oxTrust/issues/765) Question on error / oxTrust - "Can't perform redirect to viewId: /error"

- [717](https://github.com/GluuFederation/oxTrust/issues/717) Super Gluu Enroll + Subsequent Auths page

- [633](https://github.com/GluuFederation/oxTrust/issues/633) Images in developer setup are too small

### [Community Edition Setup](https://github.com/GluuFederation/community-edition-setup/issues?q=is%3Aopen+is%3Aissue+milestone%3A3.1.2)

- [393](https://github.com/GluuFederation/community-edition-setup/issues/393) In setup.py allow selection of LDAP server 

- [30](https://github.com/GluuFederation/community-edition-setup/issues/30) Don't allow to run setup.py after installation

- [367](https://github.com/GluuFederation/community-edition-setup/issues/367) Upgrade: `openIdClientPassword` changing in 'oxidp' configuration bug

- [366](https://github.com/GluuFederation/community-edition-setup/issues/366) Upgrade: permission of Shibboleth configuration bug

- [350](https://github.com/GluuFederation/community-edition-setup/issues/350) Wrong directory in gluu-server uninstall notification

- [352](https://github.com/GluuFederation/community-edition-setup/issues/352) Setup.py re-prompt for IP address upon invalid entry

- [345](https://github.com/GluuFederation/community-edition-setup/issues/345) Stopping Gluu Server does not stop memcached in 3.1

- [273](https://github.com/GluuFederation/community-edition-setup/issues/273) Failed to start rsyslog in RHEL 7.2

- [371](https://github.com/GluuFederation/community-edition-setup/issues/371) IdP starts prior to OpenLDAP in Xenial

- [363](https://github.com/GluuFederation/community-edition-setup/issues/363) Upgrade: 2.4.4 export script not working

- [134](https://github.com/GluuFederation/community-edition-setup/issues/134) Cron jobs don't start inside of the container of 2.4.3 CE deb packages

### [gluu-Asimba](https://github.com/GluuFederation/gluu-asimba/issues?q=is%3Aopen+is%3Aissue+milestone%3A3.1.2)

- [44](https://github.com/GluuFederation/gluu-Asimba/issues/44) An Asimba setting which controls the number of seconds after which Asimba refuses authentication based on AuthInstant

- [43](https://github.com/GluuFederation/gluu-Asimba/issues/43) Asimba Script's reaction for AuthnFailed message from Asimba

### [Gluu Passport](https://github.com/GluuFederation/gluu-passport/issues?q=is%3Aopen+is%3Aissue+milestone%3A3.1.2)

- [6](https://github.com/GluuFederation/gluu-passport/issues/6) Support other SAML params

- [5](https://github.com/GluuFederation/gluu-passport/issues/5) Support SAML response encryption

- [7](https://github.com/GluuFederation/gluu-passport/issues/7) Controls the number of seconds after which Passport refuses authentication

### [oxCore](https://github.com/GluuFederation/oxCore/issues?q=is%3Aopen+is%3Aissue+milestone%3A3.1.2)

- [56](https://github.com/GluuFederation/oxCore/issues/56) Redis : avoid NPE if key is null

- [59](https://github.com/GluuFederation/oxCore/issues/59) Use same connection in count method

### [SCIM Client](https://github.com/GluuFederation/SCIM-client/issues?q=is%3Aopen+is%3Aissue+milestone%3A3.1.2)

- [55](https://github.com/GluuFederation/SCIM-Client/issues/55) Deserialization of custom attributes not taking place in client-side
