# User Registration with SCIM

## Overview
SCIM service has many use cases. One interesting and often arising is that of coding your 
own user registration process. With your SCIM endpoints you can build a custom application to enter users to your LDAP directory.

## Important Considerations

Here, you have some useful tips before you start:

1. Choose a toolset you feel comfortable to work with. Keep in mind that you have to leverage the capabilities of your language/framework to issue complex **HTTPS** requests. Be sure that:

    - You will be able to use at least the following verbs: GET, POST, PUT, and DELETE

    - You can send headers in your requests as well as reading them from the service response
  
1. If not supported natively, choose a library to facilitate JSON content manipulation. As you have already noticed we have been dealing with Json for requests as well as for responses. Experience shows that being able to map from objects (or data structures) of your language to Json and viceversa helps saving hours of coding

1. Shape your data model early. List the attributes your application will operate upon and correlate with those found in the SCIM user schema. You can learn about the schema in [RFC 7644](https://tools.ietf.org/html/rfc7644). At least, take a look at the JSON-formatted schema that your Gluu Server shows: visit `https://<host-name>/identity/restv1/scim/v2/Schemas/urn:ietf:params:scim:schemas:core:2.0:User`.

1. You will have to check your LDAP contents very often as you develop and run tests. You may have to delete attributes or whole entries as your application evolves. Thus, use a suitable tool for LDAP manipulation: Use oxTrust to manipulate your users' attributes or setup a LDAP GUI client to have more control.

1. Always check your logs. In (test mode)[#working-in-test-mode] section above you can find some guidelines in this regard.

1. In this user management guide with SCIM, we have already touched upon the fundamentals of SCIM in Gluu Server and shown a good amount of sample requests for manipulation of user information. However, keep in mind the SCIM spec documents are definitely the key reference to build working request messages, specially [RFC 7643](https://tools.ietf.org/html/rfc7643), and [RFC 7644](https://tools.ietf.org/html/rfc7644).

## Summary of Tasks

In this section, we will summarize the tasks you need to undertake in order to code your application. We will not go into details of any programming language or technology to build user interfaces. 

For coding an app or script that implements a user registration process, you should:

- Code authorization routines

- Code a dummy insertion routine

- Create a form to grab new users' data

- Code routines to process the HTTP POST

- Create a feedback page

- Do adjustments in the attribute set

- Enhance your form

## Get Started
### Code Authorization Routines

This task has to do with creating utility code that will allow you to obtain tokens (whether an "access token" for test mode or a "requesting party token" - rpt - when using UMA). This code requires sending HTTPS requests to a few URLs.

In previous sections, we covered thoroughly what needs to be done for test mode for UMA basic [guidelines](#using-a-different-programming-language) were given. Ensure you have already enabled the protection for your preference in oxTrust.

If you are unsure of how to code a particular step, take a look at the Java client. These two classes do the job:

- [TestModeScimClient](https://github.com/GluuFederation/SCIM-Client/blob/version_3.1.5/scim-client2/src/main/java/gluu/scim2/client/TestModeScimClient.java)

- [UmaScimClient](https://github.com/GluuFederation/SCIM-Client/blob/version_3.1.5/scim-client2/src/main/java/gluu/scim2/client/UmaScimClient.java)

To test your authorization code, use a simple GET retrieval request.

### Code a Dummy Insertion Routine

Use the information given in the section [Creating resources](#creating-resources) to make a hardcoded POST to the user endpoint.

In summary, make sure the following works for you:

```
POST /identity/restv1/scim/v2/Users
Host: host-name...
Accept: application/scim+json
Content-Type: application/scim+json
Authorization: Bearer ...

{
	"schemas":["urn:ietf:params:scim:schemas:core:2.0:User"],
	"userName":"ajsmith",
	"name":{
		"familyName":"Smith",
		"givenName":"Joe"
	},
	"displayName":"Average Joe"
}
``` 

### Create a Form to Grab and Send New Users' Data

Design your form according to the set of attributes you are targeting. Keep it as simple as possible and include enhancements only after you are seeing progress.

Develop the code required to take the data entered in the fields of your form to build up a JSON structure the service can understand. Ensure your code creates well-formed JSON in all cases. A good number of errors stem from the fact the payload cannot be parsed by the service implementation.

### Code Routines to Process the HTTP POST

Take the code used for the dummy insertion and do the arrangements to be able to post an arbitary payload. Develop the required code to parse the response given by the server. It's important to be able to read:

- The response code. Upon a successful user creation, you have to get a 201 code

- The response header. Of particular interest is the "Location" header: it contains the URL that you can use to do a full (GET) query of the recently create resource. In our case it should look like `https://<host-name>/identity/restv1/scim/v2/Users/<new-user-inum>`

- The response body. It contains the full user representation in JSON format

While testing, it's important to compare that you are receiving in the body the contents you have sent. You will additionally receive other valuable information such as the creation timestamp.

### Create a Feedback Page

Create a success/failure page that shows the result of the operation based on the response received.

### Adjust Attribute Set

With your now-working application, do the adjustments to include attributes that may enrich your process. A common attribute could be `status`. This attribute (that maps to LDAP attribute `gluuStatus`) determines whether your created user is active or not. 

### Enhance your Form

Polish your form and add mechanisms to prevent abuse - a malicious user may end up creating lots of dummy entries. Add validations, captchas, etc. that may control indiscriminate submissions.
