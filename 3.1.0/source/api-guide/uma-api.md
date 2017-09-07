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
- claim_token_format = OPTIONAL. If this parameter is used, it MUST appear together with the claim_token parameter. A string specifying the format of the claim token in which the client is directly pushing claims to the authorization server. The string MAY be a URI. Examples of potential types of claim token formats are [OIDCCore] ID Tokens and SAML assertions.
= pct - OPTIONAL. If the authorization server previously returned a PCT along with an RPT, the client MAY include the PCT in order to optimize the process of seeking a new RPT. Given that some claims represented by a PCT are likely to contain identity information about a requesting party, a client supplying a PCT in its RPT request MUST make a best effort to ensure that the requesting party using the client now is the same as the requesting party that was associated with the PCT when it was issued. The client MAY use the PCT for the same requesting party when seeking an RPT for a resource different from the one sought when the PCT was issued, or a protected resource at a different resource server entirely. See Section 5.3 for additional PCT security considerations. See Section 3.3.5 for the form of the authorization server's response with a PCT.
- rpt - OPTIONAL. Supplying an existing RPT gives the authorization server the option of upgrading that RPT instead of issuing a new one (see Section 3.3.5.1 for more about this option).
- scope - OPTIONAL. A string of space-separated values representing requested scopes. For the authorization server to consider any requested scope in its assessment, the client MUST have pre-registered the same scope with the authorization server. The client should consult the resource server's API documentation for details about which scopes it can expect the resource server's initial returned permission ticket to represent as part of the authorization assessment (see Section 3.3.4).

