# oxTrust JSON Configurations

!!! Attention
    The official support end-of-life (EOL) date for Gluu Server 2.4.4 is December 31, 2018. Starting January 1, 2019, no further security updates or bug-fixes will be provided for Gluu Server 2.X. We strongly recommend [upgrading](https://gluu.org/docs/ce/upgrade/) to the newest version.

## Overview
This page explains the oxTrust JSON Configuration which can by found by navigating to `Configuration` > `JSON Configuration`. 

## oxtrust.properties
![image](../img/reference/config-json_oxtrustproperties.png)

The following fields are available for edit in the menu.

| Fields/Attributes | Description |
| ------------------|-------------|
| idpBindDn | The admin user of the ldap server|
| baseDN | The base doaim name of oxtrust. The default is `o=gluu` |
| orgIname | This can be left blank |
| orgSupportEmail | The support email address of the Gluu Server installation |
| applianceInum | The [INUM][inum] of the appliance |
| applianceUrl | The [URI][uri] of the appliance |
| baseEndpoint | | 
| schemaAddObjectClassWithAttributeTypesDefinition | The schema to add various attribute types |
| schemaAddObjectClassWithoutAttributeTypesDefinition | The schema to add various attribute types |

## personObjectClassTypes
This class holds the relation between the person entry and it's relative object class.

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
| photoRepositoryThumbWidth | thumb with a photo |
| photoRepositoryThumbheight | sets the thumb height of a photo |
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
| umaClientId | Identification of the [UMA][uma] client |
| umaClientKeyId | | 
| umaResourceId | |
| umaScope | Scopes available for this resource |
| recaptchaSiteKey | |
| recaptchaSecretKey | |
| cssLocation | Path to the CSS files |
| jsLocation | Path to the JS files |
| repactchUrl | Type for the recaptcha [URI][uri] attribute |

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
