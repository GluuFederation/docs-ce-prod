# API Document

## /oxauth

## Overview


#### `/oxauth/end_session`

##### requestEndSession
**GET** `/oxauth/end_session`

End current Connect session.
End current Connect session.

###### URL
    http://gluu.org/oxauth/end_session
#### Parameters
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
            <th>session_id</th>
            <td>false</td>
            <td>Session ID</td>
            <td>string</td>
        </tr>
    </table>

#### Response
[JSON[Response]](#JSON[Response])


##### Errors
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


- - -

## Data Types
