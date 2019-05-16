# Forgot Password using SCIM
The Gluu Server ships with a built-in [feature for Forgot Password](../authn-guide/pw-reset.md), but it is typically **not** recommended for use in production. Instead, we recommend organizations write their own app, or leverage an existing open source tool dedicated to offering end-users the ability to reset their lost passwords. 

## Overview
The Gluu Server exposes SCIM APIs for managing user data. This is an abstract guide describing how to implement a self-service Forgot Password workflow using those SCIM APIs. 

## Workflow 

1. User clicks "forgot" password link from the login page and is redirected to the Forgot Password application. 
1. User is asked to enter username or email. In order to avoid leaking data unnecessarily, this page should neither confirm nor deny existence of the user.          
1. If there is an active user in the system associated with the username or email specified in the previous step, an e-mail is sent to the address on file with a link that is mapped to the user account with the help of a randomly generated, non-reusable token. The link should have sufficient entropy, and should expire within a short period of time, for instance 10 minutes. 
1. User clicks the link and which opens their browser to the form.
1. The form shows two fields for the user to set `password` and `confirm password`. A tool like [zxcvbn](https://github.com/dropbox/zxcvbn) might be used in this page to enforce a minimum level of entropy for new passwords. 
1. Upon form submission in the server side, validate the data to confirm both password fields have the same content.
1. If validation passes, a password update operation is performed by doing the following: 

    ```
    PUT /identity/restv1/scim/v2/Users/INUM_OF_USER
    attributes=id

    Host: gluu.host.com
    Accept: application/scim+json
    Content-Type: application/scim+json
    Authorization: Bearer TOKEN

    {
     "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
      "password": "PASSWORD_VALUE"
    }
    ```

    where:

    - INUM_OF_USER is the inum LDAP attribute of the user in question     
    - TOKEN is obtained according to UMA flow or test mode (ref doc [here](https://gluu.org/docs/ce/user-management/scim2/))    
    - and PASSWORD_VALUE is the value to set for password     

1. If the password update was successful, the following should be expected as response:

    ```
    HTTP/1.1 200 OK
    Content-Type: application/scim+json
    Location: ...

    {
         "schemas":["urn:ietf:params:scim:schemas:core:2.0:User"],
        "id": "INUM_OF_USER"
    }
    ```

## Best Practices

There is no industry standard for implementing a Forgot Password feature. However, for an overview of best practices, review [OWASP's Forgot PW cheatsheet](https://www.owasp.org/index.php/Forgot_Password_Cheat_Sheet). 
