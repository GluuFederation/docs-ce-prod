# Single Sign-On (SSO) to GSuite(formely Google apps)
GSuite is a brand of cloud computing, productivity and collaboration tools, software and products developed by Google.
GSuite comprises Gmail, Hangouts, Calendar, and Google+ for communication; Drive for storage; Docs, Sheets, Slides, Forms, and Sites for collaboration and supports SAML.

This document will explain how to configure GSuite and the Gluu Server for single sign-on (SSO).

!!! Note
    It is highly recommended to use Google's staging apps environment before migrating to production.
    
## Create a GSuite account

You can do that [here](https://gsuite.google.com/signup/basic/welcome). Don't forget to add at least one more user account(we are going to use that user to test SSO) other than default 'admin' account you are using in Google Admin panel.

If you already have an account skip to the next section.
   
!!! Note
    You need a valid and not used domain name
   
## Configuring G Suite


- Login to your GSuite admin dashboard [here](admin.google.com).

![Image](../../img/integration/admin_console_new.png)

- From the list of options choose the `Security` tab.

- A new page will open. Select `Set up single sign-on(SSO)` from the
options.

![Image](../../img/integration/security_setting.png)

- Single Sign-On setting page will appear. 

![Image](../../img/integration/final_setup.png)

  This page contains a number of selection, and entry fields.

   * __Setup SSO with third party Identity Provider__: This
     refers to your Gluu Server instance. Enable this box.

   * __Sign-in Page URL__: Enter the uri of the sign-in page, for
     example `https://idp_hostname/idp/profile/SAML2/Redirect/SSO`.

   * __Sign-out Page URL__: Enter the uri of the logout page, for
     example `https://idp_hostname/idp/logout.jsp`.

   * __Change Password URL__: The uri an user is redirected if he wants
     to change his password. It is recommended that an organization 
     provides such a link for its end users.

   * __Verification certificate__: Upload the SAML certificate of your
     Gluu Server. The SAML certificates are available in the `/etc/certs` folder inside the Gluu Server `chroot` environment.
     At the time of writting, the cert file is `/etc/certs/idp-signing.crt`

   * __Use a domain specific issuer__: Enable this box to use a
     domain-specific issuer.

   * Save your data using the `Save changes` button on the lower right
     of the page.

Refer [Google SSO](https://support.google.com/a/answer/60224?hl=en) to know more.

## Configuring the Gluu Server

Now we need to get the Google Metadata and create a SAML Trust Relationship in the Gluu Server. Trust Relationships are created so that the IDP (your Gluu Server) can authorize/authenticate the user to the service provider (SP)--in this case, GSuite. 

### Google Metadata
In order to create a Trust Relationship, we need to grab the metadata of
GSuite. This metadata can be collected from Google. It's generally
specific to an organization account. The following is a template of the Google metadata.
Replace `domain.com` with your own domain name(the one used when creating Gsuite account).

```
<EntityDescriptor entityID="google.com/a/domain.com" xmlns="urn:oasis:names:tc:SAML:2.0:metadata">
    <SPSSODescriptor protocolSupportEnumeration="urn:oasis:names:tc:SAML:2.0:protocol">
       <NameIDFormat>urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified</NameIDFormat>
            <AssertionConsumerService index="1" Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"
            Location="https://www.google.com/a/domain.com/acs" >
            </AssertionConsumerService>
    </SPSSODescriptor>
</EntityDescriptor>
```

Got the metadata? Great, we are ready to move forward. 

### Configure custom nameID

We are going to use 'googlenmid' as custom nameID which is 'email' Type and 'mail' attribute value will be this nameID's source attribute. 


#### Configure Shibboleth to support `unspecified` nameId format required by G-Suite

The `unspecified` mean the SP don't care about the nameID format. But in our case we know that Gsuite require an email(`user@yourdomain`) address. This is why we are going to configure shibboleth to support `email`.

Edit the file `/opt/gluu/jetty/identity/conf/shibboleth3/idp/relying-party.xml.vm` and set the namedIDFormatPrecedence to `urn:oasis:names:tc:SAML:2.0:nameid-format:email`.

Configuration should be something like below: 

```
....
....
#foreach( $trustRelationship in $trustParams.trusts )

    <!-- TrustRelationship -->
        #set ($profileConfigMap = $trustRelationship.profileConfigurations)
        <!--#if(!$profileConfigMap.isEmpty())-->

        #set($entityId = $trustParams.trustEntityIds.get($trustRelationship.inum).get(0))
        #set($relyingPartyId = $StringHelper.removePunctuation($trustRelationship.inum))

        <bean parent="RelyingPartyByName" id="$relyingPartyId" c:relyingPartyIds="$entityId">
            <property name="profileConfigurations">
                <list>
            #if($trustRelationship.specificRelyingPartyConfig and (not $trustRelationship.isFederation()))
                #foreach ($mapEntry in $profileConfigMap.entrySet())

                    #set($profileConfig = $mapEntry.value)

                    #if($mapEntry.key == "SAML2SSO")

                    <bean parent="SAML2.SSO"
                          p:includeAttributeStatement="$profileConfig.includeAttributeStatement"
                          p:assertionLifetime="$profileConfig.assertionLifetime"
                          p:nameIDFormatPrecedence="urn:oasis:names:tc:SAML:2.0:nameid-format:email"
                        #if ($profileConfig.signResponses == 'conditional')
                          p:signResponses-ref="SignNoIntegrity"
                          ........
                          ........

```

Restart `identity` and `idp` services with commands like: 

 - service identity stop/start
 - service idp stop/start
 

#### Configure custom nameID named 'googlenmid' 

##### Add 'googlenmid' in LDAP schema

 - File name: 77-customAttributes.ldif
 - Location: /opt/opendj/config/schema
 - Configuration: 
```
dn: cn=schema
objectClass: top
objectClass: ldapSubentry
objectClass: subschema
cn: schema
attributeTypes: ( 1.3.6.1.4.1.48710.1.3.1400 NAME 'googlenmid'
  DESC 'Custom Attribute'
  EQUALITY caseIgnoreMatch
  SUBSTR caseIgnoreSubstringsMatch
  SYNTAX 1.3.6.1.4.1.1466.115.121.1.15
  X-ORIGIN 'Gluu custom attribute' )
objectClasses: ( 1.3.6.1.4.1.48710.1.4.101 NAME 'gluuCustomPerson'
  SUP ( top )
  AUXILIARY
  MAY ( googlenmid $ telephoneNumber $ mobile $ carLicense $ facsimileTelephoneNumber $ departmentNumber $ employeeType $ cn $ st $ manager $ street $ postOfficeBox $ employeeNumber $ preferredDeliveryMethod $ roomNumber $ secretary $ homePostalAddress $ l $ postalCode $ description $ title )
  X-ORIGIN 'Gluu - Custom persom objectclass' )
```
 - Restart opendj with: 
   - service opendj stop
   - service opendj start

##### NameID configuration in shib v3 velocity template

 - File name: attribute-filter.xml.vm
 - Location: /opt/gluu/jetty/identity/conf/shibboleth3/idp
 - Configuration: 
```
...........
...........
#foreach( $attribute in $attrParams.attributes )
#if( ! ($attribute.name.equals('transientId') or $attribute.name.equals('persistentId') or $attribute.name.equals('googlenmid') ) )
#if($attribute.name.equals('eppnForNIH'))

    <resolver:AttributeDefinition id="eduPersonPrincipalName" xsi:type="ad:Scoped" scope="%{idp.scope}" sourceAttributeID="uid">
        <resolver:Dependency ref="siteLDAP" />
        <resolver:AttributeEncoder xsi:type="enc:SAML2ScopedString" name="urn:oid:1.3.6.1.4.1.5923.1.1.1.6" friendlyName="eduPersonPrincipalName" encodeType="false" />
    </resolver:AttributeDefinition>

#else
    <resolver:AttributeDefinition xsi:type="ad:Simple" id="$attribute.name" sourceAttributeID="$attribute.name">
        <resolver:Dependency ref="siteLDAP" />
        <resolver:AttributeEncoder xsi:type="enc:SAML2String" name="$attrParams.attributeSAML2Strings.get($attribute.name)" friendlyName="$attribute.name" encodeType="false" />
    </resolver:AttributeDefinition>
#end
#end
#end

 <resolver:AttributeDefinition id="googlenmid" xsi:type="Simple"
                              xmlns="urn:mace:shibboleth:2.0:resolver:ad"
                              sourceAttributeID="mail">

        <resolver:Dependency ref="siteLDAP"/>
        <resolver:AttributeEncoder xsi:type="SAML2StringNameID"
                                xmlns="urn:mace:shibboleth:2.0:attribute:encoder"
                                nameFormat="urn:oasis:names:tc:SAML:2.0:nameid-format:email" />
</resolver:AttributeDefinition>

#if( $resovlerParams.size() > 0 )
.............
.............
```
 - Restart identity and idp services like below: 
   - service identity stop/start
   - service idp stop/start

##### Create custom attribute with oxTrust

'Register' this 'googlenmid' in your Gluu Server by following [this](https://gluu.org/docs/ce/3.1.2/admin-guide/attribute/#add-the-attribute-to-oxtrust) doc. 

### Create a SAML Trust Relationship
- Create Trust Relationship for Google Apps: 

   - How to create a trust relationship can be found [here](../../admin-guide/saml.md#trust-relationship-requirements). We need to follow the "File" method for Google Apps trust relationship. Upload the metadata which we created couple of steps back. 
    - Required attributes: 
       - You need to release the following attribute: mail and googlenmid.
       - Relying Party Configuration: SAML2SSO should be configured. 

```
        * includeAttributeStatement: check
        * assertionLifetime: default 
        * assertionProxyCount: default
        * signResponses: conditional
        * signAssertions: never
        * signRequests: conditional
        * encryptAssertions: never
        * encryptNameIds: never 
   
```
 
## Test 
  
 - Create an user in Gluu Server representing the Gsuite account you want to log into ( 2nd user other than G-Suite admin account ).       
 - Make sure the user created in step one has mail attribute available whose value is equals to what is given there in G-Suite account (example `user@yourdomain`). 
 - Initiate SSO with `http://www.google.com/gmail/hosted/[hostname_configured]`. 
 - Enjoy!   
    



