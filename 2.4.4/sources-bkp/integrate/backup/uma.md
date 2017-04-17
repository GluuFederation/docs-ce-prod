#Enterprise UMA
The Gluu Server implements UMA in a way that enables the protection
of any web resource. Through the oxTrust interface, the server admin can
write custom [authorization interception
scripts](../customize/script.md#authorization)
which may contain logic to grant (or forbid) access. All terminology
used by this page is borrowed from UMA and Connect specs.

# UMA in Action
The diagrams below detail how the various UMA actors interact.

Some helpful definitions:
- *Resource Owner (RO)*: An OAuth resource owner that is the "user" in
  User-Managed Access. This is typically an end-user (a natural person)
  but it can also be a corporation or other legal person.   
- *Resource Server (RS)*: Where the resources are held.    
- *Authorization Server (AS)*: A server that governs access based on resource owner policies.     
- *Requesting Party (RP)*: An end-user, or a corporation or other legal
  person, that uses a client to seek access to a protected resource. The
  requesting party may or may not be the same party as the resource owner.    
- *Client*: A web or native app that is used to access a digital
  resource.     
- *Protection API Token (PAT)*: An entity seeking protection API access
  MUST have the scope "uma_protection". An access token with at least
  this scope is called a protection API token (PAT) and an entity that
  can acquire an access token with this scope is by definition a resource
  server.     
- *Requesting Party Token (RPT)*: the token that a client presents to a
  resource server when trying to access a protected resource.     
- *Authorization API Token (AAT)*: An entity seeking authorization API
  access MUST have the scope "uma_authorization". An access token with
  at least this scope is called an authorization API token (AAT) and an
  entity that can acquire an access token with this scope is by 
  definition a client.      

## UMA Authorization Workflow
![UMA Authorization Workflow](../img/uma/uma_parts.png "UMA Parts")

## Detailed Authorization Overview
![Detailed authorization overview](../img/uma/uma_flow.png "UMA Parts")

## UMA Authorization Token Workflow
![UMA Authorization token workflow](../img/uma/uma_token_workflow.png "UMA Parts")

## UMA Authorization Complete Sequence
![UMA Authorization complete sequence diagram](../img/uma/uma_very_detailed_flow.png "UMA Parts")

## Discovery

The Gluu Server exposes an endpoint for discovering information about
UMA Provider configuration. A resource server or client can perform an
HTTP GET on `https://domain.com/.well-known/uma-configuration` to
retrieve a JSON object indicating the UMA Provider configuration.

Gluu Server response for UMA configuration MAY contain standard
properties (defined by UMA specification) as well as custom properties
(extension that is out of scope of this document). Gluu Server
guarantees property name uniqueness within response.

The following is an example of a GET request to the UMA configuration
discovery endpoint:

``` json
{
  "version": "1.0",
  "issuer": "https://gluuserver.org",
  "pat_profiles_supported": [
    "bearer"
  ],
  "aat_profiles_supported": [
    "bearer"
  ],
  "rpt_profiles_supported": [
    "bearer"
  ],
  "pat_grant_types_supported": [
    "authorization_code"
  ],
  "aat_grant_types_supported": [
    "authorization_code"
  ],
  "claim_profiles_supported": [
    "openid"
  ],
  "dynamic_client_endpoint": "https://gluuserver.org/oxauth/seam/resource/restv1/oxauth/register",
  "token_endpoint": "https://gluuserver.org/oxauth/seam/resource/restv1/oxauth/token",
  "user_endpoint": "https://gluuserver.org/oxauth/seam/resource/restv1/oxauth/authorize",
  "introspection_endpoint": "https://gluuserver.org/oxauth/seam/resource/restv1/host/status",
  "resource_set_registration_endpoint": "https://gluuserver.org/oxauth/seam/resource/restv1/host/rsrc",
  "permission_registration_endpoint": "https://gluuserver.org/oxauth/seam/resource/restv1/host/rsrc_pr",
  "rpt_endpoint": "https://gluuserver.org/oxauth/seam/resource/restv1/requester/rpt",
  "authorization_request_endpoint": "https://gluuserver.org/oxauth/seam/resource/restv1/requester/perm",
  "scope_endpoint": "https://gluuserver.org/oxauth/seam/resource/restv1/uma/scopes"
}
```

The JSON object returned includes the following configuration
information:

`version`: the supported UMA core protocol version.

`issuer`: the uri of the issuing authorization server.

`pat_profiles_supported`: the supported OAuth token types used for
issuing Protection API Tokens (PATs).

`aat_profiles_supported`: the supported OAuth token types used for
issuing Authorization API Tokens (AATs).

`rpt_profiles_supported`: the supported Requesting Party Token (RPT)
profiles.

`pat_grant_types_supported`: the supported OAuth grant types used for
issuing PATs.

`aat_grant_types_supported`: the supported OAuth grant types used for
issuing AATs.

`token_endpoint`: the uri to request a PAT or AAT.

`authorization_endpoint`: the uri to request authorization for issuing a
PAT or AAT.

`introspection_endpoint`: the uri to introspect an RPT.

`resource_set_registration_endpoint`: the uri for a resource server to
register a resource set.

`permission_registration_endpoint`: the uri for a resource server to
register a requested permission.

`rpt_endpoint`: the uri for the client to request authorization data.

`dynamic_client_endpoint`: the uri for registering a dynamic client.

## Resource Registration

To let the Gluu Server know which resources are protected by UMA they
must be registered. Resources are described by the following properties:

- name: name of resource
- scopes: scopes that are available for this resource
- type: type of resource (it can be string, uri or what ever, basically
  it is up to Resource Server what type it should be).
- icon_uri: uri to the icon.

These are standard properties however a resource description MAY contain
custom properties.

## Register resource via oxTrust

![oxTrust UMA Resources Interface](../img/uma/uma_oxtrust_resources.png)

![oxTrust UMA Add Resources Interface](../img/uma/uma_oxtrust_resources_add.png)

## UMA Scopes

UMA Scopes are bound to resource sets and are used by policies to check
whether the specified user has access to the resource. An UMA Scope is
described in JSON and has the following properties:

- name: name of scope (e.g. View photo, Edit photo)
- icon_uri: optional property to specify an icon for the photo

An example of a typical JSON document of scope can be seen here:

```
{
  "name": "Add photo",
  "icon_uri": "http://www.gluu.org/icons/add_photo_scope.png"
}
```

The scope JSON MAY contain custom properties which are out of scope of
this document.

## Define UMA Scopes via oxTrust

![oxTrust Scopes](../img/uma/uma_oxtrust_scopes.png)

![Add oxTrust Scopes](../img/uma/uma_oxtrust_scopes_add.png)

## Implementation specificity

The following types of scopes exist:

- internal: hosted on oxAuth (must provide a scope description).
- external: hosted on other servers.
- external_auto: a scope hosted on another server but which is
  automatically added during resource set registration or update.

**Note:** there is no uri for an internal scope because it is
configurable and depends on oxAuth hosting.

UMA url = uma_scopes_endpoint + "/" + oxId;

http://gluu.org/uma/scopes/view = http://gluu.org/uma/scopes + "/" + view

A server has to provide a scope description as JSON document. The
following uri is in use: http://gluu.org/uma/scopes/view

**Note:** The scope endpoint has to be present in UMA configuration to
make it discoverable.

#### External sample ldif

```
dn: inum=@!1111!8990!BF80,ou=scopes,ou=uma,o=@!1111,o=gluu
displayName: View
inum: @!1111!8990!BF80
objectClass: oxAuthUmaScopeDescription
objectClass: top
oxType: external
oxUrl: http://photoz.example.com/dev/scopes/view
```

#### Internal sample ldif

```
dn: inum=@!1111!8990!BF80,ou=scopes,ou=uma,o=@!1111,o=gluu
displayName: View
inum: @!1111!8990!BF80
objectClass: oxAuthUmaScopeDescription
objectClass: top
oxType: internal
oxId: View
oxIconUrl: http://seed.gluu.org/uma/icons/view_scope.png
```

# UMA Policies

UMA Policies protect UMA Resources. The protection of resources are made
via scopes. Gluu Server evaluates all policies (identified by scopes) in
order to grant access.

The UMA Policy main properties are:

- scopes: policy protects resources by scopes.
- authorization script: script that is evaluated in order to grant or
  deny access (script basically returns true or false to the server).
- name: it is best to provide an easily understandable name to the
  policy so that it is clear what the policy protects.

## Define Policies

Within the oxTrust interface the Gluu Server admin can define UMA
policies (pictured below). To achieve this, navigate to Configuration >
Manage Custom Scripts > UMA Authorization policies.

You can find more information on crafting UMA policies as well as an
example script
[here](../customize/script.md).

![Add UMA Policies](../img/uma/uma_oxtrust_policy_add.png)

## Algorithm

The algorithm follows theses rules:

- Policy protects resources based on scopes. If a scope is protected by
  a policy then during RPT authorization such a policy script has to
  return true in order to authorize access to resource, otherwise
  authorization is denied.
- Scope can be protected by multiple policies. If one scope is protected
  by multiple policies then all policies have to return true to
  authorize access. If at least one policy returned false then the
  authorization is denied.

![UMA Policy Handling](../img/interception_scripts/uma_policy_handling.jpg) 

## Requesting party trust elevation

This section defines the OX claim profile for UMA. Following is a
summary:

  - Identifying uri: http://gluu.org/uma/profiles/uma-claim-gluu-1.0
  - Profile author and contact information: Michael Schwartz and Yuriy Zabrovarnyy (info@gluu.org)
  - Updates or obsoletes: None; this profile is new.
  - Syntax and semantics of claim data: As defined below.
  - Claims gathering method: As defined below.
  - Error states: "need_reauthentication" in case AAT is not "strong" enough.
  - Security and privacy considerations: None additional.
  - Binding obligations: None additional.

If an authorization server supports the OX claim profile, it MUST supply
the "ox" value for one of its "claim_profiles_supported" values in its
configuration data.

To conform to this option, the authorization server MUST do the following:

  - send "need_reauthentication" error in case AAT does not correspond
    to authentication level and (or) mode of authorization policy.
    Together with error authorization server MUST provide:
      - domain_auth_level - REQUIRED. authentication level required to
        satisfy authorization policy.
      - domain_auth_mode - REQUIRED. authentication mode required to
        satisfy authorization policy.
      - authentication_uri - OPTIONAL. authorization server
        authentication uri for re-authentication with required
        authentication level and mode

For example:

```
HTTP/1.1 403 Forbidden
Content-Type: application/json
Cache-Control: no-store
{
  "status": "error",
  "error": "need_reauthentication",
  "domain_auth_level":20,
  "domain_auth_mode":"duo",
  "required_acr_level":2,
  "required_acr_uri":"http://example.com/global_acr",
  "authentication_uri":"http://seed.gluu.org/oxauth?auth_level=20&auth_mode=duo&client_id=..."
}
```

## UMA Resource Server Java Library

[UMA RS Java Library](https://github.com/GluuFederation/uma-rs) helps to easily protect Java based project with UMA in declarative way.

Sample declaration
```json
{"resources":[
    {
        "path":"/photo",
        "conditions":[
            {
                "httpMethods":["GET"],
                "scopes":[
                    "http://photoz.example.com/dev/actions/view"
                ]
            },
            {
                "httpMethods":["PUT", "POST"],
                "scopes":[
                    "http://photoz.example.com/dev/actions/all",
                    "http://photoz.example.com/dev/actions/add"
                ],
                "ticketScopes":[
                    "http://photoz.example.com/dev/actions/add"
                ]
            }
        ]
    },
    {
        "path":"/document",
        "conditions":[
            {
                "httpMethods":["GET"],
                "scopes":[
                    "http://photoz.example.com/dev/actions/view"
                ]
            }
        ]
    }
]
}
```

`ticketScopes` are used for UMA ticket registration. If it is skipped then ALL scopes are registered for ticket.

### Usage

```java
Configuration configuration = ConfigurationLoader.loadFromJson(inputStream(CONFIGURATION_FILE_NAME));
Collection<RsResource> values = RsProtector.instance(inputStream(PROTECTION_CONFIGURATION_FILE_NAME)).getResourceMap().values();

ServiceProvider serviceProvider = new ServiceProvider(configuration);
PatProvider patProvider = new PatProvider(serviceProvider);
ResourceRegistrar resourceRegistrar = new ResourceRegistrar(patProvider);

resourceRegistrar.register(values);
```

#### References
- [UMA 1.0.1 Specification](https://docs.kantarainitiative.org/uma/rec-uma-core.html)
- [Kantara Enterprise UMA Case Study](http://kantarainitiative.org/confluence/display/uma/Case+Study%3A+Access+Management+2.0+for+the+Enterprise) 
- [UMA Specifications](https://kantarainitiative.org/confluence/display/uma/UMA+Protocol)
- [UMA Requesting Party Sample implementation](https://github.com/GluuFederation/oxUmaDemo/tree/master/RP)
- [UMA Resource Server Sample implementation](https://github.com/GluuFederation/oxUmaDemo/tree/master/RS)
- [UMA Demo Video](http://www.gluu.co/uma-demo-video)
- [UMA Demo Local Configuration (How to)](https://gluu.org/docs/how-to/uma-demo/)
- [UMA Requesting Party Sample Live](https://kantara.gluu.org/rp/rp.html)
- [UMA Resource Server Sample Live](https://kantara.gluu.org/rs/rs.html)
- [Gluu Server](http://gluu.org)
