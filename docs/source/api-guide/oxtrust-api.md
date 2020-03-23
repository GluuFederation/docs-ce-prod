# Admin REST APIs

## Overview

Gluu Server 4.1.x offers REST APIs for the [oxTrust Admin GUI](https://gluu.org/docs/ce/4.1/admin-guide/oxtrust-ui/). With the REST API, server configurations can be automated, new GUIs can be built to expose specific admin functionality, and other integrations can be created for the Gluu admin portal.

## VM Installation instructions

Add the REST API extension to an existing Gluu 4.1.x deployment by following these steps:

1. Inside the Gluu chroot, navigate to `/custom/libs/`.

1. In this folder, download the .jar file corresponding to the Gluu Server CE 4.1 version currently installed:

    - [4.1.Final](https://ox.gluu.org/maven/org/gluu/oxtrust-api-server/4.1.Final/oxtrust-api-server-4.1.Final.jar)

1. Navigate to `/opt/gluu/jetty/identity/webapps/`.

1. Create a file called `identity.xml` if it does not already exist.

1. Add the following to `identity.xml`:

    ```
    <?xml version="1.0"  encoding="ISO-8859-1"?>
    <!DOCTYPE Configure PUBLIC "-//Jetty//Configure//EN" "http://www.eclipse.org/jetty/configure_9_0.dtd">

    <Configure class="org.eclipse.jetty.webapp.WebAppContext">
      <Set name="contextPath">/identity</Set>
      <Set name="war"><Property name="jetty.webapps" default="."/>/identity.war</Set>
      <Set name="extractWAR">true</Set>

      <Set name="extraClasspath">./custom/libs/[jarName].jar</Set>
    </Configure>
    ```

1. On the second to last line, replace `[jarName]` with the name of the `.jar` file downloaded in step 2.

1. [Restart](https://gluu.org/docs/ce/4.1/operation/services/#restart) the `identity` service.

## Kubernetes and Docker instructions

## Overview

The following sections are guides on how to access oxTrust API using within Gluu Server container deployment.
See below [oxTrust API docs](#available-api-modes) for reference.

## Prerequisites

1. `gluufederation/config-init:4.0.1_05` image (test mode client is introduced).
1. `gluufederation/persistence:4.0.1_05` image (enable oxTrust API upon deployment).
1. `gluufederation/oxauth:4.0.1_05` image.
1. `gluufederation/oxtrust:4.0.1_05` image.

## Available API Modes

The oxTrust API has two modes that administrators can configure according to need.

### Test Mode

!!! Note
    Test mode is not recommended for production. Choose UMA mode instead.

1.  Set environment variable `GLUU_OXTRUST_API_ENABLED=true` and `GUU_OXTRUST_API_TEST_MODE=true` when running `gluufederation/persistence` container to enable oxTrust API:

    ```sh
    docker run \
        --rm \
        --name persistence \
        -e GLUU_CONFIG_CONSUL_HOST=consul \
        -e GLUU_SECRET_VAULT_HOST=vault \
        -e GLUU_PERSISTENCE_TYPE=ldap \
        -e GLUU_PERSISTENCE_LDAP_MAPPING=default \
        -e GLUU_LDAP_URL=ldap:1636 \
        -e GLUU_OXTRUST_API_ENABLED=true \
        -e GLUU_OXTRUST_API_TEST_MODE=true \
        -v $PWD/vault_role_id.txt:/etc/certs/vault_role_id \
        -v $PWD/vault_secret_id.txt:/etc/certs/vault_secret_id \
        gluufederation/persistence:4.1.0_01
    ```
    
    If using kubernetes `pygluu-kubernetes.pyz` answer yes to both the following prompts: 
    
    ```sh
    Enable oxTrust Api         [N]?[Y/N]                               y
    Enable oxTrust Test Mode [N]?[Y/N]                                 y
    ```
    
    Alternatively, enable the features using oxTrust UI.
    
    1. Navigate to `Configuration > Manage Custom Scripts`, Under `UMA RPT Policies`, select and enable the custom script named `oxtrust_api_access_policy`
    
    1. Navigate to `Configuration > JSON Configuration`, select `oxTrust Configuration` tab
Search for the field named `oxTrustApiTestMode`, set it to `True` and save the change.

1.  Obtain Test mode client credentials from config and secret backends.

    1.  Grab `api_test_client_id` from config backend; in this example, we're getting `0008-b52a8524-35b2-4835-968e-481a366be8cd` as its value. This is the client ID.

    1.  Grab `api_test_client_secret` from secret backend; in this example, we're getting `TVtZwLZxp25XFDelMJNDQsa8` as its value. This is the client secret.

1.  Get token from Gluu Server; in this example we're using `https://demoexample.gluu.org`.

    ```sh
    curl -k -u '0008-b52a8524-35b2-4835-968e-481a366be8cd:TVtZwLZxp25XFDelMJNDQsa8' \
        https://demoexample.gluu.org/oxauth/restv1/token \
        -d grant_type=client_credentials
    ```

    The response example:

    ```json
    {
        "access_token": "0d14102c-70e5-485c-8b64-e56f1ecfcf3e",
        "token_type": "bearer",
        "expires_in": 299
    }
    ```

    Extract the `access_token` value (in this case, `0d14102c-70e5-485c-8b64-e56f1ecfcf3e` is the token).

1.  Make request to oxTrust API endpoints:

    ```sh
    curl -k -H 'Authorization: Bearer 0d14102c-70e5-485c-8b64-e56f1ecfcf3e' \
        https://demoexample.gluu.org/identity/restv1/api/v1/groups
    ```

    If succeed, the output is similar to the following:

    ```json
    [
        {
            "status": "ACTIVE",
            "displayName": "Gluu Manager Group",
            "description": "This group is for administrative purpose, with full acces to users",
            "members": [
                "inum=04f0d0e9-a609-4a0a-9580-ebd981a49a61,ou=people,o=gluu"
            ],
            "inum": "60B7",
            "owner": null,
            "organization": null,
            "iname": null
        }
    ]
    ```

### UMA Mode

1.  Set environment variable `GLUU_OXTRUST_API_ENABLED=true` when running `gluufederation/persistence` container to enable oxTrust API:

    ```sh
    docker run \
        --rm \
        --name persistence \
        -e GLUU_CONFIG_CONSUL_HOST=consul \
        -e GLUU_SECRET_VAULT_HOST=vault \
        -e GLUU_PERSISTENCE_TYPE=ldap \
        -e GLUU_PERSISTENCE_LDAP_MAPPING=default \
        -e GLUU_LDAP_URL=ldap:1636 \
        -e GLUU_OXTRUST_API_ENABLED=true \
        -e GLUU_OXTRUST_API_TEST_MODE=false \
        -v $PWD/vault_role_id.txt:/etc/certs/vault_role_id \
        -v $PWD/vault_secret_id.txt:/etc/certs/vault_secret_id \
        gluufederation/persistence:4.1.0_01
    ```
    
    If using kubernetes `pygluu-kubernetes.pyz` answer `Y` to enabling `oxTrust API` and `N` to enabling `Test Mode`.
    
    ```sh
    Enable oxTrust Api         [N]?[Y/N]                               y
    Enable oxTrust Test Mode [N]?[Y/N]                                 N
    ```
    Alternatively, enable the features using oxTrust UI.
    
    1. Navigate to `Configuration > Manage Custom Scripts`, Under `UMA RPT Policies`, select and enable the custom script named `oxtrust_api_access_policy`    

1.  Make request to oxTrust API (in this example, we're going to use `https://demoexample.gluu.org` URL), for example:

    ```sh
    curl -k -I https://demoexample.gluu.org/identity/restv1/api/v1/groups
    ```

    The request is rejected due to unauthenticated client and the response headers will be similar as the following:

    ```
    HTTP/1.1 401 Unauthorized
    WWW-Authenticate: UMA realm="Authorization required", host_id=demoexample.gluu.org, as_uri=https://demoexample.gluu.org/.well-known/uma2-configuration, ticket=ed5d9fa7-7117-4fc0-85c2-17a064448dc8
    ```

    Extract the ticket from `WWW-Authenticate` header; in this example the ticket is `ed5d9fa7-7117-4fc0-85c2-17a064448dc8`.

1.  Copy `api-rp.jks` and `api-rp-keys.json` from oxAuth container into host:

    ```sh
    docker cp oxauth:/etc/certs/api-rp.jks api-rp.jks \
        && docker cp oxauth:/etc/certs/api-rp-keys.json api-rp-keys.json
    ```
    
    In kubernetes get the oxauth pod name and use the following commands:
  
      ```sh
    kubectl cp oxauth-acsacsd2123:etc/certs/api-rp.jks api-rp.jks \
        && kubectl cp oxauth-acsacsd2123:etc/certs/api-rp-keys.json api-rp-keys.json
    ```
    


1.  Determine algorithm for signing JWT string, i.e. `RS256`.

    Here's an example of `api-rp-keys.json` contents:

    ```json
    {
        "keys": [
            {
                "kty": "RSA",
                "e": "AQAB",
                "use": "sig",
                "crv": "",
                "kid": "777c0619-802c-480d-9432-a5e25f85867a_sig_rs256",
                "x5c": ["MIIDAzCCAeugAwIBAgIgIoDkhKXYZG5/LDPoUEUBxLpvsUDwL+OEzkAMuMpglzLH6g9dDUyGVEh8iRg=="],
                "exp": 1606219942910,
                "alg": "RS256",
                "n": "r3LItabzy3Lg0SXf_6EZ1oANjyYQ_HCEj-r5cynyD7dnAQdXvkRLVMAby0EAoCaeEo_QkU79BCOY6o2w"
            }
        ]
    }
    ```

    Make sure `alg` value is `RS256`.
    Grab the `kid` value (in this example `777c0619-802c-480d-9432-a5e25f85867a_sig_rs256`).

1.  Grab keystore password from secret backend where key is `api_rp_client_jks_pass`. In this example, we're getting `secret` as its value.

1.  Convert `api-rp.jks` to `api-rp.pkcs12` (delete existing `api-rp.pkcs12` file if any):

    ```sh
    keytool -importkeystore \
        -srckeystore api-rp.jks \
        -srcstorepass secret  \
        -srckeypass secret \
        -srcalias 777c0619-802c-480d-9432-a5e25f85867a_sig_rs256 \
        -destalias 777c0619-802c-480d-9432-a5e25f85867a_sig_rs256 \
        -destkeystore api-rp.pkcs12 \
        -deststoretype PKCS12 \
        -deststorepass secret \
        -destkeypass secret
    ```

1.  Extract public and private key pair from `api-rp.pkcs12`:

    ```sh
    openssl pkcs12 -in api-rp.pkcs12 -nodes -out api-rp.pem -passin pass:secret
    ```

    Here's an example of generated `api-rp.pem`:

    ```text
    Bag Attributes
        friendlyName: d405b162-fb5d-4e9f-81cd-4edcb0db486a_sig_rs256
        localKeyID: 54 69 6D 65 20 31 35 37 35 31 37 34 30 33 35 32 33 30
    Key Attributes: <No Attributes>
    -----BEGIN PRIVATE KEY-----
    MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCwvKNUOZxaOcRB
    wwFtCJIqoqnaPYA0kfJEnnnm
    -----END PRIVATE KEY-----
    Bag Attributes
        friendlyName: d405b162-fb5d-4e9f-81cd-4edcb0db486a_sig_rs256
        localKeyID: 54 69 6D 65 20 31 35 37 35 31 37 34 30 33 35 32 33 30
    subject=/CN=oxAuth CA Certificates
    issuer=/CN=oxAuth CA Certificates
    -----BEGIN CERTIFICATE-----
    MIIDAzCCAeugAwIBAgIgAPS1X/1F5GFLp8xNYLbw9zs34TOwSd2Kz++dZHRijIkw
    grfXl0CuwA==
    -----END CERTIFICATE-----
    ```

    Grab the string starts with `-----BEGIN PRIVATE KEY-----` and ends with `-----END PRIVATE KEY-----`.
    This is the private key.

1.  Prepare data for generating JWT string.

    1.  Header

        ```json
        {
            "typ": "JWT",
            "alg": "RS256",
            "kid": "777c0619-802c-480d-9432-a5e25f85867a_sig_rs256"
        }
        ```

    1.  Payload

        Grab client ID from config backend where key is `oxtrust_requesting_party_client_id`. In this example we're getting `0008-76f0b100-6d68-4f21-96ca-c6e49d30094b` as its value.

        ```json
        {
            "iss": "0008-76f0b100-6d68-4f21-96ca-c6e49d30094b",
            "sub": "0008-76f0b100-6d68-4f21-96ca-c6e49d30094b",
            "exp": 1575185573,
            "iat": 1575181565,
            "jti": "2f1c50c6-0359-4913-b3f9-c17ca93a1b82",
            "aud": "https://demoexample.gluu.org/oxauth/restv1/token"
        }
        ```

        Note:

        - `iat` value is time since epoch; we can use `date +%s` command to get a value
        - `exp` value is expiration since epoch; we can use `date --date="1 hours" +%s`
        - `jti` value must be unique; we can use `uuidgen` command to get a value
        - `aud` is the URL for getting the token
        - `iss` and `sub` are client ID

    1.  Private key (see previous section about extracting private key)

    After header, payload, and private key are ready, generate JWT string using [debugger](https://jwt.io/#debugger-io) or any of supported [libraries](https://jwt.io/#libraries-io). Save the JWT string, for example:

    ```text
    eyJhbGciOiJSUzI1NiIs.RiLZyW2yYdF4P0QD0oY9zjBfsFwFSpSCRUe.3WnaETMtAIPpXQhry6SYFR1tFv1t4XO14o1qVA
    ```

1.  Grab token from `https://demoexample.gluu.org/oxauth/restv1/token`:

    ```sh
    curl -k https://demoexample.gluu.org/oxauth/restv1/token \
        -d grant_type='urn:ietf:params:oauth:grant-type:uma-ticket' \
        -d ticket='ed5d9fa7-7117-4fc0-85c2-17a064448dc8'  \
        -d client_id='0008-76f0b100-6d68-4f21-96ca-c6e49d30094b' \
        -d client_assertion_type='urn:ietf:params:oauth:client-assertion-type:jwt-bearer' \
        -d client_assertion='eyJhbGciOiJSUzI1NiIs.RiLZyW2yYdF4P0QD0oY9zjBfsFwFSpSCRUe.3WnaETMtAIPpXQhry6SYFR1tFv1t4XO14o1qVA'
        -d scope=`oxtrust-api-read oxtrust-api-write`
    ```

    The response example:

    ```json
    {
        "access_token": "d01cdc70-6519-4118-89bb-9ee1748acdd1_D8F4.E104.D094.6B62.79E0.6F8E.FB55.0509",
        "token_type": "Bearer",
        "upgraded": false,
        "pct": "0b598193-11cb-4926-9e4c-cc7c95e6ce37_CB14.8C6B.E2B2.46CD.53B2.CBEF.C50E.9FE9"
    }
    ```

    Extract value of `access_token`; in this case `d01cdc70-6519-4118-89bb-9ee1748acdd1_D8F4.E104.D094.6B62.79E0.6F8E.FB55.0509`.

1.  Retry request to get groups (this time pass along the token in the request header):

    ```sh
    curl -k -H 'Authorization: Bearer d01cdc70-6519-4118-89bb-9ee1748acdd1_D8F4.E104.D094.6B62.79E0.6F8E.FB55.0509' \
        https://demoexample.gluu.org/identity/restv1/api/v1/groups
    ```

    If succeed, the output is similar to the following:

    ```json
    [
        {
            "status": "ACTIVE",
            "displayName": "Gluu Manager Group",
            "description": "This group is for administrative purpose, with full acces to users",
            "members": [
                "inum=04f0d0e9-a609-4a0a-9580-ebd981a49a61,ou=people,o=gluu"
            ],
            "inum": "60B7",
            "owner": null,
            "organization": null,
            "iname": null
        }
    ]
    ```

    Reuse the token (as long as it still valid) to make any request to oxTrust API endpoints.

## Available API modes

The oxTrust API has two modes that administrators can configure according to need.

### Test Mode
   
Follow these steps to configure the test mode:

1. Move the oxTrust API jar to `/opt/gluu/jetty/identity/custom/libs/`.
1. Edit `identity.xml` as mentioned [above](#installation)
1. [Restart](https://gluu.org/docs/ce/4.1/operation/services/) the `identity` service
1. Log into Gluu Admin UI
1. Navigate to `Configuration` > `Manage Custom Scripts`
1. Under `UMA RPT Policies`, select and enable the custom script named `oxtrust_api_access_policy`
1. Save the custom script
1. Navigate to `Configuration` > `JSON Configuration`, select `oxTrust Configuration` tab
1. Search for the field named `oxTrustApiTestMode`, set it to `True` and save the change.
1. Add an OpenId Connect client for testing:
    
    - Client Name: **whatever you want**
    - Client secret: **a memorable secret**
    - scopes: **openid**,**permission**
    - grand types: **client_credentials**
    - Response type: **token**
    - NB: After pressing the save button, take note of the client ID generated and the secret. We need them for next step.

1. Run the command below from a terminal to request an access token from Gluu Server

    ```
    curl -k -u 'testClientId:testClientSecert' -d grant_type=client_credentials https://yourhostname/oxauth/restv1/token
    ```
    
1. Use that accesss token as Bearer token when making api calls.
   
### UMA Mode
  
The UMA mode is the mode in which the API is protected by UMA. This is the recommended mode for production server.

## Available Endpoints

| API | Description |
| --- | ----------- |
| [addClientToUmaResource](#addclienttoumaresource) | Add client to an UMA resource |
| [addGroupMember](#addgroupmember)| Add a group member |
| [addRadiusClient](#addradiusclient) | Add a new RADIUS client |
| [addScopeToClient](#addscopetoclient) | Add a scope to an OIDC client|
| [addScopeToUmaResource](#addscopetoumaresource) | Add a scope to an UMA resource |
| [create](#create) | Create a new configuration |
| [createAttribute](#createattribute) | Add a new attribute |
| [createClient](#createclient) | Add a new OpenID Connect client |
| [createCustomScript](#createcustomscript) | Add a new custom script |
| [createGroup](#creategroup) | Add a new group |
| [createPassportProvider](#createpassportprovider) | Add a new passport provider |
| [createPerson](#createperson) | Add a new person |
| [createScope](#createscope) | Add a new OpenID Connect scope |
| [createSectorIdentifier](#createsectoridentifier) | Add a new sector identifier |
| [createUmaResource](#createumaresource) | Add a new UMA resource| 
| [createUmaScope](#createumascope) | Add a new UMA scope |
| [delete](#delete) | Delete an existing configuration |
| [deleteAllProviders](#deleteallproviders) | Delete all providers |
| [deleteAllUmaScopes](#deleteallumascopes) | Delete all UMA scopes |
| [deleteAttribute](#deleteattribute) | Delete an attribute |
| [deleteAttributes](#deleteattributes) | Delete all attributes |
| [deleteClient](#deleteclient) | Delete an OpenID Connect client |
| [deleteClientScopes](#deleteclientscopes) | Delete the scopes in an OpenID Connect Client |
| [deleteClients](#deleteclients) | Delete all clients|
| [deleteCustomScript](#deletecustomscript) | Delete a custom script |
| [deleteGroup](#deletegroup) | Delete a group |
| [deleteGroupMembers](#deletegroupmembers) | Delete the members of a group |
| [deleteGroups](#deletegroups) | Delete all groups |
| [deletePeople](#deletepeople) | Delete all people |
| [deletePerson](#deleteperson) | Delete a person |
| [deleteProvider](#deleteprovider) | Delete a passport provider|
| [deleteRadiusClient](#deleteradiusclient) | Delete a RADIUS client |
| [deleteScope](#deletescope) | Delete an OpenID Connect scope|
| [deleteScopes](#deletescopes) | Delete all OpenID Connect scopes |
| [deleteSectorIdentifier](#deletesectoridentifier) | Delete a Sector Identifier |
| [deleteUmaResource](#deleteumaresource) | Delete an UMA resource |
| [deleteUmaScope](#deleteumascope) | Delete an UMA scope |
| [getAllActiveAttributes](#getallactiveattributes) | Get all active attributes |
| [getAllAttributes](#getallattributes) | Get all attributes |
| [getAllInactiveAttributes](#getallinactiveattributes) | Get all inactive attributes |
| [getAllScopes](#getallscopes) | Get all scopes |
| [getAllSectorIdentifiers](#getallsectoridentifiers) | Get all sector identifiers |
| [getAttributeByInum](#getattributebyinum) | Get a specific attribute |
| [getCasConfig](#getcasconfig) | Get the existing configuration |
| [getClientByInum](#getclientbyinum) | Get a specific OpenID Connect client |
| [getClientScope](#getclientscope) | Get scopes assigned to an OpenID client |
| [getConfiguration](#getconfiguration) | Get Gluu configuration |
| [getCurrentAuthentication](#getcurrentauthentication) | Get current authentication methods |
| [getCustomScriptsByInum](#getcustomscriptsbyinum) | Get specific custom scripts |
| [getGroupByInum](#getgroupbyinum) | Get a specific group|
| [getGroupMembers](#getgroupmembers) | Get members of a specific group |
| [getOxAuthJsonSettings](#getoxauthjsonsettings) | Get oxAuth JSON configuration settings |
| [getOxtrustJsonSettings](#getoxtrustjsonsettings) | Get oxTrust JSON configuration settings |
| [getOxtrustSettings](#getoxtrustsettings) | get oxTrust configuration settings |
| [getPassportBasicConfig](#getpassportbasicconfig) | Get Passport's basic configuration |
| [getPersonByInum](#getpersonbyinum) | Get a specific person |
| [getProviderById](#getproviderbyid) | Get a specific Passport provider |
| [getRadiusClient](#getradiusclient) | Get a specific RADIUS client |
| [getScopeByInum](#getscopebyinum) | Get a specific OpenID Connect scope |
| [getScopeClaims](#getscopeclaims) | List all claims for a scope |
| [getSectorIdentifierById](#getsectoridentifierbyid) | Get a specific Sector Identifier |
| [getServerConfig](#getserverconfig) | Get RADIUS server configuration |
| [getServerStatus](#getserverstatus) | Get current server status|
| [getSmtpServerConfiguration](#getsmtpserverconfiguration) | Get SMTP server configuration|
| [getUmaResourceById](#getumaresourcebyid) | Get a specific UMA resource |
| [getUmaResourceClients](#getumaresourceclients) | Get the clients for a specific UMA resource |
| [getUmaResourceScopes](#getumaresourcescopes) | Get the scopes for a specific UMA resource |
| [getUmaScopeByInum](#getumascopebyinum) | Get a specific UMA scope |
| [listCertificates](#listcertificates) | List descriptions of the Gluu Server's certificates |
| [listClients](#listclients) | List all OpenID Connect clients |
| [listCustomScripts](#listcustomscripts) | List all custom scripts |
| [listCustomScriptsByType](#listcustomscriptsbytype) | List all person authentication scripts |
| [listGroups](#listgroups) | List all groups |
| [listPeople](#listpeople) | List all people |
| [listProviders](#listproviders) | List all Passport providers |
| [listRadiusClients](#listradiusclients) | List all RADIUS clients |
| [listUmaResources](#listumaresources) | List all UMA resources |
| [listUmaScopes](#listumascopes) | List UMA scopes |
| [read](#read) | Get the existing configuration |
| [removeClientToUmaResource](#removeclienttoumaresource) | Remove a client from an UMA resource |
| [removeGroupMember](#removegroupmember) | Remove a member from a group |
| [removeScopeToClient](#removescopetoclient) | Remove an existing scope from a client |
| [removeScopeToUmaResource](#removescopetoumaresource) | Remove a scope from an UMA resource |
| [searchAttributes](#searchattributes) | Search attributes |
| [searchGroups](#searchgroups) | Search OpenID Connect clients |
| [searchGroups1](#searchgroups1) | Search groups |
| [searchGroups2](#searchgroups2) | Search person |
| [searchScope](#searchscope) | Search OpenID Connect scopes |
| [searchSectorIdentifier](#searchsectoridentifier) | Search sector identifiers |
| [searchUmaResources](#searchumaresources) | Search UMA resources |
| [searchUmaScopes](#searchumascopes) | Search UMA scopes |
| [status](#status) | Check the status of a configuration |
| [status1](#status1) | Check the status of an existing configuration |
| [testSmtpConfiguration](#testsmtpconfiguration) | Test the SMTP configuration |
| [update](#update) | Update the configuration |
| [update1](#update1) | Update an existing configuration |
| [updateAttribute](#updateattribute) | Update a new attribute | 
| [updateAuthenticationMethod](#updateauthenticationmethod) | Update the authentication methods | 
| [updateClient](#updateclient) | Update an OpenID Connect client | 
| [updateCustomScript](#updatecustomscript) | Update a custom script | 
| [updateGroup](#updategroup) | Update a group |
| [updateGroup1](#updategroup1) | Update a person |
| [updateOxauthJsonSetting](#updateoxauthjsonsetting) | Update an oxAuth JSON configuration setting | 
| [updateOxtrustJsonSetting](#updateoxtrustjsonsetting) | Update an oxTrust JSON configuration setting |
| [updateOxtrustSetting](#updateoxtrustsetting) | Update oxTrust settings |
| [updatePassportBasicConfig](#updatepassportbasicconfig) | Update Passport basic configuration |
| [updatePassportProvider](#updatepassportprovider) | Update a Passport provider |
| [updateRadiusClient](#updateradiusclient) | Update RADIUS client |
| [updateScope](#updatescope) | Update an OpenID Connect scope|
| [updateSectorIdentifier](#updatesectoridentifier) | Update a sector identifier | 
| [updateServerConfiguration](#updateserverconfiguration) | Update the RADIUS server configuration |
| [updateSmtpConfiguration](#updatesmtpconfiguration) | Update the SMTP configuration |
| [updateUmaResource](#updateumaresource) | Update an UMA Resource |
| [updateUmaScope](#updateumascope)| Update an UMA scope |


## API References

### addClientToUmaResource

**URL**

```
//api/v1/uma/resources/{id}/clients/{inum}
```

**HTTP Method**

`POST`

**Response Type**

UmaResource

| Field | Data Type |
|---    | --- |
| `dn` | String |
| `inum` | String |
| `id` | String |
| `name` | String |
| `iconUri` | String |
| `scopes` | List |
| `scopeExpression` | String |
| `clients` | List|
| `resources` | List |
| `rev` | String |
| `creator` | String |
| `description` | String |
| `type` | String |
| `creationDate` | Date |
| `expirationDate` | Date |
| `deletable` | Boolean |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Path | `id` | String |
| Path | `inum` | String |

-----

### addGroupMember

**URL**

```
//api/v1/groups/{inum}/members/{minum}
```

**HTTP Method**

`POST`

**Response Type**

String

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Path | `inum` | String |
| Path | `minum` | String |

-----

### addRadiusClient

**URL**

```
//api/v1/radius/clients
```

**HTTP Method**

`POST`

**Response Type**

RadiusClient

| Field | Data Type |
|---    | --- |
| `dn` | String | 
| `inum` | String |
| `name` | String | 
| `ipAddress` | String |
| `secret` | String | 
| `priority` | Integer |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Body | | `RadiusClient(RadiusClient)` |

-----

### addScopeToClient

**URL**

```
//api/v1/clients/{inum}/scopes/{sinum}
``` 

**HTTP Method**

`POST`

**Response Type**

String

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Path | `inum` | String |
| Path | `sinum` | String |

-----

### addScopeToUmaResource

**URL**

```
//api/v1/uma/resources/{id}/scopes/{inum}
```

**HTTP Method**

`POST`

**Response Type**

UmaResource

| Field | Data Type |
|---    | --- |
| `dn` | String |
| `inum` | String |
| `id` | String |
| `name` | String |
| `iconUri` | String |
| `scopes` | List |
| `scopeExpression` | String
| `clients` | List|
| `resources` | List |
| `rev` | String |
| `creator` | String |
| `description` | String |
| `type` | String |
| `creationDate` | Date |
| `expirationDate` | Date |
| `deletable` | Boolean |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Path | `id` | String |
| Path | `inum` | String |

-----

### create

**URL**

```
//api/v1/configuration/ldap
```

**HTTP Method**

`POST`

**Response Type**

LdapConfigurationDTO

| Field | Data Type |
|---    | --- |
| `configId` | String | 
| `bindDN` | String |
| `bindPassword` | String | 
| `servers` | List |
| `maxConnections` | Integer | 
| `useSSL` | Boolean |
| `baseDNs` | List |
| `primaryKey` | String | 
| `localPrimaryKey` | String | 
| `useAnonymousBind` | Boolean | 
| `enabled` | Boolean | 
| `level` | Integer |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Body | | `LdapConfigurationDTO(LdapConfigurationDTO)` |

-----

### createAttribute

**URL**

```
//api/v1/attributes
```

**HTTP Method**

`POST`

**Response Type**

GluuAttribute

| Field | Data Type | Options |
|---    | --- | --- |
| `dn` | String | |
| `selected` | Boolean | | 
| `inum` | String | | 
| `type` | String | | 
| `lifetime` | String | | 
| `sourceAttribute` | String | 
| `salt` | String |
| `nameIdType` | String | 
| `name` | String |
| `displayName` | String |  
| `description` | String |
| `origin` | String | 
| `dataType` | String | <ul> <li> `string` </li> <li> `numeric` </li> <li> `boolean` </li> <li> `binary`</li> <li> ` certificate` </li> <li> `generalizedTime` </li> </ul> |
| `editType` | List | |
| `viewType` | List | |
| `usageType` | List | |
| `oxAuthClaimName` | String | | 
| `seeAlso` | String | | 
| `status` | String | <ul> <li> `active` </li> <li> `inactive` </li> <li> `expired` </li> <li> `register` </li> </ul> |
| `saml1Uri` | String | |
| `saml2Uri` | String | |
| `urn` | String | |
| `oxSCIMCustomAttribute` | Boolean |  |
| `oxMultivaluedAttribute` | Boolean | |
| `custom` | Boolean | |
| `requred` | Boolean | |
| `attributeValidation` | AttributeValidation | | 
| `gluuTooltip` | String | |
| `adminCanAccess` | Boolean | |
| `adminCanView` | Boolean | |
| `adminCanEdit` | Boolean | |
| `userCanAccess` | Boolean | |
| `userCanView` | Boolean | |
| `whitePagesCanView` | Boolean | |  
| `userCanEdit` | Boolean | | 
| `baseDn` | String | | 

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Body | | `GluuAttribute(GluuAttribute)` |

-----

### createClient

**URL**

```
//api/v1/clients
```

**HTTP Method**

`POST`

**Response Type**

OxAuthClient

| Field | Data Type | Options |
|---    | --- | --- |
| `dn` | String | |
| `selected` | Boolean | | 
| `inum` | String | |
| `iname` | String | |
| `displayName` | String | | 
| `description` | String  | |
| `oxAuthAppType` | String | <ul> <li> `web` </li> <li> `native` </li> |
| `contacts` | List | |
| `oxAuthRedirectURIs` | List | | 
| `oxAuthPostLogoutRedirectURIs` | List | |
| `oxAuthScopes` | List | |
| `oxAuthClaims` | List | |
| `encodedClientSecret` | String | | 
| `userPassword` | String | |
| `associatedPersons` | List | |
| `oxAuthTrustedClient` | Boolean | |
| `responseTypes` | List | |
| `grantTypes` | List | |
| `logoUri` | String | |
| `clientUri` | String | |
| `policyUri` | String | |
| `tosUri` | String | |
| `jwksUri` | String | |
| `jwks` | String | |
| `sectorIdentifierUri` | String | | 
| `subjectType` | String | <ul> <li> `pairwise` </li> <li> `public` </li> </ul> |
| `idTokenTokenBindingCnf` | String | | 
| `rptAsJwt` | Boolean | |
| `accessTokenAsJwt` | Boolean | | 
| `accessTokenSigningAlg` | String | <ul> <li> `none` </li> <li> `HS256` </li> <li> `HS384` </li> <li> `HS512` </li> <li> `RS256` </li> <li> `RS384` </li> <li> `RS512` </li> <li> `ES256` </li> <li> `ES384` </li> <li> `ES512` </li> </ul> |
| `idTokenSignedResponseAlg` | String | <ul> <li> `none` </li> <li> `HS256` </li> <li> `HS384` </li> <li> `HS512` </li> <li> `RS256` </li> <li> `RS384` </li> <li> `RS512` </li> <li> `ES256` </li> <li> `ES384` </li> <li> `ES512` </li> </ul> |
| `idTokenEncryptedResponseAlg` | String | <ul> <li> `RSA1_5` </li> <li> `RSA-OAEP` </li> <li> `A128KW` </li> <li> `A256KW` </li> </ul> |
| `idTokenEncryptedResponseEnc` | String | <ul> <li> `A128CBC+HS256` </li> <li> `A256CBC+HS512` </li> <li> `A128GCM` </li> <li> `A256GCM` </li> </ul> |
| `userInfoSignedResponseAlg` | String | <ul> <li> `none` </li> <li> `HS256` </li> <li> `HS384` </li> <li> `HS512` </li> <li> `RS256` </li> <li> `RS384` </li> <li> `RS512` </li> <li> `ES256` </li> <li> `ES384` </li> <li> `ES512` </li> </ul> |
| `userInfoEncryptedResponseAlg` | String | <ul> <li> `RSA1_5` </li> <li> `RSA-OAEP` </li> <li> `A128KW` </li> <li> `A256KW` </li> </ul> |
| `userInfoEncryptedResponseEnc` | String | <ul> <li> `A128CBC+HS256` </li> <li> `A256CBC+HS512` </li> <li> `A128GCM` </li> <li> `A256GCM` </li> </ul> |
| `requestObjectSigningAlg` | String | <ul> <li> `none` </li> <li> `HS256` </li> <li> `HS384` </li> <li> `HS512` </li> <li> `RS256` </li> <li> `RS384` </li> <li> `RS512` </li> <li> `ES256` </li> <li> `ES384` </li> <li> `ES512` </li> </ul> |
| `requestObjectEncryptionAlg` | String | <ul> <li> `RSA1_5` </li> <li> `RSA-OAEP` </li> <li> `A128KW` </li> <li> `A256KW` </li> </ul> |
| `requestObjectEncryptionEnc` | String | <ul> <li> `A128CBC+HS256` </li> <li> `A256CBC+HS512` </li> <li> `A128GCM` </li> <li> `A256GCM` </li> </ul> |
| `tokenEndpointAuthMethod` | String | <ul> <li> `client_secret_basic` </li> <li> `client_secret_post` </li> <li> `client_secret_jwt` </li> <li> `private_key_jwt` </li> <li> `none` </li> |
| `tokenEndpointAuthSigningAlg` | String | <ul> <li> `none` </li> <li> `HS256` </li> <li> `HS384` </li> <li> `HS512` </li> <li> `RS256` </li> <li> `RS384` </li> <li> `RS512` </li> <li> `ES256` </li> <li> `ES384` </li> <li> `ES512` </li> </ul> |
| `defaultMaxAge` | Integer | | 
| `requireAuthTime` | Boolean | |  
| `postLogoutRedirectUris` | List | | 
| `claimRedirectURI` | List | |
| `logoutUri` | List | |
| `logoutSessionRequired` | Boolean | |
| `oxAuthPersistClientAuthorizations` | Boolean | | 
| `oxIncludeClaimsInIdToken` | Boolean | |
| `oxRefreshTokenLifetime` | Integer | |
| `accessTokenLifetime` | Integer | |
| `defaultAcrValues` | List | |
| `initiateLoginUri` | String | |
| `clientSecretExpiresAt` | Date | |
| `requestUris` | List | |
| `authorizedOrigins` | List | | 
| `softwareId` | String | |
| `softwareVersion` | String | | 
| `softwareStatement` | String | |
| `disabled` | Boolean | |
| `oxdId` | String | |
| `oxAuthClientSecret` | String | | 
| `attributes` | ClientAttributes | |
| `baseDn` | String | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Body |  | `OxAuthClient(OxAuthClient)` |

-----

### createCustomScript

**URL**

```
//api/v1/configuration/scripts
```

**HTTP Method**

`POST`

**Response Type**

CustomScript

| Field | Data Type | Options|
|---    | --- | --- |
| `dn` | String | |
| `inum` | String | | 
| `name` | String | | 
| `aliases` | List | | 
| `description` | String | | 
| `script` | String | | 
| `scriptType` | String | <ul> <li> `person_authentication` </li> <li> `introspection` </li> <li> `resource_owner_password_credentials` </li> <li> `application_session` </li> <li> `cache_refresh` </li> <li> `update_user` </li> <li> `user_registration` </li> <li> `client_registration` </li> <li> `id_generator` </li> <li> `uma_rpt_policy` </li> <li> `uma_claims_gathering` </li> <li> `consent_gathering` </li> <li> `dynamic_scope` </li> <li> `scim` </li> </ul> |
| `programmingLanguage` | String | <ul> <li> `python` </li> <li> `javascript` </li> </ul> |
| `moduleProperties` | List | | 
| `configurationProperties` | List | | 
| `level` | Integer | |
| `revision` | Long | | 
| `enabled` | Boolean | | 
| `scriptError` | ScriptError | | 
| `modified` | Boolean | | 
| `internal` | Boolean | | 
| `locationType` | String | <ul> <li> `ldap` </li> <li> `file` </li> |
| `locationPath` | String | | 
| `baseDn` | String | | 

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Body | | `CustomScript(CustomScript)` |

-----

### createGroup

**URL**

```
//api/v1/groups
```

**HTTP Method**

`POST`

**Response Type**

GluuGroupApi

| Field | Data Type | Options |
|---    | --- | --- |
| `inum` | String |  |
| `iname` | String | | 
| `displayName` | String | | 
| `description`  | String | | 
| `owner` | String | | 
| `members` | List | | 
| `organization` | String | | 
| `status` | String | <ul> <li> `active` </li> <li> `inactive` </li> <li> `expired` </li> <li> `register`  </li> </ul>|

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Body |  | `GluuGroupApi(GluuGroupApi)` |

-----

### createPassportProvider

**URL**

```
//api/v1/passport/providers
```

**HTTP Method**

`POST`

**Response Type**

Provider

| Field | Data Type |
|---    | --- |
| `id` | String | 
| `displayName` | String | 
| `type` | String |
| `mapping` | String | 
| `passportStrategyId` | String | 
| `enabled` | Boolean | 
| `callbackUrl` | String | 
| `requestForEmail` | Boolean | 
| `emailLinkingSafe` | Boolean | 
| `passportAuthnParams` | String |
| `options` | Map | 
| `logo_img` | String |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Body |  | `Provider(Provider)` |

-----

### createPerson

**URL**

```
//api/v1/users
```

**HTTP Method**

`POST`

**Response Type**

GluuPersonAPI

| Field | Data Type | Options |
|---    | --- | --- |
| `inum` | String | | 
| `iname` | String | |
| `surName` String | |
| `givenName` | String | | 
| `email` | String | |
| `password` | String | |
| `userName` | String | |
| `displayName` | String | |
| `creationDate` | Date | |
| `status` | String | <ul> <li> `active` </li> <li> `inactive` </li> <li> `expired` </li> <li> `register` </li> </ul> |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Body | | `GluuPersonApi(GluuPersonApi)` |

-----

### createScope

**URL**

```
//api/v1/scopes
```

**HTTP Method**

`POST`

**Response Type**

Scope

| Field | Data Type | Options |
|---    | --- | --- |
| `dn` | String | | 
| `inum` | String | | 
| `displayName` | String | | 
| `id` | String | | 
| `iconUrl` | String | | 
| `description` | String | | 
| `scopeType` | String | <ul> <li> `openid` </li> <li> `dynamic` </li> <li> `uma` </li> <li> `oauth` </li> </ul> |
| `oxAuthClaims` | List | | 
| `defaultScope` | Boolean | | 
| `oxAuthGroupClaims` | Boolean | | 
| `dynamicScopeScripts` | List | |  
| `umaAuthorizationPolicies` | List | | 
| `umaType` | Boolean | |
 
**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Body |  | `Scope(Scope)` |

-----

### createSectorIdentifier

**URL**

```
//api/v1/sectoridentifiers
```

**HTTP Method**

`POST`

**Response Type**

OxAuthSectoryIdentifier

| Field | Data Type |
|---    | --- |
| `dn` | String | 
| `selected` | Boolean | 
| `id` | String |
| `description` | String | 
| `redirectUris` | List | 
| `clientIds` | List | 
| `loginUri` | String |
| `baseDn` | String |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Body |  | `OxAuthSectorIdentifier(OxAuthSectorIdentifier)` |

-----

### createUmaResource

**URL**

```
//api/v1/uma/resources
```

**HTTP Method**

`POST`

**Response Type**

UmaResource

| Field | Data Type |
|---    | --- |
| `dn` | String |
| `inum` | String |
| `id` | String |
| `name` | String |
| `iconUri` | String |
| `scopes` | List |
| `scopeExpression` | String |
| `clients` | List|
| `resources` | List |
| `rev` | String |
| `creator` | String |
| `description` | String |
| `type` | String |
| `creationDate` | Date |
| `expirationDate` | Date |
| `deletable` | Boolean |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Body |  | `UmaResource(UmaResource)` |

-----

### createUmaScope

**URL**

```
//api/v1/uma/scopes
```

**HTTP Method**

`POST`

**Response Type**

Scope

| Field | Data Type | Options |
|---    | --- | --- |
| `dn` | String | | 
| `inum` | String | | 
| `displayName` | String | | 
| `id` | String | | 
| `iconUrl` | String | | 
| `description` | String | | 
| `scopeType` | String | <ul> <li> `openid`</li> <li> `dynamic` </li> <li> `uma` </li> <li> `oauth` </li> </ul> |
| `oxAuthClaims` | List | | 
| `defaultScope` | Boolean | | 
| `oxAuthGroupClaims` | Boolean | | 
| `dynamicScopeScripts` | List | |  
| `umaAuthorizationPolicies` | List | | 
| `umaType` | Boolean | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Body |  | `Scope(Scope)` |

-----

### delete

**URL**

```
//api/v1/configuration/ldap/{name}
```

**HTTP Method**

`DELETE`

**Response Type**

String

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Path | `name` | String |

-----

### deleteAllProviders

**URL**

```
//api/v1/passport/providers
```

**HTTP Method**

`DELETE`

**Response Type**

None

**Parameters**

None

-----

### deleteAllUmaScopes

**URL**

```
//api/v1/uma/scopes
```

**HTTP Method**

`DELETE`

**Response Type**

None

**Parameters**

None

-----

### deleteAttribute

**URL**

```
//api/v1/attributes/{inum}
```

**HTTP Method**

`DELETE`

**Response Type**

None

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Path | `inum` | String |

-----

### deleteAttributes

**URL**

```
//api/v1/attributes
```

**HTTP Method**

`DELETE`

**Response Type**

None

**Parameters**

None

-----

### deleteClient

**URL**

```
//api/v1/clients/{inum}
```

**HTTP Method**

`DELETE`

**Response Type**

String

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Path | `inum` | String |

-----

### deleteClientScopes

**URL**

```
//api/v1/clients/{inum}/scopes
```

**HTTP Method**

`DELETE`

**Response Type**

None

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Path | `inum` | String |

-----

### deleteClients

**URL**

```
//api/v1/clients
```

**HTTP Method**

`DELETE`

**Response Type**

None

**Parameters**

None

-----

### deleteCustomScript

**URL**

```
//api/v1/configuration/scripts/{inum}
```

**HTTP Method**

`DELETE`

**Response Type**

None

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Path | `inum` | String |

-----

### deleteGroup

**URL**

```
//api/v1/groups/{inum}
```

**HTTP Method**

`DELETE`

**Response Type**

None

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Path | `inum` | String |

-----

### deleteGroupMembers

**URL**

```
//api/v1/groups/{inum}/members
```

**HTTP Method**

`DELETE`

**Response Type**

None

**Parameters**

None

-----

### deleteGroups

**URL**

```
//api/v1/groups
```

**HTTP Method**

`DELETE`

**Response Type**

None 

**Parameters**

None

-----

### deletePeople

**URL**

```
//api/v1/users
```

**HTTP Method**

`DELETE`

**Response Type**

None

**Parameters**

None

-----

### deletePerson

**URL**

```
//api/v1/users/{inum}
```

**HTTP Method**

`DELETE`

**Response Type**

None

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Path | `inum` | String |

-----

### deleteProvider

**URL**

```
//api/v1/passport/providers/{id}
```

**HTTP Method**

`DELETE`

**Response Type**

None

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Path | `id` | String |

-----

### deleteRadiusClient

**URL**

```
//api/v1/radius/clients/{inum}
```

**HTTP Method**

`DELETE`

**Response Type**

None

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Path | `inum` | String |

-----

### deleteScope

**URL**

```
//api/v1/scopes/{inum}
```

**HTTP Method**

`DELETE`

**Response Type**

None

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Path | `inum` | String |

-----

### deleteScopes

**URL**

```
//api/v1/scopes
```

**HTTP Method**

`DELETE`

**Response Type**

None

**Parameters**

None

-----

### deleteSectorIdentifier

**URL**

```
//api/v1/sectoridentifiers/{inum}
```

**HTTP Method**

`DELETE`

**Response Type**

None

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Path | `inum` | String |

-----

### deleteUmaResource

**URL**

```
//api/v1/uma/resources/{id}
```

**HTTP Method**

`DELETE`

**Response Type**

None

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Path | `id` | String |

-----

### deleteUmaScope

**URL**

```
//api/v1/uma/scopes/{inum}
```

**HTTP Method**

`DELETE`

**Response Type**

None

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Path | `inum` | String |

-----

### getAllActiveAttributes

**URL**

```
//api/v1/attributes/active
```

**HTTP Method**

`GET`

**Response Type**

String

**Parameters**

None

-----

### getAllAttributes

**URL**

```
//api/v1/attributes
```

**HTTP Method**

`GET`

**Response Type**

String

**Parameters**

None

-----

### getAllInactiveAttributes

**URL**

```
//api/v1/attributes/inactive
```

**HTTP Method**

`GET`

**Response Type**

String

**Parameters**

None

-----

### getAllScopes

**URL**

```
//api/v1/scopes
```

**HTTP Method**

`GET`

**Response Type**

String

**Parameters**

None

-----

### getAllSectorIdentifiers

**URL**

```
//api/v1/sectoridentifiers
```

**HTTP Method**

`GET`

**Response Type**

String

**Parameters**

None

-----

### getAttributeByInum

**URL**

```
//api/v1/attributes/{inum}
```

**HTTP Method**

`GET`

**Response Type**

GluuAttribute

| Field | Data Type | Options |
|---    | --- | --- |
| `dn` | String | |
| `selected` | Boolean | | 
| `inum` | String | | 
| `type` | String | | 
| `lifetime` | String | | 
| `sourceAttribute` | String | 
| `salt` | String |
| `nameIdType` | String | 
| `name` | String |
| `displayName` | String |  
| `description` | String |
| `origin` | String | 
| `dataType` | String | <ul> <li> `string` </li> <li> `numeric` </li> <li> `boolean` </li> <li> `binary` </li> <li> `certificate` </li> <li> `generalizedTime` </li> </ul>|
| `editType` | List | |
| `viewType` | List | |
| `usageType` | List | |
| `oxAuthClaimName` | String | | 
| `seeAlso` | String | | 
| `status` | String | <ul> <li> `active` </li> <li> `inactive` </li> <li> `expired` </li> <li> `register` </li> </ul> |
| `saml1Uri` | String | |
| `saml2Uri` | String | |
| `urn` | String | |
| `oxSCIMCustomAttribute` | Boolean |  |
| `oxMultivaluedAttribute` | Boolean | |
| `custom` | Boolean | |
| `requred` | Boolean | |
| `attributeValidation` | AttributeValidation | | 
| `gluuTooltip` | String | |
| `adminCanAccess` | Boolean | |
| `adminCanView` | Boolean | |
| `adminCanEdit` | Boolean | |
| `userCanAccess` | Boolean | |
| `userCanView` | Boolean | |
| `whitePagesCanView` | Boolean | |  
| `userCanEdit` | Boolean | | 
| `baseDn` : String | | 

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Path  | `inum` | String |

-----

### getCasConfig

**URL**

```
//api/v1/configuration/cas
```

**HTTP Method**

`GET`

**Response Type**

CasProtocolDTO

| Field | Data Type |
|---    | --- |
| `casBaseURL` | String | 
| `shibbolethCASProtocolConfiguration` | `ShibbolethCASProtocolConfigurationDTO` |

**Parameters**

None

-----

### getClientByInum

**URL**

```
//api/v1/clients/{inum}
```

**HTTP Method**

`GET`

**Response Type**

OxAuthClient

| Field | Data Type | Options |
|---    | --- | --- |
| `dn` | String | |
| `selected` | Boolean | | 
| `inum` | String | |
| `iname` | String | |
| `displayName` | String | | 
| `description` | String | |
| `oxAuthAppType` | String | <ul> <li> `web` </li> <li> `native` </li> </ul> |
| `contacts` | List | |
| `oxAuthRedirectURIs` | List | | 
| `oxAuthPostLogoutRedirectURIs` | List | | 
| `oxAuthScopes` | List | |
| `oxAuthClaims` | List | |
| `encodedClientSecret` | String | | 
| `userPassword` | String | |
| `associatedPersons` | List | |
| `oxAuthTrustedClient` | Boolean | | 
| `responseTypes` | List | |
| `grantTypes` | List | | 
| `logoUri` | String | |
| `clientUri` | String | |
| `policyUri` | String | |
| `tosUri` | String | |
| `jwksUri` | String | |
| `jwks` | String | |
| `sectorIdentifierUri` | String | | 
| `subjectType` | String | <ul> <li> `pairwise` </li> <li> `public` </li> </ul> |
| `idTokenTokenBindingCnf` | String | | 
| `rptAsJwt` | Boolean | |
| `accessTokenAsJwt` | Boolean | | 
| `accessTokenSigningAlg` | String | <ul> <li> `none` </li> <li> `HS256` </li> <li> `HS384` </li> <li> `HS512` </li> <li> `RS256` </li> <li> `RS384` </li> <li> `RS512` </li> <li> `ES256` </li> <li> `ES384` </li> <li> `ES512` </li> </ul>
| `idTokenSignedResponseAlg` | String | <ul> <li>`none` </li> <li> `HS256` </li> <li> `HS384` </li> <li> `HS512` </li> <li> `RS256` </li> <li> `RS384` </li> <li> `RS512` </li> <li> `ES256` </li> <li> `ES384` </li> <li> `ES512` </li> </ul> |
| `idTokenEncryptedResponseAlg` | String | <ul> <li>`RSA1_5` </li> <li> `RSA-OAEP` </li> <li> `A128KW`</li> <li> `A256KW` </li> </ul> |
| `idTokenEncryptedResponseEnc` | String | <ul> <li> `A128CBC+HS256` </li> <li> `A256CBC+HS512` </li> <li> `A128GCM` </li> <li> `A256GCM` </li> </ul> |
| `userInfoSignedResponseAlg` | String | <ul> <li> `none` </li> <li> `HS256` </li> <li> `HS384` </li> <li> `HS512` </li> <li> `RS256` </li> <li> `RS384` </li> <li> `RS512` </li> <li> `ES256` </li> <li> `ES384` </li> <li> `ES512` </li> </ul> |
| `userInfoEncryptedResponseAlg` | String | <ul> <li> `RSA1_5` </li> <li> `RSA-OAEP` </li> <li> `A128KW` </li> <li> `A256KW` </li> </ul> |
| `userInfoEncryptedResponseEnc` | String | <ul> <li> `A128CBC+HS256` </li> <li> `A256CBC+HS512` </li> <li> `A128GCM` </li> <li> `A256GCM` </li> </ul> |
| `requestObjectSigningAlg` | String | <ul> <li> `none` </li> <li> `HS256` </li> <li> `HS384` </li> <li> `HS512` </li> <li> `RS256` </li> <li> `RS384` </li> <li> `RS512` </li> <li> `ES256` </li> <li> `ES384` </li> <li> `ES512` </li> </ul> |
| `requestObjectEncryptionAlg` | String | <ul> <li> `RSA1_5` </li> <li> `RSA-OAEP` </li> <li> `A128KW` </li> <li> `A256KW` </li> </ul> |
| `requestObjectEncryptionEnc` | String | <ul> <li> `A128CBC+HS256` </li> <li> `A256CBC+HS512` </li> <li> `A128GCM` </li> <li> `A256GCM` </li> </ul> |
| `tokenEndpointAuthMethod` | String | <ul> <li> `client_secret_basic` </li> <li> `client_secret_post` </li> <li> `client_secret_jwt` </li> <li> `private_key_jwt` </li> <li> `none` </li> </ul> |
| `tokenEndpointAuthSigningAlg` | String | <ul> <li> `none` </li> <li> `HS256` </li> <li> `HS384` </li> <li> `HS512` </li> <li> `RS256` </li> <li> `RS384` </li> <li> `RS512` </li> <li> `ES256` </li> <li> `ES384` </li> <li> `ES512` </li> </ul> |
| `defaultMaxAge` | Integer | | 
| `requireAuthTime` | Boolean | |
| `postLogoutRedirectUris` | List | |  
| `claimRedirectURI` | List | | 
| `logoutUri` | List | |
| `logoutSessionRequired` | Boolean | |  
| `oxAuthPersistClientAuthorizations` | Boolean | | 
| `oxIncludeClaimsInIdToken` | Boolean | |
| `oxRefreshTokenLifetime` | Integer | | 
| `accessTokenLifetime` | Integer | | 
| `defaultAcrValues` | List | | 
| `initiateLoginUri` | String | | 
| `clientSecretExpiresAt` | Date | |
| `requestUris` | List | |
| `authorizedOrigins` | List | | 
| `softwareId` | String | |
| `softwareVersion` | String | | 
| `softwareStatement` | String | |
| `disabled` | Boolean | |
| `oxdId` | String | |
| `oxAuthClientSecret` | String | | 
| `attributes` | ClientAttributes | |
| `baseDn` | String | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Path | `inum` | String |

-----

### getClientScope

**URL**

```
//api/v1/clients/{inum}/scopes
```

**HTTP Method**

`GET`

**Response Type**

String

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Path | `inum` | String |

-----

### getConfiguration

**URL**

```
//api/v1/configuration
```

**HTTP Method**

`GET`

**Response Type**

GluuConfiguration

| Field | Data Type | Options |
|---    | --- | --- |
| `dn` | String | | 
| `inum` | String | |
| `description` | String | | 
| `displayName` | String | | 
| `freeDiskSpace` | String | |
| `freeMemory` | String | |
| `freeSwap` | String | |
| `groupCount` | String | |
| `personCount` | String | |
| `hostname` | String | |
| `ipAddress` | String | |
| `systemUptime` | String | |
| `lastUpdate` | Date | |
| `pollingInterval` | String | | 
| `status` | String | <ul> <li> `active` </li> <li> `inactive` </li> <li> `expired` </li> <li> `register` </li> </ul> |
| `userPassword` | String | | 
| `gluuHttpStatus` | String | |
| `gluuDSStatus` | String | |
| `gluuVDSStatus` | String | |
| `gluuSPTR` | String | |
| `sslExpiry` | String | |
| `profileManagment` | Boolean | | 
| `manageIdentityPermission` | Boolean | | 
| `vdsCacheRefreshEnabled` | Boolean | |
| `cacheRefreshServerIpAddress` | String | | 
| `vdsCacheRefreshPollingInterval` | String | | 
| `vdsCacheRefreshLastUpdate` | Date | |
| `vdsCacheRefreshLastUpdateCount` | String | | 
| `vdsCacheRefreshProblemCount` | String | |
| `scimEnabled` | Boolean | |
| `passportEnabled` | Boolean | | 
| `contactEmail` | String | |
| `smtpConfiguration` | SmtpConfiguration | |
| `configurationDnsServer` | String | |
| `maxLogSize` | Integer | |
| `loadAvg` | String | |
| `oxIDPAuthentication` | List | | 
| `authenticationMode` | String | |
| `oxTrustAuthenticationMode` | String | | 
| `oxLogViewerConfig` | LogViewerConfig | |
| `oxLogConfigLocation` | String | |
| `passwordResetAllowed` | Boolean | |
| `trustStoreConfiguration` | TrustStoreConfiguration | | 
| `trustStoreCertificates` | List | |
| `cacheConfiguration` | CacheConfiguration | | 
| `baseDn` | String | | 

**Parameters**

None

-----

### getCurrentAuthentication

**URL**

```
//api/v1/acrs
```

**HTTP Method**

`GET`

**Response Type**

| Field | Data Type |
|---    | --- |
| `defaultAcr` | String | 
| `oxtrustAcr` | String |

**Parameters**

None

-----

### getCustomScriptsByInum

**URL**

//api/v1/configuration/scripts/{inum}

**HTTP Method**

`GET`

**Response Type**

CustomScript

| Field | Data Type | Options|
|---    | --- | --- |
| `dn` | String | |
| `inum` | String | | 
| `name` | String | | 
| `aliases` | List | | 
| `description` | String | | 
| `script` | String | | 
| `scriptType` | String | <ul> <li> `person_authentication` </li> <li> `introspection` </li> <li> `resource_owner_password_credentials` </li> <li> `application_session` </li> <li> `cache_refresh` </li> <li> `update_user` </li> <li> `user_registration` </li> <li> `client_registration` </li> <li> `id_generator` </li> <li> `uma_rpt_policy` </li> <li> `uma_claims_gathering` </li> <li> `consent_gathering` </li> <li> `dynamic_scope` </li> <li> `scim` </li> </ul>|
| `programmingLanguage` | String | <ul> <li> `python` </li> <li> `javascript` </li> </ul> |
| `moduleProperties` | List | | 
| `configurationProperties` | List | | 
| `level` | Integer | |
| `revision` | Long | | 
| `enabled` | Boolean | | 
| `scriptError` | ScriptError | | 
| `modified` | Boolean | | 
| `internal` | Boolean | | 
| `locationType` | String | <ul> <li> `ldap` </li> <li> `file` </li> </ul> |
| `locationPath` | String | | 
| `baseDn` | String | | 


**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Path | `inum` | String |

-----

### getGroupByInum

**URL**

```
//api/v1/groups/{inum}
```

**HTTP Method**

`GET`

**Response Type**

GluuGroupApi

| Field | Data Type | Options |
|---    | --- | --- |
| `inum` | String |  |
| `iname` | String | | 
| `displayName` | String | | 
| `description`  | String | | 
| `owner` | String | | 
| `members` | List | | 
| `organization` | String | | 
| `status` | String | <ul> <li> `active` </li> <li> `inactive` </li> <li> `expired` </li> <li> `register` </li> </ul> |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Path | `inum` | String |

-----

### getGroupMembers

**URL**

```
//api/v1/groups/{inum}/members
```

**HTTP Method**

`GET`

**Response Type**

String

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Path | `inum` | String |

-----

### getOxAuthJsonSettings

**URL**

```
//api/v1/configuration/oxauth/settings
```

**HTTP Method**

`GET`

**Response Type**

oxAuthJsonConfiguration

| Field | Data Type |
|---    | --- |
| `issuer` | String | 
| `baseEndpoint` | String |
| `authorizationEndpoint` | String | 
| `tokenEndpoint` | String |
| `tokenRevocationEndpoint` | String | 
| `userInfoEndpoint` | String |
| `clientInfoEndpoint` | String | 
| `checkSessionIFrame` | String |
| `endSessionEndpoint` | String | 
| `jwksUri` | String |
| `registrationEndpoint` | String |
| `openIdDiscoveryEndpoint` | String | 
| `openIdConfigurationEndpoint` | String | 
| `idGenerationEndpoint` | String | 
| `introspectionEndpoint` | String |
| `umaConfigurationEndpoint` | String | 
| `sectorIdentifierEndpoint` | String |
| `oxElevenGenerateKeyEndpoint` | String | 
| `oxElevenSignEndpoint` | String |
| `oxElevenVerifySignatureEndpoint` | String | 
| `oxElevenDeleteKeyEndpoint` | String | 
| `oxElevenJwksEndpoint` | String | 
| `openidSubAttribute` | String |
| `responseTypesSupported` | List | 
| `grantTypesSupported` | List |
| `subjectTypesSupported` | List | 
| `defaultSubjectType` | String |
| `userInfoSigningAlgValuesSupported` | List | 
| `userInfoEncryptionAlgValuesSupported` | List |
| `userInfoEncryptionEncValuesSupported` | List | 
| `idTokenSigningAlgValuesSupported` | List |
| `idTokenEncryptionAlgValuesSupported` | List |
| `idTokenEncryptionEncValuesSupported` | List |
| `requestObjectSigningAlgValuesSupported` | List | 
| `requestObjectEncryptionAlgValuesSupported` | List |
| `requestObjectEncryptionEncValuesSupported` | List | 
| `tokenEndpointAuthMethodsSupported` | List |
| `tokenEndpointAuthSigningAlgValuesSupported` | List |
| `dynamicRegistrationCustomAttributes` | List |
| `displayValuesSupported` | List | 
| `claimTypesSupported` | List |
| `serviceDocumentation` | String |
| `claimsLocalesSupported` | List |
| `idTokenTokenBindingCnfValuesSupported` | List | 
| `uiLocalesSupported` | List |
| `dynamicGrantTypeDefault` | List |
| `claimsParameterSupported` | Boolean |
| `requestParameterSupported` | Boolean |
| `requestUriParameterSupported` | Boolean | 
| `requireRequestUriRegistration` | Boolean |
| `allowPostLogoutRedirectWithoutValidation` | Boolean |
| `introspectionAccessTokenMustHaveUmaProtectionScope` | Boolean | 
| `opPolicyUri` | String | 
| `opTosUri` | String |
| `authorizationCodeLifetime` | Integer | 
| `refreshTokenLifetime` | Integer | 
| `idTokenLifetime` | Integer |
| `accessTokenLifetime` | Integer | 
| `umaResourceLifetime` | Integer | 
| `sessionAsJwt` | Boolean | 
| `umaRptLifetime` | Integer |
| `umaTicketLifetime` | Integer | 
| `umaPctLifetime` | Integer |
| `umaAddScopesAutomatically` | Boolean | 
| `umaValidateClaimToken` | Boolean | 
| `umaGrantAccessIfNoPolicies` | Boolean |
| `umaRestrictResourceToAssociatedClient` | Boolean |
| `umaKeepClientDuringResourceSetRegistration` | Boolean | 
| `umaRptAsJwt` | Boolean |
| `cleanServiceInterval` | Integer |
| `keyRegenerationEnabled` | Boolean | 
| `keyRegenerationInterval` | Integer |
| `defaultSignatureAlgorithm` | String | 
| `oxOpenIdConnectVersion` | String | 
| `organizationInum` | String | 
| `oxId` | String |
| `dynamicRegistrationEnabled` | Boolean | 
| `dynamicRegistrationExpirationTime` | Integer |
| `dynamicRegistrationPersistClientAuthorizations` | Boolean | 
| `trustedClientEnabled` | Boolean |
| `skipAuthorizationForOpenIdScopeAndPairwiseId` | Boolean | 
| `dynamicRegistrationScopesParamEnabled` | Boolean |
| `dynamicRegistrationCustomObjectClass` | String | 
| `personCustomObjectClassList` | List | 
| `persistIdTokenInLdap` | Boolean |
| `persistRefreshTokenInLdap` | Boolean | 
| `authenticationFiltersEnabled` | Boolean |
| `invalidateSessionCookiesAfterAuthorizationFlow` | Boolean | 
| `clientAuthenticationFiltersEnabled` | Boolean | 
| `authenticationFilters` | List |
| `clientAuthenticationFilters` | List | 
| `configurationInum` | String | 
| `sessionIdUnusedLifetime` | Integer |
| `sessionIdUnauthenticatedUnusedLifetime` | Integer | 
| `sessionIdEnabled` | Boolean |
| `sessionIdPersistOnPromptNone` | Boolean | 
| `sessionIdLifetime` | Integer |
| `configurationUpdateInterval` | Integer | 
| `cssLocation` | String | 
| `jsLocation` | String |
| `imgLocation` | String | 
| `metricReporterInterval` |  Integer |
| `metricReporterKeepDataDays` | Integer | 
| `pairwiseIdType` | String |
| `pairwiseCalculationKey` | String | 
| `pairwiseCalculationSalt` | String |
| `shareSubjectIdBetweenClientsWithSameSectorId` | Boolean | 
| `webKeysStorage` | String | 
| `dnName` | String |
| `keyStoreFile` | String | 
| `keyStoreSecret` | String |
| `endSessionWithAccessToken` | Boolean | 
| `clientWhiteList` | List | 
| `clientBlackList` | List | 
| `legacyIdTokenClaims` | Boolean |
| `customHeadersWithAuthorizationResponse` | Boolean |
| `frontChannelLogoutSessionSupported` | Boolean | 
| `updateUserLastLogonTime` | Boolean | 
| `updateClientAccessTime` | Boolean |
| `enableClientGrantTypeUpdate` | Boolean | 
| `corsConfigurationFilters` | List |
| `logClientIdOnClientAuthentication` | Boolean  |
| `logClientNameOnClientAuthentication` | Boolean | 
| `httpLoggingEnabled` | Boolean | 
| `httpLoggingExludePaths` | List |
| `externalLoggerConfiguration` | String |
| `authorizationRequestCustomAllowedParameters` | List | 
| `legacyDynamicRegistrationScopeParam` | Boolean |
| `openidScopeBackwardCompatibility` | Boolean |
| `useCacheForAllImplicitFlowObjects` | Boolean | 
| `disableU2fEndpoint` | Boolean | 
| `authenticationProtectionConfiguration` | `AuthenticationProtectionConfiguration` | 
| `fido2Configuration` | Fido2Configuration | 
| `loggingLevel` | String | 
| `errorHandlingMethod` | String | 

**Parameters**

None

-----

### getOxtrustJsonSettings

**URL**

```
//api/v1/configuration/oxtrust/settings
```

**HTTP Method**

`GET`

**Response Type**

OxTrustJsonSetting

| Field | Data Type |
|---    | --- |
| `orgName` | String | 
| `supportEmail` | String | 
| `scimTestMode` | Boolean |
| `authenticationRecaptchaEnabled` | Boolean | 
| `enforceEmailUniqueness` | Boolean |
| `loggingLevel` | String |
| `passwordResetRequestExpirationTime` | Integer |
| `cleanServiceInterval` | Integer |

**Parameters**

None

-----

### getOxtrustSettings

**URL**

```
//api/v1/configuration/settings
```

**HTTP Method**

`GET`

**Response Type**

OxtrustSetting

| Field | Data Type |
|---    | --- |
| `allowPasswordReset` | String | 
| `enablePassport `| String | 
| `enableScim` | String |
| `allowProfileManagement` | String |

**Parameters**

None

-----

### getPassportBasicConfig

**URL**

```
//api/v1/passport/config
```

**HTTP Method**

`GET`

**Response Type**

String

**Parameters**

None

-----

### getPersonByInum

**URL**

```
//api/v1/users/{inum}
```

**HTTP Method**

`GET`

**Response Type**

GluuPersonAPI

| Field | Data Type | Options |
|---    | --- | --- |
| `inum` | String | | 
| `iname` | String | |
| `surName` String | |
| `givenName` | String | | 
| `email` | String | |
| `password` | String | |
| `userName` | String | |
| `displayName` | String | |
| `creationDate` | Date | |
| `status` | String | <ul> <li> `active` </li> <li> `inactive` </li> <li> `expired` </li> <li> `register` </li> </ul>|

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Path | `inum` | String |

-----

### getProviderById

**URL**

```
//api/v1/passport/providers/{id}
```

**HTTP Method**

`GET`

**Response Type**

| Field | Data Type |
|---    | --- |
| `id` | String |
| `displayName` | String | 
| `type` | String |
| `mapping` | String |
| `passportStrategyId` | String | 
| `enabled` | Boolean |
| `callbackUrl` | String |
| `requestForEmail` | Boolean |
| `emailLinkingSafe` | Boolean |
| `passportAuthnParams` | String | 
| `options` | Map |
| `logo_img` | String | 

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Path | `id` | String |

-----

### getRadiusClient

**URL**

```
//api/v1/radius/clients/{inum}
```

**HTTP Method**

`GET`

**Response Type**

RadiusClient

| Field | Data Type |
|---    | --- |
| `dn` | String | 
| `inum` | String |
| `name` | String | 
| `ipAddress` | String |
| `secret` | String | 
| `priority` | Integer |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Path | `inum` | String |

-----

### getScopeByInum

**URL**

```
//api/v1/scopes/{inum}
```

**HTTP Method**

`GET`

**Response Type**

Scope

| Field | Data Type | Options |
|---    | --- | --- |
| `dn` | String | | 
| `inum` | String | | 
| `displayName` | String | | 
| `id` | String | | 
| `iconUrl` | String | | 
| `description` | String | | 
| `scopeType` | String | <ul> <li> `openid` </li> <li> `dynamic` </li> <li> `uma` </li> <li> `oauth` </li> </ul> |
| `oxAuthClaims` | List | | 
| `defaultScope` | Boolean | | 
| `oxAuthGroupClaims` | Boolean | | 
| `dynamicScopeScripts` | List | |  
| `umaAuthorizationPolicies` | List | | 
| `umaType` | Boolean | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Path | `inum` | String |

-----

### getScopeClaims

**URL**

```
//api/v1/scopes/{inum}/claims
```

**HTTP Method**

`GET`

**Response Type**

String

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Path | `inum` | String |

-----

### getSectorIdentifierById

**URL**

```
//api/v1/sectoridentifiers/{id}
```

**HTTP Method**

`GET`

**Response Type**
 
OxAuthSectorIdentifier
 
| Field | Data Type |
|---    | --- |
| `dn` | String | 
| `selected` | Boolean | 
| `id` | String | 
| `description` | String | 
| `redirectUris` | List | 
| `clientIds` | List | 
| `loginUri` | String | 
| `baseDn` | String | 

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Path | `id` | String |

-----

### getServerConfig

**URL**

```
//api/v1/radius/settings
```

**HTTP Method**

`GET`

**Response Type**

ServerConfiguration

| Field | Data Type |
|---    | --- |
| `dn` | String | 
| `listenInterface` | String | 
| `authPort` | Integer | 
| `acctPort` | Integer | 
| `openidUsername` | String | 
| `openidPassword` | String | 
| `openidBaseUrl` | String | 
| `acrValue` | String | 
| `scopes` | List | 
| `authenticationTimeout` | Integer | 

**Parameters**

None

-----

### getServerStatus

**URL**

```
//api/v1/configuration/status
```

**HTTP Method**

`GET`

**Response Type**

| Field | Data Type |
|---    | --- |
| `hostname` | String | 
| `ipAddress` | String | 
| `uptime` | String | 
| `lastUpdate` | Date | 
| `pollingInterval` | String | 
| `personCount` | String | 
| `groupCount` | String | 
| `freeMemory` | String | 
| `freeDiskSpace` | String |  

**Parameters**

None

-----

### getSmtpServerConfiguration

**URL**

```
//api/v1/configuration/smtp
```

**HTTP Method**

`GET`

**Response Type**

SmtpConfiguration

| Field | Data Type |
|---    | --- |
| `valid` | Boolean | 
| `host` | String | 
| `port` | Integer | 
| `requires-ssl` | Boolean | 
| `trust-host` | Boolean |
| `from-name` | String | 
| `from-email-address` | String |
| `requires-authentication` | Boolean | 
| `user-name` | String |
| `password` | String | 

**Parameters**

None

-----

### getUmaResourceById

**URL**

```
//api/v1/uma/resources/{id}
```

**HTTP Method**

`GET`

**Response Type**

UmaResource

| Field | Data Type |
|---    | --- |
| `dn` | String |
| `inum` | String |
| `id` | String |
| `name` | String |
| `iconUri` | String |
| `scopes` | List |
| `scopeExpression` | String |
| `clients` | List|
| `resources` | List |
| `rev` | String |
| `creator` | String |
| `description` | String |
| `type` | String |
| `creationDate` | Date |
| `expirationDate` | Date |
| `deletable` | Boolean |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Path | `id` | String |

-----

### getUmaResourceClients

**URL**

```
//api/v1/uma/resources/{id}/clients
```

**HTTP Method**

`GET`

**Response Type**

None

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Path | `id` | String |

-----

### getUmaResourceScopes

**URL**

```
//api/v1/uma/resources/{id}/scopes
```

**HTTP Method**

`GET`

**Response Type**

None

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Path | `id` | String |

-----

### getUmaScopeByInum

**URL**

```
//api/v1/uma/scopes/{inum}
```

**HTTP Method**

`GET`

**Response Type**
 
 Scope
 
| Field | Data Type | Options |
|---    | --- | --- |
| `dn` | String | | 
| `inum` | String | |
| `displayName` | String | | 
| `id` | String | | 
| `iconUrl` | String | | 
| `description` | String | | 
| `scopeType` | String | <ul> <li> `openid` </li> <li> `dynamic` </li> <li> `uma` </li> <li> `oauth` </li> </ul> |
| `oxAuthClaims` | List | | 
| `defaultScope` | Boolean | | 
| `oxAuthGroupClaims` | Boolean | | 
| `dynamicScopeScripts` | List | |
| `umaAuthorizationPolicies` | List | | 
| `umaType` | Boolean | | 

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Path | `inum` | String |

-----

### listCertificates

**URL**

```
//api/v1/certificates
```

**HTTP Method**

`GET`

**Response Type**

String

**Parameters**

None

-----

### listClients

**URL**

```
//api/v1/clients
```

**HTTP Method**

`GET` 

**Response Type**

String

**Parameters**

None

-----

### listCustomScripts

**URL**

```
//api/v1/configuration/scripts
```

**HTTP Method**

`GET`

**Response Type**

String

**Parameters**

None

-----

### listCustomScriptsByType

**URL**

```
//api/v1/configuration/scripts/type/{type}
```

**HTTP Method**

`GET`

**Response Type**

String

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Path | `type` | String |

-----

### listGroups

**URL**

```
//api/v1/groups
```

**HTTP Method**

`GET`

**Response Type**

String

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Query | `size` | Integer |

-----

### listPeople

**URL**

```
//api/v1/users
```

**HTTP Method**

`GET`

**Response Type**

String

**Parameters**

None

-----

### listProviders

**URL**

```
//api/v1/passport/providers
```

**HTTP Method**

`GET`

**Response Type**

String

**Parameters**

None

-----

### listRadiusClients

**URL**

```
//api/v1/radius/clients
```

**HTTP Method**

`GET`

**Response Type**

String

**Parameters**

None

-----

### listUmaResources

**URL**

```
//api/v1/uma/resources
```

**HTTP Method**

`GET`

**Response Type**

String

**Parameters**

None

-----

### listUmaScopes

**URL**

```
//api/v1/uma/scopes
```

**HTTP Method**

`GET`

**Response Type**

String

**Parameters**

None

-----

### read

**URL**

```
//api/v1/configuration/ldap
```

**HTTP Method**

`GET`

**Response Type**

String

**Parameters**

None

-----

### removeClientToUmaResource

**URL**

```
//api/v1/uma/resources/{id}/clients/{inum}
```

**HTTP Method**

`DELETE`

**Response Type**

UmaResource

| Field | Data Type |
|---    | --- |
| `dn` | String | 
| `inum` | String | 
| `id` | String | 
| `name` | String | 
| `iconUri` | String | 
| `scopes` | List | 
| `scopeExpression` | String | 
| `clients` | List |  
| `resources` | List | 
| `rev` | String | 
| `creator` | String | 
| `description` | String | 
| `type` | String | 
| `creationDate` | Date | 
| `expirationDate` | Date | 
| `deletable` | Boolean | 

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Path | `id` | String |
| Path | `inum` | String |

-----

### removeGroupMember

**URL**

```
//api/v1/groups/{inum}/members/{minum}
```

**HTTP Method**

`DELETE`

**Response Type**

None

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Path | `inum` | String |
| Path | `minum` | String |

-----

### removeScopeToClient

**URL**

```
//api/v1/clients/{inum}/scopes/{sinum}
```

**HTTP Method**

```
DELETE
```

**Response Type**

String

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Path | `inum` | String |
| Path | `sinum` | String |

-----

### removeScopeToUmaResource

**URL**

```
//api/v1/uma/resources/{id}/scopes/{inum}
```

**HTTP Method**

`DELETE`

**Response Type**

UmaResource

| Field | Data Type |
|---    | --- |
| `dn` | String | 
| `inum` | String | 
| `id` | String | 
| `name` | String | 
| `iconUri` | String | 
| `scopes` | List | 
| `scopeExpression` | String | 
| `clients` | List |  
| `resources` | List | 
| `rev` | String | 
| `creator` | String | 
| `description` | String | 
| `type` | String | 
| `creationDate` | Date | 
| `expirationDate` | Date | 
| `deletable` | Boolean | 

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Path | `id` | String |
| Path | `inum` | String |

-----

### searchAttributes

**URL**

```
//api/v1/attributes/search
```

**HTTP Method**

`GET`

**Response Type**

GluuAttribute

| Field | Data Type | Options |
|---    | --- | --- |
| `dn` | String | |
| `selected` | Boolean | | 
| `inum` | String | | 
| `type` | String | | 
| `lifetime` | String | | 
| `sourceAttribute` | String | |
| `salt` | String | |
| `nameIdType` | String | | 
| `name` | String | |
| `displayName` | String | |  
| `description` | String | |
| `origin` | String | | 
| `dataType` | String | <ul> <li> `string` </li> <li> `numeric` </li> <li> `boolean` </li> <li> `binary` </li> <li> `certificate` </li> <li> `generalizedTime` </li> </ul> |
| `editType` | List | |
| `viewType` | List | |
| `usageType` | List | |
| `oxAuthClaimName` | String | | 
| `seeAlso` | String | | 
| `status` | String | <ul> <li> `active` </li> <li> `inactive` </li> <li> `expired` </li> <li> `register` </li> </ul> |
| `saml1Uri` | String | |
| `saml2Uri` | String | |
| `urn` | String | |
| `oxSCIMCustomAttribute` | Boolean |  |
| `oxMultivaluedAttribute` | Boolean | |
| `custom` | Boolean | |
| `requred` | Boolean | |
| `attributeValidation` | AttributeValidation | | 
| `gluuTooltip` | String | |
| `adminCanAccess` | Boolean | |
| `adminCanView` | Boolean | |
| `adminCanEdit` | Boolean | |
| `userCanAccess` | Boolean | |
| `userCanView` | Boolean | |
| `whitePagesCanView` | Boolean | |  
| `userCanEdit` | Boolean | | 
| `baseDn` : String | | 

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Query | `pattern` | String |
| Query | `size` | Integer |

-----

### searchGroups

**URL**

```
//api/v1/clients/search
```

**HTTP Method**

`GET`

**Response Type**

String

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Query | `pattern` | String |
| Query | `size` | Integer |

-----

### searchGroups1

**URL**

```
//api/v1/groups/search
```

**HTTP Method**

`GET`

**Response Type**

String

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Query | `pattern` | String |
| Query | `size` | Integer |

-----

### searchGroups2

**URL**

```
//api/v1/users/search
```

**HTTP Method**

`GET`

**Response Type**

String

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Query | `pattern` | String |

----

### searchScope

**URL**

```
//api/v1/scopes/search
```

**HTTP Method**

`GET`

**Response Type**

String

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Query | `pattern` | String |
| Query | `size` | Integer |

-----

### searchSectorIdentifier

**URL**

```
//api/v1/sectoridentifiers/search
```

**HTTP Method**

`GET`

**Response Type**

String

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Query | `pattern` | String |
| Query | `size` | Integer |

-----

### searchUmaResources

**URL**

```
//api/v1/uma/resources/search
```

**HTTP Method**

`GET`

**Response Type**

String

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Query | `pattern` | String |
| Query | `size` | Integer |

-----

### searchUmaScopes

**URL**

```
//api/v1/uma/scopes/search
```

**HTTP Method**

`GET`

**Response Type**

String

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Query | `pattern` | String |

-----

### status

**URL**

```
//api/v1/configuration/ldap/status
```

**HTTP Method**

`POST`

**Response Type**

ConnectionStatusDTO

| Field | Data Type |
|---    | --- |
| up | Boolean |

**Parameters**

| Location | Parameter Name | Input |
|---   | --- | --- |
| Body |  | `LdapConnectionData(LdapConnectionData)` |

-----

### status1

**URL**

```
//api/v1/configuration/ldap/{name}/status
```

**HTTP Method**

`GET`

**Response Type**

ConnectionStatusDTO

| Field | Data Type |
|---    | --- |
| up | Boolean |

**Parameters**

| Location | Parameter Name | Input |
| ---  | --- | --- |
| Path | `name` | String |

-----

### testSmtpConfiguration

**URL**

```
//api/v1/configuration/smtp/test
```

**HTTP Method**

`GET`

**Response Type**

SmtpConfiguration

| Field | Data Type |
|---    | --- |
| `valid` | Boolean | 
| `host` | String | 
| `port` | Integer | 
| `requires-ssl` | Boolean | 
| `trust-host` | Boolean |
| `from-name` | String | 
| `from-email-address` | String |
| `requires-authentication` | Boolean | 
| `user-name` | String |
| `password` | String | 

**Parameters**

None

-----

### update

**URL**

```
//api/v1/configuration/cas
```

**HTTP Method**

`PUT`

**Response Type**

CasProtocolDTO

| Field | Data Type |
|---    | --- |
| `casBaseURL` | String | 
| `shibbolethCASProtocolConfiguration` | `ShibbolethCASProtocolConfigurationDTO` |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Body |  | `CasProtocolDTO(CasProtocolDTO)` |

-----

### update1

**URL**

```
//api/v1/configuration/ldap
```

**HTTP Method**

`PUT`

**Response Type**

LdapConfigurationDTO

| Field | Data Type |
|---    | --- |
| `configId` | String | 
| `bindDN`  | String | 
| `bindPassword` | String | 
| `servers` | List | 
| `maxConnections` | Integer |
| `useSSL` | Boolean | 
| `baseDNs` | List | 
| `primaryKey` | String  |
| `localPrimaryKey` | String | 
| `useAnonymousBind` | Boolean | 
| `enabled`  | Boolean  |
| `level` | Integer | 

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Body | | `LdapConfigurationDTO(LdapConfiguraitonDTO)` |

-----

### updateAttribute

**URL**

```
//api/v1/attributes
```

**HTTP Method**

`PUT`

**Response Type**

GluuAttribute

| Field | Data Type | Options |
|---    | --- | --- |
| `dn` | String | |
| `selected` | Boolean | | 
| `inum` | String | | 
| `type` | String | | 
| `lifetime` | String | | 
| `sourceAttribute` | String | |
| `salt` | String | |
| `nameIdType` | String | | 
| `name` | String | |
| `displayName` | String | |  
| `description` | String | |
| `origin` | String |  |
| `dataType` | String | <ul> <li> `string` </li> <li> `numeric` </li> <li> `boolean` </li> <li> `binary` </li> <li> `certificate` </li> <li> `generalizedTime` </li> </ul> |
| `editType` | List | |
| `viewType` | List | |
| `usageType` | List | |
| `oxAuthClaimName` | String | | 
| `seeAlso` | String | | 
| `status` | String | <ul> <li> `active` </li> <li> `inactive` </li> <li> `expired` </li> <li> `register` </li> </ul> |
| `saml1Uri` | String | |
| `saml2Uri` | String | |
| `urn` | String | |
| `oxSCIMCustomAttribute` | Boolean |  |
| `oxMultivaluedAttribute` | Boolean | |
| `custom` | Boolean | |
| `requred` | Boolean | |
| `attributeValidation` | AttributeValidation | | 
| `gluuTooltip` | String | |
| `adminCanAccess` | Boolean | |
| `adminCanView` | Boolean | |
| `adminCanEdit` | Boolean | |
| `userCanAccess` | Boolean | |
| `userCanView` | Boolean | |
| `whitePagesCanView` | Boolean | |  
| `userCanEdit` | Boolean | | 
| `baseDn` : String | | 

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Body | | `GluuAttribute(GluuAttribute)` |

-----

### updateAuthenticationMethod

**URL**

```
//api/v1/acrs
```

**HTTP Method**

`PUT`

**Response Type**

| Field | Data Type |
|---    | --- |
| `defaultAcr` | String | 
| `oxtrustAcr` | String | 

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Body | | `AuthenticationMethod(AuthenticationMethod)` |

-----

### updateClient

**URL**

```
//api/v1/clients
```

**HTTP Method**

`PUT`

**Response Type**

OxAuthClient

| Field | Data Type | Options |
|---    | --- | --- |
| `dn` | String | |
| `selected` | Boolean | | 
| `inum` | String | |
| `iname` | String | |
| `displayName` | String | | 
| `description` | String  | |
| `oxAuthAppType` | String | <ul> <li> `web` </li> <li> `native` </li> </ul>|
| `contacts` | List | |
| `oxAuthRedirectURIs` | List | | 
| `oxAuthPostLogoutRedirectURIs` | List | |
| `oxAuthScopes` | List | |
| `oxAuthClaims` | List | |
| `encodedClientSecret` | String | | 
| `userPassword` | String | |
| `associatedPersons` | List | |
| `oxAuthTrustedClient` | Boolean | |
| `responseTypes` | List | |
| `grantTypes` | List | |
| `logoUri` | String | |
| `clientUri` | String | |
| `policyUri` | String | |
| `tosUri` | String | |
| `jwksUri` | String | |
| `jwks` | String | |
| `sectorIdentifierUri` | String | | 
| `subjectType` | String | <ul> <li> `pairwise` </li> <li> `public` </li> </ul> |
| `idTokenTokenBindingCnf` | String | | 
| `rptAsJwt` | Boolean | |
| `accessTokenAsJwt` | Boolean | | 
| `accessTokenSigningAlg` | String | <ul> <li> `none` </li> <li> `HS256` </li> <li> `HS384` </li> <li> `HS512` </li> <li> `RS256` </li> <li> `RS384` </li> <li> `RS512` </li> <li> `ES256` </li> <li> `ES384` </li> <li> `ES512` </li> </ul> |
| `idTokenSignedResponseAlg` | String | <ul> <li> `none` </li> <li> `HS256` </li> <li> `HS384` </li> <li> `HS512` </li> <li> `RS256` </li> <li> `RS384` </li> <li> `RS512` </li> <li> `ES256` </li> <li> `ES384` </li> <li> `ES512` </li> </ul> | 
| `idTokenEncryptedResponseAlg` | String | <ul> <li> `RSA1_5` </li> <li> `RSA-OAEP` </li> <li> `A128KW` </li> <li> `A256KW` </li> </ul> |
| `idTokenEncryptedResponseEnc` | String | <ul> <li> `A128CBC+HS256` </li> <li> `A256CBC+HS512` </li> <li> `A128GCM` </li> <li> `A256GCM` </li> </ul> |
| `userInfoSignedResponseAlg` | String | <ul> <li> `none` </li> <li> `HS256` </li> <li> `HS384` </li> <li> `HS512` </li> <li> `RS256` </li> <li> `RS384` </li> <li> `RS512` </li> <li> `ES256` </li> <li> `ES384` </li> <li> `ES512` </li> </ul> |
| `userInfoEncryptedResponseAlg` | String | <ul> <li> `RSA1_5` </li> <li> `RSA-OAEP` </li> <li> `A128KW` </li> <li> `A256KW` </li> </ul> |
| `userInfoEncryptedResponseEnc` | String | <ul> <li> `A128CBC+HS256` </li> <li> `A256CBC+HS512` </li> <li> `A128GCM` </li> <li> `A256GCM` </li> </ul> |
| `requestObjectSigningAlg` | String | <ul> <li> `none` </li> <li> `HS256` </li> <li> `HS384` </li> <li> `HS512` </li> <li> `RS256` </li> <li> `RS384` </li> <li> `RS512` </li> <li> `ES256` </li> <li> `ES384` </li> <li> `ES512` </li> </ul> |
| `requestObjectEncryptionAlg` | String | <ul> <li> `RSA1_5` </li> <li> `RSA-OAEP` </li> <li> `A128KW` </li> <li> `A256KW` </li> </ul> |
| `requestObjectEncryptionEnc` | String | <ul> <li> `A128CBC+HS256` </li> <li> `A256CBC+HS512` </li> <li> `A128GCM` </li> <li> `A256GCM` </li> </ul> |
| `tokenEndpointAuthMethod` | String | <ul> <li> `client_secret_basic` </li> <li> `client_secret_post` </li> <li>  `client_secret_jwt` </li> <li> `private_key_jwt` </li> <li> `none` </li> </ul> |
| `tokenEndpointAuthSigningAlg` | String | <ul> <li> `none` </li> <li> `HS256` </li> <li> `HS384` </li> <li> `HS512` </li> <li> `RS256` </li> <li> `RS384` </li> <li> `RS512` </li> <li> `ES256` </li> <li> `ES384` </li> <li> `ES512` </li> </ul> |
| `defaultMaxAge` | Integer | | 
| `requireAuthTime` | Boolean | |  
| `postLogoutRedirectUris` | List | | 
| `claimRedirectURI` | List | |
| `logoutUri` | List | |
| `logoutSessionRequired` | Boolean | |
| `oxAuthPersistClientAuthorizations` | Boolean | | 
| `oxIncludeClaimsInIdToken` | Boolean | |
| `oxRefreshTokenLifetime` | Integer | |
| `accessTokenLifetime` | Integer | |
| `defaultAcrValues` | List | |
| `initiateLoginUri` | String | |
| `clientSecretExpiresAt` | Date | |
| `requestUris` | List | |
| `authorizedOrigins` | List | | 
| `softwareId` | String | |
| `softwareVersion` | String | | 
| `softwareStatement` | String | |
| `disabled` | Boolean | |
| `oxdId` | String | |
| `oxAuthClientSecret` | String | | 
| `attributes` | ClientAttributes | |
| `baseDn` | String | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Body |  | `OxAuthClient(OxAuthClient)` |

-----

### updateCustomScript

**URL**

```
//api/v1/configuration/scripts
```

**HTTP Method**

`PUT`

**Response Type**

CustomScript

| Field | Data Type | Options|
|---    | --- | --- |
| `dn` | String | |
| `inum` | String | | 
| `name` | String | | 
| `aliases` | List | | 
| `description` | String | | 
| `script` | String | | 
| `scriptType` | String | <ul> <li> `person_authentication` </li> <li> `introspection` </li> <li> `resource_owner_password_credentials` </li> <li> `application_session` </li> <li> `cache_refresh` </li> <li> `update_user` </li> <li> `user_registration` </li> <li> `client_registration` </li> <li> `id_generator` </li> <li> `uma_rpt_policy` </li> <li> `uma_claims_gathering` </li> <li> `consent_gathering` </li> <li> `dynamic_scope` </li> <li> `scim` </li> </ul> |
| `programmingLanguage` | String | <ul> <li> `python` </li> <li> `javascript` </li> </ul> |
| `moduleProperties` | List | | 
| `configurationProperties` | List | | 
| `level` | Integer | |
| `revision` | Long | | 
| `enabled` | Boolean | | 
| `scriptError` | ScriptError | | 
| `modified` | Boolean | | 
| `internal` | Boolean | | 
| `locationType` | String | <ul> <li> `ldap` </li> <li> `file` </li> </ul> |
| `locationPath` | String | | 
| `baseDn` | String | | 

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Body | | `CustomScript(CustomScript)` |

-----

### updateGroup

**URL**

```
//api/v1/groups
```

**HTTP Method**

`PUT`

**Response Type**

GluuGroupApi

| Field | Data Type | Options |
|---    | --- | --- |
| `inum` | String | | 
| `iname` | String | | 
| `displayName` | String | | 
| `description` | String | | 
| `owner` | String | | 
| `members` | List | | 
| `organization` | String | | 
| `status` | String | <ul> <li> `active` </li> <li> `inactive` </li> <li> `expired` </li> <li> `register` </li> </ul> |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Body | | `GluuPersonApi(GluuPersonApi)` |

-----

### updateGroup1

**URL**

```
//api/v1/users
```

**HTTP Method**

`PUT`

**Response Type**

| Field | Data Type | Options |
|---    | --- | --- |
| `inum` | String | |
| `iname` | String  | |
| `surName` | String | | 
| `givenName` | String | | 
| `email` | String | | 
| `password` | String | | 
| `userName` | String | | 
| `displayName` | String | | 
| `creationDate` | Date | | 
| `status` | String | <ul> <li> `active` </li> <li> `inactive` </li> <li> `expired` </li> <li> `register` </li> </ul>|

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Body | | `GluuPersonApi(GluuPersonApi)` |

-----

### updateOxauthJsonSetting

**URL**

```
//api/v1/configuration/oxauth/settings
```

**HTTP Method**

`PUT`

**Response Type**

oxAuthJsonConfiguration

| Field | Data Type |
|---    | --- |
| `issuer` | String | 
| `baseEndpoint` | String |
| `authorizationEndpoint` | String | 
| `tokenEndpoint` | String |
| `tokenRevocationEndpoint` | String | 
| `userInfoEndpoint` | String |
| `clientInfoEndpoint` | String | 
| `checkSessionIFrame` | String |
| `endSessionEndpoint` | String | 
| `jwksUri` | String |
| `registrationEndpoint` | String |
| `openIdDiscoveryEndpoint` | String | 
| `openIdConfigurationEndpoint` | String | 
| `idGenerationEndpoint` | String | 
| `introspectionEndpoint` | String |
| `umaConfigurationEndpoint` | String | 
| `sectorIdentifierEndpoint` | String |
| `oxElevenGenerateKeyEndpoint` | String | 
| `oxElevenSignEndpoint` | String |
| `oxElevenVerifySignatureEndpoint` | String | 
| `oxElevenDeleteKeyEndpoint` | String | 
| `oxElevenJwksEndpoint` | String | 
| `openidSubAttribute` | String |
| `responseTypesSupported` | List | 
| `grantTypesSupported` | List |
| `subjectTypesSupported` | List | 
| `defaultSubjectType` | String |
| `userInfoSigningAlgValuesSupported` | List | 
| `userInfoEncryptionAlgValuesSupported` | List |
| `userInfoEncryptionEncValuesSupported` | List | 
| `idTokenSigningAlgValuesSupported` | List |
| `idTokenEncryptionAlgValuesSupported` | List |
| `idTokenEncryptionEncValuesSupported` | List |
| `requestObjectSigningAlgValuesSupported` | List | 
| `requestObjectEncryptionAlgValuesSupported` | List |
| `requestObjectEncryptionEncValuesSupported` | List | 
| `tokenEndpointAuthMethodsSupported` | List |
| `tokenEndpointAuthSigningAlgValuesSupported` | List |
| `dynamicRegistrationCustomAttributes` | List |
| `displayValuesSupported` | List | 
| `claimTypesSupported` | List |
| `serviceDocumentation` | String |
| `claimsLocalesSupported` | List |
| `idTokenTokenBindingCnfValuesSupported` | List | 
| `uiLocalesSupported` | List |
| `dynamicGrantTypeDefault` | List |
| `claimsParameterSupported` | Boolean |
| `requestParameterSupported` | Boolean |
| `requestUriParameterSupported` | Boolean | 
| `requireRequestUriRegistration` | Boolean |
| `allowPostLogoutRedirectWithoutValidation` | Boolean |
| `introspectionAccessTokenMustHaveUmaProtectionScope` | Boolean | 
| `opPolicyUri` | String | 
| `opTosUri` | String |
| `authorizationCodeLifetime` | Integer | 
| `refreshTokenLifetime` | Integer | 
| `idTokenLifetime` | Integer |
| `accessTokenLifetime` | Integer | 
| `umaResourceLifetime` | Integer | 
| `sessionAsJwt` | Boolean | 
| `umaRptLifetime` | Integer |
| `umaTicketLifetime` | Integer | 
| `umaPctLifetime` | Integer |
| `umaAddScopesAutomatically` | Boolean | 
| `umaValidateClaimToken` | Boolean | 
| `umaGrantAccessIfNoPolicies` | Boolean |
| `umaRestrictResourceToAssociatedClient` | Boolean |
| `umaKeepClientDuringResourceSetRegistration` | Boolean | 
| `umaRptAsJwt` | Boolean |
| `cleanServiceInterval` | Integer |
| `keyRegenerationEnabled` | Boolean | 
| `keyRegenerationInterval` | Integer |
| `defaultSignatureAlgorithm` | String | 
| `oxOpenIdConnectVersion` | String | 
| `organizationInum` | String | 
| `oxId` | String |
| `dynamicRegistrationEnabled` | Boolean | 
| `dynamicRegistrationExpirationTime` | Integer |
| `dynamicRegistrationPersistClientAuthorizations` | Boolean | 
| `trustedClientEnabled` | Boolean |
| `skipAuthorizationForOpenIdScopeAndPairwiseId` | Boolean | 
| `dynamicRegistrationScopesParamEnabled` | Boolean |
| `dynamicRegistrationCustomObjectClass` | String | 
| `personCustomObjectClassList` | List | 
| `persistIdTokenInLdap` | Boolean |
| `persistRefreshTokenInLdap` | Boolean | 
| `authenticationFiltersEnabled` | Boolean |
| `invalidateSessionCookiesAfterAuthorizationFlow` | Boolean | 
| `clientAuthenticationFiltersEnabled` | Boolean | 
| `authenticationFilters` | List |
| `clientAuthenticationFilters` | List | 
| `configurationInum` | String | 
| `sessionIdUnusedLifetime` | Integer |
| `sessionIdUnauthenticatedUnusedLifetime` | Integer | 
| `sessionIdEnabled` | Boolean |
| `sessionIdPersistOnPromptNone` | Boolean | 
| `sessionIdLifetime` | Integer |
| `configurationUpdateInterval` | Integer | 
| `cssLocation` | String | 
| `jsLocation` | String |
| `imgLocation` | String | 
| `metricReporterInterval` |  Integer |
| `metricReporterKeepDataDays` | Integer | 
| `pairwiseIdType` | String |
| `pairwiseCalculationKey` | String | 
| `pairwiseCalculationSalt` | String |
| `shareSubjectIdBetweenClientsWithSameSectorId` | Boolean | 
| `webKeysStorage` | String | 
| `dnName` | String |
| `keyStoreFile` | String | 
| `keyStoreSecret` | String |
| `endSessionWithAccessToken` | Boolean | 
| `clientWhiteList` | List | 
| `clientBlackList` | List | 
| `legacyIdTokenClaims` | Boolean |
| `customHeadersWithAuthorizationResponse` | Boolean |
| `frontChannelLogoutSessionSupported` | Boolean | 
| `updateUserLastLogonTime` | Boolean | 
| `updateClientAccessTime` | Boolean |
| `enableClientGrantTypeUpdate` | Boolean | 
| `corsConfigurationFilters` | List |
| `logClientIdOnClientAuthentication` | Boolean  |
| `logClientNameOnClientAuthentication` | Boolean | 
| `httpLoggingEnabled` | Boolean | 
| `httpLoggingExludePaths` | List |
| `externalLoggerConfiguration` | String |
| `authorizationRequestCustomAllowedParameters` | List | 
| `legacyDynamicRegistrationScopeParam` | Boolean |
| `openidScopeBackwardCompatibility` | Boolean |
| `useCacheForAllImplicitFlowObjects` | Boolean | 
| `disableU2fEndpoint` | Boolean | 
| `authenticationProtectionConfiguration` | `AuthenticationProtectionConfiguration` | 
| `fido2Configuration` | Fido2Configuration | 
| `loggingLevel` | String | 
| `errorHandlingMethod` | String |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Body | | `OxAuthJsonConfiguration(OxAuthJsonConfiguration)` |

-----

### updateOxtrustJsonSetting

**URL**

```
//api/v1/configuration/oxtrust/settings
```

**HTTP Method**

`PUT`

**Response Type**

OxTrustJsonSetting

| Field | Data Type |
|---    | --- |
| `orgName` | String | 
| `supportEmail` | String | 
| `scimTestMode` | Boolean |
| `authenticationRecaptchaEnabled` | Boolean | 
| `enforceEmailUniqueness` | Boolean |
| `loggingLevel` | String |
| `passwordResetRequestExpirationTime` | Integer |
| `cleanServiceInterval` | Integer |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Body | | `OxTrustJsonSetting(OxTrustJsonSetting)` |

-----

### updateOxtrustSetting

**URL**

```
//api/v1/configuration/settings
```

**HTTP Method**

`PUT`

**Response Type**

OxtrustSetting

| Field | Data Type |
|---    | --- |
| `allowPasswordReset` | String | 
| `enablePassport `| String | 
| `enableScim` | String |
| `allowProfileManagement` | String |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Body | | `OxtrustSetting(OxtrustSetting)` |

-----

### updatePassportBasicConfig

**URL**

```
//api/v1/passport/config
```

**HTTP Method**

`PUT`

**Response Type**

String

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Body | | `Configuration(Configuration)` |

-----

### updatePassportProvider

**URL**

```
//api/v1/passport/providers
```

**HTTP Method**

`PUT`

**Response Type**

Provider

| Field | Data Type |
|---    | --- |
| `id` | String | 
| `displayName` | String | 
| `type` | String | 
| `mapping` | String | 
| `passportStrategyId` | String | 
| `enabled` | Boolean | 
| `callbackUrl` | String | 
| `requestForEmail` | Boolean | 
| `emailLinkingSafe` | Boolean | 
| `passportAuthnParams` | String | 
| `options` | Map | 
| `logo_img` | String |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Body | | Provider(Provider) |

-----

### updateRadiusClient

**URL**

```
//api/v1/radius/clients
```

**HTTP Method**

`PUT`

**Response Type**

RadiusClient

| Field | Data Type |
|---    | --- |
| `dn` | String | 
| `inum` | String | 
| `name` | String | 
| `ipAddress` | String | 
| `secret` | String | 
| `priority` | Integer |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Body | | `RadiusClient(RadiusClient)`

-----

### updateScope

**URL**

```
//api/v1/scopes
```

**HTTP Method**

`PUT`

**Response Type**

Scope

| Field | Data Type | Options |
|---    | --- | --- |
| `dn` | String | | 
| `inum` | String | | 
| `displayName` | String | | 
| `id` | String | | 
| `iconUrl` | String | | 
| `description` | String | | 
| `scopeType` | String | <ul> <li> `openid` </li> <li> `dynamic` </li> <li> `uma` </li> <li> `oauth` </li> </ul> |
| `oxAuthClaims` | List | | 
| `defaultScope` | Boolean | | 
| `oxAuthGroupClaims` | Boolean | | 
| `dynamicScopeScripts` | List | | 
| `umaAuthorizationPolicies` | List | | 
| `umaType` | Boolean | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Body | | `Scope(Scope)` |

-----

### updateSectorIdentifier

**URL**

```
//api/v1/sectoridentifiers
```

**HTTP Method**

`PUT`

**Response Type**

OxAuthSectorIdentifier


| Field | Data Type |
|---    | --- |
| `dn` | String | 
| `selected` | Boolean | 
| `id` | String | 
| `description` | String | 
| `redirectUris` | List | 
| `clientIds` | List | 
| `loginUri` | String | 
| `baseDn` | String | 

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Body | | `OxAuthSectorIdentifier(OxAuthSectorIdentifier)` |

-----

### updateServerConfiguration

**URL**

```
//api/v1/radius/settings
```

**HTTP Method**

`PUT`

**Response Type**

ServerConfiguration

| Field | Data Type |
|---    | --- |
| `dn` | String | 
| `listenInterface` | String | 
| `authPort` | Integer | 
| `acctPort` | Integer | 
| `openidUsername` | String | 
| `openidPassword` | String | 
| `openidBaseUrl` | String | 
| `acrValue` | String | 
| `scopes` | List | 
| `authenticationTimeout` | Integer | 

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Body | | `ServerConfiguration(ServerConfiguration)` |

-----

### updateSmtpConfiguration

**URL**

```
//api/v1/configuration/smtp
```

**HTTP Method**

`PUT`

**Response Type**

SmtpConfiguration

| Field | Data Type |
|---    | --- |
| `valid` | Boolean | 
| `host` | String | 
| `port` | Integer | 
| `requires-ssl` | Boolean | 
| `trust-host` | Boolean |
| `from-name` | String | 
| `from-email-address` | String |
| `requires-authentication` | Boolean | 
| `user-name` | String |
| `password` | String | 

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Body | | `SmtpConfiguration(SmtpConfiguration)` |

-----

### updateUmaResource

**URL**

```
//api/v1/uma/resources
```

**HTTP Method**

`PUT`

**Response Type**

UmaResource

| Field | Data Type |
|---    | --- |
| `dn` | String | 
| `inum` | String | 
| `id` | String | 
| `name` | String | 
| `iconUri` | String | 
| `scopes` | List | 
| `scopeExpression` | String | 
| `clients` | List | 
| `resources` | List | 
| `rev` | String | 
| `creator` | String | 
| `description` | String | 
| `type` | String | 
| `creationDate` | Date | 
| `expirationDate` | Date | 
| `deletable` | Boolean |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Body | | `UmaResource(UmaResource)` |

-----

### updateUmaScope

**URL**

```
//api/v1/uma/scopes
```

**HTTP Method**

`PUT`

**Response Type**

Scope

| Field | Data Type | Options |
|---    | --- | --- |
| `dn` | String | | 
| `inum` | String | | 
| `displayName` | String | | 
| `id` | String | | 
| `iconUrl` | String | | 
| `description` | String | | 
| `scopeType` | String | <ul> <li> `openid` </li> <li> `dynamic` </li> <li> `uma` </li> <li> `oauth` </li> </ul> |
| `oxAuthClaims` | List | | 
| `defaultScope` | Boolean | | 
| `oxAuthGroupClaims` | Boolean | | 
| `dynamicScopeScripts` | List | | 
| `umaAuthorizationPolicies` | List | | 
| `umaType` | Boolean | |

**Parameters**

| Location | Parameter Name | Input |
| --- | --- | --- |
| Body | | `Scope(Scope)` |

## License

Gluu oxTrust APIs are made available under the [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0).
