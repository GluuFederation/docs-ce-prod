# Default Configuration wihtin Gluu Server
This page contains the default configurations for Gluu Server Community Edition. The defaults are not recommended and can be changed according to the internal policy of the organization. This page will also be helpful in understanding the defaults and changing them.

## OpenID Connect

|Attribute|Description|Default|
|---------|-----------|-------|
|dynamicRegistrationExpirationTime |Expiration of client secret|86400 seconds|
|sessionIdUnusedLifetime|Expiration of session for authenticated user|86400 seconds|
|sessionIdUnauthenticatedUnusedLifetime|Expiration of session for unauthenticated user|120 seconds|
|webKeysStorage|Set to **keystore** to use a JKS file for private key storage. Set to **pkcs11** to use SoftHSMv2 storage (PKCS #11 interface) through oxEleven REST Services|keystore|

* The `clientSecretExpiresAt` parameter is used to determine the expiration time of the client secret while registring any client with Gluu Server. This parameter sent along with the register request to Gluu Server.
