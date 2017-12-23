
# Manual Gluu Server Clustering

## Introduction
If you have requirements for high availability (HA) or failover, follow the instructions below to manually configure multi-master replication (MMR) across multiple Gluu Servers.

!!! Note
    If your organization has a Gluu support contract, please email [sales@gluu.org](mailto:sales@gluu.org) for access to our automated clustering tool. 

## Concept

In this tutorial we are configuring MMR with OpenLDAP using delta-syncrepl by creating an accesslog database and configuring synchronization with the `slapd.conf` file. 

The `ldap.conf` file for each Gluu Server will allow the self-signed certs that Gluu creates and configuring the `symas-openldap.conf` to allow external connections for LDAP on ports 1636 and 636 (for SSL). 

There are also some additional steps that are required to persist Gluu functionality across servers. This is where a load-balancer/proxy is required.

## Prerequisites

Some prerequisites are necessary for setting up Gluu with delta-syncrepl MMR:   

- A minimum of three (3) servers or VMs: two (2) for Gluu Servers and one (1) for load balancing (in our example, NGINX). For the purpose of this tutorial, the server configurations are as follows:
      
```
45.55.232.15    loadbalancer.example.org (NGINX server)
159.203.126.10  idp1.example.org (Gluu Server 3.1.2 on Ubuntu 14)
138.197.65.243  idp2.example.org (Gluu Server 3.1.2 on Ubuntu 14)
```
     
- To create the following instructions we used Ubuntu 14 Trusty.     

- To create the following instructions we used an Nginx load balancer/proxy, however if you have your own load balancer, like F5 or Cisco, you should use that instead and disregard the instructions about configuring Nginx.   

- Gluu Server version 3.x using OpenLDAP.   

- Redis-server for caching sessions.   

- JXplorer or a similar LDAP browser for editing LDAP.   

## Instructions

### 1. [Install Gluu](https://gluu.org/docs/ce/3.1.2/installation-guide/install/)

- Make sure to use a separate NGINX/Load-balancing server FQDN as hostname.   

- This will be considered your "primary" server for the sake of this documentation.   

- A separate NGINX server is necessary because replicating a Gluu server to a different hostname breaks the functionality of the Gluu web page when using a hostname other than what is in the certificates. For example, if I use idp1.example.com as my host and copy that to a second server (e.g. idp2.example.com), the process of accessing the site on idp2.example.com, even with replication, will fail authentication due to a hostname conflict. So if idp1 fails, you can't access the Gluu web GUI anymore.   

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

### 2. Choose a primary server

There needs to be a primary server to replicate from initially for delta-syncrepl to inject data. After the initial sync all servers will be exactly the same, as delta-syncrepl will fill the newly created database.

- Choose one server as a base and then on every **other** server:   

```
Gluu.Root # rm /opt/gluu/data/main_db/*.mdb
```

- Now make accesslog directories on **every server** (including the primary server) and give ldap ownership:   

```
Gluu.Root # mkdir /opt/gluu/data/accesslog_db
Gluu.Root # chown -R ldap. /opt/gluu/data/
```

### 3. Modify configuration files

You now need to modify the following configuration files: `slapd.conf`, `ldap.conf` and `symas-openldap.conf`

- Creating the `slapd.conf` file for replication is relatively easy but can be prone to errors if done manually. Attached is a script and template files for creating multiple `slapd.conf` files for every server. Download git and clone the necessary files on **one** server:

```
Gluu.Root # apt-get update && apt-get install git && cd /tmp/ && git clone https://github.com/GluuFederation/cluster-mgr.git && cd /tmp/cluster-mgr/manual_install/slapd_conf_script/
```

- We need to change the configuration file for our own specific needs:

```
Gluu.Root # vi syncrepl.cfg
```

- Here we want to change the `ip_address`, `fqn_hostname`, `ldap_password` to our specific server instances. For example:

```

[server_1]
ip_address = 159.203.126.10
fqn_hostname = idp1.example.org
ldap_password = (your password)
enable = Yes

[server_2]
ip_address = 138.197.65.243
fqn_hostname = idp2.example.org
ldap_password = (your password)
enable = Yes

[server_3]
...
[nginx]
fqn_hostname = loadbalancer.example.org

```

 - Include the FQDN's and IP addresses of your Gluu servers and NGINX server (if you want the NGINX configuration file to be created automatically)

- If required, you can change the `/tmp/cluster-mgr/manual_install/slapd_conf_script/ldap_templates/slapd.conf` to fit your specific needs to include different schemas, indexes, etc. Avoid changing any of the `{#variables#}`.

- Now run the python script `create_slapd_conf.py` (Built with python 2.7) in the `/tmp/cluster-mgr/manual_install/slapd_conf_script/` directory :

```

Gluu.Root # python create_slapd_conf.py

```

- This will output multiple `.conf` files in `/tmp/cluster-mgr/manual_install/slapd_conf_script/` named to match your server FQDN:

```

Gluu.Root #  ls

... idp1.example.org   idp2.example.org  ... nginx.conf

```

