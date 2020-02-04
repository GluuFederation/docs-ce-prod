# Release Notes

## Notice

This document, also known as the Gluu Release Note, relates to the Gluu Release versioned 3.0.1. The work is licensed under “The MIT License” allowing the use, copy, modify, merge, publish, distribute, sub-license and sale without limitation and liability. This document extends only to the aforementioned release version in the heading.

UNLESS IT HAS BEEN EXPRESSLY AGREED UPON BY ANY WRITTEN AGREEMENT BEFOREHAND, THE WORK/RELEASE IS PROVIDED “AS IS”, WITHOUT ANY WARRANTY OR GUARANTEE OF ANY KIND EXPRESS OR IMPLIED. UNDER NO CIRCUMSTANCE, THE AUTHOR, OR GLUU SHALL BE LIABLE FOR ANY CLAIMS OR DAMAGES CAUSED DIRECTLY OR INDIRECTLY TO ANY PROPERTY OR LIFE WHILE INSTALLING OR USING THE RELEASE.

## Overview

### Lifecycle

Status: EOL

| Released | Community EOL | Enterprise EOL |
| --- | --- | --- |
| July 2016 | December 2018 | December 2019|

### Purpose

The document is released with the Version 3.0.1 of the Gluu Software. The purpose of this document is to provide the changes made/new features included in this release of the Gluu Software. The list is not exhaustive and there might be some omission of negligible issues, but the noteworthy features, enhancements and fixes are covered. 

### Background

The Gluu Server is a free open source identity and access management (IAM) platform. The Gluu Server is a container distribution composed of software written by Gluu and incorporated from other open source projects.

The most common use cases for the Gluu Server include single sign-on (SSO), mobile authentication, API access management, two-factor authentication, customer identity and access management (CIAM) and identity federation.

### Documentation

