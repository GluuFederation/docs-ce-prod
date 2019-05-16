# Using SAML script without SAML Proxy ( Asimba ) in Gluu Server

This documentation is going to show us how to configure Gluu Server ( v 2.4.4 ) SAML Script without SAML Proxy server ( aka. Asimba ). 
For the preparation of this documentation we have used three servers: 
  - https://test.gluu.org ( Gluu Server whose SAML script we are going to use )
  - https://nest.gluu.org ( Remote Gluu Server which is going to act as AuthN server for end users )
  - https://sp.gluu.org ( Test service provider whose protected resources we are going to access through SSO )

## Configuration in test.gluu.org server

### SAML Custom Script setup: 
  - Log into oxTrust as admin user / user who has Gluu Server administrative priviledge
  - Configuration -> Manage Custom Scripts
  - Under 'Person Authentication' tab, scroll down to 'saml': 
    - Name: saml
    - Description: SAML Authentication module
    - Programming Language: Python
    - Level: 50
    - Location Type: Ldap
    - Usage type: Web
    - Custom property ( key/value ):
      - saml_certificate_file: /etc/certs/saml.pem ( Deployer need to grab the SAML cert of remote authentication server and place it here inside SAML_Script enabled Gluu Server as 'saml.pem'. Make sure that there is no "-----BEGIN CERTIFICATE-----" and "-----END CERTIFICATE-----" delimeter in saml.pem. As for example... in our case we saved shibIDP.crt of 'nest.gluu.org' here inside saml.pem )
      - saml_deployment_type: enroll
      - saml_use_authn_context: true
      - saml_validate_response: true
      - saml_idp_sso_target_url: https://nest.gluu.org/idp/profile/SAML2/Redirect/SSO
      - saml_issuer: https://test.gluu.org/saml
      - saml_name_identifier_format: urn:oasis:names:tc:SAML:2.0:nameid-format:transient
      - saml_idp_attributes_list: urn:oid:0.9.2342.19200300.100.1.1, urn:oid:0.9.2342.19200300.100.1.3
      - saml_local_attributes_list: uid, mail
      - Script: 

### Trust Relationship
Create SAML Trust relationship for 'sp.gluu.org'
  - Log into Gluu oxTrust as admin
  - SAML -> Trust Relatonships
    - Add Relationship
      - DisplayName: sp.gluu.org
      - Description: sp test
      - Metadata Type: File
      - Upload xml metadata of 'sp.gluu.org'
      - Release attributes: (a) Email (b) Username

### Add SP Requestor
Enroll SP requestor for 'test.gluu.org/saml'
  - Log into Gluu oxTrust as admin
  - SAML -> SP Requestors
  - Add SP Requestor
    - Select parent SP Pool: requestorpool.1
    - ID: https://test.gluu.org/saml 
    - Friendly Name: oxAuth SAML
    - Metadata URL: keep it blank, we will upload metadata
    - Metadata Timeout: -1
    - Metadata File: Upload metadata for 'https://test.gluu.org/saml' [ Metadata added below ] 
    - Trust Certificate File: not required
    - Properties: no required
    - Enabled: Yes
    - Signing: No

## Configuration in nest.gluu.org server
  - SAML Trust Relationship: 
    - Create a new Trust relationship for 'https://test.gluu.org/saml'
      - DisplayName: test.gluu.org
      - Description: Test
      - Metadata Type: File
        - Grab below xml file ('https://test.gluu.org/saml' file) and use that as xml metadata to create this trust. 
      - Configure Relying Party: 
         - SAML2SSO
            - includeAttributeStatement: yes
            - assertionLifetime: 300000
            - assertionProxyCount: 0
            - signResponses: conditional
            - signAssertions: never
            - signRequests: conditional
            - encryptAssertions: never
            - encryptNameIds: never
        - Release attributes: 
          - Email
          - TransientId
          - Username

## Configuration in sp.gluu.org

Service Provider configuration is straight forward. We installed Shibboleth SP in Ubuntu 14.04 LTS. Sp configurations are also added below. 

## Files

