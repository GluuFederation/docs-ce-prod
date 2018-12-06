# oxAuth is available under the MIT License (2008). See http://opensource.org/licenses/MIT for full text.
# Copyright (c) 2016, Gluu
#
# Author: Yuriy Movchan
#

from org.xdi.model.custom.script.type.scope import DynamicScopeType
from org.xdi.util import StringHelper, ArrayHelper
from java.util import Arrays, ArrayList

import java

class DynamicScope(DynamicScopeType):
    def __init__(self, currentTimeMillis):
        self.currentTimeMillis = currentTimeMillis

    def init(self, configurationAttributes):
        print "Dynamic scope. Initialization"

        print "Dynamic scope. Initialized successfully"

        return True   

    def destroy(self, configurationAttributes):
        print "Dynamic scope. Destroy"
        print "Dynamic scope. Destroyed successfully"
        return True   

    # Update Json Web token before signing/encrypting it
    #   dynamicScopeContext is org.xdi.oxauth.service.external.context.DynamicScopeExternalContext
    #   configurationAttributes is java.util.Map<String, SimpleCustomProperty>
    def update(self, dynamicScopeContext, configurationAttributes):
        print "Dynamic scope. Update method"

        dynamicScopes = dynamicScopeContext.getDynamicScopes()
        user = dynamicScopeContext.getUser()
        jsonToken = dynamicScopeContext.getJsonToken()
        claims = jsonToken.getClaims()

        # Iterate through list of dynamic scopes in order to add custom scopes if needed
        print "Dynamic scope. Dynamic scopes:", dynamicScopes
        for dynamicScope in dynamicScopes:
            # Add organization name if there is scope = org_name
            if (StringHelper.equalsIgnoreCase(dynamicScope, "org_name")):
                claims.setClaim("org_name", "Gluu, Inc.")
                continue

            # Add work phone if there is scope = work_phone
            if (StringHelper.equalsIgnoreCase(dynamicScope, "work_phone")):
                workPhone = user.getAttribute("telephoneNumber");
                if (StringHelper.isNotEmpty(workPhone)):
                    claims.setClaim("work_phone", workPhone)
                continue

        return True

    def getApiVersion(self):
        return 1
