## UMA 2 API Document
User-Managed Access (UMA) is a profile of OAuth 2.0. UMA defines how 
resource owners can manipulate to protect the resources.
The client can have access by arbitrary requesting parties, which means the 
requesting resource can be any number of resource servers and a centralized 
authorization server managing the access based on protected resource rules and policies defined.


In order to increase interoperable communication among the 
authorization server, resource server, and client, UMA leverages 
two purpose-built APIs related to the outsourcing of authorization, 
themselves protected by OAuth (or an OAuth-based authentication protocol) in embedded fashion.


A summary of UMA 2.0 communications as below

```
                                             +------------------+
                                             |     resource     |
       +------------manage (out of scope)----|       owner      |
       |                                     +------------------+
       |                                               |
       |                protection                     |
       |                API access                  control
       |                token (PAT)              (out of scope)
       |                                               |
       v                                               v
+------------+                    +----------+------------------+
|            |                    |protection|                  |
|  resource  |                    |   API    |   authorization  |
|   server   |<-----protect-------| (needs   |      server      |
|            |                    |   PAT)   |                  |
+------------+                    +----------+------------------+
| protected  |                               |        UMA       |
| resource   |                               |       grant      |
|(needs RPT) |          requesting           |  (PCT optional)  |
+------------+          party token          +------------------+
       ^                  (RPT)               ^  persisted   ^
       |                                      |   claims     |
       |                                    push   token     |
       |                                   claim   (PCT)     |
       |                                   tokens         interact
       |                                      +--------+    for
       +------------access--------------------| client |   claims
                                              +--------+  gathering
                                                +---------------+
                                                |  requesting   |
                                                |     party     |
                                                +---------------+
```
Source: [Kantara initiative](https://docs.kantarainitiative.org/uma/ed/oauth-uma-federated-authz-2.0-07.html).

Most of the documentation is based on UMA 2 specifications since implementation is based on it

- [UMA 2.0 Grant for OAuth 2.0 Authorization Specification](https://docs.kantarainitiative.org/uma/ed/oauth-uma-grant-2.0-06.html)
- [Federated Authorization for UMA 2.0 Specification](https://docs.kantarainitiative.org/uma/ed/oauth-uma-federated-authz-2.0-07.html)

## UMA Discovery API

** /.well-known/uma2-configuration**

#### Overview

### PATH

`/.well-known/uma2-configuration`

##### getConfiguration
**GET** `/.well-known/uma2-configuration`

Provides configuration data as JSON document. It contains options and
endpoints supported by the authorization server.

###### URL
    http://sample.com/.well-known/uma2-configuration

###### Parameters

No parameters

###### Response
```json
{
  "issuer" : "https://sample.com",
  "authorization_endpoint" : "https://sample.com/oxauth/restv1/authorize",
  "token_endpoint" : "https://sample.com/oxauth/restv1/token",
  "jwks_uri" : "https://sample.com/oxauth/restv1/jwks",
  "registration_endpoint" : "https://sample.com/oxauth/restv1/register",
  "response_types_supported" : [ "code", "id_token", "token" ],
  "grant_types_supported" : [ "authorization_code", "implicit", "client_credentials", "urn:ietf:params:oauth:grant-type:uma-ticket" ],
  "token_endpoint_auth_methods_supported" : [ "client_secret_basic", "client_secret_post", "client_secret_jwt", "private_key_jwt" ],
  "token_endpoint_auth_signing_alg_values_supported" : [ "HS256", "HS384", "HS512", "RS256", "RS384", "RS512", "ES256", "ES384", "ES512" ],
  "service_documentation" : "http://sample.com/docs",
  "ui_locales_supported" : [ "en", "es" ],
  "op_policy_uri" : "http://ox.sample.com/doku.php?id=oxauth:policy",
  "op_tos_uri" : "http://ox.sample.com/doku.php?id=oxauth:tos",
  "introspection_endpoint" : "https://sample.com/oxauth/restv1/rpt/status",
  "code_challenge_methods_supported" : null,
  "claims_interaction_endpoint" : "https://sample.com/oxauth/restv1/uma/gather_claims",
  "uma_profiles_supported" : [ ],
  "permission_endpoint" : "https://sample.com/oxauth/restv1/host/rsrc_pr",
  "resource_registration_endpoint" : "https://sample.com/oxauth/restv1/host/rsrc/resource_set",
  "scope_endpoint" : "https://sample.com/oxauth/restv1/uma/scopes"
}
```

###### Errors
<table border="1">
    <tr>
        <th>Status Code</th>
        <th>Reason</th>
    </tr>
    <tr>
        <td>500</td>
        <td>Failed to build UMA configuration JSON object.</td>
    </tr>
</table>


## UMA 2 Token Endpoint API

### Overview

### PATH

`/token`

### requestRpt

**POST** 

`/token`

Client Requests RPT.

###### URL
    http://sample.com/token

###### Parameters

- grant_type - REQUIRED. MUST be the value urn:ietf:params:oauth:grant-type:uma-ticket.
- ticket - REQUIRED. The most recent permission ticket received by the client as part of this authorization process.
- claim_token - OPTIONAL. If this parameter is used, it MUST appear together with the claim_token_format parameter. A string containing directly pushed claim information in the indicated format. It MUST be base64url encoded unless specified otherwise by the claim token format. The client MAY provide this information on both first and subsequent requests to this endpoint. The client and authorization server together might need to establish proper audience restrictions for the claim token prior to claims pushing.
- claim_token_format - OPTIONAL. If this parameter is used, it MUST appear together with the claim_token parameter. A string specifying the format of the claim token in which the client is directly pushing claims to the authorization server. The string MAY be a URI. Examples of potential types of claim token formats are [OIDCCore] ID Tokens and SAML assertions.
- pct - OPTIONAL. If the authorization server previously returned a PCT along with an RPT, the client MAY include the PCT in order to optimize the process of seeking a new RPT. Given that some claims represented by a PCT are likely to contain identity information about a requesting party, a client supplying a PCT in its RPT request MUST make a best effort to ensure that the requesting party using the client now is the same as the requesting party that was associated with the PCT when it was issued. The client MAY use the PCT for the same requesting party when seeking an RPT for a resource different from the one sought when the PCT was issued, or a protected resource at a different resource server entirely. See Section 5.3 for additional PCT security considerations. See Section 3.3.5 for the form of the authorization server's response with a PCT.
- rpt - OPTIONAL. Supplying an existing RPT gives the authorization server the option of upgrading that RPT instead of issuing a new one (see Section 3.3.5.1 for more about this option).
- scope - OPTIONAL. A string of space-separated values representing requested scopes. For the authorization server to consider any requested scope in its assessment, the client MUST have pre-registered the same scope with the authorization server. The client should consult the resource server's API documentation for details about which scopes it can expect the resource server's initial returned permission ticket to represent as part of the authorization assessment (see Section 3.3.4).

###### Response

Sample response:
```
POST /token HTTP/1.1
Host: as.example.com
Authorization: Basic jwfLG53^sad$#f
...
grant_type=urn%3Aietf%3Aparams%3Aoauth%3Agrant-type%3Auma-ticket
&ticket=016f84e8-f9b9-11e0-bd6f-0021cc6004de
&claim_token=eyj0...
&claim_token_format=http%3A%2F%2Fopenid.net%2Fspecs%2Fopenid-connect-core-1_0.html%23IDToken
&pct=c2F2ZWRjb25zZW50
&rpt=sbjsbhs(/SSJHBSUSSJHVhjsgvhsgvshgsv
&scope=read
```


###### Errors
<table border="1">
    <tr>
        <th>Status Code</th>
        <th>Reason</th>
    </tr>
        <tr>
            <td>403</td>
            <td>Forbidden. Example of a &quot;need_info&quot; respo
            nse with a full set of &quot;error_details&quot; hints:&#10;&#10;HTTP/1.1 403 Forbidden&#10;Content-Type: application/json&#10;Cache-Control: no-store&#10;...&#10;&#10;{&#10; &quot;error&quot;: &quot;need_info&quot;,&#10; &quot;error_details&quot;: {&#10;   &quot;authentication_context&quot;: {&#10;     &quot;required_acr&quot;: [&quot;https://example.com/acrs/LOA3.14159&quot;]&#10;   },&#10;   &quot;requesting_party_claims&quot;: {&#10;     &quot;required_claims&quot;: [&#10;       {&#10;         &quot;name&quot;: &quot;email23423453ou453&quot;,&#10;         &quot;friendly_name&quot;: &quot;email&quot;,&#10;         &quot;claim_type&quot;: &quot;urn:oid:0.9.2342.19200300.100.1.3&quot;,&#10;         &quot;claim_token_format&quot;: &#10;[&quot;http://openid.net/specs/openid-connect-core-1_0.html#HybridIDToken&quot;],&#10;         &quot;issuer&quot;: [&quot;https://example.com/idp&quot;]&#10;       }&#10;     ],&#10;     &quot;redirect_user&quot;: true,&#10;     &quot;ticket&quot;: &quot;016f84e8-f9b9-11e0-bd6f-0021cc6004de&quot;&#10;   }&#10; }&#10;}&#10;</td>
        </tr>
        <tr>
            <td>401</td>
            <td>Unauthorized</td>
        </tr>
        <tr>
            <td>400</td>
            <td>Bad request</td>
        </tr>
</table>


## UMA 2 Resource Registration API 

**/host/rsrc/resource_set**

### Overview
Resource is defined by the resource server, which is required
by the authorization server to register the resource description.

Resource description is a JSON document with the 
following properties described in [Resource](#Resource)

RESTful API  is used by Resource Server at the authorization server's 
resource registration endpoint to create, read, update, and delete 
resource description.


Request to the resource is registration is incorrect, the authorization
server responds with an with error message by including the below  error 
codes in the response. Discussed detail in [unsupported methods](#unsupportedHeadMethod)

- unsupported_method_type: The resource server request used an unsupported HTTP method. 
  The authorization server MUST respond with the HTTP 405 (Method Not Allowed) status code.
- not_found: The resource requested from the authorization server cannot be 
  found. The authorization server MUST respond with HTTP 404 (Not Found) status code.

### PATH
 `/host/rsrc/resource_set/{rsid}`

#### deleteResource

**DELETE** `/host/rsrc/resource_set/{rsid}`

Deletes a previously registered resource description using the
DELETE method, thereby removing it from the authorization server's
protection regime.

###### URL
    http://sample.com/host/rsrc/resource_set/{rsid}
        

###### Parameters

- rsid - REQUIRED. Resource ID.

Sample request
```
DELETE /host/rsrc/resource_set/22
Authorization: Bearer 204c69636b6c69
```

###### Response

Successful response

```
HTTP/1.1 204 No content
```

###### Errors

<table border="1">
    <tr>
        <th>Status Code</th>
        <th>Reason</th>
    </tr>
    <tr>
        <td>401</td>
        <td>Unauthorized</td>
    </tr>
</table>

- - -
##### getResource

**GET** 

`/host/rsrc/resource_set/{rsid}`

Reads a previously registered resource description using the GET
method. If the request is successful, the authorization server MUST
respond with a status message that includes a body containing the
referenced resource description, along with an "_id" property.

###### URL
    http://sample.com/host/rsrc/resource_set/{rsid}

###### Parameters

- rsid - REQUIRED. Resource ID.

Sample request
```
GET /host/rsrc/resource_set/22 HTTP/1.1
Authorization: Bearer MHg3OUZEQkZBMjcx
```

###### Response

Sample response
```
HTTP/1.1 200 OK
Content-Type: application/json
...
{  
   "_id":"KX3A-39WE",
   "resource_scopes":[  
      "read-public",
      "post-updates",
      "read-private",
      "http://www.example.com/scopes/all"
   ],
   "icon_uri":"http://www.example.com/icons/sharesocial.png",
   "name":"Tweedl Social Service",
   "type":"http://www.example.com/rsrcs/socialstream/140-compatible"
}
```

###### Errors
<table border="1">
    <tr>
        <th>Status Code</th>
        <th>Reason</th>
    </tr>
    <tr>
        <td>401</td>
        <td>Unauthorized</td>
    </tr>
</table>

- - -
##### updateResource

**PUT** `/host/rsrc/resource_set/{rsid}`

Updates a previously registered resource description using the PUT
method. If the request is successful, the authorization server MUST
respond with a status message that includes an "_id" property.

###### URL
    http://sample.com/host/rsrc/resource_set/{rsid}

Sample request
```
PUT /host/rsrc/resource_set/22 HTTP/1.1
Content-Type: application/json
Authorization: Bearer 204c69636b6c69
...
{  
   "resource_scopes":[  
      "http://photoz.example.com/dev/scopes/view",
      "public-read"
   ],
   "description":"Collection of digital photographs",
   "icon_uri":"http://www.example.com/icons/sky.png",
   "name":"Photo Album",
   "type":"http://www.example.com/rsrcs/photoalbum"
}
```

###### Response

Sample successful response
```
HTTP/1.1 200 OK
...
{  
   "_id":"22"
}
```

###### Errors
<table border="1">
    <tr>
        <th>Status Code</th>
        <th>Reason</th>
    </tr>
    <tr>
        <td>401</td>
        <td>Unauthorized</td>
    </tr>
</table>

- - -
### ResourceList

#### Path

**`/host/rsrc/resource_set`**

**GET** 

`/host/rsrc/resource_set`

Lists all previously registered resource identifiers for this user using the GET method. 
The authorization server MUST return the list in the form of a JSON array of {rsid} string values.

The resource server uses this method as a first step in checking whether its understanding of protected resources is in full synchronization with
the authorization server's understanding.

###### URL
    http://sample.com/host/rsrc/resource_set

###### Parameters

Sample request
```
GET http://sample.com/host/rsrc/resource_set HTTP/1.1
Authorization: Bearer 204c69636b6c69
```

###### Response

Sample of successful response
```
HTTP/1.1 200 OK
...
[  
   "11",
   "22"
]
```

###### Errors
<table border="1">
    <tr>
        <th>Status Code</th>
        <th>Reason</th>
    </tr>
    <tr>
        <td>401</td>
        <td>Unauthorized</td>
    </tr>
</table>

- - -
##### createResource
**POST** `/host/rsrc/resource`

Adds a new resource description using the POST method. If the
request is successful, the authorization server MUST respond with a
status message that includes an _id property.

###### URL
    http://sample.com/host/rsrc/resource_set

###### Parameters

Sample request
```
POST /host/rsrc/resource_set HTTP/1.1 
Content-Type: application/json
Authorization: Bearer MHg3OUZEQkZBMjcx
...
{  
   "resource_scopes":[  
      "read-public",
      "post-updates",
      "read-private",
      "http://www.example.com/scopes/all"
   ],
   "icon_uri":"http://www.example.com/icons/sharesocial.png",
   "name":"Tweedl Social Service",
   "type":"http://www.example.com/rsrcs/socialstream/140-compatible"
}
```

###### Response

Sample successful response

```
HTTP/1.1 201 Created
Content-Type: application/json
Location: /host/rsrc/resource_set/22
...
{  
   "_id":"KX3A-39WE",
   "user_access_policy_uri":"http://as.example.com/rs/222/resource/22/policy"
}
```

###### Errors
<table border="1">
    <tr>
        <th>Status Code</th>
        <th>Reason</th>
    </tr>
        <tr>
            <td>401</td>
            <td>Unauthorized</td>
        </tr>
</table>

- - -
### unsupportedHeadMethod
**HEAD** `/host/rsrc/resource_not`

Not allowed


- - -
### unsupportedOptionsMethod
**OPTIONS** 

`/host/rsrc/resource_set`

Not allowed


## Data Types

### <a name="Resource">Resource</a>

- resource_scopes - REQUIRED. An array of strings, serving as scope identifiers, indicating the available scopes for this resource. Any of the strings MAY be either a plain string or a URI.
- description - OPTIONAL. A human-readable string describing the resource at length. The authorization server MAY use this description in any user interface it presents to a resource owner, for example, for resource protection monitoring or policy setting. The value of this parameter MAY be internationalized, as described in Section 2.2 of [RFC7591].
- icon_uri - OPTIONAL. A URI for a graphic icon representing the resource. The authorization server MAY use the referenced icon in any user interface it presents to a resource owner, for example, for resource protection monitoring or policy setting.
- name - OPTIONAL. A human-readable string naming the resource. The authorization server MAY use this name in any user interface it presents to a resource owner, for example, for resource protection monitoring or policy setting. The value of this parameter MAY be internationalized, as described in Section 2.2 of [RFC7591].
- type - OPTIONAL. A string identifying the semantics of the resource. For example, if the resource is an identity claim that leverages standardized claim semantics for "verified email address", the value of this parameter could be an identifying URI for this claim. The authorization server MAY use this information in processing information about the resource or displaying information about it in any user interface it presents to a resource owner.

## UMA Permission Registration API 

** /host/rsrc_pr**

### Overview

###  PATH

`/host/rsrc_pr`

#### registerResourcePermission

**POST** 

`/host/rsrc_pr`

Registers permission using the POST method.
The resource server uses the POST method at the endpoint. The body of
the HTTP request message contains a JSON object providing the requested
permission, using a format derived from the scope description format
specified in [OAuth-resource-reg], as follows. The object has the
following properties:

###### URL
    http://sample.com/host/rsrc_pr

###### Parameters

- resource_id - REQUIRED. The identifier for a resource to which the resource server is requesting a permission on behalf of the client. The identifier MUST correspond to a resource that was previously registered.
- resource_scopes - REQUIRED. An array referencing zero or more identifiers of scopes to which the resource server is requesting access for this resource on behalf of the client. Each scope identifier MUST correspond to a scope that was previously registered by this resource server for the referenced resource.

Sample request

```json
POST /host/rsrc_pr HTTP/1.1
Content-Type: application/json
Host: as.example.com
Authorization: Bearer 204c69636b6c69
...

{  
   "resource_id":"112210f47de98100",
   "resource_scopes":[  
      "view",
      "http://photoz.example.com/dev/actions/print"
   ]
}
```

###### Response

Sample response
```
POST /perm HTTP/1.1
Content-Type: application/json
Host: as.example.com
Authorization: Bearer 204c69636b6c69
...

[  
   {  
      "resource_id":"7b727369647d",
      "resource_scopes":[  
         "view",
         "crop",
         "lightbox"
      ]
   },
   {  
      "resource_id":"7b72736964327d",
      "resource_scopes":[  
         "view",
         "layout",
         "print"
      ]
   },
   {  
      "resource_id":"7b72736964337d",
      "resource_scopes":[  
         "http://www.example.com/scopes/all"
      ]
   }
]
```

###### Errors
<table border="1">
    <tr>
        <th>Status Code</th>
        <th>Reason</th>
    </tr>
        <tr>
            <td>401</td>
            <td>Unauthorized</td>
        </tr>
        <tr>
            <td>400</td>
            <td>Bad Request</td>
        </tr>
</table>

## Token Introspection

** /rpt/status **

### Overview

### PATH 
`/rpt/status`

###### URL
    http://sample.com/rpt/status

###### Parameters


```
POST /rpt/status HTTP/1.1
Host: as.example.com
Authorization: Bearer 204c69636b6c69
...
token=sbjsbhs(/SSJHBSUSSJHVhjsgvhsgvshgsv
```

###### Response

- resource_id - REQUIRED. A string that uniquely identifies the protected resource, access to which has been granted to this client on behalf of this requesting party. The identifier MUST correspond to a resource that was previously registered as protected.
- resource_scopes - REQUIRED. An array referencing zero or more strings representing scopes to which access was granted for this resource. Each string MUST correspond to a scope that was registered by this resource server for the referenced resource.
- exp - OPTIONAL. Integer timestamp, measured in the number of seconds since January 1 1970 UTC, indicating when this permission will expire. If the token-level exp value pre-dates a permission-level exp value, the token-level value takes precedence.
- iat - OPTIONAL. Integer timestamp, measured in the number of seconds since January 1 1970 UTC, indicating when this permission was originally issued. If the token-level iat value post-dates a permission-level iat value, the token-level value takes precedence.
- nbf - OPTIONAL. Integer timestamp, measured in the number of seconds since January 1 1970 UTC, indicating the time before which this permission is not valid. If the token-level nbf value post-dates a permission-level nbf value, the token-level value takes precedence.

Sample response
```
HTTP/1.1 200 OK
Content-Type: application/json
Cache-Control: no-store
...

{  
   "active":true,
   "exp":1256953732,
   "iat":1256912345,
   "permissions":[  
      {  
         "resource_id":"112210f47de98100",
         "resource_scopes":[  
            "view",
            "http://photoz.example.com/dev/actions/print"
         ],
         "exp":1256953732
      }
   ]
}
```

###### Errors
<table border="1">
    <tr>
        <th>Status Code</th>
        <th>Reason</th>
    </tr>
    <tr>
        <td>405</td>
        <td>Introspection of RPT is not allowed by GET HTTP method.</td>
    </tr>
</table>

## UMA Authorization Context

Available context methods:
- `getClaimToken()` - returns `claim_token` as string
- `getClaimTokenClaim(String key)` - returns `claim_token` claim by key
- `getPctClaim(String key)` - returns PCT claim by key
- `getIssuer()` - returns issuer
- `getUser(String... returnAttributes)` - returns logged in user attributes
- `getUserDn()` - returns logged in user DN
- `getClient()` - returns client object
- `getScriptDn()` - returns script DN
- `getConfigurationAttributes()` - returns configuration attributes `Map<String, SimpleCustomProperty>`
- `getScopes()` - returns scopes set
- `getScriptScopes()` - returns scopes set that are bound to currently executed script
- `getResources()` - returns resources
- `getResourceIds()` - returns resource ids
- `getClaims()` - returns claim object (for claim manipulation)
- `getClaim(String key)` - convenient method to get claim (tries to fetch claim first from `claim_token` and if not found then tries to fetch it from PCT. If not found in PCT returns null.)
- `putClaim(String claimName, Object claimValue)` - put claim
- `hasClaim(String claimName)` - returns `true` or `false`
- `removeClaim(String claimName)` - removes claim
- `addRedirectUserParam(String paramName, String paramValue)` - adds custom user parameter which will be appended during redirect to Claims-Gathering Endpoint.
- `removeRedirectUserParameter(String paramName, String paramValue)` - removes custom user parameter
- `getRedirectUserParametersMap()` - returns custom user parameters map

Source code available [here](https://github.com/GluuFederation/oxAuth/blob/version_3.1.1/Server/src/main/java/org/xdi/oxauth/uma/authorization/UmaAuthorizationContext.java)

## UMA Claims-Gathering Context

Available context methods:
- `persist()` - persists changes made in claims or session objects
- `getConfigurationAttributes()` - returns configuration attributes `Map<String, SimpleCustomProperty>`
- `isAuthenticated()` - returns `true` of `false` to identify whether user is logged in
- `getUser(String... returnAttributes)` - returns logged in user attributes
- `getUserDn()` - returns logged in user DN
- `getClient()` - returns client object
- `getConnectSessionAttributes()` - returns Connect session attributes
- `getPageClaims()` - returns claims entered by user on given page
- `getRequestParameters()` - returns request parameters as `Map<String, String[]>`
- `getStep()` - returns step
- `setStep(int step)` - sets step
- `addSessionAttribute(String key, String value)` - adds session attribute
- `removeSessionAttribute(String key)` - removes session attribute
- `getSessionAttributes()` - returns session attribute as `Map<String, String>`
- `addRedirectUserParam(String paramName, String paramValue)` - adds custom user parameter 
- `removeRedirectUserParameter(String paramName, String paramValue)` - removes custom user parameter
- `getRedirectUserParametersMap()` - returns custom user parameters map
- `getPermissions()` - gets permissions for given ticket as `List<UmaPermission>`
- `getClaim(String key)` - gets claim
- `putClaim(String claimName, Object claimValue)` - put claim
- `hasClaim(String claimName)` - returns `true` or `false`
- `removeClaim(String claimName)` - removes claim
- `getIssuer()` - returns issuer

Source code available [here](https://github.com/GluuFederation/oxAuth/blob/version_3.1.1/Server/src/main/java/org/xdi/oxauth/uma/authorization/UmaGatherContext.java)