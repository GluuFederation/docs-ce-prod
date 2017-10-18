# User Management with SCIM
The System for Cross-domain Identity Management (SCIM) 
simplifies user provisioning and user management in the cloud by defining two standards:

1) A canonical user schema;

2) A RESTful API for all necessary user management operations.

SCIM is a specification designed to reduce the complexity of user management operations by providing a common user schema and the patterns for exchanging this schema using HTTP in a platform-neutral fashion. The aim of SCIM is achieving interoperability, security, and scalability in the context of identity management.

You can think of **SCIM** merely as a **REST API** with endpoints exposing **CRUD** functionality (create, update, retrieve and delete).

For your reference, current version of the specification - 2.0 - is governed by the following documents: [RFC 7642](https://tools.ietf.org/html/rfc7642), [RFC 7643](https://tools.ietf.org/html/rfc7643), and [RFC 7644](https://tools.ietf.org/html/rfc7644).

## First steps: protect your API

The SCIM protocol does not define a specific method for authentication or authorization so that you can protect your API. In this regard there are a few guidelines in section 2 of [RFC 7644](https://tools.ietf.org/html/rfc7644). 

Gluu Server CE allows you to protect your endpoints with [UMA](../admin-guide/scim-uma.md). This is a safe and standardized approach for protecting web resources. For SCIM, we **strongly recommend** its usage. Please visit this [page](../admin-guide/scim-uma.md) to learn more on how to protect your API appropriately.

Alternatively, for testing purposes you can temporarily enable the test mode that uses a "Bearer token" approach. All examples given in this page are run under test mode and serve as a quick and easy way to start learning about SCIM.

## What's new in SCIM for version 3.1?

Starting with CE v3.1.0, the "test mode" does not use a long-lived OAuth2 access token to send requests anymore. Instead, it uses a safer short-lived token approach in combination with dynamic registration of an OpenId Connect client. This comes at the cost of having to use a programming language to interact with the service.

If you are interested in how the older approach worked, visit the [3.0.2 page](https://gluu.org/docs/ce/3.0.2/admin-guide/user-scim/#using-test-mode). There you can also find the raw `curl` HTTP requests that in general terms illustrate how low-level requests are structured. 

!!! Warning
    Recall that you cannot use your Gluu's 3.1 SCIM service with an older version of SCIM-Client.

Additionally, the root endpoints' URL has been shortened: now your service is exposed at `https://<your-host>/identity/restv1/scim/v2/`.

## Activating test mode

!!! Warning
    Test mode is a weak security approach to protect your service. This feature could be changed or removed in future releases of Gluu Server.

To enable test mode, do the following:

* Login to the oxTrust GUI

* Go to `Configuration` > `Organization Configuration` and choose "enabled" for the SCIM support property

![enable scim](../img/scim/enable-scim.png)

* Navigate to `Configuration` > `JSON Configuration` > `OxTrust Configuration`, then scroll down and set the `scimTestMode` property to true.

* Click the Save Configuration button at the bottom.

You can verify the current authentication scheme by querying the `ServiceProviderConfig` endpoint:

![image](../img/scim/scim-test-mode-config.png)

To exit test mode, just set `scimTestMode` back to `false` and then click the `Save Configuration` button.
 
## Testing with the SCIM-Client

The following instructions show how to interact with your SCIM service in test mode using [SCIM-Client](https://github.com/GluuFederation/SCIM-Client) - a Java library also developed by Gluu.

### Requisites

* In the following we will use Java as programming language. Entry-level knowledge is enough. Make sure you have Java Standard Edition installed. The use of maven as build tool is recommended
* Ensure you have enabled SCIM and test mode as shown above
* Add the SSL certificate of your Gluu server to the `cacerts` keystore of your local Java installation. There are lots of articles around the Web on how to import a certificate to the keystore. An utility called [Key Store Explorer](http://keystore-explorer.sourceforge.net) makes this task super-easy. You can find your certificate at `/opt/gluu-server-<gluu-version>/etc/certs/httpd.crt`
* Online Java-docs for SCIM-Client are available [here](https://ox.gluu.org/scim-javadocs/apidocs/index.html). You can generate java-docs locally using maven; just run `mvn javadoc:javadoc`


### Start a simple project

Create a project in your favorite IDE, and if using maven add the following snippet to your pom.xml file:

```
<properties>
	<scim.client.version>3.1.1</scim.client.version>
</properties>
...
<repositories>
  <repository>
    <id>gluu</id>
    <name>Gluu repository</name>
    <url>http://ox.gluu.org/maven</url>
  </repository>
</repositories>
...
<dependency>
  <groupId>gluu.scim.client</groupId>
  <artifactId>SCIM-Client</artifactId>
  <version>${scim.client.version}</version>
</dependency>
```

From version 3.1.0 onwards, the SCIM-Client you use should match your Gluu version. For example, if you are running Gluu Server CE v3.1.0, you must also use SCIM-Client v3.1.0.

If you don't want to use Maven, you can download the jar file for SCIM-Client here: [https://ox.gluu.org/maven/gluu/scim/client/SCIM-Client](https://ox.gluu.org/maven/gluu/scim/client/SCIM-Client). This may require you to add other libraries (jar files dependencies) manually.

### Simple retrieval

Create a Java class using the code shown below. Replace with proper values between the angle brackets for private attributes:

```
import gluu.scim2.client.factory.ScimClientFactory;
import org.gluu.oxtrust.model.scim2.*
import org.jboss.resteasy.client.core.BaseClientResponse;
import java.util.List;

public class TestScimClient {

    private String domainURL="https://<host-name>/identity/restv1";
    private String OIDCMetadataUrl="https://<host-name>/.well-known/openid-configuration";

    private void simpleSearch() throws Exception {

        ScimClient client = ScimClientFactory.getTestClient(domainURL, OIDCMetadataUrl);
        String filter = "userName eq \"admin\"";

        BaseClientResponse<ListResponse> response = client.searchUsers(filter, 1, 1, "", "", null);
        List<Resource> results=response.getEntity().getResources();

        System.out.println("Length of results list is: " + results.size());
        User admin=(User) results.get(0);
        System.out.println("First user in the list is: " + admin.getDisplayName());

    }

}
```

The first line of method `simpleSearch` is getting an object that conforms to the `ScimClient` interface. This interface consists of a number of methods that will allow you to do all CRUD (create, retrieve, update, delete) you may need.

Create a main method for class `TestScimClient` and call `simpleSearch` from there. When running you will see the output of retrieving one user (admin) and see his `displayName` on the screen.

The [SCIM protected by UMA page](../admin-guide/scim-uma/) contains examples for [adding](../admin-guide/scim-uma.md#adding-a-user) and [deleting](../admin-guide/scim-uma.md#delete-a-user) users.  
The only actual difference in coding for test mode or UMA-protected service is the way in which you initially get a `ScimClient` object instance. For test mode, just call `ScimClientFactory.getTestClient` as shown in the previous example.

### Under the hood

When running the code, in LDAP you will see one or more new entries under the clients branch (`ou=clients`). Those are new OpenId clients created by the Java client and they are employed to request short-lived tokens to access the service.
In oxTrust, you can see them easily too: navigate to `OpenId Connect` > `Clients` and notice the column `Display Name`; they are named as "SCIM-Client". 

These clients won't clutter your LDAP, they are also short-lived (one day) so they are cleaned up automatically for you.

## Extensions

[RFC 7643](https://tools.ietf.org/html/rfc7643) defines the schema for resource types in SCIM. In other words, defines structures in terms of attributes to represent users and groups as well as attribute types, mutability, cardinality, and so on. 

Despite schema covers to a good extent many attributes one might thing of, at times you will need to add your own attributes for specific needs. This is where user extensions pitch in, they allow you to create custom attributes for SCIM. To do so, you will have to:

* Add an attribute to LDAP schema
* Include the new attribute into an LDAP's objectclass such as gluuPerson or preferably, gluuCustomPerson
* Register and activate your new attribute through oxTrust GUI

Please visit this [page](../admin-guide/attribute.md#custom-attributes) for a more detailed explanation. When registering the attribute in the admin GUI, please ensure you have set the `SCIM Attribute` parameter to `true`.

![image](../img/admin-guide/user/scim-attribute.png)

Once you submit this form, your attribute will be part of the User Extension. You can verify this by inspecting the `Schema` endpoint:

`https://<host-name>/identity/restv1/scim/v2/Schemas/urn:ietf:params:scim:schemas:extension:gluu:2.0:User`

![image](../img/admin-guide/user/scim-custom-first.png)

In the JSON response, your new added attribute will appear.

You can learn more about SCIM Schema and the extension model by reading [RFC 7643](https://tools.ietf.org/html/rfc7643). Also refer to the following unit tests in SCIM-Client project for code examples in which custom attributes are involved:

* [User Extensions Object Test](https://github.com/GluuFederation/SCIM-Client/blob/version_3.1.0/src/test/java/gluu/scim2/client/UserExtensionsObjectTest.java)
* [User Extensions JSON Test](https://github.com/GluuFederation/SCIM-Client/blob/version_3.1.0/src/test/java/gluu/scim2/client/UserExtensionsJsonTest.java)