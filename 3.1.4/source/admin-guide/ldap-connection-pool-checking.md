# Brute force protection

Starting from version 3.1.4 the Gluu Server has new options to control connection pool. This can increase services availability and help to resolve environment network issues.

These are new ox-ldap.properties:

# Max wait 20 seconds. Default LDAP value  is 300 seconds. This new default value decrease in to 20 seconds
connection.max-wait-time-millis=20000

# Force to recreate polled connections after 30 minutes
connection.max-age-time-millis=1800000

# Invoke connection health check after checkout it from pool
connection-pool.health-check.on-checkout.enabled=false

# Interval to check connections in pool. Value is 3 minutes. Not used when onnection-pool.health-check.on-checkout.enabled=true
connection-pool.health-check.interval-millis=180000

# How long to wait during connection health check. Max wait 20 seconds
connection-pool.health-check.max-response-time-millis=20000

In most case environment should work well with `connection-pool.health-check.on-checkout.enabled=false`. Only if there are severe network problems in environment there is sense to enable it.
It's usefull option but due to additional check before using connection it can led to 20-30% LDAP operations performacne decrease.
In most other cases reasonable values in `connection-pool.health-check.interval-millis` and `connection.max-age-time-millis` should be enough for any environment.
