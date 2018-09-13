# Session Management

Gluu Server (OP) sessions are stored in OP cache (it can be in-memory, redis, memcached or ldap depending on `cacheProviderType` configuration property). 

OP session can have two states:

- `unauthenticated` - when end-user hits OP and is not authenticated, session object is created and put in cache with `unauthenticated` state
- `authenticated` - when user is successfully authenticated 

In browser OP session is referenced via `session_id` cookie.
 
Lets say user hits RP1 which redirects to OP for authentication. Once user is authenticated OP creates `session_id` cookie and set state to `authenticated` (in OP cache). If user hits RP2, it will redirect user for authentication to OP but since session is already authenticated OP authenticates user automatically against RP2 (without authentication prompt).  
 
Remember that the application may have it's own RP session. The hard part is that on logout, all RPs and OP has to be notified, so both OP and RP sessions are cleared/ended. 

The best way to handle this currently is "Front channel logout". This is described in the [OpenID Connect specification](http://openid.net/specs/openid-connect-frontchannel-1_0.html). 

Basically, the Gluu Server OpenID `end_session` endpoint returns an html page, which contains an iFrame for each application to which the user has authenticated. The iFrame contains a link to each application's respective logout url. This special html page should be loaded in the background (not displayed to the user). The iFrame urls should be loaded by the browser. This provides a way to "trick" the user into calling the logout page of each application, so the application's cookies can be cleared.

Learn more about the flow for logout across many applications in the [logout document](../operation/logout.md)

## Session Timeouts

Session Timeout can be configured under 
`JSON Configuration` > `oxAuth Properties`.

There are following properties related to OP session:

- `sessionIdLifetime` - lifetime of the OP session in seconds. It sets both `session_id` cookie expires property as well as OP session object expiration in cache. So it is global property for OP session objects. Since `3.1.4` it is possible to set value to 0 or -1 which means that expiration is not set (not available in `3.1.3` or earlier except `2.4.4`). In this case `session_id` cookie expire value is set to `session` value which means it is valid until browser session ends.
- `sessionIdUnusedLifetime` - unused OP session lifetime (default 1 day). If OP session is not used for given amount of time then OP session is removed. 
- `sessionIdUnauthenticatedUnusedLifetime` - lifetime of `unauthenticated` OP session. 
- `sessionIdEnabled` - specifies whether it is allowed to authenticate user by session automatically (without end-user interaction).  
- `sessionIdPersistOnPromptNone` - specifies whether persist/update session object with data if `prompt=none`. Default value is `true`, so session is persisted by default.

Since OP session has two states `authenticated` and `unauthenticated`, the `sessionIdUnauthenticatedUnusedLifetime` is used when OP session is `unauthenticated` and `sessionIdUnusedLifetime` is used when OP session is `authenticated`.

Both `unused` properties specify period of time in seconds. OP calculates this period as `currentUnusedPeriod = now - session.lastUsedAt`. So for OP session with states:

- `unauthenticated` - if `currentUnusedPeriod` >= `sessionIdUnauthenticatedUnusedLifetime` then OP session is removed.
- `authenticated` - if `currentUnusedPeriod` >= `sessionIdUnusedLifetime` then OP session is removed.

OP updates `lastUsedAt` property of OP session object:

- initially it is set during creation
- it is updated during each authentication attempt (successful or not successful)

It is important to note that OP session `lastUsedAt` property is not updated during RP usage.

List of OxAuth Properties for reference can be found in 
[OxAuth JSON Properties](../reference/JSON-oxauth-prop.md)

## FAQ

### How can we force user to log out if user is in idle state on RP during 4 hours?

OP doesn't know anything about end-user activity on RP. Therefore RP has to track activity internally and when inactivity period is reached (4 hours) RP has to perform front-channel logout.

### How can we force user to log out if the browser is closed?

Set `sessionIdLifetime` to `-1` value sets `session_id` cookie value to `expires=session` and OP session object without expiration. Most of the browsers clears cookie with `expires=session` when browser is closed. It is available in `3.1.4` version (it is not available in 3.1.3 version or earlier except 2.4.4). 
