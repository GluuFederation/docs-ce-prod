# SAML IP 
## Overview
If you need a SAML IDP to support outbound SAML single sign-on (SSO), you can install Shibboleth during your [Gluu Server deployment](../../installation-guide/install.md).      

In an outbound SAML SSO transaction a website or application (SP) redirects a user to a designated identity provider (IDP) for authentication and authorization. The IDP will authenticate the user. Upon successful authentication, the user is sent back to the SP logged in. 

In order for this transaction to happen successfully there must be pre-established trust between your IDP (Gluu Server) and SP (target application). The following section of the docs cover how to create trust with SPs in your Gluu SAML IDP. 

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

A description of each field follows:

- **Display Name**: Name of the Trust Relationship (it should be unique for every TR);       
- **Description**: Purpose of the TR and an SSO link can be added here;         

- **Metadata Type**: There are four available options to choose from. The correct Type depends on how the SP is delivering Metadata to your IDP.      

    - *File*: Choose `File` if the SP has provided an uploadable metadata document in XML format.
    - *URI*: Chose `URI` if the SP metadata is hosted on a URI that is accessible from the Internet.
    - *Generate*: Choose `Generate` if the SP is an "in-house application" or the “Shibboleth SP” is going to be installed in the target application (SP). This option will generate a how-to guide for installing the Shibboleth SP. 
    - *Federation*: Choose this option if the target application (SP) is affiliated with a federation service (e.g. InCommon, NJEdge etc.). Learn more about working with a federation [below](#federation-configuration).   
    
!!! Note 
    If you plan on using the Generate method, please note the following:       
    
    - The URL is the hostname of the SP.           
    - You must provide a **non password protected** public certificate, which is a Base64 encoded ASCII file, and contain "-----BEGIN CERTIFICATE-----" and "-----END CERTIFICATE-----".        
    - After creating the Trust Relationship, download the generated configuration files from the `Download Shibboleth2 configuration files` link and place these configuration files inside your SP configuration.              
      
- **Released**: The SPs required attributes must be added to this panel. The required attributes can be selected from the menu on the left with the heading “Release Additional Attributes”.     

- **Entity Type**: You have two options to choose for entity type.
    - *Single SP*: 
    - *Federation/Aggregate* 
    
The Trust Relationship(TR) can be added by clicking the `Add` button located in the lower left side of the page.     

## Relying Party Configuration     
Through the Relying Party configuration you can customize how different IDP profiles will respond to requests received from the SP, including encryption and digital signature options. The underlying IDPs functionality is described in [the Shibboleth wiki](https://wiki.shibboleth.net/confluence/display/IDP30/RelyingPartyConfiguration). 

oxTrust allows you to tweak a limited subset of profiles mentioned in the Shibboleth wiki. The [SAML2SSO profile](https://wiki.shibboleth.net/confluence/display/IDP30/SAML2SSOConfiguration) is the most commonly used browser SSO profile. 

The "Configure Relying Party" checkbox is accessible on the TR creation page and must be enabled with a specific profile(s) selected as active for this TR to generate a valid configuration. In most cases, just adding the SAML2SSO profile with default settings will suffice.

![enable-relying-party.png](../img/saml/enable-relying-party.png)     

Setting the checkbox will result in a link which, if clicked, will summon a list of profiles currently available for customization. Each entry in the list has a brief description of its purpose and a selection of settings for which custom values may be chosen, as can be seen on image below.     

![tr-relying-party](../img/saml/tr-relying-party.png)     
    
## Federation Configuration     
If the SP is part of an identity federation such as [InCommon](https://www.incommon.org/participants/), the Gluu administrator must add the federation as an SP in the Gluu Server. This will enable the administrator to more easily create TRs with SPs in the federation. 

The example below shows how an administrator would add a TR for the InCommon Federation.

Once a TR has been established with the federation, the Gluu Server administrator can easily create TRs with any SP included in the federation by selecting the federation from the `Federation Name` drop down menu and selecting the entity-id for the SP. 

In the example below we are creating a TR for the 'Internet2 Wiki', which is an InCommon Federation affiliated SP (meaning, the SPs entityID is available in InCommon metadata). 

![Incommon_affiliated_SP_Trust.png](../img/saml/InCommon_affiliated_SP_Trust.png)

## Securing Apps with SAML
If your target application (SP) does not already support SAML, we recommend using the [Shibboleth SP](../../integration/sswebapps/saml-sp.md) web server filter to secure and integrate the application with your Gluu SAML IDP. 


## Inbound SAML (Asimba)
Inbound SAML allows users from external domains to login at their home identity provider to gain access to resources protected by the Gluu Server. The Gluu Server uses an open source product called [Asimba](http://www.asimba.org/site/) to normalize inbound SAML. 

![asimba-overview](../img/asimba/Asimba_graph.jpg)

### End to End configuration of Asimba in Gluu Server v3

For this documentation we used three demo servers:

- https://[proxy3_hostname] is the Gluu server v3 with Shibboleth and Asimba installed along with other default components. 
- https://[idp_hostname] is the remote authentication Gluu server v2 with Shibboleth installed with other default components. 
- https://[sp_hostname] is the remote SP Gluu Server with the Shibboleth SP v26 installed.
  
This doc is divided into three major parts. Configuration in proxy server, configuration of remote AuthN server and Service Provider. 
In this whole setup we are using Gluu Servers, it's associcated open source pieces and all other well developed and maintained softwares like Shibboleth Service Provider. 

Let's start! 

#### Gluu-Asimba Server Configuration

##### Custom interception script named 'asimba' configuration

  - Log into oxTrust
  - `Configuration` > `Manage Custom Script`
  - Script name 'asimba'
    - asimba_saml_certificate_file: /etc/certs/saml.pem [ Make sure you copy ingredient of `asimba.crt` into `saml.pem` with "BEGIN CERTIFICATE" and "END CERTIFICATE" header and footer] 
    - asimba_entity_id: https://[proxy3_hostname]/saml
    - saml_deployment_type: enroll
    - saml_use_authn_context: false
    - saml_idp_sso_target_url: https://[proxy3_hostname]/asimba/profiles/saml2/sso/web
    - user_object_classes: eduPerson, gluuCustomPerson
    - saml_idp_attributes_mapping: {"uid": ["uid"], "mail": ["mail"], "issuerIDP": ["issuerIDP" ] }
    - enforce_uniqueness_attr_list: issuerIDP, uid
    - saml_generate_name_id: true
    
##### SP Requestor

  - Create a SAML metadata for native SP requestor of asimba. Grab the copy of from below and replace [proxy3_hostname] with your own server's hostname. Make sure to unix format it. 
  - `SAML` > `SP Requestors`
  - 'Add SP Requestor'
    - ID: https://[proxy3_hostname]/saml
    - Friendly Name: oxAuth SAML
    - Metadata URL: Not required
    - Metadata Timeout: -1
    - Metadata File: You can get an example script's metadata from [here](./saml_script_metadata.xml). Edit it to substitute `[proxy3_hostname]` placeholder with a real hostname your instance uses. Upload the resulting metadata to the requestor
    - Trust Certificate File: Not required
    - Properties: Not required
    - Enabled: Yes
    - Signing: No

##### Add External IDP/AuthN Server

 - `SAML` > `IDPs`
 - 'Add IDP' 
   - ID: EntityID of remote IDP. i.e. https://[idp_hostname]/idp/shibboleth
   - Friendly Name: Remote AuthN Server 1
   - Metadata URL: Not required
   - Metadata Timeout: -1
   - Metadata File: upload metadata
   - Trust Certificate File: Grab SAML metadata from remote IDP and upload that. This certificate must be no password protected and x509 format crt. If remote IDP is another Gluu Server then grab 'shibIDP.crt' from /etc/certs/ of that server.
   - NameIDFormat: urn:oasis:names:tc:SAML:2.0:nameid-format:transient [ If your remote AuthN server is also a Gluu Server ]. This NameID might vary according to various types of AuthN server. 
   - Enabled: Yes
   - Send Scoping in AuthNRequest: Yes
   - AllowCreate: Yes
   - Disable SSO for IDP: No
   - ACS index: Yes
   - Send NameIDPolicy: Yes
   - Avoid Sujbect Confirmations: No

##### asimba.xml file configuration

 - Modification of 'asimba.xml' file: 
   - location: `/etc/gluu/conf/asimba/asimba.xml`
   - Enable and uncomment whitelist of attributes: 
```
<gather>
       <attribute name="whitelist-attribute-name" />
</gather>
```
   - Allow all released attributes, add this `<attribute name="*" />` in attribute release policy: 
```
<attributerelease class="com.alfaariss.oa.engine.attribute.release.configuration.ConfigurationFactory">
        <policy id="asimba.releasepolicy.1" friendlyname="Default Attribute Release policy" enabled="true">
               <attribute name="firstname" />
               <attribute name="lastname" />
               <attribute name="email" />
               <attribute name="role" />
               <attribute name="country" />    <!-- country is defined in <global ..> attribute section -->
               <attribute name="*" />
...
  ...

```
 - Restart asimba service with 'service asimba restart'
 
##### Create custom attribute 'issuerIDP'

You need to create a custom attribute named 'issuerIDP' in this stage. Here is how you can create [custom attributes](./attribute.md#custom-attributes).


#### Remote AuthN Server Configuration

##### Create Trust Relationship

 - Download you Asimba server's metadata with https://[proxy3_hostname]/asimba/profiles/saml2 and save it as 'gluu_asimba_server_metadata.xml'
 - Log into Authentication server oxTrust ( or, management console GUI )
 - Create a new trust relationship with this metadata which you just downloaded.
 - Relying Party Configuration: 
    - SAML2SSO Profile: 
       - signResponses: conditional
       - signAssertions: never
       - signRequests: conditional
       - encryptAssertions: never
       - encryptNameIds: never
  - Attribute: Release transientID and Username attribute
  
##### New test user registration

###### Enable 'User Registration' module: 
  - Log into oxTrust
  - 'Manage Custom Scripts'
  - 'User Registration' tab
    - Custom property: enable_user = true
    - 'Enable' it
    - Hit 'Update'

###### New user registration

 - Hit 'https://[idp_hostname]/identity/register
 - Fill up the form and new user will be registered
 - We will use this user to test our SSO

#### Remote SP Configuration

##### Shibboleth SP installation

- Prepare your SP instance by following this doc: https://gluu.org/docs/ce/3.0.2/integration/webapps/saml-sp/#super-quick-ubuntu-shib-apache-install

##### shibboleth2.xml configuration

 - Download Shibboleth metadata of your Gluu-Asimba server with 'https://[prox3_hostname]/idp/shibboleth'
 - Put it inside /etc/shibboleth/ location
 - Modify 'shibboleth2.xml' file like below: 
   - SSO entityID: 
```
<SSO entityID="https://[proxy3_hostname]/idp/shibboleth"
     discoveryProtocol="SAMLDS" discoveryURL="https://ds.example.org/DS/WAYF">
     SAML2 
</SSO>
```
   - Metadata provider: 
```
<MetadataProvider type="XML" file="proxy3_gluu_org_shib.xml"/>
```
   - Restart shibd and apache2
   
#### Trust Relationship in Gluu-Asimba server

We need to create a trust relationship in Gluu-Asimba server with Shibboleth SP metadata.

 - Log into oxTrust
 - Grab Shibboleth SP metadata. You can get that with https://[sp_hostname]/Shibboleth.sso/Metadata


#### Test SSO

 - Log into Gluu-Asimba server. 
 - 'Manage Custom Scripts'
   - 'Person Authentication' tab
     - 'Enabled' `basic` authentication script
     - 'Enabled' `asimba` authentication script
 - 'Manage Authentication' 

