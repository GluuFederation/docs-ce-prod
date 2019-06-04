# oxTrust JSON Configurations
## Overview
This page explains the oxTrust JSON Configuration which can by found by navigating to `Configuration` > `JSON Configuration`. 

## oxtrust.properties
![image](../img/reference/config-json_oxtrustpropertiesv4.png)

The following fields are available for edit in the menu.

| Fields/Attributes | Description |
| ------------------|-------------|
| baseDN | The base distinguished name of oxtrust. The default is `o=gluu` |
| orgIname | This can be left blank |
| orgSupportEmail | The support email address of the Gluu Server installation |
| applianceInum | The [INUM][inum] of the appliance |
| applianceUrl | The [URI][uri] of the appliance |
| baseEndpoint | | 
| schemaAddObjectClassWithAttributeTypesDefinition | The schema to add various attribute types |
| schemaAddObjectClassWithoutAttributeTypesDefinition | The schema to add various attribute types |

## personObjectClassTypes
This class holds the relation between the person entry and its relative object class.

| Fields/Attributes | Description |
| ------------------|-------------|
| item 1 | inetOrgPerson |
| item 2 | gluuPerson |
| personCustomObjectClass| |

## personObjectClassDisplayNames
This class holds the relation between the display name of the person and the relative object class.

| Fields/Attributes | Description |
| ------------------|-------------|
| item 1 | inetOrgPerson |
| item 2 | gluuPerson |
| schemaAddAttributeDefenition | | 

## contactObjectClassDisplayNames 

Items can be added under this class by clicking on the `+ item` button.

| Fields/Attributes | Description |
| ------------------|-------------|
| photoRepositoryRootDir | Path to the root directory of photographs |
| photoRepositoryThumbWidth | thumb width of a photo |
| photoRepositoryThumbHeight | sets the thumb height of a photo |
| photoRepositoryCountLevels | count level per photo repository |
| photoRepositoryCountFoldersPerLevel | number of folders per level |
| authMode | set this tag to `basic` to use basic authentication or leave it blank to use oxAuth |
| ldifStore | Path to the [LDIF][ldif] store |
| shibboleth2IdpRootDir | root directory for the shibboleth plugin |
| shibboleth2SpConfDir | Configuration directory for the shibboleth plugin |
| pokenApplicationSecret | |
| updateAplicanceStatus | update appliance state for the site. Use `true` to allow, and `false` to forbid (default value) |
| svnConfigurationStoreRoot | Root of the [SVN][svn] configuration store |
| svnConfigurationStorePassword | Password of the [SVN][svn] configuration store |
| keystorePath | Path to the keystore |
| keystorePassword | Password to the keystore |
| allowPersonModification | Enables or disables the allowance to modify a person entry. Use `true` to allow (default value), and  `false` otherwise |
| idpUrl | [uri][uri] of the [OpenID][openid] provider that is in use |
| velocityLog | Velocity log filename with path |
| spMetadataPath | Path to the Gluu Server metadata |
| logoLocation | Directory name for the images and logos that are used |
| idpSecurityKey | Security key of the [OpenID][openid] provider |
| idpSecurityKeyPassowrd | Security password of the [OpenID][openid] provider |
| idpSecurityCert | Security certificate of the machine |

## gluuSpAttributes
Items can be added here by clicking on the `+ item` button.

