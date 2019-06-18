# Test Gluu Server ( v3.1.6 ) with SAMLTest.id

## Configuration in SAMLTest.ID site
  - Hit site: `https://samltest.id`
  - Upload or Fetch your Gluu Server Shibboleth metadata with link: `https://[hostname_of_gluu_server]/idp/shibboleth` 
  ![image](../img/samltest_id/SAMLTestID_upload_fetch_metadata.PNG)
  - After successful upload of fetching, you will see confirmation like below: 
  ![image](../img/samltest_id/SAMLTESTID_METADATA_PARSED.PNG)

## Configuration in Gluu Server
 - From `https://samltest.id/download/`, grab SAMLTest.ID SP link: `https://samltest.id/saml/sp`
 - Move to create Trust Relationship in Gluu Server. [Here](...) is how you can create SAML Trust Relationship in Gluu Server.
 ![image](../img/samltest_id/SAMLTestID_Gluu_TR.PNG)

## Test

 - Go to `https://samltest.id/start-idp-test/`
 - Login Initiator: `https://[hostname_of_gluu_server]/idp/shibboleth`
 - If everything goes well, you will your Gluu Server's login page
 - Login there
 - You will land into SAMLTest.ID page like below. ![image](../img/samltest_id/SAMLTestID_success.PNG)
 
### Logout Testing

 - To test logout from SAMLTest.ID, you need to enable `SAML2Logout` Profile from Trust Relationship like below. ![image](../img/samltest_id/SAMLTestID_Gluu_logout_TR.PNG)
 - Update it, test after 5 mins from SAMLTest.ID ![image](../img/samltest_id/SAMLTestID_sp_logout.PNG)
