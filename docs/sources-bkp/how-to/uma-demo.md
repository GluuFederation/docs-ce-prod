# Configure UMA Demo
This section will guide you through to configuring UMA demo in Gluu Server. The values will change accrding you your setup.
There are three things that needs to be ensured while configuring UMA:

1. Configurations are loaded from `<TOMCAT_HOME>/conf` directory

2. Deploy Requesting Party (RP) to `/opt/tomcat/webapps/rp` folder in the Gluu Server `chroot` environment

3. Deploy Resource Server (RS) to `/opt/tomcat/webapps/rs` folder in the Gluu Server `chroot` environment

## UMA Discovery
The UMA discovery URL or the UMA well known endpoint is located at `https://<hostname.doman>/.well-known/uma-configuration`.
This link for any IdP or UMA-enabled IdP will contain the UMA discovery information such as token endpoints and authorization endpoints.

**Note:** It is possible to register the client using [OpenID Connect Dynamic Client Registration](http://openid.net/specs/openid-connect-registration-1_0.html).

|Parameter|Description|
|---------|-----------|
|umaAatClientId<br/>umaAatClientSecret|Client Credentials for AAT|
|pat_client_id<br/> pat_client_secret|Client Credentials for PAT|
|rsPhoneWsUrl|Hard coded Resource Server endpoint|

## Resource Server Configuration
Please remember to populate the follwoing files

|Filename|Mandatory|Requirements|
|--------|-----------|----------|
|rs-protect.json|Yes|PAT Client Credentials|
|rs-protect-config.json|No|Populate if WS endpoints were changed|

### Add Client

* Click on the Clients Menu from oxTrust GUI

![image](../img/2.4/admin_oauth2_clientmenu.png)

* Click on the Add Client button

![image](../img/oxTrust/admin_oauth2_addclient.png)

* The following screen will appear and you have to fill it up with the information given below

![image](../img/oxTrust/admin_oauth2_newclient.png)

  1. Name : oxUma Demo RS (or any other name you like)

  2. Application type : web

  3. Authentication method for the Token Endpoint: client_secret_basic

  4. Redirect Login URIs: `<rs redirect uri>` eg https://gluuserver.mylifedigital/rs/rs.html (in our demo it is https://kantara.gluu.org/rs/rs.html)

  5. Scopes: openID and uma_protection (uma_protection indicates that it is PAT)

  6. Response types: token code id_token

* Populate the `rs-protect.json` file with the secret that was used in the form

## Requesting Party Configuration
### Register Client

* Click on the Clients Menu from oxTrust GUI

![image](../img/2.4/admin_oauth2_clientmenu.png)

* Click on the Add Client button

![image](../img/oxTrust/admin_oauth2_addclient.png)

* The following screen will appear and you have to fill it up with the information given below

![image](../img/oxTrust/admin_oauth2_newclient.png)

  1. Name : oxUma Demo RS (or any other name you like)

  2. Application type : web

  3. Authentication method for the Token Endpoint: client_secret_basic

  4. Redirect Login URIs: `<rp redirect uri>` eg https://gluuserver.mylifedigital/rp/rp.html (in our demo it is https://kantara.gluu.org/rs/rs.html)
  5. Scopes: openID and uma_authorization (uma_authorization indicates that it is AAT) 

* Populate the `oxuma-rp-conf.json` with the client ID and secret that was used in the form

#### Restart Tomcat
Please remember to restart tomcat using the following command after the changes are made:

`# service tomcat restart`
