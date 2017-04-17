# OpenId Connect Authorization Grant
This page provides an interface for request authorization through REST web services.
## Path
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
        <tr>
            <th>securityContext</th>
            <td>false</td>
            <td>This is an injectable interface that provides access to security related information.</td>
            <td>string</td>
        </tr>
</table>
- query

<table border="1">
        <tr>
            <th>Parameter</th>
            <th>Required</th>
            <th>Description</th>
            <th>Data Type</th>
        </tr>
        <tr>
            <th>response_mode</th>
            <td>false</td>
            <td>Informs the Authorization Server of the mechanism to be used for returning parameters from the Authorization Endpoint. This use of this parameter is NOT RECOMMENDED when the Response Mode that would be requested is the default mode specified for the Response Type.</td>
            <td>string</td>
        </tr>
</table>

#### Response
[JSON[Response]](#JSON[Response])

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
[JSON[Response]](#JSON[Response])

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

