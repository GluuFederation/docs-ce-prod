# Gluu Server Community Edition (CE) 3.0.1 Documentation
## Introduction
The Gluu Server is a free open source identity and access management 
(IAM) platform. The most common use case for the Gluu Server is Single 
Sign-On (SSO). Other common use cases include mobile authentication, 
API access management, two-factor authentication, customer identity
and access management (CIAM), and identity federation. 

The Gluu Server is a container distribution composed of software written by Gluu and incorporated from other open source projects. Gluu
projects are frequently prefixed with our open source handle: **ox** (e.g. oxAuth, oxTrust). Any code in the Gluu Server that we wrote is MIT license, and is available on [Github](https://github.com/GluuFederation/). 

SaaS, custom, open source and commercial software can be made more 
secure by leveraging a central authentication and authorization service. 
Because there are so many different kinds of apps, there is no way to 
"top down" implement proprietary security mechanisms. This is why
open standards are so important for IAM. 

While there are many open protocols for IAM, Gluu focuses on just a few. 
Consolidation saves money, and one-off integrations should be avoided. 
Our goal was to support the most widely adopted older protocols, and the 
most promising new protocols. 

The Gluu Server supports the following open web standards for 
authentication, authorization, federated identity, and identity management:

- OAuth 2.0    
- SAML 2.0   
- OpenID Connect    
- User Managed Access (UMA)    
- Simple Cloud Identity Management (SCIM)    
- FIDO Universal 2nd Factor (U2F)    
- Lightweight Directory Access Protocol (LDAP)   

If this is your first exposure to the Gluu Server, welcome to the 
community! We want to see the ecosystem flourish, and ultimately make 
the Internet a safer, more privacy protected place. In order to do that, 
we believe we need to keep the Gluu Server free so all kinds of 
organizations can use, contribute and benefit from the software.

These docs are not perfect! Please help us make them so by submitting
any improvements to our [Documentation Github](https://github.com/GluuFederation/docs).
If you're a Github pro, submit a pull request. If not, just open an issue
on any typos, bugs, or improvements you'd like to see. We need your
help... even if you're not a coder, you can contribute! 

##  oxd Client Software
Gluu offers commercial OAuth 2.0 client software called [oxd](https://oxd.gluu.org) to make securing and integrating applications with the Gluu Server easier. Your application can use any client software that implements the open standards the Gluu Server supports, but you may want to consider using oxd for the following reasons:
 
1. oxd is super-easy to use; 
2. We keep updating oxd to address the latest OAuth 2.0 security knowledge; 
3. We can provide more complete end-to-end support if we know both the client and server software;
4. oxd subscriptions help support this project so you can see more enhancements faster; 
5. There are oxd libraries for Php, Python, Java, Node, Ruby, C#, Perl and Go. If your application is programmed in another language, oxd has a simple JSON/REST API;
6. There are oxd plugins for many popular applications like: Wordpress, Drupal, Magento, OpenCart, SugarCRM, SuiteCRM, Roundcube, Shopify, and Kong. More are being added too. Next on the list are: MatterMost, RocketChat, NextCloud, and Liferay.

[Read the docs](http://oxd.gluu.org/docs)

## Support

We are committed to providing free community support! You can browse or register and post 
your questions on [Gluu support](https://support.gluu.org). All community
questions are public, and we do our best to answer them in a timely 
manner. 

Private support, guaranteed response times, and consultative 
support are available to organizations who purchase a support contract. For
more information, see [our website](https://gluu.org/pricing).

## License

All of Gluu's open source software is published under an
[MIT License](http://opensource.org/licenses/MIT). The licenses 
for other components are listed below.

|	Component	|	License	            |
|-----------------------|---------------|
|	Shibboleth IDP      | [Apache2](http://www.apache.org/licenses/LICENSE-2.0)|
|	OpenLDAP	        | [OpenLDAP Public License](http://www.openldap.org/software/release/license.html)|
|	Asimba		        | [GNU APGL 3.0](http://www.gnu.org/licenses/agpl-3.0.html)|
|	OpenDJ		        | [CDDL](https://forgerock.org/cddlv1-0/)|
|  UnboundID LDAP SDK	| [UnboundID LDAP SDK Free Use License](https://github.com/UnboundID/ldapsdk/blob/master/LICENSE-UnboundID-LDAPSDK.txt)|
| Passport-JS           | [MIT License](https://github.com/jaredhanson/passport/blob/master/LICENSE) |
| Jetty / Apache HTTPD  | [Apache2](http://www.apache.org/licenses/LICENSE-2.0)|
