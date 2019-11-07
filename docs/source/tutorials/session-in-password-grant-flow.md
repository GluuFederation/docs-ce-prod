# Session and Custom parameters and claims in `password` grant flow 

## Overview

This tutorial offers a step-by-step guide for setting up a basic proof-of-concept environment showcasing an creation SSO cookie in `password` grant flow. Refer to general documentation describing each component for more details.

## Testing

1. Install CE 4.0.1
2. Log into oxTrust admin GUI
3. Enable `resource_owner_password_credentials_custom_params_example` Resource Owner Password Credentials script
4. Enable `introspection_custom_params` 	Introspection script
5. Register OpenId client with `password` grant type.
6. Register OpenId client with next parameters:
   - Uncheck Persist Client Authorizations for demo purposes
   - Grant Types = `authorization_code`
   - Scopes = `openid user_name profile address`
   - Response Types = `code`
   - Redirect Login URIs = `http://localhost:8080/login/oauth2/code/oxauth`
   - Post Logout Redirect URIs = `http://localhost:8080`
7. Prepare and run demo  RP
   - Clone or download `https://github.com/GluuFederation/oxAuth` code from stable branch like `version_4.0.1`
   - Update RP demo application configuration in `./oxAuth/rp-spring-boot/src/main/resources/application.yml`
   - Specify `issuer-uri` CE server uri which was installed in step 1
   - Specify `client-id` and `client-secret` which were added in step 6
   - If CE server uses self signed cert next command should be executed to add certificate to java trust store
     - `echo |openssl s_client -connect <server>:443 2>&1 |sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' > cert.pem`
     - `keytool -import -alias ALIAS_OF_CERTIFICATE -keystore $PATH_TO_JAVA_HOME/jre/lib/security/cacerts -file cert.pem`
   - Run `mvn spring-boot:run` in `./oxAuth/rp-spring-boot` folder
   - Open in browser `http://localhost:8080`
   - Login/Logout to make sure that demo RP works well      
8. Issue code via `password` flow. For this step we need to use client_id/client_secret client added in step 5.
   - Get access token:
   
curl -k -u '<client_id>:<client_secret>' \
 -d "grant_type=password" \
 -d "username=admin" \
 -d "password=pwd" \
 -d "custom1=custom_value_1" \
 -d "custom2=custom_value_2" \
 https://<server>/oxauth/restv1/token

   - Get response like this:

`{"access_token":"cfdffde5-d615-4d64-afaa-f43ef7e3d932","token_type":"bearer","expires_in":299}`

   - Request access_token introspection

curl -k -H 'Authorization: Bearer <access_token>' -d "token=<access_token>" https://<server>/oxauth/restv1/introspection

   - Get response like this:
`{"sub":"","iss":"https://u184.gluu.info","active":true,"session_id":"f7881b6c-de46-45bd-9c38-955eacdcaf0a","token_type":"bearer","client_id":"91655c64-ca2d-458f-9b0a-e3a8b2afb76d","aud":"91655c64-ca2d-458f-9b0a-e3a8b2afb76d","user_id":"admin","scope":[],"acr_values":"simple_password_auth","custom1":"custom_value_1","custom2":"custom_value_2","exp":1573125769,"iat":1573125469,"jti":null,"username":"Default Admin User"}`

   - Find in response `session_id` claim
   - Open browser and add cookie for `<server>` with next values:
     - Name: session_id
     - Path: /
     - Value: <session_id> from previous step
     - Secure: true
     - HttpOnly: true
