## UMA API Document
User-Managed Access (UMA) is a profile of OAuth 2.0. UMA defines how 
resource owners can manipulate to protect the resources.
The client can have access by arbitrary requesting parties, which means the 
requesting resource can be any number of resource servers and a centralized 
authorization server managing the access based on protected resource rules and policies defined.


In order to increase interoperable communication among the 
authorization server, resource server, and client, UMA leverages 
two purpose-built APIs related to the outsourcing of authorization, 
themselves protected by OAuth (or an OAuth-based authentication protocol) in embedded fashion.


The UMA protocol has three broad phases as below

```
                                          +--------------+
                                           |   resource   |
          +---------manage (A)------------ |     owner    |
          |                                +--------------+
          |         Phase 1:                      |
          |         protect a                control (C)
          |         resource                      |
          v                                       v
   +------------+               +----------+--------------+
   |            |               |protection|              |
   |  resource  |               |   API    | authorization|
   |   server   |<-protect (B)--|  (needs  |    server    |
   |            |               |   PAT)   |              |
   +------------+               +----------+--------------+
   | protected  |                          | authorization|
   | resource   |                          |     API      |
   |(needs RPT) |                          |  (needs AAT) |
   +------------+                          +--------------+
          ^                                       |
          |         Phases 2 and 3:         authorize (D)
          |         get authorization,            |
          |         access a resource             v
          |                                +--------------+
          +---------access (E)-------------|    client    |
                                           +--------------+

                                           requesting party
```
The Three Phases of the UMA. 

- Protect a resource

- Get Authorization

- Access a Resource

## UMA Discovery API

** /.well-known/uma-configuration**

#### Overview

### PATH

`/oxauth/uma-configuration`

##### getConfiguration
**GET** `/oxauth/uma-configuration`

Provides configuration data as JSON document. It contains options and
endpoints supported by the authorization server.

###### URL
    http://gluu.org/oxauth/uma-configuration

###### Parameters
<table border="1">
    <tr>
        <th>Access</th>
        <th>Type</th>
        <th>required</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>Scopes</td>
        <td>Array(string)</td>
        <td>required</td>
        <td>-</td>
    </tr>
    <tr>
        <td>Claims</td>
        <td>string</td>
        <td>required</td>
        <td>-</td>
    </tr>
</table>

