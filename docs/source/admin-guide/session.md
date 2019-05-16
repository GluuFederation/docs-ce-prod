# Session Management

Gluu Server sessions are stored as a cookie in the browser. For each session, we know to which applications the browser has authenticated.

However, remember that the application has it's own session. The hard part is that on logout, you need to notify each application that its local session should be ended.

The best way to handle this currently is "Front channel logout". This is described in in the [OpenID Connect specification](http://openid.net/specs/openid-connect-frontchannel-1_0.html). 

Basically, the Gluu Server OpenID `end_session` endpoint returns an html page, which contains an iFrame for each application to which the user has authenticated. The iFrame contains a link to each application's respective logout url. This special html page should be loaded in the background (not displayed to the user). The iFrame urls should be loaded by the browser. This provides a way to "trick" the user into calling the logout page of each application, so the application's cookies can be cleared.

## Session Timeouts
Session Timeout can be configured under 
`JSON Configuration` > `oxAuth Properties`.

These properties are

- SessionUnusedLifeTime
- sessionIdUnauthenticatedUnusedLifetime

## SessionUnusedLifeTime

The `SessionUnusedLifeTime` property is set to a day by default. Session timeout works in a way such that if a user logs out of an application the `SessionUnusedLifeTime` gets expired. If a specific session timeout is set in an application, it will be overrided by the `SessionUnusedLifeTime` from Gluu.

If an application's Session time is less than the session time out configured in Gluu, the application's session would be reauthorized and 
set to a future time for timeout, where the applicatin's session timeout will get overrided by Gluu's Session timeout property.

## SessionIdUnauthenticatedUnusedLifeTime

List of OxAuth Properties for reference can be found in 
[OxAuth JSON Properties](../reference/JSON-oxauth-prop.md)
