# API Document

## /oxauth

## Overview
Any OpenID Client needs to register with the OpenID Provider to utilize OpenID Services, in this case register a user, and acquire a client ID and a shared secret.

#### `/oxauth/register`
### registerPost
**POST** `/oxauth/register`

Registers new dynamic client in oxAuth.
#### URL
    http://gluu.org/oxauth/register
#### Parameters
|Parameter|Description|
|---------|--------|
|redirect_uris|Redirection URI values used by the Client. One of these registered Redirection URI values must exactly match the redirect_uri parameter value used in each Authorization Request|
|response_types|A list of the OAuth 2.0 response_type values that the Client is declaring that it will restrict itself to using. If omitted, the default is that the Client will use only the code Response Type. Allowed values are code, token, id_token|
|grant_types|A list of the OAuth 2.0 Grant Types that the Client is declaring that it will restrict itself to using. The Grant Type values used by OpenID Connect are:<ul><li>**authorization_code** The Authorization Code Grant Type</li><li>**implicit** The Implicit Grant Type</li><li>**refresh_token** The Refresh Token Grant Type</li></ul>The following table lists the correspondence between response_type values that the Client will use and grant_type values that MUST be included in the registered grant_types list:<ul><li>code: authorization_code</li><li>id_token: implicit</li><li>token id_token: implicit</li><li>code id_token: authorization_code, implicit</li><li>code token: authorization_code, implicit</li><li>code token id_token: authorization_code, implicit</li></ul>|
|application_type|Kind of the application. The default, if omitted, is web. The defined values are native or web. Web Clients using the OAuth Implicit Grant Type must only register URLs using the https scheme as redirect_uris; they must not use localhost as the hostname. Native Clients must only register redirect_uris using custom URI schemes or URLs using the http: scheme with localhost as the hostname.|
|contacts|e-mail addresses of people responsible for this Client.|
|client_name|Name of the Client to be presented to the End-User.|
|logo_uri|URL that references a logo for the Client application. If present, the server displays this image to the End-User during approval. The value of this field must point to a valid image file.|
|client_uri|URL of the home page of the Client. The value of this field must point to a valid Web page. If present, the server displays this URL to the End-User in a followable fashion.|
|policy_uri|URL that the Relying Party Client provides to the End-User to read about the how the profile data will be used. The value of this field must point to a valid web page. The OpenID Provider displays this URL to the End-User if it is given.|
|tos_uri|URL that the Relying Party Client provides to the End-User to read about the Relying Party's terms of service. The value of this field must point to a valid web page. The OpenID Provider displays this URL to the End-User if it is given.|
|jwks_uri|URL for the Client's JSON Web Key Set (JWK) document. If the Client signs requests to the Server, it contains the signing key(s) the Server uses to validate signatures from the Client. The JWK Set may also contain the Client's encryption keys(s), which are used by the Server to encrypt responses to the Client. When both signing and encryption keys are made available, a use (Key Use) parameter value is required for all keys in the referenced JWK Set to indicate each key's intended usage. Although some algorithms allow the same key to be used for both signatures and encryption, doing so is not recommended, as it is less secure. The JWK x5c parameter MAY be used to provide X.509 representations of keys provided. When used, the bare key values must still be present and must match those in the certificate.|
|jwks|Client's JSON Web Key Set (JWK) document, passed by value. The semantics of the jwks parameter are the same as the jwks_uri parameter, other than that the JWK Set is passed by value, rather than by reference. This parameter is intended only to be used by Clients that, for some reason, are unable to use the jwks_uri parameter, for instance, by native applications that might not have a location to host the contents of the JWK Set. If a Client can use jwks_uri, it must not use jwks. One significant downside of jwks is that it does not enable key rotation (which jwks_uri does). The jwks_uri and jwks parameters must not be used together.|
|sector_identifier_uri|URL using the https scheme to be used in calculating Pseudonymous Identifiers by the OP. The URL references a file with a single JSON array of redirect_uri values. Providers that use pairwise sub (subject) values utilizes the sector_identifier_uri value provided in the Subject Identifier calculation for pairwise identifiers.|
|subject_type|subject_type requested for responses to this Client. The subject_types_supported Discovery parameter contains a list of the supported subject_type values for this server. Valid types include pairwise and public.|
|id_token_signed_response_alg|JWS alg algorithm (JWA) required for signing the ID Token issued to this Client. The value none must not be used as the ID Token alg value unless the Client uses only Response Types that return no ID Token from the Authorization Endpoint (such as when only using the Authorization Code Flow). The default, if omitted, is RS256. The public key for validating the signature is provided by retrieving the JWK Set referenced by the jwks_uri element from OpenID Connect Discovery.|
|id_token_encrypted_response_alg|JWE alg algorithm (JWA) required for encrypting the ID Token issued to this Client. If this is requested, the response will be signed then encrypted, with the result being a Nested JWT. The default, if omitted, is that no encryption is performed.|
|id_token_encrypted_response_enc|JWE enc algorithm (JWA) required for encrypting the ID Token issued to this Client. If id_token_encrypted_response_alg is specified, the default for this value is A128CBC-HS256. When id_token_encrypted_response_enc is included, id_token_encrypted_response_alg must also be provided.|
|userinfo_signed_response_alg|JWS alg algorithm (JWA) required for signing UserInfo Responses. If this is specified, the response will be JWT serialized, and signed using JWS. The default, if omitted, is for the UserInfo Response to return the Claims as a UTF-8 encoded JSON object using the application/json content-type.|
|userinfo_encrypted_response_alg|JWE alg algorithm (JWA) required for encrypting UserInfo Responses. If both signing and encryption are requested, the response will be signed then encrypted, with the result being a Nested JWT. The default, if omitted, is that no encryption is performed.|
|userinfo_encrypted_response_enc|JWE enc algorithm (JWA) required for encrypting UserInfo Responses. If userinfo_encrypted_response_alg is specified, the default for this value is A128CBC-HS256. When userinfo_encrypted_response_enc is included, userinfo_encrypted_response_alg must also be provided.|
|request_object_signing_alg| JWS alg algorithm (JWA) that must be used for signing Request Objects sent to the OP. All Request Objects from this Client are rejected, if not signed with this algorithm. This algorithm is used both when the Request Object is passed by value (using the request parameter) and when it is passed by reference (using the request_uri parameter). The value none may be used. The default, if omitted, is that any algorithm supported by the OP and the RP may be used.|
|request_object_encryption_alg| JWE alg algorithm (JWA) the RP is declaring that it may use for encrypting Request Objects sent to the OP. This parameter should be included when symmetric encryption will be used, since this signals to the OP that a client_secret value needs to be returned from which the symmetric key will be derived, that might not otherwise be returned. The RP may still use other supported encryption algorithms or send unencrypted Request Objects, even when this parameter is present. If both signing and encryption are requested, the Request Object will be signed then encrypted, with the result being a Nested JWT. The default, if omitted, is that the RP is not declaring whether it might encrypt any Request Objects.|
|request_object_encryption_enc|JWE enc algorithm (JWA) the RP is declaring that it may use for encrypting Request Objects sent to the OP. If request_object_encryption_alg is specified, the default for this value is A128CBC-HS256. When request_object_encryption_enc is included, request_object_encryption_alg must also be provided.|
|token_endpoint_auth_method|Requested Client Authentication method for the Token Endpoint. The options are client_secret_post, client_secret_basic, client_secret_jwt, private_key_jwt, and none. If omitted, the default is client_secret_basic, the HTTP Basic Authentication Scheme.|
|token_endpoint_auth_signing_alg|JWS alg algorithm (JWA) that must be used for signing the JWT used to authenticate the Client at the Token Endpoint for the private_key_jwt and client_secret_jwt authentication methods. All Token Requests using these authentication methods from this Client are rejected, if the JWT is not signed with this algorithm. The value none must not be used. The default, if omitted, is that any algorithm supported by the OP and the RP MAY be used.|
|default_max_age|Default Maximum Authentication Age. Specifies that the End-User must be actively authenticated if the End-User was authenticated longer ago than the specified number of seconds. The max_age request parameter overrides this default value. If omitted, no default Maximum Authentication Age is specified.|
|require_auth_time|Boolean value specifying whether the auth_time Claim in the ID Token is required. It is required when the value is true. (If this is false, the auth_time Claim can still be dynamically requested as an individual Claim for the ID Token using the claims request parameter) If omitted, the default value is false.|
|default_acr_values|Default requested Authentication Context Class Reference values. Array of strings that specifies the default acr values that the OP is being requested to use for processing requests from this Client, with the values appearing in order of preference. The Authentication Context Class satisfied by the authentication performed is returned as the acr Claim Value in the issued ID Token. The acr Claim is requested as a Voluntary Claim by this parameter. The acr_values_supported discovery element contains a list of the supported acr values supported by this server. Values specified in the acr_values request parameter or an individual acr Claim request override these default values.|
|initiate_login_uri|URI using the https scheme that a third party can use to initiate a login by the RP. The URI must accept requests via both GET and POST. The Client must understand the login_hint and iss parameters and should support the target_link_uri parameter.|
|request_uris|request_uri values that are pre-registered by the RP for use at the OP. The Servers cache the contents of the files referenced by these URIs and not retrieve them at the time they are used in a request. OPs can require that request_uri values used be pre-registered with the require_request_uri_registration discovery parameter. If the contents of the request file could ever change, these URI values should include the base64url encoded SHA-256 hash value of the file contents referenced by the URI as the value of the URI fragment. If the fragment value used for a URI changes, that signals the server that its cached value for that URI with the old fragment value is no longer valid.|

