Gluu Server supports Security Assertion Markup Language (SAML) and OpenID Connect protocols to authenticate users against Service Providers (SPs) and Requesting Parties (RPs). There are two different flows of SAML known as outbound SAML and inbound SAML, both supported out-of-the-box in Gluu Server Community Edition (Gluu CE).

## SAML

Security Assertion Markup Language (SAML) is an authentication and authorization protocol that defines the transaction process for XML-encoded assertions about authentication, authorization and attributes. The protocol is goverened by [Security Assertion Markup Language Core
(SAML) V2.0](https://docs.oasis-open.org/security/saml/v2.0/saml-core-2.0-os.pdf "SAML 2.0 Core"). The goal of this protocol is to exchange authentication and authorization data between Service Providers (SP) and the Identity Provider (IDP).
Gluu Server supports both inbound and outbound flow of SAML transaction. The oxTrutst administrator interface makes it easy to use SAML.

Trust Relationships are the foundation on which SAML works. Gluu Server makes it easy to setup Trust Relationships from the oxTrust admin interface. There are two types of flow Gluu CE supports, inbound and outbound SAML.
Trust Relationship creation is mandatory in both flows; however, the inbound flow also acts as a SAML proxy. The details about how to setup a Trust Relationship and how to setup SAML proxy follows later in this documentation. The image below is taken from wikipedia, showing a SAML transaction workflow.

![wikipedia image](https://upload.wikimedia.org/wikipedia/en/0/04/Saml2-browser-sso-redirect-post.png)

## OpenID Connect

![image](http://wiki.openid.net/f/openid-logo-wordmark.png)

[OpenID Connect](http://openid.net/connect "Connect") is a standard profile of OAuth2 which defines a protocol to enable any website, mobile application to verify the identity of the user accessing its resources through an authorization server or identity server. The protocol is API friendly and works through endpoints making it easy for applications to use it. 

OpenID Connect specification consists of different documents which outline different aspects of the protocol. The basic implementation requires the [OpenID Connect Core Specification](http://openid.net/specs/openid-connect-core-1_0.html "Core Specification"). The figure below taken from the [OpenID Connect website](http://openid.net/ "openid.net") shows the overview of the protocol and the different parts of the specification.

![openid.net image](http://openid.net/wordpress-content/uploads/2014/02/OpenIDConnect-Map-4Feb2014.png)

### Terminology


- Claim: Information about the entity
- ID Token: JSON Web Token (JWT) that contains claims about the authentication
- Issuer: The authority that issues the claims
- OpenID Provider (OP): OAuth2.0 authorization server that authenticates user through claims to the Relying Party (RP)
- Relying Party (RP): OAuth 2.0 Client application that requires authentication and claims from an OpenID Provider(OP)
- UserInfo Endpoint: An URL using https that returns authorization for the user from the OP to the RP

### Discovery

OpenID Connect provides a simple mechanism to notify about the available endpoints. This is difined in the [OpenID Connect Discovery Specification](http://openid.net/specs/openid-connect-discovery-1_0.html "OpenID Connect Discovery). 

In order for an OpenID Connect Relying Party (RP) to utilize OpenID Connect services for an End-User, the RP needs to know where the OpenID Provider is. OpenID Connect uses WebFinger to locate the OpenID Provider for an End-User.
Once the OpenID Provider has been identified, the configuration information for the OP is retrieved from a well-known location as a JSON document, including its OAuth 2.0 endpoint locations.
If you want to try a discovery request, you can make the following WebFinger request to discover the Issuer location:

```
GET /.well-known/webfinger?resource=https%3A%2F%2Fidp.gluu.org&rel=http%3A%2F%2Fopenid.net%2Fspecs%2Fconnect%2F1.0%2Fissuer HTTP/1.1
Host: idp.gluu.org

HTTP/1.1 200
Content-Type: application/jrd+json

{
    "subject": "https://idp.gluu.org",
    "links": [{
        "rel": "http://openid.net/specs/connect/1.0/issuer",
        "href": "https://idp.gluu.org"
    }]
}
```
## User-Managed Access (UMA)
![image](http://kantarainitiative.org/confluence/download/attachments/17760302/UMA-logo.png)

UMA is an oAuth based protocol to "enable a resource owner to control the authorization of data sharing and other protected-resource access made between online services on the owner’s behalf or with the owner’s authorization by an autonomous requesting party"[1][].

### Enterprise UMA
The Gluu Server implements UMA in a way that enables the protection of any web resource. Through the oxTrust interface, the server admin can write [custom authorization interception scripts][2] which may contain logic to grant (or forbid) access. The diagram below shows an overview of the UMA Authorization workflow.

![overview](../img/uma/overview.png "UMA Auth Overview")

### Terminology

- Resource Server (RS): Where the resources are held. 
- Authorization Server (AS): A server that governs access based on resource owner policies. 
- Requesting Party (RP): An end-user, or a corporation or other legal person, that uses a client to seek access to a protected resource. The requesting party may or may not be the same party as the resource owner. 
- Client: A web or native app that is used to access a digital resource. 
- Protection API Token (PAT): An entity seeking protection API access MUST have the scope "uma_protection". An access token with at least this scope is called a protection API token (PAT) and an entity that can acquire an access token with this scope is by definition a resource server. 
- Requesting Party Token (RPT): the token that a client presents to a resource server when trying to access a protected resource. 
- Authorization API Token (AAT): An entity seeking authorization API access MUST have the scope "uma_authorization". An access token with at least this scope is called an authorization API token (AAT) and an entity that can acquire an access token with this scope is by definition a client.

### UMA Workflow

The complete workflow sequence is shown in the diagram below. However there are two different authorization workflow given below for authorization and authorization token.

![auth-complete](../img/uma/auth-complete.png "UMA Complete Auth Workflow")

#### Authorization
![auth](../img/uma/auth.png "UMA Authorization Workflow")

#### Authorization Token
![auth-token](../img/uma/auth-token.png "UMA Authorization Token Workflow")

### Discovery

Gluu Server CE provides an endpoint for discovering information about UMA Provider configuration. A resource server or client can perform an HTTP GET on `https://<hostname>/.well-known/uma-configuration` to retrieve a JSON object indicating the UMA Provider configuration.

The following is an example of a GET request to the UMA configuration discovery endpoint:
```
{
  "version": "1.0",
  "issuer": "https://gluuserver.org",
  "pat_profiles_supported": [
    "bearer"
  ],
  "aat_profiles_supported": [
    "bearer"
  ],
  "rpt_profiles_supported": [
    "bearer"
  ],
  "pat_grant_types_supported": [
    "authorization_code"
  ],
  "aat_grant_types_supported": [
    "authorization_code"
  ],
  "claim_profiles_supported": [
    "openid"
  ],
  "dynamic_client_endpoint": "https://gluuserver.org/oxauth/seam/resource/restv1/oxauth/register",
  "token_endpoint": "https://gluuserver.org/oxauth/seam/resource/restv1/oxauth/token",
  "user_endpoint": "https://gluuserver.org/oxauth/seam/resource/restv1/oxauth/authorize",
  "introspection_endpoint": "https://gluuserver.org/oxauth/seam/resource/restv1/host/status",
  "resource_set_registration_endpoint": "https://gluuserver.org/oxauth/seam/resource/restv1/host/rsrc",
  "permission_registration_endpoint": "https://gluuserver.org/oxauth/seam/resource/restv1/host/rsrc_pr",
  "rpt_endpoint": "https://gluuserver.org/oxauth/seam/resource/restv1/requester/rpt",
  "authorization_request_endpoint": "https://gluuserver.org/oxauth/seam/resource/restv1/requester/perm",
  "scope_endpoint": "https://gluuserver.org/oxauth/seam/resource/restv1/uma/scopes"
}
```

!!! Note
    The UMA Response  may contain custom properties which are uniquely named for convenience and disguishing between standard & custom properties.

[1]:http://kantarainitiative.org/confluence/display/uma/Charter "UMA Charter"
[2]: ./oxtrust-ui.md "Custom Scripts"

## OAuth2.0 

![image](https://oauth.net/images/oauth-2-sm.png)

OAuth2.0 is the next version in the OAuth protocol focusing on simplicity with specific authorization flows for different platforms. The core specification is called the [OAuth 2.0 Authorization Framework](https://tools.ietf.org/html/rfc6749). OAuth introduces an authorization layer and separates the role of the client from the resource owner. The resource is accessed using access tokens instead of credentials.

### Terminology

- Resource Owner (RO): Entity that owns and controls the access to any resource
- Resource Server (RS): Where the resources are held
- Client: Any application/web-site that requests access to the protected resource stored in any RS.
- Authorization Server: The server issuing access tokens to the client after successfully authenticating the resource owner and obtaining authorization

### Workflows
####  Credentials Grant

The Client Credentials Grant allows [RO][] to use username and password as an authorization grant to obtain an access token. This flow is only encouraged when there is high degree of trust between [RO][] and the client and no other grant types are not available.

Although this grant requires direct client access to the [RO][] credentials it is used for a single request for an access token. This grant type can eliminate the need for the client to store the [RO][] credentials for future use, by exchanging the credentials with a long-lived access token or refresh token.

![client-credential-grant](../img/oauth2/client-credentials-grant.png)

The steps of the flow are:

1. The application requests an access token from the authorization server, authenticating the request with its client credentials.
2. If the client credentials are successfully authenticated, an access token is returned to the client.

This flow should be used when the resources of or any application/service are stored externally in cloud storages such as Google Storage or Amazon S3 which can be accessed using API. In this case the application needs to read and update these resources, but acting on behalf of the app itself rather than any individual user. The application can ask the OAuth authorization server for an access token directly, without the involvement of any end user.

The following is an example showing the messages between the client and the authorization server, also the example shows code fragments using the oxAuth-Client.jar API to interact with the authorization server.

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

[RO]: ./oxtrust-ui.md#41-terminology "Resource Owner"

The message sent to the authorization server is

|Request|
|-------|
|POST /oxauth/seam/resource/restv1/oxauth/token HTTP/1.1
Host: seed.gluu.org
Authorization: Basic QCExMTExITAwMDghRkY4MSEyRDM5OjYyMTNlOWI5LWM0NmQtNDAwOC04YWYxLTAzZjkxOGE4YWRlNA==
Content-Type: application/x-www-form-urlencoded
grant_type=client_credentials&scope=storage|

|Response upon successful authentication|
|--------|
|HTTP/1.1 200
Content-Type: application/json
Cache-Control: no-store, private
Pragma: no-cache
{"access_token":"c769d7ff-c476-42ab-b531-fe2f60b2f5cc","token_type":"bearer","expires_in":3600}|

#### Resource Owner Password Credential Grant

This grant allows the usage of [RO][] password credentials as an authorization grant to obtain an access token. This grant is encouraged in a high trust situation as well. The diagram below shows the flow


![password-credential-grant](../img/oauth2/password-credential-grant.png)

The steps of the flow are:
1. User presents their credentials to the application in addition to a username and password.
2. If the client credentials are successfully authenticated, an access token is returned to the client

This flow should be sparingly used bacause the password for the [RO][] is exposed to the appilcation/client. It is recommended only for first-party "official"  applications released by the API provider, and not opened up to wider third-party developer communities. If a user is asked to toe their password into "official" applications, they may become acustomed to doing so and becom evulneralbe to phishing attempts by other apps. In order to mitigat this concern, developers and IT administrators should clearly educate their users how they should dertermine which apps are "official" and which are not.

The following is an example showing the messages between the client and the authorization server, also the example shows code fragments using the oxAuth-Client.jar API to interact with the authorization server.

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

The message sent to the authorization server is


|Request|
|-------|
|POST /oxauth/seam/resource/restv1/oxauth/token HTTP/1.1
Host: seed.gluu.org
Authorization: Basic QCExMTExITAwMDghRkY4MSEyRDM5OjYyMTNlOWI5LWM0NmQtNDAwOC04YWYxLTAzZjkxOGE4YWRlNA==
Content-Type: application/x-www-form-urlencoded
grant_type=password&scope=openid&username=mike&password=secret|

|Response upon successful authentication|
|---------------------------------------|
|HTTP/1.1 200
Content-Type: application/json
Cache-Control: no-store, private
Pragma: no-cache
{"access_token":"26d55e4b-6c61-40ea-9763-3282f5db0f0e","token_type":"bearer","expires_in":3599,"refresh_token":"aba91bd9-aa10-4fca-952b-50a9a9afac28","scope":"openid","id_token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvc2VlZC5nbHV1Lm9yZyIsInVzZXJfaWQiOiJtaWtlIiwiYXVkIjoiQCExMTExITAwMDghRkY4MSEyRDM5IiwiZXhwIjoxMzM5MTk2ODgxMzAzLCJveEludW0iOiJAITExMTEhMDAwMCFENEU3Iiwib3hWYWxpZGF0aW9uVVJJIjoiaHR0cHM6XC9cL3NlZWQuZ2x1dS5vcmdcL294YXV0aFwvc2VhbVwvcmVzb3VyY2VcL3Jlc3R2MVwvb3hhdXRoXC9jaGVja19zZXNzaW9uIiwib3hPcGVuSURDb25uZWN0VmVyc2lvbiI6Im9wZW5pZGNvbm5lY3QtMS4wIn0.SzWfJsmlz62qTRw1lEJZ8PygY9eRupgmsbXLCQwPVDQ"}|

#### Gluu OAuth2 Access Management

##### Security Properties
There are some security benefits to using this flow against authenticating API calls with a username and password (via HTTP Basic access authentication or similar) although the application has access to the resource owner's password. With Basic authentication, an application needs to have continuous access to the user’s password in order to make API calls. If the user wants to revoke the access of the client, he must change the password and re-enter the password in all the applications that are allowed access to the resource.

However, if the OAuth Resource Owner Password flow is used, the application only needs access to the user’s credentials once: on first use when the credentials are exchanged for an access token. This means there’s no requirement for the app to store these credentials within the application or on the device, and revoking access is easy as well.

##### User Experience

The user experience for this flow is identical to typical password-based access requests. The application asks the user for their username and password and the user provides the information. The application then makes either a server-side or client-side request to the API provider’s authorization server, without any user-facing interface changes. If the API provider does not issue a refresh_token and the issued access_token is short-lived, the application will likely store the username and password for future authentication attempts. Unfortunately, this defeats some of the benefit of this flow.

#### Gluu OAuth2 Access Management

This flow uses Gluu Access Token (GAT) for access management. The flow needs a profile enabling a client to obtain a token from the [AS][] by explicitly specifyting the requested scopes. The diagram below shows the overview of the flow.

![gat](../img/oauth2/gat.png)

[GAT][] as a plain json object looks like the example below
```
{
    "exp": 1256953732,
    "iat": 1256912345,
    "scopes" : {
       "view", "manage"
    }
} 
```

The [GAT][] is issued at the endpoint published at `https://<hostname>/.well-known/uma-configuration`. Please note that all requests/response to/from/between RP, [RS][], [AS][] must contain "[GAT][]" HTTP header with `true` value. In this way [AS][] differentiantes calls from normal UMA.The example below shows a response with [GAT][] value set to `true`.
```
POST /gat HTTP/1.1
Host: as.example.com
Authorization: Bearer jwfLG53^sad$#f
GAT: true

{
 "scopes": ["view", "manage"]
}
```

The message sent to the authorization server is

|Request|
|-------|
|GET /users/alice/album/photo.jpg HTTP/1.1
Authorization: Bearer vF9dft4qmT
Host: gluu.example.com
GAT: true|

|Response with `rpt`|
|-------------------|
|HTTP/1.1 200 OK
Content-Type: application/json
GAT: true
{
  "rpt": "sbjsbhs(/SSJHBSUSSJHVhjsgvhsgvshgsv"
}|

[GAT]: ./oxtrust-ui.md#423-gluu-oauth2-access-management "Gluu Access Token"
[AS]: ./oxtrust-ui.md#41-terminology "Authorization Server"

## SCIM

SCIM stands for System for Cross-domain Identity Management which is a specification designed to manage user identity in cloud-based applications and services in a standardized way. Gluu Server supports SCIM version 1.0 and 2.0 out of the box. The following diagram shows the SCIM model from the [SCIM Website](http://www.simplecloud.info/).

![scim-model](../img/scim/scim-model.png)

The SCIM Specifications are available from the SCIM Website. There are two specifications in SCIM 2.0:

1. [SCIM 2.0 Core Specifications](https://tools.ietf.org/html/rfc7643)
2. [SCIM 2.0 Protocol Specification](https://tools.ietf.org/html/rfc7644)

### Terminology

The SCIM specification defines some basic terms that are used in the document. The basic terms like attribute, [SP][] are same across all the protocols. A few confusing ones are listed below from the [SCIM 2.0 Specs](https://tools.ietf.org/html/rfc7643).

- Resource:  An artifact that is managed by a service provider and that
      contains one or more attributes, e.g., "User" or "Group".

- Resource Type:  A type of a resource that is managed by a service provider.  The
      resource type defines the resource name, endpoint URL, schemas,
      and other metadata that indicate where a resource is managed and
      how it is composed, e.g., "User" or "Group".

- Schema: A collection of attribute definitions that describe the contents of an entire or partial resource, e.g.,
      "urn:ietf:params:scim:schemas:core:2.0:User".

The details of the SCIM API are given later in this documentation.
