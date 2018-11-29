# openid-implicit-client

!!! Attention
    The official support end-of-life (EOL) date for Gluu Server 2.4.4 is December 31, 2018. Starting January 1, 2019, no further security updates or bug-fixes will be provided for Gluu Server 2.X. We strongly recommend [upgrading](https://gluu.org/docs/ce/upgrade/) to the newest version.

Simple Javascript client that implements the OpenID Connect implicit flow.

This code is forked based on a javascript library written by
[Edmund Jay](https://www.linkedin.com/in/edmundjay), and referened in a
[blog](https://nat.sakimura.org/2014/12/10/making-a-javascript-openid-connect-client/)
by [Nat Sakimura](https://twitter.com/_nat_en)

To use this library, include the `openidconnect.js` your HTML page.

* Set the provider and client configuration info through JSON objects;
* Call the server – login;
* In the callback page, callback.html, you will get ID Token back,
so that you can put it into the cookie to handle the session.

---

## OIDC Variables

#### Supported Provider Options

List of the Identity Provider's configuration parameters. <br>

* **supportedProviderOptions.issuer** *(string)*: Issuer ID <br>
* **supportedProviderOptions.authorization_endpoint** *(string)*: Authorization Endpoint URL <br>
* **supportedProviderOptions.jwks_uri** *(string)*: JWKS URI <br>
* **supportedProviderOptions.claims_parameter_supported** *(boolean)*: Claims parameter support <br>
* **supportedProviderOptions.request_parameter_supported** *(boolean)*: Request parameter support <br>
* **supportedProviderOptions.jwks** *(object)*: Identity Provider's JWK Set <br>

#### Supported Request Options

Supported Login Request parameters. <br>

* **supportedRequestOptions.scope** *(string)*: Space separated scope values<br>
* **supportedRequestOptions.response_type** *(string)*: Space separated response_type values<br>
* **supportedRequestOptions.display** *(string)*: Display<br>
* **supportedRequestOptions.max_age** *(string)*: Max_age<br>
* **supportedRequestOptions.claims** *(object)*: Claims object containing what information to return in the UserInfo endpoint and ID Token<br>
* **supportedRequestOptions.claims.id_token** *(array)*: List of claims to return in the ID Token<br>
* **supportedRequestOptions.claims.userinfo** *(array)*: List of claims to return in the UserInfo endpoint<br>
* **supportedRequestOptions.request** *(boolean)*: Signed request object JWS. **Not supported yet.**<br>

#### Supported Client Options

List of supported Client configuration parameters. <br>

* **supportedClientOptions.client_id** *(string)*: The client's client_id <br>
* **supportedClientOptions.redirect_uri** *(string)*: The client's redirect_uri <br>

## OIDC Methods

#### setProviderInfo(p)
* _p - The Identity Provider's configuration options described in [OIDC.supportedProviderOptions](#supported-provider-options)_ <br>

Sets the Identity Provider's configuration parameters. It may be done declaring each parameter on code or using the returning information from [OIDC.discover('https:<nolink>//(hostname)')](#discoverissuer). It returns a boolean value indicating status of call. <br>

###### Example:
    // set Identity Provider configuration
    OIDC.setProviderInfo( {
        issuer: 'https://(hostname)',
        authorization_endpoint: 'http://(hostname)/auth.html',
        jwks_uri: 'https://(hostname)/jwks'
        });

    // set Identity Provider configuration using discovery information
    var discovery = OIDC.discover('https://(hostname)');
    if(var)
      OIDC.setProviderInfo(discovery);

#### setClientInfo(p)
* _p - The Client's configuration options described in [OIDC.supportedClientOptions](#supported-client-options)_ <br>

Sets the Client's configuration parameters. It returns a boolean value indicating status of call.

###### Example:
    // set client_id and redirect_uri
    OIDC.setClientInfo( {
       client_id: 'myclientID',
       redirect_uri: 'https://rp.example.com/callback.html'
      }
    );

#### storeInfo(providerInfo, clientInfo)
* _providerInfo - The Identity Provider's configuration options described in [OIDC.supportedProviderOptions](#supported-provider-options)_ <br>
* _clientInfo - The Client's configuration options described in [OIDC.supportedClientOptions](#supported-client-options)_ <br>

Stores the Identity Provider and Client configuration options in the browser session storage for reuse later.

#### restoreInfo()

Load and set the Identity Provider and Client configuration options from the browser session storage.

#### checkRequiredInfo(params)
* _params - List of Identity Provider and client configuration parameters_ <br>

Check whether the required configuration parameters are set. It returns a boolean value indicating whether the options have been set.

#### clearProviderInfo()

Clears the Identity Provider configuration parameters.

#### login(reqOptions)
* _reqOptions - Optional authentication request options ([OIDC.supportedRequestOptions](#supported-request-options))_ <br>

Redirect to the Identity Provider for authentication.

###### Example:
    // login with options
    OIDC.login({
       scope : 'openid profile',
       response_type : 'token id_token',
       max_age : 60,
       claims : {
          id_token : ['email', 'phone_number'],
          userinfo : ['given_name', 'family_name']
          }
    });

    // login with default
    // scope = openid and response_type = id_token
    OIDC.login();

#### verifyIdTokenSig(id_token)
* *id_token - The ID Token string* <br>

Verifies the ID Token signature using the JWK Keyset from jwks or jwks_uri of the Identity Provider Configuration options set via *[OIDC.setProviderInfo](#setproviderinfop)*. Supports only RSA signatures. It returns a boolean value indicates whether the signature is valid or not.

#### isValidIdToken(id_token)
* *id_token - The ID Token string* <br>

Validates the information in the ID Token against configuration data in the Identity Provider and Client configuration set via *[OIDC.setProviderInfo](#setproviderinfop)* and set via *[OIDC.setClientInfo](#setclientinfop)*. It returns a boolean value indicating the validity of the ID Token.

#### rsaVerifyJWS(jws, jwk)
* *jws - The JWS string* <br>
* *jwk - The JWK Key that will be used to verify the signature* <br>

Verifies the JWS string using the JWK. It returns a boolean value indicating the validity of the JWS signature.

#### getValidIdToken()

Return the ID Token string taken from the current page URL whose signature is verified and contents validated against the configuration data set via *[OIDC.setProviderInfo](#setproviderinfop)* and *[OIDC.setClientInfo](#setclientinfop)*.

#### getAccessToken()

Return Access Token string taken from the current page URL.

#### getCode()

Return Authorization Code string taken from the current page URL.

#### getIdTokenParts(id_token)
* *id_token - The ID Token string* <br>

Splits the ID Token string into the individual JWS parts. It returns an array of the JWS compact serialization components (header, payload, signature).

#### getIdTokenPayload(id_token)
* *id_token - The ID Token string* <br>

Return a JSON object with contents of the ID Token payload.

#### getJsonObject(jsonS)
* *jsonS - JSON string* <br>

Return the JSON object from the JSON string.

#### fetchJSON(url)
* *url - URL to fetch the JSON file* <br>

Retrieves the JSON file at the specified URL. The URL must have CORS enabled for this function to work. It returns a string of contents of the URL or null.

#### jwk_get_key(jwkIn, kty, use, kid)
* *jwkIn - JWK Keyset string or object.* <br>
* *kty - The 'kty' to match (RSA|EC). Only RSA is supported.* <br>
* *use - The 'use' to match (sig|enc).* <br>
* *kid - The 'kid' to match* <br>

Retrieve the JWK key that matches the input criteria. It returns an array of JWK keys that match the specified criteria.

#### discover(issuer)
* *issuer - The Identity Provider's issuer_id* <br>

Performs discovery on the Identity Provider's issuer_id. It returns the JSON object of the discovery document or null.

#### debug(toggle, id_token)
* *toggle - Boolean value that enables or disables debugging output* <br>
* *id_token - The ID Token string* <br>

Print current Client's configuration options, Identity Provider's configuration options, results for verification and validation of id_token and its signature directly on console.

#### getUserInfo(access_token)
* *access_token - Access Token string* <br>

Make the call to UserInfo endpoint with access token. It returns the user claims sent by the Identity Provider.
