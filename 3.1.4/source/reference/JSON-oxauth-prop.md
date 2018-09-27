# oxAuth Configurations
## Overview
This page explains the JSON Configuration which can be accessed by navigating to `Configuration` > `JSON Configuration` > `oxAuth Configuration`. 

## oxAuth.properties
![image](../img/reference/config-json_oxauthproperties311.png)

The following tables include the name and description of each configurable oxAuth property:

### General Configuration

Name                          |Description
---------------------------------------------------|-----------
umaValidateClaimToken                              | Validate claim_token as id_token, assuming it is issued by a local IDP
sessionAsJwt                                       | Experimental feature. This saves session data as a JWT
loginPage                                          | The login page's URL
authorizationPage                                  | The oxAuth authorization page URL
baseEndpoint                                       | The base URL for endpoints
authorizationEndpoint                              | The authorization endpoint URL
tokenEndpoint                                      | The token endpoint URL
userInfoEndpoint                                   | The User Info endpoint URL
clientInfoEndpoint                                 | The Client Info endpoint URL
checkSessionIFrame                                 | URL for an OP IFrame that supports cross-origin communications for session state information with the RP Client using the HTML5 postMessage API
endSessionEndpoint                                 | URL at the OP to which an RP can perform a redirect to request that the end user be logged out at the OP
jwksUri                                            | URL of the OP's JSON Web Key Set (JWK) document. This contains the signing key(s) the RP uses to validate signatures from the OP
registrationEndpoint                               | Registration endpoint URL
OpenIdDiscoveryEndpoint                            | Discovery endpoint URL
idGenerationEndpoint                               | ID Generation endpoint URL
introspectionEndpoint                              | Introspection endpoint URL
introspectionAccessTokenMustHaveUmaProtectionScope | If True, rejects introspection requests if access_token does not have the uma_protection scope in its authorization header
umaConfigurationEndpoint                           | UMA Configuration endpoint URL
sectorIdentifierEndpoint                           | Sector Identifier endpoint URL
oxElevenGenerateKeyEndpoint                        | oxEleven Generate Key endpoint URL
oxElevenSignEndpoint                               | oxEleven Sign endpoint URL
oxElevenVerifySignatureEndpoint                    | oxEleven Verify Signature endpoint URL
oxElevenDeleteKeyEndpoint                          | oxEleven Delete Key endpoint URL
oxElevenJwksEndpoint                               | oxEleven JWKS endpoint URL
openidSubAttribute                                 | Specifies which LDAP attribute is used for the subject identifier claim
responseTypesSupported                             | This list details which OAuth 2.0 response_type values are supported by this OP. By default, every combination of `code`, `token` and `id_token` is supported.
grantTypesSupported                                | This list details which OAuth 2.0 grant types are supported by this OP
dynamicGrantTypeDefault                            | This list details which OAuth 2.0 grant types can be set up with the client registration API
subjectTypesSupported                              | This list details which Subject Identifier types that the OP supports. Valid types include pairwise and public.
defaultSubjectType                                 | The default subject type used for dynamic client registration
userInfoSigningAlgValuesSupported                  | This JSON Array lists which JWS signing algorithms (alg values) [JWA] can be used by for the UserInfo endpoint to encode the claims in a JWT
userInfoEncryptionAlgValuesSupported               | This JSON Array lists which JWS encryption algorithms (alg values) [JWA] can be used by for the UserInfo endpoint to encode the claims in a JWT
userInfoEncryptionEncValuesSupported               | This JSON Array lists which JWS encryption algorithms (enc values) [JWA] can be used by for the UserInfo endpoint to encode the claims in a JWT
idTokenSigningAlgValuesSupported                   | A list of the JWS signing algorithms (alg values) supported by the OP for the ID Token to encode the Claims in a JWT
idTokenEncryptionAlgValuesSupported                | A list of the JWE encryption algorithms (alg values) supported by the OP for the ID Token to encode the Claims in a JWT
idTokenEncryptionEncValuesSupported                | A list of the JWE encryption algorithms (enc values) supported by the OP for the ID Token to encode the Claims in a JWT
requestObjectSigningAlgValuesSupported             | A list of the JWS signing algorithms (alg values) supported by the OP for Request Objects
requestObjectEncryptionAlgValuesSupported          | A list of the JWE encryption algorithms (alg values) supported by the OP for Request Objects
requestObjectEncryptionEncValuesSupported          | A list of the JWE encryption algorithms (enc values) supported by the OP for Request Objects
tokenEndpointAuthMethodsSupported                  | A list of Client Authentication methods supported by this Token Endpoint
tokenEndpointAuthSigningAlgValuesSupported         | A list of the JWS signing algorithms (alg values) supported by the Token Endpoint for the signature on the JWT used to authenticate the Client at the Token Endpoint for the private_key_jwt and client_secret_jwt authentication methods
dynamicRegistrationCustomAttributes                | This list details the custom attributes for dynamic registration
displayValuesSupported                             | A list of the display parameter values that the OpenID Provider supports
claimTypesSupported                                | A list of the Claim Types that the OpenID Provider supports
serviceDocumentation                               | URL of a page containing human-readable information that developers might want or need to know when using the OpenID Provider
claimsLocalesSupported                             | This list details the languages and scripts supported for values in the claims being returned
idTokenTokenBindingCnfValuesSupported              | Array containing a list of the JWT Confirmation Method member names supported by the OP for Token Binding of ID Tokens. The presence of this parameter indicates that the OpenID Provider supports Token Binding of ID Tokens. If omitted, the default is that the OpenID Provider does not support Token Binding of ID Tokens
uiLocalesSupported                                 | This list details the languages and scripts supported for the user interface
persistIdTokenInLdap                               | Specifies whether to persist id_token into LDAP (otherwise saves into cache)
persistRefreshTokenInLdap                          | Specifies whether to persist refresh_token into LDAP (otherwise saves into cache)
claimsParameterSupported                           | Specifies whether the OP supports use of the claims parameter
requestParameterSupported                          | Boolean value specifying whether the OP supports use of the request parameter
requestUriParameterSupported                       | Boolean value specifying whether the OP supports use of the request_uri parameter
requireRequestUriRegistration                      | Boolean value specifying whether the OP requires any request_uri values used to be pre-registered using the request_uris registration parameter
opPolicyUri                                        | URL that the OpenID Provider provides to the person registering the Client to read about the OP's requirements on how the Relying Party can use the data provided by the OP
opTosUri                                           | URL that the OpenID Provider provides to the person registering the Client to read about OpenID Provider's terms of service
authorizationCodeLifetime                          | The lifetime of the Authorization Code
refreshTokenLifetime                               | The lifetime of the Refresh Token
idTokenLifetime                                    | The lifetime of the ID Token
accessTokenLifetime                                | The lifetime of the short lived Access Token
umaRptLifetime                                     | UMA RPT lifetime
umaTicketLifetime                                  | UMA ticket lifetime
umaPctLifetime                                     | UMA PCT lifetime
umaResourceLifetime                                | UMA Resource lifetime
umaAddScopesAutomatically                          | Add UMA scopes automatically if it is not registered yet
Issuer                                             | URL using the https scheme with no query or fragment component that the OP asserts as its Issuer Identifier
umaGrantAccessIfNoPolicies                         | Specify whether to grant access to resources if there is no any policies associated with scopes
umaRestrictResourceToAssociatedClient              | Restrict access to resource by associated client
umaKeepClientDuringResourceSetRegistration         | Save client information during resource registration
umaRptAsJwt                                        | Issue RPT as JWT or as random string
cleanServiceInterval                               | Time interval for the Clean Service in seconds
keyRegenerationEnabled                             | Boolean value specifying whether to regenerate keys
keyRegenerationInterval                            | The interval for key regeneration in hours
defaultSignatureAlgorithm                          | The default signature algorithm to sign ID Tokens
oxOpenIdConnectVersion                             | OpenID Connect Version
organizationInum                                   | The Organization Inum
oxId                                               | URL for the Inum generator Service
dynamicRegistrationEnabled                         | Boolean value specifying whether to enable Dynamic Registration
dynamicRegistrationExpirationTime                  | Expiration time in seconds for clients created with dynamic registration, 0 means never expire
dynamicRegistrationPersistClientAuthorizations     | Boolean value specifying whether to persist client authorizations
trustedClientEnabled                               | Boolean value specifying whether a client is trusted and no authorization is required
dynamicRegistrationScopesParamEnabled              | Boolean value specifying whether to enable scopes parameter in dynamic registration
dynamicRegistrationCustomObjectClass               | LDAP custom object class for dynamic registration
personCustomObjectClassList                        | This list details LDAP custom object classes for dynamic person enrollment
authenticationFiltersEnabled                       | Boolean value specifying whether to enable user authentication filters
clientAuthenticationFiltersEnabled                 | Boolean value specifying whether to enable client authentication filters
authenticationFilters                              | This list details filters for user authentication
clientAuthenticationFilters                        | This list details filters for client authentication
applianceInum                                      | The appliance Inum
sessionIdUnusedLifetime                            | The lifetime for unused session states
sessionIdUnauthenticatedUnusedLifetime             | The lifetime for unused unauthenticated session states
sessionIdLifetime                                  | The lifetime of session id in seconds. If 0 or -1 then expiration is not set. `session_id` cookie expires when browser session ends.
sessionIdEnabled                                   | Boolean value specifying whether to enable session ID parameter
sessionIdPersistOnPromptNone                       | Boolean value specifying whether to persist session ID on prompt none
configurationUpdateInterval                        | The interval for configuration update in seconds
cssLocation                                        | The location for CSS files
jsLocation                                         | The location for JavaScript files
imgLocation                                        | The location for image files
metricReporterInterval                             | The interval for metric reporter in seconds
metricReporterKeepDataDays                         | The days to keep metric reported data
metricReporterEnabled                              | Boolean value specifying whether to enable Metric Reporter
pairwiseIdType                                     | the pairwise ID type
pairwiseCalculationKey                             | Key to calculate algorithmic pairwise IDs
pairwiseCalculationSalt                            | Salt to calculate algorithmic pairwise IDs
webKeysStorage                                     | Web Key Storage Type
dnName                                             | DN of certificate issuer
keyStoreFile                                       | The Key Store File (JKS)



[OxAuth Config JSON description](../reference/oxauth-config-json.json)
