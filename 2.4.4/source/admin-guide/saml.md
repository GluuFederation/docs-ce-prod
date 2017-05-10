# SAML
## Overview
SAML is an XML-based, open-standard data format for exchanging 
authentication and authorization data between an identity provider 
(like the Gluu Server) and a service provider (like Dropbox, O365, etc.). 
SAML is a stable and mature standard, and is well supported at many of the 
Internet's largest domains. However, the last major release of SAML was in 2005! 
Therefore it is important to understand when to use SAML and when to use a 
newer protocol like OpenID Connect to achieve your identity goals. 

Refer to these four considerations to determine which protocol 
to use for single sign-on (SSO):

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
2. User is redirected to a discovery page (presented by your IDP) that presents one or more external IDP's that they may have existing credentials at (their "home IDP");   
3. User selects their home IDP and is sent for authentication;   
4. Upon successful authentication at their home IDP, user is redirected back to your service with access to the protected resource. 

The Gluu Server bundles separate components to support both workflows (installation of each component is optional during Gluu Server deployment):

- For outbound SAML, the Gluu Server bundles the Shibboleth SAML IDP. 

- For inbound SAML, the Gluu Server bundles the Asimba SAML Proxy. 

Documentation for each service follows in the sections below. 
 
## Outbound SAML (Shibboleth)
Outbound SAML can also be called SP-initiated Single Sign-On (SSO) 
or traditional SAML. In an outbound SAML transaction a website or application (SP) 
redirects a user to a designated Identity Provider (IDP) for authentication 
and authorization. The IDP will ask for the user's credentials and upon successful 
authentication, the user is sent back to the SP logged in. 

In order for this transaction to happen successfully there must be pre-established 
trust between the IDP and the SP. In the Gluu Server, the IDPs SSO configuration is 
called a Trust Relationship (TR). The following sections cover how to create a TR in the Gluu Server. 

!!! Note
    For any outbound SAML transaction, a trust relationship must be created in the IDP.

### Trust Relationship Requirements     
Each Trust Relationship requires the infomation listed below.

**Metadata of the SP**       
Metadata is an XML file which has configuration data used to establish trust between the website (SP) and IDP (Gluu Server). Websites (SP) can provide metadata via a URL or as a separate file. Metadata can change, so a static URL typically requires the least amount of ongoing maintenance. 
  
**Required Attributes**      
Each SP may require one or many attributes in order to grant a user access. 
Required attributes vary depending on the application, and should be 
explicitly listed in the application's documentation. The Gluu Server ships with 
certain preconfigured attributes and also supports the creation of custom attributes. 
Once the attributes are available in the Gluu Server, the administrator only needs 
to click on the desired attribute(s) and it will be released to the SP upon 
successful user authentication.

### Create a Trust Relationship in the Gluu Server       
* Go to `SAML` > `Trust Relationships`
* Click on `Add Trust Relationship`
* A new page will appear where you can provide all the required information to create a Trust
  Relationship(TR).

![newTR](../img/saml/newTR.png)

* _Display Name_: Name of the Trust Relationship (it should be unique for every trust relationship)     
* _Description_: Little description. Purpose and SSO link can be added here.    
* _Metadata Type_: There are four available options to choose from. The correct Type depends on how the SP is delivering Metadata to your IDP.      
    * _File_: Choose File if the SP has provided an uploadable metadata document in XML format.
    * _URI_: Chose URI if the SP metadata is hosted on a URI that is accessible from the Internet.
    * _Generate_: Choose Generate if the SP is an "inhouse application" or the “Shibboleth SP” is going to be installed in the target application (SP). This option will generate a how-to guide for installing the Shibboleth SP. If you plan on using the Generate method, please note the following:          
            * _URL_ : This is the hostname of the SP.     
            * _Public certificate_ : You must provide the certificate, which is a Base64 encoded ASCII file, and contain "-----BEGIN CERTIFICATE-----" and "-----END CERTIFICATE-----". This certificate **can not** be password protected.               
            * After creating the Trust Relationship, download the generated configuration files from the `Download Shibboleth2 configuration files` link and place these configuration files inside your SP configuration.         
    * _Federation_: Choose this option if the target application (SP) is affiliated with a federation service (e.g. InCommon, NJEdge etc.). Once you select “Federation” as the Metadata Type, another drop down menu called “Select Federation” will appear. From this drop menu you can select the appropriate federation. After selecting the “Federation Name”, a new link called “Click to select
