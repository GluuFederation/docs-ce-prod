# SAML Proxy End to End Configuration and Testing

For this testing environment we have below pieces:

   - https://sp.gluu.org/protected/print.py –> Service Provider
   - https://test.gluu.org –> Gluu Server with SAML Script and Asimba
   - https://nest.gluu.org –> Gluu Server acting as remote authentication server

The whole workflow is:

```
SP1 (sp.gluu.org) → IDP (test.gluu.org) → oxAuth Saml script (test.gluu.org) → Asimba (test.gluu.org) → Remote IDP (nest.gluu.org) → oxAuth (test.gluu.org / any acr_values) → back_in reverser_order 

```

Description of SAML Authentication Module is available here: https://github.com/GluuFederation/oxAuth/tree/master/Server/integrations/saml


## Preparation in Gluu Server
 
During installation of Gluu Server (https://test.gluu.org), deployer need to select 'Asimba' and 'Shibboleth IDP' along with other core components (oxTrust,oxAuth,Web Server and LDAP). After the completion of installation, we can move forward for rest of the work. 

### Asimba core configuration file modification
 - File name: asimba.xml
 - Location: /opt/tomcat/webapps/asimba/WEB-INF/conf ( inside Gluu Server container )
 - After below modifications, restart tomcat: 
  - Enable whitelist for attributes 
```
<gather>
   <attribute name="whitelist-attribute-name" />
</gather>
```
  - Allow all attributes released by remote AuthN server. Add 'attribute name="*"' in attributeRelease class
```
<attributerelease class="com.alfaariss.oa.engine.attribute.release.configuration.ConfigurationFactory">
         <policy id="asimba.releasepolicy.1" friendlyname="Default Attribute Release policy" enabled="true">
                        <attribute name="firstname" />
                        <attribute name="lastname" />
                        <attribute name="email" />
                        <attribute name="role" />
                        <attribute name="country" />    <!-- country is defined in <global ..> attribute section -->
                        <attribute name="*" />
                        .............
                        .............
```
### SAML custom script configuration 

Server: https://test.gluu.org

[SAML Script](https://github.com/GluuFederation/oxAuth/blob/master/Server/integrations/saml/SamlExternalAuthenticator.py) allows Gluu Server Administrator to prepare a complete SAML Proxy setup with their Gluu Server. 
To configure this custom script, 

 - Log into Gluu Server as admin user. 

 - Configuration -> Manage Custom Scripts

 - Select/Add 'saml' script from 'Person Authentication' tab

    - Name: saml

    - Description: Saml Authentication module

    - Programming Language: Python

    - Level: 1

    - Location Type: LDAP

    - Usage Type: Web

    - Custom property (key/value)

       - saml_deployment_type: enroll_all_attr
       - saml_idp_sso_target_url: https://test.gluu.org/asimba/profiles/saml2/sso/web
       - saml_validate_response: false
       - asimba_entity_id: https://test.gluu.org/saml
       - asimba_saml_certificate_file: /etc/certs/saml.pem [ Deployer need to make sure that 'saml.pem' is there inside /etc/certs/. The ingredient of this pem is asimba.crt without '-----BEGIN CERTIFICATE-----' and '-----END CERTIFICATE-----' header and footer ] 
       - user_object_classes: eduPerson, ox-563D78CE5EDA45D900017569E2D5 [ This varies from org to org. If Organization want to process any eduPerson related attribute they need to add 'eduPerson' here. The other OC 'ox-563D....' is required if Organization need to process/use any custom attribute ] 
       - saml_idp_attributes_mapping: { "attribute_name": ["attribute_name", "SAML2 URI"] } 
         - example: ```{"uid": ["uid", "urn:oid:0.9.2342.19200300.100.1.1"], "mail": ["mail", "urn:oid:0.9.2342.19200300.100.1.3"], "givenName": ["givenName", "urn:oid:2.5.4.42"], "sn": ["sn", "urn:oid:2.5.4.4"], "eduPersonPrincipalName": ["eduPersonPrincipalName", "urn:oid:1.3.6.1.4.1.5923.1.1.1.6"] } ```
       - enforce_uniqueness_attr_list: attribute1, attribute2 [ This also varies from Org to Org ] 
         - example: ```edupersonprincipalname, uid, mail, givenName```
       - saml_use_authn_context: false
       - saml_generate_name_id: true
       - saml_update_user: true
       - Script: Grab script from github ( https://github.com/GluuFederation/oxAuth/tree/master/Server/integrations/saml ) and paste it here. 
       - Enabled: True
    
### Asimba Configuration: 

Server: https://test.gluu.org

#### Enroll Remote Authentication servers: 
    
  - Log into oxTrust as admin user
    - SAML -> IDPs
      - Add IDP
      - ID: The entityID of remote authentication server
        - example: ```https://nest.gluu.org/idp/shibboleth```
      - Friendly Name: Anything peferrable 
      - Metadata URL: Not required
      - Metadata Timeout: -1
      - Metadata File: Upload rermote IDP's xml metadata
      - Trust Certificate File: Uploade remote IDP's SAML certification. The format should be x509, crt; non password protected. 
      - NameIDFormat: Not required
      - Enabled: Yes
      - Send Scoping: Yes
      - AllowCreate: Yes
      - Disable SSO for IDP: No
      - ACS index: Yes
      - Send NameIDPolicy: Yes
      - Avoid Subject Confirmations: No
      
#### SP Requestors: 

  - Log into oxTrust as admin user
  - SAML -> SP Requestors
     - Add SP Requestor
     - Select parent SP Pool: requestorpool.1
     - ID: https://test.gluu.org/saml
     - Friendly Name: oxAuth SAML
     - Metadata URL: Not required
     - Metadata Timeout: -1
     - Metadata File: Create a SAML metadata like below and save it as 'saml_oxauth_metadata.xml'. Upload this metadata. 
     - Trust Certificate File: Not required
     - Properties: Not required
     - Enabled: Yes
     - Signing: No
     - metadata snippet: 
``` 
<md:EntityDescriptor xmlns:md="urn:oasis:names:tc:SAML:2.0:metadata" entityID="https://test.gluu.org/saml">
  <md:SPSSODescriptor protocolSupportEnumeration="urn:oasis:names:tc:SAML:2.0:protocol">
    <md:AssertionConsumerService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST" Location="https://test.gluu.org/oxauth/postlogin" index="0"/>
  </md:SPSSODescriptor>
  <md:Organization>
    <md:OrganizationName xml:lang="en">Gluu</md:OrganizationName>
    <md:OrganizationDisplayName xml:lang="en">Gluu - Open Source Access Management</md:OrganizationDisplayName>
    <md:OrganizationURL xml:lang="en">http://www.gluu.org</md:OrganizationURL>
  </md:Organization>
  <md:ContactPerson contactType="technical">
    <md:GivenName>Administrator</md:GivenName>
    <md:EmailAddress>support@gluu.org</md:EmailAddress>
  </md:ContactPerson>
</md:EntityDescriptor> 
```

### SAML Trust Relationship

Server: https://test.gluu.org

Create Trust relationships for all service provides which are included in SAML Proxy SSO workflow. In our test setup we created Trust relationship for remote SP which has entityID 'https://sp.gluu.org/shibboleth'. How to create Trust Relationship is available [here](https://gluu.org/docs/integrate/outbound-saml/)
 
## Preparation in Remote Authentication Server (IDP)

Server: https://nest.gluu.org

Create a SAML Trust Relationship with Gluu Server's Asimba bit. 
Requirements: 

- Download the Asimba metadata and use 'File' method to create Trust relationship
    - Asimba metadata is available @ `https://test.gluu.org/asimba/profiles/saml2`
- Relying Party Configuration: 'SAML2SSO' Profile 
    - example: 
        - includeAttributeStatement: Yes
        - assertionLifeTime: 300000
        - assertionProxyCount: 0
        - signResponses: conditional
        - signAssertions: never
        - signRequests: conditional
        - encryptAssertions: never
        - encryptNameIds: never

  - Attribute: Any attribute according to Service Providers own need. Any kind of nameID from below list is mandatory. 
     - nameID: 
        - `nameIDFormat="urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified"`
        - `nameIDFormat="urn:oasis:names:tc:SAML:2.0:nameid-format:transient"`
        - `nameIDFormat="urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress"`

     - How to create nameID in Gluu Server is available [here](https://gluu.org/docs/customize/attributes/#custom-nameid)

## Preparation in Service Provider (SP)

Server: https://sp.gluu.org

Preparing Service Provider for SAML Proxy worflow follows standard procedure. Service Provider need to connect with Gluu Server's Shibboleth part ( for our case, the entityID would be: https://test.gluu.org/idp/shibboleth ). How to configure any site with Shibboelth SP piece is available [here](https://gluu.org/docs/integrate/ubuntu-shib-apache/). 

## Test

Here is a quick video on how SAML Proxy SSO might look like. Here in this video we are using 'https://sp.gluu.org/protected/print.py' as our protected service provider link. After initiating the SSO, we are moved to Gluu Server's SAML Proxy discovery page ( https://test.gluu.org ). From there we selected 'Nest' as our desired authentication server. After succesful authentication we are landing to proctected resource. https://youtu.be/YEyrOWJu0yo
