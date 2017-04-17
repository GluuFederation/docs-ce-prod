from org.xdi.model.custom.script.type.uma import AuthorizationPolicyType
from org.xdi.util import StringHelper, ArrayHelper
from java.util import Arrays, ArrayList
from org.xdi.oxauth.service.uma.authorization import AuthorizationContext

import java

class AuthorizationPolicy(AuthorizationPolicyType):
    def __init__(self, currentTimeMillis):
        self.currentTimeMillis = currentTimeMillis

    def init(self, configurationAttributes):
        print "UMA authorization policy. Initialization"
        print "UMA authorization policy. Initialized successfully"

        return True   

    def destroy(self, configurationAttributes):
        print "UMA authorization policy. Destroy"
        print "UMA authorization policy. Destroyed successfully"
        return True   

    def getApiVersion(self):
        return 1

    # Process policy rule
    #   authorizationContext is org.xdi.oxauth.service.uma.authorization.AuthorizationContext
    #   configurationAttributes is java.util.Map<String, SimpleCustomProperty>
    def authorize(self, authorizationContext, configurationAttributes):
        print "UMA Authorization policy. Attempting to authorize client"
        client_id = authorizationContext.getGrant().getClientId()

        print "UMA Authorization policy. Client: ", client_id
        if (StringHelper.equalsIgnoreCase("@!1111!0008!FDC0.0FF5", client_id)):
            print "UMA Authorization policy. Authorizing client"
            return True
        else:
            print "UMA Authorization policy. Client isn't authorized"
            return False

        print "UMA Authorization policy. Authorizing client"
        return True
