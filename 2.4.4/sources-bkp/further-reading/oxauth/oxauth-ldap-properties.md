# oxauth-ldap.properties

The Gluu Server uses [Lightweight Directory Access Protocol
(LDAP)][ldap] for persistence to store [oxTrust][oxtrust] and oxAuth
data, and to cache user entries. The Gluu Server packages include [Gluu
OpenDJ][opendj], which is our fork of [OpenDJ 2.6.0][opendj-2.6.0], the
last open source release by [Forgerock][forgerock]. It is possible to
use any [LDAP][ldap] server, as long as you have the schema and security
under control.

We publish the latest schema in our community-edition-setup project. The
schema that we publish for Gluu OpenDJ should also work for [Forgerock
OpenDJ][forgerock-opendj], [UnboundID][unboundid] LDAP server, and the
[Oracle Directory Server Enterprise Edition (ODSEE)][odsee] as well.

These are the properties [oxTrust][oxtrust] uses to connect to an
[Lightweight Directory Access Protocol (LDAP)][ldap] service:

 * __bindDN__

   Authenticate with this unique entry, and bind to the [LDAP][ldap]
   server using the given domain name `dn` (initiate an [LDAP][ldap]
   session). Typically, a single [LDAP][ldap] entry consists of entries
   like `dn: dc=example,dc=com`.

 * __bindPassword__

   Authenticate to the [LDAP][ldap] server using this password. This 
   value refers to the [LDAP][ldap] entry `userPassword`.

 * __servers__

   Define both the server name and the according network port to use. 
   The value `localhost:1636` refers to the local machine, and uses port
   `1636`.

 * __useSSL__

   Enable an [SSL][ssl] connection for encrypted data transmission. For
   this entry use either `true` to enable [SSL][ssl] (default value), or
   `false` to disable [SSL][ssl].

 * __maxconnections__

   Define the maximum number of connections at the same time. The 
   default value is set to `3`.

[forgerock]: https://en.wikipedia.org/wiki/ForgeRock "Forgerock, Wikipedia"

[forgerock-opendj]: http://opendj.forgerock.org/ "OpenDJ Directory Services Project"

[ldap]: https://en.wikipedia.org/wiki/Lightweight_Directory_Access_Protocol "Lightweight Directory Access Protocol (LDAP), Wikipedia"

[odsee]: http://www.oracle.com/technetwork/middleware/id-mgmt/overview/index-085178.html "Oracle Directory Server Enterprise Edition (ODSEE)"

[opendj]: https://en.wikipedia.org/wiki/OpenDJ "OpenDJ, Wikipedia"

[opendj-2.6.0]: https://backstage.forgerock.com/#!/downloads/OpenDJ/OpenDJ%20Enterprise/2.6.0#browse "OpenDJ 2.6.0"

[oxtrust]: ../oxTrust/ "oxTrust documentation"

[ssl]: https://en.wikipedia.org/wiki/Transport_Layer_Security "Transport Layer Security (TLS), Wikipedia"

[unboundid]: https://www.unboundid.com/ "UnboundiD"
