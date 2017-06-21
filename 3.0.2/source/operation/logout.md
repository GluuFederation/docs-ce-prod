# Logout From Gluu Server
Gluu Server offers single-logout(SLO) service for OpenID Connect

## OpenID Connect SLO
Gluu Server uses OpenID Connect to end sessions for logout. 
Usually a logout link is provided to the connected SP and the session 
is killed inside the IDP. When using OpenID Connect Logout, it is 
recommeneded to test the _front channel logout_. In the _front channel 
logout_ the browser receives a page with the list of application 
logout urls each within an iframe. This causes the browser to call each 
applicaiton logout individually and finally calling the OpenID Connect 
end-session endpoint via _javascript_. 

The workflow for single logout for two applications using OpenID Connect Front-Channel Logout would be the following:

1. App-A - registers `frontchannel_logout_uri_1`
2. App-B - registers `frontchannel_logout_uri_2`
3. App-A - login to the Authorization Server (AS), in this case the Gluu Server.
4. App-B - login to AS (SSO)
5. App-A - calls `/end_session`
6. AS - returns back HTML with iframes where each iframe points to all `frontchannel_logout_uris` within this session, in our case it is `frontchannel_logout_uri_1` and `frontchannel_logout_uri_2`
7. Browser loads HTML (with all iframes, so it calls `frontchannel_logout_uri_1` and `frontchannel_logout_uri_2`)
8. App-A does not know anything about `frontchannel_logout_uri_2`, it just calls `/end_session` endpoint and it's the responsibility of the AS to track it and return the correct HTML page with iframes (once iframe is loaded, it means that `frontchannel_logout_uri_2` is called and app-B must log itself out).

Please read the [OpenID Connect Front-Channel Logout Specifications](http://openid.net/specs/openid-connect-frontchannel-1_0.html) to learn more about logout with OpenID Connect.

## SAML Logout
Although there is a SLO available for Shibboleth, 
it is not supported in Gluu Server because of its instabilities. 
Please take a look at [this page](https://wiki.shibboleth.net/confluence/display/CONCEPT/SLOIssues) for more information.

* The logout URI for SAML SP is `https://<hostname of Gluu Server>/idp/logout.jsp`<br/> Calling this URL within Gluu Server kills the session inside Gluu Server.

## Authentication Script
It is possible to use Custom Authentication Script to call individual 
logout methods for both SAML and OpenID Connect and log out of the 
desired SP/SPs when the user logs out of the Gluu Server. 
Please see the [Custom Script Guide](../authn-guide/customauthn.md) to start writing your own custom script. 