- Move each .conf file to their respective server replacing the `slapd.conf`:

```

Gluu.Root # cp /tmp/cluster-mgr/manual_install/slapd_conf_script/idp1_example_org.conf /opt/symas/etc/openldap/slapd.conf

```

and for the other server(s), my key to access the other server is outside the chroot so I have to logout to transfer

```
Gluu.Root # logout
scp /opt/gluu-server-3.1.2/tmp/cluster-mgr/manual_install/slapd_conf_script/idp2_example_org.conf root@idp2.example.org:/opt/gluu-server-3.1.2/opt/symas/etc/openldap/slapd.conf

```

- Now create and modify the ldap.conf **on every server**:

```

Gluu.Root # vi /opt/symas/etc/openldap/ldap.conf

```

- Add these lines (it's an empty file)

```

TLS_CACERT /etc/certs/openldap.pem
TLS_REQCERT never

```

- Modify the HOST_LIST entry of symas-openldap.conf **on every server**:

```

vi /opt/symas/etc/openldap/symas-openldap.conf

```


- Replace:

```

HOST_LIST="ldaps://127.0.0.1:1636/"

```

- With:

```

HOST_LIST="ldaps://0.0.0.0:1636/ ldaps:///"

```

- **On all your servers**, inside the chroot, modify `/etc/gluu/conf/ox-ldap.properties` replacing:

`servers: localhost:1636`

With (obviously use your own FQDN's):

`servers: idp1.example.org:1636,idp2.example.org:1636`

Placing all servers in your cluster topology in this config portion.

### 4. Server synchronization

It is important that our server's times are synchronized so we must install `ntp` outside of the Gluu chroot and set `ntp` to update by the minute (necessary for delta-sync log synchronization). If time gets out of sync, the entries will conflict and their could be issues with replication.

```
GLUU.root@host:/ # logout
# apt install ntp
# crontab -e
```

- Select your preferred editor and add this to the bottom of the file:

```
* * * * * /usr/sbin/ntpdate -s time.nist.gov
```
 
- This synchronizes the time every minute.

- Force-reload solserver on every server
```
# service gluu-server-3.1.2 login
# service solserver force-reload
```

- Delta-sync multi-master replication should be initializing and running. Check the logs for confirmation. It might take a moment for them to sync, but you should end up see something like the following:

```
# tail -f /var/log/openldap/ldap.log | grep sync

Aug 23 22:40:29 dc4 slapd[79544]: do_syncrep2: rid=001 cookie=rid=001,sid=001,csn=20170823224029.216104Z#000000#001#000000
Aug 23 22:40:29 dc4 slapd[79544]: syncprov_matchops: skipping original sid 001
Aug 23 22:40:29 dc4 slapd[79544]: syncrepl_message_to_op: rid=001 be_modify
```

### 5. Install NGINX

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

- The following configuration is the base template for what was created in our script.

```
events {
        worker_connections 768;
}

http {
  upstream backend_id {
    ip_hash;
    server {server1_ip_or_FQDN}:443;
    server {server2_ip_or_FQDN}:443;
  }
  upstream backend {
    server {server1_ip_or_FQDN}:443;
    server {server2_ip_or_FQDN}:443;
        
  }
  server {
    listen       80;
    server_name  {NGINX_server_FQDN};
    return       301 https://{NGINX_server_FQDN}$request_uri;
   }
  server {
    listen 443;
    server_name {NGINX_server_FQDN};

    ssl on;
    ssl_certificate         /etc/nginx/ssl/httpd.crt;
    ssl_certificate_key     /etc/nginx/ssl/httpd.key;

    location ~ ^(/)$ {
      proxy_pass https://backend;
    }
    location /.well-known {
        proxy_pass https://backend/.well-known;
    }
    location /oxauth {
        proxy_pass https://backend/oxauth;
    }
    location /identity {
        proxy_pass https://backend_id/identity;
    }

  }
}

```

### 6. Install and configure redis

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

- As I mentioned before, redis communications are not encrypted, but using a solution such as stunnel is relatively easy. Please see [how to do this here.](https://redislabs.com/blog/using-stunnel-to-secure-redis/)

- Redis can also be configured for HA and failover with multiple methods utilizing [Sentinel](https://redis.io/topics/sentinel) or [Redis-cluster](https://redis.io/topics/cluster-tutorial)

### 7. Modify JSON entries 

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

### 8. Transfer certificates

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

- Run the script

```

Gluu.Root # python keystore_Config.py

```

- Restart Identity and oxAuth on all servers, then restart all your Gluu servers.

```

Gluu.Root # service identity stop && service oxauth restart && service identity start
Gluu.Root # logout
service gluu-server-3.1.2 restart

```

- Now your administrator web UI and oxAuth have some failover redundancy. There are obviously more configurations necessary on the network layer of your topology for true HA failover, but that is outside of the scope for this documentation.          

## Support
If you have any questions or run into any issues, please open a ticket on [Gluu Support](https://support.gluu.org).
