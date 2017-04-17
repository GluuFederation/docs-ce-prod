# 
## LDAP Namespace 

The LDAP Namespace, or Directory Information Tree (DIT) structure, is
the convention for naming entries in LDAP so that they form a
hierarchical tree structure.

In general, the Gluu Server tries to keep the data pretty flat. But at
times, we use the namespace to store information that is relative to a
certain entry.

There are two root namespaces in the Gluu Server: `o=gluu` and `o=site`.
The `o=gluu` namespace is used to store all the important configuration
and entity data. The `o=site` DIT is used only when identities are being
synchronized from an external LDAP server using the Gluu Server Cache
Refresh feature.

The following table has a list of all the major branches of the tree
under `o=gluu`:

| base DN                       | Description						|
| ------------------------------| ------------------------------------------------------|
| o=gluu                        | organization entry, IPv6 style id by default          |
| @!.....			| Basic info with inum 					|
| ou=clients	                | OAuth2 client entities                                |
| ou=federation	                | OAuth2 federation metadata                            |
| ou=groups	      	        | Group entities                                        |
| ou=hosts  			| Hosts							|
| ou=oxasimba			| Asimba configuration is stored in this branch		|
| ou=oxProx	 		| oxProx configuration data				|
| ou=people	                | User entities                                         |
| ou=push			| Mobile device metadata used by oxPush			|
| ou=scopes			| Oauth2 scope entities					|
| ou=scripts			| Custom scripts are stored in this branch		|
| ou=session			| oxAuth Session data (if persistent sessions are enabled)|
| ou=u2f			| The U2F authentication requests, registration requests and registered devices are stored in this branch|
| ou=uma			| UMA policies, scopes, and resource sets 		|

## LDAP Configuration

This section has information about how the Gluu Server uses LDAP, and
other LDAP recommendations.

The Gluu Server uses LDAP for persistence to store information about
things like configuration, user claims, and client claims. Currently
Gluu ships with a forked version of OpenDJ. However, we hope to bolster
support for OpenLDAP and 389DS. If you are an LDAP guru please help us
by contributing documentation details!

## Indexing

All databases need proper indexing to function. This is particularly
true for LDAP servers. There should never be any `sub` or `one` scoped
searches to the LDAP server that are not properly indexed. Because
indexing is implementation specific, the following guidelines should
provide a good starting point. The LDAP server logs should be
periodically analyzed to identify un-indexed searches. The exact
indexing requirements may vary based on custom attributes, and custom
authentication and authorization requirements.

### OpenDJ Indexing

