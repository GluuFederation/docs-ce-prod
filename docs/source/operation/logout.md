# Logout from Gluu Server

## OpenID Connect Single Log Out (SLO)

The Gluu Server uses OpenID Connect to end sessions for logout. Usually a logout link is provided to the connected SP and the session 
is killed inside the IDP. 

When using OpenID Connect Logout, it is recommeneded to use Front-Channel Logout. In Front-Channel Logout the browser receives a page with a list of application logout urls within an iframe. This prompts the browser to call each application logout individually and the OpenID Connect end-session endpoint via Javascript. 

The workflow for single logout for two applications using OpenID Connect Front-Channel Logout would be the following:

1. App-A - registers `frontchannel_logout_uri_1`
2. App-B - registers `frontchannel_logout_uri_2`
3. App-A - login to the Authorization Server (AS), in this case the Gluu Server.
4. App-B - login to AS (SSO)
5. App-A - calls `/end_session`
6. AS - returns back HTML with iframes where each iframe points to all `frontchannel_logout_uris` within this session, in our case it is `frontchannel_logout_uri_1` and `frontchannel_logout_uri_2`
7. Browser loads HTML (with all iframes, so it calls `frontchannel_logout_uri_1` and `frontchannel_logout_uri_2`)
8. App-A does not know anything about `frontchannel_logout_uri_2`, it just calls `/end_session` endpoint and it's the responsibility of the AS to track it and return the correct HTML page with iframes (once iframe is loaded, it means that `frontchannel_logout_uri_2` is called and app-B must log itself out).

There are a few important points to note:
1. `post_logout_redirect_uri` is not mandatory but registration specification says `The value MUST have been previously registered with the OP`. We have dual behavior description directly in specification. `oxauth` ends session successfully (if session is present on OP) independently from whether `post_logout_redirect_uri` is valid or not. If it is not valid then server returns 200 with message `Session is ended successfully but redirect to post logout redirect uri is not performed because it fails validation`. Server returns 200 because session was ended successfully however inform that validation failed.
2. `id_token_hint` and `session_id` parameters are optional. Therefore OP will end session successfully if these parameters are missed. However from other side if RP included them in request OP validates them and if any of those are invalid OP returns 400 (Bad Request) http code.

`post_logout_redirect_uri` is validated against client which take part in SSO. If session does not exist or can not be identified then error page is shown. However it is possible to allow redirect to RP without validation:
 
1. set `allowPostLogoutRedirectWithoutValidation` to `true`
2. or add `post_logout_redirect_uri` to white list

Read the [OpenID Connect Front-Channel Logout Specifications](http://openid.net/specs/openid-connect-frontchannel-1_0.html) to learn more about logout with OpenID Connect.

## SAML Logout
The Shibboleth IDP (which is included in the Gluu Server) does not support single logout in any meaningful sense. Take a look at the [Shibboleth wiki](https://wiki.shibboleth.net/confluence/display/CONCEPT/SLOIssues) for more information.

To initiate SAML logout, the SP must call the Gluu Server's SAML logout URI, which can be found at: `https://<hostname>/idp/logout.jsp`. Calling this URL kills the session inside the Gluu Server IDP. The SP must also initiate a session-killing operation, or can implement [Force Re-Authentication](https://wiki.cac.washington.edu/display/infra/Configure+a+Service+Provider+to+Force+Re-Authentication) as well.

## Customizing Logout
It is possible to use a custom authentication script to call individual logout methods for both SAML and OpenID Connect and log out of the desired SP/RPs when the user logs out of the Gluu Server. Please see the [Custom Script Guide](../authn-guide/customauthn.md) to start writing your own custom scripts. 
