# IDM Synchronization

## Overview
Gluu exposes a REST service to obtain user entries that have been updated in the local Gluu database after a specified timestamp. The endpoint resides alongside the [SCIM endpoints](../api-guide/scim-api.md/) and reuses the same [protection policy](./scim2.md/#api-protection), however, it is not part of the SCIM standard itself.

## Service specification

There is a [Swagger](https://swagger.io/docs/specification/2-0/) definition document at `https://<host>/identity/scim/resource_changes.yaml` that can be used to bootstrap the process of creating a client application using tools such as [swagger-codegen](https://github.com/swagger-api/swagger-codegen) or [Swagger Hub](https://app.swaggerhub.com). 

The API document is self-explanatory, but here are some key facts:

- The service has a single operation that can be accessed via `GET` at `https://<host>/identity/restv1/scim/UpdatedUsers`

- Three query parameters can be passed: `timeStamp`, `start`, and `pagesize`.

- The operation returns a set of entries matching the search criteria. Each entry consists of a dictionary (key/value pairs), where keys are attribute names (as stored in Gluu database), and every value is an array of actual values for such attribute. In addition to the entries, the size of the result set is returned as well as the timestamp of the most recently updated entry in the set.

!!! Warning
    The computation of results is based on attribute `updatedAt`. If entries are ever modified manually (e.g. by using ldap commands), these updates will not be accounted for by the service.

## Example

The following is a sample request with a corresponding response:

```
GET /identity/restv1/scim/UpdatedUsers?timeStamp=2019-12-24T12:00:03-05:00&start=10&pagesize=100
   Host: example.com
   Authorization: Bearer ACCESS_TOKEN_HERE
```

```
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8

{
   "total": 69,
   "latestUpdateAt": "2019-12-25T18:00:00.123Z",
   "results": [
      ...
      {
         "cn": [ "Jhon Garbanzo" ],
         "displayName": [ "Jhonny" ], 
         "givenName": [ "Jhon" ],
         "gluuSLAManager": [ true ], 
         "gluuStatus": [ "active" ],
         "inum": [ "abcd-1234" ], 
         "mail": [ "jhon@office.com", "jhon@home.com" ], 
         "mobile": [ "+1987654321" ],
         "myIntegerCustomAttribute": [ 123 ],
         "sn": [ "Garbanzo" ],
         "updatedAt": [ "2019-12-25T01:27:29.934Z" ],
         "uid": [ "jhonny" ]
      },
      ...
   ]
}
```

For the above example, all entries returned have a modified timestamp newer than `2019-12-24T17:00:03` (UTC time).
