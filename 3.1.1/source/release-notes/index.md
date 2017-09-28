# Notice

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

## Purpose

The document is released with the Version 3.1.1 of the Gluu Software. The purpose of this document is to provide the changes made/new features included in this release of the Gluu Software. The list is not exhaustive and there might be some omission of negligible issues, but the noteworthy features, enhancements and fixes are covered. 

## Background

The Gluu Server is a free open source identity and access management (IAM) platform. The Gluu Server is a container distribution composed of software written by Gluu and incorporated from other open source projects. 

The most common use cases for the Gluu Server include single sign-on (SSO), mobile authentication, API access management, two-factor authentication, customer identity and access management (CIAM) and identity federation.

## Documentation

Please visit the [Gluu Documentation Page](http://www.gluu.org/docs) for the complete 
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

## What's new in version 3.1.1

### New Features
#### oxAuth
- Migration to Weld 3.0.0.CR2[#221](https://github.com/GluuFederation/oxAuth/issues/221)
- UMA 2: Implement Claims Gathering Endpoint[#300](https://github.com/GluuFederation/oxAuth/issues/300)
- UMA 2: support plain scopes[#536](https://github.com/GluuFederation/oxAuth/issues/536)
- UMA 2: introduce/upgrade metadata according to UMA 2 spec[#534](https://github.com/GluuFederation/oxAuth/issues/534)
- UMA 2: Implement support for client "pushed claims" and PCT[#533](https://github.com/GluuFederation/oxAuth/issues/533)
- Add support for token_endpoint_auth_signing_alg (OpenID Connect Dynamic Client Registration)[#92](https://github.com/GluuFederation/oxAuth/issues/92)
- Add expiration time to session_state cookie[#333](https://github.com/GluuFederation/oxAuth/issues/333)
- Support logout with expired id_token [#332](https://github.com/GluuFederation/oxAuth/issues/332)
- Request / Resonse Audit Logging[#378](https://github.com/GluuFederation/oxAuth/issues/378)
- Super-Gluu script should support AWS SNS for push notifications[#630](https://github.com/GluuFederation/oxAuth/issues/630)
- Customization in 3.1.x [#501](https://github.com/GluuFederation/oxAuth/issues/501}
- Error handling in 3.1.x[#504](https://github.com/GluuFederation/oxAuth/issues/504)

#### oxTrust
- UMA 2 : added "claims_redirect_uris" to client.[#593](https://github.com/GluuFederation/oxTrust/issues/593)
- UMA 2 : Introduce new "UMA Claims Gathering Script"[#590](https://github.com/GluuFederation/oxTrust/issues/590)
- JSF-related changes in SAML pages[#611](https://github.com/GluuFederation/oxTrust/issues/611)
- Add FluentD support[#589](https://github.com/GluuFederation/oxTrust/issues/589)
- Support TR without Metadata[#353](https://github.com/GluuFederation/oxTrust/issues/353)
- Handle coversation timeout[#626](https://github.com/GluuFederation/oxTrust/issues/626)
- Make SCIM 2.0 search MAX_COUNT configurable[#320](https://github.com/GluuFederation/oxTrust/issues/320)
- More user-friendly look of the OIDC client configuration page[#226](https://github.com/GluuFederation/oxTrust/issues/226)
- Make cache provider configurable via UI (oxCacheConfiguration attribute of gluuAppliance OS)[#485](https://github.com/GluuFederation/oxTrust/issues/485)
- Application should disable controls on processing Ajax requests [#129](https://github.com/GluuFederation/oxTrust/issues/129)
- Add "active" column to import spreadsheet [#171](https://github.com/GluuFederation/oxTrust/issues/171)

#### Community Edition
- Change method of adding scripts to setup[#313](https://github.com/GluuFederation/community-edition-setup/issues/313)
- Add setup option which allows to import additional templates after base install[#285](https://github.com/GluuFederation/community-edition-setup/issues/285)
- setup.py - using an Ampersand (&) in admin password field fails[#268](https://github.com/GluuFederation/community-edition-setup/issues/268)
- Add external configuration file which contains list of indexes whoich setup should add to OpenLDAP[#245](https://github.com/GluuFederation/community-edition-setup/issues/245)
- Add a section for csync2 tool's logs to our log rotation script.[#171](https://github.com/GluuFederation/community-edition-setup/issues/171)
- Apache MPMs differ between Gluu's packages for different distros[#139](https://github.com/GluuFederation/community-edition-setup/issues/139)
- Increase Gluu-LDAP security[#98](https://github.com/GluuFederation/community-edition-setup/issues/98)
- "Timezone" setting for setup.py[#71](https://github.com/GluuFederation/community-edition-setup/issues/71)

### Deprecated Features
#### oxAuth
- Deprecate Authn Scripts: phonefactor, wikid, toopher, oneid, inwebo [#490](https://github.com/GluuFederation/oxAuth/issues/490)
- Review Justin's UMA 1.0.1 issues workarounds[#187](https://github.com/GluuFederation/oxAuth/issues/187)
- Remove CAS from default authn scripts[#557](https://github.com/GluuFederation/oxAuth/issues/557)
- Remove jettison resteasy provider[#220](https://github.com/GluuFederation/oxAuth/issues/220)
- UMA 2: Remove AAT[#532](https://github.com/GluuFederation/oxAuth/issues/532)
- UMA 2: Remove GAT Tokens[#531](https://github.com/GluuFederation/oxAuth/issues/531)
#### oxTrust
- Remove Level from Authorization Script[#581](https://github.com/GluuFederation/oxTrust/issues/581)
- Deprecate or review native2ascii script usage[#578](https://github.com/GluuFederation/oxTrust/issues/578)
- Remove old SCIM 1 code[#631](https://github.com/GluuFederation/oxTrust/issues/631)
#### Community Edition
- Remove CustomAttributes[#311](https://github.com/GluuFederation/community-edition-setup/issues/311)
- Remove Shib. IDP/SAML Metadata related template duplications[#298](https://github.com/GluuFederation/community-edition-setup/issues/298)
- Remove CAS as install option[#247](https://github.com/GluuFederation/community-edition-setup/issues/247)
### Fixes
#### oxAuth
- setAmrClaim() in IdTokenFactory.java only allows scripts with usage type of "Both methods", instead of allowing scripts of any type[582](https://github.com/GluuFederation/oxAuth/issues/582)
- Validation URL incorrect in access token[547](https://github.com/GluuFederation/oxAuth/issues/547)
- CORS filter doesn't seem to process pre-flight requests in CE 3.1.x[542](https://github.com/GluuFederation/oxAuth/issues/542)
- Enforce Grant Type Client Restrictions[525](https://github.com/GluuFederation/oxAuth/issues/525)
- Failed to register client with custom attribute "oxAuthTrustedClient"[476](https://github.com/GluuFederation/oxAuth/issues/476)
- UMA AM validation in scenarion when oxauth behind te proxy[472](https://github.com/GluuFederation/oxAuth/issues/472)
- Under high load (400 concurrent threads) we got redirect back to login page after successfull login  in ~1-2% of requests[463](https://github.com/GluuFederation/oxAuth/issues/463)
- Random session enty update error[408](https://github.com/GluuFederation/oxAuth/issues/408)
- Support logout with expired id_token[332](https://github.com/GluuFederation/oxAuth/issues/332)
- Support AD servers without anonymous bind[190](https://github.com/GluuFederation/oxAuth/issues/190)
- Add filter to auth_ldap_server authentication method[167](https://github.com/GluuFederation/oxAuth/issues/167)
#### oxTrust
- Hostname should show FQDN in Configuration/Server Status[222](https://github.com/GluuFederation/oxTrust/issues/222)
- Use specific LDAP certificate or cacert to connect remote LDAP server[244](https://github.com/GluuFederation/oxTrust/issues/244)
- InCommon R&S should not be visible for everyone[343](https://github.com/GluuFederation/oxTrust/issues/343)
- [CR] CR doesn't map attributes like "sn" or "mail" implicitly (when there is no mapping for them in the table) anymore[314](https://github.com/GluuFederation/oxTrust/issues/314)
- Entityid selection pop-up for TRs created based on federation TR overlaps with other UI elements[306](https://github.com/GluuFederation/oxTrust/issues/306)
- SCIM v2.x Users resource endpoint returns empty list if count is omitted[360](https://github.com/GluuFederation/oxTrust/issues/360)
- Fix JSF rendering warnings[347](https://github.com/GluuFederation/oxTrust/issues/347)
- 'Generate' method in SAML Trust relationship throwing NPE[368](https://github.com/GluuFederation/oxTrust/issues/368)
- Wrong name is displayed for backend in "Change password" dialogue[376](https://github.com/GluuFederation/oxTrust/issues/376)
- No left/right scroll bar with sized down window[379](https://github.com/GluuFederation/oxTrust/issues/379)
- Deactivated SAML TR is activated as side-effect of clicking "Update" button[384](https://github.com/GluuFederation/oxTrust/issues/384)
- "System error" upon attempt to create user via oxTrust on freshly installed instance[447](https://github.com/GluuFederation/oxTrust/issues/447)
- List of SAML TRs doesn't show the actual status of its displayed items.[385](https://github.com/GluuFederation/oxTrust/issues/385)
- 2.4.4.2: It's impossible to remove entries from "Logout URI" property of OIDC client.[470](https://github.com/GluuFederation/oxTrust/issues/470)
- SAML TR added without custom RP configuration doesn't work[490](https://github.com/GluuFederation/oxTrust/issues/490)
- dynamicRegistrationExpirationTime cannot be set to 0[508](https://github.com/GluuFederation/oxTrust/issues/508)
- Federation TR's creation/editing page lacks critical controls and can't be edited[515](https://github.com/GluuFederation/oxTrust/issues/515)
- Use servers which are in 'Manage Authentication' list[525](https://github.com/GluuFederation/oxTrust/issues/525)
#### Community Edition
- apache2 does not start with "service apache2 ..."[#324](https://github.com/GluuFederation/community-edition-setup/issues/324)
- Some minor security issues in current packages.[#315](https://github.com/GluuFederation/community-edition-setup/issues/315)
- CentOS/RHEL 7.x resolv.conf is becoming blank after VM reboot[#295](https://github.com/GluuFederation/community-edition-setup/issues/295)
- Failed to stop Gluu services properly in RHEL 6.7[#272](https://github.com/GluuFederation/community-edition-setup/issues/272)
- Wrong user:group during rsyslog configuraion[#271](https://github.com/GluuFederation/community-edition-setup/issues/271)
- Don't update /etc/hosts in old dist[#270](https://github.com/GluuFederation/community-edition-setup/issues/270)
- OpenDJ schema is broken[#259](https://github.com/GluuFederation/community-edition-setup/issues/259)
- Hostname is changed outside of the container each time Gluu service is started[#198](https://github.com/GluuFederation/community-edition-setup/issues/198)
- Gluu Server does not SSL connection for localhost (prevents oxd from working on the same machine where Gluu Server installed)[#157](https://github.com/GluuFederation/community-edition-setup/issues/157)
- missing LSB information[#57](https://github.com/GluuFederation/community-edition-setup/issues/57)
