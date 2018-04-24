## New features and enhancements

SCIM server implementation was updated for version 3.1.3 in order to adhere more closely to SCIM standard and include features we had been missing. The following summarizes the most important enhancements:

### Stricter validations

Validations applied upon input data are more demanding now. We have added and fine-tuned checks to verify that data which is supposed to represent things like countries, languages, locales, timezones, e-mails, URLs, dates, etc. are syntactically valid and follow the standard recommendations.

Also we have added business logic to correctly apply the processing rules when it comes to handling read-only and immutable attributes.

### Improved searching behaviour

We have added searching capabilities so that it's possible to make general searches now, that is, you can have in your search results a mix of different resource types (Users, groups, etc.).

Sorting is not an experimental feature anymore: developers can retrieve results sorted by most of SCIM resource attributes.

The processing of filter expressions used in searches adheres more closely to spec and now it generates more accurate LDAP expressions to run. Not only you can use filters with string attributes but also any mix of boolean, date, and integer typed attributes.

Additionally if errors are found when parsing expressions, the descriptions returned are helpful to spot where the problem is.

### Safer modifications of resources via PATCHes

After studying how resource updates work according to the spec, it's easy to notice that PUT may lead to surprising results. Despite our PUT implementation is "relaxed" in a way that it's difficult to get into problematic scenarios, we have added PATCH support which enables developers to be concise about the changes they want to apply on SCIM resources. Now it's possible to define with precision what will be updated, removed, or added from a resource all in a single operation.

To learn more about PATCH see section 3.5.2 of RFC 7644. For users of SCIM-Client there is a bunch of [test cases](src/test/java/gluu/scim2/client/patch) as well.

### More control on responses content

Now **all operations** (except for bulk and delete) allow developers to specify the attributes that will be returned for every resource (User, group, etc.) included in a response by means of `attributes` and `excludedAttributes` query params. See section 3.9 of RFC 7644.

### More precise error messages

When an anomaly is presented as a result of processing a service request (e.g. a malformed input, attribute mutability conflicts, non-existing resources, etc.), the trace of messages appearing in the log is more expressive so it's easier to be on the errors trail. The error responses returned by the server are accurate about the cause of errors so ideally instead of checking logs, developers just need to inspect the contents of the reponse.

To learn more about how error handling is standardized in SCIM, please read section 3.12 of RFC 7644.

