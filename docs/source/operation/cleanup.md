# Clean up server

Server has built-in clean up service. There are a few configuration properties.

- `cleanServiceInterval` - defines interval in seconds how often run clean up service. It must be positive, if negative then clean up timer is off.
- `cleanServiceBaseDns` - list of additional `base dns` under which server will look up for expired entities (server look up for expired entries also under built-in `base dns`).
- `cleanServiceBatchChunkSize` - each clean up iteration fetches chunk of expired data per `base dn` and removes it from storage. Default value is 100. Please adjust it according to load.

Any change in configuration properties related to clean up timer takes effect only after `oxauth` restart (`service oxauth restart`).

List of built-in base Dns are printed on server startup (log level must be `debug`). Typical output in log looks as
```
[org.xdi.oxauth.service.CleanerTimer] (CleanerTimer.java:201) - Built-in base dns: [ou=registration_requests,ou=u2f,o=@!2128.9AFB.B310.EB30!0001!690B.5F8F,o=gluu, ou=resources,ou=uma,o=@!2128.9AFB.B310.EB30!0001!690B.5F8F,o=gluu, ou=clients,o=@!2128.9AFB.B310.EB30!0001!690B.5F8F,o=gluu, ou=people,o=@!2128.9AFB.B310.EB30!0001!690B.5F8F,o=gluu, ou=pct,ou=uma,o=@!2128.9AFB.B310.EB30!0001!690B.5F8F,o=gluu, o=@!2128.9AFB.B310.EB30!0001!690B.5F8F,o=gluu, ou=registered_devices,ou=u2f,o=@!2128.9AFB.B310.EB30!0001!690B.5F8F,o=gluu, ou=metric,o=@!2128.9AFB.B310.EB30!0001!690B.5F8F,o=gluu]
```

Clean up is performed based on two attributes of entity:

- `oxAuthExpiration` - date when object should be considered as expired (the number of milliseconds since January 1, 1970, 00:00:00 GMT)
- `oxDeletable` - boolean flag true/false. If false clean up job will not delete the object.
   
Clean up filter looks as `&(oxAuthExpiration<=now)(oxDeletable=true))`.

By default clean up timer is turned on however it is possible to turn it off if set `cleanServiceInterval` to negative value (server restart required).

If clean up work is externalized (e.g. external python script) then it is recommended to turn off internal server clean up (by setting `cleanServiceInterval` to negative value and then restart server).