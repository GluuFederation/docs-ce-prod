## Notice

This document, also known as the Gluu Release Note, 
relates to the Gluu Server Release versioned 3.1.3. The work is licensed under “The MIT License” 
allowing the use, copy, modify, merge, publish, distribute, sub-license and sale without 
limitation and liability. This document extends only to the aforementioned release version 
in the heading.

UNLESS IT HAS BEEN EXPRESSLY AGREED UPON BY ANY WRITTEN AGREEMENT BEFOREHAND, 
THE WORK/RELEASE IS PROVIDED “AS IS”, WITHOUT ANY WARRANTY OR GUARANTEE OF ANY KIND 
EXPRESS OR IMPLIED. UNDER NO CIRCUMSTANCE, THE AUTHOR, OR GLUU SHALL BE LIABLE FOR ANY 
CLAIMS OR DAMAGES CAUSED DIRECTLY OR INDIRECTLY TO ANY PROPERTY OR LIFE WHILE INSTALLING 
OR USING THE RELEASE.

## Purpose

The document is released with the Version 3.1.3 of the Gluu Software. The purpose of this document is to provide the changes made/new features included in this release of the Gluu Software. The list is not exhaustive and there might be some omission of negligible issues, but the noteworthy features, enhancements and fixes are covered. 

## Background

The Gluu Server is a free open source identity and access management (IAM) platform. The Gluu Server is a container distribution composed of software written by Gluu and incorporated from other open source projects. 

The most common use cases for the Gluu Server include single sign-on (SSO), mobile authentication, API access management, two-factor authentication, customer identity and access management (CIAM) and identity federation.

## Documentation

