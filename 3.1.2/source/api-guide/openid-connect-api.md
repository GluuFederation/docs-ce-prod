# OpenID Connect API

## OpenID Connect Authorization Grant

This page provides an interface for request authorization through REST web services.

## Authorization Endpoint

`/.well-known/openid-configuration`

### Path
`/oxauth/authorize`

### requestAuthorizationGet

**GET** `/oxauth/authorize`

The Authorization Endpoint performs Authentication of the end-user. This is done by sending the User Agent to the Authorization Server's Authorization Endpoint for Authentication and Authorization, using request parameters defined by OAuth 2.0 and additional parameters and parameter values defined by OpenID Connect.

### URL
`http://<hostname of Gluu Server>/oxauth/authorize`

### Parameters

<table border="1">
        <tr>
            <th>Parameter</th>
            <th>Required</th>
            <th>Description</th>
            <th>Data Type</th>
        </tr>
        <tr>
            <th>scope</th>
            <td>true</td>
            <td>OpenID Connect requests MUST contain the openid scope value. If the openid scope value is not present, the behavior is entirely unspecified. Other scope values MAY be present. Scope values used that are not understood by an implementation SHOULD be ignored.</td>
            <td>string</td>
        </tr>
        <tr>
            <th>response_type</th>
            <td>true</td>
            <td>OAuth 2.0 Response Type value that determines the authorization processing flow to be used, including what parameters are returned from the endpoints used. When using the Authorization Code Flow, this value is code.</td>
            <td>string</td>
        </tr>
        <tr>
            <th>client_id</th>
            <td>true</td>
            <td>OAuth 2.0 Client Identifier valid at the Authorization Server.</td>
            <td>string</td>
        </tr>
        <tr>
            <th>redirect_uri</th>
            <td>true</td>
            <td>Redirection URI to which the response will be sent. This URI MUST exactly match one of the Redirection URI values for the Client pre-registered at the OpenID Provider</td>
            <td>string</td>
        </tr>
        <tr>
            <th>state</th>
            <td>false</td>
            <td>Opaque value used to maintain state between the request and the callback. Typically, Cross-Site Request Forgery (CSRF, XSRF) mitigation is done by cryptographically binding the value of this parameter with a browser cookie.</td>
            <td>string</td>
        </tr>
	<tr>
	    <th>response_mode</th>
	    <td>false</td>
	    <td>This parameter informs the authorization server about the mechanism to be used to return parameters from the authorization endpoint. This is not recommended if the default for response_type is requested.</td>
	    <td>string</td>
	</tr>
        <tr>
            <th>nonce</th>
            <td>false</td>
            <td>String value used to associate a Client session with an ID Token, and to mitigate replay attacks. The value is passed through unmodified from the Authorization Request to the ID Token. Sufficient entropy MUST be present in the nonce values used to prevent attackers from guessing values.</td>
            <td>string</td>
        </tr>
        <tr>
            <th>display</th>
            <td>false</td>
            <td>ASCII string value that specifies how the Authorization Server displays the authentication and consent user interface pages to the end-user. The defined values are: page, popup, touch, wap</td>
            <td>string</td>
        </tr>
        <tr>
            <th>prompt</th>
            <td>false</td>
            <td>Space delimited, case sensitive list of ASCII string values that specifies whether the Authorization Server prompts the end-user for re-authentication and consent. The defined values are: none, login, consent, select_account</td>
            <td>string</td>
        </tr>
        <tr>
            <th>max_age</th>
            <td>false</td>
            <td>Maximum Authentication Age. Specifies the allowable elapsed time in seconds since the last time the end-user was actively authenticated by the OP. If the elapsed time is greater than this value, the OP MUST attempt to actively re-authenticate the end-user. (The max_age request parameter corresponds to the OpenID 2.0 PAPE [OpenID.PAPE] max_auth_age request parameter.) When max_age is used, the ID Token returned MUST include an auth_time Claim Value.</td>
            <td>int</td>
        </tr>
        <tr>
            <th>ui_locales</th>
            <td>false</td>
            <td>end-user&#39;s preferred languages and scripts for the user interface, represented as a space-separated list of BCP47 [RFC5646] language tag values, ordered by preference. For instance, the value &quot;fr-CA fr en&quot; represents a preference for French as spoken in Canada, then French (without a region designation), followed by English (without a region designation). An error SHOULD NOT result if some or all of the requested locales are not supported by the OpenID Provider.</td>
            <td>string</td>
        </tr>
        <tr>
            <th>id_token_hint</th>
            <td>false</td>
            <td>ID Token previously issued by the Authorization Server being passed as a hint about the end-user&#39;s current or past authenticated session with the Client. If the end-user identified by the ID Token is logged in or is logged in by the request, then the Authorization Server returns a positive response; otherwise, it SHOULD return an error, such as login_required. When possible, an id_token_hint SHOULD be present when prompt=none is used and an invalid_request error MAY be returned if it is not; however, the server SHOULD respond successfully when possible, even if it is not present. The Authorization Server need not be listed as an audience of the ID Token when it is used as an id_token_hint value.</td>
            <td>string</td>
        </tr>
        <tr>
            <th>login_hint</th>
            <td>false</td>
            <td>Hint to the Authorization Server about the login identifier the end-user might use to log in (if necessary). This hint can be used by an RP if it first asks the end-user for their e-mail address (or other identifier) and then wants to pass that value as a hint to the discovered authorization service. It is RECOMMENDED that the hint value match the value used for discovery. This value MAY also be a phone number in the format specified for the phone_number Claim. The use of this parameter is left to the OP&#39;s discretion.</td>
            <td>string</td>
        </tr>
        <tr>
            <th>acr_values</th>
            <td>false</td>
            <td>Requested Authentication Context Class Reference values. Space-separated string that specifies the acr values that the Authorization Server is being requested to use for processing this Authentication Request, with the values appearing in order of preference. The Authentication Context Class satisfied by the authentication performed is returned as the acr Claim Value, as specified in Section 2. The acr Claim is requested as a Voluntary Claim by this parameter.</td>
            <td>string</td>
        </tr>
        <tr>
            <th>amr_values</th>
            <td>false</td>
            <td>AMR Values</td>
            <td>string</td>
        </tr>
        <tr>
            <th>request</th>
            <td>false</td>
            <td>This parameter enables OpenID Connect requests to be passed in a single, self-contained parameter and to be optionally signed and/or encrypted. The parameter value is a Request Object value, as specified in Section 6.1. It represents the request as a JWT whose Claims are the request parameters.</td>
            <td>string</td>
        </tr>
        <tr>
            <th>request_uri</th>
            <td>false</td>
            <td>This parameter enables OpenID Connect requests to be passed by reference, rather than by value. The request_uri value is a URL using the https scheme referencing a resource containing a Request Object value, which is a JWT containing the request parameters.</td>
            <td>string</td>
        </tr>
        <tr>
            <th>request_session_state</th>
            <td>false</td>
            <td>Request session state</td>
            <td>string</td>
        </tr>
        <tr>
            <th>sessionState</th>
            <td>false</td>
            <td>This is an optional parameter</td>
            <td>string</td>
        </tr>
        <tr>
            <th>accessToken</th>
            <td>false</td>
            <td>This parameter is optinal and carries the access token for the request.</td>
            <td>string</td>
        </tr>
	<tr>
	    <th>origin_headers</th>
	    <td>false</td>
	    <td>This optional token is used in custom workflows.</td>
	    <td>string</td>
	</tr> 
        <tr>
            <th>codeChallange</th>
            <td>false</td>
            <td>This parameter allows the code to be challanced using PKCE.</td>
            <td>string</td>
        </tr>
        <tr>
            <th>codeChallangeMethod</th>
            <td>false</td>
            <td>This parameter allows the use of PKCE to challange code.</td>
            <td>string</td>
	</tr>
       <tr>
            <th>httpRequest</th>
            <td>false</td>
            <td>This is an optional parameter</td>
            <td>string</td>
        </tr>
