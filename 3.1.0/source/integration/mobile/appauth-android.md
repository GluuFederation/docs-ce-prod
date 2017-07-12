# AppAuth Android

## Overview
AppAuth for Android is a client SDK for communicating with 
[OAuth 2.0](https://tools.ietf.org/html/rfc6749) and 
[OpenID Connect](http://openid.net/specs/openid-connect-core-1_0.html) providers. It 
strives to directly map the requests and responses of those specifications, 
while following the idiomatic style of the implementation language. In 
addition to mapping the raw protocol flows, convenience methods are 
available to assist with common tasks like performing an action with 
fresh tokens.

The library follows the best practices set out in 
[OAuth 2.0 for Native Apps](https://tools.ietf.org/html/draft-ietf-oauth-native-apps)
including using
[Custom Tabs](http://developer.android.com/tools/support-library/features.html#custom-tabs)
for the auth request. For this reason,
`WebView` is explicitly *not* supported due to usability and security 
reasons.

The library also supports the [PKCE](https://tools.ietf.org/html/rfc7636)
extension to OAuth which was created to secure authorization codes in 
public clients when custom URI scheme redirects are used. The library is 
friendly to other extensions (standard or otherwise) with the ability to 
handle additional parameters in all protocol requests and responses.

Gluu server is certified OpenId Provider and supports
[Native Apps](https://tools.ietf.org/html/draft-ietf-oauth-native-apps)
either through custom URI scheme redirects, or App Links.

## Download
You can download (or clone) project from [Github Repository](https://github.com/openid/AppAuth-Android)

## Specification
### Supported Android Versions
AppAuth supports Android API 16 (Jellybean) and above.

When a Custom Tabs implementation is provided by a browser on 
the device (for example by [Chrome](https://developer.chrome.com/multidevice/android/customtabs)), 
Custom Tabs are used for authorization requests. Otherwise, 
the default browser is used as a fallback.

Both Custom URI Schemes (all supported versions of Android) and App Links
(API 23+) can be used with the library.

## Building the Project
### Prerequisites
The project requires the Android SDK for API level 23 
(Marshmallow) to build, though the produced binaries only 
require API level 16 (Jellybean) to be used.

### Building from Android Studio

Android Studio is an official IDE for Android.

You can find Android Studio, it's features, docs, user guide etc. 
from [Official Android Website for developers](https://developer.android.com/studio/index.html).

There are two ways to build existing project either download source code zip 
file or clone repository.
 
If you have downloaded source code zip file then follow below steps to 
import project in Android Studio:

1. Extract the source code zip file in your desired folder in your 
computer's file system.
2. Open Android Studio, Go to File -> New -> Import project. It will 
prompt to select existing project from your computer.
3. Browse the folder where you extracted source code file and select 
the build.gradle file of the project.
![import_project](../img/app-auth/import_project.png)
4. Click **OK** and it will start building project. 
   
Another way if you don't want to download source code manually and want 
to clone repository then follow below steps:   
 
1. Open Android Studio, Go to File -> New -> Project from Version Control 
-> Git.
![clone_repo_init](../img/app-auth/clone_repo_init.png)
2. It will prompt in which you need to provide following details and then 
click **Clone**.
 
   Git Repository URL: Repository URL which you want to clone
   
   Parent Directory: Folder location in which you want to store 
   project in your computer
    
   Directory Name: Project Name
![clone_repo_details](../img/app-auth/clone_repo_details.png)   
3. It will Clone repository into the folder you mentioned 
in **Parent Directory** above and start building the project.  
   
If you get an error like: Error:Could not find 
com.android.support:customtabs:23.2.0. then be sure you have installed 
the Android Support Library from the Android SDK Manager. Follow the 
Android Studio prompts to resolve the dependencies automatically.   

Once the project build successfully, you can see that there are two 
modules in the project.

1. app(Demo app which use AppAuth library)
2. library(AppAuth library project)

## Configure the Client

In order to configure client you need to specify following:

### issuer 
   Here Gluu server is the issuer hence configuration will be discovered from Gluu server
   discovery uri.

### clientId 
   Can be obtained after client registration. 

You can either manually create a client in oxTrust or register dynamically through app but 
it is recommended you should manually register client in oxTrust.

#### Manual client registration (Recommended)

To create client manually in oxTrust, follow the Gluu Server's [OpenID Connect client registration documentation](https://gluu.org/docs/ce/admin-guide/openid-connect/#client-registration-configuration).

After successful registration, it will return client id which 
will use for Authorization.

#### Dynamic client registration (Optional)

New client registration request can be constructed for dispatch:

```java
RegistrationRequest registrationRequest = new RegistrationRequest.Builder(
    serviceConfig,
    Arrays.asList(redirectUri))
    .build();
```

Requests are dispatched with the help of `AuthorizationService`. As this
request is asynchronous the response is passed to a callback:

```java
service.performRegistrationRequest(
    registrationRequest,
    new AuthorizationService.RegistrationResponseCallback() {
        @Override public void onRegistrationRequestCompleted(
            @Nullable RegistrationResponse resp,
            @Nullable AuthorizationException ex) {
            if (resp != null) {
                // registration succeeded, store the registration response
                AuthState state = new AuthState(resp);
                //proceed to authorization...
            } else {
              // registration failed, check ex for more details
            }
         }
    });
```

### redirectUri
custom URI redirection scheme for inter-app communication

#### Define redirectURI
As Authorization request will be made using custom tab, redirectURI will provide redirection 
back to the app from custom tab after request get performed successfully.
 
It is recommended to  use a custom scheme as redirectURI.You can simply use any 
custom scheme you want and need to declare it in app's manifest file.

You will find more about custom scheme from [IETF Document](https://tools.ietf.org/html/draft-ietf-oauth-native-apps-08#section-7.1) 

For example, if you declare custom scheme `myscheme` and host `client.example.com` then
redirectURL will look like: `myscheme://client.example.com`

The library configures the `RedirectUriReceiverActivity` to 
handle a custom scheme and need to declare this activity into 
your `AndroidManifest.xml` file by adding following:

```xml
    <activity android:name="net.openid.appauth.RedirectUriReceiverActivity">
        <intent-filter>
            <action android:name="android.intent.action.VIEW"/>
            <category android:name="android.intent.category.DEFAULT"/>
            <category android:name="android.intent.category.BROWSABLE"/>
            <data android:scheme="YOUR_CUSTOM_SCHEME"
                android:host="YOUR_REDIRECT_HOST"/>
        </intent-filter>
    </activity>
```

After completing authorization in custom tab, above custom scheme 
will redirect back to app.

## Configure the Demo App

Replace following `auth_config.json` file of app located at `app/res/raw/auth_config.json` 
with following content:

```json
{
  "client_id": "Put ClientId obtained from registration here",
  "redirect_uri": "Put custom scheme redirect_uri here",
  "authorization_scope": "openid email profile",
  "discovery_uri": "<IDP hostname>.well-known/openid-configuration",
  "authorization_endpoint_uri": "",
  "token_endpoint_uri": "",
  "registration_endpoint_uri": "",
  "https_required": true
}
```

And need to add a new intent-filter to the 
`net.openid.appauth.RedirectUriReceiverActivity` activity section 
of the `AndroidManifest.xml`

```
<!-- Callback from authentication screen -->
<activity android:name="net.openid.appauth.RedirectUriReceiverActivity">
   
!-- redirect URI for your new IDP -->
    <intent-filter>
        <action android:name="android.intent.action.VIEW"/>
        <category android:name="android.intent.category.DEFAULT"/>
        <category android:name="android.intent.category.BROWSABLE"/>
        <data android:scheme="YOUR_CUSTOM_SCHEME"
                        android:host="YOUR_REDIRECT_HOST"/>
    </intent-filter>
</activity>
```
**Note**: Skip this step if you've already made these changes under section **Define redirectURI** above.

Now, You are all set to run your demo app.
As soon as app will launch, it will look like this
![initial screen](../img/app-auth/start_authorization.png)

Congratulations, You've configured demo app correctly. Go ahead and click 
'Start Authorization' button to make authorization request.
 
Authorization success will look like this

![Success Auth](../img/app-auth/authorization_success.png)  

## Auth Flow

AppAuth supports both manual interaction with the OP where you need 
to perform your own token exchanges, as well as convenience methods 
that perform some of this logic for you. This example uses the convenience 
method which returns either an `AuthState` object, or an error.

### Tracking authorization state

`AuthState` is a class that keeps track of the authorization and 
token requests and responses, and provides a convenience method to
call an API with fresh tokens. This is the only object that you 
need to serialize to retain the authorization state of the 
session.Typically, one would do this by storing the authorization 
state in SharedPreferences or some other persistent store private 
to the app:

```java
@NonNull 
public AuthState readAuthState() {
  SharedPreferences authPrefs = getSharedPreferences("auth", MODE_PRIVATE);
  String stateJson = authPrefs.getString("stateJson");
  AuthState state;
  if (stateStr != null) {
    return AuthState.fromJsonString(stateJson);
  } else {
    return new AuthState();
  }
}

public void writeAuthState(@NonNull AuthState state) {
  SharedPreferences authPrefs = getSharedPreferences("auth", MODE_PRIVATE);
  authPrefs.edit()
      .putString("stateJson", state.toJsonString())
      .apply();
}
```

### Configuration

You can configure communication with Gluu server by specifying the endpoints directly:

```java
AuthorizationServiceConfiguration config =
        new AuthorizationServiceConfiguration(name, mAuthEndpoint, mTokenEndpoint);

```

Or through discovery:

```java
final Uri issuerUri = Uri.parse(`DISCOVERY_URI`);
AuthorizationServiceConfiguration config;

AuthorizationServiceConfiguration.fetchFromIssuer(
    issuerUri,
    new RetrieveConfigurationCallback() {
      @Override public void onFetchConfigurationCompleted(
          @Nullable AuthorizationServiceConfiguration serviceConfiguration,
          @Nullable AuthorizationException ex) {
        if (ex != null) {
            Log.w(TAG, "Failed to retrieve configuration for " + issuerUri, ex);
        } else {
            // service configuration retrieved, proceed to authorization...
        }
      }
  });
```

Additionally, AppAuth provides additional client configuration, 
in order to control the browsers that can be used for the 
authorization flow, or to control the HttpURLConnection 
implementation that is used for token exchange. This can be done 
by creating an `AppAuthConfiguration` object:

```java
AppAuthConfiguration appAuthConfig = new AppAuthConfiguration.Builder()
    .setBrowserMatcher(new BrowserWhitelist(
        VersionedBrowserMatcher.CHROME_CUSTOM_TAB,
        VersionedBrowserMatcher.SAMSUNG_CUSTOM_TAB))
    .setConnectionBuilder(new ConnectionBuilder() {
      public HttpURLConnection openConnect(Uri uri) throws IOException {
        URL url = new URL(uri.toString());
        HttpURLConnection connection =
            (HttpURLConnection) url.openConnection();
        if (connection instanceof HttpsUrlConnection) {
          HttpsURLConnection connection = (HttpsURLConnection) connection;
          connection.setSSLSocketFactory(MySocketFactory.getInstance());
        }
      }
    })
    .build();
```

This configuration will only permit Chrome or Samsung Browser to 
be used as a custom tab for authorization flows, and changes the 
SSL socket factory to a hypothetical custom version 
`MySocketFactory`. The modification of the socket factory is 
useful for certificate pinning, or adding some additional
certificates to the trusted set (such as for testing).

This configuration is provided to `AuthorizationService` upon 
construction:

```java
new AuthorizationService(context, appAuthConfig);
```

### Authorizing

After configuring or retrieving an authorization service 
configuration, an authorization request can be constructed for 
dispatch:

```java
AuthorizationRequest req = new AuthorizationRequest.Builder(
    config,
    clientId,
    ResponseTypeValues.CODE,
    redirectUri)
    .build();
```

Requests are dispatched with the help of `AuthorizationService`. 
As this will open a custom tab or browser instance to fulfill 
this request. An intent can be specified for both completion and 
cancellation of the authorization flow:

```java
AuthorizationService service = new AuthorizationService(context);
Intent postAuthIntent = new Intent(context, MyAuthResultHandlerActivity.class);
Intent authCanceledIntent = new Intent(context, MyAuthCanceledHandlerActivity.class);
service.performAuthorizationRequest(
    req,
    PendingIntent.getActivity(context, req.hashCode(), postAuthIntent, 0),
    PendingIntent.getActivity(context, req.hashCode(), authCanceledIntent, 0));
```

### Handling the Redirect
When the response is captured by `RedirectUriReceiverActivity`, 
it is ultimately forwarded to the activity specified in your 
completion intent, and can be extracted from the intent data:

```java
public void onCreate(Bundle b) {
  // ...
  AuthorizationResponse resp = AuthorizationResponse.fromIntent(getIntent());
  AuthorizationException ex = AuthorizationException.fromIntent(getIntent());
  if (resp != null) {
    // authorization succeeded
  } else {
    // authorization failed, check ex for more details
  }
  // ...
}
```

The full redirect URI is also provided in your completion intent:

```java
public void onCreate(Bundle b) {
  // ...
  Uri redirectUri = getIntent().getData();
  // ...
}
```

Given the auth response, a token request can be created to 
exchange the authorization code:

```java
service.performTokenRequest(
    resp.createTokenExchangeRequest(),
    new AuthorizationService.TokenResponseCallback() {
      @Override public void onTokenRequestCompleted(
            TokenResponse resp, AuthorizationException ex) {
          if (resp != null) {
            // exchange succeeded
          } else {
            // authorization failed, check ex for more details
          }
        }
    });
```

If a confidential client is created through dynamic registration, 
and the server expects the client to authenticate at the token 
endpoint, the necessary client authentication must be supplied 
in the token request. This can be simplified by making sure to 
store the registration response in the `AuthState` instance, 
then `AuthState::getClientAuthentication` can construct the 
necessary client authentication:

```java
service.performTokenRequest(
    resp.createTokenExchangeRequest(),
    state.getClientAuthentication(),
    new AuthorizationService.TokenResponseCallback() {
      @Override public void onTokenRequestCompleted(
            TokenResponse resp, AuthorizationException ex) {
          if (resp != null) {
            // exchange succeeded
          } else {
            // authorization failed, check ex for more details
          }
        }
    });
```
### Making API Calls

With an updated AuthState based on the token exchange, it is then 
possible to make requests using guaranteed fresh tokens at any 
future point:

```java
AuthState state = readAuthState();
state.performActionWithFreshTokens(service, new AuthStateAction() {
  @Override public void execute(
      String accessToken,
      String idToken,
      AuthorizationException ex) {
    if (ex != null) {
      // negotiation for fresh tokens failed, check ex for more details
      return;
    }

    // use the access token to do something ...
  }
});
```
