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

1. `post_logout_redirect_uri` is not mandatory by session specification but registration specification says `The value MUST have been previously registered with the OP`. We have dual behavior description directly in specification. `oxauth` ends session successfully (if session is present on OP) independently from whether `post_logout_redirect_uri` is valid or not and will NOT perform redirect. If redirect is required `post_logout_redirect_uri` MUST be provided. If it is not provided then server returns 400 with message `Session is ended successfully but redirect to post logout redirect uri is not performed because it fails validation` and error `post_logout_uri_not_associated_with_client`. `oxauth` consider end session without redirect as not proper behavior however it's still up to RP whether to use redirect or not.
2. `id_token_hint` and `session_id` parameters are optional. Therefore OP will end session successfully if these parameters are missed. However from other side if RP included them in request OP validates them and if any of those are invalid OP returns 400 (Bad Request) http code.

`post_logout_redirect_uri` is validated against client which take part in SSO. If the session does not exist or can not be identified, an error page is shown. However, it is possible to allow redirect to the RP without validation if `allowPostLogoutRedirectWithoutValidation` is set to `true` and it is whitelisted via `clientWhiteList` (by default, the `*` wildcard is used which makes it white listed).

There is `End Session` interception script which allows to modify HTML returned during frontchannel logout.

The sample `End Session` script is [available here](./sample-end-session.py)

Read the [OpenID Connect Front-Channel Logout Specifications](http://openid.net/specs/openid-connect-frontchannel-1_0.html) to learn more about logout with OpenID Connect.

## Back-channel logout

It is possible to use backchannel logout. Here is was spec says:

- An upside of back-channel communication is that it can be more reliable than communication through the User Agent, since in the front-channel, the RP's browser session must be active for the communication to succeed.
- A downside of back-channel communication is that the session state maintained between the OP and RP over the front-channel, such as cookies and HTML5 local storage, are not available when using back-channel communication. As a result, all needed state must be explicitly communicated between the parties.

Thus it's up to RP what logout to support, Front-channel or Back-channel.
During client registration it is recommended to specify `frontchannel_logout_uri` or `backchannel_logout_uri`. If both are specified then AS perform logout for `backchannel_logout_uri` (and ignores `frontchannel_logout_uri`). 

During Back-channel logout AS collects all `backchannel_logout_uri`s from all involved clients in SSO session and calls them asynchronously with `logout_token`.

```
POST /backchannel_logout HTTP/1.1
Host: rp.example.org
Content-Type: application/x-www-form-urlencoded

logout_token=eyJhbGci ... .eyJpc3Mi ... .T3BlbklE ...
```

If `post_logout_redirect_uri` is validated successfully then AS sends redirect to it or otherwise send back OK (200) response code (independently whether involved RPs sends back successfull response or failure).
AS redirect to `post_logout_redirect_uri` or OK (200) response indicates that AS session is ended. It doesn't mean that all RP's backchannel calls are completed successfully.

![image](../img/openid/backchannel-client-ui.png)

Read the [OpenID Connect Backchannel Logout Specifications](https://openid.net/specs/openid-connect-backchannel-1_0.html) to learn more about logout with OpenID Connect.

## SAML Logout
Gluu Server now supports SAML Single Logout. Once it's [enabled by the administrator](../admin-guide/saml.md#saml-single-logout), the logout URL is `https://[hostname]/idp/Authn/oxAuth/logout`.

The user will be directed to the following confirmation page.

![SAML2 SLO Confirmation Page](../img/saml/saml_slo_confirm.png)

## Customizing Logout
It is possible to use a custom authentication script to call individual logout methods for both SAML and OpenID Connect and log out of the desired SP/RPs when the user logs out of the Gluu Server. Please see the [Custom Script Guide](../authn-guide/customauthn.md) to start writing your own custom scripts. 
