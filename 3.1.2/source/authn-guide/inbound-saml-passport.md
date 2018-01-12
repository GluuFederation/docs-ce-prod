# Inbound SAML using Passport.js 
## Overview

The Gluu Server can be configured to delegate user authentication to one or more external SAML IDPs. 

If only one external SAML IDP needs to be supported, i.e. a one-off integration, follow the [SAML interception script](https://github.com/GluuFederation/oxAuth/tree/evolveip/Server/integrations/saml) instructions. 

If many external IDPs need to be supported, follow the instructions below. 

!!! Note
    Previous versions of Gluu relied on the Asimba SAML proxy to achieve inbound SAML. Asimba docs can be found [here](https://github.com/GluuFederation/docs-ce-prod/blob/3.1.1/3.1.1/source/authn-guide/inbound-saml-asimba.md). 

### About Passport  
Passport is an MIT licensed Express-based web application. We've modified it to call oxTrust APIs for its non-static configuration. Because its configuration is stored centrally in LDAP, you can scale Passport even in clustered topologies.

### User Provisioning
After authentication at an external IDP, both strategies mentioned above support just-in-time (JIT) user provisioning if there is no existing user record in Gluu. Once user information (attributes/claims) is obtained, it can be used by Gluu for SSO to applications.

## Prerequisites
- Gluu Server CE 3.1.2 with Passport.js   

## Instructions 
The general steps for configuring Gluu Server for inbound SAML scenario using Passport.js are as follows:

1. [Enable interception script](#enable-interception-script)
1. [Deploy custom login pages](#deploy-custom-login-pages)
1. [Configure trust relationships with external IDP(s)](#configure-trust-relationships-with-external-idps)
1. [Testing the resulting setup](#testing-the-resulting-setup)
1. [Implement discovery ("WAYF")](#implement-discovery-wayf)
1. [Troubleshooting tooltips](#troubleshooting-tooltips)

## Enable interception script

Make sure you have deployed Passport.js during installation of your Gluu Server. 

Then follow the next steps:

1. Navigate to `Configuration` > `Manage Custom Scripts` > `Person Authentication`
1. Find t
    
1. Update the existing content in the Script field with the [IDP MultiAuthn interception script](https://github.com/GluuFederation/oxAuth/blob/master/Server/integrations/passport/PassportExternalAuthenticator.py). 

1. Click on `update` at the end of the page.
![update](img/passport/auth-update.png)

1. Now navigate to `Configuration` > `Manage Authentication` > `Passport Authentication Method`

1. Select "Enabled" from `Passport Support` drop-down list;

![enable-authentication](img/passport/enable-authentication.png)

1. Once the configuration and settings have been entered, restart the passport service by following the below instructions:
    
    a. Login to chroot.
    
    b. Enter the following command to stop: `service passport stop`
    
    c. Enter the following command to start: `service passport start`

!!! Warning
    Strategies names and field names are case sensitive.
 
 
 ## Deploy custom login page(s)

Gluu includes default user-facing login pages for inbound authentication. The default login pages expose all supported external IDPs so that, when users are directed to the login page, they can select their home authentication provider. 

1. Acquire [the login page files](https://github.com/GluuFederation/oxAuth/tree/evolveip/Server/src/main/webapp/auth/passport) and add them in the `/opt/gluu/jetty/oxauth/custom/pages/auth/passport/` directory, creating an underlying directory structure as needed. Then set proper permissions for the new tree:
```
# yum -y install svn ("# apt-get install svn" for Debian/Ubuntu distros)
# mkdir -p /opt/gluu/jetty/oxauth/custom/pages/auth/
# cd /opt/gluu/jetty/oxauth/custom/pages/auth/
# svn checkout https://github.com/GluuFederation/oxAuth/branches/evolveip/Server/src/main/webapp/auth/passport
# rm -rf passport/.svn/
# chown -R jetty:jetty /opt/gluu/jetty/oxauth/custom/
```

2. Open the `/opt/gluu/jetty/oxauth/custom/pages/auth/passport/passportpostlogin.xhtml` file for editing and make sure that around line #48 it contains the following instructions:

```
var userObj = JSON.parse(userQueryString);
```
In case it contains next on instead
```
var userObj = JSON.parse(userQueryString.substring(0, userQueryString.indexOf('}') + 1));
```
..it needs to be edited accordingly.

In the same file, check instruction around line #53, and make sure it looks like
```
document.getElementById('loginForm')["loginForm:provider"].value = userObj.provider['_'];
```
..and **NOT** like
```
document.getElementById('loginForm')["loginForm:provider"].value = userObj.provider;
```

3. Restart `passport` and `oxauth` services: 

```sh 
# service passport restart
# service oxauth restart
```

## Configure trust relationships with External IDP(s)

### Register External IDP(s) with home IDP 
 
Some basic information is needed about the external IDPs. By default the script expects to find this configuration info in `/etc/gluu/conf/passport-saml-config.json`. Each supported external IDP is added as an embedded JSON object here. A sample IDP configuration is provided below. After edits are done to this file the `passport` service must be restarted for changes to be applied and new metadata to be generated:

```sh
# service passport restart
```

!!! Note
    In most cases, at this point the `passport-saml-config.json` file is already present in the container. Simply modify its configurations as needed. If manually creating the file, make sure the "node" user has permissions to access.

!!! Note
    Certificates used in this file must be in PEM (base64-encoded) format with "BEGIN" and "END" separators stripped, and must not contain any kind of line break characters (new line, carriage return, space etc)
    Next command may be used to transform an existing X.509, PEM-encoded certificate into text of required format: `# cat ~/your_cert.crt | grep -v '^---' | tr -d '\n'`

```json
{"idp1": {"entryPoint": "https://idp.example.com/idp/profile/SAML2/POST/SSO",
                "issuer": "urn:test:example",
                "identifierFormat": "urn:oasis:names:tc:SAML:2.0:nameid-format:transient",
                "authnRequestBinding": "HTTP-POST",
                "additionalAuthorizeParams": "<Some additinal params json>",
                "skipRequestCompression": "true",
                "logo_img":"{Provider Logo url #1}",
                "enable":"true",
                "cert":"MIIDbDCCAlQCCQCuwqx2PNP...........YsMw==",
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
        },
 "idp2":{"entryPoint": "https://idp2.example.com/idp/profile/SAML2/POST/SSO",
                        "issuer": "urn:test2:example",
                        "identifierFormat": "urn:oasis:names:tc:SAML:2.0:nameid-format:transient",
                        "authnRequestBinding": "HTTP-POST",
                        "additionalAuthorizeParams": "<Some additinal params json>",
                        "skipRequestCompression": "true",
                        "logo_img":"{Provider Logo url #1}",
                        "enable":"true",
                        "cert":"AVDVfsgsdafkmiaAFJiasdfmpaf...........YsMw==",
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
!!! Note
    All the given parameters are mandatory and must be included in the file; an empty string value can be used in cases when some of them are not required in a specific setup

Placeholder urls like `https://idp.example.com` must be replaced with the url of corresponding actual remote IDPs. Role of each property in the object is clarified below:
        
- `entryPoint` - IDP's entry point, an url of endpoint to which SAML request must be addressed
- `issuer` - string specifying `entityid` which Passport.js must use to represent itself in SAML requests sent to this IDP (thus it allows to use different `entityid` for each of registered IDPs, if needed)
- `identifierFormat` - name identifier's format to request from IDP
- `authnRequestBinding` - if set to "HTTP-POST", will request authentication from IDP via HTTP POST binding, otherwise defaults to HTTP Redirect.
- `additionalAuthorizeParams` - dictionary of additional query params to add to 'authorize' requests.
- `skipRequestCompression` - if set to "true", the SAML request from the service provider won't be compressed.
- `logo_img` - url pointing to logo this IDP should be represented with at Gluu's Passport login page.
- `enable` - if set to "true" this IDP is allowed to be used by users trying to become authenticated at this Gluu Server instance.
- `cert` - IDP's public PEM-encoded X.509 certificate with `BEGIN CERTIFICATE` and `END CERTIFICATE` tag lines stripped  and all line breaking characters ("\n", "\r") removed.
- `reverseMapping` - an embedded JSON object defining how SAML attributes' names show be mapped to attributes used internally by Passport.js server:
    - `email` is the user email
    - `username` is username (uid) of user
    - `displayName` is Display Name of user
    - `id` is userid of user.
    - `name` is full name of user
    - `givenName` is the first name of user
    - `familyName` is the last name of user


### Register SP with external IDPs

The Passport.js server generates SAML SP metadata for each IDP listed in the `passport-saml-config.json` file that can be used to register this SP at each remote IDP.

The metadata is published at the following url: `https://<hostname>/passport/auth/meta/idp/<IDP-id-from-passport-saml-config>`, and can also be found within the Gluu container at: `/opt/gluu/node/passport/server/idp-metadata`. This can be copied into a file and uploaded to the remote IDP.   

The actual process of creating this trust will differ depending on the IDP(s) in use. If the remote IDP is another Gluu Server, see the [SAML IDP documentation](https://gluu.org/docs/ce/3.1.2/admin-guide/saml/#create-a-trust-relationship) for required steps. 

!!! Note
    Passport.js server will generate metadata only when all required data is provided in `passport-saml-config.json`

!!! Note
    When registering Passport.js Server's SP at each remote IDP you must ensure that at least `username` and `email` attributes are released by it for each user


## Testing the resulting setup

A simple test of any Gluu Passport authentication scenario can be performed by composing and following an OpenID Connect authorization request url triggering a corresponding Gluu custom authentication script. The "Proxy-client" Demo app described below can help with testing.

Special composition of `state` url query parameter which can be used in authorization url allows OpenID Connect-enabled applications to be able to force Passport-SAML strategy to use a specific IDP for this user by pre-selecting it in advance.


### Testing the Demo app

`Proxy-client` is a demo node.js application to test the above documented Inbound SAML scenario. The project requires the latest version of node.js to be installed on the machine where the app will be running.

Steps to configure the demo app:

1. Download the [project's files](https://github.com/GluuFederation/Inbound-SAML-Demo) with `# git clone ttps://github.com/GluuFederation/Inbound-SAML-Demo`.    

2. Register a new OIDC client at your Gluu Server; next properties must be set as specified below:
    1. "Redirect login uri" contains `http://localhost:3000/profile/`
    2. "Grant types" contains `authorization_code` and `implicit`
    3. "Response types" contains `code` and `id_token`
    4. "Client secret" must not be empty

3. Edit `client-config.json` in the app's main directory and submit proper values for `ClientID` (`inum` attribute found among client's properties after it's registered at Gluu Server), `clientSecret`, and `hostname` (FQDN of your Gluu Server host)

4. Copy the `passport-saml-config.json` which you used when [registering external IdPs for Passport Inbound SSO](#register-external-idps-with-home-idp) into Demo app's main directory

5. In the console make sure Demo app's main directory is the current working directory, then execute following commands:     
    a. `# npm install`      
    b. `# node server.js`           

6. Using web browser of your choice navigate to `http://localhost:3000` and select one of the IDPs displayed on the page to initiate test flow. Eventually you should be redirected to the chosen IDP following the Inbound SAML flow
![demo_screenshot1](https://github.com/GluuFederation/Inbound-SAML-Demo/raw/master/images/demo_1.png)

7. After login at IDP of your choice you'll be redirected back at your Gluu Server instance where you might be asked to authorize the release of your personal data to the Demo app
![demo_screenshot2](https://github.com/GluuFederation/Inbound-SAML-Demo/raw/master/images/demo_2.png)

9. After giving your consent to release requested claims you'll be sent back to the Demo app with authorization code it needs to retrieve your personal data

10. Application will display claims retrieved using the code on its "/profile" page
![demo_screenshot3](https://github.com/GluuFederation/Inbound-SAML-Demo/raw/master/images/demo_3.png)
Video featuring the Demo app in action can be found [here](https://youtu.be/ubhDgGU8C8s)


### Generation of suitable authorization urls

This section describes a composition of OIDC authorization url which can be generated by application aiming for integration with Gluu Server while employing Inbound SAML powered by Passport.jst as authentication method of choice for its users, or to use it for manually testing Passsport-SAML authentication scenario (for the latter to work some OIDC client's registration must still exist at your Gluu Server so you could reference it in the url). 

Selection of Passport custom script authentication method at Gluu can be achieved either by passing its id in `acr_values` url query parameter, or by assigning it as the default `acr_value` for this client. In a correctly configured instance such request will trigger login flow presenting you with Gluu's Passport login page allowing to select authentication method you want. In case when Passport-SAML strategy is used and id of remote IDP is provided via `state` url query parameter, login page is not displayed and user is redirected to the pre-selected remote IDP right away.

[Next API article](https://gluu.org/docs/ce/api-guide/openid-connect-api/#requestauthorizationget) can be useful for learning additional details of url's layout, as well as [OIDC core spec paper](http://openid.net/specs/openid-connect-core-1_0.html).

A brief summary of url query parameters should be present in the url is provided below:
1. `clientid` (required) - id of OIDC client sending the request (its `inum` attribute in Gluu Server; the client's registration entry must exist at this Gluu Server)
1.`acr_values` (optional) - handle of authentication method to use (name of custom authentication script implementing it in Gluu Server, for example "passport"); if omitted some other means of triggering Passport.js's custom authentication script must be employed
1. `state` (required) - either an opaque random string, or a base64 encoded JSON with layout as follows: {"salt":"<salt_value>","provider":"<idp_id>"}; if the latter approach is used and remote IDP with such id is registered with Passport.js server, it will be automatically used for Inbound SAML scenario (no IDP selection page is displayed)
1. `nonce` (required) - String value used to associate an OIDC client's session with issued `id_token`, and to mitigate replay attacks; the value is passed through unmodified from authorization request to `id_token`; sufficient entropy MUST be enforced in the `nonce` values to prevent possible attackers from guessing them.
1. `acr_values` (optional) - String value used to request a specific authentication method from Gluu's oxAuth component; carries id (name) of the custom authentication (Jython) script implementing it, id of the Passport custom script in this case

Optionally, instead of composing authorization url manually next Java code snippet could be used to generate it.

```java
      //Example Java code for generation of OIDC authorization request
    
   
        import com.google.common.collect.Lists;
        import org.xdi.oxauth.client.AuthorizationRequest;
        import org.xdi.oxauth.model.common.ResponseType;
        
        import java.util.Random;
        
        public class OpenIdGenerator {
        
            static String clientid = "your_client_id"; //your OIDC client id
            static String redirect_uri = "redirect_uri"; 
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
```
A finalized authorization url may look like shown below:
```
https://example.gluu.org/oxauth/authorize?response_type=code+id_token&client_id=%40%215C0B.B148.7E63.326C%210001%21562E.F01E%210008%21664D.7760.0EC3.762D&scope=openid+profile&redirect_uri=https:%2F%2Flocalhost:8080&state=eyJwcm92aWRlciI6ImlkcDEifQ%3D%3D&nonce=S3M3R4nd0M&acr_values=passport
```
Following a correctly composed url should initiate the Inbound SAML flow powered by Passport.js

## Troubleshooting tooltips

In case of issues with this flow please make sure next requirements are met:

1. Make sure time is synchronized between all machines participating in the flow (NTP is the way to go). When clocks are out of sync it's known to cause a hard to troubleshoot state of "infinite loop" (non-ending redirection to the same set of pages).

2. Ensure that `uid` and `mail` attributes sent by remote IDP don't match corresponding attributes of any other user entry already existing at the Gluu instance where Passport-SAML script is running. By default, OpenLDAP requires both of those attributes to stay unique for each user entry.

3. Some IDPs may choose to encrypt assertions in their SAML responses in a way Passport.js won't be able to process. In case of any issues with the flow (especially the ones following the reception of SAML response from remote IDP by Passport server) try to disable assertion encryption at IDP to verify whether this is the cause of it (the response will still normally be passed over encrypted channel ensured by SSL/TLS level, providing strong enough security).

4. Passport keeps its logs under `/opt/gluu/node/passport/server/logs/` directory which can be checked for error traces and clues.
