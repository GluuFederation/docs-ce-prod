# ox LDAP Properties

## Overview

The `ox-LDAP.properties` file contains information required for Gluu to connect with its local LDAP Server for user authentication and authorization, and also provides the connection strings to various component's of Gluu to fetch required information for components installed and configured during server setup. For setup/configuration details, please refer to [Setup Script Options](../installation-guide/setup_py.md). The `ox-ldap.properties` file is stored under `/etc/gluu/conf/`

### Properties

Below are the properties included in `ox-ldap.properties` for Gluu to connect with LDAP. 

|Property|Description|
|--------|-----------|
|Bind DN| Stores the DN of the connecting LDAP server|
|Bind Password| Stores the password of the DN, which is provided during setup|
|servers|LDAP server with port number|
|useSSL|Provides a boolean value, depending on the SSL used, and is set to true or false|
|maxconnections|number of maximum connections to be used, this is can be left to be set it to default|
|certsDir|Path of the certificates stored|
|confDir|Path of the configuration directory|
|binaryAttributes|This property should be left to be default ObjectGUID|

Below screenshot is an example of `ox-ldap.properties`

![example](../img/reference/oxldapexample.png)