</table>

The parameter **response_type** determines the authorization processing flows, 
including the parameters returned from the endpoints, and these values are codes and combination of 
the values, and these combination can be as below `code`, `token`, and `id_token`.

<table border="1">
        <tr>
            <th style width=25%>Possible Combination</th>
            <th>Description</th>
        </tr>
            <tr>
                <th>code</th>
                    <td>
                         The authorization code generated by the
                         authorization server.  The authorization code MUST expire
                         shortly after it is issued to mitigate the risk of leaks.  A
                         maximum authorization code lifetime of 10 minutes is
                         RECOMMENDED.  The client MUST NOT use the authorization code
                         more than once.  If an authorization code is used more than
                         once, the authorization server MUST deny the request and SHOULD
                         revoke (when possible) all tokens previously issued based on
                         that authorization code.  The authorization code is bound to
                         the client identifier and redirection URI.
                     </td>
            </tr>
            <tr>
                <th>token</th>
                    <td>
                        If the resource owner grants the access request, the authorization
                        server issues an access token and delivers it to the client by adding
                        the following parameters to the fragment component of the redirection
                        URI using the "application/x-www-form-urlencoded" format.
                    </td>
            </tr>
            <tr>
                <th>id_token</th>
                    <td>
                        The ID Token is a security token that contains Claims about the 
                        Authentication of an End-User by an Authorization Server when using a 
                        Client, and potentially other requested Claims. The ID Token is represented 
                        as a JSON Web Token (JWT). The intended purpose of the id_token is that it 
                        MUST provide an assertion of the identity of the Resource Owner as understood 
                        by the Authorization Server. The assertion MUST specify a targeted audience, 
                        e.g. the requesting Client.
                    </td>
            </tr>
           <tr>
               <th>code token</th>
                   <td>
                        When supplied as the value for the response_type parameter, a successful response 
                        MUST include an Access Token, an Access Token Type, and an Authorization Code. 
                        The default Response Mode for this Response Type is the fragment encoding and the 
                        query encoding MUST NOT be used. Both successful and error responses SHOULD be returned 
                        using the supplied Response Mode, or if none is supplied, using the default Response Mode.
                   </td>
           </tr>
           <tr>
               <th>code id_token</th>
                   <td>
                        When supplied as the value for the response_type parameter, 
                        a successful response MUST include both an Authorization Code and an id_token. 
                        The default Response Mode for this Response Type is the fragment encoding and 
                        the query encoding MUST NOT be used. Both successful and error responses SHOULD 
                        be returned using the supplied Response Mode, or if none is supplied, using the 
                        default Response Mode.
                   </td>
           </tr>
           <tr>
               <th>id_token token</th>
                   <td>
                        When supplied as the value for the response_type parameter, 
                        a successful response MUST include an Access Token, an Access Token Type, 
                        and an id_token. The default Response Mode for this Response Type is the 
                        fragment encoding and the query encoding MUST NOT be used. Both successful 
                        and error responses SHOULD be returned using the supplied Response Mode, 
                        or if none is supplied, using the default Response Mode.
                   </td>
           </tr>
           <tr>
               <th>code id_token token</th>
                   <td>
                        When supplied as the value for the response_type parameter, 
                        a successful response MUST include an Authorization Code, an id_token, 
                        an Access Token, and an Access Token Type. The default Response Mode for this 
                        Response Type is the fragment encoding and the query encoding MUST NOT be used. 
                        Both successful and error responses SHOULD be returned using the supplied 
                        Response Mode, or if none is supplied, using the default Response Mode.
                   </td>
           </tr>
         
</table>

For authorization endpoint, parameter **response_mode** can have any of the below modes 
and in each mode authorization response is encoded in different way. 

<table border="1">
        <tr>
            <th>Authorization Mode</th>
            <th>Description</th>
        </tr>
        <tr>
            <th>query</th>
            <td>Authorization Response parameters are encoded in the 
            query string added to the redirect_uri when redirecting back to the Client.</td>
        </tr>
        <tr>
            <th>fragment</th>
            <td>Authorization Response parameters are encoded in the 
            fragment added to the redirect_uri when redirecting back to the Client.
            </td>
        </tr>
        <tr>
            <th>form_post</th>
            <td>Authorization Response parameters are encoded as HTML form values 
            that are auto-submitted in the User Agent, and thus are transmitted via 
            the HTTP POST method to the Client, with the result parameters being 
            encoded in the body using the application/x-www-form-urlencoded format.
            </td>
        </tr>
         
</table>

## Using JWTs for Passing Request Params

To enable authentication requests to be signed and optionally encrypted authorization requests params are used. Below are the parameters used as Authorization requests parameters. These request are passed as Request Objects by two ways, they are `by value` and `by reference`.

<table border="1">
    <tr>
        <th>Parameter</th>
        <th>Description</th>
		<th>Required</th>
    </tr>
        <tr>
            <td>requests</td>
            <td>This parameter enables OpenID Connect requests to be passed in a single, self-contained parameter and to be optionally signed and/or encrypted. The parameter value is a Request Object value,It represents the request as a JWT whose Claims are the request parameters.</td>
			<td>Optional</td>
        </tr>
        <tr>
            <td>request_uri</td>
            <td>This parameter enables OpenID Connect requests to be passed by reference, rather than by value. The request_uri value is a URL using the https scheme referencing a resource containing a Request Object value, which is a JWT containing the request parameters.</td>
			<td>Optional</td>
        </tr>
</table>

