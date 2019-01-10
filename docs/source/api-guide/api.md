# APIs

## Token Introspection
This API defines a method for a protected resource to query an OAuth 2.0 authorization server to determine the active state of an OAuth 2.0 token and to determine meta-information about this token.

Configuration properties: 

* `introspectionAccessTokenMustHaveUmaProtectionScope` - oxauth configuration which defines whether `access_token` used in Authorization header must have `uma_protection` scope or not. If set to true and `access_token` in Authorization header does not have `uma_protection` scope then request is rejected with 403 forbidden HTTP code with appropriate log message in oxauth.log file. 

### Path
`/restv1/introspection`

### introspect

**GET** or **POST**

`/restv1/introspection`

Client introspects OAuth 2 token.

###### URL
    http://sample.com/restv1/introspection

###### Parameters

- token - REQUIRED.  The string value of the token.  For access tokens, this is the "access_token" value returned from the token endpoint.

###### Response

Sample request/response

```
POST /introspect HTTP/1.1
Host: sample.com
Accept: application/json
Content-Type: application/x-www-form-urlencoded
Authorization: Bearer 23410913-abewfq.123483

token=2YotnFZFEjr1zCsicMWpAA

HTTP/1.1 200 OK
Content-Type: application/json

{
   "active": true,
   "client_id": "l238j323ds-23ij4",
   "username": "jdoe",
   "scope": "read write dolphin",
   "sub": "Z5O3upPC88QrAjx00dis",
   "aud": "https://protected.example.net/resource",
   "iss": "https://server.example.com/",
   "exp": 1419356238,
   "iat": 1419350238,
   "extension_field": "twenty-seven"
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
            <td>Unauthorized if access_token in Authorization header is not valid
        </tr>
        <tr>
            <td>400</td>
            <td>Bad request if request is malformed.</td>
        </tr>
</table>

## ID Generation API 
This section will discuss a few APIs used in the Gluu Server for ID generation.

### Path
`/restv1/id`

#### Overview

The API convention is set as _id_ followed by _prefix_ and _type_ or `/id/{prefix}/{type}/`.
Please see the following table to specify what type you are generating. The `prefix` is used in the 
inum to make it possible to know the type of object just by looking at the identifier.

| `prefix` | `type`               | `description`                          |
| -------- | -------------------- | -------------------------------------- |
| 0000     | people               | Person object                          |
| 0001     | organization         | Organization object                    |
| 0002     | appliance            | Appliance object                       |
| 0003     | group                | Group object                           |
| 0004     | server               | Server object                          |
| 0005     | attribute            | User attribute (claim) object          |
| 0006     | tRelationship        | SAML Trust Relationship object         |
| 0008     | client               | OAuth2 Client object                   |
| 0009     | scope                | OAuth2 Scope Object                    |
| 0010     | uma-resource-set     | UMA Resource Set Object                |
| 0011     | interception-script  | Gluu Server interception script object |
| 0012     | sector-identifier    | Managed Sector Identifier URI          |

**generateJsonInum**<br/>
**GET**`/id/{prefix}/{type}/`

Generates ID for given prefix and type.

**URL**<br/>
    http://gluu.org/id/{prefix}/{type}/

**Parameters**<br/>
- path

|Parameter|Required|Description|Data Type|
|---------|--------|-----------|---------|
|prefix|true|Prefix for id. E.g. if prefix is @!1111 and server will generate id: !0000 then ID returned by service would be: @!1111!0000|string|
|type|true|Type of id|string|

- header

|Parameter|Required|Description|Data Type|
|Authorization|false||string|

**Response**<br/>
[String[Response]](#String[Response])

**generateHtmlInum**  
**GET**`/id/{prefix}/{type}/`

Generates ID for given prefix and type.

**URL**<br/>
    http://gluu.org/id/{prefix}/{type}/
**Parameters**<br/>
- path

|Parameter|Required|Description|Data Type|
|---------|--------|-----------|---------|
|prefix|true|Prefix for id. E.g. if prefix is @!1111 and server will generate id: !0000 then ID returned by service would be: @!1111!0000|string|
|type|true|Type of id|string|
- header

|Parameter|Required|Description|Data Type|
|---------|--------|-----------|---------|
|Authorization|false|The authorization sent as a String|string|

**Response**<br/>
[String[Response]](#String[Response])
**Errors**<br/>

**generateTextInum**<br/>
**GET**`/id/{prefix}/{type}/`

Generates ID for given prefix and type.

**URL**<br/>
    http://gluu.org/id/{prefix}/{type}/
**Parameters**<br/>
- path

|Parameter|Required|Description|Data Type|
|---------|--------|-----------|---------|
|prefix|true||string|
|type|true||string|

- header

|Parameter|Required|Description|Data Type|
|---------|--------|-----------|---------|
|Authorization|false||string|

**Response**<br/>
[String[Response]](#String[Response])


**Errors**<br/>
**generateXmlInum**<br/>
**GET**`/id/{prefix}/{type}/`

Generates ID for given prefix and type.

**URL**<br/>
    http://gluu.org/id/{prefix}/{type}/
**Parameters**<br/>
- path

|Parameter|Required|Description|Data Type|
|---------|--------|-----------|---------|
|prefix|true|Prefix for id. E.g. if prefix is @!1111 and server will generate id: !0000 then ID returned by service would be: @!1111!0000|string|
|type|true|Type of id|string|
- header

|Parameter|Required|Description|Data Type|
|---------|--------|-----------|---------|
|Authorization|false||string|

**Response**<br/>
[String[Response]](#String[Response])


**Errors**<br/>
<table border="1">
    <tr>
        <th>Status Code|<th>Reason|
    </tr>
</table>
- - -

**generateHtmlInum**<br/>
**GET**`/id/{prefix}/{type}/`

Generates ID for given prefix and type.

**URL**<br/>
    http://gluu.org/id/{prefix}/{type}/
**Parameters**<br/>
- path

|Parameter|Required|Description|Data Type|
|---------|--------|-----------|---------|
|prefix|true|Prefix for id. E.g. if prefix is @!1111 and server will generate id: !0000 then ID returned by service would be: @!1111!0000|string|
|type|true|Type of id|string|
- header

|Parameter|Required|Description|Data Type|
|---------|--------|-----------|---------|
|Authorization|false||string|

**Response**<br/>
[String[Response]](#String[Response])


**Errors**<br/>
<table border="1">
    <tr>
        <th>Status Code|<th>Reason|
    </tr>
</table>
- - -
