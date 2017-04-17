# IDP Initiated SSO with Gluu Server
IDP initiated SSO enables the SAML Response to be sent to an SP landing page. In this documentation we are going to see how we can configure a SSO which is IDP-initiated in Gluu Server. 

## Requirements

 - Required attributes from SP
 - Custom metadata which will be used in Gluu Server to configure Trust Relationship. 
   - We need to grab two values from SP side: 
      - EntityID of SP
      - Location to return users for authentication, ACS or Assertion Consumer Service
 - ProviderID value from SP. 

## Prepartion in Gluu Server

### Trust Relationsihp

 - Here is a sample metadata which we need to modify a bit for our desired SP. 
    - We need to change the value of 'entityID', 'ACS' according to supplied data by SP
    - We are using 'unspecified' type NameID here. We also need to confirm this from SP side. Some SP might not support 'unspecified' type NameID. 
```
<EntityDescriptor entityID="entityID_of_SP"
    xmlns="urn:oasis:names:tc:SAML:2.0:metadata">
    <SPSSODescriptor AuthnRequestsSigned="false"
        WantAssertionsSigned="true" protocolSupportEnumeration="urn:oasis:names:tc:SAML:2.0:protocol">
        <NameIDFormat>urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified </NameIDFormat>
             <AssertionConsumerService isDefault="true"
                  index="0" Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"
                  Location="ACS_location_of_SP" />
    </SPSSODescriptor>
</EntityDescriptor>
```
 - Depending on requirement of SP, we need to release attribute and NameID. [Here](https://gluu.org/docs/customize/attributes/#custom-nameid) is how we can configure custom NameID in Gluu Server. 
 - Create Trust [Relationship](https://gluu.org/docs/integrate/outbound-saml/#how-to-create-trust-relationship) with required attribute, NameID and our latest created metadata. 

## Testing SSO

As this is IDP-intiated SSO, so we have to initiate the SSO flow from Gluu Server's Unsolicited link. In this link we have to supply providerId and returnurl for SP as well. Here is how the big IDP-initiated SSO link may look like: 
```
https://Gluu_server_hostname/idp/profile/SAML2/Unsolicited/SSO?providerId=https://providerID_from_SP&returnurl=https://returnuri_from_sp
```
