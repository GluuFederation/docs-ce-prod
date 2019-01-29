# Forgot Password using SCIM

This is an abstract guide to describe how to implement a self-service "forgot password" workflow using Gluu's SCIM APIs. 

1. User clicks a "forgot" password link 
1. User is requested to enter his username or email
1. An mail is sent to the e-mail linked to the account identified by data entered in the previous step
1. User clicks a link that takes the browser to a form
1. The form shows two fields "password" and "confirm password" the user must enter
1. Upon form submission in the server side, validate the data to confirm both password fields have the same content
1. If validation passes, a password update is performed by doing

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

1. If the password update took place, the following should be expected as response:

    ```
    HTTP/1.1 200 OK
    Content-Type: application/scim+json
    Location: ...

    {
         "schemas":["urn:ietf:params:scim:schemas:core:2.0:User"],
        "id": "INUM_OF_USER"
    }
    ```
