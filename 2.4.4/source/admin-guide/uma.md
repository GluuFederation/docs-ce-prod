# UMA
This section describes the adminisration of UMA in Gluu Server CE. The UMA administration is accessible from the oxTrust administrator interface.

![menu](../img/uma/menu.png)

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

The following section outlines how to define UMA policies from the Custom Script menu. The Custom Script page is accessed from the Configuration Menu.

![custom-script-menu](../img/oxtrust/custom-script-menu.png)
![auth-policy](../img/uma/auth-policy.png)

### UMA Policy Algorithm
The UMA Policy alrorithm has two rules that are followed. These rules must be followed while writing UMA policy using the custom script feature of Gluu Server.

- UMA Policy protects resources based on scopes. If a scope is protected by a policy, then the policy script must reutrn `true` in order to authorize access during RPT authorization.

- Multiple policies can protect a single scope. In such a case, all the policies must retun `true` to authorize access else aceess will be denied.

![policy-algorithm](../img/uma/policy-algorithm.jpg) 
