# Logout From Gluu Server
Gluu Server offers single-logout(SLO) service for OpenID Connect

## OpenID Connect SLO
Gluu Server uses OpenID Connect to end session for logout. 
Usually a logout link is provided to the connected SP and the session 
is killed inside the IdP. When using the OpenId Connect Logout, it is 
recommened to test the _front channel logout_. In the _front channel 
logout_ the browser receives a page with the list of application 
logout urls each within an iframe. This causes the browser to call each 
applicaiton logout individually and finally calling the OpenID Connect 
end-session endpoint via _javascript_. 
Please see the [OpenID Connect Frontchannel Logout Specifications](http://openid.net/specs/openid-connect-frontchannel-1_0.html) for more informaiton.

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
