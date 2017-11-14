## Gluu Server SAML Intro

## Overview
SAML is an XML-based, open-standard data format for exchanging authentication and authorization data between an identity provider 
(like the Gluu Server) and a service provider (like Dropbox, O365, or your own custom SAML app etc.). 

During deployment of the Gluu Server, you will have the option to deploy multiple open source software projects to achieve two SAML workflows: [outbound SAML](#outbound-saml) and [inbound SAML](#inbound-saml).  

Review the outbound vs inbound SAML use cases described below to determine which components you might want to include in your Gluu Server deployment. 

### Outbound SAML 
Outbound SAML can also be called SP-initiated single sign-on (SSO) or traditional SAML SSO. 

In an outbound SAML transaction a website or application (SP) redirects a user to a designated Identity Provider (IDP) for authentication and authorization. The IDP asks for the user's credentials and upon successful authentication redirects the user to the protected content. 

To achieve outbound SAML SSO, during Gluu Server deployment install the Shibboleth IDP. 

With Shibboleth included in your Gluu Server deployment, you can now refer to the following docs for configuring end-to-end SAML SSO: 

- [Shibboleth SAML IDP](./outbound-saml-shib.md)    
- [Shibboleth SAML SP](../../integration/sswebapps/saml-sp.md) 

### Inbound SAML     
Inbound SAML enables you to offer SAML authentication as a front door to your digital service. In many ways, Inbound SAML is a precursor to what is now commonly referred to as "social login". A typical user flow is: 

1. User tries to access a protected resource at your application;    
2. User is redirected to a "discovery" page (presented by your IDP) that displays one or more external IDPs where the user may have an existing identity (their "home IDP");   
3. User selects their home IDP and is sent "home" for authentication;   
4. Upon successful authentication at their home IDP, the user is redirected back to your service with access to the protected resource. 

The Gluu Server supports two software options for Inbound SAML: 

- [Passport.js SAML IDP](./inbound-saml-passport.md)      
- [Asimba SAML Proxy](./inbound-saml-asimba.md)   

Of the two options, **we recommend using Passport.js SAML for inbound SAML SSO**. Key management is more complicated in Asimba, and using Asimba requires modifications to be made in configuration files.

!!! Note
    For a realworld example of inbound SAML, check out the [Federated Login flow at EDUCAUSE](https://sso-users.educause.edu/?resumePath=%2Fidp%2FZQ4DF%2FresumeSAML20%2Fidp%2FstartSSO.ping&allowInteraction=true&reauth=false). 

## SAML vs. OpenID Connect  

SAML is stable and mature, and is well supported at many of the Internet's largest domains. 

However, the last major release of SAML was in 2005! So if your target application doesn't already support SAML, or for new application development, we recommend using using the OAuth 2.0 profile for federated identity: [OpenID Connect](./openid-connect.md). 

The following considerations might help you determine when to use SAML, and when to use OpenID Connect:

- If you have an application that already supports SAML, **use SAML**.
- If you need to support user login at an external IDP (like a customer or partner IDP), **use SAML**.
- If you have a mobile application, **use OpenID Connect**.
- If you are writing a new application, **use OpenID Connect**.