Please visit the [Gluu Documentation Page](http://www.gluu.org/docs/ce) for the complete 
documentation and administrative guide. 

## Available components in Gluu Server 3.1.3
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


## Fixes / Enhancements

### [GluuFederation/oxAuth](https://github.com/GluuFederation/oxAuth/issues?utf8=?&q=is%3Aissue+milestone%3A3.1.3+)

- [#785](https://github.com/GluuFederation/oxAuth/issues/785) ~Add support for CacheProvider/Redis authentication~

- [#755](https://github.com/GluuFederation/oxAuth/issues/755) ~Add creation and expiration dates to UMA resource entry~

- [#754](https://github.com/GluuFederation/oxAuth/issues/754) ~Add description and oxdID to client metadata~

- [#752](https://github.com/GluuFederation/oxAuth/issues/752) ~It seems oxAuth doesn't return claims in id_token when "response_type=id_token" is used~

- [#749](https://github.com/GluuFederation/oxAuth/issues/749) ~Enable client to restrict javascript origin~

- [#747](https://github.com/GluuFederation/oxAuth/issues/747) ~RPT introspection : we must keep it compatible with OAuth2 introspection and return seconds in exp~

- [#746](https://github.com/GluuFederation/oxAuth/issues/746) ~add client_id to RPT introspection~

- [#743](https://github.com/GluuFederation/oxAuth/issues/743) ~Add JSON property to enable admin to turn off authz for openid scope~

- [#739](https://github.com/GluuFederation/oxAuth/issues/739) ~Fix the list of scopes in the authorization page~

- [#738](https://github.com/GluuFederation/oxAuth/issues/738) ~Subject controlled scope~

- [#735](https://github.com/GluuFederation/oxAuth/issues/735) ~Allow to customize messages.properties~

- [#725](https://github.com/GluuFederation/oxAuth/issues/725) ~UmaRptIntrospectionService returning expiration time different than umaRptLifetime~

- [#664](https://github.com/GluuFederation/oxAuth/issues/664) ~Support extra parameters sent during UMA permission ticket request~

- [#519](https://github.com/GluuFederation/oxAuth/issues/519) ~Dynamic scope should contains list of allowed claims~

### [GluuFederation/oxTrust](https://github.com/GluuFederation/oxTrust/issues?utf8=?&q=is%3Aissue+milestone%3A3.1.3+)

- [#968](https://github.com/GluuFederation/oxTrust/issues/968) Added  Custom custom script don't behave as expected when the script name contains some character.

- [#908](https://github.com/GluuFederation/oxTrust/issues/908) ~Return 404 or 200 instead of 400 for SCIM fido search if user has no devices attached~

- [#907](https://github.com/GluuFederation/oxTrust/issues/907) ~In Add Person form user is not able to navigate to next input field by pressing the [Tab] button in keyboard~

- [#906](https://github.com/GluuFederation/oxTrust/issues/906) ~Selected Entity ID name and Change Entity ID link showing as a single link~

- [#903](https://github.com/GluuFederation/oxTrust/issues/903) ~Improve password reset functionality~

- [#877](https://github.com/GluuFederation/oxTrust/issues/877) ~Some meta information not retrieved via SCIM if user was not created or updated with the API itself~

- [#876](https://github.com/GluuFederation/oxTrust/issues/876) ~Increase upper limit on max_count for scim json property and adjust descriptive text~

- [#874](https://github.com/GluuFederation/oxTrust/issues/874) ~No certificate upload button available~

- [#872](https://github.com/GluuFederation/oxTrust/issues/872) ~Show Clients using UMA Scope~

- [#871](https://github.com/GluuFederation/oxTrust/issues/871) ~UMA scope Download/Link is 404~

- [#870](https://github.com/GluuFederation/oxTrust/issues/870) ~Make oxTrust Favicon standard Gluu transparent icosahedron~

- [#869](https://github.com/GluuFederation/oxTrust/issues/869) ~Re-login instead of displaying oops Page~

- [#868](https://github.com/GluuFederation/oxTrust/issues/868) ~Avoid execution of sorting if no sortBy param is specified in SCIM searches~

- [#866](https://github.com/GluuFederation/oxTrust/issues/866) ~'Add custom script configuration' drop down box~

- [#864](https://github.com/GluuFederation/oxTrust/issues/864) ~Display Resource creation date and associated RS~

- [#861](https://github.com/GluuFederation/oxTrust/issues/861) ~Overall user experience for adding a person by using the Add person form~

- [#860](https://github.com/GluuFederation/oxTrust/issues/860) ~GUI problems in Manage Authentication~

- [#858](https://github.com/GluuFederation/oxTrust/issues/858) ~Different lists on OIDC-related pages has remove controls' column skewed~

- [#857](https://github.com/GluuFederation/oxTrust/issues/857) ~Add 'server:port' instead of 'server' in Cache Refresh~

- [#854](https://github.com/GluuFederation/oxTrust/issues/854) ~Redirect URI delete icons don't line up~

- [#853](https://github.com/GluuFederation/oxTrust/issues/853) ~'Inbound' button available though 'Asimba' is false~

- [#850](https://github.com/GluuFederation/oxTrust/issues/850) ~AuthorizationProcessingFilter should check to which API client make an call~

- [#847](https://github.com/GluuFederation/oxTrust/issues/847) ~"SAML-> Configure Custom NameId" page uses confusing names for its controls~

- [#846](https://github.com/GluuFederation/oxTrust/issues/846) ~NameId form should update "saml-nameid.xml" too~

- [#845](https://github.com/GluuFederation/oxTrust/issues/845) ~SCIM interceptor script should implement postAddUser/postUpdateUser/postDeleteUser~

- [#844](https://github.com/GluuFederation/oxTrust/issues/844) ~UMA Resource Registration : Scope and Scope expression are mutually exclusive~

- [#842](https://github.com/GluuFederation/oxTrust/issues/842) ~Unable to remove multivalue attribute value in person form~

- [#841](https://github.com/GluuFederation/oxTrust/issues/841) ~Person form should display attribute mandatory correctly~

- [#818](https://github.com/GluuFederation/oxTrust/issues/818) ~Multi value Gluu Person attribute  delete  clears all value~

- [#787](https://github.com/GluuFederation/oxTrust/issues/787) ~oxTrust need to display and log explicit warnings about email non-uniqueness~

- [#748](https://github.com/GluuFederation/oxTrust/issues/748) ~Change data type "Photo" to "binary"~

### [GluuFederation/oxShibboleth](https://github.com/GluuFederation/oxShibboleth/issues?utf8=?&q=is%3Aissue+milestone%3A3.1.3+)

- [#42](https://github.com/GluuFederation/oxShibboleth/issues/42) ~generate ZIP file - attribute-map.xml - released attribute strings are not replaced~

- [#40](https://github.com/GluuFederation/oxShibboleth/issues/40) ~Error in relying-party.xml when "encryptNameIDs" set to "conditional"~

- [#39](https://github.com/GluuFederation/oxShibboleth/issues/39) ~Delete custom NameID from the GUI~

- [#38](https://github.com/GluuFederation/oxShibboleth/issues/38) ~Scope should use domain, not hostname~

- [#37](https://github.com/GluuFederation/oxShibboleth/issues/37) ~Shib configuration is trying to load 'openldap.crt' in 'gluu-openDJ' setup~

- [#36](https://github.com/GluuFederation/oxShibboleth/issues/36) ~Federated metadata is not loading in metadata-providers.xml~

### [GluuFederation/gluu-passport](https://github.com/GluuFederation/gluu-passport/issues?utf8=?&q=is%3Aissue+milestone%3A3.1.3+)

- [#10](https://github.com/GluuFederation/gluu-passport/issues/10) ~Readability of passport log~

### [GluuFederation/community-edition-setup](https://github.com/GluuFederation/community-edition-setup/issues?utf8=?&q=is%3Aissue+milestone%3A3.1.3+)

- [#419](https://github.com/GluuFederation/community-edition-setup/issues/419) ~Rebuild 3.1.2 RC2 with OpenDJ/Jython/Binaries update~

- [#418](https://github.com/GluuFederation/community-edition-setup/issues/418) ~Upgrade: permission of Shibb metadata after upgrade~

- [#417](https://github.com/GluuFederation/community-edition-setup/issues/417) ~Create tmpfile.d conf for jetty configuration~

### [GluuFederation/oxcore](https://github.com/GluuFederation/oxcore/issues?utf8=?&q=is%3Aissue+milestone%3A3.1.3+)

- [#75](https://github.com/GluuFederation/oxCore/issues/75) ~Fix redirect to app_script.log file after update Jython to 2.7.1~

- [#68](https://github.com/GluuFederation/oxCore/issues/68) ~Sorting in operations facade is operating upon an empty list, not actual result set~

### [GluuFederation/SCIM-Client](https://github.com/GluuFederation/SCIM-Client/issues?utf8=?&q=is%3Aissue+milestone%3A3.1.3+)

- [#68](https://github.com/GluuFederation/SCIM-Client/issues/68) ~Scim client - test source resources references UMA1 instead of uma2 discovery~

### [GluuFederation/gluu-asimba](https://github.com/GluuFederation/gluu-asimba/issues?utf8=?&q=is%3Aissue+milestone%3A3.1.3+)