Please visit [Gluu Documentation Page](http://www.gluu.org/docs) for the complete documentation and administrative guide. 

### Components included in Gluu Server CE 3.0.1

- oxAuth, oxTrust,oxCore v3.0.1
- OpenLDAP v2.4.44-5
- Shibboleth v3.2.1
- Asimba forked from v1.3.0 + v1.3.1 snapshot changes (v1.3.1 was never released)
- Passport v0.3.2
- Java v1.8.0_112
- Node.js v6.9.1
- Jetty-distribution-9.3.15.v20161220
- Jython v2.7.0

### What's new in version 3.0.1

There are some major changes in Gluu Server Community Edition 3.0.1 from replacing `tomcat` with `jetty` to dropping `opendj` for `openldap`. The changes are available in the documentation hosted at https://gluu.org/docs/operation/intro. 
Please see the specific component release pages for details.

#### New Features
##### oxAuth
- Escape parameter values to prevent XSS attack [#459](https://github.com/GluuFederation/oxAuth/issues/459)
- EndSession endpoint accepts id_token or session_state to end session [#439](https://github.com/GluuFederation/oxAuth/issues/439)
- Support JSON Property for HTTPOnly [#412](https://github.com/GluuFederation/oxAuth/issues/412)
- JSON property to control writing last update time to LDAP [#410](https://github.com/GluuFederation/oxAuth/issues/410)
- log4j: 2.x from log4j 1.x [$416](https://github.com/GluuFederation/oxAuth/issues/416)
- Login page [#414](https://github.com/GluuFederation/oxAuth/issues/414)
- Jquery library updated to 1.12.4 [#411](https://github.com/GluuFederation/oxAuth/issues/411)
##### oxTrust
- Toggle persist authorization to false when pre-authorization = true [#444](https://github.com/GluuFederation/oxTrust/issues/444)
- Logging updated to log4j 2.x [#434](https://github.com/GluuFederation/oxTrust/issues/434)
- JQuery Library updated to 1.12.4 [#421](https://github.com/GluuFederation/oxTrust/issues/421)
- OpenID Scope search uses ldap name for attribute [#419](https://github.com/GluuFederation/oxTrust/issues/419)
- oxTrust UMA properties renamed [#407](https://github.com/GluuFederation/oxTrust/issues/407)
- Creation and update stamp for users in LDAP [#406](https://github.com/GluuFederation/oxTrust/issues/406)
- Display Name used to identify users in oxTrust [#398](https://github.com/GluuFederation/oxTrust/issues/398)
##### Community Edition Setup
- o=site uses different filesystem folder [#261](https://github.com/GluuFederation/community-edition-setup/issues/261)
- Jetty - Basic Hardening [#251](https://github.com/GluuFederation/community-edition-setup/issues/251)
- oxAuth default configuration [#246](https://github.com/GluuFederation/community-edition-setup/issues/246)

#### Deprecated Features
##### oxTrust
- White Pages tab and option [#423](https://github.com/GluuFederation/oxTrust/issues/423)
- Password from TR attribute list [#466](https://github.com/GluuFederation/oxTrust/issues/466)
- SAML 1 and ShibbolethSSO [#465](https://github.com/GluuFederation/oxTrust/issues/465)

#### Fixes
##### oxAuth
- NPE in 3.0.0 [#347](https://github.com/GluuFederation/oxAuth/issues/347)
- UMA AM validation for oxauth behind proxy [#472](https://github.com/GluuFederation/oxAuth/issues/472)
- oxLastLoginTime fail : print also exception
- High load performance fixed [#461](https://github.com/GluuFederation/oxAuth/issues/461) [#463](https://github.com/GluuFederation/oxAuth/issues/463) [#438](https://github.com/GluuFederation/oxAuth/issues/438) [#408](https://github.com/GluuFederation/oxAuth/issues/408) [#400](https://github.com/GluuFederation/oxAuth/issues/400) [#399](https://github.com/GluuFederation/oxAuth/issues/399) [#384](https://github.com/GluuFederation/oxAuth/issues/384)
- Failed to register client with custom attribute "oxAuthTrustedClient" [#476](https://github.com/GluuFederation/oxAuth/issues/476)
- U2F Authentication [#455](https://github.com/GluuFederation/oxAuth/issues/455)
- hostname required to match in request to token_endpoint [#451](https://github.com/GluuFederation/oxAuth/issues/451)
- Login page footer message [#449](https://github.com/GluuFederation/oxAuth/issues/449)
- metricService doesn't persist statistics to LDAP [#448](https://github.com/GluuFederation/oxAuth/issues/448)
- DUO script fail [#444](https://github.com/GluuFederation/oxAuth/issues/444)
- Persist authorizations throws NPE [#442](https://github.com/GluuFederation/oxAuth/issues/442)
- Setting Pre-Auth true should not allow anything writter under ou=clientAuthorizations [#441](https://github.com/GluuFederation/oxAuth/issues/441)
- Persist Authorization not functioning [#440](https://github.com/GluuFederation/oxAuth/issues/440)
- Any primaryKey except UID does not function [#436](https://github.com/GluuFederation/oxAuth/issues/436)
- Token Introspection fixes [#433](https://github.com/GluuFederation/oxAuth/issues/433) [#432](https://github.com/GluuFederation/oxAuth/issues/432)
- Pairwise identifier shows inum in id_token and Userinfo [#430](https://github.com/GluuFederation/oxAuth/issues/430)
- Replaced activemq-all jar with required libraries [#425](https://github.com/GluuFederation/oxAuth/issues/425)
- SCIM-Client fails to authenticate with UMA [#402](https://github.com/GluuFederation/oxAuth/issues/402)
- Attribute values stored as UTF-8 string [#387](https://github.com/GluuFederation/oxAuth/issues/387)
- default_acr_value is not used in authentication process [#383](https://github.com/GluuFederation/oxAuth/issues/383)
- Authenticator should not add default message if count of messages >0 [#379](https://github.com/GluuFederation/oxAuth/issues/379)
- Show error page with timestamp on oxauth error [#377](https://github.com/GluuFederation/oxAuth/issues/377)
- SCIM with certain values causes Server Error 500 [#372](https://github.com/GluuFederation/oxAuth/issues/372)
- auth_level_mapping discovery has double array [#366](https://github.com/GluuFederation/oxAuth/issues/366)
#### oxTrust
- Duplicate message for menu update [#375](https://github.com/GluuFederation/oxTrust/issues/375)
- SAML submenu not appearing [#391](https://github.com/GluuFederation/oxTrust/issues/391)
- Cache Refresh not functioning [#396](https://github.com/GluuFederation/oxTrust/issues/396)
- OpenID Manual Client Registration validation update [#410](https://github.com/GluuFederation/oxTrust/issues/410)
- Unable to delete Trust Relationship [#418](https://github.com/GluuFederation/oxTrust/issues/418) [#416](https://github.com/GluuFederation/oxTrust/issues/416)
- Login redirect URI broken [#422](https://github.com/GluuFederation/oxTrust/issues/422)
- Aesthetic updates in oxTrust UI [#425](https://github.com/GluuFederation/oxTrust/issues/425) [#417](https://github.com/GluuFederation/oxTrust/issues/417)
- Unable to add users via oxTrust UI [#427](https://github.com/GluuFederation/oxTrust/issues/427)
- Unable to create Trust Relationship with metadata file [#428](https://github.com/GluuFederation/oxTrust/issues/428) [#416](https://github.com/GluuFederation/oxTrust/issues/416) [#19](https://github.com/GluuFederation/oxTrust/issues/19)
- Long value of Username causes interface to break [#430](https://github.com/GluuFederation/oxTrust/issues/430)
- Email format validation in user update tab [#432](https://github.com/GluuFederation/oxTrust/issues/432)
- Passport from strategy not mandatory [#433](https://github.com/GluuFederation/oxTrust/issues/433)
- Configure Relying Party not functioning [#436](https://github.com/GluuFederation/oxTrust/issues/436) [#405](https://github.com/GluuFederation/oxTrust/issues/405)
- Failed to update default authentication mechanism [#437](https://github.com/GluuFederation/oxTrust/issues/437)
- Passport authentication appearing in default authentication tab [#438](https://github.com/GluuFederation/oxTrust/issues/438)
- OpenIDC client removal non-functional [#439](https://github.com/GluuFederation/oxTrust/issues/439)
- OpenIDC client secret disappears when response_type is added [#440](https://github.com/GluuFederation/oxTrust/issues/440)
- Passport from broken [#441](https://github.com/GluuFederation/oxTrust/issues/441)
- Changes in Configure Relying Party not saved [#446](https://github.com/GluuFederation/oxTrust/issues/446)
- Error adding group in oxTurst [#448](https://github.com/GluuFederation/oxTrust/issues/448)
- Attribute from missing from SAML URI values [#452](https://github.com/GluuFederation/oxTrust/issues/452)
- Cache Refresh page errors [#453](https://github.com/GluuFederation/oxTrust/issues/453) [#413](https://github.com/GluuFederation/oxTrust/issues/413)
- applianceStatus Page throws error [#454](https://github.com/GluuFederation/oxTrust/issues/454)
- SP Metadata File link non-functional [#455](https://github.com/GluuFederation/oxTrust/issues/455) [#429](https://github.com/GluuFederation/oxTrust/issues/429)
- Certificate mis-named [#456](https://github.com/GluuFederation/oxTrust/issues/456)
- Trust Relationship search in oxTrust UI non-functional [#457](https://github.com/GluuFederation/oxTrust/issues/457)
- Failed to update user via oxTrust UI [#459](https://github.com/GluuFederation/oxTrust/issues/459)
- Cache Refresh link not functional [#460](https://github.com/GluuFederation/oxTrust/issues/460)
- Exception handling on passport authentication field [#462](https://github.com/GluuFederation/oxTrust/issues/462)
- Created User password does not work [#468](https://github.com/GluuFederation/oxTrust/issues/468)
- User Registration page redirects to home [#471](https://github.com/GluuFederation/oxTrust/issues/471)
- Don't display list of claims in OpenID dynamic scope creation [#472](https://github.com/GluuFederation/oxTrust/issues/472)
- User Registration throws error [#478](https://github.com/GluuFederation/oxTrust/issues/478)
- Removed Add Resource button from UMA [#480](https://github.com/GluuFederation/oxTrust/issues/480)
- Federation SP list not loading [#488](https://github.com/GluuFederation/oxTrust/issues/488)

##### Community Edition Setup
- LDAP running as root [#262](https://github.com/GluuFederation/community-edition-setup/issues/262)
- Setup script in CentOS 6.x [#260](https://github.com/GluuFederation/community-edition-setup/issues/260)
- OpenDJ schema [#259](https://github.com/GluuFederation/community-edition-setup/issues/259)
- Incorrect syntax of DN attributes [#258](https://github.com/GluuFederation/community-edition-setup/issues/258)
- Update dynamic scope scripts to conform new references to script [#257](https://github.com/GluuFederation/community-edition-setup/issues/257)
- Restart command not working in Ubuntu 14.04 [#256](https://github.com/GluuFederation/community-edition-setup/issues/256)
- CAS service fails to start in Ubuntu 14.04 [#253](https://github.com/GluuFederation/community-edition-setup/issues/253)
- Hide CAS installation by default [#252](https://github.com/GluuFederation/community-edition-setup/issues/252)
- baseDN o=gluu not readable [#243](https://github.com/GluuFederation/community-edition-setup/issues/243)
- Uninstall in Ubuntu 14.04 [#237](https://github.com/GluuFederation/community-edition-setup/issues/237)
- Gluu OpenLDAP schema [#234](https://github.com/GluuFederation/community-edition-setup/issues/234)
- OpenLDAP should listen on localhost only [#236](https://github.com/GluuFederation/community-edition-setup/issues/236)
- Remove unnecessary dependency of /etc/hostname from setup.py [#281](https://github.com/GluuFederation/community-edition-setup/issues/281)
- Rendering idp3 templates under some python builds [#269](https://github.com/GluuFederation/community-edition-setup/issues/269)
- Warning at lastest CE install [#235](https://github.com/GluuFederation/community-edition-setup/issues/235)
- Include Twilio SMS script into CE [#223](https://github.com/GluuFederation/community-edition-setup/issues/223)
