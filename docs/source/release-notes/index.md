## Notice

This document, also known as the Gluu Release Note, 
relates to the Gluu Server Release versioned 4.0. The work is licensed under “The MIT License” 
allowing the use, copy, modify, merge, publish, distribute, sub-license and sale without 
limitation and liability. This document extends only to the aforementioned release version 
in the heading.

UNLESS IT HAS BEEN EXPRESSLY AGREED UPON BY ANY WRITTEN AGREEMENT BEFOREHAND, 
THE WORK/RELEASE IS PROVIDED “AS IS”, WITHOUT ANY WARRANTY OR GUARANTEE OF ANY KIND 
EXPRESS OR IMPLIED. UNDER NO CIRCUMSTANCE, THE AUTHOR, OR GLUU SHALL BE LIABLE FOR ANY 
CLAIMS OR DAMAGES CAUSED DIRECTLY OR INDIRECTLY TO ANY PROPERTY OR LIFE WHILE INSTALLING 
OR USING THE RELEASE.

## Purpose

The document is released with the Version 4.0 of the Gluu Software. The purpose of this document is to provide the changes made/new features included in this release of the Gluu Software. The list is not exhaustive and there might be some omission of negligible issues, but the noteworthy features, enhancements and fixes are covered. 

## Background

The Gluu Server is a free open source identity and access management (IAM) platform. The Gluu Server is a container distribution composed of software written by Gluu and incorporated from other open source projects. 

The most common use cases for the Gluu Server include single sign-on (SSO), mobile authentication, API access management, two-factor authentication, customer identity and access management (CIAM) and identity federation.

## Documentation