entity id” will appear. Use this link to find and select the SP entityIDs that you wish to create SSO with. Learn how to establish trust with a federation [below](#federation-configuration).     

* _Released_: The SPs required attributes must be added to this panel. The required attributes can be selected from the menu on the left with the heading “Release Additional Attributes”.     

The Trust Relationship(TR) is added by clicking the `Add` button located in the lower left side of the page.     

### Relying Party Configuration     
If the target application does not already support SAML, the Relying Party software must be configured. The relying party configuration is accessible on the TR Creation page. The checkbox `Configure specific Relying Party` must be checked.     

![enable-relying-party.png](../img/saml/enable-relying-party.png)     

The checkbox will result in a link which can be accessed to find information about configuring the relying party for the TR. The image below shows the relying party config panel from which the administrator can add the specific option.     

![tr-relying-party](../img/saml/tr-relying-party.png)     

!!! Note     
    If the target application does not already support a federation standard like SAML, and you or the developer are planning on adding federation to the application, we strongly recommend using OpenID Connect rather than SAML. OpenID Connect is newer, easier to use, and follows modern best practices. Learn more in our blog: [OAuth vs. SAML vs. OpenID Connect](http://gluu.co/oauth-saml-openid).
    
### Federation Configuration     
If the SP is part of an identity federation such as InCommon, the administrator must add the federation as an SP in the Gluu Server. This will enable the administrator to more easily create TRs with SPs in the federation. The example below shows how an administrator would add a TR for the InCommon Federation.

![federationTR](../img/saml/federationTR.png)

Once a TR has been established with the federation, the Gluu Server administrator can easily create TRs with any SP included in the federation by selecting the federation from the `Federation Name` drop down menu and selecting the entity-id for the SP.

![federation-entityid.png](../img/saml/federation-entityid.png)

## Inbound SAML (Asimba)
Inbound SAML allows users from external domains to login at their home identity provider to gain access to resources protected by the Gluu Server. The Gluu Server uses an open source product called [Asimba](http://www.asimba.org/site/) to normalize inbound SAML. 

The following documentation provides a step-by-step guide for configuring Asimba with two (2) IDPs and a single (1) SP. The guide includes use of a SAML interception script which is shipped with the Gluu Server and simplifies the process of using Asimba. The administrator can add multiple IDPs or SPs (as required) using the method outlined below. Each SP and IDP must be connected to the IDP that has the Asimba module enabled.

!!! Note 
    A description of the SAML interception script is available [here](https://github.com/GluuFederation/oxAuth/tree/master/Server/integrations/saml).

![asimba-overview](../img/asimba/Asimba_graph.jpg)
  
### Notes
  - For this documentation and we used three demo servers:
     - `https://[proxy_hostname]` is the proxy Gluu server with Shibboleth and Asimba installed.
     - `https://[idp_hostname]` is the remote authentication Gluu server with Shibboleth installed.
     - `https://[sp_hostname]` is the remote SP Gluu Server with the Shibboleth SP installed.
  - For this documentation we use the Gluu Server version 2.4.4.2 and the Shibboleth SP version 2.6.
  

### Gluu-Asimba Server Configuration

#### Custom Interception script named saml/asimba configuration

 - Log into oxTrust
 - Configuration -> Manage Custom Scripts
 - Script name 'saml'
   - Custom property ( key/value ):
     - asimba_entity_id: `https://[proxy_hostname]/saml`
     - enforce_uniqueness_attr_list: issuerIDP, uid
     - saml_deployment_type: enroll_all_attr
     - saml_idp_attributes_mapping: { "attribute_name": ["attribute_name", "SAML2 URI"] }
       - example: ``` {"uid": ["uid", "urn:oid:0.9.2342.19200300.100.1.1"], "mail": ["mail", "urn:oid:0.9.2342.19200300.100.1.3"], "issuerIDP": ["issuerIDP" ] } ```
     - saml_idp_sso_target_url: `https://[proxy_hostname]/asimba/profiles/saml2/sso/web`
     - saml_update_user: true
     - user_object_classes: gluuPerson, ox-1A1EAA99F942902300012AE17F0A [ This 'ox-1A1EAA99F942902300012AE17F0A' OC value is different for your server. To get your own value, search for                                                 'gluuAttributeOrigin' in ldap ]
     - saml_use_authn_context: false
     - saml_generate_name_id: true
     - asimba_saml_certificate_file: /etc/certs/saml.pem [ You need to create a 'saml.pem' cert inside /etc/certs/ location. The ingredient of this pem will be asimba.crt without 'BEGIN'                                                 and 'END' tag. Permissin of this pem will be tomcat:tomcat ]
     - saml_validate_response: false
   - Script: Script is attached below. named 'SAML script'.

#### SP Requestor

 - SAML -> SP Requestors
 - 'Add SP Requestor'
   - ID: `https://[proxy_hostname]/saml`
   - Friendly Name: oxAuth SAML
   - Metadata URL: Not required
   - Metadata Timeout: -1
   - Metadata File: Create a SAML metadata like below and save it as 'saml_oxauth_metadata.xml'. Upload this metadata. Replace entityID and ACS Location with your hostname.
      - Sample metadata attached below. Named 'SAML oxAuth metadata'
    - Trust Certificate File: Not required
    - Properties: Not required
    - Enabled: Yes
    - Signing: No

#### Add External IDP

 - SAML -> IDPs
 - 'Add IDP'
   - ID: EntityID of remote IDP. i.e. `https://[idp_hostname]/idp/shibboleth`
   - Friendly Name: Remote AuthN Server 1
   - Metadata URL: Not required
   - Metadata Timeout: -1
   - Metadata File: Upload metadata
   - Trust Certificate File: Grab SAML metadata from remote IDP and upload that. This certificate must be no password protected and x509 format crt. If remote IDP is another Gluu Server                                                 then grab 'shibIDP.crt' from /etc/certs/ of that server.
   - NameIDFormat: urn:oasis:names:tc:SAML:2.0:nameid-format:transient
   - Enabled: Yes
   - Send Scoping: Yes
   - AllowCreate: Yes
   - Disable SSO for IDP: No
   - ACS Index: Yes
   - Send NameIDPolicy: Yes
   - Avoid Subject Confirmations: No
   - Add

 #### asimba.xml file configuration

  - SSH into VM
  - Log into Gluu Server container
  - As user 'tomcat', open 'asimba.xml'. Location: /opt/tomcat/webapps/asimba/WEB-INF/conf
  - Uncomment
       ```
       <gather>
           <attribute name="whitelist-attribute-name" />
       </gather>
       ```
   - Add `attribute name="*"` in attribute release class and restart tomcat

```
        <attributerelease class="com.alfaariss.oa.engine.attribute.release.configuration.ConfigurationFactory">
                <policy id="asimba.releasepolicy.1" friendlyname="Default Attribute Release policy" enabled="true">
                        <attribute name="firstname" />
                        <attribute name="lastname" />
                        <attribute name="email" />
                        <attribute name="role" />
                        <attribute name="country" />
                        <attribute name="*" />
                        
 ```

#### Create custom attribute named 'issuerIDP'

  - Log into oxTrust
  - Configuration -> Attributes
  - 'Add Attribute'
    - Name: issuerIDP
    - SAML1 URI: nothing
    - SAML2 URI: nothing
    - Display Name: issuerIDP
    - Type: Text
    - Edit Type: admin
    - View Type: admin + user
    - Usage Type: Not defined
    - Multivalued: False
    - oxAuth claim name: blank
    - SCIM Attribute: False
    - Description: Custom attribute to grab issuerIDP info
    - Status: Active
    - 'Update'

### Remote Authentication Server configuration

#### Create Trust Relationship

  - Download you Asimba server's metadata with `https://[proxy_hostname]/asimba/profiles/saml2` and save it as 'gluu_asimba_server_metadata.xml'
  - Log into Authentication Server's oxTrust
  - Create a new trust relationship with this metadata which you just downloaded.
  - RelyingParty configuration:
    - SAML2SSO profile:
      - signResponses: conditional
      - signAssertions: never
      - signRequests: conditional
      - encryptAssertions: never
      - encryptNameIds: never
  - Attribute: Release transientID and Username attribute


#### New test user registration

##### Enable 'User Registration' module

 - Log into oxTrust
 - 'Manage Custom Scripts'
 - 'User Registration' tab
   - Custom property: enable_user = true
   - 'Enabled' it
   - Hit 'Update'

##### New user registration

  - Hit `https://[idp_hostname]/identity/register`
  - Fill up the form and new user will be registered
  - We will use this user to test SSO.

### Remote SP configuration

#### Shibboleth SP installation

 - Install SP by following: https://gluu.org/docs/ce/2.4.4/integration/saml-sp/#super-quick-ubuntu-shib-apache-install doc

#### shibboleth2.xml configuration

 - Download Shibboleth metadata of your Gluu-Asimba Server with `https://[proxy_hostname]/idp/shibboleth`
 - Put it inside /etc/shibboleth/ location
 - Modify shibboleth2 xml file like below:
    - SSO entityID:
```
   <SSO entityID="https://[proxy_hostname]/idp/shibboleth"
       discoveryProtocol="SAMLDS" discoveryURL="https://ds.example.org/DS/WAYF">
       SAML2 SAML1
   </SSO>
```

   - Metadata provider:

```
<MetadataProvider type="XML" validate="true" file="proxy_server_metadata.xml"/>
```

- Restart shibd and apache2

 ### Trust relationship in Gluu-Asimba server

 We need to create a trust relationship in Gluu-Asimba server with Shibboleth SP metadata.

  - Log into Gluu-Asimba server
  - Grab Shibboleth SP metadata. You can get that with `https://[sp_hostname]/Shibboleth.sso/Metadata`


 ### Test SSO

  - Log into Gluu-Asimba server and enable 'basic' script from 'Manage Custom Scripts' section.
  - Go to 'Manage Authentication'
    - 'Default Authentication Method'
      - Authentication mode: saml
      - oxTrust authentication mode: basic
      - Hit 'Update'
   - Try SP SSO link ( for our case it's `https://[sp_hostname]/protected/printHeaders.py` ). Note: for testing you need to use the test user you registered in auth.gluu.org.


* [Youtube Video Link](https://youtu.be/YEyrOWJu0yo)
