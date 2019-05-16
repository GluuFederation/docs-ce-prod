# oxRay

[LifeRay][liferay] OpenID Connect plugin to authenticate users using
Gluu IdP.
[TOC]

## Overview

The oxAuth LifeRay plugin is used to authenticate and auto-log users
from Gluu Server into [LifeRay][liferay] with the same credentials. It
is built on top of oxAuth, the OpenID Connect provider by Gluu.

The oxAuth plugin intercepts any attempt to login from anywhere in the
LifeRay and redirects the request and the user to an oxAuth server where
the identification takes place, actually. If the user has authorized the
server to share some of his basic information with the oxAuth plugin,
the user will be redirected back to the LifeRay CMS, and logged in,
automatically.

The goal of this project is to use the LifeRay CMS as the basis for an
organizational personal data store service.

Note: This plugin does not support auto-user creation from information
supplied by the oxAuth Plugin. Instead, it can be implemented by
extending the plugin.

## Deployment

The plugin is provided in two variants--[Maven][maven] and [Ant][ant].
You can either use Maven or the LifeRay plugin SDK to build and deploy
this plugin as a standard LifeRay hot deployable WAR file.

### Deploying WAR file using Maven

This requires a prerequisite: make sure that you have [Maven][maven]
installed on your system to build this plugin from source.