[Indexing Attribute Values](http://opendj.forgerock.org/opendj-server/doc/bootstrap/admin-guide/#chap-indexing)


### 389DS Indexing

[Indexing Architecture](http://directory.fedoraproject.org/docs/389ds/design/database-architecture.html)

### OpenLDAP Indexing


[OpenLDAP Tuning](http://www.openldap.org/doc/admin24/tuning.html)


**Recommended Indexes for OX**

Indexed attributes in OpenDS on seed.gluu.org server:

    | cn               | equality, substring | default | 
    | --               | ------------------- | ------- | 
    | entryUUID        | equality            | default | 
    | givenName        | equality, substring | default | 
    | mail             | equality, substring | default | 
    | member           | equality            | default | 
    | sn               | equality, substring | default | 
    | telephoneNumber  | equality, substring | default | 
    | uid              | equality            | default | 
    | uniqueMember     | equality            | default | 
    | uniqueIdentifier | equality            | Gluu    | 
    | inum             | equality            | Gluu    | 
    | oxid             | equality            | Gluu    | 
    | lastModifiedTime | ordering            | Gluu    | 
    | oxAuthExpiration | ordering            | Gluu    | 

For o=site cache refresh will search on the 'Primary Key'. So it will
not be possible for us to know which attributes need to be indexed until
configuration time.

### Configuring LDAP indexing to improve OX applications performance

In order to keep optimal server load it is necessary to configure
indexing for OpenDJ LDAP server. OpenDJ support these index types:
approximate, equality, ordering, presence, substring, virtual list view,
extensible matching rule. There is more information about index types in
[OpenDJ Admin
Guide](http://opendj.forgerock.org/opendj-server/doc/admin-guide/#indexes-overview).
It is possible to add them for any LDAP attribute. OpenDJ will use them
during searching result entries.

Default OpenDJ installation has few preconfigured indexes for these
attributes: aci, cn, dn2id, ds-sync-conflict, ds-sync-hist, entryUUID,
givenName, id2children, id2subtree, mail, member, objectClass, sn,
telephone­Number, uid, unique­Member. This table contains definition of
these indexes: [default
Indexes](http://opendj.forgerock.org/opendj-server/doc/admin-guide/#default-indexes).

### oxAuth filters

oxAuth has a few parts which allows custom LDAP filters:
	
	`<auth-filters-enabled>`true`</auth-filters-enabled>`
	`<auth-filters>`
	    `<auth-filter>`
	        `<!--filter>`(&amp;(associatedClient=*{0}*)(myPinCode={1}))`</filter-->`
	        `<filter>`(&amp;(mail=*{0}*)(inum={1}))`</filter>`
	        `<!-- If bind=true oxAuth should try to bind to entry which it found by filter specified above -->`
	        `<bind>`false`</bind>`
	        `<base-dn>`o=gluu`</base-dn>`
	    `</auth-filter>`
	
	    `<auth-filter>`
	        `<filter>`uid={0}`</filter>`
	        `<bind>`true`</bind>`
	        `<bind-password-attribute>`pwd`</bind-password-attribute>`
	        `<base-dn>`o=gluu`</base-dn>`
	    `</auth-filter>`
	`</auth-filters>`
	
	`<!-- Custom client filters to be able identify client by custom id. -->`
	`<client-auth-filters-enabled>`true`</client-auth-filters-enabled>`
	`<client-auth-filters>`
	    `<client-auth-filter>`
	        `<filter>`myCustomAttr1={0}`</filter>`
	        `<base-dn>`ou=clients,o=@!1111,o=gluu`</base-dn>`
	    `</client-auth-filter>`
	    `<!--client-auth-filter>`
	        `<filter>`(&amp;(myCustomAttr1={0})(myCustomAttr2={0}))`</filter>`
	        `<base-dn>`ou=clients,o=@!1111,o=gluu`</base-dn>`
	    `</client-auth-filter-->`
	`</client-auth-filters>`

oxAuth uses them to find clients. Hence it is necessary to configure
indexing for these filters. If there are no indexes for the filter
attributes OpenDJ might use an unindexed search.

### Determining what needs indexing

OpenDJ has built in functionality to help the admin find unindexed
searches. More information about this is available in the OpenDJ Admin
Guide [Determining What Needs
Indexing](http://opendj.forgerock.org/opendj-server/doc/admin-guide/#debug-search-indexes).

### Sample commands to add indexes

Add an index for the inum attribute.

	./dsconfig create-local-db-index --backend-name userRoot --type generic --index-name inum --set index-type:equality --set index-entry-limit:4000 --hostName host --port 4444 --bindDN cn=Directory\ Manager -j /tmp/.pw --trustAll --noPropertiesFile --no-prompt
	./dsconfig set-backend-prop --backend-name userRoot --set enabled:false --hostName host --port 4444 --bindDN cn=Directory\ Manager -j /tmp/.pw --trustAll --noPropertiesFile --no-prompt
	./rebuild-index --baseDN o=gluu --index inum
	./dsconfig set-backend-prop --backend-name userRoot --set enabled:true --hostName host --port 4444 --bindDN cn=Directory\ Manager -j /tmp/.pw --trustAll --noPropertiesFile --no-prompt
	
	./dsconfig create-local-db-index --backend-name inumDB --type generic --index-name inum --set index-type:equality --set index-entry-limit:4000 --hostName host --port 4444 --bindDN cn=Directory\ Manager -j /tmp/.pw --trustAll --noPropertiesFile --no-prompt
	./dsconfig set-backend-prop --backend-name inumDB --set enabled:false --hostName host --port 4444 --bindDN cn=Directory\ Manager -j /tmp/.pw --trustAll --noPropertiesFile --no-prompt
	./rebuild-index --baseDN o=site --index inum
	./dsconfig set-backend-prop --backend-name inumDB --set enabled:true --hostName host --port 4444 --bindDN cn=Directory\ Manager -j /tmp/.pw --trustAll --noPropertiesFile --no-prompt

Add an index for the uniqueIdentifier attribute.

	./dsconfig create-local-db-index --backend-name userRoot --type generic --index-name uniqueIdentifier --set index-type:equality --set index-entry-limit:4000 --hostName host --port 4444 --bindDN cn=Directory\ Manager -j /tmp/.pw --trustAll --noPropertiesFile --no-prompt
	./dsconfig set-backend-prop --backend-name userRoot --set enabled:false --hostName host --port 4444 --bindDN cn=Directory\ Manager -j /tmp/.pw --trustAll --noPropertiesFile --no-prompt
	./rebuild-index --baseDN o=gluu --index uniqueIdentifier
	./rebuild-index --baseDN o=site --index uniqueIdentifier
	./dsconfig set-backend-prop --backend-name userRoot --set enabled:true --hostName host --port 4444 --bindDN cn=Directory\ Manager -j /tmp/.pw --trustAll --noPropertiesFile --no-prompt

Add an index for the oxId attribute.

	./dsconfig create-local-db-index --backend-name userRoot --type generic --index-name oxId --set index-type:equality --set index-entry-limit:4000 --hostName host --port 4444 --bindDN cn=Directory\ Manager -j /tmp/.pw --trustAll --noPropertiesFile --no-prompt
	./dsconfig set-backend-prop --backend-name userRoot --set enabled:false --hostName host --port 4444 --bindDN cn=Directory\ Manager -j /tmp/.pw --trustAll --noPropertiesFile --no-prompt
	./rebuild-index --baseDN o=gluu --index oxId
	./rebuild-index --baseDN o=site --index oxId
	./dsconfig set-backend-prop --backend-name userRoot --set enabled:true --hostName host --port 4444 --bindDN cn=Directory\ Manager -j /tmp/.pw --trustAll --noPropertiesFile --no-prompt

Add an index for the lastModifiedTime attribute.

	./dsconfig create-local-db-index --backend-name userRoot --type generic --index-name lastModifiedTime --set index-type:ordering --set index-entry-limit:4000 --hostName host --port 4444 --bindDN cn=Directory\ Manager -j /tmp/.pw --trustAll --noPropertiesFile --no-prompt
	./dsconfig set-backend-prop --backend-name userRoot --set enabled:false --hostName host --port 4444 --bindDN cn=Directory\ Manager -j /tmp/.pw --trustAll --noPropertiesFile --no-prompt
	./rebuild-index --baseDN o=gluu --index lastModifiedTime
	./rebuild-index --baseDN o=site --index lastModifiedTime
	./dsconfig set-backend-prop --backend-name userRoot --set enabled:true --hostName host --port 4444 --bindDN cn=Directory\ Manager -j /tmp/.pw --trustAll --noPropertiesFile --no-prompt

Add an index for oxAuthExpiration attribute.

	./dsconfig create-local-db-index --backend-name userRoot --type generic --index-name oxAuthExpiration --set index-type:ordering --set index-entry-limit:4000 --hostName host --port 4444 --bindDN cn=Directory\ Manager -j /tmp/.pw --trustAll --noPropertiesFile --no-prompt
	./dsconfig set-backend-prop --backend-name userRoot --set enabled:false --hostName host --port 4444 --bindDN cn=Directory\ Manager -j /tmp/.pw --trustAll --noPropertiesFile --no-prompt
	./rebuild-index --baseDN o=gluu --index oxAuthExpiration
	./rebuild-index --baseDN o=site --index oxAuthExpiration
	./dsconfig set-backend-prop --backend-name userRoot --set enabled:true --hostName host --port 4444 --bindDN cn=Directory\ Manager -j /tmp/.pw --trustAll --noPropertiesFile --no-prompt

Determine the current status of indexes.

	./dbtest list-index-status --backendID userRoot -b o=gluu

## Replication

The Gluu Server was designed to take advantage of LDAP replication. Each
server has its own special configuration for replication. Below are some
pointers to the respective platform's documentation on how to manage
replication.

## OpenDJ

[Managing Replication - OpenDJ Admin Guide](http://opendj.forgerock.org/opendj-server/doc/bootstrap/admin-guide/#chap-replication
)

## OpenLDAP

[Replication](http://www.openldap.org/doc/admin24/replication.html)

## 389DS

[Managing Replication](https://access.redhat.com/documentation/en-US/Red_Hat_Directory_Server/9.0/html/Administration_Guide/Managing_Replication.html)

