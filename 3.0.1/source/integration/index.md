# Gluu Server Integration Guide
The integration guide will help you understand how to integrate custom developed, open source, off-the-shelf, and SaaS web and mobile applications with your Gluu Server access management platform.  

## SaaS Applications 
Integrating SaaS applications with your Gluu Server is fairly straightforward. Presumably the app already supports SAML or OpenID Connect and provides documentation for configuring your IDP (Gluu Server) for SSO. We have documentation for configuring the Gluu Server for SSO to a few popular SaaS applications like Google and Salesforce. If we do not have a guide for configuring the app in question, simply perform a Goolge search for `<SaaS Provider> SAML` or `<SaaS Provider> OpenID Connect`. Follow the provider's instructions for configuring your IDP for SSO and test (and re-test!). 

!!!Note
    If the SaaS application in question does not already support SAML or OpenID Connect, our best advice is find a similar product or provider that does integrate with your standards-based security infrastructure. 

## Non-SaaS Applications
Two design patterns have emerged for securing custom developed, open source, and off-the-shelf applications:

1. [Use a web server filter / reverse proxy](#web-server-filter--reverse-proxy); or,
2. [Call the federation APIs directly](#server-side-client-sdks).

In the Web Server and Client SDKs sections of the integration guide we document how to use supported software to implement each approach, respectively. Which approach to pick depends on a trade-off between easier devops (option 1), and how deeply you want to integrate centralized security policies into your application (option 2).

### Web Server Filter / Reverse Proxy
The most commonly used approach for enterprise SSO has been to use a Web Server Filter / Reverse Proxy to enforce the presence of a token in an HTTP Request. If no token is present, the Web server may re-direct the person, or return a meaningful code or message to the application. The guides in the Web Server Integrations section of the docs include instructions for using Apache and Nginx software we have confirmed to work against the Gluu Server. 

### Client SDKs
The other integration option is to call the federation APIs directly in your application. In general, calling the API’s directly will enable the application to make “smarter” decisions, which can have a positive impact on usability and ultimately result in better security. Libraries exist for SAML, OpenID Connect and UMA in many languages. However, due to the complexity associated with properly implementing the APIs, we recommend using one of the supported Client SDKs covered in our documentation to help with the heavy lifting. 

!!! Note
    Given ongoing maintenance considerations, and the security implications of getting the implementation correct, we **strongly encourage** you to use our commercial OAuth 2.0 client software, [oxd](./oauth2.md/), to secure web applications. 
        
## Mobile Apps    
To integrate custom developed and open source mobile applications with your Gluu Server access management platform, use the AppAuth OpenID Connect libraries for iOS and Android written by Google.
    

