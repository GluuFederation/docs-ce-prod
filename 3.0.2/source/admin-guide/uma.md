# UMA
## Overview
As a profile of OAuth 2.0 that is complementary to OpenID Connect, UMA defines RESTful, JSON-based, standardized flows and constructs for coordinating the protection of any API or web resource in a way that will be familiar to any developer already acquainted with OAuth.

UMA defines interfaces between authorization servers (AS) and resource servers (RS) that, by default, enable centralized policy decision-making for improved service delivery, auditing, policy administration, and accountability, even in a very loosely coupled "public API" environment. Custom profiles enable flexibility to move the decision-making line outward to distributed applications, to account for local preferences in API ecosystems. 

!!! Note
    The Gluu Server functions as an UMA AS and provides an interface for scripting unique policies for access management. To secure your application with UMA RS code, we **strongly recommend** using Gluu’s client software, [oxd](http://oxd.gluu.org).

### Authorization Policy Expression Language
UMA does not standardize a policy expression language, enabling flexibility in policy expression and evaluation through XACML, other declarative policy languages, or procedural code as warranted by conditions. It also has a fluid way to handle federated authorization policy.

### Authentication-Agnostic
UMA inherits authentication agnosticism from OAuth. It concentrates on authorization, not on authentication. 
It has been profiled to work with OpenID Connect to gather identity claims from whoever is attempting access, 
and enables true claims-based authorization (with simple group- or role-based policies a natural subset). 
For more on UMA-API in Gluu, see [UMA-API](../api-guide/uma-api.md). 
For more about [UMA](https://docs.kantarainitiative.org/uma/rec-uma-core.html)

## Resource Registration
The resources protected by UMA must be registered in oxTrust. The following propterties describe a resource:

- name
- scopes
- type
- icon\_uri

The resource type can be a string, URI or any other supported value type supported by Gluu Server CE. The properties shown above are not concrete, and it is possible that a resource may contain custom properties. An example of the resource JSON is given beow:

```
{
"name":"scim_access",
"icon_uri":"https:\/\/centos.gluu.info\/identity\/uma\/scope\/file\/scim_access"
}
```

!!! Note
    Resource JSON may contain custom properties.

![uma-resources](../img/uma/uma-resources.png)

The search bar can be used to search for any existing resource within Gluu Server. New resoruces can be added by clicking on the `Add Resource Set` button. The following screenshot shows the page that will appear up on clicking the add resource button.

![add-resource-set](../img/uma/add-resource-set.png)

The properties of a resource is visible in this page. There are two additional buttons that allows the administrator to add specific resource or scope as well. By default, Gluu Server is shipped with SCIM resources protected by UMA.

![add-resource](../img/uma/add-resource.png)

![add-scope](../img/uma/add-scope.png)

## Scopes
The scopes in UMA are bount to resource sets and used by policies to check whether the specified user has access to the resource. The scopes are described in JSON and has the following properties:

- name
- icon\_uri

An example  of the scope JSON is given below:

```
{
  "name": "Add photo",
  "icon_uri": "http://www.gluu.org/icons/add_photo_scope.png"
}
```

!!! Note
    Scope JSON may contain custom properties.

There are three (3) types of scopes in UMA:

1. `internal`: the scope is hosted within oxAuth in Gluu Server CE
2. `external`: the scope is hosted in a different server
3. `external_auto`: the scope is hosted in a different server, but it is added to Gluu Server CE during the resource registration

There is no URI for an internal scope because it sits within oxAuth in the Gluu Server. The UMA URL is represented in the format

```
UMA URL=uma_scopes_endpoint+"/"+oxId;
```

The following is an example of an UMA URL:

```
https://gluu.org/uma/scopes/view
```

!!! Note
    The scope endpoint has to be present in UMA configuration to make it discoverable.

The `ldif` for both external and internal scope is given below:

**External sample ldif**
```
dn: inum=@!1111!8990!BF80,ou=scopes,ou=uma,o=@!1111,o=gluu
displayName: View
inum: @!1111!8990!BF80
objectClass: oxAuthUmaScopeDescription
objectClass: top
oxType: external
oxUrl: http://photoz.example.com/dev/scopes/view
```

**Internal sample ldif**
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

### Add Scope
This section defines the process of defining UMA scopes from oxTrust. The scopes are accessed from the `Scopes` page under `UMA` from the oxTrust menu.

![uma-scopes](../img/uma/uma-scopes.png)

The search bar can be used to look for available scopes. New scopes are added by clicking on the `Add Scope Description` button which will bring up the interface shown below.

![uma-scopes](../img/uma/scopes-add.png)

Additionally there is an option to add authorization policy with the new scope.

## UMA Policies
UMA policies protect UMA Resources via scopes. Gluu Server evaluates all policies, identified by scopes, to grant access to resources. There are three (3) main properties of a policy:

1. scopes: policy protects resources by scopes
2. authorization script: script that is evaluated in order to grant/deny access
3. name: a human readable name to the UMA policy

The following section outlines how to define UMA policies from the Custom Script menu. The Custom Script page is accessed by navigating to `Configuration` > `Custom Scripts`.

![auth-policy](../img/uma/auth-policy.png)

### UMA Policy Algorithm
The UMA Policy alrorithm has two rules that are followed. These rules must be followed while writing UMA policy using the custom script feature of Gluu Server.

- UMA Policy protects resources based on scopes. If a scope is protected by a policy, then the policy script must reutrn `true` in order to authorize access during RPT authorization.

- Multiple policies can protect a single scope. In such a case, all the policies must retun `true` to authorize access else aceess will be denied.

![policy-algorithm](../img/uma/policy-algorithm.jpg) 
