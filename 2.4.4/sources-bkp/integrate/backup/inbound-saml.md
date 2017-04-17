# Inbound SAML in Gluu Server

To achieve inbound SAML, the Gluu Server uses an open source product called Asimba. The main use case for Asimba is to enable websites to use a single IdP
for single sign-on (SSO) even when the organization may have a number of
IdPs that are trusted. For more information, please review the [Asimba
website](http://www.asimba.org/site/).

## Required Setup

|Setup hostname|Description|
|--------------|-----------|
|https://sp.gluu.org|This is a shibboleth SP connected to _https://test.gluu.org_|
|https://test.gluu.org| This is a Gluu Server SAML IdP with Asimba|
|https://nest.gluu.org|This is a second Gluu Server SAML IdP connected to _https://test.gluu.org_ |

**Note:** Ideally all SPs and IdPs should be connected to Asimba server. In this case we are following that rule as well.

## Add IdP
The IdP can be added from the Gluu Admin Panel (oxTrust) and navigating to SAML --> IDP.

* Log into the oxTrust interface

* Navigate to SAML --> Idp
![image](../img/2.4/asimba_idp.png)

* Click on 'Add IDP' button
![image](../img/2.4/asimba-idp_button.png)

* Fill up the form with the information below:
    
    * ID: The entityID of the remote ID/ADFS 

        - Example: `https:<hostname_of_gluu_server>/idp/shibboleth`  

    * Friendly Name: Anything you want 

    * Metadata URL: Keep it blank, we will upload metadata

    * Metadata Timeout: Keep it as it is. 

    * Metadata File: Download metadata of remote IDP/ADFS and upload that XML file. 
    
        - Example: The metadata for Gluu IdP can be downloaded using `wget -c https:<hostname_of_gluu_server>/idp/shibboleth`

    * Trust Certificate File: Grab the SAML cert from remote IDP/ADFS and upload that x509 crt

        - Example: You will get the SAML cert from Gluu Server's metadata link or available inside `/etc/certs/shibIDP.crt`

    * NameIDFormat: SAML2 URI if remote IDP is a Gluu Server

        - Example: `urn:oasis:names:tc:SAML:2.0:nameid-format:transient'

* Restart tomcat service: 'service tomcat restart' from Gluu Server container

![image](../img/2.4/add_idp.png)

## Add SP

* Log into oxTrust interface

* Navigate to SAML --> SP Requestor
![image](../img/2.4/asimba-sp_menu.png)

* Click on 'Add SP Requestor'
![image](../img/2.4/asimba-sp_addbutton.png)

* Please fill up the form with the information below:

    * ID: The entityID of SP

        - Example: Shibboleth SP entityID: `https://sp.gluu.org/shibboleth`

    * Friendly Name: Anything is fine

    * Metadata URL: Keep it blank; we will upload metadata

    * Metadata Timeout: Keep it as it is

    * Metadata File: Upload SP metadata ( xml file )

    * Trust Certificate File: Upload SAML cert from SP

* Restart tomcat service: 'service tomcat restart' from Gluu Server container

![image](../img/2.4/add_sp2mod.png)

## Add Selectors
This feature will allow you 'automatically' select specific IDP for specific SP. As for example: If OrgA has SP 'orgASP.gluu.org' and 'orgAIDP.gluu.org' respectively and if you configure selector for 'orgASP.gluu.org' –> 'orgAIDP.gluu.org', then after whenever user will go to 'orgASP.gluu.org', your Gluu Server's Asimba will automatically forward user to 'orgAIDP.gluu.org' for authentication.

* Log into oxTrust interface

* Navigate to SAML --> Selectors
![image](../img/2.4/add-selector_menu.png)

* Click on the 'Add Selector' button
![image](../img/2.4/add-selector_button.png)

    * Select SP Requestor: Select your desired SP from drop down menu

    * Select IDP : Select your desired IDP from drop down menu

* Click on the 'Update' button

* Restart tomcat service: 'service tomcat restart' from Gluu Server container

![image](../img/2.4/selector.png)

## Attributes Handling
oxAsimba will transact all kind of attributes whichever authentication server ( remote IDP/ADFS ) can release to SP. By default this feature is not enabled.

* Gluu Server administrator needs to add `<attribute name=“*” />` inside `attributerelease class` in the `asimba.xml` file under `/opt/tomcat/webapps/asimba/WEB-INF/conf` folder

```
         <attributerelease class="com.alfaariss.oa.engine.attribute.release.configuration.ConfigurationFactory">
                <policy id="asimba.releasepolicy.1" friendlyname="Default Attribute Release policy" enabled="true">
                        <attribute name="firstname" />
                        <attribute name="lastname" />
                        <attribute name="email" />
                        <attribute name="role" />
                        <attribute name="*" />
                </policy>
        </attributerelease> 
```

* Uncomment 'attributegatherer' part

```
 <gather>
  <attribute name="whitelist-attribute-name" />
 </gather> 
```

* Restart tomcat service: 'service tomcat restart' from Gluu Server container

## Inbound SAML End to End Testing
Gluu Server supports Inbound SAML using the custom script feature. 
A step by step guide is available in the `How To` 
section called [Inbound SAML End to End Testing](../how-to/saml_proxy_end_to_end.md)
