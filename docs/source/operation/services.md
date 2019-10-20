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

``` tab="Ubuntu 18, RHEL 7, Debian 9, or CentOS 7"
systemctl start [service name]
```

``` tab="Ubuntu 16"
service [service name] start
```

### Stop

``` tab="Ubuntu 18, RHEL 7, Debian 9, or CentOS 7"
systemctl stop [service name]
```

``` tab="Ubuntu 16"
service [service name] stop
```

### Status

``` tab="Ubuntu 18, RHEL 7, Debian 9, or CentOS 7"
systemctl status [service name]
```

``` tab="Ubuntu 16"
service [service name] status
```

### Restart

``` tab="Ubuntu 18, RHEL 7, Debian 9, or CentOS 7"
systemctl restart [service name]
```

``` tab="Ubuntu 16"
service [service name] restart
```

### Reload
This command is used for the `apache2` and `httpd` services.

``` tab="Ubuntu 18, RHEL 7, Debian 9, or CentOS 7"
systemctl reload [service name]
```

``` tab="Ubuntu 16"
service [service name] reload
```
