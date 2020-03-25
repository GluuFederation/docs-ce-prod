# Coding custom scripts and pages: a developer's reference

## Objects available

oxAuth is a Weld+JSF application. That means custom scripts and custom pages (JSF facelets) can make use of business logic already encapsulated in the (Weld) managed beans available.

Specifically, custom pages can use EL expressions to get/bind values or call methods of classes annotated with `javax.inject.Named` as long as they are part of the application's WAR file or [external libraries](../operation/custom-design.md#subdirectories) added to the classpath. Thus, practically all `@Named` beans belonging to [oxAuth](https://github.com/GluuFederation/oxAuth) or [oxCore](https://github.com/GluuFederation/oxCore) subprojects are potential candidates.

In addition to that, there are the usual implicit JSP/JSF [objects](http://incepttechnologies.blogspot.com/p/jsf-implicit-objects.html) plus the `i18n` labels map (`msgs`) used for [localization](../operation/custom-design/#subdirectories) purposes.

In the case of custom scripts, any class in oxAuth's classpath can be used as well as the standard Java 8 classes. 

!!! Note
    Relevant javadocs links: [oxAuth](https://ox.gluu.org/javadocs/oxauth/) <!--and [oxCore](?)--> (choose the version matching your Gluu Server version).

While there are hundreds of classes available for reuse, the following summarizes the most commonly used:

### Category: Authentication

#### Class: `AuthenticationService`

|Description|Managed bean|Project|Full name|References|
|-|-|-|-|-|
|Allows to authenticate a user or obtain the current authenticated user|Yes (Stateless)|oxauth-server|`org.gluu.oxauth.service.AuthenticationService`|[code](https://github.com/GluuFederation/oxAuth/blob/version_4.1.0/Server/src/main/java/org/gluu/oxauth/service/AuthenticationService.java)|

Relevant methods:

|Signature|Description|
|-|-|
|`boolean authenticate(String userName)`|Performs authentication for the user whose identifier (`userName`) is passed as parameter|
|`boolean authenticate(String userName, String password)`|Performs authentication for the user whose identifier (`userName`) is passed as parameter. The `password` supplied must be the correct password of the user in question|
|`User getAuthenticatedUser()`|Returns a representation of the currently authenticated user. `null` if no user is currently authenticated. See [User](#class-user) data object|

#### Class: `Authenticator`

|Description|Managed bean|Project|Full name|References|
|-|-|-|-|-|
|This class is mainly used in facelets templates for authentication flows to proceed in the sequence of steps|Yes (RequestScoped)|oxauth-server|`org.gluu.oxauth.auth.Authenticator`|[code](https://github.com/GluuFederation/oxAuth/blob/version_4.1.0/Server/src/main/java/org/gluu/oxauth/auth/Authenticator.java)|

Relevant methods:

|Signature|Description|
|-|-|
|boolean authenticate()|Makes the authentication flow proceed by calling the `authenticate` method of the custom script|
|String prepareAuthenticationForStep()|Makes the authentication flow proceed by calling the `prepareForStep` method of the custom script|

See also: [Person authentication](../admin-guide/custom-script/#person-authentication)

### Category: User Management

#### Class: `UserService`

|Description|Managed bean|Project|Full name|References|
|-|-|-|-|-|
|Allows CRUD of users in the local database|Yes (ApplicationScoped)|oxauth-common|`org.gluu.oxauth.service.UserService`|[code](https://github.com/GluuFederation/oxAuth/blob/version_4.1.0/common/src/main/java/org/gluu/oxauth/service/UserService.java)|

Relevant methods:

|Signature|Description|
|-|-|
|`User addUser(User user, boolean active)`|Creates a new user based on the representation passed as parameter. `active` parameter denotes whether user status (`gluuStatus` attribute) will be `active` or `register`|
|`User addUserAttribute(String userId, String attributeName, String attributeValue)`|Adds an attribute to the user identified by `userId` in the database with the name and value passed. Returns a representation of the modified user or `null` in case of failure or if such name/attribute is already part of such user|
|`boolean addUserAttribute(User user, String attributeName, String attributeValue)`|Adds an attribute to the `user` object with the name and value passed. This method only alters the `user` argument and does not persist changes. Returns `false` if such name/attribute is already part of `user`
|`User addUserAttributeByUserInum(String userInum, String attributeName, String attributeValue)`|Adds an attribute to the user whose `inum`  attribute (in the database) equals to `userInum` using the name and value passed. Returns a representation of the modified user or `null` in case of failure or if such name/attribute is already part of such user|
|`CustomAttribute getCustomAttribute(User user, String attributeName)`|Gets a representation of the attribute whose name is passed for the user in question (`user`). Returns `null` if no such attribute is populated|
|`String getDnForUser(String inum)`|Obtains the DN (distinguished name) of the user whose `inum` attribute equals to `userInum` (no check that such user may exist is actually made)|
|`User getUser(String userId, String... returnAttributes)`|Retrieves a user representation for the user identified with `userId` containing only the attributes requested (`returnAttributes`). `null` is returned if no such user exists|
|`User getUserByAttribute(String attributeName, String attributeValue)`|Retrieves a user (first available) such that the attribute referenced (`attributeName`) has the value passed (`attributeValue`). `null` is returned if no such user exists|
|`String getUserInum(String userId)`|Retrieves the `inum` database attribute for the user identified with `userId`.`null` is returned if no such user exists|
|`User removeUserAttribute(String userId, String attributeName, String attributeValue)`|Removes `attributeValue` from the values of the attribute whose name is passed (`attributeName`) for the user identified with `userId`|
|`User replaceUserAttribute(String userId, String attributeName, String oldAttributeValue, String newAttributeValue)`|Updates the user identified with `userId` by replacing the value of the attribute `attributeName` with the value passed. `null` is returned if no such user exists|
|`void setCustomAttribute(User user, String attributeName, String attributeValue)`|Sets the value of the attribute `attributeName` with the single value `attributeValue` for the user representation passes as parameter. This method does not persist changes|
|`User updateUser(User user)`|Updates the user represented by `user` object in the database|

See also: 
- [User](#class-user) data object
- [CustomAttribute](#class-customattribute) data object

#### Class: `User`

|Description|Managed bean|Project|Full name|References|
|-|-|-|-|-|
|A class employed to represent a user entry in the database. Provides getters and setters to retrieve and assign value(s) for attributes|No|oxauth-common|`org.gluu.oxauth.model.common.User`|[code](https://github.com/GluuFederation/oxAuth/blob/version_4.1.0/common/src/main/java/org/gluu/oxauth/model/common/User.java)|

#### Class: `CustomAttribute`

|Description|Managed bean|Project|Full name|References|
|-|-|-|-|-|
|A class that models an attribute. An attribute has a name and a collection of associated values|No|oxcore-persistence-model|`org.gluu.persist.model.base.CustomAttribute`|[code](https://github.com/GluuFederation/oxCore/blob/version_4.1.0/persistence-model/src/main/java/org/gluu/persist/model/base/CustomAttribute.java)|

### Category: Session Management

#### Class: `Identity`

|Description|Managed bean|Project|Full name|References|
|-|-|-|-|-|
|Mainly used to carry data between steps of authentication flows|Yes (RequestScoped)|oxauth-server|`org.gluu.oxauth.security.Identity`|[code](https://github.com/GluuFederation/oxAuth/blob/version_4.1.0/Server/src/main/java/org/gluu/oxauth/security/Identity.java)|

Relevant methods:

|Signature|Description|
|-|-|
|`Object getWorkingParameter(String name)`|Retrieves a working parameter by name previously set via `setWorkingParameter`|
|`void setWorkingParameter(String name, Object value)`|Binds data to a name for further use in an authentication flow. Recommended values to store are `String`s|
|`SessionId getSessionId()`|Retrieves a reference to the associated server session object, see [SessionId](https://github.com/GluuFederation/oxAuth/blob/version_4.1.0/Server/src/main/java/org/gluu/oxauth/model/common/SessionId.java)|

<!-- SessionIdService --> 

### Category: Networking

#### Class: `HttpService`
|Description|Managed bean|Project|Full name|References|
|-|-|-|-|-|
|Provides utility methods to execute HTTP requests, manipulate responses, etc.|Yes (ApplicationScoped)|oxauth-server|`org.gluu.oxauth.service.net.HttpService`|[code](https://github.com/GluuFederation/oxAuth/blob/version_4.1.0/Server/src/main/java/org/gluu/oxauth/service/net/HttpService.java)|

Relevant methods:

|Signature|Description|
|-|-|
|`HttpClient getHttpsClient()`|Returns an instance of `org.apache.http.client.HttpClient` (see oxcore-util class [SslDefaultHttpClient](https://github.com/GluuFederation/oxCore/blob/version_4.1.0/oxUtil/src/main/java/org/gluu/net/SslDefaultHttpClient.java))|
|`HttpServiceResponse executeGet(HttpClient httpClient, String requestUri)`|Perform a GET on the URI requested. Returns an instance of `org.gluu.oxauth.model.net.HttpServiceResponse` (a wrapper on `org.apache.http.HttpResponse`)|
|`byte[] getResponseContent(HttpResponse httpResponse)`|Consumes the bytes of the associated response. Returns `null` if the response status code is not 200 (OK)|

### Category: Cache

#### Class: `CacheService`

|Description|Managed bean|Project|Full name|References|
|-|-|-|-|-|
|Provides a unified means to interact with the underlying cache provider configured in the Gluu Server|Yes (ApplicationScoped)|oxcore-service|`org.gluu.service.CacheService`|[code](https://github.com/GluuFederation/oxCore/blob/version_4.1.0/oxService/src/main/java/org/gluu/service/CacheService.java)|

Relevant methods:

|Signature|Description|
|-|-|
|`void clear()`|Flushes the whole cache|
|`Object get(String key)`|Retrieves the value of `key` in the cache. `null` if there is no such key present|
|`void put(int expirationInSeconds, String key, Object object)`|Puts an object in the cache associated to the key passed. An expiration in seconds can be provided|
|`put(String key, Object object)`|Puts an object in the cache associated to the key passed. The expiration used is the default expiration configured in Gluu|
|`void remove(String key)`|Removes an entry from the cache|

See also: [Cache Provider](https://gluu.org/docs/ce/reference/cache-provider-prop/)

### Category: JSF

#### Class: `FacesService`

|Description|Managed bean|Project|Full name|References|
|-|-|-|-|-|
|Provides utilities to properly build encoded URLs and make redirections. This class is often used in custom scripts|Yes (RequestScoped)|oxcore-jsf-util|`org.gluu.jsf2.service.FacesService`|[code](https://github.com/GluuFederation/oxCore/blob/version_4.1.0/oxJsfUtil/src/main/java/org/gluu/jsf2/service/FacesService.java)|

Relevant methods:

|Signature|Description|
|-|-|
|`void redirectToExternalURL(String url)`|Redirects the user's browser to the URL passed as parameter|
|`String encodeParameters(String url, Map<String, Object> parameters)`|Builds a URL by appending query parameters as supplied in `parameters` map. Every value in the map is properly URL-encoded|

#### Class: `FacesMessages`

|Description|Managed bean|Project|Full name|References|
|-|-|-|-|-|
|Allows manipulation of JSF context messages|No|oxcore-jsf-util|`org.gluu.jsf2.message.FacesMessages`|[code](https://github.com/GluuFederation/oxCore/blob/version_4.1.0/oxJsfUtil/src/main/java/org/gluu/jsf2/message/FacesMessages.java)|

Relevant methods:

|Signature|Description|
|-|-|
|`void add(Severity severity, String message)`|Adds a message to the JSF context with the severity (`javax.faces.application.FacesMessage.Severity`) specified|
|`void clear()`|Clears the messages of the JSF context|
|`String evalAsString(String expression)`|Evaluates an EL expression using the JSF context and returns the result as a String|
|`void setKeepMessages()`|Sets the "keep messages" property of the JSF flash|

See also: ["Displaying error conditions to end-users"](#example-displaying-error-conditions-to-end-users)

### Category: Miscellaneous Utilities

#### Class: `CdiUtil`

|Description|Managed bean|Project|Full name|References|
|-|-|-|-|-|
|Allows to obtain references of managed beans. This is particularly useful in custom scripts|No|oxcore-service|`org.gluu.service.cdi.util.CdiUtil`|[code](https://github.com/GluuFederation/oxCore/blob/version_4.1.0/oxService/src/main/java/org/gluu/service/cdi/util/CdiUtil.java)|

Relevant methods:

|Signature|Description|
|-|-|
|<T> T bean(Class<T> clazz)|Gets the managed bean belonging to the class passed as parameter|

Example (jython code):

```
from org.gluu.oxauth.service import UserService
from org.gluu.oxauth.service import AuthenticationService
...
userService = CdiUtil.bean(UserService)
authenticationService = CdiUtil.bean(AuthenticationService)
```

#### Class: `StringHelper`

|Description|Managed bean|Project|Full name|References|
|-|-|-|-|-|
|Provides many utility methods that often arise in the manipulation of Strings|No|oxcore-util|`org.gluu.util.StringHelper`|[code](https://github.com/GluuFederation/oxCore/blob/version_4.1.0/oxUtil/src/main/java/org/gluu/util/StringHelper.java)|

Relevant methods:see "References" column.

#### Class: `EncryptionService`

|Description|Managed bean|Project|Full name|References|
|-|-|-|-|-|
|Allows to encrypt/decrypt strings using a 3DES cipher whose salt is found in chroot at `/etc/gluu/conf/salt`|Yes (ApplicationScoped)|oxauth-server|`org.gluu.oxauth.service.EncryptionService`|[code](https://github.com/GluuFederation/oxAuth/blob/version_4.1.0/Server/src/main/java/org/gluu/oxauth/service/EncryptionService.java)|

Relevant methods:

|Signature|Description|
|-|-|
|String decrypt(String encryptedString)|Decrypts the encrypted string supplied|
|Properties decryptAllProperties(Properties connectionProperties)|Returns a `java.util.Properties` object with all decrypted values found in `connectionProperties`|
|`String encrypt(String unencryptedString)`|Encrypts the string supplied|

## Example: Displaying error conditions to end-users

When coding certain flows, it is important to be able to display errors in the xhtml templates based on conditions that occur as the  associated custom script runs. For this purposes, the `FacesMessage` bean can be used. Here is an example that adds an error message in the UI:

``` 
from org.gluu.jsf2.message import FacesMessages
from org.gluu.service.cdi.util import CdiUtil
from javax.faces.application import FacesMessage
...

facesMessages = CdiUtil.bean(FacesMessages) 
facesMessages.setKeepMessages()
facesMessages.add(FacesMessage.SEVERITY_ERROR, "Please enter a valid username")
```

The error will appear in the associated template using the following markup:

```
...
<h:messages />
...
```
