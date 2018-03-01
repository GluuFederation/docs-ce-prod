# JavaScript

## Overview
The following documentation demonstrates how to use Gluu's [OpenID Connect JavaScript implicit client](https://github.com/GluuFederation/openid-implicit-client) to send users from an single page vanilla JS app to the Gluu Server for authentication and authorization.

> Note: The code used for this client was forked from a JavaScript library written by Edmund Jay.

## What is the JavaScript Implicit Client?
This JavaScript client implements the [OpenID Connect implicit flow](http://openid.net/specs/openid-connect-core-1_0.html#ImplicitFlowAuth). The Implicit Flow is mainly used by Clients implemented in a browser using a scripting language. The Access Token and ID Token are returned directly to the Client, which may expose them to the End-User and applications that have access to the End-User's User Agent. The Authorization Server does not perform Client Authentication.

The OpenID Connect Implicit Flow follows the following steps:

- Client prepares an Authentication Request containing the desired request parameters.
- Client sends the request to the Authorization Server.
- Authorization Server Authenticates the End-User.
- Authorization Server obtains End-User Consent/Authorization.
- Authorization Server sends the End-User back to the Client with an ID Token and, if requested, an Access Token.
- Client validates the ID token and retrieves the End-User's Subject Identifier.

## Installation

To use this library, include the openidconnect.js dependency to your HTML page. You can get it from the Github CDN.

```html
<script src="https://cdn.rawgit.com/GluuFederation/openid-implicit-client/master/openidconnect.js"></script>
```
The next steps for the installation are:

- Setting the provider and client configuration info through JSON objects;
- Calling the server – login;
- In the callback page, callback.html, you will get ID Token back, so that you can put it into the cookie to handle the session.



## Configuration

### Setting info and authentication

The library works with clients manually registered and it also allows a dynamic client registration. Please remember that for security purposes, during manual client registration you should set a Redirect Login URI to the address of the web page you intend to deploy.

The first step for the configuration should be setting the client and provider info. The first one should be done through a JSON object.

```JavaScript
var clientInfo = {
                client_id : '(your-client-id)',
                redirect_uri : 'https://(hostname)/login-callback.html'
                };
```

The dynamic client registration is done by declaring a JSON object without the client_id. The redirect_uri is a mandatory information.

```JavaScript
var clientInfo = {
                redirect_uri : 'callback.html'
                };
```

The provider info is retrieved by calling the function `OIDC.discover()`.

```JavaScript
var providerInfo = OIDC.discover('https://idp.example.com/');
```
The following functions set the information previously declared:
```JavaScript
OIDC.setClientInfo( clientInfo );
OIDC.setProviderInfo( providerInfo );
```
After setting client and provider information we choose to save all that data in the `sessionStorage` so we can restore them later at the callback-page and for that we use the method `storeInfo`.

```JavaScript
OIDC.storeInfo(providerInfo, clientInfo);
```
Still regarding our `sessionStorage`, we choose to remove both nonce and state from previous session to avoid conflict of data.

```JavaScript
sessionStorage.removeItem('state');
sessionStorage.removeItem('nonce');
```
The authentication homepage for this sample is composed by HTML tables to show our client information and the login request. The latest is a JSON object composed by all the information passed to the server authorization endpoint through the method `login`. This function is called on click of a button and its parameters are optional authentication request options. For our sample client this functionality is set as following:

```HTML
<button onClick="OIDC.login( {scope : 'openid profile email',
                            response_type : 'token id_token'} );"
        type="button" class="btn btn-success" >Authenticate</button>
```

### Login page

The login page of this sample is called `login-callback.html` and it basically prints the Id Token and User claims issued by the Identity Provider. As mentioned before, the URI for this page should be set as the redirect_uri of the client registered on the Gluu Server. The first step to manage the desired claims should be restoring the information saved on the sessionStorage. The function `restoreInfo` not only retrieves the client and provider information but it also sets them once again as described in the previous section of this tutorial.

```JavaScript
OIDC.restoreInfo();
```
In order to print the id_token claims you should use the method `getValidIdToken`. It gets the ID Token from the current page URL whose signature is verified and contents validated against the configuration data set during restoration. The first step to get the user claims is to get the Access Token that is also included in the current page URL. And it can be done by the method `getAccessToken`. The next code lines of our sample login-callback page are the following:

```JavaScript
var id_token = OIDC.getValidIdToken();
var access_token = OIDC.getAccessToken();
```

Now that you have the ID Token and the Access Token, you are able to get the ID Token claims and the User claims. The first one is returned by the function `getIdTokenParts`. The second one is a response for a HTTP request done by the method `getUserInfo` to the userinfo_endpoint of our IP. Both information are parsed to JSON Objects.

```JavaScript
var tokenClaims = JSON.parse(OIDC.getIdTokenParts(id_token)[1]);
var userInfoClaims = JSON.parse(OIDC.getUserInfo(access_token));
```
For our example we choose to present all data in HTML tables and to make things easier we created the function `JSONObjToHTMLTable`. So it is possible to call this method passing a JSON object as an argument and it will return a HTML string with the JSON in a table format.

```JavaScript
var tokenClaimsHTMLString = JSONObjToHTMLTable(tokenClaims);
var userInfoClaimsHTMLString = JSONObjToHTMLTable(userInfoClaims);
```

The last code line in our login page sample is calling the `debug` function. It prints in browser console the client information, provider information and the results to the verification and validation tests of the ID Token.

```JavaScript
OIDC.debug(true, id_token);
```

### Dynamic client registration

In case a client is not registered on Identity Provider yet it is possible to automatically register a new client. This library allows to dynamically register the client and proceed to the steps as described on the previous sections. In order to do that, you should just declare the `clientInfo` with the `redirect_uri` and omit a `client_id`. The `setClientInfo` method is responsible to check the existence of a `client_id` and in case it is not declared the function will do the registration of a new client at the IP with the known `redirect_uri`. After the well-succeed registration the same function retrieve the `client_id` parameter from this registered client and adds it to `clientInfo`. So to dynamically register a new client just declare `redirect_uri` of your `clientInfo` and call the method `setClientInfo` afterwards.

```JavaScript
var clientInfo = {
                redirect_uri : 'https://(hostname)/login-callback.html'
                };
OIDC.setClientInfo( clientInfo );
```  
