#OX LDAP Properties

## Overview

ox-LDAP.properties file contains information required for the Gluu CE Server to connect with LDAP for authenticating and authorizing the user/admin and also provides the connection strings to various component's of Gluu CE or site to fetch required information for the installed and configured components during setup after installation. For setup/configuration detail, please refer to [Setup Script Options](../installation-guide/setup_py.md) ox-ldap.properties file will be stored under `/etc/gluu/conf/`

## Properties in ox-LDAP

Below are the properties that are written in ox-ldap.properties for the 
Gluu CE server to connect with LDAP. 

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

Below screenshot is an example of ox-ldap.properties

![example](../img/reference/oxldapexample.png)
