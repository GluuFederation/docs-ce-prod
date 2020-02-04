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

## Lifecycle

Status: Active Release

| Released | Community EOL | Enterprise EOL |
| --- | --- | --- |
| November 2018 | April 2020 | April 2021 |

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
- Support for OpenID Connect Token Binding
- Support JWT access tokens
- LDAP passwords migration from BCRYPT to SSHA
- Configure JWT for access tokens on a per client basis
- Persist client authorizations


## Fixes / Enhancements

### [GluuFederation/oxAuth](https://github.com/GluuFederation/oxAuth/issues?utf8=?&q=is%3Aissue+milestone%3A3.1.4+)

- [#910](https://github.com/GluuFederation/oxAuth/issues/910) Authorization Endpoint does not respect expired access_token

- [#908](https://github.com/GluuFederation/oxAuth/issues/908) Changing "accessTokenLifetime" nside Configuration Doesn't impact Access Token Lifetime

- [#907](https://github.com/GluuFederation/oxAuth/issues/907) OTP doesn't work in centos6

- [#905](https://github.com/GluuFederation/oxAuth/issues/905) Issues with Passport custom script's SAML branch

- [#899](https://github.com/GluuFederation/oxAuth/issues/899) Cache clean service remove active Unathenticated Sessions

- [#898](https://github.com/GluuFederation/oxAuth/issues/898) Remove URL remove rewrite servlet dependecy

- [#897](https://github.com/GluuFederation/oxAuth/issues/897) Blocked account starts countdown again

- [#892](https://github.com/GluuFederation/oxAuth/issues/892) Extra string on OTP login screen

- [#891](https://github.com/GluuFederation/oxAuth/issues/891) Extra string on OTP login screen

- [#889](https://github.com/GluuFederation/oxAuth/issues/889) Introspect endpoint has to return 401 https status code instead of 400 in case of invalid authorization header

- [#887](https://github.com/GluuFederation/oxAuth/issues/887) No info about blocked account

- [#885](https://github.com/GluuFederation/oxAuth/issues/885) Error Message on Login page must appear in one place

- [#881](https://github.com/GluuFederation/oxAuth/issues/881) Implement token expiration logic for password reset

- [#880](https://github.com/GluuFederation/oxAuth/issues/880) Enhance password reset email

- [#879](https://github.com/GluuFederation/oxAuth/issues/879) Weird password reset message

- [#878](https://github.com/GluuFederation/oxAuth/issues/878) Dead link in Super Gluu login

- [#877](https://github.com/GluuFederation/oxAuth/issues/877) No info about blocked account

- [#875](https://github.com/GluuFederation/oxAuth/issues/875) Add better handling for session expired events

- [#874](https://github.com/GluuFederation/oxAuth/issues/874) SuperGluu screen throws error

- [#873](https://github.com/GluuFederation/oxAuth/issues/873) Add backwards compatibility configuration switch

- [#871](https://github.com/GluuFederation/oxAuth/issues/871) Twilio phone error

- [#870](https://github.com/GluuFederation/oxAuth/issues/870) OTP login failure -- 2 error messages

- [#867](https://github.com/GluuFederation/oxAuth/issues/867) Review the ui_locales param (Authentication Request)

- [#866](https://github.com/GluuFederation/oxAuth/issues/866) Unwanted http redirection

- [#864](https://github.com/GluuFederation/oxAuth/issues/864) Customized logo should apply to every public facing pages

- [#863](https://github.com/GluuFederation/oxAuth/issues/863) Update lock account to include expiration

- [#862](https://github.com/GluuFederation/oxAuth/issues/862) Add brute force protection to default password authentication

- [#852](https://github.com/GluuFederation/oxAuth/issues/852) Introspection response must return `scope` instead of `scopes`.

- [#851](https://github.com/GluuFederation/oxAuth/issues/851) Fixing broken server side tests for 3.1.4

- [#850](https://github.com/GluuFederation/oxAuth/issues/850) New FIDO configuration endpoint

- [#846](https://github.com/GluuFederation/oxAuth/issues/846) Combined Super Gluu / SMS authn script

- [#845](https://github.com/GluuFederation/oxAuth/issues/845) Broken server side test marked as successfull

- [#844](https://github.com/GluuFederation/oxAuth/issues/844) UMA Scope Expression evaluator

- [#843](https://github.com/GluuFederation/oxAuth/issues/843) Expiration with session

- [#840](https://github.com/GluuFederation/oxAuth/issues/840) OpenID Connect Token Bound Authentication 1.0

- [#837](https://github.com/GluuFederation/oxAuth/issues/837) Different clients must receive a different sub value also when the sector identifier is the same

- [#836](https://github.com/GluuFederation/oxAuth/issues/836) Certification for the FormPost Response Mode Implementation

- [#834](https://github.com/GluuFederation/oxAuth/issues/834) Remove the sign up link present in the login page for passport

- [#833](https://github.com/GluuFederation/oxAuth/issues/833) Set default values for RPT and PCT expiration

- [#832](https://github.com/GluuFederation/oxAuth/issues/832) JKS expiration should be checked

- [#831](https://github.com/GluuFederation/oxAuth/issues/831) A few issues with OIDC logout flow

- [#829](https://github.com/GluuFederation/oxAuth/issues/829) It is possible to invoke refresh_token flow with access_token (instead of refresh_token)

- [#826](https://github.com/GluuFederation/oxAuth/issues/826) UMA 2 : Fix NPE if required claims_redirect_uri is not passed

- [#824](https://github.com/GluuFederation/oxAuth/issues/824) UMA : Introduce separate ticket lifetime configuration

- [#821](https://github.com/GluuFederation/oxAuth/issues/821) Remove hardcoded code from passport page

- [#820](https://github.com/GluuFederation/oxAuth/issues/820) Stack trace on 'Failed to load session from LDAP'

- [#819](https://github.com/GluuFederation/oxAuth/issues/819) UMA 2 : restrict access to resource by associated client (make it configurable)

- [#817](https://github.com/GluuFederation/oxAuth/issues/817) Add startSession and endSession methods to application_session script

- [#816](https://github.com/GluuFederation/oxAuth/issues/816) Review the prepareForStep method of passport social script

- [#812](https://github.com/GluuFederation/oxAuth/issues/812) Restrict requesting claims individually

- [#807](https://github.com/GluuFederation/oxAuth/issues/807) OTP 2FA / enrollment page + login page

- [#803](https://github.com/GluuFederation/oxAuth/issues/803) "acr_values" contains "null" in introspection endpoint's response

- [#802](https://github.com/GluuFederation/oxAuth/issues/802) NPE during end_session if client is expired and does not exist in LDAP anymore

- [#801](https://github.com/GluuFederation/oxAuth/issues/801) Getting NullPointerException whlie authorizing user

- [#799](https://github.com/GluuFederation/oxAuth/issues/799) If custom script getPageForStep throws error Authenticator shoudl redirect to error page

- [#798](https://github.com/GluuFederation/oxAuth/issues/798) Relax log level when claims gathering script name is blank

- [#797](https://github.com/GluuFederation/oxAuth/issues/797) Implemented migration password script from BCRYPT to SSHA

- [#796](https://github.com/GluuFederation/oxAuth/issues/796) User should be redirect to error page instead of login when an exception occurs during external authentication

- [#791](https://github.com/GluuFederation/oxAuth/issues/791) Dynamic Registration: Minor request - add new info logger

- [#787](https://github.com/GluuFederation/oxAuth/issues/787) Supply more external methods for client operations

- [#778](https://github.com/GluuFederation/oxAuth/issues/778) Update crypto-js to latest version

- [#773](https://github.com/GluuFederation/oxAuth/issues/773) Persist Client Authorizations

- [#769](https://github.com/GluuFederation/oxAuth/issues/769) Restore authentication script parameters from session with right simple java type

- [#764](https://github.com/GluuFederation/oxAuth/issues/764) Create oxAuth JSON property to disable fido u2f endpoints

- [#753](https://github.com/GluuFederation/oxAuth/issues/753) Create Authorization Script to check BCrypt Hash

- [#745](https://github.com/GluuFederation/oxAuth/issues/745) Allow user to select type of cookie used by oxAuth

- [#654](https://github.com/GluuFederation/oxAuth/issues/654) Add support of "old" caching mode 'LDAP'

- [#638](https://github.com/GluuFederation/oxAuth/issues/638) Allow configuration of JWT for access token on a per client basis

- [#562](https://github.com/GluuFederation/oxAuth/issues/562) Made PAT configurable for introspection_endpoint  protection

- [#230](https://github.com/GluuFederation/oxAuth/issues/230) Resource Owner Password Credential Grant Interception Script

### [GluuFederation/oxTrust](https://github.com/GluuFederation/oxTrust/issues?utf8=?&q=is%3Aissue+milestone%3A3.1.4+)

- [#1277](https://github.com/GluuFederation/oxTrust/issues/1277) Dropdown for SCIM Attribute shouldn't have "SCIM Attribute"

- [#1276](https://github.com/GluuFederation/oxTrust/issues/1276) Enhance icons for multivalued Attributes

- [#1274](https://github.com/GluuFederation/oxTrust/issues/1274) Too many popups for already used reset pwd email

- [#1272](https://github.com/GluuFederation/oxTrust/issues/1272) Adjust metric changes

- [#1270](https://github.com/GluuFederation/oxTrust/issues/1270) Logo inconsistency

- [#1268](https://github.com/GluuFederation/oxTrust/issues/1268) Problems with public-facing pages

- [#1265](https://github.com/GluuFederation/oxTrust/issues/1265) Change button location in Cache Refresh

- [#1259](https://github.com/GluuFederation/oxTrust/issues/1259) oxtrust allows user to delete email and username

- [#1257](https://github.com/GluuFederation/oxTrust/issues/1257) Issues when adding several redirect_uri for an OIDC client's entry

- [#1255](https://github.com/GluuFederation/oxTrust/issues/1255) Make logo on password reminder page customizable

- [#1252](https://github.com/GluuFederation/oxTrust/issues/1252) Captcha on Forgot password

- [#1250](https://github.com/GluuFederation/oxTrust/issues/1250) Fix Manage authetication captcha

- [#1248](https://github.com/GluuFederation/oxTrust/issues/1248) Make Registration page logo customizable

- [#1246](https://github.com/GluuFederation/oxTrust/issues/1246) Pressing Enter in Any Field For Organization Configuration Will Default to SMTP

- [#1242](https://github.com/GluuFederation/oxTrust/issues/1242) Change User password from profile page don't take effect

- [#1239](https://github.com/GluuFederation/oxTrust/issues/1239) Change Bind Password under "Manage Authentication" not working

- [#1238](https://github.com/GluuFederation/oxTrust/issues/1238) It is not possible to set oxIdTokenTokenBindingCnf client property via oxTrust (required for Token Binding)

- [#1235](https://github.com/GluuFederation/oxTrust/issues/1235) Unify button color

- [#1234](https://github.com/GluuFederation/oxTrust/issues/1234) Password reset UI enhancements

- [#1233](https://github.com/GluuFederation/oxTrust/issues/1233) Buggy preview

- [#1231](https://github.com/GluuFederation/oxTrust/issues/1231) Unable to change OIDC client secret

- [#1228](https://github.com/GluuFederation/oxTrust/issues/1228) User registration not working when captcha is enabled

- [#1227](https://github.com/GluuFederation/oxTrust/issues/1227) Change password expiration time

- [#1226](https://github.com/GluuFederation/oxTrust/issues/1226) Adjust space Log viewer configuration

- [#1224](https://github.com/GluuFederation/oxTrust/issues/1224) Fix mail expiration message

- [#1222](https://github.com/GluuFederation/oxTrust/issues/1222) User registration is failing

- [#1218](https://github.com/GluuFederation/oxTrust/issues/1218) Update of pre-installed client fail with Oops page

- [#1216](https://github.com/GluuFederation/oxTrust/issues/1216) Adjust Cache Refresh fields

- [#1214](https://github.com/GluuFederation/oxTrust/issues/1214) User registration has Test too tip field

- [#1213](https://github.com/GluuFederation/oxTrust/issues/1213) Disappearing error button

- [#1210](https://github.com/GluuFederation/oxTrust/issues/1210) Export Attribute | Add Export button at top

- [#1208](https://github.com/GluuFederation/oxTrust/issues/1208) Adding password ( popup ) from CR config - oxTrust crashing

- [#1207](https://github.com/GluuFederation/oxTrust/issues/1207) Placeholders not cleared & keys editable

- [#1205](https://github.com/GluuFederation/oxTrust/issues/1205) Center string in registration page

- [#1204](https://github.com/GluuFederation/oxTrust/issues/1204) Correct strings in Oops page

- [#1203](https://github.com/GluuFederation/oxTrust/issues/1203) SCIM Group creation or update returns the same member list provided in input

- [#1200](https://github.com/GluuFederation/oxTrust/issues/1200) Password reset mail should inform user about the expiration time

- [#1198](https://github.com/GluuFederation/oxTrust/issues/1198) Add QA identifiers

- [#1197](https://github.com/GluuFederation/oxTrust/issues/1197) Add new method getBindCredentials method to CR script to allow dynamically change AD password

- [#1195](https://github.com/GluuFederation/oxTrust/issues/1195) Users import should support custom attribute too

- [#1191](https://github.com/GluuFederation/oxTrust/issues/1191) Unify field/dropdown/radio button design

- [#1190](https://github.com/GluuFederation/oxTrust/issues/1190) Disappearing icons in Passport Authentication method

- [#1188](https://github.com/GluuFederation/oxTrust/issues/1188) User form misaligned

- [#1186](https://github.com/GluuFederation/oxTrust/issues/1186) Fix feature *Change user password**

- [#1180](https://github.com/GluuFederation/oxTrust/issues/1180) UMA resource fields moved to the right

- [#1178](https://github.com/GluuFederation/oxTrust/issues/1178) Validation of Import People causes error

- [#1174](https://github.com/GluuFederation/oxTrust/issues/1174) Extra string on OTP login screen

- [#1173](https://github.com/GluuFederation/oxTrust/issues/1173) Empty page in update OIDC client

- [#1172](https://github.com/GluuFederation/oxTrust/issues/1172) Not able to add user

- [#1171](https://github.com/GluuFederation/oxTrust/issues/1171) Email validation on add user screen

- [#1169](https://github.com/GluuFederation/oxTrust/issues/1169) Ubuntu 16 - Oxtrust - no option to add password in "Add User"

- [#1164](https://github.com/GluuFederation/oxTrust/issues/1164) Messed up checkboxes in Register Attribute

- [#1163](https://github.com/GluuFederation/oxTrust/issues/1163) Unable to add custom attribute in openDJ

- [#1158](https://github.com/GluuFederation/oxTrust/issues/1158) align "remove source server" in CR Source Backend server tab

- [#1157](https://github.com/GluuFederation/oxTrust/issues/1157) Attribute mapping entries on Cache Refresh becomes empty

- [#1156](https://github.com/GluuFederation/oxTrust/issues/1156) Setting OIDC expiration date to 2099 delete the client few minutes after update

- [#1153](https://github.com/GluuFederation/oxTrust/issues/1153) Persistent placeholders, no ^ v symbols

- [#1152](https://github.com/GluuFederation/oxTrust/issues/1152) Weird password reset message

- [#1151](https://github.com/GluuFederation/oxTrust/issues/1151) Enhance password reset email

- [#1150](https://github.com/GluuFederation/oxTrust/issues/1150) Unable to add/update same Login Redirect URL or Post Logout URL in Gluu server

- [#1148](https://github.com/GluuFederation/oxTrust/issues/1148) Unable to create TR from "Federation" Entity Type

- [#1146](https://github.com/GluuFederation/oxTrust/issues/1146) oxTrust Auditing Log Fixes

- [#1145](https://github.com/GluuFederation/oxTrust/issues/1145) No info about blocked account

- [#1144](https://github.com/GluuFederation/oxTrust/issues/1144) Dead link in Super Gluu login page

- [#1143](https://github.com/GluuFederation/oxTrust/issues/1143) custom scripts levels  all in zero

- [#1140](https://github.com/GluuFederation/oxTrust/issues/1140) Login fails after switching back to auth_ldap_server method

- [#1139](https://github.com/GluuFederation/oxTrust/issues/1139) Admin password can be seen when adding person

- [#1138](https://github.com/GluuFederation/oxTrust/issues/1138) Email validation on Edit profile page

- [#1137](https://github.com/GluuFederation/oxTrust/issues/1137) Register attribute page fields are misaligned

- [#1131](https://github.com/GluuFederation/oxTrust/issues/1131) Bugged user search validation

- [#1129](https://github.com/GluuFederation/oxTrust/issues/1129) Fix typo

- [#1126](https://github.com/GluuFederation/oxTrust/issues/1126) Scopes Not Appearing While Adding New OpenID Client

- [#1122](https://github.com/GluuFederation/oxTrust/issues/1122) "Enter your client id here" and "Enter your client secret here" must be placeholders Passport strategies

- [#1120](https://github.com/GluuFederation/oxTrust/issues/1120) Cache refresh

- [#1117](https://github.com/GluuFederation/oxTrust/issues/1117) Change user password feature not working

- [#1116](https://github.com/GluuFederation/oxTrust/issues/1116) Error when editing existing user

- [#1115](https://github.com/GluuFederation/oxTrust/issues/1115) Validate user email when adding new new via Admin Ui

- [#1109](https://github.com/GluuFederation/oxTrust/issues/1109) Impossible to add new user via admin Ui

- [#1103](https://github.com/GluuFederation/oxTrust/issues/1103) Hide Client secret on OpenID Connect page

- [#1099](https://github.com/GluuFederation/oxTrust/issues/1099) Gender field should be a dropdown on Profile page, User add/Update Page

- [#1092](https://github.com/GluuFederation/oxTrust/issues/1092) Enhance error message

- [#1091](https://github.com/GluuFederation/oxTrust/issues/1091) Placeholder instead of Build Number

- [#1090](https://github.com/GluuFederation/oxTrust/issues/1090) Email validation in System Configuration

- [#1083](https://github.com/GluuFederation/oxTrust/issues/1083) Client secret expires in...?

- [#1082](https://github.com/GluuFederation/oxTrust/issues/1082) Weird Client Secret behavior

- [#1081](https://github.com/GluuFederation/oxTrust/issues/1081) Clear search fields

- [#1080](https://github.com/GluuFederation/oxTrust/issues/1080) Uncaught TypeError

- [#1079](https://github.com/GluuFederation/oxTrust/issues/1079) Unify upload interface

- [#1078](https://github.com/GluuFederation/oxTrust/issues/1078) Attribute import message

- [#1077](https://github.com/GluuFederation/oxTrust/issues/1077) Offer means to create UMA resource and edit associated client

- [#1074](https://github.com/GluuFederation/oxTrust/issues/1074) View log tab should show the name of the current log file

- [#1073](https://github.com/GluuFederation/oxTrust/issues/1073) Fix misleading oxMemCache-Config title

- [#1072](https://github.com/GluuFederation/oxTrust/issues/1072) Move captcha setting to "Manage Authentication" into new tab

- [#1071](https://github.com/GluuFederation/oxTrust/issues/1071) Reset password form should has captcha

- [#1070](https://github.com/GluuFederation/oxTrust/issues/1070) Update base libs

- [#1068](https://github.com/GluuFederation/oxTrust/issues/1068) Typo in Cache Refresh configuration page

- [#1064](https://github.com/GluuFederation/oxTrust/issues/1064) Uploading org_logo and org_favicon is throwing error / not uploading

- [#1061](https://github.com/GluuFederation/oxTrust/issues/1061) add search to oxtrust attribute page

- [#1060](https://github.com/GluuFederation/oxTrust/issues/1060) editing attribute has unacceptable value for "multivalued" by default

- [#1056](https://github.com/GluuFederation/oxTrust/issues/1056) Remove Level feature from Cache Refresh config

- [#1053](https://github.com/GluuFederation/oxTrust/issues/1053) Fix duplicate source server name:

- [#1051](https://github.com/GluuFederation/oxTrust/issues/1051) Validate contact values entered in openID clients form

- [#1048](https://github.com/GluuFederation/oxTrust/issues/1048) The button to remove Source Ldap Server under LDAP Manage Authentication don't shows up on every screen.

- [#1043](https://github.com/GluuFederation/oxTrust/issues/1043) Manage LDAP Authentication duplicated name

- [#1041](https://github.com/GluuFederation/oxTrust/issues/1041) oxTrust Auditing

- [#1040](https://github.com/GluuFederation/oxTrust/issues/1040) Pretty Print OpenID Client Config

- [#1037](https://github.com/GluuFederation/oxTrust/issues/1037) Remove requiredness for streetAddress in scim

- [#1033](https://github.com/GluuFederation/oxTrust/issues/1033) Error message on logout from client side

- [#1032](https://github.com/GluuFederation/oxTrust/issues/1032) Non-Fatal Error in oxTrust "SecurityEvaluationException"

- [#1028](https://github.com/GluuFederation/oxTrust/issues/1028) Oxtrust allow to update user with duplicate uid when users are created through SCIM

- [#1027](https://github.com/GluuFederation/oxTrust/issues/1027) Lists at "Manage Sector Identifiers" pages are skewed

- [#1025](https://github.com/GluuFederation/oxTrust/issues/1025) Remove the sign up link present in the login page for passport

- [#1024](https://github.com/GluuFederation/oxTrust/issues/1024) Add i18n support to passwordReminder.xhtml

- [#1020](https://github.com/GluuFederation/oxTrust/issues/1020) Add clientID and clientSecret rows by  default in passport

- [#1018](https://github.com/GluuFederation/oxTrust/issues/1018) New redis configuration ssl parameters support

- [#1014](https://github.com/GluuFederation/oxTrust/issues/1014) Ability to Disable Gathering Of Metrics

- [#1012](https://github.com/GluuFederation/oxTrust/issues/1012) The notification bubble that appears after updating the manage authentication seems a little off

- [#1011](https://github.com/GluuFederation/oxTrust/issues/1011) Better Button Locations in OpenID Connect Client Configuration

- [#1009](https://github.com/GluuFederation/oxTrust/issues/1009) The person import feature thrown error when the excel file upload has been created via a recent Excel version

- [#1007](https://github.com/GluuFederation/oxTrust/issues/1007) All file upload features in Gluu 3.1.3 don't works

- [#1002](https://github.com/GluuFederation/oxTrust/issues/1002) Adding organization logo throw an exception

- [#996](https://github.com/GluuFederation/oxTrust/issues/996) Log login initator exception with TRACE level only

- [#975](https://github.com/GluuFederation/oxTrust/issues/975) Password Reset: Reset link should be send only if the provide email exists in LDAP

- [#970](https://github.com/GluuFederation/oxTrust/issues/970) OTP 2FA / enrollment page + login page

- [#966](https://github.com/GluuFederation/oxTrust/issues/966) Validate sector_identifier_uri on Create/Update Client

- [#953](https://github.com/GluuFederation/oxTrust/issues/953) Auto-generate client secret

- [#952](https://github.com/GluuFederation/oxTrust/issues/952) log statements of level lower than INFO not shown after start

- [#949](https://github.com/GluuFederation/oxTrust/issues/949) Relax requiredness for attributes in oxtrust's user form?

- [#941](https://github.com/GluuFederation/oxTrust/issues/941) Replace Apache Velocity with Apache FreeMarker

- [#913](https://github.com/GluuFederation/oxTrust/issues/913) Move texts from xhtml/java into oxtrust_en.properties

- [#907](https://github.com/GluuFederation/oxTrust/issues/907) In Add Person form user is not able to navigate to next input field by pressing the [Tab] button in keyboard

- [#865](https://github.com/GluuFederation/oxTrust/issues/865) Use JSON Logic GUI to display scope expression

- [#808](https://github.com/GluuFederation/oxTrust/issues/808) Remove UMA > "Add Resource" Button

- [#703](https://github.com/GluuFederation/oxTrust/issues/703) Update OpenID Client page to support JWT access tokens

- [#557](https://github.com/GluuFederation/oxTrust/issues/557) Improve Passport.js user experience

### [GluuFederation/oxShibboleth](https://github.com/GluuFederation/oxShibboleth/issues?utf8=?&q=is%3Aissue+milestone%3A3.1.4+)

- [#44](https://github.com/GluuFederation/oxShibboleth/issues/44) Update Idp to V3.3.3

- [#43](https://github.com/GluuFederation/oxShibboleth/issues/43) eduPerson schema update

### [GluuFederation/gluu-passport](https://github.com/GluuFederation/gluu-passport/issues?utf8=?&q=is%3Aissue+milestone%3A3.1.4+)

- [#45](https://github.com/GluuFederation/gluu-passport/issues/45) HTTP ERROR 404 on /oxauth/postlogin

- [#44](https://github.com/GluuFederation/gluu-passport/issues/44) login.errorSessionInvalidMessage after changing passport-saml-config.json

- [#43](https://github.com/GluuFederation/gluu-passport/issues/43) Cannot find modules errors when starting passport

- [#41](https://github.com/GluuFederation/gluu-passport/issues/41) Support multivalued attributes

- [#40](https://github.com/GluuFederation/gluu-passport/issues/40) Build passport-node_modules.tar.gz during passport build

- [#39](https://github.com/GluuFederation/gluu-passport/issues/39) Introduce step 2 for passport flow

- [#38](https://github.com/GluuFederation/gluu-passport/issues/38) Rework flow and unify custom scripts

- [#37](https://github.com/GluuFederation/gluu-passport/issues/37) Bundle passport with openid connect support

- [#35](https://github.com/GluuFederation/gluu-passport/issues/35) `Error in parsing JSON in getJSON` in passport log at startup

- [#34](https://github.com/GluuFederation/gluu-passport/issues/34) Provide an easier way to upload a strategy logo

- [#32](https://github.com/GluuFederation/gluu-passport/issues/32) Make logging level a parameter in config file

- [#31](https://github.com/GluuFederation/gluu-passport/issues/31) NPE upon start when no strategies are defined

- [#25](https://github.com/GluuFederation/gluu-passport/issues/25) Log enhancement: declare missing resource ( lack of authN server )

- [#18](https://github.com/GluuFederation/gluu-passport/issues/18) Passport should POST user data to /oxauth/postlogin

- [#14](https://github.com/GluuFederation/gluu-passport/issues/14) Updating certain inbound attributes showing errors in log

- [#12](https://github.com/GluuFederation/gluu-passport/issues/12) Re-attempt to get oxAuth metadata and token

- [#11](https://github.com/GluuFederation/gluu-passport/issues/11) Passport should return non zero exit code on startup errors

### [GluuFederation/community-edition-setup](https://github.com/GluuFederation/community-edition-setup/issues?utf8=?&q=is%3Aissue+milestone%3A3.1.4+)

- [#484](https://github.com/GluuFederation/community-edition-setup/issues/484) Build development package for CE

- [#481](https://github.com/GluuFederation/community-edition-setup/issues/481) low level creation of users with duplicate uids possible

- [#480](https://github.com/GluuFederation/community-edition-setup/issues/480) Update some scripts

- [#479](https://github.com/GluuFederation/community-edition-setup/issues/479) Hide LDAP selection typy if there is only one option

- [#477](https://github.com/GluuFederation/community-edition-setup/issues/477) Fix typo in installation progress

- [#475](https://github.com/GluuFederation/community-edition-setup/issues/475) Passport not started after 3.1.4 installation

- [#474](https://github.com/GluuFederation/community-edition-setup/issues/474) running setup.py shows IP address instead of hostname as default option

- [#473](https://github.com/GluuFederation/community-edition-setup/issues/473) Hide asimba in installation summary

- [#470](https://github.com/GluuFederation/community-edition-setup/issues/470) Updater should enable http-forwarder

- [#469](https://github.com/GluuFederation/community-edition-setup/issues/469) Use a real world value for OTP lookAheadWindow

- [#468](https://github.com/GluuFederation/community-edition-setup/issues/468) Passport Strategies are missing when migration from 3.1.2 to 3.1.3

- [#467](https://github.com/GluuFederation/community-edition-setup/issues/467) Create index for oxUmaResourcePermission & oxTicket

- [#465](https://github.com/GluuFederation/community-edition-setup/issues/465) Adjust, add or update all files required for Gluu Casa

- [#464](https://github.com/GluuFederation/community-edition-setup/issues/464) 2.4.4 to 3.1.x migration - custom attribute migration

- [#461](https://github.com/GluuFederation/community-edition-setup/issues/461) Build package with token binding module for apache2

- [#460](https://github.com/GluuFederation/community-edition-setup/issues/460) Passport installation should be offline

- [#455](https://github.com/GluuFederation/community-edition-setup/issues/455) Add scopes to cred-manager client only if they are not already defaulted in CE installation

- [#447](https://github.com/GluuFederation/community-edition-setup/issues/447) Shibboleth IDP client should have its own OpenID client creds

- [#444](https://github.com/GluuFederation/community-edition-setup/issues/444) rename  uma_client_authz_rpt_policy to scim_access_policy

- [#443](https://github.com/GluuFederation/community-edition-setup/issues/443) RHEL based gluu-server container now showing any message

- [#440](https://github.com/GluuFederation/community-edition-setup/issues/440) 2.4.x to 3.1.3 upgrade ( OpenDJ --> OpenDJ ): don't export `100-user.ldif` schema

- [#439](https://github.com/GluuFederation/community-edition-setup/issues/439) OpenLDAP enabled Gluu to OpenDJ-Gluu upgrade: ldap search filter not updating

- [#437](https://github.com/GluuFederation/community-edition-setup/issues/437) Remove '99-user.ldif' schema related calling

- [#436](https://github.com/GluuFederation/community-edition-setup/issues/436) 3.0.x to 3.1.x upgrade: metadata-provider template broken

- [#427](https://github.com/GluuFederation/community-edition-setup/issues/427) Asimba should be available in 3.1.4 as deprecated commmonent only

- [#425](https://github.com/GluuFederation/community-edition-setup/issues/425) Setup should prepare CE to work with dynamic IP correctly

- [#420](https://github.com/GluuFederation/community-edition-setup/issues/420) Update node passport init.d script

- [#100](https://github.com/GluuFederation/community-edition-setup/issues/100) Ensure 'hostname' is not 'localhost' by default

### [GluuFederation/oxcore](https://github.com/GluuFederation/oxcore/issues?utf8=?&q=is%3Aissue+milestone%3A3.1.4+)

### [GluuFederation/SCIM-Client](https://github.com/GluuFederation/SCIM-Client/issues?utf8=?&q=is%3Aissue+milestone%3A3.1.4+)

- [#70](https://github.com/GluuFederation/SCIM-Client/issues/70) Add test cases for special chars handling

- [#69](https://github.com/GluuFederation/SCIM-Client/issues/69) Allow searching with startindex values higher than max_count

### [GluuFederation/gluu-asimba](https://github.com/GluuFederation/gluu-asimba/issues?utf8=?&q=is%3Aissue+milestone%3A3.1.4+)
