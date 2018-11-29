# Office 365 Integration with Gluu Server

!!! Attention
    The official support end-of-life (EOL) date for Gluu Server 2.4.4 is December 31, 2018. Starting January 1, 2019, no further security updates or bug-fixes will be provided for Gluu Server 2.X. We strongly recommend [upgrading](https://gluu.org/docs/ce/upgrade/) to the newest version.

This guide is created to use Microsoft Office 365 Single-Sign-On with Gluu Server.
It is assumed that an Office 365 subscription is available/registered.

**Note:** The attributes `ObjectGUID` and `IDPEmail` are mandatory for O365 SSO. The domain of `IDPEmail` must match the registered domain as well.
## Office 365 Configuration

1. Please create a test user from Office365 Admin Panel<br/>
   Alternatively, use [this doc](https://azure.microsoft.com/en-us/documentation/articles/active-directory-aadconnect/) to connect backend Azure Active Directory (AD) 

2. Register the domain from the Office365 (O365) Admin Panel from **Settings --> Domains**

    * *Verify* the domain

3. Register Gluu Server in O365

    * Install/Use Windows Server 2012 R2

    * [Install and Configure](https://technet.microsoft.com/en-us/library/jj205464) Windows Powershell *cmdlets*

    * Create a script named `gluu1.ps1` with the following template changing domain, hostname of Gluu Server and Certificate
```
 Connect-MsolService

$dom = "company.org"
$url = "https://<hostname>/idp/profile/SAML2/POST/SSO"
$uri = "https://<hostname>/idp/shibboleth"
$logouturl = "https://<hostname>/idp/logout.jsp"
$cert = "Mx....SAML_cert_of_your_Gluu_Server...Tdsg9R0XO3AnBeHRtGmAA="

Set-MsolDomainAuthentication -DomainName $dom -FederationBrandName $dom -Authentication Federated  -PassiveLogOnUri $url -SigningCertificate $cert -IssuerUri $uri -LogOffUri $logouturl -PreferredAuthenticationProtocol SAMLP 
```

4. Run the `gluu.ps1` script from Windows Server 2012 R2

## Gluu Server Configuration
### Custom Attributes
The configuration begins by creating a few custom attributes named `IDPEmail`, `ImmutableID` and `objectguid`.
Please see [this doc](../admin-guide/saml/#saml-attributes) to create custom attributes.

1. `IDPEmail` Custom Attribute
![image](../img/integration/idpemail.png)

2. `ImmutableID` Custom Attribute
![image](../img/integration/immutableid.png)

3. `objectguid` Custom Attribute
![image](../img/integration/objectguid.png)

### OpenDJ Configuration

1. Edit the `100-user.ldif` file under `/opt/opendj/config/schema` folder.

    * Remove the `obhectGUID` entry from the file

    * Add the following new entry
```
attributeTypes: ( 1454676848732 NAME 'objectGUID' SYNTAX 1.3.6.1.4.1.1466.115.121.1.5 USAGE userApplications X-ORIGIN 'gluu' ) 
```
    * Restart OpenDJ

2. Edit the `attribute-resolver.xml.vm` file under `/opt/tomcat/conf/shibboleth2/idp` folder

    * Add `$attribute.name.equals('ImmutableID') ` with the existing *($attribute.name.equals('transientId')* to look like the snippet below
```
#if(!($attribute.name.equals('transientId')or$attribute.name.equals('ImmutableID'))) 
```

    * Add `IDPEmail` attribute definition
```
 <resolver:AttributeDefinition xsi:type="ad:Simple" id="UserId" sourceAttributeID="IDPEmail">
                        <resolver:Dependency ref="siteLDAP" />
                        <resolver:AttributeEncoder xsi:type="enc:SAML2String" name="IDPEmail" friendlyName="UserId" />
        </resolver:AttributeDefinition> 
```

    * Add `ImmutableID` attribute definition
```
 <resolver:AttributeDefinition id="ImmutableID" xsi:type="Simple"
                              xmlns="urn:mace:shibboleth:2.0:resolver:ad"
                              sourceAttributeID="objectguid">

        <resolver:Dependency ref="siteLDAP"/>
        <resolver:AttributeEncoder xsi:type="SAML2StringNameID"
                                xmlns="urn:mace:shibboleth:2.0:attribute:encoder"
                                nameFormat="urn:oasis:names:tc:SAML:2.0:nameid-format:persistent" />
</resolver:AttributeDefinition> 
```

### Identity Mapping
The cache refresh mechanism is used to populate the Gluu Server LDAP with data from a backend LDAP/AD. The `objectGUID` attribute must be pulled from the backend data source to Gluu Server.

* Edit the `ox-ldap.properties`, `oxauth-ldap.properties` and `oxidp-ldap.properties` files to add the following
```
binaryAttributes=objectGUID,objectguid 
```
**Note:**'objectGUID' (the first one) is the attribute which contains binary values in the backend AD and 'objectguid' (the second one) is the Gluu Server binary attribute name which will pull value from 'objectGUID' attribute

* Restart Tomcat

### Create Trust Relationship
Please see [this doc](../admin-guide/saml.md) to create trust relationships.

* Configure Relaying Party like the following screenshot
![image](../img/integration/o365_trelationship.png)

