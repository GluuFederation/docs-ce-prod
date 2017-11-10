## Gluu Server SAML Intro

## Overview
SAML is an XML-based, open-standard data format for exchanging authentication and authorization data between an identity provider 
(like the Gluu Server) and a service provider (like Dropbox, O365, etc.). 

SAML is a stable and mature standard, and is well supported at many of the Internet's largest domains. 

However, the last major release of SAML was in 2005! Therefore it is important to understand when to use SAML and when to use a newer protocol like OpenID Connect to achieve your identity goals. 

Use the following bullet points to help determine when to use SAML, and when to user a newer protocol like OpenID Connect:

- If you have an application that already supports SAML, use SAML.
- If you need to support user login at an external IDP (like a customer or partner IDP), use SAML.
- If you have a mobile application, use OpenID Connect.
- If you are writing a new application, use OpenID Connect.

If you are continuing with the SAML documentation it is presumed your use case aligns with one or both of the first two bullet points above. If not, we recommend that you review the [OpenID Connect](./openid-connect.md) portion of the Gluu Server docs. 

### Outbound vs. Inbound SAML 
There are two main SAML authentication workflows: outbound SAML and inbound SAML. 

Outbound SAML can also be called SP-initiated Single Sign-On (SSO) or traditional SAML. 
In an outbound SAML transaction a website or application (SP) redirects a user to a 
designated Identity Provider (IDP) for authentication and authorization. 
The IDP asks for the user's credentials and upon successful authentication redirects the user to the protected content. 

Inbound SAML enables an organization to offer SAML authentication as a front door to their digital service. Inbound SAML is a common requirement for SaaS providers who need to support the authentication requirements of large enterprise customers.

The typical user flow for inbound SAML is as follows: 

1. User tries to access your protected resource;    
2. User is redirected to a discovery page (presented by your IDP) that presents one or more external IDP's where the user may have an existing identity (their "home IDP");   
3. User selects their home IDP and is sent for authentication;   
4. Upon successful authentication at their home IDP, user is redirected back to your service with access to the protected resource. 

The Gluu Server bundles separate components to support both workflows (installation of each component is optional during Gluu Server deployment):

- For outbound SAML, the Gluu Server bundles the [Shibboleth SAML IDP](#outbound-saml-shibboleth). 

- For inbound SAML, the Gluu Server bundles the [Asimba SAML Proxy](#inbound-saml-asimba). 

Documentation for each service follows in the sections below. 
