# Session Timeout in Gluu

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
