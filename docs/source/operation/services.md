# Service Commands

## Overview

Many configuration changes require stopping or restarting individual services within the Gluu Server. 

## Commands

### Start

``` tab="Ubuntu 18 or CentOS 7"
systemctl [service name] start
```

``` tab="Other OS"
service [service name] start
```

### Stop

``` tab="Ubuntu 18 or CentOS 7"
systemctl [service name] stop
```

``` tab="Other OS"
service [service name] stop
```

### Status

``` tab="Ubuntu 18 or CentOS 7"
systemctl [service name] status
```

``` tab="Other OS"
service [service name] status
```

### Restart

``` tab="Ubuntu 18 or CentOS 7"
systemctl [service name] restart
```

``` tab="Other OS"
service [service name] restart
```

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
