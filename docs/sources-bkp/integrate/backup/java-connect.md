# Using OpenID Connect to authenticate a person in Java

The [OpenID Connect](https://openid.net/connect/) Protocol offers Java
developers a way to authenticate a person at any Internet domain that
supports the standard. To accomplish this, the domain must provide a way
to register clients--the website and mobile applications that use the
authentication API offered by the domain.

## Discovery

Discovery is the first step! Luckily, its super-easy! All you have to 
do is make a get request to
`https://{domain}/.well-known/openid-configuration`.

This will return a JSON object, as described in the
[specification](http://openid.net/specs/openid-connect-discovery-1_0.html).
For example, you can see Gluu's OpenID Connect discovery
[url](https://idp.gluu.org/.well-known/openid-configuration).

This will tell you everything you need to know about this OpenID Connect
provider, like what are the endpoints (URLs), what crypto is supported,
and what user claims can you ask for.

An [example](https://github.com/GluuFederation/oxAuth/blob/master/RP/src/main/java/org/xdi/oxauth/action/OpenIdConnectDiscoveryAction.java)
of a Discovery Request, using the oxAuth RP library.

## Client Registration

In SAML, the website was called a "Service Provider." In OpenID Connect,
the website (or mobile application) is called a "Client". Clients can be
registered manually by the OP, but more frequently, clients use the
[Dynamic Registration
API](http://openid.net/specs/openid-connect-registration-1_0.html) to
automate the process.

## Obtaining the id_token 

After your client is registered, it is time to get down to business.
OpenID Connect offers two common workflows for authentication: basic
(where the person is using a browser, and can be re-directed) and
implicit where the client sends the credentials, including the secret.
There is a useful implements guide for
[basic](http://openid.net/specs/openid-connect-basic-1_0.html) and
[implicit](http://openid.net/specs/openid-connect-implicit-1_0.html).

## Logout 

OpenID Connect defines a mechanism for [Session
Management](http://openid.net/specs/openid-connect-session-1_0.html).
The idea is that JavaScript in a web tab can detect that another tab has
logged out. One detection of a logout event, the Web application can
cleanup sessions in any backend systems as necessary. It is not 100%
effective. If the tab is closed when the logout occurs in another tab,
the event may not be detected, and the backend systems are advised to
timeout sessions.

## Using OpenID Connect from JavaScript
See [OpenID Connect plugin for Passport](http://www.gluu.co/.qqh2) for further details.
