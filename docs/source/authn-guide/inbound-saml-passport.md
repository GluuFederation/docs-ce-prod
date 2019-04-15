# Inbound SAML using Passport

## Requisites

The [introductory page](??) provides a quick glance at key concepts to get the most out of inbound identity with Gluu Passport. Ensure your installation already has [Passport component installed](???#passport-setup). Now proceed to enable it:

1. Custom script:

    - In oxTrust navigate to `Configuration` > `Custom scripts`          
    - Navigate to the `Person Authentication` tab, expand the script labelled `passport_saml`, check `enabled`, and click `Update`    ![Enable passport_saml](../img/user-authn/passport/enable-passport.png)     
    - Navigate to the `UMA RPT Policies` tab, expand the script labelled `scim_access_policy`, check `enabled`, and click `Update`       
      
1. Passport support:    

    - In oxTrust navigate to `Configuration` > `Organization configuration` > `System configuration`
    - In `Passport support` choose `Enabled`    
    - Click `Update`    

    ![enable passport](../img/user-authn/passport/enable_passport.png) 


## Integrating IDPs for inbound SAML

The following are the steps required to integrate an external IDP for inbound SAML

1. Add the IDP in the admin UI
1. Register Passport metadata with external IDP
1. Configure attributes mappings
1. Make use of `passport_saml` authentication

### Add the IDP in the admin UI

1. In oxTrust navigate to `Configuration` > `Passport` > `Providers`

1. Click on `Add new provider`

1. Enter a display name for the IDP

1. In `type` choose "saml"

1. Supply a `logo path` for this provider. Check this [section](??#about-logo-images) of the introductory page to learn more.

1. Check `Is enabled` (unless there is a reason to leave this provider integration temporarily disabled)

1. Checking `Request For Email` or `Email linking` is not required unless you want to exercise a [custom flow](??#altering-flow-behaviour).

As mentioned earlier in the [introduction to inbound identity](??#supported-providers), Passport reuses [Passport.js](http://www.passportjs.org/) strategies to facilitate integrating a variety of identity provider "flavors". In the case of IDPs, the [passport-saml](https://github.com/bergie/passport-saml/) strategy is used. This strategy supports a high level of customization via [configuration parameters](https://github.com/bergie/passport-saml/#config-parameter-details) which you an specify in the "Provider options" panel.

By default only a small set of parameters for a working setup are shown in the options panel, namely:

- entryPoint: URL to which SAML requests can be sent to
- identifierFormat: Identifier format to request from IDP
- authnRequestBinding: SAML binding to user for requesting authentication, only `HTTP-POST` or `HTTP-Redirect` are supported. If not provided, default is `HTTP-Redirect`
- issuer: `entityID` of Passport as SP (eg. `urn:test:example`). You can use different values or the same across different IDPs
- cert: IDPs public PEM-encoded X.509 certificate used to validate incoming SAML responses. Include only the body of the certificate: supress the `BEGIN CERTIFICATE` and `END CERTIFICATE` lines, whitespaces, and all line breaking characters (new line/carriage return).

!!! Note: 
    The certificate supplied for `cert` is the one intended for signing. For example, if you are using Shibboleth bundled in a Gluu Server instance, visit `https://<gluu-host>/idp/shibboleth` and see the contents of XML tag `KeyDescriptor` where `use="signing"` inside `IDPSSODescriptor` tag.

#### Supply extra properties if needed

Add other properties you migh consider relevant. For details on this topic you can check `passport-saml` repo [documentation](https://github.com/bergie/passport-saml/#config-parameter-details). If not specified, the following properties are added by default:

|Property|Value|
|-|-|
|validateInResponseTo|true|
|requestIdExpirationPeriodMs|3600000|
|decryptionPvk|/etc/certs/passport-sp.key|
|decryptionCert|/etc/certs/passport-sp.crt|

To be more precise `decryptionPvk` and `decryptionCert` are filled with values `SP TLS cert` and `SP TLS key` found in the basic configuration: In oxTrust visit `Passport` > `Basic Configuration`.

#### Cache Provider configuration

When `validateInResponseTo` is set to `true`, a simple in-memory cache is used to store the IDs of the SAML requests emitted by Passport. Then the `InResponseTo` of SAML responses are validated against the cache. Check [here](https://github.com/bergie/passport-saml/#cache-provider) to learn more. This cache can lead to validation errors when your Gluu Passport environment consists of more than one server (eg. a clustered setup).

To account for this scenario, we provide a safe cache for validation based on Redis. In most cases, a clustered Gluu installation already leverages a redis cache for functioning, so we can reuse it here. To use such cache, add a property with name `redisCacheOptions` and for its value pass a dictionary with keys as seen [here](https://github.com/NodeRedis/node_redis#options-object-properties).

The following is an example for `redisCacheOptions` value:

```
{ host: 'server.co', port: 6379, password: 'secret' }
```

**Note**:
Navigate in oxTrust to `Configuration` > `JSON configuration` > `Cache provider configuration`. If `cacheProviderType` equals to REDIS, you are safe to go and can reuse some of the parameters found under `redisConfiguration` section for `redisCacheOptions`. If your clustered setup is using a different cache provider please check the corresponding Cluster Manager [docs](https://gluu.org/docs/cm/3.1.4/deploy/#cache)  or open a support ticket.


### Register Passport metadata with external IDP

Passport will automatically generate SP metadata for every enabled IDP added through the admin UI. The next step is to register metadata at every external IDP.

Metadata can be accessed in a browser at `https://<hostname>/passport/auth/meta/idp/<PROVIDER-ID>` where `PROVIDER-ID` is the identifier assigned to the IDP added. In oxTrust just visit `Passport` > `Providers` and see ID column in the providers table. Metadata can also be found in the Gluu chroot filesystem under `/opt/gluu/node/passport/server/idp-metadata`. 

Register metadata contents in your remote external IDPs. The actual process for this differs across IDP implementations. As an example, when the remote IDP is another Gluu Server, a [trust relationship](https://gluu.org/docs/ce/admin-guide/saml/#create-a-trust-relationship) should be created. Review the corresponding documentation for your IDPs. 

Ensure to apply the required configurations at the IDP so the attributes of your interest are released to the SP.

### Configure attributes mapping

A mapping is a mechanism that defines how the profile data released by the IDP is saved to local Gluu LDAP. See [attribute mapping](??#attribute-mapping-and-transformation). By default, IDPs use the `saml_ldap_profile` mapping which is inspired on the [X.500/LDAP Attribute Profile](http://www.oasis-open.org/committees/download.php/28042/sstc-saml-attribute-x500-cs-01.pdf).

To learn more about how mappings work check the [tutorial](??). Also review the file `/opt/gluu/node/passport/server/mappings/saml_ldap_profile.js` in Gluu chroot. If the mapping does not suit your needs or requires adjustments, do not edit the default mapping file but create a new one based on its contents. You may also check the `saml_basic_profile` which is inspired on the SAML Basic Attribute Profile.

Provide the filename (excluding extension) of the mapping to use in the details form of the external provider (field `mapping`).

### Make use of `passport_saml` authentication

If you plan to offer inbound SAML from an OpenID Connect application, you can use the same steps described for [Social Login](#Protect the application with `passport_social` authentication) except the acr value to use has to be `passport_saml`.

If your application is a SP (SAML provider), ....

## IDP-initiated inbound flow

### Overview

The standard inbound SAML flow resembles the [generic flow](??#sample-authentication-flow) of inbound identity. In certain circumstances, the IDP may attempt to initiate the flow by delivering a SAML response without any previously existing SAML request. This is called "IPD-initiated inbound" flow.

The approach in Gluu to handle this scenario consists of detecting if SAML responses are unsolicited (ie not associated to preliminar SAML requests) by examining the SAML `inResponseTo` attribute. If `inResponseTo` is missing, it is considered an action initiated by the IDP.

When this kind of request is received by Passport SP, the usual profile mapping takes place, and then the profile data is sent (encoded) in the parameters of an OpenID Connect authorization request to oxAuth. The request is processed by oxAuth and the user provisioning occurs locally as it does in the standard flow.

In the context of OpenID Connect, this will generate a redirection to a URL whose handler logic should be able to take the user to its final destination. This logic can be seen as part of an OpenID Connect Requesting party (the analog of a SP in SAML world).

The following diagram depicts the flow:

??flow diag

### About the Assertion Consumer Service URL

Unsolicited SAML responses can be posted to:

```
https://<your-gluu-host>/passport/auth/saml/<PROVIDER-ID>/callback
```

where `PROVIDER-ID` is the identifier assigned to the given IDP. In oxTrust just visit `Passport` > `Providers` and see ID column in the providers table. 

This is the same endpoint used in the regular flow where SAML requests do exist

### Configuring the flow

To facilitate the process describe above, Gluu includes by default the following to minimize the amount of configurations and coding required:

- A pre-exising OpenID client to be used for issuing the authorization request. 
- UI forms in oxTrust to easily configure the parameters of the authorization to generate per IDP registered in Passport
- A sample redirector page which sends the user's browser to a URL (supposed to be previously passed as `relayState` in the initial SAML response).

In order to enable IDP-initiated inbound capabilities for an existing IDP, proceed as below:

- Navigate to `Passport` > `IDP-initiated flows config`
- Click the `Add` button
- Choose the IDP you want to enable to use the IDP-initiated flow
- Accept the defaults and click on `Update`

From here on, if the IDP sends an unsolicited response to Passport ACS, an OIDC authorization request will be issued by using the client that appears selected on the top of the form (by default it will be the "Passport IDP-initiated flow Client"). After the user is authenticated in Gluu, a redirection will be made to `https://<your-gluu-host>/oxauth/auth/passport/sample-redirector.htm` which will simply redirect to the value of the `relayState` which is assummed to be a valid URL.

### Customization

The IDP-initiated flows configuration page in oxTrust provides default values for a working setup with minimal effort. If you require to tweak the behavior you have to build your own redirect page. There you can handle `relayState` your way and potentially show options in case `relayState` is absent. You can learn how to retrieve this value checking the source code of the `sample-redirector.htm`. Follow these steps:

- Login to chroot
- Run `jar -xf /opt/gluu/jetty/oxauth/webapps/oxauth.war auth/passport/sample-redirector.xhtml`
- Provide the new redirect URI in oxTrust (`Passport` > `IDP-initiated flows config`)

!!! Note:
    The page will receive in the request the typical parameters of an OIDC authorization flow. Do not transfer those parameters to other requests/redirects your handler logic may perform.

## Implementing IDP discovery ("WAYF")

IDP Discovery refers to process of determining which IDP users should be sent to for authentication (also known as: "Where Are You From", or WAYF). There are many ways to achieve this, but the following methods are most commonly used in practice.

### Discovery based on supplied email address

Email-based discovery, or "identifier-first" login, relies on an email address to discover where to send an user for authentication. It can be implemented as follows:

1. Users are asked for an email address which they usually use for logging in their home IDP.

1. The domain name part of the email address is parsed and evaluated; the domain name part is a sub-string of the email address following the "@" character.

1. Check if such IDP is allowed to be used with this application. The list of allowed IDPs will usually be derived from IDP entries in `passport-saml-config.json` file of target Gluu Server.

1. If found, an OpenID Connect authorization request URL can be buit by supplying the IDP id in a custom parameter (as described [here](./passport.md#preselecting-an-external-provider)).

1. The user is redirected to the URL of the previous step, triggering the Passport Inbound SAML scenario.

1. The Passport SAML authentication script parses the custom parameter, and the flow proceeds to the designated IDP.

### Landing page discovery

If you do not mind exposing the list of your external IDP partners, you can allow users to choose which IDP better suits their needs by displaying all IDPs you've established trust with. This is the standard behavior in Gluu Server with Passport.

###  Discovery based on sub-domain or sub-directory

If you provide a dedicated sub-domain or sub-path namespace to your customers or partners (URLs like `https://customer1.mydomain.com` or `https://mydomain.com/customer1` illustrate this approach), then you can perform discovery based on this as well. When an unauthenticated user tries to access any protected resources related to those dedicated namespaces, an appropriate IDP related to it can be looked up in a configuration file and its id encoded into a custom parameter of the authorization request before redirecting the user to Gluu Server.

## Troubleshooting tips

In case of issues during setup or tests, consider the following:

1. Make sure that the system clocks are synchronized between all the machines that participate in the flow (NTP is the way to go). When clocks are out of sync, it's known to cause a hard to troubleshoot state of an "infinite loop" (non-ending redirection across a given set of pages).

1. Some IDPs may choose to encrypt assertions in their SAML responses in a way that the Passport module is not able to understand. In case of any issues with the flow (especially the ones following the reception of SAML response from remote IDP by the Passport module) try to disable assertions' encryption at involved IDP in order to verify whether this is the cause (the response will still normally being passed over the encrypted channel via the SSL/TLS providing strong enough security).

1. [Log files](./passport.md#log-level) can be a useful source of clues about what is going on under the hood.

1. For debugging purposes, you can print the contents of profile data you are receiving from the external provider. Follow the guidelines given [here](./passport.md#inspecting-profile-data).

If you still have trouble, feel free to open a [support ticket](https://support.gluu.org) for further assistance. Please provide all related log entries to speed up the resolution process.
