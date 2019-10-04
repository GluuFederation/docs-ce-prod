# Logout from Gluu Server

## OpenID Connect Single Log Out (SLO)

The Gluu Server uses OpenID Connect to end sessions for logout. Usually a logout link is provided to the connected SP and the session is killed inside the IDP. 

When using OpenID Connect Logout, it is recommeneded to use Front-Channel Logout. In Front-Channel Logout the browser receives a page with a list of application logout urls within an iframe. This prompts the browser to call each application logout individually and the OpenID Connect end-session endpoint via Javascript. 

The workflow for single logout for two applications using OpenID Connect Front-Channel Logout would be the following:

1. App-A - registers `frontchannel_logout_uri_1`

1. App-B - registers `frontchannel_logout_uri_2`

1. App-A - login to the Authorization Server (AS), in this case the Gluu Server.

1. App-B - login to AS (SSO)

1. App-A - calls `/end_session`

1. AS - returns back HTML with iframes where each iframe points to all `frontchannel_logout_uris` within this session, in our case it is `frontchannel_logout_uri_1` and `frontchannel_logout_uri_2`

1. Browser loads HTML (with all iframes, so it calls `frontchannel_logout_uri_1` and `frontchannel_logout_uri_2`)

1. App-A does not know anything about `frontchannel_logout_uri_2`, it just calls `/end_session` endpoint and it's the responsibility of the AS to track it and return the correct HTML page with iframes (once iframe is loaded, it means that `frontchannel_logout_uri_2` is called and app-B must log itself out).

There are a few important points to note:

1. `post_logout_redirect_uri` is not mandatory by session specification but registration specification says `The value MUST have been previously registered with the OP`. We have dual behavior description directly in specification. `oxauth` ends session successfully (if session is present on OP) independently from whether `post_logout_redirect_uri` is valid or not. If it's not valid (or not provided) `oxauth` will NOT perform redirect. If redirect is required `post_logout_redirect_uri` MUST be provided. If it is not provided then server returns 400 with message `Session is ended successfully but redirect to post logout redirect uri is not performed because it fails validation` and error `post_logout_uri_not_associated_with_client`. `oxauth` consider end session without redirect as not proper behavior however it's still up to RP whether to use redirect or not.
2. `id_token_hint` and `session_id` parameters are optional. Therefore OP will end session successfully if these parameters are missed. However from other side if RP included them in request OP validates them and if any of those are invalid OP returns 400 (Bad Request) http code.

1. `id_token_hint` and `session_id` parameters are optional. Therefore OP will end session successfully even if these parameters are not present. However, from if the RP includes them in the request and the OP validates them, and if any of those are invalid, the OP will return a 400 (Bad Request) http code. `post_logout_redirect_uri` is validated against the client which takes part in SSO. If a session does not exist, or can not be identified, then an error page is shown. However it is possible to allow a redirect to the RP without validation if `allowPostLogoutRedirectWithoutValidation` is set to `true`, and it is white listed via `clientWhiteList` (by default `*` wildcard is used which makes it white listed).

Read the [OpenID Connect Front-Channel Logout Specifications](http://openid.net/specs/openid-connect-frontchannel-1_0.html) to learn more.

## SAML Logout
Gluu Server now supports SAML2 Single Logout. Once it's [enabled by the adminstrator](../admin-guide/saml.md#saml-single-logout), the logout URL is `https://[hostname]/idp/Authn/oxAuth/logout`.

The user will be directed to the following confirmation page.

![SAML2 SLO Confirmation Page](../img/saml/saml_slo_confirm.png)

## Customizing Logout
It is possible to use a custom authentication script to call individual logout methods for both SAML and OpenID Connect and log out of the desired SP/RPs when the user logs out of the Gluu Server. Please see the [Custom Script Guide](../authn-guide/customauthn.md) to start writing your own custom scripts. 
