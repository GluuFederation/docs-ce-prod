# TestShib2 Testing For Gluu Server

## Trust Relationship in IdP

It is necessary to create a Trust Relationship in the IdP for TestShib2.

1. Log into the Gluu IdP as an admin user.

2. Click on SAML --> Trust Relationships

![SAML TR](../img/SamlIDPAdminGuide/testshib_samltr.png)

3. To create a new Trust Relationship, click on the "Add Relationship" button.

![Add TR](../img/SamlIDPAdminGuide/testshib_addtr.png)

 (a) Configuration

      i. Display Name: TestShib2 testing

     ii. Description: TestShib2 TR

    iii. Metadata type: URL

     iv. Provide TestShib2 XML metadata link: http://www.testshib.org/metadata/testshib-providers.xml

      v. Release Attributes: First Name, Username, TransientId if required and released in IdP.

     vi. Click "Add".

![Adding TR](../img/SamlIDPAdminGuide/testshib_addingtr.png)

## Gluu IdP Configuration in Testshib Site

1. Go to the TestShib website by typing "http://www.testshib.org/" in the web browser.

2. Click on "Register".

3. Upload the metadata of the IdP in the testshib webpage.

    (a) To collect the metadata of Gluu IdP, please go to "https://support.gluu.org/216/.

![Upload Metadata](../img/SamlIDPAdminGuide/testshib_uploadmetadata.png)

    (b) After successful update, TestShib will present a confirmation page.

![Confirmation](../img/SamlIDPAdminGuide/testshib_confirmation.png)

## IdP SSO Testing

1. Click on "TEST" in the TestShib website.

2. Hit the "https://sp.testshib.org" link.

![Test](../img/SamlIDPAdminGuide/testshib_test.png)

3. Provide the entityID of the IdP in the input box. The entityID for Gluu IdP is "https://host_name_of_IdP/idp/shibboleth".

![Test Shib](../img/SamlIDPAdminGuide/testshib_testshib.png)

4. Click "Go" and the user will be forwarded to the IdP for authentication. If the authentication is successful, then the browser will show a shibboleth protected TestShib page.

![Protected Page](../img/SamlIDPAdminGuide/testshib_protectedpage.png)
