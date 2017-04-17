# API for oxAuth Clientinfo 
This document provides interface for Client Info REST web services.
## Path
`/oxauth/clientinfo`
## Overview
The ClientInfo Endpoint is an OAuth 2.0 Protected Resource that returns Claims about the registered client.

### clientinfoGet
|Parameter|Description|Data Type|
|---------|-----------|---------|
|access_token |The access token for oxAuth|string|
|authorization| The authorization for the client|string|
|securityContext| Injectable interface providing access to security info|context|

### clientinfoPost
|Parameter|Description|Data Type|
|---------|-----------|---------|
|access_token |The access token for oxAuth|string|
|authorization| The authorization for the client|string|
|securityContext| Injectable interface providing access to security info|context|

