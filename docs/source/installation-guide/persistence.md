# Persistence Mechanisms

!!! Info
    This page is under construction. There will be some formatting issues, broken links, and other mistakes while it's being finalized.

## Overview

Starting from first version CE uses LDAP layer to store data. 4.0 uses reviewed and extended persistence mechanism with new functionalities:

1. There is no dependency on specific DB persistence module.

1. It’s possible to add new persistence plugins.

1. It’s possible to split data between few persistence modules.

In 4.0 CE has 3 persistence modules:

1. LDAP persistence module (https://github.com/GluuFederation/oxCore/tree/master/persistence-ldap). It’s default persistence method in CE.

1. Couchbase persistence module (https://github.com/GluuFederation/oxCore/tree/master/persistence-couchbase). Setup supports local Couchbase and remote installation with pre-installed Couchbase server.
 
1. Hybrid persistence module (https://github.com/GluuFederation/oxCore/tree/master/persistence-hybrid) This meta module allows to map data to different persistence modules. For example company can use LDAP for users/groups entrees and other layer to store rests of the entries.

Internal data model is the same for all persistence modules. This consistency is based on generic annotations, filters API, persistence API, entry type (objectClass) and persistence key (Domain Name). Here is sample persistence bean:

![Entry definitions](../img/admin-guide/installation-guide/entry_definition.png)
    
Persistence entry manager API provides CRUID operations which work with persistence beans. The base API defined in PersistenceEntryManager (https://github.com/GluuFederation/oxCore/blob/master/persistence-core/src/main/java/org/gluu/persist/PersistenceEntryManager.java) in oxcore-persistence-core library.


## Persistence Layer Dependencies

This diagram shows EntryManager dependencies and it type resolution based on persistence.type specified in gluu.properties

![Dependency Chart](../img/admin-guide/installation-guide/persistence_dependencies.png)

## Persistence Layers

### LDAP

This module uses LDAP server to store data. The module code is in project oxcore-persistence-ldap (https://github.com/GluuFederation/oxCore/tree/master/persistence-ldap).
There are few major data structure changes in 4.0 data model:

- Dropped `o=<inumOrg>` sub level
- Dropped `ou=appliances` sub level
- Moved configuration to `ou=configuration,o=gluu`
- Moved `ou=tokens` and `ou=authoriztions` from client sub-entries to `o=gluu`

In 4.0 there is migrator which can migrate existing data set to new model.
Here is typical LDAP tree after CE installation.

![LDAP Data tree structure](../img/admin-guide/installation-guide/ldap_data_tree.png)

This module uses configuration specified in `/etc/gluu/conf/gluu-ldap.properties`:

```

bindDN: <ldap_binddn>
bindPassword: <encoded_ ldap_pw>
servers: <ldap_hostname>:<ldaps_port>

useSSL: true
ssl.trustStoreFile: <ldapTrustStoreFn>
ssl.trustStorePin: <encoded_ldapTrustStorePass>
ssl.trustStoreFormat: pkcs12

maxconnections: 10

# Max wait 20 seconds
connection.max-wait-time-millis=20000

# Force to recreate polled connections after 30 minutes
connection.max-age-time-millis=1800000

# Invoke connection health check after checkout it from pool
connection-pool.health-check.on-checkout.enabled=false

# Interval to check connections in pool. Value is 3 minutes. Not used when onnection-pool.health-check.on-checkout.enabled=true
connection-pool.health-check.interval-millis=180000

# How long to wait during connection health check. Max wait 20 seconds
connection-pool.health-check.max-response-time-millis=20000

binaryAttributes=objectGUID
certificateAttributes=userCertificate

```

Default setting can be used in most number of environments

### Couchbase

This is new 4.0 persistence layer. Data model in it is very similar to LDAP layer. Hence existing DB can be converted from ldif to Couchbase. Here is sample data entry with key `scopes_10B2`:

```
{
  "dn": "inum=10B2,ou=scopes,o=gluu",
  "objectClass": "oxAuthCustomScope",
  "defaultScope": false,
  "description": "View your local username in the Gluu Server.",
  "inum": "10B2",
  "oxAuthClaim": [
    "inum=42E0,ou=attributes,o=gluu"
  ],
  "oxId": "user_name",
  "oxScopeType": "openid"
}
```

![Couchbase Buckets list](../img/admin-guide/installation-guide/couchbase_buckets.png)
    
The list of buckets is not hardcoded and can be changed via configuration file `gluu-couchbase.properties`
Here is default mapping configuration:

```
buckets: gluu, gluu_client, gluu_cache, gluu_site, gluu_token, gluu_authorization, gluu_user, gluu_statistic

bucket.default: gluu
bucket.gluu_user.mapping: people, groups
bucket.gluu_cache.mapping: cache
bucket.gluu_statistic.mapping: statistic
bucket.gluu_site.mapping: cache-refresh
bucket.gluu_authorization.mapping: authorizations
bucket.gluu_token.mapping: tokens
bucket.gluu_client.mapping: clients
```

There are 2 mandatory keys in this configuration `buckets` and `bucket.default`. `buckets` provides information about all available buckets. `bucket.default` is the main bucket which applications should use if other mapping rules were not applied.

Third type of lines `bucket.<>.mapping: <comma_separated_second_level_names>` gives applications information in which bucket store specified entry. The value here is the RDN value of second level in LDAP tree.

Table below specify list of entry types which applications store in buckets:

| Bucket | Entry Type |
| --- | --- |
|gluu | gluuOrganization |
| | gluuConfiguration |  
| | oxAuthConfiguration |
| | oxTrustConfiguration |
| | oxPassportConfiguration |
| | oxApplicationConfiguration |
| | gluuAttribute |
| | oxCustomScript |
| | oxAuthCustomScope |
| | oxSectorIdentifier |
| | oxUmaResource |
| | oxUmaResourcePermission |
| | oxAuthUmaRPT |
| | oxAuthUmaPCT |
| | oxDeviceRegistration |
| | oxU2fRequest |
| gluu_client | oxAuthClient |
| gluu_cache | oxCacheEntity |
| gluu_site | gluuInumMap |
| gluu_authorization | oxClientAuthorization |
| gluu_token | oxAuthToken |
| gluu_user | gluuPerson |
| | gluuGroup|
| | pairwiseIdentifier |
| | oxDeviceRegistration |
| | oxFido2AuthenticationEntry |
| | oxFido2RegistrationEntry |
| gluu_statistic | oxMetric |

Both LDAP and Couchbase persistence layers uses Gluu Filter API (https://github.com/GluuFederation/oxCore/blob/master/persistence-filter/src/main/java/org/gluu/search/filter/Filter.java) in order to minimize CE dependency on specific DB. At runtime Couchbase persistence layer convert them to N1QL query language.

This module uses configuration specified in `/etc/gluu/conf/gluu-couchbase.properties`:

```
servers: <hostname>

connection.connect-timeout:10000
connection.connection-max-wait-time: 20000
connection.operation-tracing-enabled: false

# If mutation tokens are enabled, they can be used for advanced durability requirements,
# as well as optimized RYOW consistency.
connection.mutation-tokens-enabled: false

# Sets the pool size (number of threads to use) for all non blocking operations in the core and clients
# (default value is the number of CPUs).
# connection.computation-pool-size: 5

# Default scan consistency. Possible values are: not_bounded, request_plus, statement_plus
connection.scan-consistency: not_bounded

auth.userName: <couchbase_server_user>
auth.userPassword: <encoded_couchbase_server_pw>

buckets: gluu, gluu_client, gluu_cache, gluu_site, gluu_token, gluu_authorization, gluu_user, gluu_statistic

bucket.default: gluu
bucket.gluu_user.mapping: people, groups
bucket.gluu_cache.mapping: cache
bucket.gluu_statistic.mapping: statistic
bucket.gluu_site.mapping: cache-refresh
bucket.gluu_authorization.mapping: authorizations
bucket.gluu_token.mapping: tokens
bucket.gluu_client.mapping: clients

password.encryption.method: <encryption_method>

ssl.trustStore.enable: <ssl_enabled>
ssl.trustStore.file: <couchbaseTrustStoreFn>
ssl.trustStore.pin: <encoded_couchbaseTrustStorePass>
ssl.trustStore.format: pkcs12

binaryAttributes=objectGUID
certificateAttributes=userCertificate
```

### Hybrid

This is meta-DB persistence layer. The main role of it to add abstraction layer to help split data between DBs. It can be used to resolve for example next issue:

1. Store expired entries in another DB to reduce main DB size. Example id_token which need for end_session endpoint
1. Store modifications history
1. Use LDAP to store users data
1. Etc.

This module combines other persistence layers. Hence all used layers should have right configuration. This module uses configuration specified in `/etc/gluu/conf/gluu-hybrid.properties`. Here is sample file:

```
storages: couchbase, ldap
storage.default: couchbase
storage.ldap.mapping: people, groups
storage.couchbase.mapping: clients, cache, site, tokens, statistic, authorization
```

In this example CE applications will use LDAP for `ou=people` and `ou=groups`. All other data will we stored in Couchbase DB.

## Generic configuration properties

In 4. file which provides base configuration details is `/etc/gluu/conf/gluu.properties.

Here is self-explanatory sample configuration:

```
persistence.type=couchbase

oxauth_ConfigurationEntryDN=ou=oxauth,ou=configuration,o=gluu
oxtrust_ConfigurationEntryDN=ou=oxtrust,ou=configuration,o=gluu
oxidp_ConfigurationEntryDN=ou=oxidp,ou=configuration,o=gluu
oxcas_ConfigurationEntryDN=ou=oxcas,ou=configuration,o=gluu
oxpassport_ConfigurationEntryDN=ou=oxpassport,ou=configuration,o=gluu
oxradius_ConfigurationEntryDN=ou=oxradius,ou=configuration,o=gluu

certsDir=/etc/certs
confDir=
pythonModulesDir=/opt/gluu/python/libs
```
