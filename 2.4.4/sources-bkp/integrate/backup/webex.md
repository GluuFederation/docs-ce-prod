# How to configure Cisco WebEx with Gluu Server

## Configuration in Gluu Server

### Attributes

#### Attribute creation with oxTrust

- 'WebexNameID'
  - Name: webexnameid
  - SAML1 URI: urn:gluu:dir:attribute-def:webexnameid
  - SAML2 URI: urn:oid:webexnameid
  - DisplayName: WebexNameID
  - Type: Text
  - Edit Type: admin
  - View Type: admin + user
  - Usage Type: Not definte
  - Multivalue: False
  - SCIM Attribute: False
  - Description: Custom nameID for WebEx, takes value from uid (through Shibboleth's config files)
  - ![WebexNameID attribute](https://raw.githubusercontent.com/docs/sources/img/SAMLTrustRelationships/webex_webexnameid.png)
- 'wxemail'
  - Name: email_webex
  - SAML1 URI: email
  - SAML2 URI: email
  - DisplayName: wxemail
  - Type: Text
  - Edit type: admin
  - View type: admin + user
  - Usage type: Not defined
  - Multivalue: False
  - SCIM Attribute: False
  - Description: Custom attribute for WebEX SSO. Pulling email from backend. 
  - ![wxemail](https://raw.githubusercontent.com/docs/sources/img/SAMLTrustRelationships/webex_wxemail.png)
- 'wxfirstname'
  - Name: firstname_webex
  - SAML1 URI: firstname
  - SAML2 URI: firstname
  - Display Name: wxfirstname
  - Type: Text
  - Edit Type: admin
  - View Type: admin + user
  - Usage Type: Not defined
  - Multivalued: False
  - SCIM Attribute: False
  - Description: Custom attribute for WebEX SSO, pulling 'givenname' from backend. 
  - ![wxfirstname](https://raw.githubusercontent.com/docs/sources/img/SAMLTrustRelationships/webex_wxfirstname.png)
- 'wxlastname'
  - Name: lastname_webex
  - SAML1 URI: lastname
  - SAML2 URI: lastname
  - Display Name: wxlastname
  - Type: Text
  - Edit Type: admin
  - View Type: admin + user
  - Usage Type: Not defined
  - Multivalued: False
  - SCIM Attribute: False
  - Description: Custom attribute for WebEX SSO, pulling 'sn' from backend. 
  - ![wxlastname](https://raw.githubusercontent.com/docs/sources/img/SAMLTrustRelationships/webex_wxlastname.png)
- 'wxuid'
  - Name: uid_webex
  - SAML1 URI: uid
  - SAML2 URI: uid
  - Display Name: wxuid
  - Type: Text
  - Edit Type: admin
  - View Type: admin + user
  - Usage Type: Not defined
  - Multivalue: False
  - SCIM Attribute: False
  - Description: Custom attribute for WebEX SSO, pulling 'uid' from backend. 
  - ![wxuid](https://raw.githubusercontent.com/docs/sources/img/SAMLTrustRelationships/webex_wxuid.png)


#### Configuring attribute resolver

Add below snippets in 'attribute-resolver.xml.vm' ( location: /opt/tomcat/conf/shibboleth2/idp )

- Attribute definition: 
```
#if( ! ($attribute.name.equals('transientId') or $attribute.name.equals('webexnameid') or $attribute.name.equals('webexnameidmail') or $attribute.name.equals('firstname_webex') or $attribute.name.equals('uid_webex') or $attribute.name.equals('lastname_webex') or $attribute.name.equals('email_webex')  ) )
```

- Attribute declaration: 

```
<resolver:AttributeDefinition xsi:type="ad:Simple" id="firstname_webex" sourceAttributeID="firstname_webex">
        <resolver:Dependency ref="siteLDAP" />
        <resolver:AttributeEncoder xsi:type="enc:SAML2String" nameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:unspecified" name="firstname" />
    </resolver:AttributeDefinition>

<resolver:AttributeDefinition xsi:type="ad:Simple" id="uid_webex" sourceAttributeID="uid_webex">
        <resolver:Dependency ref="siteLDAP" />
        <resolver:AttributeEncoder xsi:type="enc:SAML2String" nameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:unspecified" name="uid" />
    </resolver:AttributeDefinition>

<resolver:AttributeDefinition xsi:type="ad:Simple" id="lastname_webex" sourceAttributeID="lastname_webex">
        <resolver:Dependency ref="siteLDAP" />
        <resolver:AttributeEncoder xsi:type="enc:SAML2String" nameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:unspecified" name="lastname" />
    </resolver:AttributeDefinition>

<resolver:AttributeDefinition xsi:type="ad:Simple" id="email_webex" sourceAttributeID="email_webex">
        <resolver:Dependency ref="siteLDAP" />
        <resolver:AttributeEncoder xsi:type="enc:SAML2String" nameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:unspecified" name="email" />
    </resolver:AttributeDefinition>

    <resolver:AttributeDefinition id="webexnameid"
                                      xsi:type="Simple"
                                      xmlns="urn:mace:shibboleth:2.0:resolver:ad"
                                      sourceAttributeID="uid">
        <resolver:Dependency ref="siteLDAP" />
        <resolver:AttributeEncoder xsi:type="SAML2StringNameID"
                                   xmlns="urn:mace:shibboleth:2.0:attribute:encoder"
                                   nameFormat="urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified"/>
    </resolver:AttributeDefinition>
```
- Restart tomcat


### Trust Relationship
