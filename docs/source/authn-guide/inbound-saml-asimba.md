# Inbound SAML using Asimba
## Overview
Inbound SAML enables an organization to offer SAML authentication as a front door to their digital service. Inbound SAML is a common requirement for organizations that need to support the authentication requirements of large enterprise customers.

During deployment of the Gluu Server, you can install an open source product called [Asimba](http://www.asimba.org/site/) to normalize inbound SAML. 

![asimba-overview](../img/asimba/Asimba_graph.jpg)

!!! Note
    For new inbound SSO deployments, we strongly recommend using the [inbound SSO using Passport.js strategy](./inbound-saml-passport.md). 

## Requirements
For this documentation we used three demo servers:

- `https://[proxy3_hostname]` is the Gluu server v3 with Shibboleth and Asimba installed along with other default components. 
- `https://[idp_hostname]` is the remote authentication Gluu server v2 with Shibboleth installed with other default components. 
- `https://[sp_hostname]` is the remote SP Gluu Server with the Shibboleth SP v26 installed.
  
This doc is divided into three main parts:

1. [Proxy server configuration](#proxy-server-configuration);    
2. [Remote AuthN server configuration](#remote-authn-server-configuration);      
3. [Service Provider configuration](#service-provider-configuration).     

## Proxy Server Configuration

### Asimba custom interception script

  - Log into oxTrust
  - `Configuration` > `Manage Custom Script`
  - Script name 'asimba'
    - asimba_saml_certificate_file: `/etc/certs/saml.pem` (make sure you copy the contents of `asimba.crt` into `saml.pem` with "BEGIN CERTIFICATE" and "END CERTIFICATE" in the header and footer) 
    - asimba_entity_id: `https://[proxy3_hostname]/saml`
    - saml_deployment_type: enroll
    - saml_use_authn_context: false
    - saml_idp_sso_target_url: `https://[proxy3_hostname]/asimba/profiles/saml2/sso/web`
    - user_object_classes: eduPerson, gluuCustomPerson
    - saml_idp_attributes_mapping: {"uid": ["uid"], "mail": ["mail"], "issuerIDP": ["issuerIDP" ] }
    - enforce_uniqueness_attr_list: issuerIDP, uid
    - saml_generate_name_id: true
    
### SP Requestor

  - Create a SAML metadata for native SP requestor of asimba. Grab the copy of from below and replace [proxy3_hostname] with your own server's hostname. Make sure to unix format it. 
  - `SAML` > `SP Requestors`
  - 'Add SP Requestor'
    - ID: `https://[proxy3_hostname]/saml`
    - Friendly Name: oxAuth SAML
    - Metadata URL: Not required
    - Metadata Timeout: -1
    - Metadata File: You can get an example script's metadata from [here](./saml_script_metadata.xml). Edit it to substitute `[proxy3_hostname]` placeholder with a real hostname your instance uses. Upload the resulting metadata to the requestor
    - Trust Certificate File: Not required
    - Properties: Not required
    - Enabled: Yes
    - Signing: No

### Add External IDP/AuthN Server

 - `SAML` > `IDPs`
 - 'Add IDP' 
   - ID: EntityID of remote IDP. i.e. `https://[idp_hostname]/idp/shibboleth`
   - Friendly Name: Remote AuthN Server 1
   - Metadata URL: Not required
   - Metadata Timeout: -1
   - Metadata File: upload metadata
   - Trust Certificate File: Grab SAML metadata from remote IDP and upload that. This certificate must be no password protected and x509 format crt. If remote IDP is another Gluu Server then grab `shibIDP.crt` from `/etc/certs/` of that server.
   - NameIDFormat: urn:oasis:names:tc:SAML:2.0:nameid-format:transient [ If your remote AuthN server is also a Gluu Server ]. This NameID might vary according to various types of AuthN server. 
   - Enabled: Yes
   - Send Scoping in AuthNRequest: Yes
   - AllowCreate: Yes
   - Disable SSO for IDP: No
   - ACS index: Yes
   - Send NameIDPolicy: Yes
   - Avoid Sujbect Confirmations: No

### asimba.xml file configuration

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
 
### Create custom attribute 'issuerIDP'

You need to create a custom attribute named 'issuerIDP' in this stage. Here is how you can create [custom attributes](./attribute.md#custom-attributes).


## Remote AuthN Server Configuration

### Create Trust Relationship

 - Download you Asimba server's metadata with `https://[proxy3_hostname]/asimba/profiles/saml2` and save it as `gluu_asimba_server_metadata.xml`
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
  
### New test user registration

#### Enable 'User Registration' module:    
  - Log into oxTrust
  - 'Manage Custom Scripts'
  - 'User Registration' tab
    - Custom property: enable_user = true
    - 'Enable' it
    - Hit 'Update'

#### New user registration    

 - Hit `https://[idp_hostname]/identity/register`
 - Fill up the form and new user will be registered
 - We will use this user to test our SSO

## Service Provider Configuration

### Shibboleth SP installation

- Prepare your SP instance by following this doc: https://gluu.org/docs/ce/3.0.2/integration/webapps/saml-sp/#super-quick-ubuntu-shib-apache-install

### shibboleth2.xml configuration

 - Download Shibboleth metadata of your Gluu-Asimba server with `https://[prox3_hostname]/idp/shibboleth`
 - Put it inside `/etc/shibboleth/` location
 - Modify `shibboleth2.xml` file like below: 
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
   
## Trust Relationship in Gluu-Asimba server

We need to create a trust relationship in Gluu-Asimba server with Shibboleth SP metadata.

 - Log into oxTrust
 - Grab the Shibboleth SP metadata at `https://[sp_hostname]/Shibboleth.sso/Metadata`


## Test SSO

 - Log into Gluu-Asimba server. 
 - 'Manage Custom Scripts'
   - 'Person Authentication' tab
     - 'Enabled' `basic` authentication script
     - 'Enabled' `asimba` authentication script
 - 'Manage Authentication' 

