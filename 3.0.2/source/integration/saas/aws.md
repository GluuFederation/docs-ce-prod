# Login to AWS Webconsole using Gluu

This doc will teach you how setup Gluu to be your IDP for access to the AWS webconsole. By using Gluu as your IDP, you can bypass the process of creating user accounts in AWS.  

This will help you better manage access based on LDAP groups within your enterprise environment rather then hard coding access with username and passwords or access keys and secret keys.

## Requirements
You will need to have a Gluu instance that is accessible by AWS. In our situation we deployed Gluu on an EC2 instance with a load balancer fronting the server in AWS.  

We also used route 53 to get a domain name and managed Certificate tied to the Gluu domain name. This provided access to our Gluu Server from AWS.

## AWS Configuration

### Create Identity Provider
First you need to get the Shibboleth meta data file from your Gluu installation, which can be found by navigating to the following URL: `https://<hostname>/idp/shibboleth`. With that file you can create an IDP in your AWS account. 

Now go to your AWS IAM webconsole and click on Identity Providers on the left. Click on the Create Provider. Give your provider a unique name and upload your Gluu xml file. This will establish your Gluu server as a trusted IDP.

### Create AWS Role
Next create a role with the permissions you want to give people. You can set whatever out of the box or custom 
policies you want and attach it to the AWS Role that you create. For example, you could have an admin role, power user role and a 
read only role with the appropriate policies attached. If you have questions about this, there are docs in AWS to help you do this.  

### Attach Trust Policy
After	creating	the	role	you	can	attach	the	trust	relationship	between	the	Role	and	the	Gluu	IDP	provider.		Here	is	a	
sample	of	the	relationship	policy.

```
{
		"Version":	"2012-10-17",
		"Statement":	[
				{
						"Effect":	"Allow",
						"Principal":	{
								"Federated":	"arn:aws:iam::<<YourAccountNumber>>:saml-provider/Gluu"
						},
						"Action":	"sts:AssumeRoleWithSAML",
						"Condition":	{
								"StringEquals":	{
										"SAML:aud":	[
												"https://<hostname>/idp/profile/SAML2/Unsolicited/SSO?
providerId=urn:amazon:webservices",
												"https://signin.aws.amazon.com/saml"
										]
								}
						}
				}
		]
}
```

### Create AWS Custom Attributes in LDAP

Now you need to add two new attributes into your Gluu LDAP. Follow [these instructions](https://gluu.org/docs/ce/admin-guide/attribute/#add-the-attribute-to-ldap) to add new attributes in your LDAP server. 

Here are a few sample attribute values we added to the custom.schema doc:

```
attributetype ( 1.3.6.1.4.1.48710.1.3.1003 NAME 'RoleEntitlement'
        EQUALITY caseIgnoreMatch
        SUBSTR caseIgnoreSubstringsMatch
        SYNTAX 1.3.6.1.4.1.1466.115.121.1.15
        X-ORIGIN 'Gluu - AWS Assume Role' )
```   
      
```
attributetype ( 1.3.6.1.4.1.48710.1.3.1004 NAME 'RoleSessionName'
        EQUALITY caseIgnoreMatch
        SUBSTR caseIgnoreSubstringsMatch
        SYNTAX 1.3.6.1.4.1.1466.115.121.1.15
        X-ORIGIN 'Gluu - AWS Assume Role Session Name' )
```   
 
```
objectclass ( 1.3.6.1.4.1.48710.1.4.101 NAME 'gluuCustomPerson'
        SUP ( top )
        AUXILIARY
        MAY ( telephoneNumber $ mobile $ RoleEntitlement $ RoleSessionName )
        X-ORIGIN 'Gluu - Custom persom objectclass' )
```  
      
Make sure the `attributetype` LDAP ID number is unique. Save and test the custom configuration.

### Add Attributes in Gluu Webconsole

