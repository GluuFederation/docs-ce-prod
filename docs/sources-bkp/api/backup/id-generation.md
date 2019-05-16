# ID Generation API Document
This document outlines the API for ID Generation for Gluu Server.
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

##### generateJsonInum
**GET** `/id/{prefix}/{type}/`

Generates ID for given prefix and type.

###### URL
    http://gluu.org/id/{prefix}/{type}/
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
            <th>prefix</th>
            <td>true</td>
            <td>Prefix for id. E.g. if prefix is @!1111 and server will generate id: !0000 then ID returned by service would be: @!1111!0000</td>
            <td>string</td>
        </tr>
        <tr>
            <th>type</th>
            <td>true</td>
            <td>Type of id</td>
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
[String[Response]](#String[Response])


###### Errors
<table border="1">
    <tr>
        <th>Status Code</th>
        <th>Reason</th>
    </tr>
</table>


- - -

##### generateHtmlInum
**GET** `/id/{prefix}/{type}/`

Generates ID for given prefix and type.

###### URL
    http://gluu.org/id/{prefix}/{type}/
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
            <th>prefix</th>
            <td>true</td>
            <td>Prefix for id. E.g. if prefix is @!1111 and server will generate id: !0000 then ID returned by service would be: @!1111!0000</td>
            <td>string</td>
        </tr>
        <tr>
            <th>type</th>
            <td>true</td>
            <td>Type of id</td>
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
            <td>The authorization sent as a String</td>
            <td>string</td>
        </tr>
    </table>

###### Response
[String[Response]](#String[Response])
###### Errors
<table border="1">
    <tr>
        <th>Status Code</th>
        <th>Reason</th>
    </tr>
</table>
- - -
##### generateTextInum
**GET** `/id/{prefix}/{type}/`

Generates ID for given prefix and type.
Generates ID for given prefix and type.

###### URL
    http://gluu.org/id/{prefix}/{type}/
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
            <th>prefix</th>
            <td>true</td>
            <td></td>
            <td>string</td>
        </tr>
        <tr>
            <th>type</th>
            <td>true</td>
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
[String[Response]](#String[Response])


###### Errors
<table border="1">
    <tr>
        <th>Status Code</th>
        <th>Reason</th>
    </tr>
</table>
- - -

##### generateXmlInum
**GET** `/id/{prefix}/{type}/`

Generates ID for given prefix and type.
Generates ID for given prefix and type.

###### URL
    http://gluu.org/id/{prefix}/{type}/
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
            <th>prefix</th>
            <td>true</td>
            <td>Prefix for id. E.g. if prefix is @!1111 and server will generate id: !0000 then ID returned by service would be: @!1111!0000</td>
            <td>string</td>
        </tr>
        <tr>
            <th>type</th>
            <td>true</td>
            <td>Type of id</td>
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
[String[Response]](#String[Response])


###### Errors
<table border="1">
    <tr>
        <th>Status Code</th>
        <th>Reason</th>
    </tr>
</table>
- - -

##### generateHtmlInum
**GET** `/id/{prefix}/{type}/`

Generates ID for given prefix and type.

###### URL
    http://gluu.org/id/{prefix}/{type}/
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
            <th>prefix</th>
            <td>true</td>
            <td>Prefix for id. E.g. if prefix is @!1111 and server will generate id: !0000 then ID returned by service would be: @!1111!0000</td>
            <td>string</td>
        </tr>
        <tr>
            <th>type</th>
            <td>true</td>
            <td>Type of id</td>
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
[String[Response]](#String[Response])


###### Errors
<table border="1">
    <tr>
        <th>Status Code</th>
        <th>Reason</th>
    </tr>
</table>
- - -

