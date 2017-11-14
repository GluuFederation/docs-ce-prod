# Outbound SAML using Shibboleth
## Overview
If you need a SAML IDP to support outbound SAML single sign-on (SSO), you can install Shibboleth during your [Gluu Server deployment](../../installation-guide/install.md).      

In an outbound SAML SSO transaction a website or application (SP) redirects a user to a designated identity provider (IDP) for authentication and authorization. The IDP will authenticate the user. Upon successful authentication, the user is sent back to the SP logged in. 

In order for this transaction to happen successfully there must be pre-established trust between your IDP (Gluu Server) and SP (target application). 

The following section of the docs cover how to create trust with SPs in your Gluu Server IDP. 

## Trust Relationship Requirements     
In the Gluu Server, the SAML IDPs SSO configuration is called a Trust Relationship (TR). Each TR requires the infomation listed below.

### Metadata of the SP             
Metadata is an XML file which has configuration data used to establish trust between the website (SP) and IDP (Gluu Server). Websites (SP) can provide metadata via a URL or as a separate file. Metadata can change, so a static URL typically requires the least amount of ongoing maintenance. 

### Metadata of the Gluu Server       
The Gluu Server's SAML metadata may be needed from time to time. It can be found at `https://hostname/idp/shibboleth`.
  
### Attribute Release      
Each SP may require one or more user attributes from the IDP in order to grant a person access to a protected resource. Required attributes vary depending on the application, and should be explicitly specified in the target application's documentation. The administrator can use the oxTrust interface to release the necessary attributes to the SP (as described [below](#create-a-trust-relationship-in-the-gluu-server). 

!!! Note    
    For a broader discussion of attributes, including how to create custom attributes and how to [configure the NameID attribute](./attribute/#defining-nameid) for your SAML service, refer to the [attributes documentation](./attribute.md).
    
## Create a Trust Relationship
Follow these instructions to create a SAML TR in your Gluu Server: 

1. Go to `SAML` > `Trust Relationships`    
2. Click on `Add Trust Relationship`     
3. A new page will appear where you can provide all the required information to create a Trust
  Relationship(TR).     

![newTR](../img/saml/samlfederationTR.png)

* _Display Name_: Name of the Trust Relationship (it should be unique for every TR)     
* _Description_: Purpose of the TR and an SSO link can be added here.    
* _Metadata Type_: There are four available options to choose from. The correct Type depends on how the SP is delivering Metadata to your IDP.      
    * _None_
    * _File_: Choose `File` if the SP has provided an uploadable metadata document in XML format.
    * _URI_: Chose `URI` if the SP metadata is hosted on a URI that is accessible from the Internet.
    * _Generate_: Choose `Generate` if the SP is an "in-house application" or the “Shibboleth SP” is going to be installed in the target application (SP). This option will generate a how-to guide for installing the Shibboleth SP. If you plan on using the Generate method, please note the following:          
            * _URL_ : This is the hostname of the SP.     
            * _Public certificate_ : You must provide the certificate, which is a Base64 encoded ASCII file, and contain "-----BEGIN CERTIFICATE-----" and "-----END CERTIFICATE-----". This certificate **can not** be password protected.               
            * After creating the Trust Relationship, download the generated configuration files from the `Download Shibboleth2 configuration files` link and place these configuration files inside your SP configuration.         
    * _Federation_: Choose this option if the target application (SP) is affiliated with a federation service (e.g. InCommon, NJEdge etc.). Once you select `Federation` as the Metadata Type, another drop down menu called `Select Federation` will appear. From this drop menu you can select the appropriate federation. After selecting the `Federation Name`, a new link called `Click to select
entity id` will appear. Use this link to find and select the SP entityIDs that you wish to create SSO with. Learn more about working with a federation [below](#federation-configuration).     

* _Released_: The SPs required attributes must be added to this panel. The required attributes can be selected from the menu on the left with the heading “Release Additional Attributes”.     
* _Entity Type_: You have two options to choose for entity type.
    * _Single SP_: 
    * _Federation/Aggregate_
    
The Trust Relationship(TR) is added by clicking the `Add` button located in the lower left side of the page.     

## Relying Party Configuration     
This feature allows to further customize how different IDPs profiles will respond to requests received from this SP, including encryption and digital signature options. The underlying IDPs functionality is described in [the Shibboleth Wiki](https://wiki.shibboleth.net/confluence/display/IDP30/RelyingPartyConfiguration). 

oxTrust allows you to tweak a limited subset of profiles mentioned in the Shibboleth wiki (linked above). For our purposes, the [SAML2SSO profile](https://wiki.shibboleth.net/confluence/display/IDP30/SAML2SSOConfiguration) is the most common browser SSO profile used in today's SAML world. 

The "Configure Relying Party" checkbox is accessible on the TR Creation page and must be enabled with a specific profile(s) selected as active for this TR to generate a valid configuration. In most cases, just adding SAML2SSO profile with default settings to the list to the right will do.

![enable-relying-party.png](../img/saml/enable-relying-party.png)     

Setting the checkbox will result in a link which, if clicked, will summon a list of profiles currently available for customization. Each entry in the list has a brief description of its purpose and a selection of settings for which custom values may be chosen, as can be seen on image below.     

![tr-relying-party](../img/saml/tr-relying-party.png)     

!!! Note     
    If the target application doesn't already make use of legacy protocols like SAML, and your project or organization are just about to add SSO/federation capabilities to it, we strongly recommend consider using OpenID Connect rather than SAML. OpenID Connect offers newer, easier to use approaches to solutions for the same problems, and follows modern best practices while doing it. You can learn more about it in our blog here: [OAuth vs. SAML vs. OpenID Connect](http://gluu.co/oauth-saml-openid).
    
## Federation Configuration     
If the SP is part of an identity federation such as [InCommon](https://www.incommon.org/participants/), the Gluu administrator must add the federation as an SP in the Gluu Server. 

This will enable the administrator to more easily create TRs with SPs in the federation. The example below shows how an administrator would add a TR for the InCommon Federation.

Once a TR has been established with the federation, the Gluu Server administrator can easily create TRs with any SP included in the federation by selecting the federation from the `Federation Name` drop down menu and selecting the entity-id for the SP. As for example here we are creating 'Internet2 Wiki' Trust Relationship which is InCommon affiliated ( that means, SP's entityID is available in InCommon metadata ). 

![Incommon_affiliated_SP_Trust.png](../img/saml/InCommon_affiliated_SP_Trust.png)

## Securing Apps with SAML
If your target application (SP) does not already support SAML, we recommend using the [Shibboleth SP](../../integration/sswebapps/saml-sp.md) web server filter to secure and integrate the application with your Gluu SAML IDP. 

