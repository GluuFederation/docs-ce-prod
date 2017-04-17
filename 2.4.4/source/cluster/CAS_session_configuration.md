# CAS session configuration in Gluu Server CE cluster

'Session Management' is crucial in CAS cluster setup. CAS single server installation is easy with Gluu Server's out of the box pieces. 
For CAS cluster in Gluu Server CE cluster environment we need to apply couple of changes; which are stated below. 
This is the second part of CAS configuration in Gluu Server CE. We performed these operations in a 2-node Gluu CE cluster which are based
on CentOS6.x operating system. 

## Memcached configuration

 - Deployer need to perform this operation as 'root' inside Gluu Server container
 - Install 'memcached-1.2.8-repcached-2.2-1.el6_.x86_64.rpm'
    - Get RPM from Gluu 
      - RPM is rare in internet; deployer can use the 'memcached-repcached' source to build his/her own setup
	  - rpm -ivh memcached-1.2.8-repcached-2.2-1.el6_.x86_64.rpm
 - Modify 'memcached' configuration file ( location: /etc/sysconfig/memcached )
    - Working configuration: 
```
GLUU.[root@idp-d ~]# cat /etc/sysconfig/memcached
PORT="11211"
USER="memcached"
MAXCONN="1024"
CACHESIZE="64"
OPTIONS=""
```
 - Restart memcached with 'service memcached restart'

## Twemproxy ( aka. nutcracker ) configuration

 - Deployer need to perform this operation as 'root' inside Gluu Server container
 - Install 'nutcracker-0.3.0-1.x86_64.rpm'
	  - Get RPM from Gluu
		    - RPM is rare; deployer can use the 'twemproxy' source to build his/her own setup
	  - rpm -ivh nutcracker-0.3.0-1.x86_64.rpm
 - Configure 'nutcracker' configuration: ( location: /etc/nutcracker/nutcracker.yml )
    - Reference: https://github.com/twitter/twemproxy
    - listening address: Nutcracker listening address and port
    - hash: Name of hash functions
    - distribution: We are using 'ketama' 
    - timeout: Value in msec. This value represents the waiting interval for establishing and receiving a connection from a server. 
    - backlog: TCP backlog argument. 
    - server_retry_timeout: Time in msec. to wait before retyring a temporarily ejected server. 
    - server_failure_limit: Numeric value; number of consecutive failure after a temporary ejected connection from server. 
    - servers: IP address with memcached port number and weight for all nodes in cluster. Adding internal hostname for all servers will be a good choice. 
    - Working condition: 
```
GLUU:
  listen: 127.0.0.1:22123
  hash: fnv1a_64
  distribution: ketama
  timeout: 400
  backlog: 1024
  preconnect: true
  auto_eject_hosts: true
  server_retry_timeout: 600000
  server_failure_limit: 1
  servers:
  - 192.168.1.2 :11211:1 idp1.gluu.org
  - 192.168.1.3 :11211:1 idp2.gluu.org
```

  - Restart nutcracker: service nutcracker restart

## Configure CAS for nutcracker/twemproxy
  
  - Deployer need to perform this operation as 'tomcat' user inside Gluu Server container
  - Point CAS server to use nutcracker instead of memcached directly. 
     - Location: '/opt/tomcat/webapps/cas/WEB-INF/cas.properties'
     - Working condition:
```
#=======================================
# Memcached connection configuration
#=======================================
memcached.servers=127.0.0.1:22123
```

## Firewall setting
   - Modify firewall with below setting:
```
-A INPUT -s 192.168.1.2 -p tcp -m tcp --dport 22123 -j ACCEPT
-A INPUT -p tcp --destination-port 11211 -m state --state NEW  -m iprange --src-range 192.168.1.2-192.168.1.3 -j ACCEPT
-A INPUT -p udp --destination-port 11211 -m state --state NEW  -m iprange --src-range 192.168.1.2-192.168.1.3 -j ACCEPT
```

## Testing

Best testing is to make sure both server are UP behind LB and push SSO from CAS app. 
See if both servers can respond and 'IF ONE SERVER GENERATE A TICKET', 'OTHER SERVER CAN VALIDATE THAT SERVICE-TICKET'