| Fields/Attributes | Description |
| ------------------|-------------|
| configGeneration | This entry controls the automatic generation of the configuration files. Use `enable` to allow and `disable` otherwise |
| idpLdapProtocol | Protocol used by the [LDAP][ldap] server |
| idpLdapServer | Hostname of the [LDAP][ldap] server with port |
| orgInum | [INUM][inum] of the organization |
| idpBindDn | Domain name of the [OpenID][openid] provider |
| idpBindPassowrd | Password for the [OpenID][openid] provider |
| idpUserFields | |
| gluuSpCert | Certificate name and location of the Gluu Server |
| mysqlUrl | MySql connector as [URI][uri] |
| mysqlUser | Username for the MySql server |
| mysqlPassword | Passowrd for the MySql server |
| shibboleth2FederationRootDir | Root directory for the [Shobboleth][shibboleth] federation plugin |
| cacheRefreshEnabled | Value of the cache refresh mechanism. Use `true` to enable and `false` otherwise |
| cacheRefreshIntervalMinutes | Time in minutes counting down to next cache-refresh event |
| caCertsLocation | Keystore to use for downloaded [SSL][ssl] certificates |
| caCertsPassphrase | Password for the caCerts keystore |
| tempCertDir | Temporary location for certificates while certificate update procedure |
| certDir | Locaiton of certificates used in configuration files |
| servicesRestartTrigger | Location of the file which will restart the applicance server if deleted |
| persistSVN | State of persistence in [SVN][svn]. Use `true` to enable or `false` otherwise |
| oxAuthAuthorizeUrl | Authorization [URI][uri] for oxAuth |
| oxAuthTokenUrl | Token [URI][uri] for oxAuth |
| oxAuthValidateTokenUrl | [URI][uri] for oxAuth token validation |
| oxAuthEndSessionUrl | [URI][uri] for oxAuth session termination |
| oxAuthLogoutUrl | [URI][uri] for logging out of oxAuth |
| oxAuthTokenValidationUrl | [URI][uri] for oxAuth token validation |
| oxAuthUserInfo | [URI][uri] for oxAuth user information |
| oxAuthSectorIdentifierUrl | [URI][uri] for oxAuth sector identifier |
| oxAuthClientId | Identification number for oxAuth client |
| oxAuthClientPassowrd | Password for oxAuth client |
| oxAuthClientScope | Scope of the oxAuth client |
| loginRedirectUrl | Redirect [URI][uri] for oxAuth |
| logoutRedirectUrl | [URI][uri] for oxAuth | 

## clusteredInums
Items can be added here by clicking on the `+ item` button.

| Fields/Attributes | Description |
| ------------------|-------------|
| clientAssociationAttribute | Attribute which identifies the [OpenID][openid] client |
| oxAuthIssuers | [URI][uri] of the issuer authorization server |
| ignoreValidation | Control to check/ignore token validation. Use `true` to validate or `false` otherwise|
| umaIssuer | [URI][uri] of the issuer authorization server |
| scimUmaClientId | Identification of the [UMA][uma] client |
| scimUmaClientKeyId | | 
| scimUmaResourceId | |
| scimUmaScope | Scopes available for this resource |
| scimUmaClientKeyStoreFile| |
| scimUmaClientKeyStorePassword| |
| passportUmaClientId| |
| passportUmaClientKeyId| |
| passportUmaResourceID | |
| passportUmaScope| |
| passportUmaClientKeyStoreFile | |
| recaptchaSiteKey | |
| recaptchaSecretKey | |
| cssLocation | Path to the CSS files |
| jsLocation | Path to the JS files |
| metricReporterInterval | The interval for metric reporter in seconds |
| metricReporterKeepDataDays| The number of days to keep metric reported data |
| metricReporterEnabled | Boolean value specifying whether to enable Metric Reporter |
| rptConnectionPoolUseConnectionPooling |
| rptConnectionPoolMaxTotal | |
| rptConnectionPoolDefaultMaxPerRoute | |
| rptConnectionPoolValidateAfterInactivity | |
| rptConnectionPoolCustomKeepAliveTimeout | |
| scimTestMode | |
| shibbolethVersion | |
| shibboleth3ldpRootDir | |
| shibboleth3SpConfDir | |
| organizationName | |
| idp3SigningCert | |
| idp3EncryptionCert | |
| disableJdkLogger | Boolean value specifying whether to disable JDK loggers |
| passwordResetRequestExpirationTime | Expiration time in secionds for password reset requests |
| cleanServiceInterval | Time interval for the Clean Service in seconds |

### clientWhiteList

This list details the whitelisted client redirection URIs

### clientBlackList

This list details the blacklisted client redirection URIs

### Scim Properties



[inum]: https://en.wikipedia.org/wiki/INum_Initiative "INUM definition in wikipedia"
[uri]: https://en.wikipedia.org/wiki/Uniform_Resource_Identifier "Uniform Resource Identifier"
[ldif]: https://en.wikipedia.org/wiki/LDAP_Data_Interchange_Format "LDAP Data Interchange Format"
[svn]: https://en.wikipedia.org/wiki/Apache_Subversion "Apache Subversion"
[openid]: https://en.wikipedia.org/wiki/OpenID "OpenID Connect"
[shibboleth]: https://en.wikipedia.org/wiki/Shibboleth_%28Internet2%29 "Shibboleth"
[ssl]: https://en.wikipedia.org/wiki/Transport_Layer_Security "Secure Sockets Layer"
[uma]: https://en.wikipedia.org/wiki/User-Managed_Access "User-Managed Access"


### Description of OxTrust Properties

Description of OxTrust Properties can be viewed [here](../reference/oxtrust-prop.json)

Oxtrust import JSON description [here](../reference/oxtrust-import-person.json)