## SAML Script: 
```
from org.jboss.seam.contexts import Context, Contexts
from org.jboss.seam.security import Identity
from javax.faces.context import FacesContext
from org.xdi.model.custom.script.type.auth import PersonAuthenticationType
from org.xdi.oxauth.service import UserService, ClientService, AuthenticationService, AttributeService
from org.xdi.oxauth.service.net import HttpService
from org.xdi.util import StringHelper
from org.xdi.util import ArrayHelper
from org.gluu.saml import SamlConfiguration, AuthRequest, Response
from java.util import Arrays, ArrayList, HashMap, IdentityHashMap
from org.xdi.oxauth.model.common import User
from org.xdi.ldap.model import CustomAttribute

import java

try:
    import json
except ImportError:
    import simplejson as json

class PersonAuthentication(PersonAuthenticationType):
    def __init__(self, currentTimeMillis):
        self.currentTimeMillis = currentTimeMillis

    def init(self, configurationAttributes):
        print "Saml. Initialization"

        saml_certificate_file = configurationAttributes.get("saml_certificate_file").getValue2()
        saml_idp_sso_target_url = configurationAttributes.get("saml_idp_sso_target_url").getValue2()
        saml_issuer = configurationAttributes.get("saml_issuer").getValue2()
        saml_use_authn_context = StringHelper.toBoolean(configurationAttributes.get("saml_use_authn_context").getValue2(), True)
        if (saml_use_authn_context):
            saml_name_identifier_format = configurationAttributes.get("saml_name_identifier_format").getValue2()
        else:
            saml_name_identifier_format = None

        saml_certificate = self.loadCeritificate(saml_certificate_file)
        if (StringHelper.isEmpty(saml_certificate)):
            print "Saml. Initialization. File with x509 certificate should be not empty"
            return False

        samlConfiguration = SamlConfiguration()

        # Set the issuer of the authentication request. This would usually be the URL of the issuing web application
        samlConfiguration.setIssuer(saml_issuer)

        # Tells the IdP to return a persistent identifier for the user
        samlConfiguration.setNameIdentifierFormat(saml_name_identifier_format)
  
        # The URL at the Identity Provider where to the authentication request should be sent
        samlConfiguration.setIdpSsoTargetUrl(saml_idp_sso_target_url)

        # Enablediable RequestedAuthnContext
        samlConfiguration.setUseRequestedAuthnContext(saml_use_authn_context)
        
        # Load x509 certificate
        samlConfiguration.loadCertificateFromString(saml_certificate)
        
        self.samlConfiguration = samlConfiguration

        self.attributesMapping = None
        if (configurationAttributes.containsKey("saml_idp_attributes_list") and
            configurationAttributes.containsKey("saml_local_attributes_list")):

            saml_idp_attributes_list = configurationAttributes.get("saml_idp_attributes_list").getValue2()
            if (StringHelper.isEmpty(saml_idp_attributes_list)):
                print "Saml. Initialization. The property saml_idp_attributes_list is empty"
                return False

            saml_local_attributes_list = configurationAttributes.get("saml_local_attributes_list").getValue2()
            if (StringHelper.isEmpty(saml_local_attributes_list)):
                print "Saml. Initialization. The property saml_local_attributes_list is empty"
                return False

            self.attributesMapping = self.prepareAttributesMapping(saml_idp_attributes_list, saml_local_attributes_list)
            if (self.attributesMapping == None):
                print "Saml. Initialization. The attributes mapping isn't valid"
                return False

        self.samlExtensionModule = None
        if (configurationAttributes.containsKey("saml_extension_module")):
            saml_extension_module_name = configurationAttributes.get("saml_extension_module").getValue2()
            try:
                self.samlExtensionModule = __import__(saml_extension_module_name)
                saml_extension_module_init_result = self.samlExtensionModule.init(configurationAttributes)
                if (not saml_extension_module_init_result):
                    return False
            except ImportError, ex:
                print "Saml. Initialization. Failed to load saml_extension_module:", saml_extension_module_name
                print "Saml. Initialization. Unexpected error:", ex
                return False

        print "Saml. Initialized successfully"
        return True   

    def destroy(self, configurationAttributes):
        print "Saml. Destroy"
        print "Saml. Destroyed successfully"
        return True

    def getApiVersion(self):
        return 1

    def isValidAuthenticationMethod(self, usageType, configurationAttributes):
        return True

    def getAlternativeAuthenticationMethod(self, usageType, configurationAttributes):
        return None

    def authenticate(self, configurationAttributes, requestParameters, step):
        context = Contexts.getEventContext()
        authenticationService = AuthenticationService.instance()
        userService = UserService.instance()

        saml_map_user = False
        saml_enroll_user = False
        saml_enroll_all_user_attr = False
        # Use saml_deployment_type only if there is no attributes mapping
        if (configurationAttributes.containsKey("saml_deployment_type")):
            saml_deployment_type = StringHelper.toLowerCase(configurationAttributes.get("saml_deployment_type").getValue2())
            
            if (StringHelper.equalsIgnoreCase(saml_deployment_type, "map")):
                saml_map_user = True

            if (StringHelper.equalsIgnoreCase(saml_deployment_type, "enroll")):
                saml_enroll_user = True

            if (StringHelper.equalsIgnoreCase(saml_deployment_type, "enroll_all_attr")):
                saml_enroll_all_user_attr = True

        saml_allow_basic_login = False
        if (configurationAttributes.containsKey("saml_allow_basic_login")):
            saml_allow_basic_login = StringHelper.toBoolean(configurationAttributes.get("saml_allow_basic_login").getValue2(), False)

        use_basic_auth = False
        if (saml_allow_basic_login):
            # Detect if user used basic authnetication method
            credentials = Identity.instance().getCredentials()

            user_name = credentials.getUsername()
            user_password = credentials.getPassword()
            if (StringHelper.isNotEmpty(user_name) and StringHelper.isNotEmpty(user_password)):
                use_basic_auth = True

        if ((step == 1) and saml_allow_basic_login and use_basic_auth):
            print "Saml. Authenticate for step 1. Basic authentication"

            context.set("saml_count_login_steps", 1)

            credentials = Identity.instance().getCredentials()
            user_name = credentials.getUsername()
            user_password = credentials.getPassword()

            logged_in = False
            if (StringHelper.isNotEmptyString(user_name) and StringHelper.isNotEmptyString(user_password)):
                userService = UserService.instance()
                logged_in = userService.authenticate(user_name, user_password)

            if (not logged_in):
                return False

            return True

        if (step == 1):
            print "Saml. Authenticate for step 1"

            currentSamlConfiguration = self.getCurrentSamlConfiguration(self.samlConfiguration, configurationAttributes, requestParameters)
            if (currentSamlConfiguration == None):
                print "Saml. Prepare for step 1. Client saml configuration is invalid"
                return False

            saml_response_array = requestParameters.get("SAMLResponse")
            if ArrayHelper.isEmpty(saml_response_array):
                print "Saml. Authenticate for step 1. saml_response is empty"
                return False

            saml_response = saml_response_array[0]

            print "Saml. Authenticate for step 1. saml_response:", saml_response

            samlResponse = Response(currentSamlConfiguration)
            samlResponse.loadXmlFromBase64(saml_response)
            
            saml_validate_response = True
            if (configurationAttributes.containsKey("saml_validate_response")):
                saml_validate_response = StringHelper.toBoolean(configurationAttributes.get("saml_validate_response").getValue2(), False)

            if (saml_validate_response):
                if (not samlResponse.isValid()):
                    print "Saml. Authenticate for step 1. saml_response isn't valid"

            saml_response_name_id = samlResponse.getNameId()
            if (StringHelper.isEmpty(saml_response_name_id)):
                print "Saml. Authenticate for step 1. saml_response_name_id is invalid"
                return False

            print "Saml. Authenticate for step 1. saml_response_name_id:", saml_response_name_id

            saml_response_attributes = samlResponse.getAttributes()
            print "Saml. Authenticate for step 1. attributes: ", saml_response_attributes

            # Use persistent Id as saml_user_uid
            saml_user_uid = saml_response_name_id
            
            if (saml_map_user):
                # Use mapping to local IDP user
                print "Saml. Authenticate for step 1. Attempting to find user by oxExternalUid: saml:", saml_user_uid

                # Check if the is user with specified saml_user_uid
                find_user_by_uid = userService.getUserByAttribute("oxExternalUid", "saml:" + saml_user_uid)

                if (find_user_by_uid == None):
                    print "Saml. Authenticate for step 1. Failed to find user"
                    print "Saml. Authenticate for step 1. Setting count steps to 2"
                    context.set("saml_count_login_steps", 2)
                    context.set("saml_user_uid", saml_user_uid)
                    return True

                found_user_name = find_user_by_uid.getUserId()
                print "Saml. Authenticate for step 1. found_user_name:", found_user_name
                
                user_authenticated = authenticationService.authenticate(found_user_name)
                if (user_authenticated == False):
                    print "Saml. Authenticate for step 1. Failed to authenticate user"
                    return False
            
                print "Saml. Authenticate for step 1. Setting count steps to 1"
                context.set("saml_count_login_steps", 1)

                post_login_result = self.samlExtensionPostLogin(configurationAttributes, find_user_by_uid)
                print "Saml. Authenticate for step 1. post_login_result:", post_login_result

                return post_login_result
            elif (saml_enroll_user):
                # Use auto enrollment to local IDP
                print "Saml. Authenticate for step 1. Attempting to find user by oxExternalUid: saml:", saml_user_uid

                # Check if the is user with specified saml_user_uid
                find_user_by_uid = userService.getUserByAttribute("oxExternalUid", "saml:" + saml_user_uid)

                if (find_user_by_uid == None):
                    # Auto user enrollemnt
                    print "Saml. Authenticate for step 1. There is no user in LDAP. Adding user to local LDAP"

                    # Convert saml result attributes keys to lover case
                    saml_response_normalized_attributes = HashMap()
                    for saml_response_attribute_entry in saml_response_attributes.entrySet():
                        saml_response_normalized_attributes.put(
                            StringHelper.toLowerCase(saml_response_attribute_entry.getKey()), saml_response_attribute_entry.getValue())

                    currentAttributesMapping = self.prepareCurrentAttributesMapping(self.attributesMapping, configurationAttributes, requestParameters)
                    print "Saml. Authenticate for step 1. Using next attributes mapping", currentAttributesMapping

                    newUser = User()
                    for attributesMappingEntry in currentAttributesMapping.entrySet():
                        idpAttribute = attributesMappingEntry.getKey()
                        localAttribute = attributesMappingEntry.getValue()

                        localAttributeValue = saml_response_normalized_attributes.get(idpAttribute)
                        if (localAttribute != None):
                            newUser.setAttribute(localAttribute, localAttributeValue)

                    newUser.setAttribute("oxExternalUid", "saml:" + saml_user_uid)
                    print "Saml. Authenticate for step 1. Attempting to add user", saml_user_uid, " with next attributes", newUser.getCustomAttributes()

                    find_user_by_uid = userService.addUser(newUser, True)
                    print "Saml. Authenticate for step 1. Added new user with UID", find_user_by_uid.getUserId()

                found_user_name = find_user_by_uid.getUserId()
                print "Saml. Authenticate for step 1. found_user_name:", found_user_name

                user_authenticated = authenticationService.authenticate(found_user_name)
                if (user_authenticated == False):
                    print "Saml. Authenticate for step 1. Failed to authenticate user"
                    return False

                print "Saml. Authenticate for step 1. Setting count steps to 1"
                context.set("saml_count_login_steps", 1)

                post_login_result = self.samlExtensionPostLogin(configurationAttributes, find_user_by_uid)
                print "Saml. Authenticate for step 1. post_login_result:", post_login_result

                return post_login_result
            elif (saml_enroll_all_user_attr):
                print "Saml. Authenticate for step 1. Attempting to find user by oxExternalUid: saml:" + saml_user_uid

                # Check if the is user with specified saml_user_uid
                find_user_by_uid = userService.getUserByAttribute("oxExternalUid", "saml:" + saml_user_uid)

                if (find_user_by_uid == None):
                    print "Saml. Authenticate for step 1. Failed to find user"

                    user = User()
                    customAttributes = ArrayList()
                    for key in attributes.keySet():
                        ldapAttributes = attributeService.getAllAttributes()
                        for ldapAttribute in ldapAttributes:
                            saml2Uri = ldapAttribute.getSaml2Uri()
                            if(saml2Uri == None):
                                saml2Uri = attributeService.getDefaultSaml2Uri(ldapAttribute.getName())
                            if(saml2Uri == key):
                                attribute = CustomAttribute(ldapAttribute.getName())
                                attribute.setValues(attributes.get(key))
                                customAttributes.add(attribute)

                    attribute = CustomAttribute("oxExternalUid")
                    attribute.setValue("saml:" + saml_user_uid)
                    customAttributes.add(attribute)
                    user.setCustomAttributes(customAttributes)

                    if(user.getAttribute("sn") == None):
                        attribute = CustomAttribute("sn")
                        attribute.setValue(saml_user_uid)
                        customAttributes.add(attribute)

                    if(user.getAttribute("cn") == None):
                        attribute = CustomAttribute("cn")
                        attribute.setValue(saml_user_uid)
                        customAttributes.add(attribute)

                    find_user_by_uid = userService.addUser(user, True)
                    print "Saml. Authenticate for step 1. Added new user with UID", find_user_by_uid.getUserId()

                found_user_name = find_user_by_uid.getUserId()
                print "Saml. Authenticate for step 1. found_user_name:", found_user_name

                user_authenticated = authenticationService.authenticate(found_user_name)
                if (user_authenticated == False):
                    print "Saml. Authenticate for step 1. Failed to authenticate user"
                    return False

                print "Saml. Authenticate for step 1. Setting count steps to 1"
                context.set("saml_count_login_steps", 1)

                post_login_result = self.samlExtensionPostLogin(configurationAttributes, find_user_by_uid)
                print "Saml. Authenticate for step 1. post_login_result:", post_login_result

                return post_login_result
            else:
                # Check if the is user with specified saml_user_uid
                print "Saml. Authenticate for step 1. Attempting to find user by uid:", saml_user_uid

                find_user_by_uid = userService.getUser(saml_user_uid)
                if (find_user_by_uid == None):
                    print "Saml. Authenticate for step 1. Failed to find user"
                    return False

                found_user_name = find_user_by_uid.getUserId()
                print "Saml. Authenticate for step 1. found_user_name:", found_user_name

                user_authenticated = authenticationService.authenticate(found_user_name)
                if (user_authenticated == False):
                    print "Saml. Authenticate for step 1. Failed to authenticate user"
                    return False

                print "Saml. Authenticate for step 1. Setting count steps to 1"
                context.set("saml_count_login_steps", 1)

                post_login_result = self.samlExtensionPostLogin(configurationAttributes, find_user_by_uid)
                print "Saml. Authenticate for step 1. post_login_result:", post_login_result

                return post_login_result
        elif (step == 2):
            print "Saml. Authenticate for step 2"

            sessionAttributes = context.get("sessionAttributes")
            if (sessionAttributes == None) or not sessionAttributes.containsKey("saml_user_uid"):
                print "Saml. Authenticate for step 2. saml_user_uid is empty"
                return False

            saml_user_uid = sessionAttributes.get("saml_user_uid")
            passed_step1 = StringHelper.isNotEmptyString(saml_user_uid)
            if (not passed_step1):
                return False

            credentials = Identity.instance().getCredentials()
            user_name = credentials.getUsername()
            user_password = credentials.getPassword()

            logged_in = False
            if (StringHelper.isNotEmptyString(user_name) and StringHelper.isNotEmptyString(user_password)):
                logged_in = userService.authenticate(user_name, user_password)

            if (not logged_in):
                return False

            # Check if there is user which has saml_user_uid
            # Avoid mapping Saml account to more than one IDP account
            find_user_by_uid = userService.getUserByAttribute("oxExternalUid", "saml:" + saml_user_uid)

            if (find_user_by_uid == None):
                # Add saml_user_uid to user one id UIDs
                find_user_by_uid = userService.addUserAttribute(user_name, "oxExternalUid", "saml:" + saml_user_uid)
                if (find_user_by_uid == None):
                    print "Saml. Authenticate for step 2. Failed to update current user"
                    return False

                post_login_result = self.samlExtensionPostLogin(configurationAttributes, find_user_by_uid)
                print "Saml. Authenticate for step 2. post_login_result:", post_login_result

                return post_login_result
            else:
                found_user_name = find_user_by_uid.getUserId()
                print "Saml. Authenticate for step 2. found_user_name:", found_user_name
    
                if StringHelper.equals(user_name, found_user_name):
                    post_login_result = self.samlExtensionPostLogin(configurationAttributes, find_user_by_uid)
                    print "Saml. Authenticate for step 2. post_login_result:", post_login_result
    
                    return post_login_result
        
            return False
        else:
            return False

    def prepareForStep(self, configurationAttributes, requestParameters, step):
        context = Contexts.getEventContext()
        authenticationService = AuthenticationService.instance()

        if (step == 1):
            print "Saml. Prepare for step 1"
            
            httpService = HttpService.instance();
            request = FacesContext.getCurrentInstance().getExternalContext().getRequest()
            assertionConsumerServiceUrl = httpService.constructServerUrl(request) + "/postlogin"
            print "Saml. Prepare for step 1. Prepared assertionConsumerServiceUrl:", assertionConsumerServiceUrl
            
            currentSamlConfiguration = self.getCurrentSamlConfiguration(self.samlConfiguration, configurationAttributes, requestParameters)
            if (currentSamlConfiguration == None):
                print "Saml. Prepare for step 1. Client saml configuration is invalid"
                return False

            # Generate an AuthRequest and send it to the identity provider
            samlAuthRequest = AuthRequest(currentSamlConfiguration)
            external_auth_request_uri = currentSamlConfiguration.getIdpSsoTargetUrl() + "?SAMLRequest=" + samlAuthRequest.getRequest(True, assertionConsumerServiceUrl)

            print "Saml. Prepare for step 1. external_auth_request_uri:", external_auth_request_uri
            
            context.set("external_auth_request_uri", external_auth_request_uri)

            return True
        elif (step == 2):
            print "Saml. Prepare for step 2"

            return True
        else:
            return False

    def getExtraParametersForStep(self, configurationAttributes, step):
        if (step == 2):
            return Arrays.asList("saml_user_uid")

        return None

    def getCountAuthenticationSteps(self, configurationAttributes):
        context = Contexts.getEventContext()
        if (context.isSet("saml_count_login_steps")):
            return context.get("saml_count_login_steps")
        
        return 2

    def getPageForStep(self, configurationAttributes, step):
        if (step == 1):
            saml_allow_basic_login = False
            if (configurationAttributes.containsKey("saml_allow_basic_login")):
                saml_allow_basic_login = StringHelper.toBoolean(configurationAttributes.get("saml_allow_basic_login").getValue2(), False)

            if (saml_allow_basic_login):
                return "/login.xhtml"
            else:
                return "/auth/saml/samllogin.xhtml"

        return "/auth/saml/samlpostlogin.xhtml"

    def logout(self, configurationAttributes, requestParameters):
        return True

    def isPassedStep1():
        credentials = Identity.instance().getCredentials()
        user_name = credentials.getUsername()
        passed_step1 = StringHelper.isNotEmptyString(user_name)

        return passed_step1

    def loadCeritificate(self, saml_certificate_file):
        saml_certificate = None

        # Load certificate from file
        f = open(saml_certificate_file, 'r')
        try:
            saml_certificate = f.read()
        except:
            print "Failed to load certificate from file:", saml_certificate_file
            return None
        finally:
            f.close()
        
        return saml_certificate

    def getClientConfiguration(self, configurationAttributes, requestParameters):
        # Get client configuration
        if (configurationAttributes.containsKey("saml_client_configuration_attribute")):
            saml_client_configuration_attribute = configurationAttributes.get("saml_client_configuration_attribute").getValue2()
            print "Saml. GetClientConfiguration. Using client attribute:", saml_client_configuration_attribute

            if (requestParameters == None):
                return None

            client_id = None
            client_id_array = requestParameters.get("client_id")
            if (ArrayHelper.isNotEmpty(client_id_array) and StringHelper.isNotEmptyString(client_id_array[0])):
                client_id = client_id_array[0]

            if (client_id == None):
                eventContext = Contexts.getEventContext()
                if (eventContext.isSet("sessionAttributes")):
                    client_id = eventContext.get("sessionAttributes").get("client_id")

            if (client_id == None):
                print "Saml. GetClientConfiguration. client_id is empty"
                return None

            clientService = ClientService.instance()
            client = clientService.getClient(client_id)
            if (client == None):
                print "Saml. GetClientConfiguration. Failed to find client", client_id, " in local LDAP"
                return None

            saml_client_configuration = clientService.getCustomAttribute(client, saml_client_configuration_attribute)
            if ((saml_client_configuration == None) or StringHelper.isEmpty(saml_client_configuration.getValue())):
                print "Saml. GetClientConfiguration. Client", client_id, " attribute", saml_client_configuration_attribute, " is empty"
            else:
                print "Saml. GetClientConfiguration. Client", client_id, " attribute", saml_client_configuration_attribute, " is", saml_client_configuration
                return saml_client_configuration

        return None

    def getCurrentSamlConfiguration(self, currentSamlConfiguration, configurationAttributes, requestParameters):
        saml_client_configuration = self.getClientConfiguration(configurationAttributes, requestParameters)
        if (saml_client_configuration == None):
            return currentSamlConfiguration
        
        saml_client_configuration_value = json.loads(saml_client_configuration.getValue())

        client_saml_certificate = None      
        client_saml_certificate_file = saml_client_configuration_value["saml_certificate_file"]
        if (StringHelper.isNotEmpty(client_saml_certificate_file)):
            client_saml_certificate = self.loadCeritificate(client_saml_certificate_file)
            if (StringHelper.isEmpty(client_saml_certificate)):
                print "Saml. BuildClientSamlConfiguration. File with x509 certificate should be not empty. Using default configuration"
                return currentSamlConfiguration

        clientSamlConfiguration = currentSamlConfiguration.clone()
        
        if (client_saml_certificate != None):
            clientSamlConfiguration.loadCertificateFromString(client_saml_certificate)

        client_saml_issuer = saml_client_configuration_value["saml_issuer"]
        clientSamlConfiguration.setIssuer(client_saml_issuer)
        
        saml_use_authn_context = saml_client_configuration_value["saml_use_authn_context"]
        client_use_saml_use_authn_context = StringHelper.toBoolean(saml_use_authn_context, True)
        clientSamlConfiguration.setUseRequestedAuthnContext(client_use_saml_use_authn_context)

        return clientSamlConfiguration

    def prepareAttributesMapping(self, saml_idp_attributes_list, saml_local_attributes_list):
        saml_idp_attributes_list_array = StringHelper.split(saml_idp_attributes_list, ",")
        if (ArrayHelper.isEmpty(saml_idp_attributes_list_array)):
            print "Saml. PrepareAttributesMapping. There is no attributes specified in saml_idp_attributes_list property"
            return None
        
        saml_local_attributes_list_array = StringHelper.split(saml_local_attributes_list, ",")
        if (ArrayHelper.isEmpty(saml_local_attributes_list_array)):
            print "Saml. PrepareAttributesMapping. There is no attributes specified in saml_local_attributes_list property"
            return None

        if (len(saml_idp_attributes_list_array) != len(saml_local_attributes_list_array)):
            print "Saml. PrepareAttributesMapping. The number of attributes in saml_idp_attributes_list and saml_local_attributes_list isn't equal"
            return None
        
        attributeMapping = IdentityHashMap()
        containsUid = False
        i = 0
        count = len(saml_idp_attributes_list_array)
        while (i < count):
            idpAttribute = StringHelper.toLowerCase(saml_idp_attributes_list_array[i])
            localAttribute = StringHelper.toLowerCase(saml_local_attributes_list_array[i])
            attributeMapping.put(idpAttribute, localAttribute)

            if (StringHelper.equalsIgnoreCase(localAttribute, "uid")):
                containsUid = True

            i = i + 1

        if (not containsUid):
            print "Saml. PrepareAttributesMapping. There is no mapping to mandatory 'uid' attribute"
            return None
        
        return attributeMapping

    def prepareCurrentAttributesMapping(self, currentAttributesMapping, configurationAttributes, requestParameters):
        saml_client_configuration = self.getClientConfiguration(configurationAttributes, requestParameters)
        if (saml_client_configuration == None):
            return currentAttributesMapping

        saml_client_configuration_value = json.loads(saml_client_configuration.getValue())

        clientAttributesMapping = self.prepareAttributesMapping(saml_client_configuration_value["saml_idp_attributes_list"], saml_client_configuration_value["saml_local_attributes_list"])
        if (clientAttributesMapping == None):
            print "Saml. PrepareCurrentAttributesMapping. Client attributes mapping is invalid. Using default one"
            return currentAttributesMapping

        return clientAttributesMapping

    def samlExtensionPostLogin(self, configurationAttributes, user):
        if (self.samlExtensionModule != None):
            try:
                post_login_result = self.samlExtensionModule.postLogin(configurationAttributes, user)
                print "Saml. ExtensionPostlogin result:", post_login_result

                return post_login_result
            except Exception, ex:
                print "Saml. ExtensionPostlogin. Failed to execute postLogin method"
                print "Saml. ExtensionPostlogin. Unexpected error:", ex
                return False
            except java.lang.Throwable, ex:
                print "Saml. ExtensionPostlogin. Failed to execute postLogin method"
                ex.printStackTrace() 
                return False
                    
        return True
```

