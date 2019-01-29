# Forgot Password using SCIM

This is an abstract guide to describe how to implement a self-service Forgot Password workflow using Gluu's SCIM APIs. 

1. User clicks "forgot" password link from the login page and is redirected to the forgot pw application 
1. User is asked to enter username or email    

    !!! Note
    It's best not to indicate if the user exists to avoid leaking data unnecessarily.      
    
1. An e-mail is sent to the address associated with the account with a randomly generated link the user can click to reset password
1. User clicks the link that takes the browser to a form
1. The form shows two fields for the user to set `password` and `confirm password`
1. Upon form submission in the server side, validate the data to confirm both password fields have the same content
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

For an overview of best practices to follow when implementing your custom page, review [OWASP's Forgot PW cheatsheet](https://www.owasp.org/index.php/Forgot_Password_Cheat_Sheet). 
