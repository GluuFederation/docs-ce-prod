# Inbound SAML using Passport.js 
## Overivew

The Gluu Server uses the [SAML IDP MultiAuthn interception script](https://github.com/GluuFederation/oxAuth/blob/evolveip/Server/integrations/idp/IdpMultiAuthnExternalAuthenticator.py) to enable inbound SAML single sign-on with Passport.js.

Post-authentication, the script uses just-in-time provisioning to add users to the Gluu LDAP server if a local account does not already exist. In this way, the Gluu SAML and OpenID Connect providers can gather claims and maintain SSO as normal.

!!! Note
    Passport is an Express-based web application. We've modified it to call oxTrust APIs for its non-static configuration. Because its configuration is stored centrally in LDAP, you can scale Passport even in clustered topologies.

### Prerequisites
- A Gluu Server with Passport.js installed during setup ([Installation Instructions](https://github.com/GluuFederation/gluu-passport#setup-passportjs-with-gluu));
- [IDP MultiAuthn interception script](https://github.com/GluuFederation/oxAuth/blob/evolveip/Server/integrations/idp/IdpMultiAuthnExternalAuthenticator.py).

### Sequence Diagram

Below is a sequence diagram to help clarify the workflow for user authentication and provisioning. 

![Sequence Diagram](sequence-diagram.png "Title")

1. User-Agent calls gluu for Authentication with provided IDP name as base64 encoded json in state param like state=`base64({"salt":"<SALTVALUE>",provider":"<idp_name>"})`;        
2. Gluu Sever multiauthn script checks the IDP name;    
3. Gluu server calls Node-Passport server for a JWT token;       
4. Node-Passport server generates a JWT token and provides it in response to Gluu server;      
5. Gluu Server multiauthn script prepares the URL for passport server with provided IDP;    
6. Gluu server make a request to the Node-Passport server with the JWT token to authenticate the user for IDP provider;    
7. Node-Passport server redirects the user to the external IDP provider;    
8. After successful user authentication, the IDP will callback the Node-Passport server along with user details and access token;   
9. Node-Passport server will redirect back to Gluu Server with the user details and access token;      
10. The multiauthn interception script will check if the user exists in Gluu's OpenLDAP server.         
	a. If the user exists then the user will be logged into the system.       
	b. If the user does not exist, the interception script will create a new user with the required details in the Gluu OpenLDAP and log the user into the system.    



### How to configure Gluu server for Inbound single sign-on

During installation of the Gluu Server select `yes` to install Passport.js when prompted.

1. Navigate to `Configuration` > `Manage Custom Scripts`.
1. Enable Passport script in `Person Authentication` tab. ![Enable passport](https://github.com/GluuFederation/gluu-passport/blob/master/img/passport/enable-passport.png)
    1. We need to update existing script with [IDP MultiAuthn interception script](https://github.com/GluuFederation/oxAuth/blob/evolveip/Server/integrations/idp/IdpMultiAuthnExternalAuthenticator.py). so open link and copy script and replace passport script with script in the link. If you do not want to replace current script and add new one You can do That as well.For that you can add passport-inboundSAML as new strategy using oxTrust.Follow this link for details [link](https://github.com/GluuFederation/Inbound-SAML-Demo/wiki/Steps-for-creating--SAML_IDP_MultiAuthn_interception_script).
1. Click on `update` at the end of the page.![update](https://github.com/GluuFederation/gluu-passport/blob/master/img/passport/auth-update.png)
1. To set the strategies navigate to `Configuration` > `Manage Authentication` > `Default Authenticaion`
1. Click on `Passport Authentication Method` tab and `Passport Support` to enabled.![enable-authentication](https://github.com/GluuFederation/gluu-passport/blob/master/img/passport/enable-authentication.png)
1. Add configuration json file `passport-saml-config.json` containing IDP information in `/etc/gluu/conf`
1. Once the configuration and settings have been entered, restart the passport service or Gluu Server by following the below instructions:
    
    a. Login to chroot.
    
    b. Enter the following command to stop: `service passport stop`
    
    c. Enter the following command to start: `service passport start`

!!! Warning
	Strategies names and field names are case sensitive.


### How to configure Passport Server Configurations
**You can do passport server configuration either with setup script(beta) or do it your self manually**

#### 1. Configurations with setup script
_Steps to use setup scripts_ 
1) Download or clone [Github repo](https://github.com/GluuFederation/Inbound-SAML-Demo)
1) Copy setup-script directory/folder in side gluu server's chroot.(command will be like this `cp -a <path to downloaded repo>/setup-script /opt/gluu-server-3.1.1/root/
`)
1) Login to gluu-server's chroot with command (` service gluu-server-3.1.1 login`)
1) Navigte inside setup-script directory (`cd setup-script`)
1) Run **`passport-setup.py`**(`./passport-setup.py`) it will may take some time depend on you internet speed and machine configurations because script also run commands like `npm install`.
1) That's it (Follow console intsruction to restart passport and oxauth server or simply just restart gluu server) 
1) You might require to run `chmod 777 -R /opt/gluu/node/passport/` after runnig this script to reset the file permissions 

####  2. Configurations manually 
For saml based authentication with passport. We need to enable saml by following steps:

```sh 
su - node
export PATH=$PATH:/opt/node/bin
cd /opt/gluu/node/passport
npm install passport-saml --save

```
		
In file /opt/gluu/node/passport/server/app.js add configs for saml.
```javascript

global.saml_config = require('/etc/gluu/conf/passport-saml-config.json')
```

In file /opt/gluu/node/passport/server/routes/index.js add the route for saml.

```javascript
var passportSAML = require('../auth/saml').passport;
var fs = require('fs');
```

```javascript
//===================saml ==================== 
    var entitiesJSON = global.saml_config;
for (key in entitiesJSON) {
    //with out cert param in saml_config it will not work
    if (entitiesJSON[key].cert && entitiesJSON[key].cert.length > 5) {
        router.post('/auth/saml/' + key + '/callback',
            passportSAML.authenticate(key, {
                failureRedirect: '/passport/login'
            }),
            callbackResponse);

        router.get('/auth/saml/' + key + '/:token',
            validateToken,
            passportSAML.authenticate(key));
    }
    else {
        router.get('/auth/saml/' + key + '/:token',
            validateToken,
            function (req, res) {
            err = {
              message:"cert param is required to validate signature of saml assertions response"
            };
                logger.log('error', 'Cert Error: ' + JSON.stringify(err));
                logger.sendMQMessage('Cert Error: ' + JSON.stringify(err));
                res.status(400).send("Internal Error");
            });
    }
}

```

Exposing metadata through global url

```javascript
router.get('/auth/meta/idp/:idp',
    function (req, res) {
        var idp = req.params.idp;
        logger.info(idp);
        fs.readFile(__dirname + '/../idp-metadata/' + idp + '.xml', (e, data) => {
            if (e)
                res.status(404).send("Internal Error");
            else
                res.status(200).set('Content-Type', 'text/xml').send(String(data));
        });
    });

```

In file /opt/gluu/node/passport/server/auth/configureStrategies.js add the support for saml strategy.

```javascript
var SamlStrategy = require('./saml');
```

```javascript
  //add this line in 
  SamlStrategy.setCredentials();
```

Put saml strategy file name `saml.js` from gluu-passport [repo](https://github.com/GluuFederation/gluu-passport/blob/version_3.1.1/server/auth/saml.js) on path `/opt/gluu/node/passport/server/auth/`


**Important fix**
next we need to cutomise passportpostlogin.xml to use this project with 3.1.1 this will be fix in next version of gluu
> copy [passportpostlogin.xhtml](https://github.com/GluuFederation/oxAuth/blob/evolveip/Server/src/main/webapp/auth/passport/passportpostlogin.xhtml) from link and paste to `opt/gluu/jetty/oxauth/custom/pages/auth/passport` (you need to create missing directories(/auth/passport))


Now restart passport service. 

```sh 
service passport stop
service passport start
```

##### Note :- _we recommends you to use  manual step to configure your passport server instead of step if you have done modification to your passport server because script will override your changes and replace with fresh codes._  


## Onboarding new IDP's.

Add new IDP Configuration in /etc/gluu/conf/passport-saml-config.json file. A sample of IDP Configuration is given below:

```json
{"idp1": {"entryPoint": "https://dev1.gluu.org/idp/profile/SAML2/POST/SSO",
                "issuer": "urn:test:example",
                "identifierFormat": "urn:oasis:names:tc:SAML:2.0:nameid-format:transient",
                "authnRequestBinding": "HTTP-POST",
                "additionalAuthorizeParams": "<Some additinal params json>",
                "skipRequestCompression": "true",
                "cert":"MIIDbDCCAlQCCQCuwqx2PNP...........YsMw==",//single line with out space and \n (importatnt)
                "reverseMapping": {
                        "email" : "email",
                        "username": "urn:oid:0.9.2342.19200300.100.1.1",
                        "displayName": "urn:oid:2.16.840.1.113730.3.1.241",
                        "id":  "urn:oid:0.9.2342.19200300.100.1.1",
                        "name": "urn:oid:2.5.4.42",
                        "givenName": "urn:oid:2.5.4.42",
                        "familyName": "urn:oid:2.5.4.4",
                        "provider" :"issuer"
                }
        }
}
```

In above snippet replace "idp1" with the name of IDP for which IDP configuration needed to be added. It has following keys:
		
		- `entryPoint` is mandatory field which is identity provider entry point is the address to authenticate through SAML SSO. 
		- `issuer` is mandatory field which is issuer string supply to identity provider.
		- `identifierFormat` if true, name identifier format to request from identity provider.
		- `authnRequestBinding` if set to HTTP-POST, will request authentication from IDP via HTTP POST binding, otherwise defaults to HTTP Redirect.
		- `additionalAuthorizeParams` dictionary of additional query params to add to 'authorize' requests.
		- `skipRequestCompression` if set to true, the SAML request from the service provider won't be compressed.
		- `cert` Identity Provider's public PEM-encoded X.509 certificate with  The `BEGIN CERTIFICATE` and `END CERTIFICATE` lines should be stripped out and the certificate should be provided on a single line.All \n must be removed from string.
		- `reverseMapping` is IDP representation of user fields
		- `email` is the user email
		- `username` is username of user
		- `displayName` is Display Name of user
		- `id` is userid for user.
		- `name` is full name of user
		- `givenName` is first name of user
		- `familyName` is last name of user

##### note :- If you have used Script for setup. passport-saml-config.jsonjson file will be created by script for you just need to modify as per your configurations
		
## How to use 

### Instructions 

>We are going to follow [sequence diagram](https://github.com/GluuFederation/Inbound-SAML-Demo/wiki/Readme_single#sequence-diagram) to use this project

### Steps
1) We need OpenID connect client to send Authentication request to interception script.
    1) We assueme that you know how to create openid connect client in gluu server. For more details you can follow this [Client registration Doc](https://gluu.org/docs/ce/admin-guide/openid-connect/#client-registration-configuration).
    1) If you have not create new separate strategy,In your created client set `passport` as `arc_value`  or if you have created separate script than set `acr_value` as according to it. If you have followed [link](https://github.com/GluuFederation/Inbound-SAML-Demo/wiki/Steps-for-creating--SAML_IDP_MultiAuthn_interception_script) and created strategy with name `passportsaml` your acr_value will be **passportsaml**.
    1) set redirect_uri as per your project requirements.

1) Now we will use this client craeted in step 1 for Authentication requests.
    1) We need to call standard gluu GET Authentication request using created clientID and acr_value.
    1) Follow [GLuu openid-connect-api](https://gluu.org/docs/ce/api-guide/openid-connect-api/#requestauthorizationget)to create authentication request
    1) Additionally we need to add state and nonce as query params with created  authentication request.
    1) state -> base64 of json {"salt":"<salt_value>","provider":"<idp_name>"}.    
    1) Nonce -> String value used to associate a Client session with an ID Token, and to mitigate replay attacks. The value is passed through unmodified from the Authorization Request to the ID Token. Sufficient entropy MUST be present in the nonce values used to prevent attackers from guessing values.
    ```java
      //Example for generating getAuthentication request in java
    
   
        import com.google.common.collect.Lists;
        import org.xdi.oxauth.client.AuthorizationRequest;
        import org.xdi.oxauth.model.common.ResponseType;
        
        import java.util.Random;
        
        public class OpenIdGenerator {
        
            static String clientid = "your_client_id";
            static String redirect_uri = "redirect_uril";
            static String host = "your_glue host";
            static String acr_valur = "acr_value";
        
        
            public static void main(String[] args) throws Exception {
                String nounce = String.valueOf(randInt(100000000, 999999999));
                AuthorizationRequest authorizationRequest = new AuthorizationRequest(Lists.newArrayList(ResponseType.CODE, ResponseType.ID_TOKEN)
                        , clientid
                        , Lists.newArrayList("openid", "profile")
                        , redirect_uri, String.valueOf(randInt(100000000, 999999999)));
                authorizationRequest.setRedirectUri(redirect_uri);
                authorizationRequest.setState("You state value"); //base64 of json {"salt":"<salt_value>","provider":"<idp_name>"}
                authorizationRequest.setAcrValues(Lists.newArrayList(acr_valur));
                String queryString = "https://" + host + "/oxauth/authorize?" + authorizationRequest.getQueryString();
                System.out.println(queryString);
            }
        
            public static int randInt(int min, int max) {
        
                // Usually this can be a field rather than a method variable
                Random rand = new Random();
        
                // nextInt is normally exclusive of the top value,
                // so add 1 to make it inclusive
                int randomNum = rand.nextInt((max - min) + 1) + min;
        
                return randomNum;
            }
        }
     
     //output will be like this :- https://gluu.evp.org/oxauth/authorize?response_type=code+id_token&client_id=%40%215C0B.B148.7E63.326C%210001%21562E.F01E%210008%21664D.7760.0EC3.762D&scope=openid+profile&redirect_uri=https%3A%2F%2Flocalhost%3A8080&state=eyJwcm92aWRlciI6ImlkcDEifQ%3D%3D&nonce=232334315&acr_values=passportsaml
    ```
1) open generated links will lead your application for `SAML IDP MultiAuthentiocation` flow. 

## Demo project(proxy-client)


* Proxy-client is the demo application in node.js to test Passport Inbound SSO


>It is very easy to run. You just require latest node-js installed on your machine 


#### Steps

1. Clone [project](https://github.com/GluuFederation/Inbound-SAML-Demo) using git clone 
1. Register new OIDC client in your gluu server with redirect uri _http://localhost:3000/profile_ and copy clientID and secrete.
1. open **client-config.json** and file details like openid ClientID clinetSecret and hostname
1. copy same **passport-saml-config.json** which you used in setting up [**Passport Inbound SSO**](https://github.com/GluuFederation/Inbound-SAML-Demo/wiki/Readme_single#onboarding-new-idps) 
1. open terminal navigate to project directory
1. execute following commands 
    1. `npm install`
    1.  `node server.js`
1. That's it to open de mo ,hit http:localhost:3000 in browser and click on button with idp name to test your configuration. It will redirects you to your configured idp using SAML SSO for login page.![demo_screenshot1](https://github.com/GluuFederation/Inbound-SAML-Demo/blob/master/images/demo_1.png)

1. After login, you might ask to allow permission to access your personal data.
![demo_screenshot2](https://github.com/GluuFederation/Inbound-SAML-Demo/blob/master/images/demo_2.png)

1. On allowing from Authorization page Server will redirect to Prox-client (Demo application) with Query params like  `...../profile/response_type=code&scope=openid&client_id=s6BhdRkqt3&state=af0ifjsldkj&redirect_uri=https%3A%2F%2Fclient.example.og%2Fcb`

1. using Information from query params of rerdirect uri demo Application will fetch the user information and display it on profile page![demo_screenshot3](https://github.com/GluuFederation/Inbound-SAML-Demo/blob/master/images/demo_3.png)


