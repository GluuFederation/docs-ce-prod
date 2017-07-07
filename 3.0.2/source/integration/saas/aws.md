# Login to AWS Webconsole using Gluu

This doc will teach you how setup Gluu to be your IDP for access to AWS webconsole. By using Gluu as your IDP, you can bypass the process of creating user accounts in AWS.  

This will help you better manage access based on LDAP groups within your enterprise environment rather then hard coding access with username and passwords or access keys and secret keys.

## Requirements
You will need to have a Gluu instance that is accessible by AWS. In our situation we deployed Gluu on an EC2 instance with a load balancer fronting the server in AWS.  

We also used route 53 to get a domain name and managed Certificate tied to the Gluu domain name. This provided access to our Gluu Server from AWS.
