# Service Commands

## Overview

Many configuration changes require stopping or restarting individual services within the Gluu Server. The process to do so differs slightly depending on the operating system in use.

## Available services

The following list of services included with the Gluu Server may differ from deployment to deployment based on installed components.

- httpd/apache2
- oxauth
- oxauth-rp
- identity
- idp
- passport
- casa
- gluu-radius
- opendj
- couchbase-server
- memcached
- redis

## Commands

### Start

``` tab="Ubuntu 18 or CentOS 7"
systemctl start [service name]
```

``` tab="Other OS"
service [service name] start
```

### Stop

``` tab="Ubuntu 18 or CentOS 7"
systemctl stop [service name]
```

``` tab="Other OS"
service [service name] stop
```

### Status

``` tab="Ubuntu 18 or CentOS 7"
systemctl status [service name]
```

``` tab="Other OS"
service [service name] status
```

### Restart

``` tab="Ubuntu 18 or CentOS 7"
systemctl restart [service name]
```

``` tab="Other OS"
service [service name] restart
```
