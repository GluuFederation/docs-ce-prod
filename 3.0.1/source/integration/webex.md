# Cisco WebEx configuration in Gluu Server v3

## Custom Attribute Creation

We need to create couple of custom attributes and one custom nameID. List of custom attributes and nameID is stated below. [Here](../admin-guide/saml.md#custom-nameid) is how we can create custom attributes. 

 - uidwebex
 - emailwebex
 - firstnamewebex
 - lastnamewebex
 - webexnameid
 
In secord part ( oxTrust operation ) of creating custom attribute, we need to follow couple of points for these special attributes. Here is how each attribute should be created: 

 - uidwebex: 
    - Name: uidwebex
    - SAML1 URI: uid
    - SAML2 URI: uid
    - DisplayName: uidwebex
    - Type: Text
    - Rest are default values. 

 - emailwebex:
    - Name: emailwebex
    - SAML1 URI: email
    - SAML2 URI: email
    - DisplayName: wxemail
    - Rest are default values

 - wxfirstname
    - Name: firstnamewebex
    - SAML1 URI: firstname
    - SAML2 URI: firstname
    - DisplayName: wxfirstname
    - Type: Text
    - Rest are default values. 
   
 - wxlastname: 
    - Name: lastnamewebex
    - SAML1 URI: lastname
    - SAML2 URI: lastname
    - DisplayName: wxlastname
    - Rest are default values. 

 - webexnameid
    - Name: webexnameid
    - SAML1 URI: urn:gluu:dir:attribute-def:webexnameid
    - SAML2 URI: urn:oid:webexnameid
    - DisplayName: webexnameid
    - Type: Text
    - Rest are default values. 
  

## WebEx Attribute generation

We need to modify attributeDefinition for these attributes. Configuration is applied in `attribute-resolver.xml.vm` file which is located in `/opt/gluu/jetty/identity/conf/shibboleth3/idp/`

### Attribute Definition

  - Attribute 'uidwebex': 
    - Add 'uidwebex' in 'if statement': 
```
#if( ! ($attribute.name.equals('transientId') or $attribute.name.equals('persistentId') $attribute.name.equals('uidwebex') ) )
```
    - Declaration of 'uidwebex': 

``` 
<resolver:AttributeDefinition xsi:type="ad:Simple" id="uidwebex" sourceAttributeID="uidwebex">
        <resolver:Dependency ref="siteLDAP" />
        <resolver:AttributeEncoder xsi:type="enc:SAML2String" nameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:unspecified" name="uid" />
</resolver:AttributeDefinition>
```
  - Attribute 'emailwebex': 
    - Append 'emailwebex' in 'if statement': 
    
```
#if( ! ($attribute.name.equals('transientId') or $attribute.name.equals('persistentId') or $attribute.name.equals('uidwebex') or $attribute.name.equals('emailwebex') ) )
```
    - Declaration of 'emailwebex': 
```
<resolver:AttributeDefinition xsi:type="ad:Simple" id="emailwebex" sourceAttributeID="emailwebex">
        <resolver:Dependency ref="siteLDAP" />
        <resolver:AttributeEncoder xsi:type="enc:SAML2String" nameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:unspecified" name="email" />
    </resolver:AttributeDefinition>
```
  - Attribute 'firstnamewebex': 
     - Append 'firstnamewebex' in 'if statement' just like above attributes
     - Declaration of 'firstnamewebex': 
```
<resolver:AttributeDefinition xsi:type="ad:Simple" id="firstnamewebex" sourceAttributeID="firstnamewebex">
        <resolver:Dependency ref="siteLDAP" />
        <resolver:AttributeEncoder xsi:type="enc:SAML2String" nameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:unspecified" name="firstname" />
    </resolver:AttributeDefinition>
```
  - Attribute 'lastnamewebex': 
     - Append 'lastnamewebex' in 'if statement'
     - Declaration of 'lastnamewebex': 
```
<resolver:AttributeDefinition xsi:type="ad:Simple" id="lastnamewebex" sourceAttributeID="lastnamewebex">
        <resolver:Dependency ref="siteLDAP" />
        <resolver:AttributeEncoder xsi:type="enc:SAML2String" nameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:unspecified" name="lastname" />
</resolver:AttributeDefinition>
```

  - NameID 'webexnameid': 
     - Append 'webexnameid' in 'if statement'
     - Declaration of 'webexnameid': 
     
```    
<resolver:AttributeDefinition id="webexnameid"
        xsi:type="Simple"
        xmlns="urn:mace:shibboleth:2.0:resolver:ad"
        sourceAttributeID="mail">
    <resolver:Dependency ref="siteLDAP" />
    <resolver:AttributeEncoder xsi:type="SAML2StringNameID"
             xmlns="urn:mace:shibboleth:2.0:attribute:encoder"
             nameFormat="urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress"/>
 </resolver:AttributeDefinition>
 
```

  - SAML2 NameID Generation: 
       - File: saml-nameid.xml
       - Location: /opt/shibboleth-idp/conf
       - Add bean inside SAML2 NameID util:list
       
```
<bean parent="shibboleth.SAML2AttributeSourcedGenerator"
    p:format="urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress"
    p:attributeSourceIds="#{ {'webexnameid'} }" />
```

  - Restart 'idp' and 'identity' services with: 
    - service idp restart
    - service identity restart

## Trust Relationship 

 - Grab WebEx metadata and remove all Name Identifier other than 'emailAddress'. Save this newly modified metadata
 - Log into oxTrust 
 - SAML -> Add Trust Relationships
    - DisplayName: WebEx
    - Description: anything is fine
    - Entity Type: Single SP
    - Metadata Location: File
    - SP Metadata File: upload newly modified metadata
    - Upload public certificate: not required
    - SP Logout URL: not required
    - Configure Relying Party: Yes
        - SAML2SSO: 
            - includeAttributeStatement: Yes
            - assertionLifeTime: 300000
            - signResponse: conditional
            - signAssertions: never
            - signRequests: conditional
            - encryptAssertions: never
            - encryptNameIds: never
    - Released attributes: 
        - lastnamewebex
        - uidwebex
        - webexnameid
        - wxemail
        - wxfistname
        - mail