Please visit the [Gluu Documentation Page](http://www.gluu.org/docs/ce) for the complete 
documentation and administrative guide. 

## Available components in Gluu Server 4.0
- oxAuth, oxTrust, oxCore v4.0
- Gluu OpenDJ v3.0.1
- Shibboleth v3.3.3
- Passport v4.0
- Java v1.8.0_112
- Node.js v9.9.0
- Jetty-distribution-9.4.12.v20180830
- Jython v2.7.2a
- Weld 3.0.0
- FluentD 3.5
- Redis

## New features

## Fixes / Enhancements

### [GluuFederation/oxAuth](https://github.com/GluuFederation/oxAuth/issues?utf8=?&q=is%3Aissue+milestone%3A4.0+)

- [#1058](https://github.com/GluuFederation/oxAuth/issues/1058) URL-Encoding problem when retrieving value of custom param of authz request

- [#1057](https://github.com/GluuFederation/oxAuth/issues/1057) Reported by GG: No permissions associated with ticket

- [#1055](https://github.com/GluuFederation/oxAuth/issues/1055) Allow to update key generator interval without server restart

- [#1052](https://github.com/GluuFederation/oxAuth/issues/1052) Resource Owner Password Credential Grant Interception Script Buggly Logic

- [#1047](https://github.com/GluuFederation/oxAuth/issues/1047) KeyGenerator should allow to specify expiration in hours instead of days

- [#1044](https://github.com/GluuFederation/oxAuth/issues/1044) Remove usages of Filter.create to create string-based filters

- [#1042](https://github.com/GluuFederation/oxAuth/issues/1042) Client authorization live in LDAP forever. Need to move it under client entity to clean it up

- [#1035](https://github.com/GluuFederation/oxAuth/issues/1035) Remove ou=session and from LDAP and static oxAuth configuration

- [#1034](https://github.com/GluuFederation/oxAuth/issues/1034) Fix NPE in RO Grant when client hasn't redirect_uri

- [#1033](https://github.com/GluuFederation/oxAuth/issues/1033) Change oxauth persistence model: Drop 'oxAuthGrant' objects from persistence and reduce load on ~30%

- [#1031](https://github.com/GluuFederation/oxAuth/issues/1031) Server does not track clients that take part in SSO if ACR is changed (flow 4, 4.0)

- [#1021](https://github.com/GluuFederation/oxAuth/issues/1021) Move attributes mapping logic out of passport scripts

- [#1020](https://github.com/GluuFederation/oxAuth/issues/1020) Adjust passport scripts to conform to new configuration structure

- [#1007](https://github.com/GluuFederation/oxAuth/issues/1007) CIBA: Update Discovery Metadata

- [#995](https://github.com/GluuFederation/oxAuth/issues/995) invalid_grant_and_session, wrong description?

- [#983](https://github.com/GluuFederation/oxAuth/issues/983) Prepare successful 4.0 oxauth build before go on with new features

- [#982](https://github.com/GluuFederation/oxAuth/issues/982) OB: OAuth 2.0 Mutual TLS Client Authentication and Certificate Bound Access Tokens

- [#957](https://github.com/GluuFederation/oxAuth/issues/957) Remove completely authorization by 'access_token' from Authorization Endpoint

- [#950](https://github.com/GluuFederation/oxAuth/issues/950) Align claims in id_token and Userinfo

- [#946](https://github.com/GluuFederation/oxAuth/issues/946) Support OAuth MTLS Client Authentication and Certificate Bound Access Tokens

- [#894](https://github.com/GluuFederation/oxAuth/issues/894) 'loginPage' value

- [#884](https://github.com/GluuFederation/oxAuth/issues/884) Don't return refresh token if client doesn't have refresh_token grant

- [#847](https://github.com/GluuFederation/oxAuth/issues/847) Bouncycastle throw ClassCastException after upgrade to 1.59

- [#841](https://github.com/GluuFederation/oxAuth/issues/841) Bug: extra error string

- [#813](https://github.com/GluuFederation/oxAuth/issues/813) CleanupTimer has to run in own connection pool to not effect oxauth performance

- [#784](https://github.com/GluuFederation/oxAuth/issues/784) Add support for Token Revocation

- [#767](https://github.com/GluuFederation/oxAuth/issues/767) Could you add these authorization code request and response sections in a future version of oxauth-rp

- [#748](https://github.com/GluuFederation/oxAuth/issues/748) UMA RPT Policy evaluator: if no policies it grants access. We have to make it configurable (e.g. deny instead of grant)

- [#734](https://github.com/GluuFederation/oxAuth/issues/734) 'uniqueIdentifier' removal in replicated server / clustered Gluu Server

- [#678](https://github.com/GluuFederation/oxAuth/issues/678) Couchbase Support

- [#602](https://github.com/GluuFederation/oxAuth/issues/602) Update client resets grant-types if it has no value

- [#548](https://github.com/GluuFederation/oxAuth/issues/548) Add s_hash to id_Token

- [#480](https://github.com/GluuFederation/oxAuth/issues/480) acr_values router script

- [#413](https://github.com/GluuFederation/oxAuth/issues/413) Increase size of oxAuth-rp text areas

- [#313](https://github.com/GluuFederation/oxAuth/issues/313) Support Proof of Possession Tokens

- [#308](https://github.com/GluuFederation/oxAuth/issues/308) Support JWT Token Revocation

- [#267](https://github.com/GluuFederation/oxAuth/issues/267) IDP Initiated Authentication Script

- [#207](https://github.com/GluuFederation/oxAuth/issues/207) User Review of Persistent Client Scope Authorizations

### [GluuFederation/oxTrust](https://github.com/GluuFederation/oxTrust/issues?utf8=?&q=is%3Aissue+milestone%3A4.0+)

- [#1616](https://github.com/GluuFederation/oxTrust/issues/1616) Adapt oxTrust to oxAuth scope changes

- [#1612](https://github.com/GluuFederation/oxTrust/issues/1612) Calendar popup for Date type attributes

- [#1611](https://github.com/GluuFederation/oxTrust/issues/1611) Couchbase: can't access OpenId Scopes and Clients page

- [#1610](https://github.com/GluuFederation/oxTrust/issues/1610) Couchbase & LDAP: Can't access passport pages

- [#1608](https://github.com/GluuFederation/oxTrust/issues/1608) Attribute disappears from the list if administrator is forbidden to edit it

- [#1605](https://github.com/GluuFederation/oxTrust/issues/1605) oxTrust RS code (passport, scim, oxtrust-api) must set scopes for protection

- [#1603](https://github.com/GluuFederation/oxTrust/issues/1603) Some UI Fixes

- [#1600](https://github.com/GluuFederation/oxTrust/issues/1600) Error showing certificates list

- [#1599](https://github.com/GluuFederation/oxTrust/issues/1599) OIDC revamp

- [#1598](https://github.com/GluuFederation/oxTrust/issues/1598) gluu4 build -24, redundant/typo on client -> encryption/signing tab

- [#1597](https://github.com/GluuFederation/oxTrust/issues/1597) viewing new client opens to last tab viewed of previous client

- [#1596](https://github.com/GluuFederation/oxTrust/issues/1596) OIDC client view screen squished with long redirect URIs

- [#1594](https://github.com/GluuFederation/oxTrust/issues/1594) 4.0 QA: Error in User Registration

- [#1582](https://github.com/GluuFederation/oxTrust/issues/1582) Email Validation Wrong Message Displayed

- [#1579](https://github.com/GluuFederation/oxTrust/issues/1579) Password/Confirm Password Validation shown for all mandatory fields

- [#1576](https://github.com/GluuFederation/oxTrust/issues/1576) Add new clean configuration properties in oxTrust

- [#1574](https://github.com/GluuFederation/oxTrust/issues/1574) Remove deprecated linktrack code and pages

- [#1573](https://github.com/GluuFederation/oxTrust/issues/1573) Oops error when showing an UMA resource with associated client deleted

- [#1572](https://github.com/GluuFederation/oxTrust/issues/1572) When displaying a sector identifier check if the clients assign to it are still present in LDAP

- [#1562](https://github.com/GluuFederation/oxTrust/issues/1562) Move some log line from INFO level to DEBUG level

- [#1560](https://github.com/GluuFederation/oxTrust/issues/1560) Old configuration properties clean up

- [#1558](https://github.com/GluuFederation/oxTrust/issues/1558) Merge some 3.1.6 commit manually into master

- [#1552](https://github.com/GluuFederation/oxTrust/issues/1552) Remove Asimba GUI and API 

- [#1538](https://github.com/GluuFederation/oxTrust/issues/1538) Move existing api code into master

- [#1536](https://github.com/GluuFederation/oxTrust/issues/1536) Create a module for oxtrust_api

- [#1534](https://github.com/GluuFederation/oxTrust/issues/1534) Add form for IDP-initiating flow configuration

- [#1533](https://github.com/GluuFederation/oxTrust/issues/1533) Revamp form for providers management configuration

- [#1532](https://github.com/GluuFederation/oxTrust/issues/1532) Add form for passport configuration management

- [#1531](https://github.com/GluuFederation/oxTrust/issues/1531) Create passport forms as needed

- [#1530](https://github.com/GluuFederation/oxTrust/issues/1530) Refactor passport configuration endpoint

- [#1512](https://github.com/GluuFederation/oxTrust/issues/1512) Client: add ability to specify client attributes as JSON

- [#1510](https://github.com/GluuFederation/oxTrust/issues/1510) Fix compilation error on Jenkins build

- [#1490](https://github.com/GluuFederation/oxTrust/issues/1490) Improvements in sector identifier and redirect uri assignment in oxTrust UI

- [#1483](https://github.com/GluuFederation/oxTrust/issues/1483) Fix security issue

- [#1481](https://github.com/GluuFederation/oxTrust/issues/1481) Move to Java 1.8

- [#1471](https://github.com/GluuFederation/oxTrust/issues/1471) OIDC clients get deleted by cleanUp services

- [#1470](https://github.com/GluuFederation/oxTrust/issues/1470) Fix Password Reset

- [#1469](https://github.com/GluuFederation/oxTrust/issues/1469) Fix certificates issue

- [#1468](https://github.com/GluuFederation/oxTrust/issues/1468) Error while adding TR

- [#1467](https://github.com/GluuFederation/oxTrust/issues/1467) Error while adding OIDC scope

- [#1466](https://github.com/GluuFederation/oxTrust/issues/1466) Regular expression never evaluate on attribute named userPassword

- [#1461](https://github.com/GluuFederation/oxTrust/issues/1461) Couchbase with multiple buckets

- [#1332](https://github.com/GluuFederation/oxTrust/issues/1332) Should localhost be allowed in redirect uri for clients?

- [#1291](https://github.com/GluuFederation/oxTrust/issues/1291) Show All Attributes shows error page

- [#1290](https://github.com/GluuFederation/oxTrust/issues/1290) Impossible to add new TR

- [#1289](https://github.com/GluuFederation/oxTrust/issues/1289) Impossible to add new User

- [#1106](https://github.com/GluuFederation/oxTrust/issues/1106) OpenID client auto-generated password is not cryptographically strong

- [#1088](https://github.com/GluuFederation/oxTrust/issues/1088) SMTP Server configuration are not saved

- [#998](https://github.com/GluuFederation/oxTrust/issues/998) SCIM2 filter code should build filter graph to allow to convert it in any filter type

- [#992](https://github.com/GluuFederation/oxTrust/issues/992) Use automate tests to test API instead of manual testing

- [#935](https://github.com/GluuFederation/oxTrust/issues/935) Server Log API

- [#934](https://github.com/GluuFederation/oxTrust/issues/934) Server Status API

- [#933](https://github.com/GluuFederation/oxTrust/issues/933) oxAuth configuration API

- [#932](https://github.com/GluuFederation/oxTrust/issues/932) oxTrust configuration API

- [#931](https://github.com/GluuFederation/oxTrust/issues/931) Registration API

- [#930](https://github.com/GluuFederation/oxTrust/issues/930) Custom scripts API

- [#929](https://github.com/GluuFederation/oxTrust/issues/929) Certificates API

- [#928](https://github.com/GluuFederation/oxTrust/issues/928) Attributes API

- [#927](https://github.com/GluuFederation/oxTrust/issues/927) Authentication Method API

- [#926](https://github.com/GluuFederation/oxTrust/issues/926) Organization profile API

- [#925](https://github.com/GluuFederation/oxTrust/issues/925) Personal profile API

- [#924](https://github.com/GluuFederation/oxTrust/issues/924) Users API - People

- [#923](https://github.com/GluuFederation/oxTrust/issues/923) Users API - Groups

- [#922](https://github.com/GluuFederation/oxTrust/issues/922) CAS API

- [#921](https://github.com/GluuFederation/oxTrust/issues/921) UMA API

- [#920](https://github.com/GluuFederation/oxTrust/issues/920) OpenID Connect API

- [#919](https://github.com/GluuFederation/oxTrust/issues/919) SAML - Asimba API

- [#918](https://github.com/GluuFederation/oxTrust/issues/918) SAML - TrustRelationship API

- [#820](https://github.com/GluuFederation/oxTrust/issues/820) Verify user's memberOf is synced when group members are changed via SCIM

- [#815](https://github.com/GluuFederation/oxTrust/issues/815) Show Modality according to requirement

- [#812](https://github.com/GluuFederation/oxTrust/issues/812) Rename @protected SCIM annotation to @ScimProtectedApi

- [#803](https://github.com/GluuFederation/oxTrust/issues/803) Protect oxTrust APIs by UMA

- [#786](https://github.com/GluuFederation/oxTrust/issues/786) Cover oxTrust API by tests

- [#785](https://github.com/GluuFederation/oxTrust/issues/785) Cover all oxTrust GUI by oxTrust API

- [#784](https://github.com/GluuFederation/oxTrust/issues/784) Prepare working prototype which demonstrates oxTrust API

- [#783](https://github.com/GluuFederation/oxTrust/issues/783) Prepare client/server code to protect oxTrust API endpoints using UMA

- [#762](https://github.com/GluuFederation/oxTrust/issues/762) Expose APIs for everything

- [#758](https://github.com/GluuFederation/oxTrust/issues/758) Couchbase Support

- [#697](https://github.com/GluuFederation/oxTrust/issues/697) Gluu Server memory usage (3.1.0)

- [#551](https://github.com/GluuFederation/oxTrust/issues/551) Remove ou=appliances

### [GluuFederation/oxShibboleth](https://github.com/GluuFederation/oxShibboleth/issues?utf8=?&q=is%3Aissue+milestone%3A4.0+)

- [#35](https://github.com/GluuFederation/oxShibboleth/issues/35) Create authentication flow to replace RemoteUser flow 

- [#30](https://github.com/GluuFederation/oxShibboleth/issues/30) SAML metadata is not processing properly 

- [#25](https://github.com/GluuFederation/oxShibboleth/issues/25) Don't show stacktrace 

- [#24](https://github.com/GluuFederation/oxShibboleth/issues/24) SLO binding links are breaking IDP metadata

- [#16](https://github.com/GluuFederation/oxShibboleth/issues/16) /opt/shibboleth-idp/metadata/idp-metadata.xml (No such file or directory) 

- [#5](https://github.com/GluuFederation/oxShibboleth/issues/5) Override Logout Functionality 

### [GluuFederation/gluu-passport](https://github.com/GluuFederation/gluu-passport/issues?utf8=?&q=is%3Aissue+milestone%3A4.0+)

- [#60](https://github.com/GluuFederation/gluu-passport/issues/60) Add a cache provider when inResponseTo validation is used in a clustered environment

- [#46](https://github.com/GluuFederation/gluu-passport/issues/46) More verbose and explicit error message than "Go back and register!" on failures

- [#19](https://github.com/GluuFederation/gluu-passport/issues/19) Passport should support dynamic mapping

- [#4](https://github.com/GluuFederation/gluu-passport/issues/4) Rename repo to oxPassport

### [GluuFederation/community-edition-setup](https://github.com/GluuFederation/community-edition-setup/issues?utf8=?&q=is%3Aissue+milestone%3A4.0+)

- [#529](https://github.com/GluuFederation/community-edition-setup/issues/529) Fix Couchbase indexes creation

- [#528](https://github.com/GluuFederation/community-edition-setup/issues/528) UMA org units must be created during installation

- [#527](https://github.com/GluuFederation/community-edition-setup/issues/527) Generate initial JWKS with expiration time 'keyRegenerationInterval' + 'idTokenLifetime'

- [#526](https://github.com/GluuFederation/community-edition-setup/issues/526) Ubuntu 16 uninstall - apt purge removing opt directory

- [#525](https://github.com/GluuFederation/community-edition-setup/issues/525) Replace python 2.7 with python 3.x

- [#522](https://github.com/GluuFederation/community-edition-setup/issues/522) Remove orgInum, applianceInum, and Inum from RDN

- [#520](https://github.com/GluuFederation/community-edition-setup/issues/520) Disable OpenDJ JMX connection handler

- [#519](https://github.com/GluuFederation/community-edition-setup/issues/519) Remove Asimba and OpenLDAP support

- [#518](https://github.com/GluuFederation/community-edition-setup/issues/518) LDAP schema is broken

- [#512](https://github.com/GluuFederation/community-edition-setup/issues/512) Create the passport configuration upon installation only?

- [#511](https://github.com/GluuFederation/community-edition-setup/issues/511) Move passport configuration to LDAP

- [#509](https://github.com/GluuFederation/community-edition-setup/issues/509) Ask user to select jdk 8 or 11 in experimental mode

- [#508](https://github.com/GluuFederation/community-edition-setup/issues/508) Implement systemctl scripts for CentOS 7

- [#507](https://github.com/GluuFederation/community-edition-setup/issues/507) Migrate gluu-server startup scripts to systemctl

- [#501](https://github.com/GluuFederation/community-edition-setup/issues/501) Modification in 101-ox.ldif schema for birthdate

- [#489](https://github.com/GluuFederation/community-edition-setup/issues/489) Create static inums

- [#483](https://github.com/GluuFederation/community-edition-setup/issues/483) Typo when restarting the Gluu Server

- [#462](https://github.com/GluuFederation/community-edition-setup/issues/462) Support Ubuntu 18.04.1 and deprecate 14.04 support

- [#457](https://github.com/GluuFederation/community-edition-setup/issues/457) Gluu is vulnerable to BEAST

- [#453](https://github.com/GluuFederation/community-edition-setup/issues/453) Remove Asimba from Options Dialogue

- [#452](https://github.com/GluuFederation/community-edition-setup/issues/452) Couchbase should not listen by default on all server IPs

- [#451](https://github.com/GluuFederation/community-edition-setup/issues/451) Don't prompt to install IDP if admin selected Couchbase as persistence DB

- [#450](https://github.com/GluuFederation/community-edition-setup/issues/450) Create additional Couchbase backends during install

- [#449](https://github.com/GluuFederation/community-edition-setup/issues/449) Command to import LDIF into Couchbase

- [#448](https://github.com/GluuFederation/community-edition-setup/issues/448) Improve Couchbase up-checking method

- [#445](https://github.com/GluuFederation/community-edition-setup/issues/445) IDP Script runs before OpenDJ causing issues

- [#438](https://github.com/GluuFederation/community-edition-setup/issues/438) OpenLDAP replication in Gluu 3.1.3 is taking too much time to sync changes

- [#431](https://github.com/GluuFederation/community-edition-setup/issues/431) Authentication scripts' levels need to be updated

- [#423](https://github.com/GluuFederation/community-edition-setup/issues/423) 3.0.2 -> 3.1.2 upgrade / custom branding for login not working

- [#412](https://github.com/GluuFederation/community-edition-setup/issues/412) Automate package updates

- [#361](https://github.com/GluuFederation/community-edition-setup/issues/361) Upgrade: LDAP data import too slow

- [#360](https://github.com/GluuFederation/community-edition-setup/issues/360) In setup script: allow selection of LDAP or Couchbase as the database

- [#358](https://github.com/GluuFederation/community-edition-setup/issues/358) Getting 404 for '.well-known/simple-web-discovery' endpoint

- [#275](https://github.com/GluuFederation/community-edition-setup/issues/275) Configure firewall on host to open https port after installing CE

- [#170](https://github.com/GluuFederation/community-edition-setup/issues/170) Dockerizing Gluu Server

### [GluuFederation/SCIM-Client](https://github.com/GluuFederation/SCIM-Client/issues?utf8=?&q=is%3Aissue+milestone%3A4.0+)

- [#62](https://github.com/GluuFederation/SCIM-Client/issues/62) Add support for boolean custom attributes

- [#60](https://github.com/GluuFederation/SCIM-Client/issues/60) Service metadata endpoints must reject the presence of filter query param

- [#59](https://github.com/GluuFederation/SCIM-Client/issues/59) Wrong modeling of SearchRequest and its schema

- [#57](https://github.com/GluuFederation/SCIM-Client/issues/57) Bugs in filter functionality

- [#56](https://github.com/GluuFederation/SCIM-Client/issues/56) Refactor Bulk Operation service code

- [#54](https://github.com/GluuFederation/SCIM-Client/issues/54) Move SCIM-related oxtrust.properties inside the "ScimProperties" object

- [#53](https://github.com/GluuFederation/SCIM-Client/issues/53) Cases 10.2/10.3, delete a user with if-match etag

- [#52](https://github.com/GluuFederation/SCIM-Client/issues/52) Cases 7.2/7.3, retrieve a user with if-none-match etag

- [#51](https://github.com/GluuFederation/SCIM-Client/issues/51) Cases 5.13/5.14, update a user with if-match etag

- [#49](https://github.com/GluuFederation/SCIM-Client/issues/49) Case 6.3, add a value to a multi-valued attribute with PATCH

- [#48](https://github.com/GluuFederation/SCIM-Client/issues/48) Case 6.2, Update a multi-valued attribute with PATCH

- [#47](https://github.com/GluuFederation/SCIM-Client/issues/47) Case 6.1, Update a simple attribute with PATCH

- [#45](https://github.com/GluuFederation/SCIM-Client/issues/45) Cases 11.1/11.2, searching with POST /.search

- [#44](https://github.com/GluuFederation/SCIM-Client/issues/44) Cases 4.4/5.4/5.5/5.6, handling of immutable attribute

- [#43](https://github.com/GluuFederation/SCIM-Client/issues/43) Groups endpoint allows writing non-existing members

- [#42](https://github.com/GluuFederation/SCIM-Client/issues/42) Group assignment for users should be done at /Group not through /Users endpoint

- [#41](https://github.com/GluuFederation/SCIM-Client/issues/41) Adjust /Schemas endpoint impl to pick attributes characteristics automatically

- [#40](https://github.com/GluuFederation/SCIM-Client/issues/40) casa 8.11/8.12, retrieve a list of users with attributes query param (POST)

- [#39](https://github.com/GluuFederation/SCIM-Client/issues/39) Replace deprecated ProxyFactory usage in client code

- [#38](https://github.com/GluuFederation/SCIM-Client/issues/38) Cases 7.4/7.5 retrieve a user with attributes query param

- [#37](https://github.com/GluuFederation/SCIM-Client/issues/37) Cases 8.3/8.4, Retrieve a list of users with attributes query param

- [#36](https://github.com/GluuFederation/SCIM-Client/issues/36) Cases 5.8/5.9, update a user with attributes query param

- [#35](https://github.com/GluuFederation/SCIM-Client/issues/35) Cases 4.5/4.6, create a user with attributes query param

- [#34](https://github.com/GluuFederation/SCIM-Client/issues/34) Remove hard-coded list of ISO3166 countries

- [#33](https://github.com/GluuFederation/SCIM-Client/issues/33) Enhance ResourceTypes endpoint

- [#32](https://github.com/GluuFederation/SCIM-Client/issues/32) Add a logging framework

- [#31](https://github.com/GluuFederation/SCIM-Client/issues/31) Remove redundant code in authorization check for SCIM service

- [#30](https://github.com/GluuFederation/SCIM-Client/issues/30) Service does not handle properly the attributes/excludedAttributes parameters

- [#29](https://github.com/GluuFederation/SCIM-Client/issues/29) Add support for PATCH verb to service

- [#28](https://github.com/GluuFederation/SCIM-Client/issues/28) In user retrieval JSON response has the type attribute malformed for certain multi-valued attributes

- [#27](https://github.com/GluuFederation/SCIM-Client/issues/27) Creating and retrieval operations return unexpected attributes

- [#26](https://github.com/GluuFederation/SCIM-Client/issues/26) Validate locale attribute

- [#25](https://github.com/GluuFederation/SCIM-Client/issues/25) Validate timezone attribute