## Metadata for 'test.gluu.org/saml'

```
<md:EntityDescriptor xmlns:md="urn:oasis:names:tc:SAML:2.0:metadata" entityID="https://test.gluu.org/saml">
  <md:SPSSODescriptor protocolSupportEnumeration="urn:oasis:names:tc:SAML:2.0:protocol">
    <md:AssertionConsumerService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST" Location="https://test.gluu.org/oxauth/postlogin" index="0"/>
  </md:SPSSODescriptor>
  <md:Organization>
    <md:OrganizationName xml:lang="en">Gluu</md:OrganizationName>
    <md:OrganizationDisplayName xml:lang="en">Gluu - Open Source Access Management</md:OrganizationDisplayName>
    <md:OrganizationURL xml:lang="en">http://www.gluu.org</md:OrganizationURL>
  </md:Organization>
  <md:ContactPerson contactType="technical">
    <md:GivenName>Administrator</md:GivenName>
    <md:EmailAddress>support@gluu.org</md:EmailAddress>
  </md:ContactPerson>
</md:EntityDescriptor>
```



## sp.gluu.org configuration files

### shibboleth2.xml
```
<SPConfig xmlns="urn:mace:shibboleth:2.0:native:sp:config"
    xmlns:conf="urn:mace:shibboleth:2.0:native:sp:config"
    xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"
    xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol"
    xmlns:md="urn:oasis:names:tc:SAML:2.0:metadata"
    clockSkew="180">

    <!--
    By default, in-memory StorageService, ReplayCache, ArtifactMap, and SessionCache
    are used. See example-shibboleth2.xml for samples of explicitly configuring them.
    -->

    <!--
    To customize behavior for specific resources on Apache, and to link vhosts or
    resources to ApplicationOverride settings below, use web server options/commands.
    See https://wiki.shibboleth.net/confluence/display/SHIB2/NativeSPConfigurationElements for help.

    For examples with the RequestMap XML syntax instead, see the example-shibboleth2.xml
    file, and the https://wiki.shibboleth.net/confluence/display/SHIB2/NativeSPRequestMapHowTo topic.
    -->

    <!-- The ApplicationDefaults element is where most of Shibboleth's SAML bits are defined. -->
    <ApplicationDefaults entityID="https://sp.gluu.org/shibboleth"
                         REMOTE_USER="eppn persistent-id targeted-id">

        <!--
        Controls session lifetimes, address checks, cookie handling, and the protocol handlers.
        You MUST supply an effectively unique handlerURL value for each of your applications.
        The value defaults to /Shibboleth.sso, and should be a relative path, with the SP computing
        a relative value based on the virtual host. Using handlerSSL="true", the default, will force
        the protocol to be https. You should also set cookieProps to "https" for SSL-only sites.
        Note that while we default checkAddress to "false", this has a negative impact on the
        security of your site. Stealing sessions via cookie theft is much easier with this disabled.
        -->
        <Sessions lifetime="28800" timeout="3600" relayState="ss:mem"
                  checkAddress="false" handlerSSL="false" cookieProps="http">

            <!--
            Configures SSO for a default IdP. To allow for >1 IdP, remove
            entityID property and adjust discoveryURL to point to discovery service.
            (Set discoveryProtocol to "WAYF" for legacy Shibboleth WAYF support.)
            You can also override entityID on /Login query string, or in RequestMap/htaccess.
            -->
            <SSO entityID="https://test.gluu.org/idp/shibboleth"
                 discoveryProtocol="SAMLDS" discoveryURL="https://ds.example.org/DS/WAYF">
              SAML2 SAML1
            </SSO>

            <!-- SAML and local-only logout. -->
            <Logout>SAML2 Local</Logout>

            <!-- Extension service that generates "approximate" metadata based on SP configuration. -->
            <Handler type="MetadataGenerator" Location="/Metadata" signing="false"/>

            <!-- Status reporting service. -->
            <Handler type="Status" Location="/Status" acl="127.0.0.1 ::1"/>

            <!-- Session diagnostic service. -->
            <Handler type="Session" Location="/Session" showAttributeValues="false"/>

            <!-- JSON feed of discovery information. -->
            <Handler type="DiscoveryFeed" Location="/DiscoFeed"/>
        </Sessions>

        <!--
        Allows overriding of error template information/filenames. You can
        also add attributes with values that can be plugged into the templates.
        -->
        <Errors supportContact="root@localhost"
            helpLocation="/about.html"
            styleSheet="/shibboleth-sp/main.css"/>

        <!-- Example of remotely supplied batch of signed metadata. -->
        <!--
        <MetadataProvider type="XML" uri="http://federation.org/federation-metadata.xml"
              backingFilePath="federation-metadata.xml" reloadInterval="7200">
            <MetadataFilter type="RequireValidUntil" maxValidityInterval="2419200"/>
            <MetadataFilter type="Signature" certificate="fedsigner.pem"/>
        </MetadataProvider>
        -->

        <!-- Example of locally maintained metadata. -->
        <!--
        <MetadataProvider type="XML" file="partner-metadata.xml"/>
        -->

        <MetadataProvider type="XML" validate="true" file="/etc/shibboleth/test_gluu_org_metadata.xml"/>

        <!-- Map to extract attributes from SAML assertions. -->
        <AttributeExtractor type="XML" validate="true" reloadChanges="false" path="attribute-map.xml"/>

        <!-- Use a SAML query if no attributes are supplied during SSO. -->
        <AttributeResolver type="Query" subjectMatch="true"/>

        <!-- Default filtering policy for recognized attributes, lets other data pass. -->
        <AttributeFilter type="XML" validate="true" path="attribute-policy.xml"/>

        <!-- Simple file-based resolver for using a single keypair. -->
        <CredentialResolver type="File" key="/etc/certs/sp_gluu_org.key" certificate="/etc/certs/sp_gluu_org.crt"/>

        <!--
        The default settings can be overridden by creating ApplicationOverride elements (see
        the https://wiki.shibboleth.net/confluence/display/SHIB2/NativeSPApplicationOverride topic).
        Resource requests are mapped by web server commands, or the RequestMapper, to an
        applicationId setting.

        Example of a second application (for a second vhost) that has a different entityID.
        Resources on the vhost would map to an applicationId of "admin":
        -->
        <!--
        <ApplicationOverride id="admin" entityID="https://admin.example.org/shibboleth"/>
        -->
    </ApplicationDefaults>

    <!-- Policies that determine how to process and authenticate runtime messages. -->
    <SecurityPolicyProvider type="XML" validate="true" path="security-policy.xml"/>

    <!-- Low-level configuration about protocols and bindings available for use. -->
    <ProtocolProvider type="XML" validate="true" reloadChanges="false" path="protocols.xml"/>

</SPConfig>

```