###### Response
[](#)


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
 `/host/rsrc/resource/{rsid}`

#### deleteResource

**DELETE** `/host/rsrc/resource/{rsid}`

Deletes a previously registered resource description using the
DELETE method, thereby removing it from the authorization server's
protection regime.

###### URL
    http://sample.com/host/rsrc/resource{rsid}

###### Parameters
- path

    <table border="1">
        <tr>
            <th>Parameter</th>
            <th>Required</th>
            <th>Description</th>
            <th>Data Type</th>
        </tr>
        <tr>
            <th>rsid</th>
            <td>true</td>
            <td>Resource description ID</td>
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
[Resource](#Resource)

JSON body of a successful response will contain the following properties

<table border="1">
        <tr>
            <th>Parameter</th>
            <th>Required</th>
            <th>Description</th>
            <th>Data Type</th>
        </tr>
        <tr>
            <th>_id</th>
            <td>required</td>
            <td>A string value repeating the authorization server-defined 
            identifier for the web resource corresponding to the resource. Its appearance in the body makes it readily available as an object identifier for various resource set management tasks.</td>
            <td>string</td>
        </tr>
        <tr>
            <th>user_access_policy_uri</th>
            <td>optional</td>
            <td>A URI that allows the resource server to redirect an end-user 
            resource owner to a specific user interface within the authorization 
            server where the resource owner can immediately set or modify access policies 
            subsequent to the resource registration action just completed. 
            The authorization server is free to choose the targeted user interface.</td>
            <td>string</td>
        </tr>
</table>

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

`/host/rsrc/resource{rsid}`

Reads a previously registered resource description using the GET
method. If the request is successful, the authorization server MUST
respond with a status message that includes a body containing the
referenced resource description, along with an "_id" property.

###### URL
    http://sample.com/host/rsrc/resource{rsid}

###### Parameters
- path

    <table border="1">
        <tr>
            <th>Parameter</th>
            <th>Required</th>
            <th>Description</th>
            <th>Data Type</th>
        </tr>
        <tr>
            <th>rsid</th>
            <td>true</td>
            <td>Resource description object ID</td>
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
[Resource](#Resource)

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
**PUT** `/host/rsrc/resource{rsid}`

Updates a previously registered resource description using the PUT
method. If the request is successful, the authorization server MUST
respond with a status message that includes an "_id" property.

###### URL
    http://sample.com/host/rsrc/resource/{rsid}

###### Parameters
- body

    <table border="1">
        <tr>
            <th>Parameter</th>
            <th>Required</th>
            <th>Description</th>
            <th>Data Type</th>
        </tr>
        <tr>
            <th>body</th>
            <td>true</td>
            <td>Resource description JSON object</td>
            <td><a href="#Resource">Resource</a></td>
        </tr>
    </table>
- path

    <table border="1">
        <tr>
            <th>Parameter</th>
            <th>Required</th>
            <th>Description</th>
            <th>Data Type</th>
        </tr>
        <tr>
            <th>rsid</th>
            <td>true</td>
            <td>Resource description ID</td>
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
[](#)

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

**`/host/rsrc/resource`**

**GET** 

`/host/rsrc/resource`

Lists all previously registered resource identifiers for 
this user using the GET method. 
The authorization server MUST return the list in
the form of a JSON array of {rsid} string values.

The resource server uses this method as a first step in checking whether
its understanding of protected resources is in full synchronization with
the authorization server's understanding.

###### URL
    http://sample.com/host/rsrc/resource

###### Parameters
- query

    <table border="1">
        <tr>
            <th>Parameter</th>
            <th>Required</th>
            <th>Description</th>
            <th>Data Type</th>
        </tr><tr>
            <th>Name</th>
            <td>required</td>
            <td>A human-readable string describing some scope (extent) of access. 
            The authorization server MAY use this name in any user interface 
            it presents to the resource owner.</td>
            <td>string</td>
        </tr>
        <tr>
            <th>icon_uri</th>
            <td>optional</td>
            <td>A URI for a graphic icon representing the scope. 
            The authorization server MAY use the referenced icon in 
            any user interface it presents to the resource owner.</td>
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
            <td>required</td>
            <td>access token in the header, 
            response from the authorization server
            , if the request is successful. 
            Along with the properties below</td>
            <td>string</td>
        </tr>
        <tr>
            <th>_id</th>
            <td>required</td>
            <td>Obtained the request is successful, 
            from the authroization server</td>
            <td>string</td>
        </tr>
        <th>Name</th>
            <td>required</td>
            <td>A human-readable string describing some scope (extent) of access. 
            The authorization server MAY use this name in any user interface 
            it presents to the resource owner.</td>
            <td>string</td>
        </tr>
        <tr>
            <th>icon_uri</th>
            <td>optional</td>
            <td>A URI for a graphic icon representing the scope. 
            The authorization server MAY use the referenced icon in 
            any user interface it presents to the resource owner.</td>
            <td>string</td>
        </tr>
        <tr>
            <th>scopes</th>
            <td>required</td>
            <td></td>
            <td>string</td>
        </tr>
    </table>

###### Response
[Resource](#Resource)

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
    http://sample.com/host/rsrc/resource

###### Parameters
- body

    <table border="1">
        <tr>
            <th>Parameter</th>
            <th>Required</th>
            <th>Description</th>
            <th>Data Type</th>
        </tr>
        <tr>
            <th>body</th>
            <td>true</td>
            <td>Resource description</td>
            <td><a href="#Resource">Resource</a></td>
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
            <td>required</td>
            <td></td>
            <td>string</td>
        </tr>
    </table>

###### Response
[](#)

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
**HEAD** `/host/rsrc/resource`

Not allowed

#### URL
    http://sample.com/host/rsrc/resource

#### Parameters
<table border = "1">
    <tr>
        <th>Parameter</th>
        <th>Required</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>error</td>
        <td>required</td>
        <td>A single error code. Values for this 
        property are defined throughout this specification.</td>
    </tr>
    <tr>
        <td>error_description</td>
        <td>optional</td>
        <td>A URI identifying a human-readable web 
        page with information about the error.</td>
     </tr>
    <tr>
        <td>error_uri</td>
        <td>optional</td>
        <td>A single error code. Values for this 
        property are defined throughout this specification.</td>
     </tr> 
</table>

#### Errors
<table border="1">
    <tr>
        <th>Status Code</th>
        <th>Reason</th>
    </tr>
</table>

- - -
### unsupportedOptionsMethod
**OPTIONS** 

`/host/rsrc/resource`

Not allowed

#### URL
    http://sample.com/host/rsrc/resource

#### Parameters
[unsupported methods]

#### Errors
<table border="1">
    <tr>
        <th>Status Code</th>
        <th>Reason</th>
    </tr>
</table>

- - -

## Data Types

### <a name="Resource">Resource</a>

<table border="1">
    <tr>
        <th>Type</th>
        <th>Required</th>
        <th>Access</th>
        <th>Description</th>
        <th>Notes</th>
    </tr>
    <tr>
        <td>string</td>
        <td>required</td>
        <td>name</td>
        <td>A human-readable string describing a set of 
        one or more resources. The authorization server 
        MAY use this name in any user interface it presents 
        to the resource owner.</td>
        <td>-</td>
    </tr>
    <tr>
        <td>string</td>
        <td>optional</td>
        <td>uri</td>
        <td>A URI that provides the network location for the 
        resource being registered. For example, if the 
        resource corresponds to a digital photo, the value 
        of this property could be an HTTP-based URI identifying 
        the location of the photo on the web. The authorization 
        server MAY use this information in various ways to 
        inform clients about a resource's location.</td>
        <td> When a client attempts access to a presumptively 
        protected resource without an access token, the resource 
        server needs to ascertain the authorization server and 
        resource identifier associated with that resource 
        without any context to guide it. In practice, this likely 
        means that the URI reference used 
        by the client needs to be unique per resource.</td>
    </tr>
    <tr>
        <td>string</td>
        <td>optional</td>
        <td>type</td>
        <td>A string uniquely identifying the semantics of the 
        resource. For example, if the resource 
        consists of a single resource that is an identity 
        claim that leverages standardized claim semantics for 
        "verified email address", the value of this property 
        could be an identifying URI for this claim. 
        The authorization server MAY use this information in 
        processing information about the resource or 
        displaying information about it in any user 
        interface it presents to the resource owner.</td>
        <td>-</td>
    </tr>
    <tr>
        <td>Array[string]</td>
        <td>required</td>
        <td>scopes</td>
        <td>An array of strings indicating the available scopes for this resource. 
        Any of the strings MAY be either a plain string or a URI </td>
        <td>-</td>
    </tr>
    <tr>
        <td>string</td>
        <td>optional</td>
        <td>icon_uri</td>
        <td>A URI for a graphic icon representing the resource. The authorization server MAY use the referenced icon in 
        any user interface it presents to the resource owner.</td>
        <td>-</td>
    </tr>
</table>

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
- body

    <table border="1">
        <tr>
            <th>Parameter</th>
            <th>Required</th>
            <th>Description</th>
            <th>Data Type</th>
        </tr>
        <tr>
            <th>body</th>
            <td>true</td>
            <td>The identifier for a resource to which this client is seeking access. The identifier MUST correspond to a resource that was previously registered.</td>
            <td><a href="#UmaPermission">UmaPermission</a></td>
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
        <tr>
            <th>Host</th>
            <td>false</td>
            <td></td>
            <td>string</td>
        </tr>
    </table>

###### Response
[](#)

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

- - -

## Data Types

### <a name="UmaPermission">UmaPermission</a>

<table border="1">
    <tr>
        <th>type</th>
        <th>required</th>
        <th>access</th>
        <th>description</th>
        <th>notes</th>
    </tr>
    <tr>
        <td>Date</td>
        <td>optional</td>
        <td>issuedAt</td>
        <td>Issued date of the permission request</td>
        <td>-</td>
    </tr>
    <tr>
        <td>Array[string]</td>
        <td>required</td>
        <td>scopes</td>
        <td>-</td>
        <td>-</td>
    </tr>
    <tr>
        <td>Date</td>
        <td>optional</td>
        <td>expiresAt</td>
        <td>Expiry of the permission request</td>
        <td>-</td>
    </tr>
    <tr>
        <td>string</td>
        <td>required</td>
        <td>resourceId</td>
        <td>-</td>
        <td>-</td>
    </tr>
    <tr>
        <td>Date</td>
        <td>optional</td>
        <td>nbf</td>
        <td>not before</td>
        <td>-</td>
    </tr>
</table>

## UMA rpt Status API 

** /rpt/status **

### Overview

### PATH 
`/rpt/status`

#### requestRptStatusGet

**GET** 
`/rpt/status`

Not allowed

###### URL
    http://sample.com/rpt/status

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
            <th>token</th>
            <td>required</td>
            <td></td>
            <td>string</td>
        </tr>
        <tr>
            <th>token_type_hint</th>
            <td>required</td>
            <td></td>
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
[](#)

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

- - -
##### requestRptStatus
**POST** `/rpt/status`

The resource server MUST determine a received RPT's status, including
both whether it is active and, if so, its associated authorization data,
before giving or refusing access to the client. An RPT is associated
with a set of authorization data that governs whether the client is
authorized for access. 

The token's nature and format are dictated by its profile. The profile
might allow it to be self-contained, such that the resource server is
able to determine its status locally, or might require or allow the
resource server to make a run-time introspection request of the
authorization server that issued the token.

The endpoint MAY allow other parameters to provide further context to
the query. For instance, an authorization service may need to know the
IP address of the client accessing the protected resource in order to
determine the appropriateness of the token being presented.

To prevent unauthorized token scanning attacks, the endpoint MUST also
require some form of authorization to access this endpoint, such as
client authentication as described in OAuth 2.0 [RFC6749] or a separate
OAuth 2.0 access token such as the bearer token described in OAuth 2.0
Bearer Token Usage [RFC6750]. The methods of managing and validating
these authentication credentials are out of scope of this specification.

###### URL
    http://sample.com/rpt/status

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
            <th>token</th>
            <td>true</td>
            <td>The string value of the token. For access tokens, this
is the "access_token" value returned from the token endpoint as defined
in OAuth 2.0 [RFC6749] section 5.1. For refresh tokens, this is the
"refresh_token" value returned from the token endpoint as defined in
OAuth 2.0 [RFC6749] section 5.1. Other token types are outside the scope
of this specification.</td>
            <td>string</td>
        </tr>
        <tr>
            <th>token_type_hint</th>
            <td>false</td>
            <td>A hint about the type of the token submitted for
introspection. The protected resource MAY pass this parameter in order
to help the authorization server to optimize the token lookup. If the
server is unable to locate the token using the given hint, it MUST
extend its search across all of its supported token types. An
authorization server MAY ignore this parameter, particularly if it is
able to detect the token type automatically. Values for this field are
defined in OAuth Token Revocation [RFC7009].</td>
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
[](#)

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

