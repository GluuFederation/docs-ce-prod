# ID Generation API Document
This API Guide will discuss a few APIs used in the Gluu Server for ID generation.

## Path
`/id`
### Overview

The API convention is set as _id_ followed by _prefix_ and _type_ or `/id/{prefix}/{type}/`.
Please se the following table to specify what type you are generating. The `prefix` is used in the 
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

**generateHtmlInum
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