1. Checkout the Maven source from the [oxRay Repository][https://github.com/GluuFederation/oxRay/tree/master/6.2.x/maven/gluu-openid-connect-hook].

2. Open the file `pom.xml` in `gluu-openid-connect-hook`, and update
your local LifeRay Tomcat bundle path. This is required for building the
WAR file and deploying to the LifeRay Tomcat bundle.

![configure_pom_xml](https://raw.githubusercontent.com/GluuFederation/oxRay/master/img/configure_pom_xml.jpg)

3. Run the following command in the `gluu/6.2.x/maven/gluu-openid-connect-hook` 
directory:

```
mvn clean install package liferay:deploy
```

This will take a few seconds to download the dependency `jar` files, and
generate the LifeRay-compiled deployable WAR file. It will be placed
within your `<liferay-bundle-folder>/deploy` directory, and the hot
deployable process will start.

### Using LifeRay Plugin SDK With Ant

This requires a prerequisite: we assume that you have the plugin SDK
both installed and configured with LifeRay bundle.

1. Checkout the gluu-openid-connect-hook plugin source from the
repository, and place these files in your local directory for the plugin
SDK. Usually, this is `liferay-plugins-sdk-6.2.0-ce-ga1/hooks`.

2. Run the following command in the folder `liferay-plugins-sdk-6.2.0-ce-ga1/hooks/gluu-openid-connect-hook`:

```
ant clean deploy
```

### Using Binary From Repository

You can also download a compiled binary as a standard LifeRay deployable
WAR file from the following location:

[oxRay LifeRay Deployable War File](https://github.com/GluuFederation/oxRay/blob/master/6.2.x/binary/gluu-openid-connect-hook-6.2.0.1.war)

Copy this WAR file in your LifeRay bundle. Usually, this is located at
`liferay-portal-6.2.0-ce-ga1/deploy`.

Once the plugin is deployed as a WAR file either using Maven or Ant, you
will see the following success message in your LifeRay Tomcat server:

![deploy_success](https://raw.githubusercontent.com/GluuFederation/oxRay/master/img/deploy_success.jpg)

### Client Registration

A LifeRay application needs to be registered with the Authorization
server before initiating an authentication request/response with OAuth
IdP server.

The following steps are necessary to obtain both a client id and a
client secret. These data will be used within the LifeRay portal
properties.

1. Go to the location `https://seed.gluu.org/oxauth-rp/home.seam`.
2. You will see the Dynamic Client Registration Section.
3. Enter the Registration Endpoint uri, for example
`https://idp.example.org/oxauth/seam/resource/restv1/oxauth/authorize`.
	* You can derive this uri from your IdP auto-discovery uri which is
like that: `https://<Your IDP Server Domain>/.well-known/openid-configuration`.
	* You can search for the registration endpoint, and copy that uri here.
4. Enter the redirect uris as `http://localhost:8080/openidconnect/callback`:
	* Replace your domain name with `localhost:8080`
	* This will be your LifeRay handler for logging a user into LifeRay,
automatically, when a redirect comes back from the OAuth server.
5. Select the Response Types: CODE
6. Select the Application Type: WEB
7. For development purposes use: NATIVE (if you are testing on a local
machine with `localhost:8080` domain)
8. Enter Client Name: LifeRay App (you can choose any name here).
9. All other options can be left as they are--please see the attached
screenshot:

![client_registration](https://raw.githubusercontent.com/GluuFederation/oxRay/master/img/dynamic_client_registration_screen1.jpg)

10. Click `Submit`, and both the following `Registration Request` and
`Registration Response` will be displayed:

![json-request-response](https://raw.githubusercontent.com/GluuFederation/oxRay/master/img/json-request-response.jpg)

11. Save the Registration Response to your local system. The parameters
`client_id` and `client_secret` are used in LifeRay when configuring
`portal-ext.properties`.

#### Modifying portal.properties

It is necessary to modify `portal-ext.properties` file to reflect oxAuth
server client credentials and server's URL. It can be accomplished by
navigating into the `liferay-portal-6.2.0-ce-ga1` folder, where the file
`portal-ext.properties` is stored.

Note: To either activate or deactivate the oxAuth plugin put the value
`true` (to activate) or `false` (to deactivate), respectively.

```
gluu.openidconnect.auth.enabled=true
```

* oxAuth client ID and client secret:

```
gluu.openidconnect.client.id=@!1111!0008!51CE.1E59
gluu.openidconnect.client.secret=65777eb7-87a8-4d60-9dbc-d31d43971f2b
```

* OAuth server domain

```
gluu.openidconnect.idp.domain=https://idp.gluu.org`
```

* OAuth server auto discovery uri

```
gluu.openidconnect.url.discovery=https://idp.gluu.org/.well-known/openid-configuration
```

* Your OAuth server logout uri (typically, this will be used to logout a
user from OAuth when a user logs out from LifeRay)

```
gluu.openidconnect.idp.logout=https://idp.gluu.org/identity/logout
```

* LifeRay server callback uri that will be used as a handling response
by the OAuth server after authentication:
   * replace the `localhost:8080` with your LifeRay domain name:

```
gluu.openidconnect.client.redirect.url=http://localhost:8080/openidconnect/callback
```
     This page will be invoked when the user does not exist in the
     LifeRay database, but gets authenticated from the OAuth Server.

* Typically, create a LifeRay page with the name `/no-such-user-found`,
  or redirect to the LifeRay registration page uri like that:

```
gluu.openidconnect.no.such.user.redirect.url=http://localhost:8080/no-such-user-found
```

Restart the LifeRay server after editing the file
`portal-ext.properties`.

### Login Using the LifeRay Front End

* Server Bootup
	* Once the LifeRay server is restarted, open your browser and
      navigate to the uri `http://localhost:8080`.

* Login uri
	* Once the LifeRay page successfully loaded navigate to the OpenID
      connect page at `http://localhost:8080/openidconnect/login`.

Note: you can edit the theme code, and link to the login uri as
`http://localhost:8080/openidconnect/login`. In result the user will
always redirect to the OAuth server for authentication.

* OAuth authentication
	* The LifeRay login uri will redirect users to the OAuth IdP server
      for user authentication. Internally, passing the oAuth client id 
      as the following screen:

![oauth-login](https://raw.githubusercontent.com/GluuFederation/oxRay/master/img/oauth_login.jpg)

* Request for permission
	* This screen can be configured depending upon your OAuth Server
      implementation.

![oauth_info_confirm](https://raw.githubusercontent.com/GluuFederation/oxRay/master/img/oauth_info_confirm.jpg)

* OAuth callback (user auto-login to LifeRay)
	* After a successful authentication with the OAuth server, IdP will
send a callback to LifeRay with a specific code as a parameter:

```
http://localhost:8080/openidconnect/callback?code=xxx`
```

This will be intercepted by our oxAuth LifeRay plugin. Upon validation
of the token with the Gluu IdP, it will result in a login of the user to
the LifeRay. The user will be redirected to his respective start page.

![liferay_success_login](https://raw.githubusercontent.com/GluuFederation/oxRay/master/img/liferay_success_login.jpg)

[ant]: https://en.wikipedia.org/wiki/Apache_Ant "Apache Ant, Wikipedia"

[liferay]: https://en.wikipedia.org/wiki/Liferay "LifeRay, Wikipedia"

[maven]: https://en.wikipedia.org/wiki/Apache_Maven "Apache Maven, Wikipedia"

[oxray]: https://github.com/Gluufederation/oxRay/6.2.x/maven "oxRay repository"
