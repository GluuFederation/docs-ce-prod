# oxTrust Configuration

oxTrust is a [JBoss][jboss] Seam application that provides
organizational cloud identity management services, including
[REST][rest] service endpoints and a user friendly cloud identity
management console aka a Graphical User Interface (GUI).

oxTrust is tightly coupled with [oxAuth][oxauth]. oxAuth configuration
is stored in [LDAP][ldap], and it would be hard to generate the right
configuration entries without oxTrust. The projects are separate
projects because in a high throughput cluster deployment, many oxAuth
servers are needed versus a few oxTrust instances.

## oxTrust Properties

The oxTrust has quite a few properties to control its behaviour. This
consists of general properties, [SVN][svn]-related properties as well as
display and authentication properties.

### General Properties

These properties control the general setup of oxTrust, and set several
appliance-specific variables.

 * __applianceInum__ sets the [INum][inum] of the appliance

 * __orgInum__ sets the [INum][inum] of the organization

 * __orgDisplayName__ holds the display name of the organization.

 * __orgShortName__ holds the short name of the organization.

 * __idp.url__ holds the uri of the [OpenID][openid] provider that is in use.

 * __appliance.url__ holds the uri of the appliance.

 * __keystore.path__ holds the path to the keystore.

 * __keystore.password__ holds the password to the keystore.

 * __person-objectClass-types__ holds the relation between the person 
   entry, and its according object class. An example value is
   `inetOrgPerson, gluuPerson`.

 * __person-objectClass-displayNames__ holds the relation between the
   display name of the person, and its according object class. An 
   example value is `inetOrgPerson, gluuPerson`.

### SVN-related Properties

The following properties define settings that are related to the
revision control system [SVN][svn].

 * __svn.configuration-store.root__ sets the root of the [SVN][svn]
   configuration store.

 * __svn.configuration-store.user__ sets the user name of the
   [SVN][svn] configuration store.

 * __svn.configuration-store.password__ sets the password of the 
   [SVN][svn] configuration store.

 * __person.allow-modification__ enables or disables the allowance to
   modify a person entry. Use `true` to allow (default value), and
   `false` to forbid.

 * __site.update-appliance-status__ change the update appliance state
   for the site. Use `true` to allow, and `false` to forbid (default
   value).

 * __persist-in-svn__ control the state of persistence in the
   [SVN][svn]. Use `true` to enable, and `false` to disable (default
   value).

 * __baseDN__ set the base domain name of oxTrust. The default value is
   `o=gluu`.

### Attribute Schema Definitions

The following properties define the schema to add various attribute
types.

 * __schema.add.attribute.attributeTypes__ `( %%s-oid NAME '%%s' EQUALITY caseIgnoreMatch ORDERING caseIgnoreOrderingMatch SUBSTR caseIgnoreSubstringsMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 USAGE userApplications X-SCHEMA-FILE '100-user.ldif' X-ORIGIN 'gluu' )`

 * __schema.add-without-attribute-types.objectClass.objectClasses__ `( %%s-oid NAME '%%s' SUP top STRUCTURAL MUST objectClass X-SCHEMA-FILE '100-user.ldif' X-ORIGIN 'gluu' )`

 * __schema.add-with-attribute-types.objectClass.objectClasses__ `( %%s-oid NAME '%%s' SUP top STRUCTURAL MUST objectClass MAY ( %%s ) X-SCHEMA-FILE '100-user.ldif' X-ORIGIN 'gluu' )`

### Display Properties

These properties refer to the visual settings of oxTrust.

 * __photo.repository.root-dir__ sets the path to the root directory of
   photographs. The default value is `/var/photos`.

 * __photo.repository.thumb-width__ sets the thumb with of a photo. 
   The default value is `300` pixels.

 * __photo.repository.thumb-height__ sets the thumb height of a photo.
   The default value is `300` pixels.

 * __photo.repository.count-levels__ sets the count level per photo
   repository. The default value is `3`.

 * __photo.repository.count-folders-per-level__ sets the number of
   folders per level. The default value is `20`.

 * __velocity.log__ this entry defines the filename in which the
   velocity logfile is kept. The default value is
   `/opt/tomcat/logs/velocity.log`.

 * __logo.location__ this entry defines the directory name for both the
   images, and the logos that are in use. The default value is
   `/var/photos`.

### Authentication Properties

