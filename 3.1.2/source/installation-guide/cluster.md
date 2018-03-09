
# Manual Gluu Server Clustering

## Introduction
If you have requirements for high availability (HA) or failover, follow the instructions below to manually configure multi-master replication (MMR) across multiple Gluu Servers.

!!! Note
    If your organization has a Gluu support contract, you have a license to use our automated clustering tool: [Cluster Manager](https://gluu.org/docs/cm). Highly recommended :)  

## Concept

Enable OpenDJ replication and also make configuration changes to make Gluu Server highly avaiable, via a proxy.


## Prerequisites

### Ports
Next ports are used by different components to communicate with their peers at other nodes of a cluster. Additional configuration 
efforts may be needed to ensure they can be reached by incoming connections.

|Port| Application| Relation |
-----|------------- | ---
| 22 | SSH | Utility |
| 443| SSL/TLS | Load-balancer to oxAuth |
|4444| OpenDJ Replication| Between Gluu Servers |
|6379| Redis Server | From oxAuth to Redis |
|8989| OpenDJ Replication|  Between Gluu Servers |
|30865| Csync2 Default |  Between Gluu Servers |

### Software
Some prerequisites are necessary for setting up Gluu with delta-syncrepl MMR:   

- A minimum of three (3) servers or VMs: two (2) for Gluu Servers and one (1) for load balancing (in our example, NGINX). For the purpose of this tutorial, the server configurations are as follows:
      
```
45.55.232.15    loadbalancer.example.org (NGINX server)
159.203.126.10  idp1.example.org (Gluu Server 3.1.2 on Ubuntu 14)
138.197.65.243  idp2.example.org (Gluu Server 3.1.2 on Ubuntu 14)
```
     
- To create the following instructions we used Ubuntu 14 Trusty.     

- To create the following instructions we used an Nginx load balancer/proxy, however if you have your own load balancer, like F5 or Cisco, you should use that instead and disregard the instructions about configuring Nginx.   

- Gluu Server version 3.1.2 using OpenDJ.   

- Redis-server for caching short-lived tokens.   

- JXplorer or a similar LDAP browser for editing LDAP.   

## Instructions

### 1. Install Gluu

- First you need to [Install Gluu](https://gluu.org/docs/ce/3.1.2/installation-guide/install/) on one of the servers. It will be referred to as the "primary" for the sake of simplification. Once everything is configured, there will be no primary in the multi-master configuration.

!!! Warning
    Make sure to use a separate NGINX/Load-balancing server FQDN as hostname.   
    Make sure to select OpenDJ as your LDAP choice [1].

- A separate NGINX server is necessary because replicating a Gluu server to a different hostname breaks the functionality of the Gluu web page when using a hostname other than what is in the certificates. For example, if I use idp1.example.com as my host and copy that to a second server (e.g. idp2.example.com), the process of accessing the site on idp2.example.com, even with replication, will fail authentication due to a hostname conflict. So if idp1 fails, you won't be able to use Gluu Server effectively.

- Now for the rest of the servers in the cluster, [download the Gluu packages](https://gluu.org/docs/ce/3.1.2/installation-guide/install/) but **don't run `setup.py` yet**.   

- We want to copy the `/install/community-edition-setu/setup.properties.last` file from the first install to the other servers as `setup.properties` so we have the exact same configurations. (Here I have ssh access to my other server outisde the Gluu chroot)

```

scp /opt/gluu-server-3.1.2/install/community-edition-setup/setup.properties.last root@idp2.example.org:/opt/gluu-server-3.1.2/install/community-edition-setup/setup.properties

```

- Once you have the `setup.properties` file in place on the **other** server(s), modify the IP to the current server:

```

Gluu.Root # cd /install/community-edition
Gluu.Root # vi setup.properties

...
passport_rs_client_jks_pass=xmQNp8RRuP0P
cmd_jar=/opt/jre/bin/jar
oxauth_openid_jks_pass=t1j5ykEaHFs1
idp3WebappFolder=/opt/shibboleth-idp/webapp
countryCode=US
ip=138.197.65.243						<------ changed this to the current server IP
opendj_ldap_binddn=cn\=directory manager
installSaml=False
sysemProfile=/etc/profile
ldap_setup_properties=./templates/opendj-setup.properties
default_openid_jks_dn_name=CN\=oxAuth CA Certificates
oxtrust_config_json=./output/oxtrust-config.json
openldapTLSCACert=/etc/certs/openldap.pem
installJce=True
ldapPassFn=/home/ldap/.pw
...

```

- Now run setup.py   

```

Gluu.Root # ./setup.py

```

- The rest of the configurations for the install should be automatically loaded and all you need to do here is press `Enter`

### 2. Enable Replication

On the first server (idp1.example.org, in our example), utilize these commands inside the Gluu chroot to initialize and enable replication. All `<password>`'s should be changed to the same password.

```
# /opt/opendj/bin/dsreplication enable --host1 idp1.example.org --port1 4444 --bindDN1 "cn=directory manager" --bindPassword1 <password> --replicationPort1 8989 --host2 idp2.example.org --port2 4444 --bindDN2 "cn=directory manager" --bindPassword2 <password> --replicationPort2 8989 --adminUID admin --adminPassword <password> --baseDN "o=gluu" -X -n

# /opt/opendj/bin/dsreplication initialize --baseDN "o=gluu" --adminUID admin --adminPassword <password> --hostSource idp1.example.org --portSource 4444  --hostDestination idp2.gluu.org --portDestination 4444 -X -n
```

Now run these commands on the first server to secure the communication:

```
/opt/opendj/bin/dsconfig -h idp1.example.org -p 4444 -D "cn=Directory Manager" -w <password> --trustAll -n set-crypto-manager-prop --set ssl-encryption:true
/opt/opendj/bin/dsconfig -h idp2.example.org -p 4444 -D "cn=Directory Manager" -w <password> --trustAll -n set-crypto-manager-prop --set ssl-encryption:true
```

Now archive the OpenDJ keystore:

```
# tar -cf opendj_crts.tar -C /opt/opendj/config/ keystore keystore.pin truststore
```

And transfer them to the other nodes and run the following command:

```
# tar -xf opendj_crts.tar -C /opt/opendj/config/
```

Note, if you want to check the status of OpenDJ replication run the following command:

```
/opt/opendj/bin/dsreplication status -n -X -h idp1.example.org -p 4444 -D "cn=Directory Manager" -I admin -w <password>
```

Next we should [install csync2](https://linuxaria.com/howto/csync2-a-filesystem-syncronization-tool-for-linux) for file system replication.

The necessary directories to replicate are as follows:

```
/opt/gluu/jetty/identity/conf/shibboleth3/idp/
/opt/gluu/jetty/identity/conf/shibboleth3/sp/
/opt/shibboleth-idp/conf
/opt/shibboleth-idp/metadata/
/opt/shibboleth-idp/sp/
/opt/shibboleth-idp/temp_metadata/
/etc/gluu/conf/
/etc/certs/
/opt/symas/etc/openldap/schema
```

### 3. Install NGINX

**If you have your own load balancer, you can use the following NGINX configuration documentation as a guide for how to proxy with the Gluu server.**

On loadbalancer.example.org 

```

apt-get install nginx -y

```

- We need the `httpd.crt` and `httpd.key` certs from one of the Gluu servers.   

- From the NGINX server:  

```

mkdir /etc/nginx/ssl/

```

- From the first Gluu server you installed:

```

scp /opt/gluu-server-3.1.2/etc/certs/httpd.key root@loadbalancer.example.org:/etc/nginx/ssl/
scp /opt/gluu-server-3.1.2/etc/certs/httpd.crt root@loadbalancer.example.org:/etc/nginx/ssl/

```

- And from the server we created our nginx.conf file (idp1.example.org in my case), to the NGINX server (loadbalancer.example.org)

- The following is a working `nginx.conf` example template for a Gluu cluster.

```
events {
        worker_connections 6500;
}

http {
  upstream backend_id {
  ip_hash;
  server idp1.example.org:443 max_fails=2 fail_timeout=10s;
  server idp2.example.org:443 max_fails=2 fail_timeout=10s;
  }
  upstream backend {
  server idp1.example.org:443 max_fails=2 fail_timeout=10s;
  server idp2.example.org:443 max_fails=2 fail_timeout=10s;
  }
  server {
    listen       80;
    server_name  loadbalancer.example.org;
    return       301 https://loadbalance.example.org$request_uri;
   }
  server {
    listen 443;
    server_name loadbalancer.example.org;

    ssl on;
    ssl_certificate         /etc/nginx/ssl/httpd.crt;
    ssl_certificate_key     /etc/nginx/ssl/httpd.key;

    location ~ ^(/)$ {
      proxy_pass https://backend;
      proxy_redirect          off;
      proxy_next_upstream     error timeout invalid_header http_500;
      proxy_connect_timeout   2;
      proxy_set_header        Host            $host;
      proxy_set_header        X-Real-IP       $remote_addr;
      proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    location /.well-known {
        proxy_pass https://backend/.well-known;
        proxy_redirect          off;
        proxy_next_upstream     error timeout invalid_header http_500;
        proxy_connect_timeout   2;
        proxy_set_header        Host            $host;
        proxy_set_header        X-Real-IP       $remote_addr;
        proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    location /oxauth {
        proxy_pass https://backend/oxauth;
        proxy_redirect          off;
        proxy_next_upstream     error timeout invalid_header http_500;
        proxy_connect_timeout   2;
        proxy_set_header        Host            $host;
        proxy_set_header        X-Real-IP       $remote_addr;
        proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    location /identity {
        proxy_pass https://backend_id/identity;
        proxy_redirect          off;
        proxy_next_upstream     error timeout invalid_header http_500;
        proxy_connect_timeout   2;
        proxy_set_header        Host            $host;
        proxy_set_header        X-Real-IP       $remote_addr;
        proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    location /cas {
        proxy_pass https://backend/cas;
        proxy_redirect          off;
        proxy_next_upstream     error timeout invalid_header http_500;
        proxy_connect_timeout   2;
        proxy_set_header        Host            $host;
        proxy_set_header        X-Real-IP       $remote_addr;
        proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    location /asimba {
        proxy_pass https://backend/asimba;
        proxy_redirect          off;
        proxy_next_upstream     error timeout invalid_header http_500;
        proxy_connect_timeout   2;
        proxy_set_header        Host            $host;
        proxy_set_header        X-Real-IP       $remote_addr;
        proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    location /passport {
        proxy_pass https://backend/passport;
        proxy_redirect          off;
        proxy_next_upstream     error timeout invalid_header http_500;
        proxy_connect_timeout   2;
        proxy_set_header        Host            $host;
        proxy_set_header        X-Real-IP       $remote_addr;
        proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
    }

  }
}


```

Please adjust the configuration for your IDP (Gluu Servers) and your Load Balancer FQDN's

### 4. Install and configure redis

Now you need to install and configure redis-server on one or more servers. 

- Redis-server is an memory caching solution created by redis-labs. It's ideal for clustering solutions but needs additional encryption.       
- Mind you, this can not be configured on your NGINX server or you'll get routing issues when attempting to cache.
     
- The standard redis-server's configuration file binds to `127.0.0.1`. We need to comment out this entry so that it listens to external requests.    

```
vi /etc/redis/redis.conf
```

- Modify this entry

```

bind 127.0.0.1

```

- Now restart redis-server

```

service redis-server force-reload

```

!!! Warning
    As I mentioned before, redis communications are not encrypted, but using a solution such as stunnel is relatively easy. Please see [how to do this here.](https://redislabs.com/blog/using-stunnel-to-secure-redis/)

!!! Note
    Redis can also be configured for HA and failover with multiple methods utilizing [Sentinel](https://redis.io/topics/sentinel) or [Redis-cluster](https://redis.io/topics/cluster-tutorial)

### 5. Modify JSON entries 

Use JXplorer (or a similar LDAP browser) to modify some of the JSON entries in LDAP for handling accessible caching and multiple authorization servers.      

- In JXplorer, you can connect to your LDAP server using your credentials you configured with setup.py. For example:     

![alt text](https://raw.githubusercontent.com/GluuFederation/cluster-mgr/master/manual_install/images/JXplorer%20config.png)

- What we need to do is open "gluu" -> "appliances" -> the first inum here will be where all the attributes we need to modify will be.

- We have to modify the "oxCacheConfig" attribute to include our redis-server FQDN. Here I installed redis-server outside of one of my Gluu chroots.

![alt text](https://raw.githubusercontent.com/GluuFederation/cluster-mgr/master/manual_install/images/ManualCache_ox.png)

- The important things I changed were "cacheProviderType" from "IN_MEMORY" to "REDIS". After that, in the "redisConfiguration" portion of "servers", I added "idp1.example.org:6379" which is the server I installed redis-server. 6379 is the default port redis-server listens and you can add as many servers as you want her, they just need to be comma separated.

- We also must make sure that all LDAP servers are utilized for authorization by modifying the "oxIDPAuthentication" attribute.

![alt text](https://raw.githubusercontent.com/GluuFederation/cluster-mgr/master/manual_install/images/ManualCache_auth.png)

- Here all I did was changed the servers from localhost:1636 to the FQDN's of my servers.

```

"servers\": [\"idp1.example.org:1636\",\"idp2.example.org:1636\"],

```

- Now click `Submit` on the bottom after all your changes. 

### 6. Transfer certificates

Now you need to transfer certificates from the first server to the other servers.

- It's necessary to copy certificates from the primary server we installed Gluu on and replace the certificates in `/etc/certs/` on the other servers.       

- From the primary server:

```

scp /opt/gluu-server-3.1.2/etc/certs/* root@idp2.example.org:/opt/gluu-server-3.1.2/etc/certs/

```

- We must give ownership of the certs to gluu, with the exception of `oxauth-keys.j*` which need to be owned by jetty

- On the server the certificates were just transferred to:

```

Gluu.Root # cd /etc/certs/
Gluu.Root # chown .gluu *
Gluu.Root # chown jetty.jetty oxauth-keys.j*

```

- Next we need to update the keystores in all of our Gluu instances, including the primary server. 

- Download this script to **every** server, which automatically removes and adds the necessary certificates to the keystore.

```

Gluu.Root # wget https://raw.githubusercontent.com/GluuFederation/cluster-mgr/master/manual_install/keystore_Config.py

```

- Modify the `hostname` to your NGINX/Load-balancer's FQDN.

```
import os.path
import subprocess

cmd_keytool = '/opt/jre/bin/keytool'
hostname = "loadbalancer.example.org"
```

- Run the script

```

Gluu.Root # python keystore_Config.py

```

This error is fine, if OpenLDAP is not installed, and vice versa for OpenDJ.

```
keytool error: java.io.FileNotFoundException: /etc/certs/openldap.crt (No such file or directory)
```

- Restart Identity and oxAuth on all servers, then restart all your Gluu servers.

```

Gluu.Root # service identity stop && service oxauth restart && service identity start
Gluu.Root # logout
service gluu-server-3.1.2 restart

```

- Now your administrator web UI and oxAuth has some failover redundancy. There are obviously more configurations necessary on the network layer of your topology for true HA failover, but that is outside of the scope for this documentation.          

## Support
If you have any questions or run into any issues, please open a ticket on [Gluu Support](https://support.gluu.org).
