# Notice

This document, also known as the Gluu Release Note, 
relates to the Gluu Release versioned 3.1.0. The work is licensed under “The MIT License” 
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

The document is released with the Version 3.1.0 of the Gluu Software. The purpose of this document is to provide the changes made/new features included in this release of the Gluu Software. The list is not exhaustive and there might be some omission of negligible issues, but the noteworthy features, enhancements and fixes are covered. 

## Background

The Gluu Server is a free open source identity and access management (IAM) platform. The Gluu Server is a container distribution composed of software written by Gluu and incorporated from other open source projects. 

The most common use cases for the Gluu Server include single sign-on (SSO), mobile authentication, API access management, two-factor authentication, customer identity and access management (CIAM) and identity federation.

## Documentation

Please visit the [Gluu Documentation Page](http://www.gluu.org/docs) for the complete 
documentation and administrative guide. 

## Components included in Gluu Server CE 3.1.0
- oxAuth, oxTrust,oxCore v3.1.0
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

## What's new in version 3.1.0

### New Features
#### oxAuth
- Migration to Weld 3.0.0.CR2[#221](https://github.com/GluuFederation/oxAuth/issues/221)
- UMA 2: Implement Claims Gathering Endpoint[#300](https://github.com/GluuFederation/oxAuth/issues/300)
- JWT Session Support[#142](https://github.com/GluuFederation/oxAuth/issues/142)
- Issue new RPT as JWT for each authorization request[#145](https://github.com/GluuFederation/oxAuth/issues/145)
- Support OAuth2 Token Exchange Format[#116](https://github.com/GluuFederation/oxAuth/issues/116)
- Cache Refresh should run update with thread priority slower than main process[#482](https://github.com/GluuFederation/oxAuth/issues/482)
- Super-Gluu script should support AWS SNS for push notifications[#630](https://github.com/GluuFederation/oxAuth/issues/630)
- Error handling in 3.1.x[#504](https://github.com/GluuFederation/oxAuth/issues/504)
- UMA 2 : support plain scopes[#536](https://github.com/GluuFederation/oxAuth/issues/536)
- UMA 2 : introduce/upgrade metadata according to UMA 2 spec[#534](https://github.com/GluuFederation/oxAuth/issues/534)
- UMA 2 : Implement support for client "pushed claims" and PCT[#533](https://github.com/GluuFederation/oxAuth/issues/533)
- UMA 2 : Remove AAT[#532](https://github.com/GluuFederation/oxAuth/issues/532)
- UMA 2 : Remove GAT Tokens[#531](https://github.com/GluuFederation/oxAuth/issues/531)
- Improve entropy of Session Cookie value[#17](https://github.com/GluuFederation/oxAuth/issues/317)
- Scope Internationalization[#311](https://github.com/GluuFederation/oxAuth/issues/311)
#### oxTrust
- UMA 2 : added "claims_redirect_uris" to client.[#593](https://github.com/GluuFederation/oxTrust/issues/593)
- UMA 2 : Introduce new "UMA Claims Gathering Script"[#590](https://github.com/GluuFederation/oxTrust/issues/590)
- JSF-related changes in SAML pages[#611](https://github.com/GluuFederation/oxTrust/issues/611)
- Add FluentD support[#589](https://github.com/GluuFederation/oxTrust/issues/589)
- UMA 2 Scopes : Adapt oxTrust code according to scopes changes in oxAuth[#573](https://github.com/GluuFederation/oxTrust/issues/573)
- Support TR without Metadata[#353](https://github.com/GluuFederation/oxTrust/issues/353)
- Allow add index to custom attribute[#325](https://github.com/GluuFederation/oxTrust/issues/325)
- Handle coversation timeout[#626](https://github.com/GluuFederation/oxTrust/issues/626)
- Make SCIM 2.0 search MAX_COUNT configurable[#320](https://github.com/GluuFederation/oxTrust/issues/320)
- Import / Export Schema[#392](https://github.com/GluuFederation/oxTrust/issues/392)
- More user-friendly look of the OIDC client configuration page[#226](https://github.com/GluuFederation/oxTrust/issues/226)
- Make cache provider configurable via UI (oxCacheConfiguration attribute of gluuAppliance OS)[#485](https://github.com/GluuFederation/oxTrust/issues/485)
- CR should support different mapping for each backend[#373](https://github.com/GluuFederation/oxTrust/issues/373)
- Localization of oxTrust UI[#506](https://github.com/GluuFederation/oxAuth/issues/506#issue-223064367)
- Migration to Weld 3.0.0[#567](https://github.com/GluuFederation/oxTrust/issues/567)
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
- Duo not working[#628](https://github.com/GluuFederation/oxAuth/issues/628)
- Consent screen can throw NPE after timeout[#627](https://github.com/GluuFederation/oxAuth/issues/627)
- java.lang.IllegalStateException: Counter for nested ContextualHttpServletRequest was removed before it should be![#626](https://github.com/GluuFederation/oxAuth/issues/626)
- Not able to register profile, email scope[#624](https://github.com/GluuFederation/oxAuth/issues/624)
- basic_multi_auth script not loading[#623](https://github.com/GluuFederation/oxAuth/issues/623)
- OTP ( hotp ) not working[#620](https://github.com/GluuFederation/oxAuth/issues/620)
- OpenID Dynamic Client Registration is failing[#615](https://github.com/GluuFederation/oxAuth/issues/615)
- U2F Authentication not working[#613](https://github.com/GluuFederation/oxAuth/issues/613)
- Super Gluu is broken[#608](https://github.com/GluuFederation/oxAuth/issues/608)
- Cert authentication is broken[#607](https://github.com/GluuFederation/oxAuth/issues/607)
- [Gluu 3.0.2] Error 500 on login with grant_type = password and bad password[#604](https://github.com/GluuFederation/oxAuth/issues/604)
- Custom Authentication (U2F, Super Gluu, Basic change password)  not working[#599](https://github.com/GluuFederation/oxAuth/issues/599)
- Update oxauth-rp home.xhtml to fix claimsRedirectUris issue[#597](https://github.com/GluuFederation/oxAuth/issues/597)
- Why it is client secret is always required in token request Api?[#590](https://github.com/GluuFederation/oxAuth/issues/590)
- oxAuth should initialize custom scripts in separate thread[#588](https://github.com/GluuFederation/oxAuth/issues/588)
- Cyclic redirect when there are 2 pages with same name but in different folders[#587](https://github.com/GluuFederation/oxAuth/issues/587)
- Fix DisplaysPolicyUriInLoginPage test[#583](https://github.com/GluuFederation/oxAuth/issues/583)
- setAmrClaim() in IdTokenFactory.java only allows scripts with usage type of "Both methods", instead of allowing scripts of any type[#582](https://github.com/GluuFederation/oxAuth/issues/582)

#### oxTrust
- SAML TRs cannot be created in web UI[#648](https://github.com/GluuFederation/oxTrust/issues/648)
- JSF 2.2 and navigation.xml review after page.xml convertion[#613](https://github.com/GluuFederation/oxTrust/issues/613)
- Cache Refresh (CR) not working[#647](https://github.com/GluuFederation/oxTrust/issues/647)
- User profile is not displayed in Oxtrust[#644](https://github.com/GluuFederation/oxTrust/issues/644)
- Unable to Add users via oxTrust[#643](https://github.com/GluuFederation/oxTrust/issues/643)
- Fix CR background job start[#640](https://github.com/GluuFederation/oxTrust/issues/640)
- SAML TR added without custom RP configuration doesn't work[#490](https://github.com/GluuFederation/oxTrust/issues/490)
- Can't add SAML TRs in web UI[#639](https://github.com/GluuFederation/oxTrust/issues/639)
- Custom Scripts fail to update[#637](https://github.com/GluuFederation/oxTrust/issues/637)
- Configure Log Viewer Error Message[#635](https://github.com/GluuFederation/oxTrust/issues/635)
- SAML TR unable to add attributes[#619](https://github.com/GluuFederation/oxTrust/issues/619)
- Import xls file not available[#618](https://github.com/GluuFederation/oxTrust/issues/618)
- Several JSF-related exceptions in 3.1.0 blocks usage[#591](https://github.com/GluuFederation/oxTrust/issues/591)
- Issues with SMTP server configuration[#608](https://github.com/GluuFederation/oxTrust/issues/608)
- Issues with password reset feature[#607](https://github.com/GluuFederation/oxTrust/issues/607)
- Fix UMA scope validation logic for id[#582](https://github.com/GluuFederation/oxTrust/issues/582)
- Passport authentication displayed (but not default acr or oxTrust acr)[#677](https://github.com/GluuFederation/oxTrust/issues/677)
- change "Default" to "Allow for dynamic client registration"[#676](https://github.com/GluuFederation/oxTrust/issues/676)
- User registration not working[#659](https://github.com/GluuFederation/oxTrust/issues/659)
- Custom nameid functionality requires update[#620](https://github.com/GluuFederation/oxTrust/issues/620)
- List of SAML TRs doesn't show the actual status of its displayed items.[#385](https://github.com/GluuFederation/oxTrust/issues/385)
- Deactivated SAML TR is activated as side-effect of clicking "Update" button[#384](https://github.com/GluuFederation/oxTrust/issues/384)
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