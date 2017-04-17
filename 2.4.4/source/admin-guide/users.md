[TOC]

<!--

				********** This part needs some maintenance **********

- [SCIM oxAuth Authentication](#scim-oxauth-authentication)
	- [Base configuration: create oxAuth client](#base-configuration-create-oxauth-client)
	- [configuration (Resource Server)](#configuration-resource-server)
	- [SCIM Client (Requesting Party) sample code](#scim-client-requesting-party-sample-code)
- [SCIM UMA Authentication](#scim-uma-authentication )
	- [Base configuration: Create oxAuth Clients, Policies](#base-configuration-create-oxauth-clients-policies)
	- [oxTrust configuration (Resource Server)](#oxtrust-configuration-resource-server)
	- [SCIM Client (Requesting Party) sample code](#scim-client-requesting-party-sample-code)

-->

# User Management

To keep the Gluu Server up-to-date with the latest user claims, your
organization can either "push" or "pull" identity data. In the "pull"
mode, otherwise known as LDAP Synchronization or Cache Refresh, the Gluu
Server can use an existing LDAP identity source like Microsoft Active
Directory as the authoritative source of identity information. If you
"push" identities to the Gluu Server, you can use the JSON/REST SCIM
API. Local user management can also be performed inside oxTrust. Each
method is detailed below.

## Cache Refresh

Cache Refresh was built by Gluu to pull user information from a backend
Active Directory/LDAP Server. Cache refresh dynamically synchronizes
user information from the backend data source to a local LDAP server in
order to maximize performance. Cache refresh is documented in our
[configuration section](/oxtrust/index.md#cache-refresh).

## Self Registration

Self-Registration is done by users on a self-service basis. Since
oxTrust user registration cannot add users to a backend LDAP or Active
Directory server, self-registration will only be effective if GluuLDAP
is used for authentication of users.

BY default a a limited number of attribute is present in default
self-registration form. If more attributes are needed they can be added
in Registration Management of Organization Configuration. Learn more
about Registration Management
[here](/oxtrust/index.md#manage-registration).

## Local User Management

In oxTrust, you can add, edit and manage people, groups and user
attributes and claims to ensure the proper information is released about
the right people.

### People
To manage people, navigate to User > Manage People, as shown in the
screenshot below.

![](/img/admin-guide/users/manage_people.png)

From this interface you can add users and search for specific users.
Because the user database can potentially be very large, a value is
required in the search field. In other words, you can not click search
with a blank entry to populate all users. If you need to see all users,
this would be best performed manually within the Gluu OpenDJ server.
Upon performing a user search, a list will be populated with all users
that match the search, as shown in the screenshot below.

![Search Users](/img/admin-guide/users/admin_users_searchadmin.png)

To edit a user, simply click on any of the hyperlinks associated with
that user and you will be taken to a user management interface where you
can modify that specific attributes relating to that user as displayed
below.

![Manage Users](/img/admin-guide/users/admin_users_edituser.png)

### Import People
This feature allows the Gluu Server Administrator to bulk import users.
The user *xls* file can be added using the **Add** button.

![Import User](/img/admin-guide/users/admin_config_people.png)

Validation checking for the added *xls* file can be done using the
**Validate** button. If the file is not formatted properly, the server
will reject the same with an error as shown below in the screenshot.

![Validation Error Message](/img/admin-guide/users/admin_config_people_validation.png)

## Groups
Out of the box, the Gluu Server includes one group: Gluu Server manager
group, named: “gluuManager”. Groups can be added and populated as
needed. By using the *Manage Groups* feature, the Gluu Server
Administrator can add, delete or modify any group or user within a
group. The list of available groups can be viewed by hitting the
_Search_ button with a blank search box.
![Manage User Groups](/img/admin-guide/users/admin_users_managegroups.png)

The Gluu Server Administrator can modify information such as Display
Name, Group Owner, Visibility type etc. The Server Administrator can
also add or delete users within existing groups. The group information
is represented as shown below.
![View group information](/img/admin-guide/users/admin_users_groupinfo.png)

If any member of the Organization is required to be added in any
specific group, this can be achieved be clicking on the Add Member
button. The flow is _Add Member --> Search the name/email of the user
--> Select the user --> Click OK --> Update._
![Add Member](/img/admin-guide/users/admin_users_addmember.png)


<!--

				********** This part needs some maintenance **********

## SCIM oxAuth Authentication

This is a step by step guide to configure oxTrust and SCIM client for
oxAuth authentication.

### Base Configuration: Create oxAuth Client
In order to access SCIM endpoints, an oxAuth client should be registered
with scopes "openid" and "user_name". Authentication method (or LDAP
Property “oxAuthTokenEndpointAuthMethod”) of this client should have
value “client_secret_basic”.
 
A new client can be created through various methods: [Client
Registration](http://ox.gluu.org/doku.php?id=oxauth:clientregistration),
using [oxTrust](http://ox.gluu.org/doku.php?id=oxtrust:home) GUI, or
manually adding an entry to LDAP.

Sample result entry:

        dn: inum=@!1111!0008!F781.80AF,ou=clients,o=@!1111,o=gluu
        objectClass: oxAuthClient
        objectClass: top
        displayName: SCIM
        inum: @!1111!0008!F781.80AF
        oxAuthAppType: web
        oxAuthClientSecret: eUXIbkBHgIM=
        oxAuthIdTokenSignedResponseAlg: HS256
        oxAuthScope: inum=@!1111!0009!E4B4,ou=scopes,o=@!1111,o=gluu
        oxAuthScope: inum=@!1111!0009!E4B5,ou=scopes,o=@!1111,o=gluu
        oxAuthTokenEndpointAuthMethod: client_secret_basic

###  Configuration (Resource Server)

It's possible to enable/disable SCIM endpoints in oxTrust under
"Organization Configuration" page.

## SCIM Client (Requesting Party) Sample Code

This is a sample SCIM Client code which requests user information from
server.

    package gluu.scim.client.dev.local;
    
    import gluu.scim.client.ScimClient;
    import gluu.scim.client.ScimResponse;

    import javax.ws.rs.core.MediaType;
    
    public class TestScimClient {
	    public static void main(String[] args) {
		    final ScimClient scimClient = ScimClient.oAuthInstance("admin", "secret", "@!9BCF.396B.14EB.1974!0001!CA0D.1918!0008!2F06.F0DF", "secret",
				    "https://centos65.gluu.info/identity/seam/resource/restv1", "https://centos65.gluu.info/oxauth/seam/resource/restv1/oxauth/token");
		    try {
			    ScimResponse response1 = scimClient.retrievePerson("@!9BCF.396B.14EB.1974!0001!CA0D.1918!0000!A8F2.DE1E.D7FB", MediaType.APPLICATION_JSON);
			    System.out.println(response1.getResponseBodyString());
		    } catch (Exception ex) {
			    ex.printStackTrace();
		    }
	    }
    
    }

Values in this example are correspond to client entry fields from first
section.

## SCIM UMA Authentication

This is step by step guide to configure UMA for oxTrust and SCIM client.
High level architecture overview is available in the following article
[OX SCIM Architecture
Overview](http://ox.gluu.org/doku.php?id=oxtrust:scim:uma_authentication#ox_scim_architecture_overview).

### Base Configuration: Create oxAuth Clients, Policies

1. Register oxAuth client with scope “uma_protection”. Property “oxAuthTokenEndpointAuthMethod” of this client should has value “client_secret_basic”. It's possible to do that using few methods: [Client Registration](http://ox.gluu.org/doku.php?id=oxauth:clientregistration), using [oxTrust](http://ox.gluu.org/doku.php?id=oxtrust:home) GUI, manually add entry to LDAP. oxTrust will use this oxAuth client to obtain PAT. Sample result entry:

        dn: inum=@!1111!0008!F781.80AF,ou=clients,o=@!1111,o=gluu
        objectClass: oxAuthClient
        objectClass: top
        displayName: Resource Server Client
        inum: @!1111!0008!F781.80AF
        oxAuthAppType: web
        oxAuthClientSecret: eUXIbkBHgIM=
        oxAuthIdTokenSignedResponseAlg: HS256
        oxAuthScope: inum=@!1111!0009!6D96,ou=scopes,o=@!1111,o=gluu
        oxAuthTokenEndpointAuthMethod: client_secret_basic

2. Register oxAuth client with scope “uma_authorization”. Property “oxAuthTokenEndpointAuthMethod” of this client should has value “client_secret_basic”. It's possible to do that using few methods: [Client Registration](http://ox.gluu.org/doku.php?id=oxauth:clientregistration), using [oxTrust](http://ox.gluu.org/doku.php?id=oxtrust:home) GUI, manually add entry to LDAP. SCIM Client will use this oxAuth client to obtain AAT. Sample result entry:

        dn: inum=@!1111!0008!FDC0.0FF5,ou=clients,o=@!1111,o=gluu
        objectClass: oxAuthClient
        objectClass: top
        displayName: Requesting Party Client
        inum: @!1111!0008!FDC0.0FF5
        oxAuthAppType: web
        oxAuthClientSecret: eUXIbkBHgIM=
        oxAuthIdTokenSignedResponseAlg: HS256
        oxAuthScope: inum=@!1111!0009!6D97,ou=scopes,o=@!1111,o=gluu
        oxAuthTokenEndpointAuthMethod: client_secret_basic

3. Create UMA policy. These are list of steps which allows to add new policy: 

 	1. Log with administrative privileges into oxTrust.
 	2. Open menu “Configuration→Manage Custom Scripts”.
 	4. Select “UMA Authorization Policies” tab and click “Add custom script configuration”.
 	5. Select language “Python”.
 	6. Paste this base policy script:


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

            # Authorize access to resource
            #   authorizationContext is org.xdi.oxauth.service.uma.authorization.AuthorizationContext
            #   configurationAttributes is java.util.Map<String, SimpleCustomProperty>
            def authorize(self, authorizationContext, configurationAttributes):
                print "UMA Authorization policy. Attempting to authorize client"
                client_id = authorizationContext.getGrant().getClientId()
                user_id = authorizationContext.getGrant().getUserId()

                print "UMA Authorization policy. Client: ", client_id
                print "UMA Authorization policy. User: ", user_id
                if (StringHelper.equalsIgnoreCase("@!1111!0008!FDC0.0FF5", client_id)):
                    print "UMA Authorization policy. Authorizing client"
                    return True
                else:
                    print "UMA Authorization policy. Client isn't authorized"
                    return False

                print "UMA Authorization policy. Authorizing client"
                return True
 - Replace in script above client inum "@!1111!0008!FDC0.0FF5" with client inum which were added in step 2.
 - Click "Enabled" check box.
 - Click "Update" button.

Note: There is sample UMA Authorization Policy in CE. You can modify it instead of adding new one.

4. Add UMA scope. These are list of steps which allows to add new scope.
 - Log with administrative privileges into oxTrust.
 - Open menu “OAuth2→UMA”.
 - Select “Scopes” tab and click “Add Scope Description”.
 - Select “Internal” type.
 - Fill the form.
 - Select policy which we added in previous step.
 - Click “Add” button. Sample result entry:

            dn: inum=@!1111!D386.9FB1,ou=scopes,ou=uma,o=@!1111,o=gluu
            objectClass: oxAuthUmaScopeDescription
            objectClass: top
            displayName: Access SCIM
            inum: @!1111!D386.9FB1
            owner: inum=@!1111!0000!D9D9,ou=people,o=@!1111,o=gluu
            oxPolicyScriptDn: inum=@!1111!CA0D.1918!2DAF.F995,ou=scripts,o=@!1111,o=gluu
            oxId: access_scim
            oxRevision: 1
            oxType: internal

5. Register UMA resource set. It's possible to do that via Rest API or via oxTrust GUI. Sample code: [https://github.com/GluuFederation/oxAuth/blob/master/Client/src/test/java/org/xdi/oxauth/ws/rs/uma/RegisterResourceSetFlowHttpTest.java) These are list of steps which allows to add new resource set.
 - Log with administrative privileges into oxTrust.
 - Open menu “OAuth2→UMA”.
 - Select “Resources” tab and click “Add Resource Set”.
 - Fill the form.
 - Add UMA Scope which we created in previous steps.
 - Add Client which we created in second step.
 - Click “Add” button. Sample result entry:

                dn: inum=@!1111!C264.D316,ou=resource_sets,ou=uma,o=@!1111,o=gluu
                objectClass: oxAuthUmaResourceSet
                objectClass: top
                displayName: SCIM Resource Set
                inum: @!1111!C264.D316
                owner: inum=@!1111!0000!D9D9,ou=people,o=@!1111,o=gluu
                oxAuthUmaScope: inum=@!1111!D386.9FB1,ou=scopes,ou=uma,o=@!1111,o=gluu
                oxFaviconImage: http://example.org/scim_resource_set.jpg
                oxId: 1403179695657
                oxRevision: 1

### oxTrust configuration (Resource Server)

Add next oxTrust UMA related configuration properties to oxTrust.properties:

    # UMA SCIM protection
    uma.issuer=https://centos65.gluu.info
    uma.client_id=@!1111!0008!F781.80AF
    uma.client_password=<encrypted_password>
    uma.resource_id=1403179695657
    uma.scope=https://centos65.gluu.info/oxauth/seam/resource/restv1/uma/scopes/access_scim

Values of these properties correspond to entries from first section.

Note: In order to recreate oxTrust configuration in LDAP you should
remove oxTrust configuration entry from LDAP and restart tomcat. Example
DN of oxTrust configuration entry:
ou=oxtrust,ou=configuration,inum=@!1111!0002!4907,ou=appliances,o=gluu

### SCIM Client (Requesting Party) sample code

This is sample SCIM Client code which request user information from server.

    package gluu.scim.client.dev.local;
    
    import gluu.scim.client.ScimClient;
    import gluu.scim.client.ScimResponse;

    import javax.ws.rs.core.MediaType;
    
    public class TestScimClient {
	    public static void main(String[] args) {
		    final ScimClient scimClient = ScimClient.umaInstance("https://centos65.gluu.info/identity/seam/resource/restv1", "https://centos65.gluu.info/.well-known/uma-configuration",
				    "@!1111!0008!FDC0.0FF5", "secret");

		    try {
			    ScimResponse response1 = scimClient.retrievePerson("@!1111!0008!FDC0.0FF5", MediaType.APPLICATION_JSON);
			    System.out.println(response1.getResponseBodyString());
		    } catch (Exception ex) {
			    ex.printStackTrace();
		    }
	    }
    
    }

Values from these example correspond to entries from first section.

-->