## Request Object by Value
The `request` Authorization Request parameter is used to enable OpenID Connect requests to pass single, self-contained parameter and optionally signed and/or encrypred. The requests is represented as a JWT whose claims are request parameters. This JWT is called a Request Object. The `request` parameter is **Optional**. When `request` parameter is used, the OpenID connect request parameter values contained in JWT supersede those passed using OAuth 2.0 request syntax.  However, parameters MAY also be passed using the OAuth 2.0 request syntax even when a Request Object is used; this would typically be done to enable a cached, pre-signed (and possibly pre-encrypted) Request Object value to be used containing the fixed request parameters, while parameters that can vary with each request, such as state and nonce, are passed as OAuth 2.0 parameters. 

The request to be valid in OAuth 2.0 Authorization Request, values for `response_type` and `client_id` parameters MUST be included using the OAuth 2.0 request syntax, since they are REQUIRED by OAuth 2.0. The values for these parameters MUST match those in the Request Object.

`request` and `request_uri` parameters MUST NOT be included in Request Objects.
	
The following is a non-normative example of the Claims in a Request Object before base64url encoding and signing: 
	
	
	  {
	   "iss": "s6BhdRkqt3",
	   "aud": "https://server.example.com",
	   "response_type": "code id_token",
	   "client_id": "s6BhdRkqt3",
	   "redirect_uri": "https://client.example.org/cb",
	   "scope": "openid",
	   "state": "af0ifjsldkj",
	   "nonce": "n-0S6_WzA2Mj",
	   "max_age": 86400,
	   "claims":
		{
		 "userinfo":
		  {
		   "given_name": {"essential": true},
		   "nickname": null,
		   "email": {"essential": true},
		   "email_verified": {"essential": true},
		   "picture": null
		  },
		 "id_token":
		  {
		   "gender": null,
		   "birthdate": {"essential": true},
		   "acr": {"values": ["urn:mace:incommon:iap:silver"]}
		  }
		}
	  }

	

###  Using the `request` Request Parameter

The Client sends the Authorization Request to the Authorization Endpoint. 

The following is a non-normative example of an Authorization Request using the request parameter (with line wraps within values for display purposes only): 

	
	  https://server.example.com/authorize?
		response_type=code%20id_token
		&client_id=s6BhdRkqt3
		&redirect_uri=https%3A%2F%2Fclient.example.org%2Fcb
		&scope=openid
		&state=af0ifjsldkj
		&nonce=n-0S6_WzA2Mj
		&request=eyJhbGciOiJSUzI1NiIsImtpZCI6ImsyYmRjIn0.ew0KICJpc3MiOiA
		iczZCaGRSa3F0MyIsDQogImF1ZCI6ICJodHRwczovL3NlcnZlci5leGFtcGxlLmN
		vbSIsDQogInJlc3BvbnNlX3R5cGUiOiAiY29kZSBpZF90b2tlbiIsDQogImNsaWV
		udF9pZCI6ICJzNkJoZFJrcXQzIiwNCiAicmVkaXJlY3RfdXJpIjogImh0dHBzOi8
		vY2xpZW50LmV4YW1wbGUub3JnL2NiIiwNCiAic2NvcGUiOiAib3BlbmlkIiwNCiA
		ic3RhdGUiOiAiYWYwaWZqc2xka2oiLA0KICJub25jZSI6ICJuLTBTNl9XekEyTWo
		iLA0KICJtYXhfYWdlIjogODY0MDAsDQogImNsYWltcyI6IA0KICB7DQogICAidXN
		lcmluZm8iOiANCiAgICB7DQogICAgICJnaXZlbl9uYW1lIjogeyJlc3NlbnRpYWw
		iOiB0cnVlfSwNCiAgICAgIm5pY2tuYW1lIjogbnVsbCwNCiAgICAgImVtYWlsIjo
		geyJlc3NlbnRpYWwiOiB0cnVlfSwNCiAgICAgImVtYWlsX3ZlcmlmaWVkIjogeyJ
		lc3NlbnRpYWwiOiB0cnVlfSwNCiAgICAgInBpY3R1cmUiOiBudWxsDQogICAgfSw
		NCiAgICJpZF90b2tlbiI6IA0KICAgIHsNCiAgICAgImdlbmRlciI6IG51bGwsDQo
		gICAgICJiaXJ0aGRhdGUiOiB7ImVzc2VudGlhbCI6IHRydWV9LA0KICAgICAiYWN
		yIjogeyJ2YWx1ZXMiOiBbInVybjptYWNlOmluY29tbW9uOmlhcDpzaWx2ZXIiXX0
		NCiAgICB9DQogIH0NCn0.nwwnNsk1-ZkbmnvsF6zTHm8CHERFMGQPhos-EJcaH4H
		h-sMgk8ePrGhw_trPYs8KQxsn6R9Emo_wHwajyFKzuMXZFSZ3p6Mb8dkxtVyjoy2
		GIzvuJT_u7PkY2t8QU9hjBcHs68PkgjDVTrG1uRTx0GxFbuPbj96tVuj11pTnmFC
		UR6IEOXKYr7iGOCRB3btfJhM0_AKQUfqKnRlrRscc8Kol-cSLWoYE9l5QqholImz
		jT_cMnNIznW9E7CDyWXTsO70xnB4SkG6pXfLSjLLlxmPGiyon_-Te111V8uE83Il
		zCYIb_NMXvtTIVc1jpspnTSD7xMbpL-2QgwUsAlMGzw
	

## Request Object by Reference
The `request_uri` Authorization Request parameter enables OpenID Connect 
requests to be passed by reference, rather than by value. 
This parameter is used identically to the request parameter, other than that the 
Request Object value is retrieved from the resource at the specified URL, rather than 
passed by value. 

The `request_uri_parameter_supported` Discovery result indicates whether the OP 
supports this parameter. Should an OP not support this parameter and an RP uses it, 
the OP MUST return the `request_uri_not_supported` error.  When `request_uri` parameter is used, 
the OpenID Connect request parameter values contained in the referenced JWT supersede 
those passed using the OAuth 2.0 request syntax. However, parameters MAY also be passed using 
the OAuth 2.0 request syntax even when a `request_uri` is used; this would typically be done 
to enable a cached, pre-signed (and possibly pre-encrypted) Request Object value to be used 
containing the fixed request parameters, while parameters that can vary with each request, 
such as state and nonce, are passed as OAuth 2.0 parameters. 

The request to be a valid OAuth 2.0 Authorization Request, 
values for the `response_type` and `client_id` parameters MUST be included 
using the OAuth 2.0 request syntax, since they are REQUIRED by OAuth 2.0. 
The values for these parameters MUST match those in the Request Object

### URL Referencing the Request Object

The Client stores the Request Object resource either locally or remotely at a 
URL the Server can access. This URL is the Request URI, `request_uri`. 

