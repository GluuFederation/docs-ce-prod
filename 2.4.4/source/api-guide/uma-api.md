## UMA API Document

!!! Attention
    The official support end-of-life (EOL) date for Gluu Server 2.4.4 is December 31, 2018. Starting January 1, 2019, no further security updates or bug-fixes will be provided for Gluu Server 2.X. We strongly recommend [upgrading](https://gluu.org/docs/ce/upgrade/) to the newest version.

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
        <td>Array[string]</td>
        <td>optional</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
    </tr>
    <tr>
        <td>string</td>
        <td>optional</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
    </tr>
    <tr>
        <td>Array[string]</td>
        <td>optional</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
    </tr>
    <tr>
        <td>Array[string]</td>
        <td>optional</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
    </tr>
    <tr>
        <td>string</td>
        <td>optional</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
    </tr>
    <tr>
        <td>string</td>
        <td>optional</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
    </tr>
    <tr>
        <td>Array[string]</td>
        <td>optional</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
    </tr>
    <tr>
        <td>string</td>
        <td>optional</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
    </tr>
    <tr>
        <td>string</td>
        <td>optional</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
    </tr>
    <tr>
        <td>string</td>
        <td>optional</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
    </tr>
    <tr>
        <td>string</td>
        <td>required</td>
        <td>-</td>
        <td>An uri indicating the party operating the authorization server.</td>
        <td>An uri indicating the party operating the authorization server.</td>
    </tr>
    <tr>
        <td>string</td>
        <td>optional</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
    </tr>
    <tr>
        <td>string</td>
        <td>optional</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
    </tr>
    <tr>
        <td>Array[string]</td>
        <td>optional</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
    </tr>
    <tr>
        <td>string</td>
        <td>optional</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
    </tr>
    <tr>
        <td>string</td>
        <td>optional</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
    </tr>
    <tr>
        <td>Array[string]</td>
        <td>optional</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
    </tr>
    <tr>
        <td>string</td>
        <td>required</td>
        <td>-</td>
        <td>The version of the UMA core protocol to which this authorization server conforms. The value MUST be the string "1.0".</td>
        <td>The version of the UMA core protocol to which this authorization server conforms. The value MUST be the string "1.0".</td>
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
            <td>403</td>
            <td>Forbidden. Example of a &quot;need_info&quot; response with a full set of &quot;error_details&quot; hints:&#10;&#10;HTTP/1.1 403 Forbidden&#10;Content-Type: application/json&#10;Cache-Control: no-store&#10;...&#10;&#10;{&#10; &quot;error&quot;: &quot;need_info&quot;,&#10; &quot;error_details&quot;: {&#10;   &quot;authentication_context&quot;: {&#10;     &quot;required_acr&quot;: [&quot;https://example.com/acrs/LOA3.14159&quot;]&#10;   },&#10;   &quot;requesting_party_claims&quot;: {&#10;     &quot;required_claims&quot;: [&#10;       {&#10;         &quot;name&quot;: &quot;email23423453ou453&quot;,&#10;         &quot;friendly_name&quot;: &quot;email&quot;,&#10;         &quot;claim_type&quot;: &quot;urn:oid:0.9.2342.19200300.100.1.3&quot;,&#10;         &quot;claim_token_format&quot;: &#10;[&quot;http://openid.net/specs/openid-connect-core-1_0.html#HybridIDToken&quot;],&#10;         &quot;issuer&quot;: [&quot;https://example.com/idp&quot;]&#10;       }&#10;     ],&#10;     &quot;redirect_user&quot;: true,&#10;     &quot;ticket&quot;: &quot;016f84e8-f9b9-11e0-bd6f-0021cc6004de&quot;&#10;   }&#10; }&#10;}&#10;</td>
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
        <td>boolean</td>
        <td>optional</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
    </tr>
    <tr>
        <td>int</td>
        <td>optional</td>
        <td>-</td>
        <td>-</td>
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
        <td>optional</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
    </tr>
    <tr>
        <td>string</td>
        <td>optional</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
    </tr>
    <tr>
        <td>string</td>
        <td>optional</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
    </tr>
</table>

## UMA Create rpt API 

** /requester/rpt**

### Overview


### PATH
 `/requester/rpt`

 ##### getRequesterPermissionToken
**POST** `/requester/rpt`

The endpoint at which the requester asks the AM to issue an RPT.

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
</table>

## UMA Resource Registration API 

**/host/rsrc/resource_set**

### Overview

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
**GET** `/host/rsrc/resource_set{rsid}`

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
#### `/host/rsrc/resource_set`
##### getResourceSetList
**GET** `/host/rsrc/resource_set`

Lists all previously registered resource set identifiers for this user
using the GET method. The authorization server MUST return the list in
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
        </tr>
        <tr>
            <th>scope</th>
            <td>false</td>
            <td>Scope uri</td>
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
##### unsupportedHeadMethod
**HEAD** `/host/rsrc/resource_set`

Not allowed

###### URL
    http://gluu.org/host/rsrc/resource_set

###### Parameters

###### Response
[](#)

###### Errors
<table border="1">
    <tr>
        <th>Status Code</th>
        <th>Reason</th>
    </tr>
</table>

- - -
##### unsupportedOptionsMethod
**OPTIONS** `/host/rsrc/resource_set`

Not allowed

###### URL
    http://gluu.org/host/rsrc/resource_set

###### Parameters

###### Response
[](#)

###### Errors
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
        <th>type</th>
        <th>required</th>
        <th>access</th>
        <th>description</th>
        <th>notes</th>
    </tr>
    <tr>
        <td>string</td>
        <td>optional</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
    </tr>
    <tr>
        <td>string</td>
        <td>optional</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
    </tr>
    <tr>
        <td>string</td>
        <td>optional</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
    </tr>
    <tr>
        <td>Array[string]</td>
        <td>optional</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
    </tr>
    <tr>
        <td>string</td>
        <td>optional</td>
        <td>-</td>
        <td>-</td>
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
            <td><a href="#RegisterPermissionRequest">RegisterPermissionRequest</a></td>
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

### <a name="RegisterPermissionRequest">RegisterPermissionRequest</a>

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
        <td>-</td>
        <td>-</td>
        <td>-</td>
    </tr>
    <tr>
        <td>Array[string]</td>
        <td>optional</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
    </tr>
    <tr>
        <td>Date</td>
        <td>optional</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
    </tr>
    <tr>
        <td>string</td>
        <td>optional</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
    </tr>
    <tr>
        <td>Date</td>
        <td>optional</td>
        <td>-</td>
        <td>-</td>
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
            <td>false</td>
            <td></td>
            <td>string</td>
        </tr>
        <tr>
            <th>token_type_hint</th>
            <td>false</td>
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

