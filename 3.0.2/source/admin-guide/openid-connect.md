# OpenID Connect 

## Overview

OpenID Connect is an identity layer that profiles and extends OAuth 2.0. 
It defines a sign-in flow that enables an application (client) to 
authenticate a person, and to obtain authorization to obtain 
information (or "claims") about that person. For more information, 
see [http://openid.net/connect](http://openid.net/connect)

It's handy to know some OpenID Connect terminology:

- The *end user* or *subject* is the person being authenticated.

- The *OpenID Provider* or *OP* is the equivalent of the SAML IDP. It 
holds the credentials (like a username/ password) and information about 
the subject. The Gluu Server is an OP.

- The *Relying Party* or  *RP* is software, like a mobile application 
or website, which needs to authenticate the subject. The RP is an OAuth 
client. [oxd](https://oxd.gluu.org) is an RP.

Read [this blog](http://gluu.co/oauth-saml-openid) for a good overview of OpenID Connect versus SAML.

## OpenID Connect in the Gluu Server

The Gluu Server passes all [OpenID Provider conformance profiles](http://openid.net/certification/). 
It supports the all the current specifications: Core, Dynamic Client 
Registration, Discovery, Form Post Response Mode, Session Management, 
and the draft for Front Channel Logout.

### OpenID Connect Flows

The Gluu Server supports all flows defined in the Core spec, including
implicit, code, and hybrid. The implicit flow, where the token and
id_token are returned from the authorization endpoint, should only 
be used for applications that run in the browser, like a Javascript 
client. The code flow or hybrid flow should be used for server side
applications, where code on the web server can more securely call
the token endpoint to obtain a token. The most useful response type 
for the hybrid flow is "code id_token". Using this flow, you can verify
the integrity of the code by inspecting the `c_hash` claim in the 
id_token.

If you are using the code flow, the response type should only be code.
There is no point in using response type "code token id_token"--the extra
tokens returned by the authorization endpoint will only create additional
calls to the LDAP server and slow you down. If you are going to trade
the code at the token endpoint for a new token and id_token, you don't
need them from the authorization endpoint too.

### Configuration / Discovery 

A good place to start when you're learning about OpenID Connect is
the configuration endpoint, which is located in the Gluu Server
at the following URL: `https://hostname/.well-known/openid-configuration`
The Gluu Server also supports [WebFinger](http://en.wikipedia.org/wiki/WebFinger),
as specified in the OpenID Connect specification. You can test Webfinger
using the oxAuth-RP tool mentioned above. For more information, see 
the [OpenID Connect Discovery Specification](http://openid.net/specs/openid-connect-discovery-1_0.html)

### Client Registration / Configuration

OAuth clients need a client_id, and need to supply a login redirect uri--
where the Authorization Server should redirect the end user to, post
authorization. The Gluu Server enables an administrator to manually create
a client via the oxTrust web interface. However, OpenID Connect also
defines a standard API where clients can register themselves--
[Dynamic Client Registration](http://openid.net/specs/openid-connect-registration-1_0.html). You can
find the registration URL by calling the configuration endpoint 
(`/.well-known/openid-configuration`).        

You may not want clients to dynamically register themselves! To disable
this endpoint, in the oxAuth JSON properties, set the 
`dynamicRegistrationEnabled` value to False.                 

If you want to add a client through oxTrust, you can use the manual form:
by click the `Add Client` button.            

![add-client](../img/openid/add-client.png)

There are many client configuration parameters. Most of these are 
specified in the OpenID Connect [Dynamic Client Registration](http://openid.net/specs/openid-connect-registration-1_0.html) specification.
There are two configurations params which can only be configured via 
oxTrust by an administrator. These include:

 - Pre-Authorization -- Use this if you want to suppress the end user
 authorization prompt. This is handy for SSO scenarios where the clients
 are your own (not third party), and there is no need to prompt the 
 person to approve the release of information.      
 
 - Persist Client Authorizations -- Use this option if you only want 
 to prompt the end user once to authorize the release of user 
 information. It will cause the data to be persisted under the person's
 entry in the Gluu LDAP server.                

### Custom Client Registration

Using the Client Registration custom interception scripts,
you can implement post-registration business logic. You have access to 
the data that the client used to register. You could validate data, 
populate extra client claim, or modify the scope registrations. You
could even call API's to determine if you want to allow the 
registration at all. To access the interface for custom scripts in 
oxTrust, navigate to Configuration --> Custom Scripts --> Client Registration.

![custom-client](../img/openid/custom-client.png)           

The script is [available here](./sample-client-registration-script.py)                      

### Logout

The OpenID Connect [Session Management](http://openid.net/specs/openid-connect-session-1_0.html) specification is still marked as draft, and new mechanisms for logout are in the works. The current specification requires JavaScript to detect that the session has been ended in the browser. It works... unless the tab with the JavaScript happens to be closed when the logout event happens on another tab. Also, inserting JavaScript into every page is not feasible for some applications. 

The Gluu Server also support the draft for [Front Channel Logout](http://openid.net/specs/openid-connect-frontchannel-1_0.html). This
is our recommended logout strategy. Using this mechanism, an html page is rendered which contains one iFrame for each application that 
needs to be notified of a logout. The Gluu Server keeps track of which clients are associated with a session (i.e. your browser). This 
mechanism is not perfect. If the end user's web browser is blocking third party cookies, it may break front channel logout. Also, the Gluu Server has no record if the logout is successful--only the browser knows. This means that if the logout fails, it will not be logged or retried. The good thing about front channel logout is that the application can clear application cookies in the end user's browser. To use front channel logout, the client should register logout_uri's, or `frontchannel_logout_uri` for clients using the Dynamic Client Registration API. 

## Scopes

In OAuth, scopes are used to specify extents of access. For a sign-in 
flow like OpenID Connect, scopes end up corresponding to the release of
user claims. The Gluu Server supports the 
[standard scopes](http://openid.net/specs/openid-connect-core-1_0.html#ScopeClaims) defined 
in the OpenID Connect specification. You can also define your own scopes,
and map them to any user attributes which you have registered. 

To add Scope and Claims in OpenID Connect

1. Click on `Configuration` > `OpenID Connect`           
     
    ![menu](../img/openid/clientmenu.png)

2. Click on Add scope on the screen to the right            
    ![scopeadd](../img/openid/admin_oauth2_scope.png)
3. You will presented the screen below to the enter the Scope Details                      
    
    ![scopedetails](../img/openid/add-scope1.png)

4. To add more claims, simply click "Add Claim" and you will be presented
with the following screen:                     

    ![Add Claims](../img/openid/add-scope-claim.png)

| Field | Description |
|---| ---|
| Display Name | Name of the scope which will be displayed when searched |
| Description | Text that will be displayed to the end user during approval of the scope |
| Scope Type | OpenID, Dynamic or OAuth  |
| Default Scope | If True, the scope may be requested during Dynamic Client Registration |

Scope Type "OpenID" specifies to the Gluu Server that this scope will
be used to map user claims; "Dynamic" specifies to the Gluu Server that
the scope values will be generated from the result of the Dynamic Scopes 
custom interception script; "OAuth" specifies that the scope will have
no claims, it will be meaningful to an external resource server. 

Specifying a scope as "Default" means that a client can request it 
during dynamic client registration. The only default scope is `openid`, 
which is required by the OpenID Connect specification. You can always 
explicitly release a scope to a certain client later on, but this will 
require some manual intervention by the Gluu Server admin.

## Multi-Factor Authentication for Clients

The `acr_values` parameter is used to specify a specific 
workflow for authentication. The value of this parameter, or the 
`default_acr_values` client metadata value, corresponds to the 
"Name" of a custom authentication script.

Out-of-the-box supported `acr` values include: 

|  ACR Value  	| Description			|
|---------------|-------------------------------|
|  u2f		| [FIDO U2F Device](../authn-guide/U2F.md)|
|  super_gluu	| [Multi-factor authentication](../authn-guide/supergluu.md)|
|  duo		| [Duo soft-token authentication](../authn-guide/duo.md)|
|  cert	| [Smart card or web browser X509 personal certificates](../authn-guide/cert-auth/)|
|  cas	| External CAS server|
|  gplus	| [Google+ authentication](../authn-guide/google.md)|
|  OTP	| [OATH one time password](../authn-guide/otp.md) |
|  asimba	| Use of the Asimba proxy for inbound SAML |
|  twilio_sms	| Use of the Twilio Saas to send SMS one time passwords |
|  passport	| Use of the [Passport component for social login](../ce/authn-guide/passport/) |
|  yubicloud	| Yubico cloud OTP verification service |
|  uaf	| experimental support for the FIDO UAF protocol |
|  basic_lock	| [Enables lockout after a certain number of failures](../authn-guide/intro/#configuring-account-lockout) |
|  basic	| [Sample script using local LDAP authentication](../ce/authn-guide/basic/) |

## OpenID Connect Client Software 

Although you can use generic OAuth client libraries, you would have 
to write some extra code to take advantage of OpenID Connect's 
security features. For example, there is no id_token in OAuth, so you 
won't find any code for id_token validation in an OAuth library. A good 
OpenID Connect client will do much of the heavy lifting for you. 

### JavaScript Client

A JavaScript client is one of the easiest ways to use OpenID Connect. 
Gluu maintains a project called [OpenID Implicit Client](https://github.com/GluuFederation/openid-implicit-client).

You'll have to add the client manually to the Gluu Server via the GUI. 
When completing the `add client` form, you can use the following 
configuration:

```
Client Name: Implicit Test Client
response_type: token id_token
Application Type: Web
Pre-Authorization: Enabled
Subject Type: public
Scopes: openid, profile, email
Response Types: token id_token
Grant Types: implicit
```

Once you have registered the client in the Gluu Server, all you need to 
do is update the `client_id`, `redirect_uri`, and `providerInfo` values 
in the login page html. Assuming you've checked out the project into a 
web accessible folder, then navigate to the page and test! 

### Server-Side libraries

Many applications are "server-side", meaning the web page displays 
content but most of the dynamic business logic resides on the web server. 
The OpenID Foundation maintains a list of client libraries on 
[their website](http://openid.net/developers/libraries). However, our 
experience has been that the quality of these libraries varies widely. 
Some are not well documented, other are not updated frequently, and some 
do not implement essential security features available in OpenID Connect. 
In addition, if a wide array of client libraries are used it becomes 
difficult to monitor and patch security vulnerabilities. For this reason, 
we recommend that you use our OpenID Connect middleware software called 
[oxd](http://oxd.gluu.org).  

oxd is not open source, but it is very reasonably priced at $0.33 per 
day per server--or ~$10/month. The code is available on 
[GitHub](https://github.com/gluufederation/oxd), and there are free 
open source oxd libraries available for PHP, Java, Python, C#, Node, 
Ruby, Perl and Go. There are also plugins available for several popular 
open source applications.

[Watch the oxd demo](http://gluu.co/oxd-demo).

[Get an oxd license for free](http://oxd.gluu.org)

### Web Server Plugins

A popular approach to protecting web applications is to use a web server 
filter to intercept the request, and make sure the person using that 
connection is authenticated and authorized. The web server with the filter 
may directly serve the application, or may proxy to a backend service. 
Leveraging the web server is a well established pattern, used by older 
access management platforms like CA Siteminder and Oracle Access Manager. 

One of the advantages of the web server filter approach is that the 
application developer does not need to know that much about the 
security protocols--if the request makes it through to the application, 
the person has been authenticated and the request is authorized. Another 
advantage is that the application security is administered by the system 
administrators, not by developers. For example, it may be easier to 
manage and audit apache configuration than to read a bunch of code. 

One of the best OpenID Connect relying party implementations was written 
by Hans Zandbelt, called [mod_auth_openidc](https://github/com/pingidentity/mod_auth_openidc). It is an authentication and authorization module for the Apache 2.x HTTP server that authenticates users against an OpenID Connect Provider (OP). The software can be found on GitHub and is included in the package management system for several Linux distributions. There are binary packages available, and if you are good at compiling C code, you can build it yourself from the source. 

Note: if you are an Nginx fan, there is a similar 
[Lua implementation](https://github.com/pingidentity/lua-resty-openidc) 
to make NGINX operate as an OpenID Connect RP or OAuth 2.0 RS. 

### AppAuth for Mobile Applications

One of the most compelling reasons to use Connect is to authenticate 
people from a mobile application. The IETF draft 
[OAuth 2.0 for Native Apps](https://tools.ietf.org/html/draft-ietf-oauth-native-apps-06) 
provides an overview of an improved design for mobile security. In 
addition to the security features of OpenID Connect, this draft suggests 
the use of a PKCE and custom URI schemes (i.e. an application can 
register a URI such as myapp:// instead of https://).

In 2016, Google released and then donated code to the OpenID Foundation 
called AppAuth for [Android](https://github.com/openid/AppAuth-android) 
and [iOS](https://github.com/openid/AppAuth-iOS). The AppAuth projects 
also include sample applications. Simulataneously, Google announced that 
it was deprecating the use of WebViews--a strategy used by mobile app 
developers which is vulnerable to malicious application code. Not only 
does AppAuth provide secure authentication, it enables SSO across the 
system browser and mobile applications. It accomplishes this by 
leveraging new operating system features that enable the system browser 
to be called by an application in an opaque view that does not enable 
an app developer to steal a person's credentials, or other applications 
to steal codes or tokens. Using this approach, mobile app developers can 
use the authorization code or hybrid flow (as described earlier). 

The Gluu Server is the only free open source OpenID Connect Provider 
that currently supports AppAuth. 

## oxAuth RP

The Gluu Server ships with an optional OpenID Connect RP web application, 
which is handy for testing.  It's called oxauth-rp. During Gluu Server 
setup, you'll be asked if you want to install it--which you should on 
a development environment. It will be deployed on `https://<hostname>/oxauth-rp`. 
Using this tool you can exercise all of the OpenID Connect API's, 
including discovery, client registration, authorization, token, 
userinfo, and end_session. 

