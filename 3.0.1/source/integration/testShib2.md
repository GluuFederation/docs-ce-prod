# Test Gluu Server with TestShib2

Here in this documentation we are showing how we can test Gluu Server with TestShib2. 
Please note that, you need to install 'Shibboleth IDP' in your Gluu server while running setup.py script. 

## TestShib2 configuration

 - Go to https://www.testshib.org/index.html
 - Click on 'Register'. Here we need to register our Gluu Server
 - Grab the SAML metadata of Gluu Server with: `https://[hostname_of_gluu_server]/idp/shibboleth`
 - Upload that XML file here in 'https://www.testshib.org/register.html' page
 - After successful registration, you will something like this: 
 - Now let's move forward to 'Gluu Server configuration' 
 
## Gluu Server configuration

 - Download TestShib2 metadata from `https://www.testshib.org/metadata/testshib-providers.xml`
 - Log into Gluu Server oxTrust 
 - Create Trust Relationship with TestShib-provider metadata: 
   - We need to create a 'Federation' trust relationship with this metadata
   - SAML -> Add Trust Relationship
     - DisplayName: TestShib federation
     - Description: TestShib federation
     - Entity type: Single SP
     - Metadata Location: File
     - SP metadata file: upload 'testshib-providers.xml' metadata
     - 'Add'
     - Wait for validation success for this trust relationship. 
 - Create Trust Relationship with TestShib SP: 
   - Now we need to create a 'Federated trust relationship'
     - DisplayName: TestShib SP trust
     - Description: TestShib federated SP
     - Entity Type: Single SP
     - Metadata Location: Select 'Federation' from drop down menu
     - Federation Name: 'TestShib Federation'
     - Entity ID: click on this link, select 'https://sp.testshib.org/shibboleth-sp'
     - Configure Relying Party: not required
     - Released: Username
     - 'Add'
     - Screenshot

## TestShib2 configuration: part 2

 - Hit 'https://sp.testshib.org/' in browser
 - Put the entityID of your Gluu Server here. 
 - Hit 'Go'. 
 - If everything goes well, you will something like this: 
## Troubleshooting

