# Configure Google

In order to call Google API's, you need to register as a developer and
create client credentials. Here are some
[instructions](https://developers.google.com/identity/protocols/OAuth2)
for these steps.

The first thing you'll need to do is Create a Project on Google to obtain
client credentials. Click "Create project" and enter your desired
project name.

![image](../img/admin-guide/multi-factor/01-create-project.png)

Then click on your newly created project from the listing on the
dashboard, and under the Credentials section, create a new "OAuth2 2.0
client ID". 

![image](../img/admin-guide/multi-factor/02-create-oauth2-creds.png)

Google will ask you to configure your consent screen, to add your logo
and other information displayed to the user to authorize Google to
release information.

![image](../img/admin-guide/multi-factor/03-create-oauth2-creds.png)

Fill out the form...

![image](../img/admin-guide/multi-factor/04-configure-authorization-page.png)

Now you're ready to create the credentials. Enter "Authorized JavaScript
origins". It should be the uri of your Gluu Server--for example
`https://idp.example.com`.

![image](../img/admin-guide/multi-factor/05-create-oauth2-creds.png)

Google will display the client-id and the according secret ... ignore
it. Instead, download the JSON file which you are going to upload into
your Gluu Server, next.

![image](../img/admin-guide/multi-factor/06-download_json.png)

Move this file to the location `/etc/gluu/conf/google.json`. The JSON
file will look something like this example (no... these data are not
valid credentials!):

```
{
  "web": {
    "client_id": "7a64e55f-724d4e8c91823d5f1f18a0b2.apps.googleusercontent.com",
    "auth_uri": "https:\/\/accounts.google.com\/o\/oauth2\/auth",
    "token_uri": "https:\/\/accounts.google.com\/o\/oauth2\/token",
    "auth_provider_x509_cert_url": "https:\/\/www.googleapis.com\/oauth2\/v1\/certs",
    "client_secret": "bb76a2c99be94e35b874",
    "javascript_origins": [
    "https:\/\/brookie.gluu.info"
    ]
  }
}
```

The last step is to enable Google+ API's:

- Navigate back to the Google API [console](https://console.developers.google.com/project)
- Select project and enter project name
- Open new project "API & auth -> API" menu item in configuration navigation tree
- Click "Google+ API"
- Click "Enable API" button

**Configure oxTrust**

Follow the steps below to configure the certificate authentication in the oxTrust Admin GUI.

1. Click on Manage Custom Scripts under Configuration on the Main Menu.

2. Click on the `Add Custom Scritp` button
[add-script-button](../img/admin-guide/multi-factor/add-script-button.png)

3. Fill up the form and add the [Google External Authenticator](./GooglePlusExternalAuthenticator.py) Script.

You'll also need to add some custom properties:

 * __gplus_client_secrets_file__: `/etc/gluu/conf/google.json`
 * __gplus_deployment_type__: enroll
 * __gplus_remote_attributes_list__: email, given_name, family_name, and locale
 * __gplus_local_attributes_list__: uid, mail, givenName, sn, cn, preferredLanguage

1. __gplus_client_secrets_file__ - It is a mandatory property that holds
   the path to the application configuration file downloaded from Google
   console for application. An example is `/etc/certs/gplus_client_secrets.json`.

### Setting Google App
These are the single steps needed to ClientSecret and ClientID 
or Google JSON:

a) Log into: `https://console.developers.google.com/project`

b) Click "Create project" and enter project name

c) Open new project "API & auth -> Credentials" menu item in configuration navigation tree

d) Click "Add credential" with type "OAuth 2.0 client ID"

e) Select "Web application" application type

f) Enter "Authorized JavaScript origins". It should be CE server DNS
       name, for example `https://gluu.info`.

g) Click "Create" and Click "OK" in next dialog

h) Click "Download JSON" in order to download
       `gplus_client_secrets.json` file.

Also it is mandatory to enable Google+ API:
    
