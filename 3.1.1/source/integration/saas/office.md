# Office 365 configuration in Gluu Server v3

This doc will guide you on how to setup a Gluu Server as your identity provider (IDP) for access to Office 365. 
By using a Gluu Server as your IDP you can bypass the process of storing passwords directly in O365.

!!! Note
    The attributes `ObjectGUID` and `IDPEmail` are mandatory for O365 SSO. The domain of `IDPEmail` must match the 
    registered domain as well.
    
## Requirements

- A Gluu Server with the Shibboleth IDP installed;
- An O365 account with administrative privilege.
- ADFS which will act as 'Service Provider' to Gluu Server. O365 will be connected to ADFS. 

## Office 365 Configuration 

1. Create a test user from Office365 Admin Panel. Alternatively, you can 
use [this doc](https://azure.microsoft.com/en-us/documentation/articles/active-directory-aadconnect/) to connect a 
backend Azure Active Directory (AD).  

2. Register the domain from the Office365 (O365) Admin Panel from `Settings` > `Domains`

    - `Verify` the domain

3. Register Gluu Server in O365

    - Install/Use Windows Server 2012 R2

    - [Install and Configure](https://technet.microsoft.com/en-us/library/jj205464) Windows Powershell *cmdlets*

    - Create a script and run through `Connect-MsolService`. 
    
    - For Gluu Server, values would be something like these: 
    
```
ActiveLogOnUri                         : https://<hostname>/idp/profile/SAML2/SOAP/ECP
PassiveLogonUri                        : https://<hostname>/idp/profile/SAML2/POST/SSO 
DefaultInteractiveAuthenticationMethod :
FederationBrandName                    : Gluu Inc.
IssuerUri                              : https://<hostname>/idp/shibboleth
LogOffUri                              : https://<hostname>/idp/logout.jsp
MetadataExchangeUri                    : https://<hostname>/idp/shibboleth
NextSigningCertificate                 :
OpenIdConnectDiscoveryEndpoint         :
SigningCertificate                     : The SAML cert ( shibIDP.crt ) from Gluu Server

```

## Gluu Server Configuration

### Custom Attributes  

The configuration begins by creating a few custom attributes named `IDPEmail`, `ImmutableID` and `objectguid`. 
Refer to [this doc](../../admin-guide/attribute/#custom-attributes) to create custom attributes.

#### 'objectguid' configuration

'objectguid' is pulling binary data of 'objectGUID' attribute from backend Active Directory. Gluu Server administrator need to configure 
this attribute in such a way that it can 'pull' the exact binary value from backend Active Directory. Here is the complete process listed below: 

 - Stop cache refresh if you are running Cache Refresh to pull user's information from backend AD. 
 - Create custom attribute named 'objectguid' according to Gluu doc. 
   - Name: objectguid
   - SAML1 URI: urn:gluu:dir:attribute-def:objectguid
   - SAML2 URI: urn:oid:1.3.6.1.4.1.48710.1.3.1001
   - Display Name: objectguid
   - Type: Text
   - Edit type: admin
   - View type: admin, user
   - Usage Type: Not defined
   - Multivalued: False
   - oxAuth claim name: blank
   - SCIM Attribute: False
   - Description: anything you prefer
   - Status: Active
  - Add mapping in 'ox-ldap.properties' file 
   - Location: /etc/gluu/conf
   - binaryAttributes=objectGUID, objectguid [ first 'objectGUID' is Active directory one, second one is newly created custom attribute inside Gluu Server ] 
   - Save configuration
   - Restart Gluu-Server container
 - Configure Cache Refresh so this new custom attribute can pull value from 'objectGUID' of active directory
 - Compare values
 



### IDP configuration
The cache refresh mechanism is used to populate the Gluu Server LDAP with data from a backend LDAP/AD. The `objectGUID` 
attribute must be pulled from the backend data source to Gluu Server.

- Edit the `ox-ldap.properties` (location: `/etc/gluu/conf/ox-ldap.properties`) to add the following:

`binaryAttributes=objectGUID,objectguid`

!!! Note 
    `objectGUID` (the first one) is the attribute which contains binary values in the backend AD 
    and `objectguid` (the second one) is the Gluu Server binary attribute name which will pull value from `objectGUID` attribute

- Restart oxAuth, identity, and idp services

        ```
        # service identity stop
        # service identity start
        # service oxauth stop
        # service oxauth start
        ```
### Identity Mapping

Two attributes require for mapping: 

 - IDPEmail
 - objectguid

`IDPEmail` pull data from backend's email attribute and `objectguid` get data from backend's objectGUID. 

### Create Trust Relationship
Refer [here](../../admin-guide/saml/#create-a-trust-relationship-in-the-gluu-server) to create trust relationships. Need to grab metadata from Micrsoft. Metadata will look like below: 

```
  <?xml version="1.0" encoding="utf-8"?>
  <EntityDescriptor ID="abcdefghijklmn" entityID="urn:federation:MicrosoftOnline" xmlns="urn:oasis:names:tc:SAML:2.0:metadata" xmlns:alg="urn:oasis:names:tc:SAML:metadata:algsupport">
    <Signature xmlns="http://www.w3.org/2000/09/xmldsig#">
      <SignedInfo>
        <CanonicalizationMethod Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
        <SignatureMethod Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1"/>
        <Reference URI="#opqrstuvwxyz">
          <Transforms>
            <Transform Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature"/>
            <Transform Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
          </Transforms>
          <DigestMethod Algorithm="http://www.w3.org/2000/09/xmldsig#sha1"/>
          <DigestValue>........</DigestValue>
        </Reference>
      </SignedInfo>
      <SignatureValue>

        ....
        ....
        ....

      </X509Certificate>
    </X509Data>
    </KeyInfo>
  </Signature>
    <Extensions>
      <alg:DigestMethod Algorithm="http://www.w3.org/2000/09/xmldsig#sha1"/>
      <alg:SigningMethod Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1"/>
    </Extensions>
    
    <SPSSODescriptor protocolSupportEnumeration="urn:oasis:names:tc:SAML:2.0:protocol" WantAssertionsSigned="true">
      <KeyDescriptor use="signing">
        <ds:KeyInfo xmlns:ds="http://www.w3.org/2000/09/xmldsig#">
          <ds:X509Data>
            <ds:X509Certificate>
              
              ....
              ....
              ....

            </ds:X509Certificate>
          </ds:X509Data>
        </ds:KeyInfo>
      </KeyDescriptor>
      <KeyDescriptor use="signing">
        <ds:KeyInfo xmlns:ds="http://www.w3.org/2000/09/xmldsig#">
          <ds:X509Data>
            <ds:X509Certificate>
              
              ....
              ....
              ....

            </ds:X509Certificate>
          </ds:X509Data>
        </ds:KeyInfo>
      </KeyDescriptor>

      <SingleLogoutService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST" Location="https://login.microsoftonline.com/login.srf"/>

      <NameIDFormat>urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress</NameIDFormat>
      <NameIDFormat>urn:mace:shibboleth:1.0:nameIdentifier</NameIDFormat>
      <NameIDFormat>urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified</NameIDFormat>
      <NameIDFormat>urn:oasis:names:tc:SAML:2.0:nameid-format:transient</NameIDFormat>
      <NameIDFormat>urn:oasis:names:tc:SAML:2.0:nameid-format:persistent</NameIDFormat>

      <AssertionConsumerService isDefault="true" index="0" Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST" Location="https://login.microsoftonline.com/login.srf"/>
      <AssertionConsumerService index="1" Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST-SimpleSign" Location="https://login.microsoftonline.com/login.srf"/>

      <!-- PAOS functionality is NOT supported by this service. The binding is only included to ease setup and integration with Shibboleth ECP -->
      <AssertionConsumerService index="2" Binding="urn:oasis:names:tc:SAML:2.0:bindings:PAOS" Location="https://login.microsoftonline.com/login.srf"/>
    </SPSSODescriptor>
  </EntityDescriptor>


```

### Configure Relaying Party

Refer to [Relaying Party](../../admin-guide/saml/#relying-party-configuration) Configuration for more details. 
Relaying Party configuration screen should look like below.

![image](../../img/integration/o365_trelationship.png)