### attribute-map.xml

```
<Attributes xmlns="urn:mace:shibboleth:2.0:attribute-map" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

    <!--
    The mappings are a mix of SAML 1.1 and SAML 2.0 attribute names agreed to within the Shibboleth
    community. The non-OID URNs are SAML 1.1 names and most of the OIDs are SAML 2.0 names, with a
    few exceptions for newer attributes where the name is the same for both versions. You will
    usually want to uncomment or map the names for both SAML versions as a unit.
    -->

    <!-- First some useful eduPerson attributes that many sites might use. -->

    <Attribute name="urn:mace:dir:attribute-def:eduPersonPrincipalName" id="eppn">
        <AttributeDecoder xsi:type="ScopedAttributeDecoder"/>
    </Attribute>
    <Attribute name="urn:oid:1.3.6.1.4.1.5923.1.1.1.6" id="eppn">
        <AttributeDecoder xsi:type="ScopedAttributeDecoder"/>
    </Attribute>

    <Attribute name="urn:mace:dir:attribute-def:eduPersonScopedAffiliation" id="affiliation">
        <AttributeDecoder xsi:type="ScopedAttributeDecoder" caseSensitive="false"/>
    </Attribute>
    <Attribute name="urn:oid:1.3.6.1.4.1.5923.1.1.1.9" id="affiliation">
        <AttributeDecoder xsi:type="ScopedAttributeDecoder" caseSensitive="false"/>
    </Attribute>

    <Attribute name="urn:mace:dir:attribute-def:eduPersonAffiliation" id="unscoped-affiliation">
        <AttributeDecoder xsi:type="StringAttributeDecoder" caseSensitive="false"/>
    </Attribute>
    <Attribute name="urn:oid:1.3.6.1.4.1.5923.1.1.1.1" id="unscoped-affiliation">
        <AttributeDecoder xsi:type="StringAttributeDecoder" caseSensitive="false"/>
    </Attribute>

    <Attribute name="urn:mace:dir:attribute-def:eduPersonEntitlement" id="entitlement"/>
    <Attribute name="urn:oid:1.3.6.1.4.1.5923.1.1.1.7" id="entitlement"/>

    <!-- A persistent id attribute that supports personalized anonymous access. -->

    <!-- First, the deprecated/incorrect version, decoded as a scoped string: -->
    <Attribute name="urn:mace:dir:attribute-def:eduPersonTargetedID" id="targeted-id">
        <AttributeDecoder xsi:type="ScopedAttributeDecoder"/>
        <!-- <AttributeDecoder xsi:type="NameIDFromScopedAttributeDecoder" formatter="$NameQualifier!$SPNameQualifier!$Name" defaultQualifiers="true"/> -->
    </Attribute>

    <!-- Second, an alternate decoder that will decode the incorrect form into the newer form. -->
    <!--
    <Attribute name="urn:mace:dir:attribute-def:eduPersonTargetedID" id="persistent-id">
        <AttributeDecoder xsi:type="NameIDFromScopedAttributeDecoder" formatter="$NameQualifier!$SPNameQualifier!$Name" defaultQualifiers="true"/>
    </Attribute>
    -->

    <!-- Third, the new version (note the OID-style name): -->
    <Attribute name="urn:oid:1.3.6.1.4.1.5923.1.1.1.10" id="persistent-id">
        <AttributeDecoder xsi:type="NameIDAttributeDecoder" formatter="$NameQualifier!$SPNameQualifier!$Name" defaultQualifiers="true"/>
    </Attribute>

    <!-- Fourth, the SAML 2.0 NameID Format: -->
    <Attribute name="urn:oasis:names:tc:SAML:2.0:nameid-format:persistent" id="persistent-id">
        <AttributeDecoder xsi:type="NameIDAttributeDecoder" formatter="$NameQualifier!$SPNameQualifier!$Name" defaultQualifiers="true"/>
    </Attribute>

    <!-- Some more eduPerson attributes, uncomment these to use them... -->
    <!--
    <Attribute name="urn:mace:dir:attribute-def:eduPersonPrimaryAffiliation" id="primary-affiliation">
        <AttributeDecoder xsi:type="StringAttributeDecoder" caseSensitive="false"/>
    </Attribute>
    <Attribute name="urn:mace:dir:attribute-def:eduPersonNickname" id="nickname"/>
    <Attribute name="urn:mace:dir:attribute-def:eduPersonPrimaryOrgUnitDN" id="primary-orgunit-dn"/>
    <Attribute name="urn:mace:dir:attribute-def:eduPersonOrgUnitDN" id="orgunit-dn"/>
    <Attribute name="urn:mace:dir:attribute-def:eduPersonOrgDN" id="org-dn"/>

    <Attribute name="urn:oid:1.3.6.1.4.1.5923.1.1.1.5" id="primary-affiliation">
        <AttributeDecoder xsi:type="StringAttributeDecoder" caseSensitive="false"/>
    </Attribute>
    <Attribute name="urn:oid:1.3.6.1.4.1.5923.1.1.1.2" id="nickname"/>
    <Attribute name="urn:oid:1.3.6.1.4.1.5923.1.1.1.8" id="primary-orgunit-dn"/>
    <Attribute name="urn:oid:1.3.6.1.4.1.5923.1.1.1.4" id="orgunit-dn"/>
    <Attribute name="urn:oid:1.3.6.1.4.1.5923.1.1.1.3" id="org-dn"/>

    <Attribute name="urn:oid:1.3.6.1.4.1.5923.1.1.1.11" id="assurance"/>

    <Attribute name="urn:oid:1.3.6.1.4.1.5923.1.5.1.1" id="member"/>

    <Attribute name="urn:oid:1.3.6.1.4.1.5923.1.6.1.1" id="eduCourseOffering"/>
    <Attribute name="urn:oid:1.3.6.1.4.1.5923.1.6.1.2" id="eduCourseMember"/>
    -->

    <!-- Examples of LDAP-based attributes, uncomment to use these... -->
    <!--
    <Attribute name="urn:mace:dir:attribute-def:cn" id="cn"/>
    <Attribute name="urn:mace:dir:attribute-def:sn" id="sn"/>
    <Attribute name="urn:mace:dir:attribute-def:givenName" id="givenName"/>
    <Attribute name="urn:mace:dir:attribute-def:displayName" id="displayName"/>
    <Attribute name="urn:mace:dir:attribute-def:mail" id="mail"/>
    <Attribute name="urn:mace:dir:attribute-def:telephoneNumber" id="telephoneNumber"/>
    <Attribute name="urn:mace:dir:attribute-def:title" id="title"/>
    <Attribute name="urn:mace:dir:attribute-def:initials" id="initials"/>
    <Attribute name="urn:mace:dir:attribute-def:description" id="description"/>
    <Attribute name="urn:mace:dir:attribute-def:carLicense" id="carLicense"/>
    <Attribute name="urn:mace:dir:attribute-def:departmentNumber" id="departmentNumber"/>
    <Attribute name="urn:mace:dir:attribute-def:employeeNumber" id="employeeNumber"/>
    <Attribute name="urn:mace:dir:attribute-def:employeeType" id="employeeType"/>
    <Attribute name="urn:mace:dir:attribute-def:preferredLanguage" id="preferredLanguage"/>
    <Attribute name="urn:mace:dir:attribute-def:manager" id="manager"/>
    <Attribute name="urn:mace:dir:attribute-def:seeAlso" id="seeAlso"/>
    <Attribute name="urn:mace:dir:attribute-def:facsimileTelephoneNumber" id="facsimileTelephoneNumber"/>
    <Attribute name="urn:mace:dir:attribute-def:street" id="street"/>
    <Attribute name="urn:mace:dir:attribute-def:postOfficeBox" id="postOfficeBox"/>
    <Attribute name="urn:mace:dir:attribute-def:postalCode" id="postalCode"/>
    <Attribute name="urn:mace:dir:attribute-def:st" id="st"/>
    <Attribute name="urn:mace:dir:attribute-def:l" id="l"/>
    <Attribute name="urn:mace:dir:attribute-def:o" id="o"/>
    <Attribute name="urn:mace:dir:attribute-def:ou" id="ou"/>
    <Attribute name="urn:mace:dir:attribute-def:businessCategory" id="businessCategory"/>
    <Attribute name="urn:mace:dir:attribute-def:physicalDeliveryOfficeName" id="physicalDeliveryOfficeName"/>

    <Attribute name="urn:oid:2.5.4.3" id="cn"/>
    <Attribute name="urn:oid:2.5.4.4" id="sn"/>
    <Attribute name="urn:oid:2.5.4.42" id="givenName"/>
    <Attribute name="urn:oid:2.16.840.1.113730.3.1.241" id="displayName"/>
    <Attribute name="urn:oid:0.9.2342.19200300.100.1.3" id="mail"/>
    <Attribute name="urn:oid:2.5.4.20" id="telephoneNumber"/>
    <Attribute name="urn:oid:2.5.4.12" id="title"/>
    <Attribute name="urn:oid:2.5.4.43" id="initials"/>
    <Attribute name="urn:oid:2.5.4.13" id="description"/>
    <Attribute name="urn:oid:2.16.840.1.113730.3.1.1" id="carLicense"/>
    <Attribute name="urn:oid:2.16.840.1.113730.3.1.2" id="departmentNumber"/>
    <Attribute name="urn:oid:2.16.840.1.113730.3.1.3" id="employeeNumber"/>
    <Attribute name="urn:oid:2.16.840.1.113730.3.1.4" id="employeeType"/>
    <Attribute name="urn:oid:2.16.840.1.113730.3.1.39" id="preferredLanguage"/>
    <Attribute name="urn:oid:0.9.2342.19200300.100.1.10" id="manager"/>
    <Attribute name="urn:oid:2.5.4.34" id="seeAlso"/>
    <Attribute name="urn:oid:2.5.4.23" id="facsimileTelephoneNumber"/>
    <Attribute name="urn:oid:2.5.4.9" id="street"/>
    <Attribute name="urn:oid:2.5.4.18" id="postOfficeBox"/>
    <Attribute name="urn:oid:2.5.4.17" id="postalCode"/>
    <Attribute name="urn:oid:2.5.4.8" id="st"/>
    <Attribute name="urn:oid:2.5.4.7" id="l"/>
    <Attribute name="urn:oid:2.5.4.10" id="o"/>
    <Attribute name="urn:oid:2.5.4.11" id="ou"/>
    <Attribute name="urn:oid:2.5.4.15" id="businessCategory"/>
    <Attribute name="urn:oid:2.5.4.19" id="physicalDeliveryOfficeName"/>
    -->


    <Attribute name="urn:oid:0.9.2342.19200300.100.1.1" id="uid"/>
    <Attribute name="urn:oid:0.9.2342.19200300.100.1.3" id="mail"/>

</Attributes>
```
