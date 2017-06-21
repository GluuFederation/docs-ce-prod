# User Management with SCIM

This section outlines how to do user management with the System for Cross-domain Identity Management - SCIM.

## Requirements

Please visit [SCIM protected by UMA](scim-uma.md) and grab the following in accordance with your environment:

* URL of UMA metadata endpoint
* Requesting party (RP) client ID
* RP JKS file and its password

Also ensure you have activated SCIM and UMA as described [here](scim-uma.md). 

If you pretend to use Java for coding, take into account the following considerations: 

* In your development machine, add the SSL certificate of your Gluu server to the JRE's `cacerts` certificate key store. There are lots of articles around the Web on how to import a certificate to the keystore.

* If you are using Maven, here is how to add the SCIM-Client to your project:
```
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

As a good practice, the SCIM-Client version should match your Gluu CE version. For example, 
if you are running CE v3.0.2, you must also use SCIM-Client v3.0.2.

## Add User
There are two methods to add users:

1. [JSON String](#json-string)
2. [User Object](#user-object)

#### Required Parameters
|Parameter|Description|
|---------|-----------|
|userName | The intended username for the end-user|
|givenName| The first name of the end-user|
|familyName| The last name of the end-user|
|displayName| The formatted first name followed by last name|
|_groups_| Optional parameter if the user is added to any specific group|

#### JSON String
A user can be added by supplying a JSON string representation with appropriate attributes. The following is an example of such a JSON written to a `properties` file:

```
json_string = {	\
  "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],	\
  "externalId": "12345",	\
  "userName": "newUser",	\
  "name": { "givenName": "json", "familyName": "json", "middleName": "N/A", "honorificPrefix": "", "honorificSuffix": ""},	\
  "displayName": "json json",	\
  "nickName": "json",	\
  "profileUrl": "http://www.gluu.org/",	\
  "emails": [	\
    {"value": "json@gluu.org", "type": "work", "primary": "true"},	\
    {"value": "json2@gluu.org", "type": "home", "primary": "false"}	\
  ],	\
  "addresses": [{"type": "work", "streetAddress": "621 East 6th Street Suite 200", "locality": "Austin", "region": "TX", "postalCode": "78701", "country": "US", "formatted": "621 East 6th Street Suite 200  Austin , TX 78701 US", "primary": "true"}],	\
  "phoneNumbers": [{"value": "646-345-2346", "type": "work"}],	\
  "ims": [{"value": "test_user", "type": "Skype"}],	\
  "userType": "CEO",	\
  "title": "CEO",	\
  "preferredLanguage": "en-us",	\
  "locale": "en_US",	\
  "active": "true",	\
  "password": "secret",	\
  "groups": [{"display": "Gluu Test Group", "value": "@!9B22.5F33.7D8D.B890!0001!880B.F95A!0003!60B7"}],	\
  "roles": [{"value": "Owner"}],	\
  "entitlements": [{"value": "full access"}],	\
  "x509Certificates": [{"value": "cert-12345"}]	\
}
```

Here, backslashes "\\" allow us to span the contents in several lines.

Assuming you named the file as `scim-client.properties`, you could write a snippet like this to create the new user. Just supply suitable values for calling the `umaInstance` method - you can use an empty string for umaAatClientKeyId:

```
Properties p= new Properties();
p.load(new FileInputStream("scim-client.properties"));
String jsonPerson=p.getProperty("json_string");

Scim2Client client = Scim2Client.umaInstance(domain, umaMetaDataUrl, umaAatClientId, umaAatClientJksPath, umaAatClientJksPassword, umaAatClientKeyId);
ScimResponse response = client.createPersonString(jsonPerson, MediaType.APPLICATION_JSON);
```

#### User Object

You may also use an "*objectual*" approach to dealing with users. The following code snippet employs the class `org.gluu.oxtrust.model.scim2.User` of SCIM-Client.

```
User user = new User();

Name name = new Name();
name.setGivenName("Given Name");
name.setFamilyName("Family Name");
user.setName(name);

user.setActive(true);

user.setUserName("newUser_" +  + new Date().getTime());
user.setPassword("secret");
user.setPreferredLanguage("US_en");

List<Email> emails = new ArrayList<Email>();
Email email = new Email();
email.setPrimary(true);
email.setValue("a@b.com");
email.setDisplay("a@b.com");
email.setType(Email.Type.WORK);
email.setReference("");
emails.add(email);
user.setEmails(emails);

List<PhoneNumber> phoneNumbers = new ArrayList<PhoneNumber>();
PhoneNumber phoneNumber = new PhoneNumber();
phoneNumber.setPrimary(true);
phoneNumber.setValue("123-456-7890");
phoneNumber.setDisplay("123-456-7890");
phoneNumber.setType(PhoneNumber.Type.WORK);
phoneNumber.setReference("");
phoneNumbers.add(phoneNumber);
user.setPhoneNumbers(phoneNumbers);

List<Address> addresses = new ArrayList<Address>();
Address address = new Address();
address.setPrimary(true);
address.setValue("test");
address.setDisplay("My Address");
address.setType(Address.Type.WORK);
address.setReference("");
address.setStreetAddress("My Street");
address.setLocality("My Locality");
address.setPostalCode("12345");
address.setRegion("My Region");
address.setCountry("My Country");
address.setFormatted("My Formatted Address");
addresses.add(address);
user.setAddresses(addresses);

ScimResponse response = client.createUser(user, new String[]{});
System.out.println("response HTTP code = " + response.getStatusCode());
System.out.println("response body = " + response.getResponseBodyString());
```

### Delete User

To delete a user only his id (the LDAP `inum` attribute) is needed. You can see the `id` of the just user created by inspecting the JSON response.

```
ScimResponse response = client.deletePerson(id);
assertEquals(response.getStatusCode(), 200, "User could not be deleted, status != 200");
```

#### Required Parameter

|Parameter|Description|
|---------|-----------|
|id	  |The LDAP `inum` of the user to be deleted|

### User Extensions

User Extensions allow you to create Custom Attributes in SCIM 2.0. To do so, follow these steps:

* Add attribute to LDAP schema
* Include the new attribute into an LDAP's objectclass such as gluuPerson or preferably, gluuCustomPerson
* Register and activate your new attribute through oxTrust GUI

Please visit this [page](attribute.md#custom-attributes) for a more detailed explanation. When registering the attribute in the admin GUI, please ensure you have set the `SCIM Attribute` parameter to `true`.

![image](../img/admin-guide/user/scim-attribute.png)

Once you submit this form, your attribute will be part of the User Extension. You can verify this by inspecting the `Schema` endpoint:

`<domain root>/identity/seam/resource/restv1/scim/v2/Schemas/urn:ietf:params:scim:schemas:extension:gluu:2.0:User`

![image](../img/admin-guide/user/scim-custom-first.png)

In the JSON response, your new added attribute will appear.

You can learn more about SCIM Schema and Schema Extensions by reading [RFC 7643](https://tools.ietf.org/html/rfc7643). You can also refer to the following unit tests in SCIM-Client project for code examples in which custom attributes are involved:

* [User Extensions Object Test](https://github.com/GluuFederation/SCIM-Client/blob/version_3.0.1/src/test/java/gluu/scim2/client/UserExtensionsObjectTest.java)
* [User Extensions JSON Test](https://github.com/GluuFederation/SCIM-Client/blob/version_3.0.1/src/test/java/gluu/scim2/client/UserExtensionsJsonTest.java)