###### Response
[UmaConfiguration](#UmaConfiguration)

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

- - -

## Data Types

### <a name="UmaConfiguration">UmaConfiguration</a>

<table border="1">
    <tr>
        <th>type</th>
        <th>required</th>
        <th>access</th>
        <th>description</th>
        <th>notes</th>
    </tr>
    <tr>
        <td>string</td>
        <td>required</td>
        <td>version</td>
        <td>The version of the UMA core protocol to which this authorization server conforms. The value MUST be the string "1.0".</td>
        <td>-</td>
    </tr>
    <tr>
        <td>string</td>
        <td>required</td>
        <td>issuer</td>
        <td>A URI indicating the party operating the authorization server.</td>
        <td>-</td>
    </tr>
    <tr>
        <td>Array[string]</td>
        <td>required</td>
        <td>patProfilesSupported</td>
        <td>OAuth access token profiles supported by this authorization server for PAT issuance. The property value is an array of string values, where each string value is either a reserved keyword defined in this specification or a URI identifying an access token profile defined elsewhere. The reserved keyword "bearer" as a value for this property stands for the OAuth bearer token profile [OAuth-bearer]. The authorization server is REQUIRED to support this profile, and to supply this string value explicitly. The authorization server MAY declare its support for additional access token profiles for PATs.</td>
        <td>-</td>
    </tr>
    <tr>
        <td>Array[string]</td>
        <td>required</td>
        <td>aatProfilesSupported</td>
        <td>OAuth access token profiles supported by this authorization server for AAT issuance. The property value is an array of string values, where each string value is either a reserved keyword defined in this specification or a URI identifying an access token profile defined elsewhere. The reserved keyword "bearer" as a value for this property stands for the OAuth bearer token profile [OAuth-bearer]. The authorization server is REQUIRED to support this profile, and to supply this string value explicitly. The authorization server MAY declare its support for additional access token profiles for AATs.</td>
        <td>-</td>
    </tr>
    <tr>
        <td>Array[string]</td>
        <td>required</td>
        <td>rptProfilesSupported</td>
        <td>UMA RPT profiles supported by this authorization server for RPT issuance. The property value is an array of string values, where each string value is either a reserved keyword defined in this specification or a URI identifying an RPT profile defined elsewhere. The reserved keyword "bearer" as a value for this property stands for the UMA bearer RPT profile defined in Section 3.3.2. The authorization server is REQUIRED to support this profile, and to supply this string value explicitly. The authorization server MAY declare its support for additional RPT profiles.</td>
        <td>-</td>
    </tr>
    <tr>
        <td>Array[string]</td>
        <td>required</td>
        <td>patGrantTypesSupported</td>
        <td>OAuth grant types supported by this authorization server in issuing PATs. The property value is an array of string values. Each string value MUST be one of the grant_type values defined in [OAuth2], or alternatively a URI identifying a grant type defined elsewhere.</td>
        <td>-</td>
    </tr>
    <tr>
        <td>Array[string]</td>
        <td>required</td>
        <td>aatGrantTypesSupported</td>
        <td>OAuth grant types supported by this authorization server in issuing AATs. The property value is an array of string values. Each string value MUST be one of the grant_type values defined in [OAuth2], or alternatively a URI identifying a grant type defined elsewhere.</td>
        <td>-</td>
    </tr>
    <tr>
        <td>Array[string]</td>
        <td>optional</td>
        <td>claimTokenProfilesSupported</td>
        <td>Claim formats and associated sub-protocols for gathering claims from requesting parties, as supported by this authorization server. The property value is an array of string values, which each string value is either a reserved keyword defined in this specification or a URI identifying a claim profile defined elsewhere.</td>
        <td>-</td>
    </tr>
    <tr>
        <td>Array[string]</td>
        <td>optional</td>
        <td>umaProfilesSupported</td>
        <td>UMA profiles supported by this authorization server. The property value is an array of string values, where each string value is a URI identifying an UMA profile. Examples of UMA profiles are the API extensibility profiles defined in Section 5.</td>
        <td>-</td>
    </tr>
    <tr>
        <td>string</td>
        <td>required</td>
        <td>dynamicClientEndpoint</td>
        <td>The endpoint to use for performing dynamic client registration. Usage of this endpoint is defined by [DynClientReg]. The presence of this property indicates authorization server support for the dynamic client registration feature and its absence indicates a lack of support.</td>
        <td>-</td>
    </tr>
    <tr>
        <td>string</td>
        <td>required</td>
        <td>tokenEndpoint</td>
        <td>The endpoint URI at which the resource server or client asks the authorization server for a PAT or AAT, respectively. A requested scope of "uma_protection" results in a PAT. A requested scope of "uma_authorization" results in an AAT. Usage of this endpoint is defined by [OAuth2].</td>
        <td>-</td>
    </tr>
    <tr>
        <td>string</td>
        <td>required</td>
        <td>resourceSetRegistrationEndpoint</td>
        <td>The endpoint URI at which the resource server introspects an RPT presented to it by a client. Usage of this endpoint is defined by [OAuth-introspection] and Section 3.3.1. A valid PAT MUST accompany requests to this protected endpoint.</td>
        <td>-</td>
    </tr>
    <tr>
        <td>string</td>
        <td>required</td>
        <td>introspectionEndpoint</td>
        <td>The endpoint URI at which the resource server introspects an RPT presented to it by a client. Usage of this endpoint is defined by [OAuth-introspection] and Section 3.3.1. A valid PAT MUST accompany requests to this protected endpoint.</td>
        <td>-</td>
    </tr>
    <tr>
        <td>string</td>
        <td>required</td>
        <td>permissionRegistrationEndpoint</td>
        <td>The endpoint URI at which the resource server registers a client-requested permission with the authorization server. Usage of this endpoint is defined by Section 3.2. A valid PAT MUST accompany requests to this protected endpoint.</td>
        <td>-</td>
    </tr>
    <tr>
        <td>string</td>
        <td>required</td>
        <td>rptEndpoint</td>
        <td>The endpoint URI at which the client asks the authorization server for an RPT. Usage of this endpoint is defined by Section 3.4.1. A valid AAT MUST accompany requests to this protected endpoint.</td>
        <td>-</td>
    </tr>
    <tr>
        <td>string</td>
        <td>required</td>
        <td>gatEndpoint</td>
        <td>The endpoint URI at which the client asks the authorization server for an GAT. Usage of this endpoint is defined by Gluu documentation.</td>
        <td>-</td>
    </tr>
    <tr>
        <td>string</td>
        <td>required</td>
        <td>authorizationEndpoint</td>
        <td>The endpoint URI at which the client asks to have authorization data associated with its RPT. Usage of this endpoint is defined in Section 3.4.2. A valid AAT MUST accompany requests to this protected endpoint.</td>
        <td>-</td>
    </tr>
    <tr>
        <td>string</td>
        <td>required</td>
        <td>scopeEndpoint</td>
        <td>Scope endpoint</td>
        <td>-</td>
    </tr>
    <tr>
        <td>string</td>
        <td>required</td>
        <td>requestingPartyClaimsEndpoint</td>
        <td>The endpoint URI at which the authorization server interacts with the end-user requesting party to gather claims. If this property is absent, the authorization server does not interact with the end-user requesting party for claims gathering.</td>
        <td>-</td>
    </tr>
    <tr>
        <td>string</td>
        <td>optional</td>
        <td>rptAsJwt</td>
        <td>RPT as JWT</td>
        <td>-</td>
    </tr>
    <tr>
        <td>string</td>
        <td>optional</td>
        <td>rptAsJwt</td>
        <td>RPT as JWT</td>
        <td>-</td>
    </tr>
</table>

## UMA Authorization API

### Overview

### PATH

`/requester/perm`

### requestRptPermissionAuthorization

**POST** 

`/requester/perm`

Client Requests Authorization Data
Once in possession of a permission ticket and an AAT for this
authorization server, the client asks the authorization server to give
it authorization data corresponding to that permission ticket. It
performs a POST on the RPT endpoint, supplying its own AAT in the header
and a JSON object in the body with a "ticket" property containing the
ticket as its value.

If the client had included an RPT in its failed access attempt, It MAY
also provide that RPT in an "rpt" property in its request to the
authorization server.

In circumstances where the client needs to provide requesting party
claims to the authorization server, it MAY also include a "claim_tokens"
property in its request; see Section 3.4.1.2.1 for more information. The
authorization server uses the ticket to look up the details of the
previously registered requested permission, maps the requested
permission to operative resource owner policies based on the resource
set identifier and scopes associated with it, potentially requests
additional information, and ultimately responds positively or negatively
to the request for authorization data.

The authorization server bases the issuing of authorization data on
resource owner policies. These policies thus amount to an asynchronous
OAuth authorization grant. The authorization server is also free to
enable the resource owner to set policies that require the owner to
interact with the server in near-real time to provide consent subsequent
to an access attempt. All such processes are outside the scope of this
specification.

###### URL
    http://gluu.org/requester/perm

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
            <td>false</td>
            <td></td>
            <td><a href="#RptAuthorizationRequest">RptAuthorizationRequest</a></td>
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
            <td>the resource server will receive
             an error of any kind from the authorization server 
             when trying to register a requested permission such that 
             it did not receive a permission ticket, then assuming the 
             resource server chooses to respond to the client</td>
            <td>string</td>
        </tr>
        <tr>
            <th>Host</th>
            <td>false</td>
            <td>The Client Host seeking access</td>
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


- - -

## Data Types

### <a name="ClaimTokenList">ClaimTokenList</a>

<table border="1">
    <tr>
        <th>type</th>
        <th>required</th>
        <th>access</th>
        <th>description</th>
        <th>notes</th>
    </tr>
    <tr>
        <td>string</td>
        <td>required</td>
        <td>format</td>
        <td>A string specifying the format of the accompanying 
        claim tokens. 
        The string MAY be a URI.</td>
        <td>-</td>
    </tr>
    <tr>
        <td>string</td>
        <td>required</td>
        <td>token</td>
        <td>A string containing the claim information in the 
        indicated format, base64url encoded if it is not already so encoded. If claim token format features are included that require special interpretation, the client and authorization server are assumed to have a prior relationship 
        that establishes how to interpret these features.</td>
        <td>-</td>
    </tr>
</table>

### <a name="RptAuthorizationRequest">RptAuthorizationRequest</a>

<table border="1">
    <tr>
        <th>type</th>
        <th>required</th>
        <th>access</th>
        <th>description</th>
        <th>notes</th>
    </tr>
    <tr>
        <td><a href="#ClaimTokenList">ClaimTokenList</a></td>
        <td>required</td>
        <td>claims</td>
        <td>-</td>
     </tr>
    <tr>
        <td>string</td>
        <td>required</td>
        <td>rpt</td>
        <td>Requesting party token</td>
        <td>-</td>
    </tr>
    <tr>
        <td>string</td>
        <td>required</td>
        <td>ticket</td>
        <td>The same permission ticket value that the client 
        provided in the request. It MUST be present 
        if and only if the authorization_state is need_info.</td>
        <td>-</td>
    </tr>
</table>

## UMA Create rpt API 

** /requester/rpt**

## Overview
The endpoint at which the requester asks the 
AM to issue an RPT.

### PATH
 `/requester/rpt`

##### PermissionToken
 
**POST** 

`/requester/rpt`

###### URL
    http://gluu.org/requester/rpt

###### Parameters
- header

    <table border="1">
        <tr>
            <th>Parameter</th>
            <th>Required</th>
            <th>Description</th>
            <th>Data Type</th>
        </tr>
        <tr>
            <th>ticket</th>
            <td>required</td>
            <td>-</td>
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

## UMA Resource Registration API 

**/host/rsrc/resource_set**

### Overview
Resource set is defined by the resource server, which is required
by the authorization server to register the resource set description.

Resource set description is a JSON document with the 
following properties described in [ResourceSet](#ResourceSet)

RESTful API  is used by Resource Server at the authorization server's 
resource set registration endpoint to create, read, update, and delete 
resource set description.



Request to the resource set is registration is incorrect, the authorization
server responds with an with error message by including the below  error 
codes in the response. Discussed detail in [unsupported methods](#unsupportedHeadMethod)

- unsupported_method_type: The resource server request used an unsupported HTTP method. 
  The authorization server MUST respond with the HTTP 405 (Method Not Allowed) status code.
- not_found: The resource set requested from the authorization server cannot be 
  found. The authorization server MUST respond with HTTP 404 (Not Found) status code.

### PATH
 `/host/rsrc/resource_set{rsid}`

#### deleteResourceSet

**DELETE** `/host/rsrc/resource_set{rsid}`

Deletes a previously registered resource set description using the
DELETE method, thereby removing it from the authorization server's
protection regime.

###### URL
    http://gluu.org/host/rsrc/resource_set{rsid}

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
            <td>Resource set description ID</td>
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
[ResourceSet](#ResourceSet)

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
            identifier for the web resource corresponding to the resource set. Its appearance in the body makes it readily available as an object identifier for various resource set management tasks.</td>
            <td>string</td>
        </tr>
        <tr>
            <th>user_access_policy_uri</th>
            <td>optional</td>
            <td>A URI that allows the resource server to redirect an end-user 
            resource owner to a specific user interface within the authorization 
            server where the resource owner can immediately set or modify access policies 
            subsequent to the resource set registration action just completed. 
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
##### getResourceSet

**GET** 

`/host/rsrc/resource_set{rsid}`

Reads a previously registered resource set description using the GET
method. If the request is successful, the authorization server MUST
respond with a status message that includes a body containing the
referenced resource set description, along with an "_id" property.

###### URL
    http://gluu.org/host/rsrc/resource_set{rsid}

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
            <td>Resource set description object ID</td>
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
[ResourceSet](#ResourceSet)

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
##### updateResourceSet
**PUT** `/host/rsrc/resource_set{rsid}`

Updates a previously registered resource set description using the PUT
method. If the request is successful, the authorization server MUST
respond with a status message that includes an "_id" property.

###### URL
    http://gluu.org/host/rsrc/resource_set{rsid}

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
            <td>Resource set description JSON object</td>
            <td><a href="#ResourceSet">ResourceSet</a></td>
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
            <td>Resource set description ID</td>
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
### ResourceSetList

#### Path

**`/host/rsrc/resource_set`**

**GET** 

`/host/rsrc/resource_set`

Lists all previously registered resource set identifiers for 
this user using the GET method. 
The authorization server MUST return the list in
the form of a JSON array of {rsid} string values.

The resource server uses this method as a first step in checking whether
its understanding of protected resources is in full synchronization with
the authorization server's understanding.

###### URL
    http://gluu.org/host/rsrc/resource_set

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
[ResourceSet](#ResourceSet)

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
##### createResourceSet
**POST** `/host/rsrc/resource_set`

Adds a new resource set description using the POST method. If the
request is successful, the authorization server MUST respond with a
status message that includes an _id property.

###### URL
    http://gluu.org/host/rsrc/resource_set

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
            <td>Resource set description</td>
            <td><a href="#ResourceSet">ResourceSet</a></td>
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
**HEAD** `/host/rsrc/resource_set`

Not allowed

#### URL
    http://gluu.org/host/rsrc/resource_set

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

`/host/rsrc/resource_set`

Not allowed

#### URL
    http://gluu.org/host/rsrc/resource_set

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

### <a name="ResourceSet">ResourceSet</a>

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
        resource set being registered. For example, if the 
        resource set corresponds to a digital photo, the value 
        of this property could be an HTTP-based URI identifying 
        the location of the photo on the web. The authorization 
        server MAY use this information in various ways to 
        inform clients about a resource set's location.</td>
        <td> When a client attempts access to a presumptively 
        protected resource without an access token, the resource 
        server needs to ascertain the authorization server and 
        resource set identifier associated with that resource 
        without any context to guide it. In practice, this likely 
        means that the URI reference used 
        by the client needs to be unique per resource set.</td>
    </tr>
    <tr>
        <td>string</td>
        <td>optional</td>
        <td>type</td>
        <td>A string uniquely identifying the semantics of the 
        resource set. For example, if the resource set 
        consists of a single resource that is an identity 
        claim that leverages standardized claim semantics for 
        "verified email address", the value of this property 
        could be an identifying URI for this claim. 
        The authorization server MAY use this information in 
        processing information about the resource set or 
        displaying information about it in any user 
        interface it presents to the resource owner.</td>
        <td>-</td>
    </tr>
    <tr>
        <td>Array[string]</td>
        <td>required</td>
        <td>scopes</td>
        <td>An array of strings indicating the available scopes for this resource set. 
        Any of the strings MAY be either a plain string or a URI </td>
        <td>-</td>
    </tr>
    <tr>
        <td>string</td>
        <td>optional</td>
        <td>icon_uri</td>
        <td>A URI for a graphic icon representing the resource 
        set. The authorization server MAY use the referenced icon in 
        any user interface it presents to the resource owner.</td>
        <td>-</td>
    </tr>
</table>

## UMA Permission Registration API 

** /host/rsrc_pr**

### Overview

###  PATH

`/host/rsrc_pr`

#### registerResourceSetPermission

**POST** 

`/host/rsrc_pr`

Registers permission using the POST method.
The resource server uses the POST method at the endpoint. The body of
the HTTP request message contains a JSON object providing the requested
permission, using a format derived from the scope description format
specified in [OAuth-resource-reg], as follows. The object has the
following properties:

###### URL
    http://gluu.org/host/rsrc_pr

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
            <td>The identifier for a resource set to which this client is seeking access. The identifier MUST correspond to a resource set that was previously registered.</td>
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
        <td>resourceSetId</td>
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
    http://gluu.org/rpt/status

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
    http://gluu.org/rpt/status

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