a) Log into `https://console.developers.google.com/project`
    
b) Select project and enter project name
    
c) Open new project "API & auth -> API" menu item in configuration navigation tree
    
d) Click "Google+ API"
    
e) Click "Enable API" button

2. __gplus_deployment_type__ - Specify the deployment mode. It is an
optional property. If this property isn't specified the script tries to
find the user in the local LDAP by 'subject_identifier' claim specified
in id_token. If this property has a 'map' value the script allows to map
'subject_identifier' to the local user account. If this property has an
'enroll' value the script adds a new user to the local LDAP with status
'active'. In order to map the IDP attributes to the local attributes it
uses properties from both gplus_remote_attributes_list and
gplus_local_attributes_list. The allowed values are map and enroll.

3. __gplus_remote_attributes_list__ - Comma-separated list of attribute
names (user claims) that Google+ returns which map to local attributes
in the `gplus_local_attributes_list` property. It is mandatory only if
`gplus_deployment_type` is set to 'enroll'.

4. __gplus_local_attributes_list__ - Comma-separated list of Gluu Server
LDAP attribute names that are mapped to Google user claims from the
`gplus_remote_attributes_list` property. It is mandatory only if
`gplus_deployment_type` is set to 'enroll'.

5. __extension_module__ - Optional property to specify the full path of
an external module that implements two methods:

```python
    # This is called when the authentication script initializes
    def init(conf_attr):
        # Code here
        return True/False

    # This is called after authentication
    def postLogin(conf_attr, user):
        # Code here
        return True    # or return False
```

6. __gplus_client_configuration_attribute__ - Optional property to
specify the client entry attribute name which can override
`gplus_client_secrets_file file` content. It can be used in cases when
all clients should use a separate `gplus_client_secrets.json`
configuration.

## Testing

One simple way to test the configuration is to use oxTrust. In the
"Configure Authentication" dropdown menu, select "Google" (or whatever
you entered as the "Name" of the custom authentication script--as the
default authentication method.

![image](../img/admin-guide/multi-factor/08-select_default_authentication.png)

After you login and logout, you should be presented with a new login
form that has the Google login button:

![image](../img/admin-guide/multi-factor/09-google-authentication-button.png)

After clicking the Google login button, you are presented for
authorization--Google needs to make sure its ok to release attributes to
the Gluu Server:

![image](../img/admin-guide/multi-factor/10-google-authorization.png)

If the script doesn't work, and you locked yourself out of oxTrust,
don't worry! You can create an LDIF file, for example `revert.ldif`, to
set back the default authentication method, like this:

```
dn: inum=@!1E3B.F133.14FA.5062!0002!4B66.CF9C,ou=appliances,o=gluu
changetype: modify
replace: oxAuthenticationMode
oxAuthenticationMode: internal
```

oxAuthenticationMode corresponds to the 'Name' of the customer
authentication script in oxTrust. Use `internal` to revert to the
default LDAP authentication. You'll have to change the `inum` with the
`inum` of your installation. You can find it using ldapsearch like this:

```
root@gluu3-ubuntu:/opt/symas/bin# ./ldapsearch -h locahost -p 1389 -D "cn=directory manager,o=gluu" -w "{password provided during setup}" -b "ou=appliances,o=gluu" -s one "objectclass=*" inum
```

`~/.pw` is a file with your Directory Manager password. If you don't
remember it, try to find it using `grep`: 

```
grep ldapPass= /install/community-edition-setup/setup.properties.last
```

Once your LDIF looks ok, then use `ldapmodify` to revert back to
password authentication:

```
root@gluu3-ubuntu:/opt/symas/bin# ./ldapmodify -h localhost -p 1389 -D "cn=directory manager,o=gluu" -w "{password provided during setup}" -f revert.ldif
```

If things go wrong, it can leave the sessions in your browser in a bad
state. If things get really weird, remove the cookies in your browser
for the hostname of your Gluu Server.