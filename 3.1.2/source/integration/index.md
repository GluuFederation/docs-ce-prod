# Single Sign-On (SSO) Integration Guide
The SSO integration guide offers a list of supported SAML and OpenID Conenct "client" (SP/RP) software projects that can be used to secure and integrate web and mobile applications with the Gluu Server IDP. 

Unless otherwise noted, all software in the integration guide is free open source software (FOSS).

!!! Warning
    Gluu will **not** support any SAML, OpenID Connect, or OAuth client software other than the projects listed below (including custom written clients!). 
    
## Server Side Web Apps
Many applications are "server-side", meaning the web page displays content but most of the dynamic business logic resides on the web server. Two design patterns have emerged for securing server-side web applications: 

1. Web server filters and reverse proxies;            
1. Leveraging OAuth 2.0 directly in your application. 

Option 1 offers easier devops. Option 2 enables a tighter integration with centralized security policies into your application.

### Web Server Filters
Web Server filters are a tried and true approach to achieving SSO with web applications. The web server filter enforces the presence of a token in a HTTP Request. If no token is present, the Web server may re-direct the person, or return a meaningful code or message to the application. Your devops team will love this approach–they can just manage the web server configuration files. It will be crystal clear to them what policies apply to what URLs. 

Gluu supports the following SAML and OpenID Connect web server filters: 
  
- SAML: [Shibboleth SP](./sswebapps/saml-sp.md)     

- OpenID Connect: [Apache mod_auth_openidc](./sswebapps/openidc-rp.md), [Nginx lua-resty-openidc](https://github.com/zmartzone/lua-resty-openidc)

### Client Software 
Client software performs some of the heavy lifting for developers around leveraging OAuth 2.0 in applications. Calling API’s directly enables “smarter” handling of authentication and authorization in applications. For example, transaction level security can be more easily implemented by calling OAuth 2.0 APIs directly. This approach will have a positive impact on usability and security. 

Gluu supports the following software to secure and integrate server-side web applications:

- [oxd](https://gluu.org/docs/oxd) (commercial software)

## Single Page Apps
Single Page Applications (SPAs) can be seen as a mix between traditional Web SSO and API access: the application itself is loaded from a (possibly protected) regular website and the Javascript code starts calling APIs in another (or the same) domain(s). For this use case, the OpenID Connect spec points to using the “Implicit grant type” for passing token(s) to the SPA since that grant was specifically designed with the “in-browser client” in mind. 

Gluu supports the following software to secure and integrate SPA’s:

- [AppAuth JS](https://github.com/openid/AppAuth-JS/)
- [Gluu's OIDC JS Client](./spa/oauth-js-implicit.md)


## Native Apps
To integrate native apps with your Gluu Server, we recommend the AppAuth libraries for iOS , MacOS, and Android. AppAuth strives to directly map the requests and responses of those specifications, while following the idiomatic style of the implementation language. In addition to mapping the raw protocol flows, convenience methods are available to assist with common tasks like performing an action with fresh tokens.

Gluu supports the following software to secure and integrate native apps:

- [AppAuth iOS and macOS](https://github.com/openid/AppAuth-iOS)
- [AppAuth Android](https://github.com/openid/AppAuth-Android)

## SaaS / Off-the-shelf Applications 
Integrating SaaS and off-the-shelf applications with your Gluu Server should be fairly straightforward. Presumably the app already supports SAML or OpenID Connect and provides documentation for configuring your IDP (Gluu Server) for SSO. 

There is existing Gluu documentation for configuring SSO to popular applications like [Google](./saas/google.md) and [Salesforce](./saas/salesforce.md). If there is not an existing guide, perform a Goolge search for `<SaaS Provider> SAML` or `<SaaS Provider> OpenID Connect`. Follow the provider's instructions for configuring your IDP for SSO and test (and re-test!). 

- Refer to the [OpenID Connect Provider (OP) documentation](../admin-guide/openid-connect.md) for configuring your Gluu OP for SSO
- Refer to the [SAML Identity Provider (IDP) documentation](../admin-guide/saml.md) for configuring your Gluu SAML IDP for SSO

!!!Note
    If the SaaS application in question does not already support SAML or OpenID Connect, our best advice is find a similar product or provider that does integrate with your standards-based security infrastructure. 



