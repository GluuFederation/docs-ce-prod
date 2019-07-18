# Server clean up

## Overview
The Gluu Server has a built-in service to remove unused and expired files. It runs out-of-the-box, but has several customizable properties as detailed below. 

## Properties

- `cleanServiceInterval` - defines how often to run the clean up service in seconds. It must be a positive number. To turn off the service, set the interval to a negative number.
- `cleanServiceBaseDns` - list of `base dns` under which the server will look for expired entities and entries in addition to the built-in `base dn`
- `cleanServiceBatchChunkSize` - each clean up iteration fetches a chunk of expired data per `base dn` and removes it from storage. The default value is 100. Adjust it according to server load.

[Restart](./services.md#restart) the `oxauth` service for the configuration changes to take effect.

## Log output

A list of built-in base DNs is printed upon server startup (the log level must be set to `debug`). This is an example of the log output:

```
[org.xdi.oxauth.service.CleanerTimer] (CleanerTimer.java:201) - Built-in base dns:  
[ou=registration_requests,ou=u2f,o=@!2128.9AFB.B310.EB30!0001!690B.5F8F,o=gluu,   
ou=resources,ou=uma,o=@!2128.9AFB.B310.EB30!0001!690B.5F8F,o=gluu, ou=clients,o=@!2128.9AFB.B310.EB30!0001!690B.5F8F,o=gluu,  
ou=people,o=@!2128.9AFB.B310.EB30!0001!690B.5F8F,o=gluu, ou=pct,ou=uma,o=@!2128.9AFB.B310.EB30!0001!690B.5F8F,o=gluu,  
o=@!2128.9AFB.B310.EB30!0001!690B.5F8F,o=gluu, ou=registered_devices,ou=u2f,o=@!2128.9AFB.B310.EB30!0001!690B.5F8F,o=gluu,  
ou=metric,o=@!2128.9AFB.B310.EB30!0001!690B.5F8F,o=gluu]
```

## Affected attributes

Clean up is performed based on two entity attributes:

- `oxAuthExpiration` - the date when the object should be considered expired (formatted in Unix time, the number of milliseconds since January 1, 1970, 00:00:00 GMT)
- `oxDeletable` - boolean flag set to true or false. If `false`, the clean up job will not delete the object.
   
The clean up filter is in the following format:

```
&(oxAuthExpiration<=now)(oxDeletable=true))
```

## Disabling the clean up service

By default, the clean up timer is turned on. To turn it off, set the `cleanServiceInterval` property to a negative value (server restart is required).

If the clean up task is performed externally, such as through an external Python script, turn off the internal server clean up.
