# Inbound OpenID Connect using Passport.js

Out of the box, passport supports integration with several well-known social sites for inbound authentication. In this page we demonstrate how to add an additional authentication provider, namely an OpenID Connect provider (OP).

## Requirements

- Gluu Server 3.1.3 with Passport.js 

!!! Note
    If Passport was not included during initial installation, it can be installed post installation following [these instructions](../operation/faq.md#adding-passportjs-andor-shibboleth-idp-post-installation)

## Backup your passport application

There are some minor file changes that you'll need to apply in your passport app. It's good idea to have a copy at hand in case of problem. Login to chroot and backup passport:

```
service gluu-server-3.1.3 login
#cd ~ 
#mkdir temp
#cp -R /opt/gluu/node/passport/ temp
``` 

## Install passport-openidconnect

Ensure your VM has internet access. The following will add the [passport-openidconnect](https://github.com/jaredhanson/passport-openidconnect) strategy to the modules used by the application.

```
#cd /opt/gluu/node/passport/
#export PATH=$PATH:/opt/node/bin
#npm install passport-openidconnect --save
```

Output should look like this:
```
+ passport-openidconnect@0.0.2
added 4 packages in 1.234s
```

## Update required UI files

Create a logo image in png format for this provider. Copy the file to `/opt/gluu/jetty/oxauth/custom/static/img`. You may have to create the `img` folder. 

The file name should be the same as the provider name, eg. `mypartner.png` in this case.

Download the file [passportlogin.xhtml](https://github.com/GluuFederation/oxAuth/blob/version_3.1.3/Server/src/main/webapp/auth/passport/passportlogin.xhtml) and do these edits:

- After line 333 add logic to properly read the new image. The following will work:

```
if (social_name.match("mypartner")) {
	img = '../../ext/resources/img/' + social_name + '.png'
}
```

- After line 312 add logic so that the new provider is recognized. Like the following:

```
if (provider.match("mypartner")) {
	send_url = url_social;
}
```

`cd` to `/opt/gluu/jetty/oxauth/custom/pages` and create a directory named `auth` and then one named `passport` inside it. 
Finally copy the edited file to `/opt/gluu/jetty/oxauth/custom/pages/auth/passport`.

Restart oxauth (eg `#service oxauth restart`), and then navigate to `https://<host-name>/oxauth/ext/resources/img/mypartner.png` in a browser. You should be able to see your image now.

## Create an OIDC client to interact with your external OP

In this example we assume you are creating a client in a **separate** Gluu Server installation. For this purpose the oxTrust admin UI can be used. 

Login with admin credentials to `https://<host-name>/identity` and go to "OpenId" > "Clients" > "Add". Provide the following settings:

- client name: *any of your choosing*

- application type: native

- pre-authorization: false

- persist client authorizations: true

- subject type: pairwise

- jws algorithm ID token: rs256

- authentication method for token endpoint: client_secret_post

- require auth time: false

- scopes: openid, profile, user_name, email

- grant types: authorization_code

- logout session required: false

- response types: code

- redirect login uri: `https://<host-name>/passport/auth/mypartner/callback` 


It's important to note that `passport-openidconnect` **only** supports the code flow. Additionally, comunication with the token endpoint is carried out via POST.

## Supply client details in passport side

In oxTrust of the Gluu server where passport resides, go to "Configuration" >  "Manage Authentication" > "Passport authentication method". Click on "add strategy". As name use `mypartner`. Click "add new property" and use `clientID` with the respective value (looks like `@!E051.5609.8133.5BC7!0001!0884.4792!0008!2FA2.683F`)

Add another property for `clientSecret` and fill appropriately.


!!! Note:
    In this example "mypartner" was used to name the strategy. If you want a different one, recall to appropriately replace occurrences throughout all files modified or added.
    
## Create strategy

We have to add and edit some files to make passport aware of our new openId connect client.

### Create `mypartner.js` file:

  1. `# cd /opt/gluu/node/passport/server/auth`
  1. Paste the following content inside that file:
 
    var passport = require('passport');  
    var passport=new passport.Passport();
    var MyPartnerOIDCStrategy = require('passport-openidconnect').Strategy;  
    var setCredentials = function(credentials) {  
    var callbackURL = global.applicationHost.concat("/passport/auth/mypartner/callback");  
        passport.use(new MyPartnerOIDCStrategy({  
        issuer: 'https://server.example.com/',  
        authorizationURL: 'https://server.example.com/authorize',  
    	tokenURL: 'https://server.example.com/token',  
    	userInfoURL: 'https://server.example.com/userinfo',  
    	clientID: credentials.clientID,  
    	clientSecret: credentials.clientSecret,  
      	callbackURL: callbackURL,  
        scope: 'profile user_name email'  
            },  
            function(iss, sub, profile, accessToken, refreshToken, done) {  
                var userProfile = {  
        id: profile.id,  
        name: profile.displayName,  
        username: profile._json.user_name || profile.id,  
        email: profile._json.email || "",  
        givenName: profile.name.givenName || "",  
        familyName: profile.name.familyName || "",  
        provider: "mypartner",  
        accessToken: accessToken  
                };  
                return done(null, userProfile);  
            }  
        ));  
    };  
  
        module.exports = {  
            passport: passport,  
            setCredentials: setCredentials  
        };  
     
    

!!! Note
    Provide suitable values for OP's endpoints (lines 7-10)

### Edit file `index.js`:
 - `#cd /opt/gluu/node/passport/server/routes`
 - Edit the index.js file:`#vi index.js`
 - Add this line somewhere at the beginning of this file: 
  
    var passportOIDCPartner = require('../auth/mypartner').passport;   
    
 - Add a new route in that file:

```
    //=== my openid partner ===  
    router.get('/auth/mypartner/callback',  
        passportOIDCPartner.authenticate('openidconnect', {  
            failureRedirect: '/passport/login'  
        }),  
        callbackResponse);  
    
    router.get('/auth/mypartner/:token',  
        validateToken,  
        passportOIDCPartner.authenticate('openidconnect'));   
```

### Edit `configureStrategies.js`:

- `#cd /opt/gluu/node/passport/server/auth`  
- Edit the file `#vi configureStrategies.js`  
- Add this line at the beginning:  

    `var PartnerOIDCStrategy = require('./mypartner');`  
   
- Add the below block after other if blocks:  
  
   ` //PartnerStrategy`  
   ` if (data.passportStrategies.mypartner) {`  
   `     logger.log('info', 'MyPartner Strategy details received');`  
   `     PartnerOIDCStrategy.setCredentials(data.passportStrategies.mypartner);`  
   `     }        `  

## Test

Restart passport (e.g. service passport restart). Passport log will show an entry like "[INFO] MyPartner Strategy details received". Log is located at `/opt/gluu/node/passport/server/logs` 

Setup an application to use `passport_social` as authentication method. You can use oxTrust for this purpose: in the machine where passport is installed, login with admin credentials to `https://<host-name>/identity` 

Go to "Configuration" >  "Manage Authentication" > "Default Authn method" and choose "passport_social" for "oxTrust acr". Leave this browsing session opened and wait 1 minute till the server picks the change

Open a separate browsing session (e.g. incognito) and try to access `https://<host-name>/identity`, you'll see a button for the new OP in the right-hand pane and authentication should proceed there.
