# Notice

This document, also known as the Gluu Release Note, 
relates to the Gluu Release versioned 3.0.2. The work is licensed under “The MIT License” 
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

The document is released with the Version 3.0.2 of the Gluu Software. The purpose of this document is to provide the changes made/new features included in this release of the Gluu Software. The list is not exhaustive and there might be some omission of negligible issues, but the noteworthy features, enhancements and fixes are covered. 

## Background

The Gluu Server is a free open source identity and access management (IAM) platform. The Gluu Server is a container distribution composed of software written by Gluu and incorporated from other open source projects. 

The most common use cases for the Gluu Server include single sign-on (SSO), mobile authentication, API access management, two-factor authentication, customer identity and access management (CIAM) and identity federation.

## Documentation

The documentation for Gluu software is available at [Gluu Documentation Page](http://www.gluu.org/docs). Please visit the link for the complete documentation and administrative guide. 

## Components included in Gluu Server CE 3.0.2
- oxAuth, oxTrust,oxCore v3.0.2
- OpenLDAP v2.4.44-5
- Shibboleth v3.2.1
- Asimba forked from v1.3.0 + v1.3.1 snapshot changes (v1.3.1 was never released)
- Passport v0.3.2
- Java v1.8.0_112
- Node.js v6.9.1
- Jetty-distribution-9.3.15.v20161220
- Jython v2.7.0

## What's new in version 3.0.2
Major bugs have been fixed as below

### New Features
#### oxAuth
- Default CORS support in web.xml file [#523](https://github.com/GluuFederation/oxAuth/issues/523)
- Client registration allowed with http for localhost [#496](https://github.com/GluuFederation/oxAuth/issues/496)
- UMA RPT audit logs contain client_id and user_id [#483](https://github.com/GluuFederation/oxAuth/issues/483)
#### oxTrust
- Central log4j2.xml location [#522](https://github.com/GluuFederation/oxTrust/issues/522)
- TR download metadata file in background [#349](https://github.com/GluuFederation/oxTrust/issues/349)
- Validated id_token acr claim equals specified oxTrust authn method [#513](https://github.com/GluuFederation/oxTrust/issues/513)
- IDP v3 CAS configuration in oxTrust [#377](https://github.com/GluuFederation/oxTrust/issues/377)
- Password reminder action uses wrong condition to enable/disable this functionality [#334](https://github.com/GluuFederation/oxTrust/issues/334)
- Support inetOrgPerson [#516](https://github.com/GluuFederation/oxTrust/issues/516)
#### Community Edition
- Check LDAP passwords and reject invalid shell characters like $ [#299](https://github.com/GluuFederation/community-edition-setup/issues/299)


###Deprecated Features

#### oxTrust
- Extra Update Password button[ #224](https://github.com/GluuFederation/oxTrust/issues/224)

### Fixes
#### oxAuth
- CORS filter not processing pre-flight requests #541 [#458](https://github.com/GluuFederation/oxAuth/issues/458)
- "X-Frame-Options" header set by Apache prevents opiframe from being used by RP [#543](https://github.com/GluuFederation/oxAuth/issues/543)
- Security error thrown using implicit flow when request the userinfo endpoint [#529](https://github.com/GluuFederation/oxAuth/issues/529)
- UserInfoRestWebServiceImpl throwing 503 error [#518](https://github.com/GluuFederation/oxAuth/issues/518)
- Error message [#462](https://github.com/GluuFederation/oxAuth/issues/462)
- Binary tokens are indexed [#194](https://github.com/GluuFederation/oxAuth/issues/192)
- UMA resource_set name is mandatory [#468](https://github.com/GluuFederation/oxAuth/issues/468)
- Certificate authentication jetty support [#481](https://github.com/GluuFederation/oxAuth/issues/481)

#### oxTrust
- Default authentication method names changed [#518](https://github.com/GluuFederation/oxTrust/issues/518) [#506](https://github.com/GluuFederation/oxTrust/issues/506) [#521](https://github.com/GluuFederation/oxTrust/issues/521)
- Birthday attribute schema does not match format [#562](https://github.com/GluuFederation/oxTrust/issues/562)
- SAML metadata fix [#561](https://github.com/GluuFederation/oxTrust/issues/561) [#529](https://github.com/GluuFederation/oxTrust/issues/529)
- Password reset [#552](https://github.com/GluuFederation/oxTrust/issues/552)
- Unable to remove custom script [#537](https://github.com/GluuFederation/oxTrust/issues/537)
- UMA resource set GUI corrupts scopes field [#484](https://github.com/GluuFederation/oxTrust/issues/484)
- SAML TR add issue [#505](https://github.com/GluuFederation/oxTrust/issues/505) [#351](https://github.com/GluuFederation/oxTrust/issues/351)
- User entry created via oxTrust lacks "eduPerson" objectclass [#499](https://github.com/GluuFederation/oxTrust/issues/499)
#### Community Edition
- Remove IP address from https config [#300](https://github.com/GluuFederation/community-edition-setup/issues/300)
- Gluu Server 3.0.1 fails to start after VM reboot[#274](https://github.com/GluuFederation/community-edition-setup/issues/274)
- Error in import30.py script [#279](https://github.com/GluuFederation/community-edition-setup/issues/279)
- Import30.py is not importing SPs [#280](https://github.com/GluuFederation/community-edition-setup/issues/280)
- Change attribute ldif to better support inetOrgPerson [#282](https://github.com/GluuFederation/community-edition-setup/issues/282)
- OpenLDAP certificates are signed with wrong CN [#289](https://github.com/GluuFederation/community-edition-setup/issues/289)
- 3.0.2 debian 8 services are not starting after reboot[#304](https://github.com/GluuFederation/community-edition-setup/issues/304)
- 3.0.2 Ubuntu 16.04 - all services are not starting after VM reboot [#305](https://github.com/GluuFederation/community-edition-setup/issues/305)
- Gluu Server v3.0.2 not installing in Ubuntu 16.04 [#312](https://github.com/GluuFederation/community-edition-setup/issues/312)
