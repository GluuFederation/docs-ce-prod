# SCIM 1.1

## SCIM 1.1 Specifications

You can see the detailed SCIM 1.1 specification documents
[here](http://www.simplecloud.info/specs/draft-scim-api-01.html).

## SCIM 1.1 Endpoints

- [User Endpoint](#user-endpoint)
- [Group Endpoint](#group-endpoint)
- [Bulk Operation Endpoint](#bulk-operation-endpoint)


## User Endpoint

##### /seam/resource/restv1/Users
- - -
##### getUser
**GET** `/host/seam/resource/restv1/scim/v1/Users{rsid}`

Returns a user on the basis of provided id as path parameter. The
resource MUST be already registered with the mentioned id.

###### URL
    http://gluu.org/host/seam/resource/restv1/scim/v1/Users{rsid}

##### Request
###### Parameters
- Following are the details about parameters:
    <table border="1">
        <tr>
            <th>Parameter</th>
            <th>Location</th>
	    <th>Required</th>
            <th>Description</th>
            <th>Data Type</th>
        </tr>
        <tr>
            <th>rsid</th>
	    <td>path</td>
	    <td>TRUE</td>
            <td>Resource set description ID</td>
            <td>string</td>
        </tr>
	<tr>
            <th>Authorization</th>
	    <td>header</td>
	    <td>FALSE</td>
            <td></td>
            <td>string</td>
        </tr>
    </table>


##### Response
**Content Type:**  application/json, application/xml

###### Success
-	<table border="1">
	    <tr>
			<th>Status Code</th>
			<th>Reason</th>
			<th>Description</th>
	    </tr>
	    <tr>
			<th>200</th>
			<th>Successful Operation</th>
			<th>Resource returned successfully</th>
	    </tr>
	</table>

###### Errors
-	<table border="1">
	    <tr>
			<th>Status Code</th>
			<th>Reason</th>
			<th>Description</th>
	    </tr>
		<tr>
		    <th>400</th>
		    <td>BAD REQUEST</td>
		    <td>Request cannot be parsed, is syntactically incorrect, or violates schema.</td>
		</tr>
		<tr>
		    <th>401</th>
		    <td>UNAUTHORIZED</td>
		    <td>Authorization header is invalid or missing.</td>
		</tr>
		<tr>
		    <th>403</th>
		    <td>FORBIDDEN</td>
		    <td>Operation is not permitted based on the supplied
authorization.</td>
		</tr>
		<tr>
		    <th>404</th>
		    <td>NOT FOUND</td>
		    <td>Specified user does not exist.</td>
		</tr>
	</table>

- - -

## Group Endpoint

### /seam/resource/restv1/Groups
- - -
##### getGroup
**GET** `/host/seam/resource/restv1/scim/v1/Groups{rsid}`

Returns a group on the basis of the provided id as a path parameter. The
group MUST be already registered with the mentioned id.

###### URL
    http://gluu.org/host/seam/resource/restv1/scim/v1/Groups{rsid}

##### Request
###### Parameters
- Following are the details about parameters:
    <table border="1">
        <tr>
            <th>Parameter</th>
            <th>Location</th>
	    <th>Required</th>
            <th>Description</th>
            <th>Data Type</th>
        </tr>
        <tr>
            <th>rsid</th>
	    <td>path</td>
	    <td>TRUE</td>
            <td>Resource set description ID.</td>
            <td>string</td>
        </tr>
	<tr>
            <th>Authorization</th>
	    <td>header</td>
	    <td>FALSE</td>
            <td></td>
            <td>string</td>
        </tr>
    </table>

##### Response
**Content Type:**  application/json, application/xml

###### Success
-	<table border="1">
	    <tr>
			<th>Status Code</th>
			<th>Reason</th>
			<th>Description</th>
	    </tr>
	    <tr>
			<th>200</th>
			<th>Successful Operation</th>
			<th>Group returned successfully.</th>
	    </tr>
	</table>

###### Errors
-	<table border="1">
	    <tr>
			<th>Status Code</th>
			<th>Reason</th>
			<th>Description</th>
	    </tr>
		<tr>
		    <th>400</th>
		    <td>Bad Request</td>
		    <td>Request cannot be parsed, is syntactically incorrect, or violates schema.</td>
		</tr>
		<tr>
		    <th>401</th>
		    <td>Unauthorized</td>
		    <td>Authorization header is invalid or missing.</td>
		</tr>
		<tr>
		    <th>403</th>
		    <td>Forbidden</td>
		    <td>Operation is not permitted based on the supplied authorization.</td>
		</tr>
		<tr>
		    <th>404</th>
		    <td>Not Found</td>
		    <td>Specified user does not exist.</td>
		</tr>
	</table>

- - -


## Bulk Operation Endpoint

### /seam/resource/restv1/scim/v1/Bulk
- - -

<a id="bulkOperation">Bulk Operation</a>

SCIM Bulk Operation enables consumers to work with a potentially large
collection (bulk) of Resource operations in a single request. A body of
a bulk operation may contain a set of HTTP Resource operations using one
of the API supported HTTP methods; i.e., POST, PUT, PATCH or DELETE.
(see http://www.simplecloud.info/specs/draft-scim-api-01.html#bulk-resources
for more details.)

#### Security

* Authorization

#### Request


**Content-Type:** application/json, application/xml

##### Parameters

<table border="1">
    <tr>
        <th>Name</th>
        <th>Located in</th>
        <th>Required</th>
        <th>Description</th>
        <th>Default</th>
        <th>Schema</th>
    </tr>
    <tr>
        <th>Authorization</th>
        <td>header</td>
        <td>no</td>
        <td></td>
        <td> - </td>
        <td>string </td>
    </tr>
    <tr>
        <th>body</th>
        <td>body</td>
        <td>no</td>
        <td>BulkRequest</td>
        <td> - </td>
        <td><a href="#/definitions/BulkRequest">BulkRequest</a></td>
    </tr>
</table>

#### Response

**Content-Type: ** application/json, application/xml


| Status Code | Reason      | Response Model |
|-------------|-------------|----------------|
| 200    | successful operation | <a href="#/definitions/BulkResponse">BulkResponse</a>|

- - -

## Definitions

## <a name="/definitions/BulkOperation">BulkOperation</a>

<table border="1">
    <tr>
        <th>name</th>
        <th>type</th>
        <th>required</th>
        <th>description</th>
        <th>example</th>
    </tr>
    
        <tr>
            <td>bulkId</td>
            <td>string</td>
            <td>optional</td>
            <td>-</td>
            <td></td>
        </tr>
    
        <tr>
            <td>version</td>
            <td>string</td>
            <td>optional</td>
            <td>-</td>
            <td></td>
        </tr>
    
        <tr>
            <td>method</td>
            <td>string</td>
            <td>optional</td>
            <td>-</td>
            <td></td>
        </tr>
    
        <tr>
            <td>path</td>
            <td>string</td>
            <td>optional</td>
            <td>-</td>
            <td></td>
        </tr>
    
        <tr>
            <td>location</td>
            <td>string</td>
            <td>optional</td>
            <td>-</td>
            <td></td>
        </tr>
    
        <tr>
            <td>data</td>
            <td>object</td>
            <td>optional</td>
            <td>-</td>
            <td></td>
        </tr>
    
        <tr>
            <td>status</td>
            <td>string</td>
            <td>optional</td>
            <td>-</td>
            <td></td>
        </tr>
    
        <tr>
            <td>response</td>
            <td>object</td>
            <td>optional</td>
            <td>-</td>
            <td></td>
        </tr>
</table>

## <a name="/definitions/BulkRequest">BulkRequest</a>

<table border="1">
    <tr>
        <th>name</th>
        <th>type</th>
        <th>required</th>
        <th>description</th>
        <th>example</th>
    </tr>
    
        <tr>
            <td>schemes</td>
            <td>array[string]</td>
            <td>optional</td>
            <td>-</td>
            <td></td>
        </tr>
    
        <tr>
            <td>failOnErrors</td>
            <td>integer (int32)</td>
            <td>optional</td>
            <td>-</td>
            <td></td>
        </tr>
    
        <tr>
            <td>operations</td>
            <td>array[<a href="#/definitions/BulkOperation">BulkOperation</a>]</td>
            <td>optional</td>
            <td>-</td>
            <td></td>
        </tr>
</table>

## <a name="/definitions/BulkResponse">BulkResponse</a>

<table border="1">
    <tr>
        <th>name</th>
        <th>type</th>
        <th>required</th>
        <th>description</th>
        <th>example</th>
    </tr>
    
        <tr>
            <td>schemes</td>
            <td>array[string]</td>
            <td>optional</td>
            <td>-</td>
            <td></td>
        </tr>
    
        <tr>
            <td>operations</td>
            <td>array[<a href="#/definitions/BulkOperation">BulkOperation</a>]</td>
            <td>optional</td>
            <td>-</td>
            <td></td>
        </tr>
</table>

