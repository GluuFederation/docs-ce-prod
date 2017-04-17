# SCIM 2.0 User Add/Delete
This section outlines how to add/remove user from Gluu Server CE using [SCIM-Client](https://github.com/GluuFederation/SCIM-Client).
## Add User
There are two methods to add users:

1. [JSON Sting](#json-string)
2. [User Object](#user-object)

### Required Parameters
|Parameter|Description|
|---------|-----------|
|userName | The intended username for the end-user|
|givenName| The first name of the end-user|
|familyName| The last name of the end-user|
|displayName| The formatted first name followed by last name|
|_groups_| Optional parameter if the user is added to any specific group|

### JSON String
The user is added using a JSON object string using the required parameters; however it is possible to add more parameters. The following is an example of a JSON string used to add a user.

```
        Scim2Client client = Scim2Client.umaInstance(domain, umaMetaDataUrl, umaAatClientId, umaAatClientJksPath, umaAatClientJksPassword, umaAatClientKeyId);
        String createJson = {"schemas":["urn:ietf:params:scim:schemas:core:2.0:User"],"externalId":"12345","userName":"newUser","name":{"givenName":"json","familyName":"json","middleName":"N/A","honorificPrefix":"","honorificSuffix":""},"displayName":"json json","nickName":"json","profileUrl":"http://www.gluu.org/","emails":[{"value":"json@gluu.org","type":"work","primary":"true"},{"value":"json2@gluu.org","type":"home","primary":"false"}],"addresses":[{"type":"work","streetAddress":"621 East 6th Street Suite 200","locality":"Austin","region":"TX","postalCode":"78701","country":"US","formatted":"621 East 6th Street Suite 200  Austin , TX 78701 US","primary":"true"}],"phoneNumbers":[{"value":"646-345-2346","type":"work"}],"ims":[{"value":"nynytest_user","type":"Skype"}],"userType":"CEO","title":"CEO","preferredLanguage":"en-us","locale":"en_US","active":"true","password":"secret","groups":[{"display":"Gluu Test Group","value":"@!9B22.5F33.7D8D.B890!0001!880B.F95A!0003!60B7"}],"roles":[{"value":"Owner"}],"entitlements":[{"value":"full access"}],"x509Certificates":[{"value":"cert-12345"}]}
        ScimResponse response = client.createPersonString(createJson, MediaType.APPLICATION_JSON);
```
### User Object
The following code snippet uses the User object.

```
        User user = new User();

        Name name = new Name();
        name.setGivenName("Given Name");
        name.setMiddleName("Middle Name");
        name.setFamilyName("Family Name");
        user.setName(name);

        user.setActive(true);

        user.setUserName("newUser_" +  + new Date().getTime());
        user.setPassword("secret");
        user.setDisplayName("Display Name");
        user.setNickName("Nickname");
        user.setProfileUrl("");
        user.setLocale("en");
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
        System.out.println("response body = " + response.getResponseBodyString());

        assertEquals(response.getStatusCode(), 201, "Could not add user, status != 201");

        User userCreated = Util.toUser(response, client.getUserExtensionSchema());
        String id = userCreated.getId();
```

## Delete User
To delete a user only the id (the LDAP `inum`) is needed.

```
        ScimResponse response = client.deletePerson(id);
        assertEquals(response.getStatusCode(), 200, "User could not be deleted, status != 200");
```

### Required Parameter

|Parameter|Description|
|---------|-----------|
|id	  |The LDAP `inum` of the user to be deleted|

## User Extensions

SCIM 2.0 User Extensions implementation in Gluu server is very simple. Just set the custom attribute's `SCIM Attribute` parameter to `true` in oxTrust GUI and it will be recognized as a User extension. It is a must to create new custom attributes to be used as User extensions for a cleaner implementation.

![image](../img/2.4/scim-attribute.png)

You can verify the User extensions via the `Schema` endpoint:

`<domain root>/identity/seam/resource/restv1/scim/v2/Schemas/urn:ietf:params:scim:schemas:extension:gluu:2.0:User`

![image](../img/2.4/scim-custom-first.png)

Now for the actual code, you can refer to the unit tests in SCIM-Client:

* [UserExtensionsObjectTest](https://github.com/GluuFederation/SCIM-Client/blob/master/src/test/java/gluu/scim2/client/UserExtensionsObjectTest.java)
* [UserExtensionsJsonTest](https://github.com/GluuFederation/SCIM-Client/blob/master/src/test/java/gluu/scim2/client/UserExtensionsJsonTest.java)