#### Response
Client Identificator or INUM, a client shared secret and the account expiration date in a [JSON[Response]]

#### Errors
<table border="1">
    <tr>
        <th>Status Code</th>
        <th>Reason</th>
    <tr/>
	<tr>
            <td>400</td>
            <td>invalid_request&#10;The request is missing a required parameter, includes an unsupported parameter or parameter value, repeats the same parameter, uses more than one method for including an access token, or is otherwise malformed.  The resource server SHOULD respond with the HTTP 400 (Bad Request) status code.</td>
        </tr>
        <tr>
            <td>401</td>
            <td>invalid_token&#10;The access token provided is expired, revoked, malformed, or invalid for other reasons.  The resource SHOULD respond with the HTTP 401 (Unauthorized) status code.  The client MAY request a new access token and retry the protected resource request.</td>
        </tr>
        <tr>
            <td>403</td>
            <td>insufficient_scope&#10;The request requires higher privileges than provided by the access token.  The resource server SHOULD respond with the HTTP 403 (Forbidden) status code and MAY include the &quot;scope&quot;&#10; attribute with the scope necessary to access the protected resource.</td>
        </tr>
	<tr>
	    <td>302</td>
	    <td>access_denies&#14; The request is denied by the authorization server.</td>
	</tr>

</table>

