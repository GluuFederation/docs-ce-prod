# Single Sign-On (SSO) to Office 365

This doc will guide you on how to setup a Gluu Server as your identity provider (IDP) for access to Office 365. 
By using a Gluu Server as your IDP you can bypass the process of storing passwords directly in O365.

!!! Note
    The attributes `ObjectGUID` and `IDPEmail` are mandatory for O365 SSO. The domain of `IDPEmail` must match the 
    registered domain as well.
    
## Requirements

- A Gluu Server with the Shibboleth IDP installed
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
 
##### Create custom attribute named 'objectguid' according to Gluu doc. 

 - Follow [doc](https://gluu.org/docs/ce/3.1.2/admin-guide/attribute/#custom-attributes) to create this custom attribute. Deployer need to follow below rules when creating this attribute in oxTrust ( 2nd phase of creating custom attribute ). 

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

##### Add mapping in 'ox-ldap.properties' file 

   - Location: /etc/gluu/conf
   - binaryAttributes=objectGUID, objectguid [ first 'objectGUID' is Active directory one, second one is newly created custom attribute inside Gluu Server ] 
   - Save configuration
   - Restart Gluu-Server container
 
##### Configure Cache Refresh so this new custom attribute can pull value from 'objectGUID' of active directory

   - Compare values
 
#### 'IDPEmail' configuration

IDPEmail is pulling email_address from backend Active directory. Standard custom configuration ( with a little changes in SAML1 URI and SAML2 URI )

 - SAML1 URI: urn:gluu:dir:attribute-def:IDPEmail
 - SAML2 URI: urn:oid:1.3.6.1.4.1.48710.1.3.1003

Also we need to apply a little snippet for 'IDPEmail' in 'attribute-resolver.xml' velocity template, which is stated below. 
 
#### 'ImmutableID' nameID configuration

This is a 'persistent' type nameID; base attribute 'objectguid'. Follow the doc on how to create [custom NameID doc](https://gluu.org/docs/ce/3.1.2/admin-guide/attribute/#defining-nameid)

##### Configuration in 'attribute-resolver.xml.vm', the velocity template file: 

 - Location: /opt/gluu/jetty/identity/conf/shibboleth3/idp/
 - Whole configuration: 

```
<?xml version="1.0" encoding="UTF-8"?>
<resolver:AttributeResolver
        xmlns:resolver="urn:mace:shibboleth:2.0:resolver"
        xmlns:ad="urn:mace:shibboleth:2.0:resolver:ad"
        xmlns:dc="urn:mace:shibboleth:2.0:resolver:dc"
        xmlns:enc="urn:mace:shibboleth:2.0:attribute:encoder"
        xmlns:sec="urn:mace:shibboleth:2.0:security"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="urn:mace:shibboleth:2.0:resolver http://shibboleth.net/schema/idp/shibboleth-attribute-resolver.xsd
                            urn:mace:shibboleth:2.0:resolver:ad http://shibboleth.net/schema/idp/shibboleth-attribute-resolver-ad.xsd
                            urn:mace:shibboleth:2.0:resolver:dc http://shibboleth.net/schema/idp/shibboleth-attribute-resolver-dc.xsd
                            urn:mace:shibboleth:2.0:attribute:encoder http://shibboleth.net/schema/idp/shibboleth-attribute-encoder.xsd
                            urn:mace:shibboleth:2.0:security http://shibboleth.net/schema/idp/shibboleth-security.xsd">

    <!-- ========================================== -->
    <!--      Attribute Definitions                 -->
    <!-- ========================================== -->

#foreach( $attribute in $attrParams.attributes )
#if( ! ($attribute.name.equals('transientId') or $attribute.name.equals('persistentId') or $attribute.name.equals('ImmutableID') ) )
#if($attribute.name.equals('eppnForNIH'))

    <resolver:AttributeDefinition id="eduPersonPrincipalName" xsi:type="ad:Scoped" scope="$idp.scope" sourceAttributeID="uid">
        <resolver:Dependency ref="siteLDAP" />
        <resolver:AttributeEncoder xsi:type="enc:SAML2ScopedString" name="urn:oid:1.3.6.1.4.1.5923.1.2.1.6" friendlyName="eduPersonPrincipalName" encodeType="false" />
    </resolver:AttributeDefinition>

#else

    <resolver:AttributeDefinition xsi:type="ad:Simple" id="$attribute.name" sourceAttributeID="$attribute.name">
        <resolver:Dependency ref="siteLDAP" />
        <resolver:AttributeEncoder xsi:type="enc:SAML2String" name="$attrParams.attributeSAML2Strings.get($attribute.name)" friendlyName="$attribute.name" encodeType="false" />
    </resolver:AttributeDefinition>
#end
#end
#end


        <resolver:AttributeDefinition xsi:type="ad:Simple" id="UserId" sourceAttributeID="IDPEmail">
                        <resolver:Dependency ref="siteLDAP" />
                        <resolver:AttributeEncoder xsi:type="enc:SAML2String" name="IDPEmail" friendlyName="UserId" />
        </resolver:AttributeDefinition>


<resolver:AttributeDefinition id="ImmutableID" xsi:type="Simple"
                              xmlns="urn:mace:shibboleth:2.0:resolver:ad"
                              sourceAttributeID="objectguid">
                              <resolver:Dependency ref="siteLDAP"/>
                <resolver:AttributeEncoder xsi:type="SAML2StringNameID"
                xmlns="urn:mace:shibboleth:2.0:attribute:encoder"
                nameFormat="urn:oasis:names:tc:SAML:2.0:nameid-format:persistent" />
</resolver:AttributeDefinition>

    <!-- ========================================== -->
    <!--      Data Connectors                       -->
    <!-- ========================================== -->

    <resolver:DataConnector id="siteLDAP" xsi:type="dc:LDAPDirectory"
                            ldapURL="$ldapUrl"
                            baseDN="o=gluu"
                            principal="cn=Directory Manager,o=gluu"
                            principalCredential="$ldapPass"
                            useStartTLS="%{idp.attribute.resolver.LDAP.useStartTLS}">
                            <dc:FilterTemplate>
                                <![CDATA[
                                    (uid=$requestContext.principalName)
                                ]]>
                            </dc:FilterTemplate>


        <dc:StartTLSTrustCredential id="LDAPtoIdPCredential" xsi:type="sec:X509ResourceBacked">
            <sec:Certificate>%{idp.attribute.resolver.LDAP.trustCertificates}</sec:Certificate>
        </dc:StartTLSTrustCredential>

    </resolver:DataConnector>

</resolver:AttributeResolver>

```
 - [Restart](../../operation/services.md#restart) the `identity` service


##### Configuration of 'saml-nameid.xml'

 - Location: /opt/shibboleth-idp/conf/
 - Full configuration: 

```
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:context="http://www.springframework.org/schema/context"
       xmlns:util="http://www.springframework.org/schema/util"
       xmlns:p="http://www.springframework.org/schema/p"
       xmlns:c="http://www.springframework.org/schema/c"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd
                           http://www.springframework.org/schema/context http://www.springframework.org/schema/context/spring-context.xsd
                           http://www.springframework.org/schema/util http://www.springframework.org/schema/util/spring-util.xsd"

       default-init-method="initialize"
       default-destroy-method="destroy">

    <!-- ========================= SAML NameID Generation ========================= -->

    <!--
    These generator lists handle NameID/Nameidentifier generation going forward. By default,
    transient IDs for both SAML versions are enabled. The commented examples are for persistent IDs
    and generating more one-off formats based on resolved attributes. The suggested approach is to
    control their use via release of the underlying source attribute in the filter policy rather
    than here, but you can set a property on any generator called "activationCondition" to limit
    use in the most generic way.

    Most of the relevant configuration settings are controlled using properties; an exception is
    the generation of arbitrary/custom formats based on attribute information, examples of which
    are shown below.

    -->

    <!-- SAML 2 NameID Generation -->
    <util:list id="shibboleth.SAML2NameIDGenerators">

        <ref bean="shibboleth.SAML2TransientGenerator" />

        <!-- Uncommenting this bean requires configuration in saml-nameid.properties. -->

<!--
        <ref bean="shibboleth.SAML2PersistentGenerator" />
-->


        <!--
        <bean parent="shibboleth.SAML2AttributeSourcedGenerator"
            p:format="urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress"
            p:attributeSourceIds="#{ {'mail'} }" />
        -->


       <bean parent="shibboleth.SAML2AttributeSourcedGenerator"
            p:format="urn:oasis:names:tc:SAML:2.0:nameid-format:persistent"
            p:attributeSourceIds="#{ { 'ImmutableID' } }" />


    </util:list>

    <!-- SAML 1 NameIdentifier Generation -->
    <util:list id="shibboleth.SAML1NameIdentifierGenerators">

        <ref bean="shibboleth.SAML1TransientGenerator" />

        <!--
        <bean parent="shibboleth.SAML1AttributeSourcedGenerator"
            p:format="urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress"
            p:attributeSourceIds="#{ {'mail'} }" />
        -->

    </util:list>

</beans>
```
 - [Restart](../../operation/services.md#restart) the `idp` service

### Trust relationship for O365

 - DisplayName: Office365
 - Description: whichever sounds good to you
 - Entity Type: Single SP
 - Metadata Location: File
 - Sp metadata file: 
   - Save this metadata in a file named 'office365.xml' [ make sure it's unix compatible ] and upload it durning Trust Relationship creation. 
```
<?xml version="1.0" encoding="utf-8"?>
<EntityDescriptor xmlns="urn:oasis:names:tc:SAML:2.0:metadata" entityID="urn:federation:MicrosoftOnline">
  <SPSSODescriptor WantAssertionsSigned="true" protocolSupportEnumeration="urn:oasis:names:tc:SAML:2.0:protocol">

    <NameIDFormat>urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress</NameIDFormat>
    <NameIDFormat>urn:mace:shibboleth:1.0:nameIdentifier</NameIDFormat>
    <NameIDFormat>urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified</NameIDFormat>
    <NameIDFormat>urn:oasis:names:tc:SAML:2.0:nameid-format:transient</NameIDFormat>
    <NameIDFormat>urn:oasis:names:tc:SAML:2.0:nameid-format:persistent</NameIDFormat>

    <AssertionConsumerService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST" Location="https://login.microsoftonline.com/login.srf" index="0" isDefault="true"/>
    <AssertionConsumerService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST-SimpleSign" Location="https://login.microsoftonline.com/login.srf" index="1"/>
    <AssertionConsumerService Binding="urn:oasis:names:tc:SAML:2.0:bindings:PAOS" Location="https://login.microsoftonline.com/login.srf" index="2" />

  </SPSSODescriptor>
</EntityDescriptor>

```
 - Released attributes: 
   - IDPEmail
   - ImmutableID
 - 'Add' this trust relationship
 - Wait for the 'validation success' and 'Active' status for this trust relationship
 - Configure Relying Party: 
   - SAML2SSO Profile configuration: 
     - includeAttributeStatement: default
     - assertionLifeTime: default
     - signResponses: never
     - signAsserstions: never
     - signRequests: never
     - encryptAssertions: never
     - encryptNameIds: never
   - Save
  - Update trust relationship
  - Wait for 5 mins and Test




