# Client Credentials Grant

The Client Credentials Grant allows resource owner to use password
credentials (i.e. username and password) as an authorization grant to
obtain an access token. The credentials should only be used when there
is a high degree of trust between the resource owner and the client
(e.g. its device operating system or a highly privileged application),
and when other authorization grant types are not available (such as an
authorization code).

Even though this grant type requires direct client access to the
resource owner credentials, the resource owner credentials are used for
a single request and are exchanged for an access token. This grant type
can eliminate the need for the client to store the resource owner
credentials for future use, by exchanging the credentials with a
long-lived access token or refresh token.

The flow is illustrated below:

![flow](https://raw.githubusercontent.com/GluuFederation/docs/master/sources/img/openid_connect/client_credentials_grant.png)

The steps of the flow are:

1. The application requests an access token from the authorization server, authenticating the request with its client credentials.

2. If the client credentials are successfully authenticated, an access token is returned to the client.

## When Should the Client Credentials Flow Be Used?

The Client Credentials flow should be used when the resources of or any
application/service are stored externally in cloud storages such as
Google Storage or Amazon S3 which can be accessed using API. In this
case the application needs to read and update these resources, but
acting on behalf of the app itself rather than any individual user.
The application can ask the OAuth authorization server for an access
token directly, without the involvement of any end user.

## Example Flow

The following is an example showing the messages between the client and
the authorization server, also the example shows code fragments using
the oxAuth-Client.jar API to interact with the authorization server.

```
// Parameters
String tokenUrl = "https://seed.gluu.org/oxauth/seam/resource/restv1/oxauth/token";
 
// Request
TokenClient tokenClient = new TokenClient(tokenUrl);
TokenResponse response = tokenClient.execClientCredentialsGrant(scope, clientId, clientSecret);
 
int status response.getStatus(); // 200 if succeed
String accessToken = response.getAccessToken();
TokenType tokenType response.getTokenType(); // bearer
```

The message sent to the authorization server is:

* Request

```
POST /oxauth/seam/resource/restv1/oxauth/token HTTP/1.1
Host: seed.gluu.org
Authorization: Basic QCExMTExITAwMDghRkY4MSEyRDM5OjYyMTNlOWI5LWM0NmQtNDAwOC04YWYxLTAzZjkxOGE4YWRlNA==
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials&scope=storage
```

If the client credentials are successfully authenticated, an access token is returned to the client.

* Response

```
HTTP/1.1 200
Content-Type: application/json
Cache-Control: no-store, private
Pragma: no-cache

{"access_token":"c769d7ff-c476-42ab-b531-fe2f60b2f5cc","token_type":"bearer","expires_in":3600}
```

# Resource Owner Password Credentials Grant

The resource owner password credentials (i.e. username and password) can
be used directly as an authorization grant to obtain an access token.
The credentials should only be used when there is a high degree of trust
between the resource owner and the client (e.g. its device operating
system or a highly privileged application), and when other authorization
grant types are not available (such as an authorization code).

Even though this grant type requires direct client access to the
resource owner credentials, the resource owner credentials are used for
a single request and are exchanged for an access token. This grant type
can eliminate the need for the client to store the resource owner
credentials for future use, by exchanging the credentials with a
long-lived access token or refresh token.

The flow is illustrated below:

![flow](https://raw.githubusercontent.com/GluuFederation/docs/master/sources/img/openid_connect/resource_owner_password_credentials_flow.png)

The steps of the flow are:

1. User presents their credentials to the application in addition to a username and password.

2. If the client credentials are successfully authenticated, an access token is returned to the client

## When Should the Resource Owner Password Flow Be Used?

This flow should be used sparingly because the resource owner’s password
is exposed to the application. It is recommended only for first-party
“official” applications released by the API provider, and not opened up
to wider third-party developer communities. If a user is asked to type
their password into “official” applications, they may become accustomed
to doing so and become vulnerable to phishing attempts by other apps. In
order to mitigate this concern, developers and IT administrators should
clearly educate their users how they should determine which apps are
“official” and which are not.

## Security Properties

There are some security benefits to using this flow against
authenticating API calls with a username and password (via HTTP Basic
access authentication or similar) although the application has access to
the resource owner's password. With Basic authentication, an application
needs to have continuous access to the user’s password in order to make
API calls. If the user wants to revoke the access of the client, he must
change the password and re-enter the password in all the applications
that are allowed access to the resource.

However, if the OAuth Resource Owner Password flow is used, the
application only needs access to the user’s credentials once: on first
use when the credentials are exchanged for an access token. This means
there’s no requirement for the app to store these credentials within the
application or on the device, and revoking access is easy as well.

## User Experience

The user experience for this flow is identical to typical password-based
access requests. The application asks the user for their username and
password and the user provides the information. The application then
makes either a server-side or client-side request to the API provider’s
authorization server, without any user-facing interface changes. If the
API provider does not issue a refresh_token and the issued access_token
is short-lived, the application will likely store the username and
password for future authentication attempts. Unfortunately, this defeats
some of the benefit of this flow.

## Example Flow

The following is an example showing the messages between the client and
the authorization server, also the example shows code fragments using
the oxAuth-Client.jar API to interact with the authorization server.

```
// Parameters
String tokenUrl = "https://seed.gluu.org/oxauth/seam/resource/restv1/oxauth/token";
 
// Call the service
TokenClient tokenClient = new TokenClient(tokenUrl);
TokenResponse response = tokenClient.execResourceOwnerPasswordCredentialsGrant(username, password, scope, clientId, clientSecret);
 
// Handle response
int status = response.getStatus(); // 200 if succeed
String accessToken = response.getAccessToken(); // 26d55e4b-6c61-40ea-9763-3282f5db0f0e
TokenType tokenType = response.getTokenType(); // Enumeration: bearer
String refreshToken = response.getRefreshToken(); // aba91bd9-aa10-4fca-952b-50a9a9afac28
```

* Request

```
POST /oxauth/seam/resource/restv1/oxauth/token HTTP/1.1
Host: seed.gluu.org
Authorization: Basic QCExMTExITAwMDghRkY4MSEyRDM5OjYyMTNlOWI5LWM0NmQtNDAwOC04YWYxLTAzZjkxOGE4YWRlNA==
Content-Type: application/x-www-form-urlencoded

grant_type=password&scope=openid&username=mike&password=secret
```

* Response

```
HTTP/1.1 200
Content-Type: application/json
Cache-Control: no-store, private
Pragma: no-cache

{"access_token":"26d55e4b-6c61-40ea-9763-3282f5db0f0e","token_type":"bearer","expires_in":3599,"refresh_token":"aba91bd9-aa10-4fca-952b-50a9a9afac28","scope":"openid","id_token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc2VlZC5nbHV1Lm9yZyIsInVzZXJfaWQiOiJtaWtlIiwiYXVkIjoiQCExMTExITAwMDghRkY4MSEyRDM5IiwiZXhwIjoxMzM5MTk2ODgxMzAzLCJveEludW0iOiJAITExMTEhMDAwMCFENEU3Iiwib3hWYWxpZGF0aW9uVVJJIjoiaHR0cHM6XC9cL3NlZWQuZ2x1dS5vcmdcL294YXV0aFwvc2VhbVwvcmVzb3VyY2VcL3Jlc3R2MVwvb3hhdXRoXC9jaGVja19zZXNzaW9uIiwib3hPcGVuSURDb25uZWN0VmVyc2lvbiI6Im9wZW5pZGNvbm5lY3QtMS4wIn0.SzWfJsmlz62qTRw1lEJZ8PygY9eRupgmsbXLCQwPVDQ"}
```
# Gluu OAuth2 Access Management
[GAT][Gluu Access Token] is used for Gluu OAuth2 Access Management.
## Overview
![image](https://ox.gluu.org/lib/exe/fetch.php?media=uma:gat.png)
Centralized Access Management needs a profile enabling a client ot obtain a token from the AS by explicitly specifyting the 
requested scopes.
## Gluu Access Token
### GAT as plain json
```
{
    "exp": 1256953732,
    "iat": 1256912345,
    "scopes" : {
       "view", "manage"
    }
}
```

The [GAT][Gluu Access Token] is issued at a new endpoint which is published at `<hostname>/.well-known/uma-configuration`

**Important:** all requests/response to/from/between RP, RS, AS must contain "GAT" HTTP header with "true" value. In this way 
AS differentiante calls from normal UMA.

### AS Respnse for RP
```
POST /gat HTTP/1.1
Host: as.example.com
Authorization: Bearer jwfLG53^sad$#f
GAT: true

{
 "scopes": ["view", "manage"]
}
```

### AS Response for RP
GAT is returned in the `rpt` key as value.
```
HTTP/1.1 200 OK
Content-Type: application/json
GAT: true

{
  "rpt": "sbjsbhs(/SSJHBSUSSJHVhjsgvhsgvshgsv"
}
```

### RP Request Resource with GAT
```
GET /users/alice/album/photo.jpg HTTP/1.1
Authorization: Bearer vF9dft4qmT
Host: photoz.example.com
GAT: true
```

## Discovery
```
   ...
   "gat_endpoint":"https://<host>/<relative path>/gat",
   ...
```
 
