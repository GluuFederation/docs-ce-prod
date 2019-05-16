# Session Timeout in Gluu

!!! Attention
    The official support end-of-life (EOL) date for Gluu Server 2.4.4 is December 31, 2018. Starting January 1, 2019, no further security updates or bug-fixes will be provided for Gluu Server 2.X. We strongly recommend [upgrading](https://gluu.org/docs/ce/upgrade/) to the newest version.

Session Timeout can be configured under 
JSON Configuration>OxAuth Properties.

These properties are

- SessionUnusedLifeTime
- sessionIdUnauthenticatedUnusedLifetime

## SessionUnusedLifeTime

SessionUnusedLifeTime property is set to default for a day. 
Session timeout works in such way that if the application is logged out, 
if SessionUnusedLifeTime gets expired. If specific session timeout is set 
in an application, it would be overrided by the SessionUnusedLifeTime from 
Gluu.

If application's Session time is less than the session time out 
configured in Gluu, the application's session would be reauthorized and 
set to a future time for timeout, where the applicatin's session timeout 
will be overrided by Gluu's Session timeout property.

## SessionIdUnauthenticatedUnusedLifeTime



List of OxAuth Properties for reference can be found in 
[OxAuth JSON Properties](../reference/JSON-oxauth-prop.md)