If values for Claims are included in the Request Object , it MUST NOT be revealed 
to anybody but the Authorization Server. As such, the `request_uri` MUST have appropriate 
entropy for its lifetime. It is RECOMMENDED that it be removed if it is known that 
it will not be used again or after a reasonable timeout unless access control measures are taken. 

The following is a non-normative example of a Request URI value 
(with line wraps within values for display purposes only): 
	
	
		https://client.example.org/request.jwt#GkurKxf5T0Y-mnPFCHqWOMiZi4VS138cQO_V7PZHAdM
	

### using the `request_uri` Request Parameter Request
The Client sends the Authorization Request to the Authorization Endpoint. 

The following is a non-normative example of an Authorization Request using the request_uri parameter (with line wraps within values for display purposes only): 

	
	  https://server.example.com/authorize?
		response_type=code%20id_token
		&client_id=s6BhdRkqt3
		&request_uri=https%3A%2F%2Fclient.example.org%2Frequest.jwt
		%23GkurKxf5T0Y-mnPFCHqWOMiZi4VS138cQO_V7PZHAdM
		&state=af0ifjsldkj&nonce=n-0S6_WzA2Mj
		&scope=openid
	
	
For more details on Authorization request parameters using JWTs, refer [here](http://openid.net/specs/openid-connect-core-1_0.html#JWTRequests)

#### Response
##### Successful Reponse
 The authorization server issues an access token and optional refresh
   token, and constructs the response by adding the following parameters
   to the entity-body of the HTTP response with a 200 (OK) status code:
   
<table border="1">
    <tr>
        <th>Parameter</th>
        <th>Description</th>
        <th>Required</th>
    </tr>
        <tr>
            <td>access_token</td>
            <td>The access token issued by the authorization server.</td>
            <td>Required</td>
        </tr>
        <tr>
            <td>token_type</td>
            <td>The access token type provides the client with the information
                   required to successfully utilize the access token to make a protected
                   resource request (along with type-specific attributes).  The client
                   MUST NOT use an access token if it does not understand the token
                   type. Value is case insensitive.</td>
            <td>Required</td
        </tr>
        <tr>
            <td>expires_in</td>
            <td>The lifetime in seconds of the access token.  For
         example, the value "3600" denotes that the access token will
         expire in one hour from the time the response was generated.
         If omitted, the authorization server SHOULD provide the
         expiration time via other means or document the default value.</td>
            <td>RECOMMENDED</td>
        </tr>
        <tr>
            <td>refresh_token</td>
            <td>The refresh token, which can be used to obtain new
         access tokens using the same authorization grant</td>
            <td>Optional</td>
        </tr>
        <tr>
            <td>scope</td>
            <td>Optional, identical to the scope requested by the client.
                Required, The scope of the access token is used as
                `request parameter` or `response parameter`</td>
            <td>Optional and Required depending on the `scope`</td>
        </tr>
  </table>

#### Error Response
<table border="1">
    <tr>
        <th>Parameter</th>
        <th>Description</th>
        <th>Required</th>
    </tr>
        <tr>
            <td>error</td>
            <td>A single ASCII error code from the below table</td>
            <td>Required</td>
        </tr>
        <tr>
            <td>error_description</td>
            <td>Human-readable ASCII [USASCII] text providing
                additional information, used to assist the client developer in
                understanding the error that occurred.
                Values for the "error_description" parameter MUST NOT include
                characters outside the set %x20-21 / %x23-5B / %x5D-7E.</td>
            <td>Optional</td>
        </tr>
        <tr>
            <td>error_uri</td>
            <td>A URI identifying a human-readable web page with
                information about the error, used to provide the client
                developer with additional information about the error.
                Values for the "error_uri" parameter MUST conform to the
                URI-reference syntax and thus MUST NOT include characters
                outside the set %x21 / %x23-5B / %x5D-7E.</td>
            <td>Optional</td>
        </tr>
</table>
<table border="1">
    <tr>
        <th>Status Code</th>
        <th>Reason</th>
    </tr>
        <tr>
            <td>302</td>
            <td>interaction_required&#10;    The Authorization Server requires end-user interaction of some form to proceed. This error MAY be returned when the prompt parameter value in the Authentication Request is none, but the Authentication Request cannot be completed without displaying a user interface for end-user interaction. </td>
        </tr>
        <tr>
            <td>302</td>
            <td>login_required&#10;    The Authorization Server requires end-user authentication. This error MAY be returned when the prompt parameter value in the Authentication Request is none, but the Authentication Request cannot be completed without displaying a user interface for end-user authentication. </td>
        </tr>
        <tr>
            <td>302</td>
            <td>account_selection_required&#10;    The end-user is REQUIRED to select a session at the Authorization Server. The end-user MAY be authenticated at the Authorization Server with different associated accounts, but the end-user did not select a session. This error MAY be returned when the prompt parameter value in the Authentication Request is none, but the Authentication Request cannot be completed without displaying a user interface to prompt for a session to use. </td>
        </tr>
        <tr>
            <td>302</td>
            <td>consent_required&#10;    The Authorization Server requires end-user consent. This error MAY be returned when the prompt parameter value in the Authentication Request is none, but the Authentication Request cannot be completed without displaying a user interface for end-user consent. </td>
        </tr>
        <tr>
            <td>302</td>
            <td>invalid_request_uri&#10;    The request_uri in the Authorization Request returns an error or contains invalid data. </td>
        </tr>
        <tr>
            <td>302</td>
            <td>invalid_request_object&#10;    The request parameter contains an invalid Request Object. </td>
        </tr>
        <tr>
            <td>302</td>
            <td>request_not_supported&#10;    The OP does not support use of the request parameter</td>
        </tr>
        <tr>
            <td>302</td>
            <td>request_uri_not_supported&#10;    The OP does not support use of the request_uri parameter</td>
        </tr>
        <tr>
            <td>302</td>
            <td>registration_not_supported&#10;    The OP does not support use of the registration parameter</td>
        </tr>
        <tr>
            <td>400</td>
            <td>The request parameters contain an invalid option, e.g. an unusual grant type.</td>
        </tr>
        <tr>
            <td>401</td>
            <td>The request could not be authenticated using the client_id and client_secret.</td>
        </tr>
        <tr>
            <td>500</td>
            <td>Either an internal server error occurred (e.g. opendj server is down), or the username and password 
                do not match any known user.
            </td>
        </tr>
</table>

### requestAuthorizationPost
**POST** `/oxauth/authorize`

Performs authorization.
The Authorization Endpoint performs Authentication of the end-user.

### URL
`http://<hostname of Gluu Server>/oxauth/authorize`
### Parameters
<table border="1">
        <tr>
            <th>Parameter</th>
            <th>Required</th>
            <th>Description</th>
            <th>Data Type</th>
        </tr>
        <tr>
            <th>scope</th>
            <td>true</td>
            <td>OpenID Connect requests MUST contain the openid scope value. If the openid scope value is not present, the behavior is entirely unspecified. Other scope values MAY be present. Scope values used that are not understood by an implementation SHOULD be ignored.</td>
            <td>string</td>
        </tr>
        <tr>
            <th>response_type</th>
            <td>true</td>
            <td>OAuth 2.0 Response Type value that determines the authorization processing flow to be used, including what parameters are returned from the endpoints used. When using the Authorization Code Flow, this value is code.</td>
            <td>string</td>
        </tr>
        <tr>
            <th>client_id</th>
            <td>true</td>
            <td>OAuth 2.0 Client Identifier valid at the Authorization Server.</td>
            <td>string</td>
        </tr>
        <tr>
            <th>redirect_uri</th>
            <td>true</td>
            <td>Redirection URI to which the response will be sent. This URI MUST exactly match one of the Redirection URI values for the Client pre-registered at the OpenID Provider</td>
            <td>string</td>
        </tr>
        <tr>
            <th>state</th>
            <td>false</td>
            <td>Opaque value used to maintain state between the request and the callback. Typically, Cross-Site Request Forgery (CSRF, XSRF) mitigation is done by cryptographically binding the value of this parameter with a browser cookie.</td>
            <td>string</td>
        </tr>
        <tr>
            <th>response_mode</th>
            <td>false</td>
            <td>Informs the Authorization Server of the mechanism to be used for returning parameters from the Authorization Endpoint. This use of this parameter is NOT RECOMMENDED when the Response Mode that would be requested is the default mode specified for the Response Type.</td>
            <td>string</td>
        </tr>
        <tr>
            <th>nonce</th>
            <td>false</td>
            <td>String value used to associate a Client session with an ID Token, and to mitigate replay attacks. The value is passed through unmodified from the Authorization Request to the ID Token. Sufficient entropy MUST be present in the nonce values used to prevent attackers from guessing values.</td>
            <td>string</td>
        </tr>
        <tr>
            <th>display</th>
            <td>false</td>
            <td>ASCII string value that specifies how the Authorization Server displays the authentication and consent user interface pages to the end-user. The defined values are: page, popup, touch, wap</td>
            <td>string</td>
        </tr>
        <tr>
            <th>prompt</th>
            <td>false</td>
            <td>Space delimited, case sensitive list of ASCII string values that specifies whether the Authorization Server prompts the end-user for re-authentication and consent. The defined values are: none, login, consent, select_account</td>
            <td>string</td>
        </tr>
        <tr>
            <th>max_age</th>
            <td>false</td>
            <td>Maximum Authentication Age. Specifies the allowable elapsed time in seconds since the last time the end-user was actively authenticated by the OP. If the elapsed time is greater than this value, the OP MUST attempt to actively re-authenticate the end-user. (The max_age request parameter corresponds to the OpenID 2.0 PAPE [OpenID.PAPE] max_auth_age request parameter.) When max_age is used, the ID Token returned MUST include an auth_time Claim Value.</td>
            <td>int</td>
        </tr>
        <tr>
            <th>ui_locales</th>
            <td>false</td>
            <td>end-user&#39;s preferred languages and scripts for the user interface, represented as a space-separated list of BCP47 [RFC5646] language tag values, ordered by preference. For instance, the value &quot;fr-CA fr en&quot; represents a preference for French as spoken in Canada, then French (without a region designation), followed by English (without a region designation). An error SHOULD NOT result if some or all of the requested locales are not supported by the OpenID Provider.</td>
            <td>string</td>
        </tr>
        <tr>
            <th>id_token_hint</th>
            <td>false</td>
            <td>ID Token previously issued by the Authorization Server being passed as a hint about the end-user&#39;s current or past authenticated session with the Client. If the end-user identified by the ID Token is logged in or is logged in by the request, then the Authorization Server returns a positive response; otherwise, it SHOULD return an error, such as login_required. When possible, an id_token_hint SHOULD be present when prompt=none is used and an invalid_request error MAY be returned if it is not; however, the server SHOULD respond successfully when possible, even if it is not present. The Authorization Server need not be listed as an audience of the ID Token when it is used as an id_token_hint value.</td>
            <td>string</td>
        </tr>
        <tr>
            <th>login_hint</th>
            <td>false</td>
            <td>Hint to the Authorization Server about the login identifier the end-user might use to log in (if necessary). This hint can be used by an RP if it first asks the end-user for their e-mail address (or other identifier) and then wants to pass that value as a hint to the discovered authorization service. It is RECOMMENDED that the hint value match the value used for discovery. This value MAY also be a phone number in the format specified for the phone_number Claim. The use of this parameter is left to the OP&#39;s discretion.</td>
            <td>string</td>
        </tr>
        <tr>
            <th>acr_values</th>
            <td>false</td>
            <td>Requested Authentication Context Class Reference values. Space-separated string that specifies the acr values that the Authorization Server is being requested to use for processing this Authentication Request, with the values appearing in order of preference. The Authentication Context Class satisfied by the authentication performed is returned as the acr Claim Value, as specified in section 2. The acr Claim is requested as a Voluntary Claim by this parameter.</td>
            <td>string</td>
        </tr>
        <tr>
            <th>amr_values</th>
            <td>false</td>
            <td>AMR Values</td>
            <td>string</td>
        </tr>
        <tr>
            <th>request</th>
            <td>false</td>
            <td>This parameter enables OpenID Connect requests to be passed in a single, self-contained parameter and to be optionally signed and/or encrypted. The parameter value is a Request Object value, as specified in section 6.1. It represents the request as a JWT whose Claims are the request parameters.</td>
            <td>string</td>
        </tr>
        <tr>
            <th>request_uri</th>
            <td>false</td>
            <td>This parameter enables OpenID Connect requests to be passed by reference, rather than by value. The request_uri value is a URL using the https scheme referencing a resource containing a Request Object value, which is a JWT containing the request parameters.</td>
            <td>string</td>
        </tr>
        <tr>
            <th>request_session_state</th>
            <td>false</td>
            <td>Request session state</td>
            <td>string</td>
        </tr>
        <tr>
            <th>session_state</th>
            <td>false</td>
            <td>Session state of this call</td>
            <td>string</td>
        </tr>
        <tr>
            <th>access_token</th>
            <td>false</td>
            <td>Access token</td>
            <td>string</td>
        </tr>
        <tr>
            <th>origin_headers</th>
            <td>false</td>
            <td>Origin headers. Used in custom workflows.</td>
            <td>string</td>
        </tr>
	<tr>
	    <th>code_challange</th>
	    <td>false</td>
	    <td>PKCE Code challange</td>
	    <td>string</td>
	</tr>
	<tr>
	    <th>code_challange_method</td>
	    <td>false</td>
	    <td>PKCE code challange method</td>
	    <td>string</td>
	</tr>
</table>

#### Response
[JSON[Response]](#successful-reponse)

#### Errors
<table border="1">
    <tr>
        <th>Status Code</th>
        <th>Reason</th>
    </tr>
        <tr>
            <td>302</td>
            <td>interaction_required&#10;    The Authorization Server requires end-user interaction of some form to proceed. This error MAY be returned when the prompt parameter value in the Authentication Request is none, but the Authentication Request cannot be completed without displaying a user interface for end-user interaction. </td>
        </tr>
        <tr>
            <td>302</td>
            <td>login_required&#10;    The Authorization Server requires end-user authentication. This error MAY be returned when the prompt parameter value in the Authentication Request is none, but the Authentication Request cannot be completed without displaying a user interface for end-user authentication. </td>
        </tr>
        <tr>
            <td>302</td>
            <td>account_selection_required&#10;    The end-user is REQUIRED to select a session at the Authorization Server. The end-user MAY be authenticated at the Authorization Server with different associated accounts, but the end-user did not select a session. This error MAY be returned when the prompt parameter value in the Authentication Request is none, but the Authentication Request cannot be completed without displaying a user interface to prompt for a session to use. </td>
        </tr>
        <tr>
            <td>302</td>
            <td>consent_required&#10;    The Authorization Server requires end-user consent. This error MAY be returned when the prompt parameter value in the Authentication Request is none, but the Authentication Request cannot be completed without displaying a user interface for end-user consent. </td>
        </tr>
        <tr>
            <td>302</td>
            <td>invalid_request_uri&#10;    The request_uri in the Authorization Request returns an error or contains invalid data. </td>
        </tr>
        <tr>
            <td>302</td>
            <td>invalid_request_object&#10;    The request parameter contains an invalid Request Object. </td>
        </tr>
        <tr>
            <td>302</td>
            <td>request_not_supported&#10;    The OP does not support use of the request parameter</td>
        </tr>
        <tr>
            <td>302</td>
            <td>request_uri_not_supported&#10;    The OP does not support use of the request_uri parameter</td>
        </tr>
        <tr>
            <td>302</td>
            <td>registration_not_supported&#10;    The OP does not support use of the registration parameter</td>
        </tr>
</table>


- - -

## OpenID Connect Token Endpoint

### Overview


#### Path

`/oxauth/token`**

#### requestAccessToken

**POST** `/oxauth/token`

To obtain an Access Token, an ID Token, and optionally a Refresh Token,
the RP (Client) sends a Token Request to the Token Endpoint to obtain a
Token Response. Token Endpoint requires Client Authentication methods to 
authenticate clients to the authorization server.

Below are the Client Authentication methods:
<table border="1">
        <tr>
            <th>Method</th>
            <th>Description</th>
        </tr>
        <tr>
            <th>client_secret_basic</th>
            <td>Clients that have received a client_secret value from the 
            Authorization Server authenticate with the Authorization Server 
            using the HTTP Basic authentication scheme. </td>
        </tr>
        <tr>
            <th>client_secret_post</th>
            <td>Clients that have received a client_secret value from the Authorization Server, authenticate with the 
            Authorization Server by including the Client Credentials in the request body. </td>
        </tr>
        <tr>
            <th>client_secret_jwt</th>
            <td>Clients that have received a client_secret value from the 
            Authorization Server create a JWT using an HMAC SHA algorithm</td>
	 </tr>
	 <tr>
            <th>private_key_jwt</th>
            <td>Clients that have registered a public key sign a JWT using that key</td>
	 </tr>
	 <tr>
            <th>none</th>
            <td>The Client does not authenticate itself at the Token Endpoint, either because it uses only the Implicit Flow (and so does not use the Token Endpoint) or because it is a Public Client with no Client Secret or other authentication mechanism.</td>
	 </tr>
</table>
The JWT MUST contain the following REQUIRED Claim Values and MAY contain the following OPTIONAL Claim Values: 
<table border="1">
        <tr>
            <th>Claim Values</th>
            <th>Description</th>
        </tr>
        <tr>
            <th>iss</th>
            <td>REQUIRED. Issuer. This MUST contain the client_id of the OAuth Client.</td>
        </tr>
        <tr>
            <th>sub</th>
            <td>REQUIRED. Subject. This MUST contain the client_id of the OAuth Client. </td>
        </tr>
        <tr>
            <th>aud</th>
            <td>REQUIRED. Audience. The aud (audience) Claim. Value that identifies the Authorization Server as an intended audience. The Authorization Server MUST verify that it is an intended audience for the token. The Audience SHOULD be the URL of the Authorization Server's Token Endpoint.</td>
	 </tr>
	 <tr>
            <th>jti</th>
            <td>REQUIRED. JWT ID. A unique identifier for the token, which can be used to prevent reuse of the token. These tokens MUST only be used once, unless conditions for reuse were negotiated between the parties; any such negotiation is beyond the scope of this specification.</td>
	 </tr>
	 <tr>
            <th>exp</th>
            <td>REQUIRED. Expiration time on or after which the ID Token MUST NOT be accepted for processing.</td>
	 </tr>
	 <tr>
            <th>iat</th>
            <td>OPTIONAL. Time at which the JWT was issued. </td>
	 </tr>
</table>
For more details on [client Authentication](http://openid.net/specs/openid-connect-core-1_0.html#ClientAuthentication) 

###### URL
    http://gluu.org/oxauth/token

###### Parameters
<table border="1">
        <tr>
            <th>Parameter</th>
            <th>Required</th>
            <th>Description</th>
            <th>Data Type</th>
        </tr>
        <tr>
            <th>grant_type</th>
            <td>true</td>
            <td>Grant type value, one of these: authorization_code, implicit, password, client_credentials, refresh_token as described in OAuth 2.0 [RFC6749].</td>
            <td>string</td>
        </tr>
        <tr>
            <th>code</th>
            <td>false</td>
            <td>Code which is returned by authorization endpoint (For
                grant_type=authorization_code).</td>
            <td>string</td>
        </tr>
        <tr>
            <th>redirect_uri</th>
            <td>false</td>
            <td>Redirection uri to which the response will be sent. This
                uri MUST exactly match one of the redirection uri values for the client
                pre-registered at the OpenID Provider.</td>
            <td>string</td>
        </tr>
        <tr>
            <th>username</th>
            <td>false</td>
            <td>End-User username.</td>
            <td>string</td>
        </tr>
        <tr>
            <th>password</th>
            <td>false</td>
            <td>End-User password.</td>
            <td>string</td>
        </tr>
        <tr>
            <th>scope</th>
            <td>false</td>
            <td>OpenID Connect requests MUST contain the openid scope value. If the openid scope value is not present, the behavior is entirely unspecified. Other scope values MAY be present. Scope values used that are not understood by an implementation SHOULD be ignored.</td>
            <td>string</td>
        </tr>
        <tr>
            <th>assertion</th>
            <td>false</td>
            <td>Assertion.</td>
            <td>string</td>
        </tr>
        <tr>
            <th>refresh_token</th>
            <td>false</td>
            <td>Refresh token.</td>
            <td>string</td>
        </tr>
        <tr>
            <th>oxauth_exchange_token</th>
            <td>false</td>
            <td>oxauth_exchange_token.</td>
            <td>string</td>
        </tr>
        <tr>
            <th>client_id</th>
            <td>false</td>
            <td>OAuth 2.0 Client Identifier valid at the Authorization Server.</td>
            <td>string</td>
        </tr>
        <tr>
            <th>client_secret</th>
            <td>false</td>
            <td>The client secret. The client MAY omit the parameter if the client secret is an empty string.</td>
            <td>string</td>
        </tr>
    </table>

###### Response
[JSON[Response]](#successful-reponse)


###### Errors
<table border="1">
    <tr>
        <th>Status Code</th>
        <th>Reason</th>
    </tr>
        <tr>
            <td>400</td>
            <td>invalid_request&#10; The request is missing a required parameter, includes an unsupported parameter value (other than grant type), repeats a parameter, includes multiple credentials,&#10; utilizes more than one mechanism for authenticating the client, or is otherwise malformed.</td>
        </tr>
        <tr>
            <td>400</td>
            <td>invalid_client&#10;Client authentication failed (e.g., unknown client, no client authentication included, or unsupported&#10;authentication method). The authorization server MAY return an HTTP 401 (Unauthorized) status code to indicate&#10;which HTTP authentication schemes are supported. If the client attempted to authenticate via the &quot;Authorization&quot;&#10;request header field, the authorization server MUST respond with an HTTP 401 (Unauthorized) status code and&#10;include the &quot;WWW-Authenticate&quot; response header field matching the authentication scheme used by the client.</td>
        </tr>
        <tr>
            <td>400</td>
            <td>invalid_grant&#10; The provided authorization grant (e.g., authorization code, resource owner credentials) or refresh token is&#10; invalid, expired, revoked, does not match the redirection uri used in the authorization request, or was issued to another client.</td>
        </tr>
        <tr>
            <td>400</td>
            <td>unauthorized_client&#10;The authenticated client is not authorized to use this authorization grant type.</td>
        </tr>
        <tr>
            <td>400</td>
            <td>unsupported_grant_type&#10;The authorization grant type is not supported by the authorization server.</td>
        </tr>
        <tr>
            <td>400</td>
            <td> invalid_scope&#10;The requested scope is invalid, unknown, malformed, or exceeds the scope granted by the resource owner.</td>
        </tr>
</table>

## API for oxAuth Clientinfo 

This document provides interface for Client Info REST web services.

### Path

`/oxauth/clientinfo`

### Overview

The ClientInfo Endpoint is an OAuth 2.0 Protected Resource that returns Claims about the registered client.

#### clientinfoGet

|Parameter|Description|Data Type|
|---------|-----------|---------|
|access_token |The access token for oxAuth|string|
|authorization| The authorization for the client|string|

#### clientinfoPost

|Parameter|Description|Data Type|
|---------|-----------|---------|
|access_token |The access token for oxAuth|string|
|authorization| The authorization for the client|string|

## OpenID Connect Register Client API

### Overview

Any OpenID Client needs to register with the OpenID Provider to utilize 
OpenID Services, in this case register a user, and acquire a client ID and a shared secret.

### Path

`/oxauth/register`

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

#### Client Registration Response

Upon successful registration, the client registration returns the newly-created Client Identifier and, if applicable, a Client Secret, along with all registered Metadata about this Client, including any fields provisioned by the Authorization Server itself. The Authorization Server MAY reject or replace any of the Client's requested field values and substitute them with suitable values. If this happens, the Authorization Server MUST include these fields in the response to the Client. An Authorization Server MAY ignore values provided by the client, and MUST ignore any fields sent by the Client that it does not understand. 

The response MAY contain a Registration Access Token that can be used by the Client to perform subsequent operations upon the resulting Client registration. 

A successful response SHOULD use the HTTP 201 Created status code and return a JSON document [RFC4627] using the application/json content type with the following fields and the Client Metadata parameters as top-level members of the root JSON object: 

<table border="1">
    <tr>
        <th>Parameter</th>
        <th>Description</th>
        <th>Required</th>
    <tr/>
        <tr>
            <td>client_id</td>
            <td>Unique Client Identifier. It MUST NOT be currently valid for any other registered Client.</td>
            <td>Required</td>
        </tr>
        <tr>
            <td>client_secret</td>
            <td>Client Secret. The same Client Secret value MUST NOT be assigned 
            to multiple Clients. This value is used by Confidential Clients to authenticate 
            to the Token Endpoint. It is not needed for Clients selecting a 
            `token_endpoint_auth_method` of `private_key_jwt` unless symmetric encryption will be used.</td>
            <td>Optional</td>
        </tr>
        <tr>
            <td>registration_access_token</td>
            <td>Registration Access Token that can be used at the 
            Client Configuration Endpoint to perform subsequent operations upon the Client registration.</td>
            <td>Optional</td>
        </tr>
        <tr>
            <td>registration_client_uri</td>
            <td>Location of the Client Configuration Endpoint where the Registration Access 
            Token can be used to perform subsequent operations upon the resulting Client registration. 
            Implementations MUST either return both a Client Configuration Endpoint 
            and a Registration Access Token or neither of them.</td>
            <td>Optional</td>
        </tr>
        <tr>
            <td>client_id_issued_at</td>
            <td>Time at which the Client Identifier was issued. Its value is a JSON number 
            representing the number of seconds from 1970-01-01T0:0:0Z as measured in UTC 
            until the date/time.</td>
            <td>Optional</td>
        </tr>
        <tr>
            <td>client_secret_expires_at</td>
            <td>if client_secret is issued. Time at which the client_secret will 
            expire or 0 if it will not expire. Its value is a JSON number representing the number of 
            seconds from 1970-01-01T0:0:0Z as measured in UTC until the date/time.</td>
            <td>Required</td>
        </tr>

</table>


#### Client Registration Error Response

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
Other members MAY also be used. This specification defines the following error codes: 
<table border="1">
    <tr>
        <th>Status Code</th>
        <th>Description</th>
    <tr/>
        <tr>
            <td>invalid_redirect_uri</td>
            <td>The value of one or more redirect_uris is invalid.</td>
        </tr>
        <tr>
            <td>invalid_client_metadata</td>
            <td>The value of one of the Client Metadata fields is invalid and the 
            server has rejected this request. Note that an Authorization Server MAY 
            choose to substitute a valid value for any requested parameter of a Client's Metadata.</td>
        </tr>
</table>

Below is an example of Error Response

      HTTP/1.1 400 Bad Request
      Content-Type: application/json
      Cache-Control: no-store
      Pragma: no-cache
    
      {
       "error": "invalid_redirect_uri",
       "error_description": "One or more redirect_uri values are invalid"
      }

### registerPut
**PUT** `/oxauth/register`

This operation updates the Client Metadata for a registered client.
#### URL
    http://gluu.org/oxauth/register
#### Parameters
The request is sent as an `HTTP PUT` request to the client registration endpoint with JSON object containing updated client's metadata in its body.

|Parameter|Description|
|---------|-----------|
|client_id |Url query parameter containing id of the client to update|
|Authorization header|Authorization header carrying "registration_access_token" issued before as a Bearer token|
|Request's body|JSON object containing client's metadata|

#### Response
Client Identificator or INUM, a client shared secret and the account expiration date in a [JSON Response](#Client Registration Error Response)

### registerGet
**GET** `/oxauth/register`

This operation retrieves the Client Metadata for a previously registered client.
#### URL
    http://gluu.org/oxauth/register
#### Parameters
The request is sent as an `HTTP POST` to the client registration endpoint as JSON with the parameters.

|Parameter|Description|
|---------|-----------|
|client_id |Url query parameter containing id of the client which properties are being requested|
|Authorization header|Authorization header carrying "registration_access_token" issued before as a Bearer token|
 
#### Response
Client Identificator or INUM, a client shared secret and the account expiration date in a [JSON Response](#Client Registration Error Response)

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

## OpenID Connect End Session API

#### Overview

#### Path

`/oxauth/end_session`

##### requestEndSession

**GET** 

`/oxauth/end_session`

End current Connect session.


###### URL
    http://gluu.org/oxauth/end_session
###### Parameters
- query

    <table border="1">
        <tr>
            <th>Parameter</th>
            <th>Required</th>
            <th>Description</th>
            <th>Data Type</th>
        </tr>
        <tr>
            <th>id_token_hint</th>
            <td>true</td>
            <td>Previously issued ID Token (id_token) passed to the logout endpoint as a hint about the End-User&#39;s current authenticated session with the Client. This is used as an indication of the identity of the End-User that the RP is requesting be logged out by the OP. The OP need not be listed as an audience of the ID Token when it is used as an id_token_hint value.</td>
            <td>string</td>
        </tr>
        <tr>
            <th>post_logout_redirect_uri</th>
            <td>false</td>
            <td>URL to which the RP is requesting that the End-User&#39;s User Agent be redirected after a logout has been performed. The value MUST have been previously registered with the OP, either using the post_logout_redirect_uris Registration parameter or via another mechanism. If supplied, the OP SHOULD honor this request following the logout.</td>
            <td>string</td>
        </tr>
        <tr>
            <th>state</th>
            <td>false</td>
            <td>Opaque value used by the RP to maintain state between the logout request and the callback to the endpoint specified by the post_logout_redirect_uri parameter. If included in the logout request, the OP passes this value back to the RP using the state query parameter when redirecting the User Agent back to the RP.</td>
            <td>string</td>
        </tr>
        <tr>
            <th>session_state</th>
            <td>false</td>
            <td>JSON [RFC7159] string that represents the End-User's login state at the OP. It MUST NOT contain the space (" ") character. This value is opaque to the RP. This is REQUIRED if session management is supported.</td>
            <td>string</td>
        </tr>
    </table>

###### Response
Client Identificator or INUM, a client shared secret and the account expiration date in a [JSON Response](#Client Registration Error Response)


###### Errors
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
            <td>400</td>
            <td>invalid_grant&#10;The provided access token is invalid, or was issued to another client.</td>
        </tr>
</table>

## OpenID Connect User Info API

### Overview


### Path

`/oxauth/userinfo`

#### requestUserInfoPost

**POST** 

`/oxauth/userinfo`

Returns Claims about the authenticated End-User.
The Access Token obtained from an OpenID Connect Authentication Request is 
sent as a Bearer Token.

###### URL
    http://gluu.org/oxauth/userinfo
###### Parameters
- form

    <table border="1">
        <tr>
            <th>Parameter</th>
            <th>Required</th>
            <th>Description</th>
            <th>Data Type</th>
        </tr>
        <tr>
            <th>access_token</th>
            <td>true</td>
            <td>OAuth 2.0 Access Token.</td>
            <td>string</td>
        </tr>
    </table>
- header

    <table border="1">
        <tr>
            <th>Parameter</th>
            <th>Required</th>
            <th>Description</th>
            <th>Data Type</th>
        </tr>
        <tr>
            <th>Authorization</th>
            <td>false</td>
            <td></td>
            <td>string</td>
        </tr>
    </table>

###### Response
[JSON[Response]](#successful-reponse)


###### Errors
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
</table>

##### requestUserInfoGet
**GET** `/oxauth/userinfo`

Returns Claims about the authenticated End-User.
The Access Token obtained from an OpenID Connect Authentication Request is sent as a Bearer Token.

###### URL
    http://gluu.org/oxauth/userinfo
###### Parameters
- query

    <table border="1">
        <tr>
            <th>Parameter</th>
            <th>Required</th>
            <th>Description</th>
            <th>Data Type</th>
        </tr>
        <tr>
            <th>access_token</th>
            <td>true</td>
            <td>OAuth 2.0 Access Token.</td>
            <td>string</td>
        </tr>
    </table>
- header

    <table border="1">
        <tr>
            <th>Parameter</th>
            <th>Required</th>
            <th>Description</th>
            <th>Data Type</th>
        </tr>
        <tr>
            <th>Authorization</th>
            <td>false</td>
            <td></td>
            <td>string</td>
        </tr>
    </table>

###### Response
[JSON[Response]](#successful-reponse)


###### Errors
<table border="1">
    <tr>
        <th>Status Code</th>
        <th>Reason</th>
    </tr>
        <tr>
            <td>400</td>
            <td>invalid_request&#10;The request is missing a required parameter, includes an unsupported parameter or parameter value, repeats the same parameter, uses more than one method for including an access token, or is otherwise malformed. The resource server SHOULD respond with the HTTP 400 (Bad Request) status code.</td>
        </tr>
        <tr>
            <td>401</td>
            <td>invalid_token&#10;The access token provided is expired, revoked, malformed, or invalid for other reasons. The resource SHOULD respond with the HTTP 401 (Unauthorized) status code. The client MAY request a new access token and retry the protected resource request.</td>
        </tr>
        <tr>
            <td>403</td>
            <td>insufficient_scope&#10;The request requires higher privileges than provided by the access token. The resource server SHOULD respond with the HTTP 403 (Forbidden) status code and MAY include the &quot;scope&quot;&#10; attribute with the scope necessary to access the protected resource.</td>
        </tr>
</table>
