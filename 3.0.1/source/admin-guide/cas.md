# CAS
## Overview
The Central Authentication Service (CAS) is a single sign-on protocol for the web. Its purpose is to permit a user to access multiple applications while providing their credentials (such as userid and password) only once while allowing applications to authenticate users without gaining access to those credentials, such as a password. The name CAS also refers to a software package that implements this protocol, which recently become a part of Shibboleth IdP v3 package. As Gluu CE includes Shibboleth to support for SAML protocol flows, it incorporates all CAS-related functionality that comes with it. The most recent version of CAS protocol is 3. Shibboleth support most of the [CAS protocol v2 specification](https://apereo.github.io/cas/5.0.x/protocol/CAS-Protocol-V2-Specification.html), including attribute release and CAS proxy support.

Nowdays CAS is hardly the most advanced and agile SSO protocol. Unless you've got a legacy software or pre-existing infrastracture
in your network which revolves around it, chances are high there are much better solutions at hand.

Refer to these five considerations to determine which protocol 
to use for single sign-on (SSO):

- If you have an application that already supports SAML, use SAML.
- If you need to support user login at an external IDP (like a customer or partner IDP), use SAML.
- If you have a mobile application, use OpenID Connect.
- If you are writing a new application, use OpenID Connect.
- If you have some legacy applications which only support CAS for SSO, use CAS

If you are continuing with the CAS documentation it is presumed your use case aligns with the last bullet above.
If it doesn't and your app provides other options for SSO (like, SAML) - may be it's time for a switch? You may want to
see [SAML](./saml.md) and [OpenID Connect](./openid-connect.md) portions of the Gluu Server docs in this case. 

### Outbound vs. Inbound CAS 
Gluu provides two main scenarios involving CAS flows. By analogy with SAML scenarios let's call them "outbound CAS" and "inbound CAS".

Outbound CAS is a traditional way to employ the protocol. Website or application (or, more likely, CAS client acting on behalf of them)
redirects a user to a designated CAS server for authentication and authorization. CAS server authenticates the user, checks whether such application is
allowed to use the service, then redirects user's browser back to the application/CAS client with a `service ticket`. The ticket is then validated by them by
calling respective validate endpoint at CAS server via back-channel connection. Depending on protocol version and extenstion used, some attributes may
also be sent in response to validation call.

In contrary, inbound CAS is a way for Gluu server itself to delegate authentication to some remote CAS server in your organization's network. By doing so it allows you to leverage your existing infrastracture and broadens your authentication options. From a technical standpoint it's just another [custom authentication script](../authn-guide/customauthn/) which is already pre-packaged in your instance. You can find out more about how to configure it on [corresponding Github page](https://github.com/GluuFederation/oxAuth/tree/master/Server/integrations/cas2).

## Outbound CAS
In Gluu CE 3.0 outbound CAS configuration is split into two different parts. First CAS support must be enabled in web UI.
Then applications which should be allowed to use this CAS server must be added to service registry - this part is done from linux console (inside the container)

### Enabling CAS

!!! Note
    CAS is very demanding in terms of clocks' syncronization between CAS server and CAS client
    Make sure ntp is configured and running on both hosts, and their times are as close as possible before proceeding!

Please follow next steps to enable the feature:

1. Log in to oxTrust administrator web UI
2. Proceed to "Configuration -> Manage authentication -> CAS Protocol"
3. Leave all settings on the page at defaults, set "Enabled" checkbox and click the "Update" button
4. Click the "Update configuration files" button

![tr-relying-party](../img/cas/cas_enabling.jpg)  

### Configuring service registry

Let's start by configuring a very basic CAS setup which only returns user's id to requesting application (will use it as a foundation to build a more functional setup(s) upon later on)

1. Move into the Gluu CE container: `# service gluu-server-3.0.1 login`
2. Edit `/opt/gluu/jetty/identity/conf/shibboleth3/idp/cas-protocol.xml.vm` template file by putting a "ServiceDefinition" bean reloadableServiceRegistry inside pre-existing "reloadableServiceRegistry" bean fxas examplified below. You must use a regexp defining your application instead of `https:\/\/([A-Za-z0-9_-]+\.)*example\.org(:\d+)?\/.*`
3. Restart the idp service to apply your changes: `# service idp restart`

```
    <bean id="reloadableServiceRegistry"
          class="%{idp.cas.serviceRegistryClass:net.shibboleth.idp.cas.service.PatternServiceRegistry}">
        <property name="definitions">
            <list>
                <!--
                <bean class="net.shibboleth.idp.cas.service.ServiceDefinition"
                      c:regex="https://([A-Za-z0-9_-]+\.)*example\.org(:\d+)?/.*"
                      p:group="proxying-services"
                      p:authorizedToProxy="true"
                      p:singleLogoutParticipant="true" />
                <bean class="net.shibboleth.idp.cas.service.ServiceDefinition"
                      c:regex="http://([A-Za-z0-9_-]+\.)*example\.org(:\d+)?/.*"
                      p:group="non-proxying-services"
                      p:authorizedToProxy="false" /
                -->

                <bean class="net.shibboleth.idp.cas.service.ServiceDefinition"
                      c:regex="https:\/\/([A-Za-z0-9_-]+\.)*example\.org(:\d+)?\/.*"
                      p:group="institutional-services"
                      p:authorizedToProxy="false" />

            </list>
        </property>
    </bean>
```

At this point you should start getting a valid CAS response from `https://your.gluu.host/idp/profile/cas/serviceValidate` containing at least user id.
CAS as part of Shibboleth IdP is logging to `/opt/shibboleth-idp/logs/idp-process.log`. You can control verbosity of the IdP's logs by editing logging levels in `/opt/shibboleth-idp/conf/logback.xml`
