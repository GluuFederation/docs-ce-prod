# App Auth Android

## Overview

AppAuth for Android is a client SDK for communicating with OAuth 2.0 and OpenID Connect providers. It strives to directly map the requests and responses of those specifications, while following the idiomatic style of the implementation language. In addition to mapping the raw protocol flows, convenience methods are available to assist with common tasks like performing an action with fresh tokens.
## Auth Flow

AppAuth supports both manual interaction with the Authorization Server where you need to perform your own token exchanges, as well as convenience methods that perform some of this logic for you. This example uses the convenience method which returns either an XXXAuthState object, or an error.

XXXAuthState is a class that keeps track of the authorization and token requests and responses, and provides a convenience method to call an API with fresh tokens. This is the only object that you need to serialize to retain the authorization state of the session.

## Requirements

To use app-auth we need three parameters: issuer, clientId and redirectUri:
- issuer - from which the configuration will be discovered
- clientId - from dynamic client registration response 
- redirectUri - this scheme must be registered as a scheme in the project's manifest file

## Configuration

First, we need to do dynamic client registration, for that go to - https://ce-dev.gluu.org/oxauth-rp/home.htm
On the top enter https://ce-dev.gluu.org as OpenID Connect Discovery url:

![discovery_url](../img/app-auth/discovery_url.png)

After on form "Dynamic Client Registration" fill next fields:
- Registration Endpoint: https://ce-dev.gluu.org/.well-known/openid-configuration
- Redirect URIs (space-separated): appscheme://client.example.com
- Post Logout Redirect URIs (space-separated): https://net.openid.appauthdemo.logout
- Response Types: CODE
- Grant Types: AUTHORIZATION_CODE
- Application Type: NATIVE

![dynamic_registration](../img/app-auth/dinamic_registration.png)

## Main workflow diagram

![flowDiagram](../img/app-auth/flowDiagram.png)

## Integration
Need to make following changes in your code to integrate AppAuth in your android app
- Need to put `client_id` and `client_secret` values obtained from dynamic registration response into `idp_configs.xml`(app/res/values/idp_configs.xml) file of your android project. It will look like this.

  ```
    <string name="openid_client_id" translatable="false">put client_id here</string>
    <string name="openid_client_secret" translatable="false">put client_secret here</string>
  ```
- Above `client_id` and `client_secret` will be use for Authorization.To use these values for authorization need to specify them to Identity Provider.
  your IdentityProvider.java class should be look like this.
  
  ```
    public static final IdentityProvider OPEN_ID = new IdentityProvider(
            "OpenID",
            R.bool.openid_enabled,
            R.string.openid_discovery_uri,
            NOT_SPECIFIED, // auth endpoint is discovered
            NOT_SPECIFIED, // token endpoint is discovered
            NOT_SPECIFIED, // dynamic registration not supported
            R.string.openid_client_id, // set openid_client_id here
            R.string.openid_client_secret, // set openid_client_secret here
            R.string.openid_auth_redirect_uri,
            R.string.openid_logout_redirect_uri,
            R.string.openid_scope_string,
            R.drawable.btn_openid,
            R.string.openid_name,
            android.R.color.white);
  ```
- We are using a custom scheme to send the OAuth redirect back to app. The library configures the `RedirectUriReceiverActivity` to handle a custom scheme and need to declare this activity into your `AndroidManifest.xml` file by adding following:
  
  ```
    <activity android:name="net.openid.appauth.RedirectUriReceiverActivity">
                <intent-filter>
                    <action android:name="android.intent.action.VIEW"/>
                    <category android:name="android.intent.category.DEFAULT"/>
                    <category android:name="android.intent.category.BROWSABLE"/>
                    <data android:scheme="appscheme"
                      android:host="client.example.com"/>
                </intent-filter>
            </activity>
  ```
    After completing authorization in custom tab, above custom scheme(appscheme) will redirect back to app.