These properties refer to the authentication settings of oxTrust.

 * __gluuSP.shared.attributes__ sets the shared attributes. The default
   value is `uid, mail, sn, givenName` that refer to the attributes user
   id, email address, short name, and the displayed name.

 * __gluuSP.metadata__ sets the path to the Gluu Server metadata. The
   default value is `/opt/idp/metadata`.

 * __shibboleth2.idp.root-dir__ sets the root directory for the
   [shibboleth][shibboleth] plugin. The default value is `/opt/idp`.

 * __shibboleth2.federation.root-dir__ sets the root directory for the
   [shibboleth][shibboleth] federation plugin. The default value is
   `/opt/shibboleth-federation`.

 * __shibboleth2.sp.conf-dir__ sets the configuration directory for the
   [shibboleth][shibboleth] plugin. The default value is `/etc/shibboleth`.

 * __configGeneration__ set this entry to control the automatic
   generation of the configuration file. Use `enabled` to allow that, 
   and `disabled` otherwise (default value).

 * __idp.securityCert__ holds the security certificate of the
   [OpenID][openid] provider.

 * __idp.securityKey__ holds the security key of the [OpenID][openid] provider.

 * __.securityCert__ holds the security certificate of the machine.

 * __idp.securityKeyPassword__ holds the security key password of the
   [OpenID][openid] provider.

 * __idp.bindDN__ holds the domain name the [OpenID][openid] provider is
   bound to.

 * __idp.bindPassword__ holds the password the [OpenID][openid] provider 
   is bound to.

 * __idp.useSSL__ enables or disables a secure connection via
   [SSL][ssl]. Use `true` to enable (default value), or `false` to disable
   the usage of [SSL][ssl].

 * __idp.ldap.server__ holds the name of OpenID [LDAP][ldap] server.

 * __mysql.url__ defines the MySQL connector as uri. The default value is
   `jdbc:mysql:///localhost` for the local machine using the JDBC driver.

 * __mysql.user__ defines the user name for the MySQL connection. The
   default value is `idp`.

 * __mysql.password__ defines the password for the MySQL connection. The
   default value is empty.

 * __ldifStoreDir__  defines the path to the [LDAP Data Interchange Format
   (LDIF)][ldif] store. The default value is `/var/removedldif/`.

 * __cacertsLocation__ holds the value
   `/usr/java/latest/jre/lib/security/cacerts`. This option defines a
   keystore to be used for downloaded [SSL][ssl] certificates. It is a 
   good idea to have all trusted root Certification Authority (CA) at 
   this keystore. It defaults to the Tomcat SSL keystore that is defined in
   `server.xml`.

 * __cacertsPassphrase__ If this option is present it will be used as a
   passphrase to a keystore that is defined in the tag `cacertsLocation`.
   It is only needed if `cacertsLocation` is defined and is protected by 
   password. For default jre cacerts behavior (empty password) - leace 
   commented.

 * __certDir__ holds the value `/etc/certs/`. This is the location of
   certificates used in configuration files.

 * __certDirTemp__ holds the value `/etc/certs/temp`. This is the
   temporary location for certificates while user performs update
   procedures.

 * __servicesRestartTrigger__ holds the filename
   `/opt/gluu/trigger_restart_of_services_delete_me_to_do_so`. Deleting
   this file works as a trigger that restarts the appliance services.

 * __oxtrust.auth.mode__  set this tag to `basic` without the quotation 
   to use basic authentication or leave it blank to use oxAuth.

 * __oxauth.authorize.url__ defines the oxAuth authorization uri.

 * __oxauth.token.url__ defines the oxAuth token uri.

 * __oxauth.token.validation.url__ defines the oxAuth uri for token
   validation.

 * __oxauth.checksession.url__ defines the oxAuth uri to check the
   current session.

 * __oxauth.userinfo.url__ defines the oxAuth uri for user information

 * __oxauth.logout.url__ defines the oxAuth uri to log out

 * __oxauth.client.id__ defines the id of the oxAuth client

 * __oxauth.client.credentials__ defines the credentials for the oxAuth
   client.

 * __oxauth.client.password__ defines the password for the oxAuth client

 * __oxauth.client.scope__ defines the scope of the oxAuth client. The
   default value is `openid+profile+address+email`.

## oxTrustLdap Properties

These are the properties oxTrust uses to connect to [LDAP][ldap]
services:

 * __bindDN__ defines the [LDAP][ldap] domain name to bind to

 * __bindPassword__ defines the [LDAP][ldap] password to bind to

 * __servers__ defines the [LDAP][ldap] hostname, and the according
   network port for the connection. The default value is 
   `localhost:1636` for the local machine on port `1636`.

 * __useSSL__ enable this tag to initiate a secure connection via 
   [SSL][ssl]. Set this tag to `true` (default value), or `false` 
   if otherwise wanted.

 * __maxconnections__ set this entry to define the maximum number of
   parallel connections. The default value is set to `3`.

 * __baseConfigurationDN__ defines the [LDAP][ldap] domain name for base
   configuration

 * __createLdapConfigurationEntryIfNotExist__ if an [LDAP][ldap]
   configuration entry does not exist it can be created, automatically. 
   Set this tag to `true` (default value), or `false` if otherwise wanted.

[inum]: https://en.wikipedia.org/wiki/INum_Initiative "INum Initiative, Wikipedia"

[jboss]: https://en.wikipedia.org/wiki/WildFly "JBoss, Wildfly, Wikipedia"

[ldap]: https://en.wikipedia.org/wiki/Lightweight_Directory_Access_Protocol "Lightweight Directory Access Protocol (LDAP), Wikipedia"

[ldif]: https://en.wikipedia.org/wiki/LDAP_Data_Interchange_Format "LDAP Data Interchange Format (LDIF), Wikipedia"

[openid]: https://en.wikipedia.org/wiki/OpenID "OpenID, Wikipedia"

[oxauth]: http://www.gluu.org/docs/reference/oxAuth/ "oxAuth, Gluu Docs"

[rest]: https://en.wikipedia.org/wiki/Representational_state_transfer "Representational state transfer (REST), Wikipedia"

[shibboleth]: https://en.wikipedia.org/wiki/Shibboleth_%28Internet2%29 "Shibboleth (Internet2), Wikipedia"

[ssl]: https://en.wikipedia.org/wiki/Transport_Layer_Security "Transport Layer Security, Wikipedia"

[svn]: https://en.wikipedia.org/wiki/Apache_Subversion "Apache Subversion, Wikipedia"
