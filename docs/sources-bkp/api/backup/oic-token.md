# API Document

### /oxauth

## Overview

#### `/oxauth/token` 
#### requestAccessToken
**POST** `/oxauth/token`

To obtain an Access Token, an ID Token, and optionally a Refresh Token,
the RP (Client) sends a Token Request to the Token Endpoint to obtain a
Token Response.

###### URL
    http://gluu.org/oxauth/token
### Parameters
- form

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

#### Response
[JSON[Response]](#JSON[Response])


#### Errors
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


- - -

## Data Types