### registerPut
**PUT** `/oxauth/register`

This operation updates the Client Metadata for a registered client.
#### URL
    http://gluu.org/oxauth/register
#### Parameters
The request is sent as an `HTTP POST` to the client registration endpoint as JSON with the parameters.

|Parameter|Description|
|---------|-----------|
|clientId |The unique client identifier usually INUM|
|authorization| The authorization for the client|
|httpRequest| The HTTP Request object|
|securityContext| Injectable interface providing access to security info|

#### Response
Client Identificator or INUM, a client shared secret and the account expiration date in a [JSON[Response]]

#### Errors
<table border="1">
    <tr>
        <th>Status Code</th>
        <th>Reason</th>
    <tr/>
        <tr>
            <td>400</td>
            <td>invalid_request&#10;The request is missing a required parameter, includes an unsupported parameter or parameter value, repeats the same parameter, uses more than one method for including an access token, or is otherwise malformed.  The resource server SHOULD respond with the HTTP 400 (Bad Request) status code.</td>
        </tr>
        <tr>
            <td>401</td>
            <td>invalid_token&#10;The access token provided is expired, revoked, malformed, or invalid for other reasons.  The resource SHOULD respond with the HTTP 401 (Unauthorized) status code.  The client MAY request a new access token and retry the protected resource request.</td>
        </tr>
        <tr>
            <td>403</td>
            <td>insufficient_scope&#10;The request requires higher privileges than provided by the access token.  The resource server SHOULD respond with the HTTP 403 (Forbidden) status code and MAY include the &quot;scope&quot;&#10; attribute with the scope necessary to access the protected resource.</td>
        </tr>
        <tr>
            <td>302</td>
            <td>access_denies&#14; The request is denied by the authorization server.</td>
        </tr>

</table>


### registerGet
**GET** `/oxauth/register`

This operation retrieves the Client Metadata for a previously registered client.
#### URL
    http://gluu.org/oxauth/register
#### Parameters
The request is sent as an `HTTP POST` to the client registration endpoint as JSON with the parameters.

|Parameter|Description|
|---------|-----------|
|clientId |The unique client identifier usually INUM|
|securityContext|injectable interface that provides access to security related info.|
 
#### Response
Client Identificator or INUM, a client shared secret and the account expiration date in a [JSON[Response]]

#### Errors
<table border="1">
    <tr>
        <th>Status Code</th>
        <th>Reason</th>
    </tr>
        <tr>
            <td>400</td>
            <td>invalid_request&#10;The request is missing a required parameter, includes an unsupported parameter or parameter value, repeats the same parameter, uses more than one method for including an access token, or is otherwise malformed.  The resource server SHOULD respond with the HTTP 400 (Bad Request) status code.</td>
        </tr>
        <tr>
            <td>401</td>
            <td>invalid_token&#10;The access token provided is expired, revoked, malformed, or invalid for other reasons.  The resource SHOULD respond with the HTTP 401 (Unauthorized) status code.  The client MAY request a new access token and retry the protected resource request.</td>
        </tr>
        <tr>
            <td>403</td>
            <td>insufficient_scope&#10;The request requires higher privileges than provided by the access token.  The resource server SHOULD respond with the HTTP 403 (Forbidden) status code and MAY include the &quot;scope&quot;&#10; attribute with the scope necessary to access the protected resource.</td>
        </tr>
        <tr>
            <td>302</td>
            <td>access_denies&#14; The request is denied by the authorization server.</td>
        </tr>
</table>


