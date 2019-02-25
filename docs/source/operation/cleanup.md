# Clean up server

Server has built-in clean up service. There are a few configuration properties.

- `cleanServiceInterval` - defines interval in seconds how often run clean up service. It must be positive, if negative then clean up timer is off.
- `cleanServiceBaseDns` - list of `base dns` under which server will look up for expired entities.
- `cleanServiceBatchChunkSize` - each clean up iteration fetches chunk of expired data per `base dn` and removes it from storage.

Any change in configuration properties related to clean up timer takes effect only of `oxauth` restart (`service oxauth restart`).

Clean up is performed based on two attributes of entity:

- `oxAuthExpiration` - date when object should be considered as expired (the number of milliseconds since January 1, 1970, 00:00:00 GMT)
- `oxDeletable` - boolean flag true/false. If false clean up job will not delete the object.
   
Clean up filter looks as `&(oxAuthExpiration<=now)(oxDeletable=true))`.

By default clean up timer is turned on however it is possible to turn it off if set `cleanServiceInterval` to negative value (server restart requires).

If clean up work is externalized (e.g. external python script) then it is recommended to turn off internal server clean up (by setting `cleanServiceInterval` to negative value and then restart server).