[This section](#how-do-i-add-custom-error-handling) explains how to do error handling for SCIM-Client users.

### New chances for post-processing

Formerly, developers might execute custom code via Python interception scripts just before changes were being saved to LDAP whether for creation, update, or removal of users and groups. Now, in addition to pre-persistence events, there is also room for post-persistence processing. This way developers can trigger execution of custom code that is applicable only after changes are actually saved.

### Server output is compliant
We have striven after standard compliance and fixed subtle mistakes and deviations from the spec that were detected in serialization routines. 

### Better javadocs
Java users can benefit from comprehensive api docs in maven projects such as `scim-client2` and `oxtrust-scim`.


## Important updates for developers

### Behavior changes

In previous implementations we detected a few practices that did not stick appropriately to the standard. Now they are fixed but you may need to adjust your applications or workflows accordingly.

#### No group assignments at /Users endpoint

According to spec (see section 4.1.2 of RFC 7643) the multi-valued attribute "groups" in User resource "... has a mutability of *readOnly*, and group membership changes MUST be applied via the Group Resource". Mistakenly, our previous implementations allowed developers to do group assignments via POST or PUT in the /Users endpoint.

Please adjust your code so that memberships are only manipulated via /Groups . This is done by passing a list for the Group's attribute called "members". It suffices to supply the "value" subattribute for every member: it will contain the "id" of the User you are trying to assign.

The implementation takes care of updating group and user entries in LDAP accordingly and consistently after every modification. You can use PUT to replace (overwrite) all members of a Group at once, or PATCH to add or remove specific users to the existing members list.

#### Adjustments in how attributes are returned

Two aspects have changed with regards to multi-valued attributes:

* The subattribute called *operation* was removed because it is simply not part of the specification. You will not be able to set its value or retrieve it now (even if it was stored in LDAP in the past)
* When a multi-valued attribute is empty, it is not returned in the response. Previously, any operation (create, retrieve, update, etc...) that returned a resource was showing an empty json list `[]` for multi-valued attributes that had no data assigned (e.g. a user with no addresses). Update your code to account for the fact that the attribute will not be there when it has no info.

For single-valued attributes that are not assigned (no data), the same rule applies. The previous implementation returned the attribute with null value in the Json response, like this:

```
{
...
   "language" : null,
...
}
```

In current version, the attribute/value pair is not present.

#### Bulks not returning resource contents

As section 3.7 of RFC 7644 mentions, when a bulk operation is successful the server may elect to omit the response body. We have chosen to do so in contrast to previous implementation that included the complete resource contents back to the client. This allows us to reduce the overhead of Bulk operations.

When the status of an operation is not in the 200-series response, the body of the error is actually included.


### About SCIM-Client

As previously mentioned, current SCIM server implementation is revamped with new features. This is also the case for the Java-based "SCIM-Client" project. The following highlights the most prominent changes and improvements:

* **Client now mirrors more closely the SCIM protocol**: We have adjusted the (client) API used to interact with the service: Java methods that developers must call to send requests to the service are now quite similar to the operations the SCIM standard itself contains. This is a big advantage: developers familiar with the SCIM spec can start working immediately, while those who are not can start learning about SCIM protocol and schema as they are coding.

* **More Jsonized**: Complementary to the previous aspect, we have grown the number of examples (test cases) that use Json payloads. By glancing through a json file (not written in a single-line `.properties` file) developers can get the grasp of what's happenning in test cases more easily, and at the same time are learning about how requests are physically structured. In other words, getting acquainted with the SCIM spec.

* **A simplified and type-safe approach to manipulate custom attributes**. Now it's easier to supply the values of attributes associated to the User extension. To retrieve values, convenience methods are available so there is no need to do casting or call data type constructors manually.

* **Inclusion of a logging framework**:  We have added *Log4j2* support for a more comfortable debugging experience. In previous versions, the `out.println` approach was used.

* **A thorough migration to RestEasy 3**: For version 3.1.0 of SCIM-Client, the project upgraded from RestEasy 2 to RestEasy 3. However, some deprecated APIs and 2.0 techniques still remained in the code. For current version we have introduced changes following the recommended 3.0 practices to stay current. This way the upcoming version of the client (that we aim to support RestEasy 3.1) will also have a smoother migration process. For more information on migration from RestEasy 2 to 3, see chapter 1 of the ["Upgrading from Resteasy 2 to Resteasy 3 guide"](http://docs.jboss.org/resteasy/docs/resteasy-upgrade-guide-en-US.pdf). As a byproduct of this update, developers can now add [custom error handling](#how-do-i-add-custom-error-handling) capabilities to their applications, a feature that had been missing for long.

* **Requires Java SE 8**. 
<!-- This update not only allowed us to stay current but to write test cases in a more concise and straightforward way -->

These **enhancements may come at a cost** for you. We will analyze the implications of this in the following section.

### Is my existing code affected by new features?

If you have been using SCIM-Client in your projects, and want to take advantage of the new features found in server as well as in client implementation we suggest to refactor your code so that it uses the new `scim-client2` maven artifact. With it you can:

* Modify resources via PATCH (a convenient feature that had been missing for long)
* Execute general searches, that is, searches not focused on a single type of resource (e.g. only Users)
* Supply the `excludedAttributes` query param (whether in creation, modification or retrieval operations)
* Inspecting the raw responses coming from the server
* Do custom error handling
* Release resources when no more requests will be issued

If you definitely do not want to alter your existing code base you can still use the old style `scim-client` artifact and work as you used to (a few [special cases apply](#are-there-any-special-cases-to-account-if-still-using-older-client)). 

In summary, version 3.1.3 of the project includes two modules:

* scim-client: Equivalent to 3.1.2 (a few test cases were updated to conform to newer service implementation)
* scim-client2: The newer client. For 3.2 onwards, this will be the only module delivered in this project. This version has more complete java-docs.

Choose one of the following pom fragments for your projects:

```
<!-- new -->
<dependency>
  <groupId>gluu.scim.client</groupId>
  <artifactId>scim-client2</artifactId>
  <version>3.1.3.Final</version>
</dependency>
```

```
<!-- deprecated -->
<dependency>
  <groupId>gluu.scim.client</groupId>
  <artifactId>scim-client</artifactId>
  <version>3.1.3.Final</version>
</dependency>
```

### How to migrate my current code to use the newer SCIM-Client API?

There are four major aspects this shift entails:

#### Changes in method signatures

The Java interface `gluu.scim2.client.ScimClient` does not exist anylonger and has been replaced by `gluu.scim2.client.rest.ClientSideService`. This newer interface is basically the same interface used as contract for the web service implementation. In other words, the *client* and *server* side are using the same contract. Methods in the new interface are quite similar to those in the older, however,

* A few method names have changed to follow a consistent naming convention,
* Most methods are written in two versions: one that receives a Java object and another that expects a (Json) String, 
* Almost all signatures contain additional parameters (for example to support `excludedAttributes` feature), and additionally, 
* Methods do not have any `throw` clauses.

The object you used to obtain when calling `gluu.scim2.client.factory.ScimClientFactory#getClient` or `gluu.scim2.client.factory.ScimClientFactory#getTestClient` belonged to the interface `ScimClient`. Now it can belong to `ClientSideService` or a more restrictive (smaller) interface if you wish (see gluu.scim2.client.BaseTest#setupClient and `gluu.scim2.client.factory.ScimClientFactory` to learn more).

#### Changes for reading responses

As mentioned above, we upgraded to newer RestEasy 3.0 practices for building clients. We replaced the Resteasy client framework in `resteasy-jaxrs` by the JAX-RS 2.0 compliant resteasy-client module. The project now uses the JAX-RS 2.0 Client API in conjuction with the Resteasy Proxy Framework (see [jboss doc page](https://docs.jboss.org/resteasy/docs/3.0.21.Final/userguide/html/RESTEasy_Client_Framework.html)) and we share an interface between client and server. We have already touched upon this point: the client proxy now resembles more closely the service contract (we reuse the same service interface instead of defining a new one as in the older client).

The most important implication regarding RestEasy changes is that `org.jboss.resteasy.client.core.BaseClientResponse<T>` is no longer used and instead `javax.ws.rs.core.Response` comes into play. So you will have no more something like:

```
BaseClientResponse<User> response = client.createUser(...);
```

but will have to use

```
Response response2 = client2.createUser(...);
```

Note that `Response`, unlike the deprecated `ClientResponse<T>` (superclass of `BaseClientResponse<T>`), is not a generic type, so it is necessary to give a type when extracting a response entity. Thus, you should turn the following:

```
user = response.getEntity();
```

into

```
user = response2.readEntity(UserResource.class);
```

`getEntity` method is also part of `Response` but it plays a different role (read the API docs of RestEasy). It is necessary to call `readEntity` to extract the response entity under most circumstances. 

For convenience, SCIM-Client **automatically** buffers the response data for any call made to a service method. In other words, the underlying input stream is totally consumed and closed. This has a nice couple of advantages:

* You don't have to worry about using the `close` method of `Response` - even if there is no usage of `readEntity` in your code. This may happen when you are only interested in the status code of a response.

* You may call `readEntity` any number of times for the same `Response` object - something that will usually lead to exceptions using a standard approach. This way, you can make with no problem something like:
```
logger.info("Raw response received was {}", response2.readEntity(String.class);
user = response2.readEntity(UserResource.class);
```

Note that now we are allowed to "see" the response received from the server - something not achievable with the previous SCIM-Client version.

#### Data model changes

The package `org.gluu.oxtrust.model.scim2` has been refactored to be better structured. As usual this package resides in the `oxtrust-scim` maven module of oxTrust project. It has the main classes to represent the attributes and subattributes of SCIM resources (user, group and fido device), as well as other supporting classes. Despite `oxtrust-scim` lies in the "server side" project, it plays a key role for the client side. 

The new SCIM server implementation brought a few changes:

* A new subpackage `user` was created to hold all POJOs used to represent the attributes and sub-attributes (in SCIM spec jargon) for the user resource
* A new subpackage `group` was created to hold all POJOs related to the group resource
* A new subpackage `bulk` was created to hold classes used to describe bulk operations
* A few class names have changed. The most impacting ones are listed [in the migration guide](#data-model)

#### Handling custom attributes

To specify custom attributes in previous versions, developers used to pass an instance of `Extension` when calling method `addExtension` of `User` object. The usage of `Extension` class has been limited for metadata purposes only and now the way to represent a set of custom attributes is via the `CustomAttributes` class.

The superclass for all SCIM resources, namely `org.gluu.oxtrust.model.scim2.BaseScimResource`, has methods `addCustomAttributes` and `getCustomAttributes` for setting and reading respectively, the custom attributes values. 

With `CustomAttributes` now is possible to specify values of type `Boolean`, `DateTime`, and `Integer` in addition to previously supported `String`, `BigDecimal`, `Date`, and `List`. Retrieving custom attribute values is not restricted to calling a `getValue` method returning a `String` anymore. Now it's possible to provide a return type parameter in order to receive instances of the desired type directly avoiding manual conversion to target types.
The same goes for multi-valued attributes (the type of collection elements is parameterized as well). 

Having `addCustomAttributes` and `getCustomAttributes` not directly tied to the User resource enables the possibility to offer extensions for any kind of resource in future implementations of SCIM service.

### A small migration guide

<!--
If you get to this point, you are a devoted developer happy of getting rid of deprecated stuff such as `ClientRequest`, `ProxyFactory`, and `ClientResponse`. Not to mention the methods in `gluu.scim2.client.ScimClient` and `gluu.scim2.client.rest.ScimService`...

If you are lazy, or don't have time, just **keep using the SCIM-Client 3.1.2** as we mentioned [earlier](#is-my-existing-code-affected-by-new-features).
-->

The following will serve as a guide so you can quickly refactor your existing code. The use of an IDE is highly recommended:

#### Data model

|Class in 3.1.2|In package|New class|In package|
|--------------|----------|---------|----------|
|**User**|org.gluu.oxtrust.model.scim2|**UserResource**|org.gluu.oxtrust.model.scim2.user|
|**Group**|org.gluu.oxtrust.model.scim2|**GroupResource**|org.gluu.oxtrust.model.scim2.group|
|**FidoDevice**|org.gluu.oxtrust.model.scim2.fido|**FidoDeviceResource**|org.gluu.oxtrust.model.scim2.fido|
|**ResourceType**|org.gluu.oxtrust.model.scim2.provider|**ResourceType**|org.gluu.oxtrust.model.scim2.provider|
|**SchemaType**|org.gluu.oxtrust.model.scim2.schema|**SchemaResource**|org.gluu.oxtrust.model.scim2.schema|
|**Resource**|org.gluu.oxtrust.model.scim2|**BaseScimResource**|org.gluu.oxtrust.model.scim2|

**Notes**:

* The user supporting classes `Name`, `Address`, `Email`, `Entitlement`, `PhoneNumber`, `Photo`, `Role`, and `X509Certificate` have been moved to package `org.gluu.oxtrust.model.scim2.user`.

#### Service methods

Recall that `ClientSideService` conglomerates all methods defined in the following interfaces:
 
* gluu.scim2.client.rest.ClientSideUserService
* gluu.scim2.client.rest.ClientSideGroupService
* gluu.scim2.client.rest.ClientSideFidoDeviceService
* org.gluu.oxtrust.ws.rs.scim2.IUserWebService
* org.gluu.oxtrust.ws.rs.scim2.IGroupWebService
* org.gluu.oxtrust.ws.rs.scim2.IFidoDeviceWebService

##### Users manipulation

The following table lists user methods found in the previous client that are not present in the current one but that still have an alternative to achieve the same functionalities.

|Method in ScimClient|Replace with method|Defined at interface|
|--------------------|----------|--------------------|
|createPerson|createUser|IUserWebService|
|createPersonString|createUser|IUserWebService|
|retrievePerson|getUserById|IUserWebService|
|retrieveUser|getUserById|IUserWebService|
|updatePerson|updateUser|IUserWebService|
|updatePersonString|updateUser|IUserWebService|
|deletePerson|deleteUser|IUserWebService|

###### Removed methods

`retrieveAllUsers` is not available in new client. Providing a method that returns all users is discouraged since there is no way to force callers to provide parameters that restrict the amount of data returned apart from the `maxResults` inherent to service behavior (see section 5 of RFC 7643).

If you still need to return a list of all users in LDAP you can:

* Execute a search (use `searchUsersPost` or `searchUsers`)
* Pass an empty (or null) filter
* Pass null for count
* Provide a suitable value for the `attrsList` parameter. This the same well-known `attributes` query param the spec refers to. This way you can reduce the amount of attributes retrieved per user. 

For examples, see the following test cases:
* [QueryParamCreateUpdateTest](https://github.com/GluuFederation/SCIM-Client/blob/version_3.1.3/scim-client2/src/test/java/gluu/scim2/client/singleresource/QueryParamCreateUpdateTest.java)
* [QueryParamRetrievalTest](https://github.com/GluuFederation/SCIM-Client/blob/version_3.1.3/scim-client2/src/test/java/gluu/scim2/client/singleresource/QueryParamRetrievalTest.java)
* [ComplexSearchUserTest](https://github.com/GluuFederation/SCIM-Client/blob/version_3.1.3/scim-client2/src/test/java/gluu/scim2/client/search/ComplexSearchUserTest.java)

###### Extended attributes

Custom attributes manipulation has been simplified: now they are handled via `CustomAttributes` class (check the api docs of `org.gluu.oxtrust.model.scim2.CustomAttributes`). Visit [this page](scim2.md#handling-custom-attributes-in-scim-client) to learn more about this topic. 

##### Groups manipulation

The following table lists group methods found in the previous client that are not present in the current one but that still have an alternative to achieve the same functionalities.

|Method in ScimClient|Replace with method|Defined at interface|
|--------------------|----------|--------------------|
|createGroupString|createGroup|IGroupWebService|
|retrieveGroup|getGroupById|IGroupWebService|
|updateGroupString|updateGroup|IGroupWebService|

###### Removed methods

`retrieveAllGroups` is not available in new client. Use a similar strategy to that of finding all users. Use `searchGroups` or `searchGroupsPost` for the task.

###### New methods

`patchGroup` allows you to apply a PATCH operation upon a group.

##### Fido devices manipulation

The following table lists fido devices methods found in the previous client that are not present in the current one but that still have an alternative to achieve the same functionalities.

|Method in ScimClient|Replace with method|Defined at interface|
|--------------------|----------|--------------------|
|searchFidoDevices|searchDevices|IFidoDeviceWebService|
|searchFidoDevicesPost|searchDevicesPost|IFidoDeviceWebService|
|retrieveFidoDevice|getDeviceById|IFidoDeviceWebService|
|updateFidoDevice|updateDevice|IFidoDeviceWebService|
|deleteFidoDevice|deleteDevice|IFidoDeviceWebService|

##### Metadata 

|Method in ScimClient|Replace with method|Defined at interface|
|--------------------|----------|--------------------|
|retrieveServiceProviderConfig|getServiceProviderConfig|ClientSideService|
|retrieveResourceTypes|getResourceTypes|ClientSideService|

###### Removed methods

* `getUserExtensionSchema` is not available in new client. Use the new `getSchemas` method of `ClientSideService` to obtain this information.

###### New methods

* `getSchemas` allows to issue a GET request to the `/Schemas` endpoint to retrieve all the information of supported schemas in the server implementation.

##### Miscelaneous

* New method `searchResourcesPost` allows to search all resource types at once (by using POST on /.search endpoint).
* New method `close` allows to free resources allocated by the underlying RestEasy client employed to perform the networking operations. Once you call this method, you must not issue any request - you will have to obtain a new client instance from `gluu.scim2.client.factory.ScimClientFactory`

### Are there any special cases to account if still using older client?

Yes. The following are the limitations you should account for:

* When using `searchUsersPost`, `searchGroupsPost`, and `searchFidoDevicesPost` methods, the *attributesArray* param is ignored.

* For BulkOperations, responses cannot be read, more exactly, calling `getOperations` on class `BulkResponse` will always return an empty list. This is due to a problem in deserialization of bulk responses for versions <= 3.1.2.

### How do I add custom error handling?

This [page](scim2.md#error-handling) shows examples on how to process a failed operation received from your service. 
