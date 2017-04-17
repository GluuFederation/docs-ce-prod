# Interception Scripts

## Overview
Interception scripts allow the Gluu Server to support unique requirements for many aspects of a central authentication and authorization service. Interception scripts can be written in [Jython](http://www.jython.org/docs/tutorial/indexprogress.html). Jython was chosen because an interpreted language facilitates dynamic creation of business logic, and makes it easier to distribute this logic to a cluster of Gluu servers. Jython enables developers to use either Java or Python classes. Combined with the option of calling web services from Python or Java, this enables the Gluu Server to support any business-driven policy requirement.

The web interface for Custom Scripts can be accessed by navigating to `Configuration` > `Manage Custom Scritps`.

## Interception Script Methods
There are three methods that inherit a base interface

|Inherited Methods|Method description|
|-----------------|------------------|
|`def init(self, configurationAttributes)` |This method is only called once during the script initialization. It can be used for global script initialization, initiate objects etc|
|`def destroy(self, configurationAttributes)` |This method is called once to destroy events. It can be used to free resource and objects created in the `init()` method|
|`def getApiVersion(self)` |The `getApiVersion` method allows API changes in order to do transparent migration from an old script to a new API. Currently all scripts should return `1`|

The `configurationAttributes` parameter is `java.util.Map<String, SimpleCustomProperty>` with properties specified in `oxConfigurationProperty` attributes.

The script manager only loads enabled scripts. Hence, after enabling or disabling a
script, the script manager should trigger an event to either load or
destroy a script, respectively. All scripts are stored in LDAP in the
`ou=scripts,o=<org_inum>,o=gluu` branch.

Here is a sample entry:

```
    dn: inum=@!1111!031C.4A65,ou=scripts,o=@!1111,o=gluu
    objectClass: oxCustomScript
    objectClass: top
    description: <custom_script_description>
    displayName: <display_name>
    gluuStatus: true
    inum: @!1111!031C.4A65
    oxLevel: <priority>
    oxModuleProperty: {"value1":"module_property_name","value2":"module_property_value","description":""}
    oxConfigurationProperty: {"value1":"configuration_property_name","value2":"configuration_property_value","description":""}
    oxRevision: <revision>
    oxScript: <custom_script>
    oxScriptType: <script_type>
    programmingLanguage: python
```

The script manager reloads scripts automatically without needing to
restart the application once `oxRevision` is increased.

## Interception Script Logs
The log files regarding interception scripts are stored in the
`oxauth.log` file. The logs are separated according to the module they
affect. The oxAuth custom script logs are stored in `oxauth_script.log`
and the oxTrust custom script logs are stored in the
`oxtrust_script.log`. Please refer to these log files to troubleshoot errors in
the interception scripts or following the workflow of the script.

!!! Note 
    A `print` statement may not work on some environments if the `PYTHON_HOME` environment variable is not set. Make sure it points to a valid python installation.

More details on Logs can be found in [Log Management](../operation/logs.md)

## Person Authentication     
**For a list of pre-written, open source Gluu authentication scripts, 
view our [server integrations](https://github.com/GluuFederation/oxAuth/tree/master/Server/integrations)**

An authentication script enables you to customize the user
authentication experience. For example, you can write a script that
enables a two-factor authentication mechanism like Duo Security. By
default oxAuth offers basic username/password authentication. Authentication 
scripts allow an admin to implement more secure workflows to meet
an organizations security requirements. It extends the base script type
with the `init`, `destroy` and `getApiVersion` methods but also adds the
following methods:

|Method|`isValidAuthenticationMethod(self, usageType, configurationAttributes)`|
|---|---|
|**Description**|This method is used to check if the authentication method is in a valid state. For example we can check there if a 3rd party mechanism is available to authenticate users. As a result it should either return `True` or `False`|
|Method Parameter|`usageType` is `org.xdi.model.AuthenticationScriptUsageType`<br/>`configurationAttributes` is `java.util.Map<String, SimpleCustomProperty>`|

|Method|`def getAlternativeAuthenticationMethod(self, usageType, configurationAttributes)`|
|---|---|
|**Description**|This method is called only if the current authentication method is in an invalid state. Hence authenticator calls it only if `isValidAuthenticationMethod` returns False. As a result it should return the reserved authentication method name|
|Method Parameter|`uageType` is `org.xdi.model.AuthenticationScriptUsageType`<br/>`configurationAttributes` is `java.util.Map<String, SimpleCustomProperty>`|

|Method|`def authenticate(self, configurationAttributes, requestParameters, step)`|
|---|---|
|**Description**|This method is the key method within the person authentication script. It checks if the user has passed the specified step or not. As a result it should either return `True` or `False`|
|Method Parameter|`requestParameters` is `java.util.Map<String, String[]>`<br/>`step` is java integer<br/>`configurationAttributes` is `java.util.Map<String, SimpleCustomProperty>`|

|Method|`def prepareForStep(self, configurationAttributes, requestParameters, step)`|
|---|---|
|**Description**|This method can be used to prepare variables needed to render the login page and store them in an according event context. As a result it should either return `True` or `False`|
|Method Parameter|`requestParameters` is `java.util.Map<String, String[]>`<br/>`step` is a java integer<br/>`configurationAttributes` is `java.util.Map<String, SimpleCustomProperty>`|

|Method|`def getCountAuthenticationSteps(self, configurationAttributes)`|
|---|---|
|**Description**|This method should return an integer value with the number of steps in the authentication workflow|
|Method Parameter|`configurationAttributes` is `java.util.Map<String, SimpleCustomProperty>`|

|Method|`def getExtraParametersForStep(self, configurationAttributes, step)`|
|---|---|
|**Description**|This method provides a way to notify the authenticator that it should store specified event context parameters event in the oxAuth session. It is needed in a few cases, for example when an authentication script redirects the user to a 3rd party authentication system and expects the workflow to resume after that. As a result it should return a java array of strings|
|Method Parameter|`configurationAttributes` is `java.util.Map<String, SimpleCustomProperty>`<br/>`step` is a java integer|

|Method|`def getPageForStep(self, configurationAttributes, step)`|
|---|---|
|**Description**|This method allows the admin to render a required page for a specified authentication step. It should return a string value with a path to an XHTML page. If the return value is empty or null, the authenticator should render the default log in page `/login.xhtml`|
|Method Parameter|`configurationAttributes` is `java.util.Map<String, SimpleCustomProperty>`<br/>`step` is a java integer|

|Method|`def logout(self, configurationAttributes, requestParameters)`|
|---|---|
|**Description**|This method is not mandatory. It can be used in cases when you need to execute specific logout logic within the authentication script when oxAuth receives an end session request. Also, it allows oxAuth to stop processing the end session request workflow if it returns `False`. As a result it should either return `True` or `False`|
|Method Parameters|`configurationAttributes` is `java.util.Map<String, SimpleCustomProperty>`<br/>`requestParameters` is `java.util.Map<String, String[]>`|

This script can be used in oxAuth application only.

- [Sample Authentication Script](./sample-authentication-script.py)
### Certificate Authentication
Gluu Server CE offers a person authentication module enabling Certificate Authentication.
The image below contains the design diagram for this module.

![image](../img/admin-guide/Cert%20design.jpg)

The script has a few properties:

|	Property	|Description|	Allowed Values			|example|
|-------|--------------|------------|-----------------|
|`chain_cert_file_path`	|mandatory property pointing to certificate chains in [pem][pem] format	|file path| `/etc/certs/chain_cert.pem`	|
|`map_user_cert`		|specifies if the script should map new user to local account		|true/false| true|
|`use_generic_validator`	|enable/disable specific certificate validation				|true/false| false|
|`use_path_validator`	|enable/disable specific certificate validation				|true/false| true|
|`use_oscp_validator`|enable/disable specific certificate validation				|true/false| false|
|`use_crl_validator`|enable/disable specific certificate validation				|true/false| false|
|`crl_max_response_size`	|specifies the maximum allowed size of [CRL][crl] response		| Integer > 0| 2|

- [Sample Certificate Authentication Script](./UserCertExternalAuthenticator.py)        

## Update User     

oxTrust allows an admin to add and modify users which belong to groups.
In order to simplify this process and apply repeating actions, oxTrust
supports an Update User script. In this script it is possible to modify
a person entry before it is stored in LDAP.

This script type adds only one method to the base script type:

|Method|`def updateUser(self, user, persisted, configurationAttributes)`|
|---|---|
|**Description**|This method updates the user|
|Method Parameter|`user` is `org.gluu.oxtrust.model.GluuCustomPerson`<br/>persisted is a boolean value to specify the operation type: add/modify<br/>`configurationAttributes` is `java.util.Map<String, SimpleCustomProperty>`|

This script can be used in an oxTrust application only.

- [Sample Update User Script](./sample-update-user-script.py)

## User Registration      

oxTrust allows users to perform self-registration. In order to
control/validate user registrations there is the user registration
script type.

This script type adds three methods to the base script type:

|Methods|`def initRegistration(self, user, requestParameters, configurationAttributes)`<br/>`def preRegistration(self, user, requestParameters, configurationAttributes)`<br/>`def postRegistration(self, user, requestParameters, configurationAttributes)`|
|---|---|
|**Description**|This method enables/disables user account based on the custom property's value|
|Method Parameters|`user` is `org.gluu.oxtrust.model.GluuCustomPerson`<br/>`requestParameters` is `java.util.Map<String, String[]>`<br/>`configurationAttributes` is `java.util.Map<String, SimpleCustomProperty>`|
|Custom Property|`enable_user`--> defaults to `false`|
|Description|It controls whether or not this user account will be ready for loggin into the Gluu Server CE instance|

The methods are executed in the following order:

|Order|Method|Expected Return|
|-----|------|-----------|
|First|`initRegistration()`|True/False|
|Second|`preRegistration()`|True/False|
|Third|`postRegistration()`|True/False|

First oxTrust executes the `initRegistration` method to do an initial
user entry update. The `preRegistration` method is called before storing
the user entry in LDAP. Hence in this script it is possible to validate
the user entry. The `postRegistration` method is called after
successfully storing the user entry in LDAP. In this method, for
example, the script can send an e-mail or send notifications to other
organization systems about the new user entry.

- [Sample User Registration Script](./sample-user-registration-script.py)

## Client Registration      

oxAuth implements the [OpenID Connect dynamic client
registration](https://openid.net/specs/openid-connect-registration-1_0.html)
specification. All new clients have the same default access scopes and
attributes except password and client ID. The Client Registration script
allows an admin to modify this limitation. In this script it is possible
to get a registration request, analyze it, and apply customizations to
registered clients. For example, a script can give access to specified
scopes if `redirect_uri` belongs to a specified service or domain.

This script type adds only one method to the base script type:

|Method|`def updateClient(self, registerRequest, client, configurationAttributes)`|
|---|---|
|**Method Parameter**|`registerRequest` is `org.xdi.oxauth.client.RegisterRequest`<br/>`client` is `org.xdi.oxauth.model.registration.Client`<br/>`configurationAttributes` is `java.util.Map<String, SimpleCustomProperty>`|

This script can be used in an oxAuth application only.

- [Sample Client Registration Script](./sample-client-registration-script)


## Dynamic Scopes      
The dynamic scope custom script allows the parsing of token returned from `user_info endpoint` into 
LDAP attributes. The `id_token` is returned from `user_info endpoint` and the values are dynamically placed 
in the LDAP attributes in Gluu Server.

- [Sample Dynamic Scope Script](./sample-dynamic-script.py) 

## ID Generator       

By default oxAuth/oxTrust uses an internal method to generate unique
identifiers for new person/client, etc. entries. In most cases the
format of the ID is:

`'!' + idType.getInum() + '!' + four_random_HEX_characters + '.' + four_random_HEX_characters.`

The ID generation script enables an admin to implement custom ID
generation rules.

This script type adds only one method to the base script type:

|Method|`def generateId(self, appId, idType, idPrefix, configurationAttributes)`|
|---|---|
|**Method Parameter**|`appId` is application ID<br/>`idType` is ID Type<br/>`idPrefix` is ID Prefix<br/>`user` is `org.gluu.oxtrust.model.GluuCustomPerson`<br/>`configurationAttributes` is `java.util.Map<String, SimpleCustomProperty>`|

This script can be used in an oxTrust application only.

- [Sample ID Generation Script](./sample-id-generation.py)      

## Cache Refresh       

In order to integrate an interception script with an existing
authentication server oxTrust provides a mechanism called [Cache
Refresh](../admin-guide/user-group/#ldap-synchronization) to copy
user data to the local LDAP server. During this process it is possible
to specify key attribute(s) and specify attribute name transformations.
There are also cases when it can be used to overwrite attribute values
or to add new attributes based on other attribute values.

This script type adds only one method to the base script type:

|Method|`def updateUser(self, user, configurationAttributes)`|
|---|---|
|**Method Parameter**|`user` is `org.gluu.oxtrust.model.GluuCustomPerson`<br/>`configurationAttributes` is `java.util.Map<String, SimpleCustomProperty>`|

This script can be used in an oxTrust application only.

- [Sample Cache Refresh Script](./sample-cache-refresh-script.py)

 
## UMA Authorization Policies     

This is a special script for UMA. It allows an admin to protect UMA
scopes with policies. It is possible to add more than one UMA policy to
an UMA scope. On requesting access to a specified resource, the
application should call specified UMA policies in order to grant or deny
access.

This script type adds only one method to the base script type:

|Method|`def authorize(self, authorizationContext, configurationAttributes)`|
|---|---|
|**Method Parameter**|`authorizationContext` is `org.xdi.oxauth.service.uma.authorization.AuthorizationContext`<br/>`configurationAttributes` is `java.util.Map<String, SimpleCustomProperty>`|

This script can be used in an oxAuth application only.

- [Sample Authorization Script](./sample-uma-authorization-script.py)


## Application Session Management      

This script allows an admin to notify 3rd party systems about requests
to end an OAuth session. This method is triggered by an oxAuth call to
the `end_session` endpoint. It's possible to add multiple scripts with
this type. The application should call all of them according to the
level.

This script type adds only one method to the base script type:

|Method|`def endSession(self, httpRequest, authorizationGrant, configurationAttributes)`|
|---|---|
|**Method Parameter**|`httpRequest` is `javax.servlet.http.HttpServletRequest`<br/>`authorizationGrant` is `org.xdi.oxauth.model.common.AuthorizationGrant`<br/>`configurationAttributes` is `java.util.Map<String, SimpleCustomProperty>`|

This script can be used in an oxAuth application only.

- [Sample Application Session Management Script](./sample-application-session-script.py)

[pem]: https://en.wikipedia.org/wiki/Privacy-enhanced_Electronic_Mail "Privacy-enhanced Electronic Mail"
