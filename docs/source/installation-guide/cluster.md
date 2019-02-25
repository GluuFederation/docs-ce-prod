
# Manual Gluu Server Clustering

## Introduction
If you have requirements for high availability (HA) or failover, follow the instructions below to manually configure multi-master replication (MMR) across multiple Gluu Servers.

Gluu also offers a tool to automate the steps below, called [Cluster Manager](https://gluu.org/docs/cm). Cluster Manager is licensed under the [Gluu Support license](https://github.com/GluuFederation/cluster-mgr/blob/master/LICENSE), which requires a Gluu support contract for use *in production*. All organizations may use Cluster Manager for development purposes.  

## Concept

Clustering uses OpenDJ replication and configuration changes to greatly improve Gluu Server availability, via a proxy.

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

- A minimum of three (3) servers or VMs: two (2) for Gluu Servers and one (1) for load balancing (in our example, NGINX).

- A separate NGINX server is necessary because replicating a Gluu server to a different hostname breaks the functionality of the Gluu web page when using a hostname other than what is in the certificates. For example, if I use idp1.example.com as my host and copy that to a second server (e.g. idp2.example.com), the process of accessing the site on idp2.example.com, even with replication, will fail authentication due to a hostname conflict. So if idp1 fails, you won't be able to use Gluu Server effectively.

- For the purpose of this tutorial, the server configurations are as follows:
      
```
45.55.232.15    loadbalancer.example.org (NGINX server)
159.203.126.10  idp1.example.org (Gluu Server 3.1.5 on Ubuntu 16.04 )
138.197.65.243  idp2.example.org (Gluu Server 3.1.5 on Ubuntu 16.04 )

```
     
- To create the following instructions we used Ubuntu 16.04     

- To create the following instructions we used an Nginx load balancer/proxy, however if you have your own load balancer, like F5 or Cisco, you should use that instead and disregard the instructions about configuring NGINX   

- Gluu Server version 3.1.5 using OpenDJ   

- Redis-server for caching short-lived tokens   

- JXplorer or a similar LDAP browser for editing LDAP   

## Instructions

### 1. Install Gluu

- First you need to [Install Gluu](https://gluu.org/docs/ce/installation-guide/install/) on one of the servers. It will be referred to as the "primary" for the sake of simplification. Once everything is configured, there will be no primary in the multi-master configuration

- On all of the non-primary Gluu Cluster members (not the NGINX server), [download the Gluu packages](https://gluu.org/docs/ce/installation-guide/install/) but **don't run `setup.py` yet**!   

- On the primary Gluu Server, log in to the chroot and cd to `/install/community-edition-setup/`

- After setup was completed on the primary server, a file named "setup.properties.last" was created in the same directory. We want to copy the `/install/community-edition-setup/setup.properties.last` file from the first install to the other servers as `setup.properties`. This will allow us to to maintain the same configuration across the nodes.(Here I have SSH access to my other server outside the Gluu chroot)

If you do not have `scp` command you must install `openssh-client`:

```
apt-get install openssh-client

```
!!! Note
    Make sure that all your hosts file have the correct configuration to point the Ips of all IDPs and loadbalancer to the responding hostnames. For us all three servers have the following added in `/etc/hosts`.
    
    ```
    45.55.232.15    loadbalancer.example.org (NGINX server) -- for us this has not been setup yet
    159.203.126.10  idp1.example.org (Gluu Server 3.1.5 on Ubuntu 16.04)
    138.197.65.243  idp2.example.org (Gluu Server 3.1.5 on Ubuntu 16.04)
    
    ```
    
Otherwise continue to the following command changing `myuser@idp2.example.org` to your login credentials for each idp server your sending it to :

```

scp /opt/gluu-server-3.1.5/install/community-edition-setup/setup.properties.last myuser@idp2.example.org:/opt/gluu-server-3.1.5/install/community-edition-setup/setup.properties

```

If this throws a `Permission denied` error, that means your user, here `myuser`, does not have permission to write in the directory. Use the following command at the server you are trying to send the file to, here that is `idp2.example.org`. Change `<user>` to the user used in the command above, here `myuser`.

```
chown <user> /opt/gluu-server-3.1.5/install/community-edition-setup/

```

for security the `<user>` should always be set back to `root` so after transfer of files is completed run the command again with `root` as `<user>`.

```
chown root /opt/gluu-server-3.1.5/install/community-edition-setup/

```

- If the Gluu server has not been started, start it and login. Once you have the `setup.properties` file in place on the **other** server(s), modify the IP to the current server, we only have one so we changed our `ip=159.203.126.10` of idp1 server to the IP of idp2 server which is `ip=138.197.65.243.


```
service gluu-server-3.1.5 start
service gluu-server-3.1.5 login
Gluu.Root # vi /install/community-edition-setup/setup.properties
setup.properties

...
passport_rs_client_jks_pass=xmQNp8RRuP0P
cmd_jar=/opt/jre/bin/jar
oxauth_openid_jks_pass=t1j5ykEaHFs1
idp3WebappFolder=/opt/shibboleth-idp/webapp
countryCode=US
ip=138.197.65.243						<------ changed this from 159.203.126.10 to the current server IP
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

- Now run `setup.py`.   

```
cd /install/community-edition-setup
./setup.py

```

- The rest of the configurations for the install should be automatically loaded as shown below. All you need to do here is press `Enter`

```
Installing Gluu Server...
Detected OS  :  ubuntu
Detected init:  systemd
Detected Apache:  2.4

Installing Gluu Server...

For more info see:
  ./setup.log
  ./setup_error.log


** All clear text passwords contained in ./setup.properties.last.


hostname                                             idp1.example.org
orgName                                                 Example Inc.
os                                                         ubuntu
city                                                       Austin
state                                                          Tx
countryCode                                                    US
support email                                    support@example.org
Applications max ram                                         3072
Admin Pass                                                   test
Install oxAuth                                               True
Install oxTrust                                              True
Install LDAP                                                 True
Install Apache 2 web server                                  True
Install Shibboleth SAML IDP                                 False
Install oxAuth RP                                           False
Install Passport                                            False


Proceed with these values [Y|n]


```

!!! Note
    Make sure that all your hosts file have the correct configuration to point the Ips of all IDPs and loadbalancer to the responding hostnames. For us all three servers have the following added in `/etc/hosts` and in the Gluu containers `/etc/hosts`.
    
    ```
    45.55.232.15    loadbalancer.example.org (NGINX server) -- for us this has not been setup yet
    159.203.126.10  idp1.example.org (Gluu Server 3.1.5 on Ubuntu 16.04)
    138.197.65.243  idp2.example.org (Gluu Server 3.1.5 on Ubuntu 16.04)
    
    ```

### 2. Replication

- Run the commands below in the Gluu container for all your **Nodes** , here that would be for `idp1.example.org` and `idp2.example.org`  :

  Any attempts to login to the LDAP in anyform might result in an instant timeout error due to Java enabling Endpoint Identification which disrputs LDAPS connections. We have to set the default value to `true` by explicitly stating it in the `java.properties` file.

  ```
  sed -i 's/dsreplication.java-args=-Xms8m -client/dsreplication.java-args=-Xms8m -client-Dcom.sun.jndi.ldap.object.disableEndpointIdentification=true/g' /opt/opendj/config/java.properties
  ```
  
  To set the new properties run the command in the Gluu container.

   ```
   
   /opt/opendj/bin/dsjavaproperties

   ```
   
   You should recieve an operation successful message:
   
   ```
   
   The operation was successful.  The server commands will use the java arguments and java home specified in the properties file located in /opt/opendj/config/java.properties

   ```
   We need to make all nodes accessible to each other by setting the listening address to `0.0.0.0`. In your command you may have to change `cn=directory manager` to your CN ( by default `cn=directory manager` unless changed ) ,and  `<password>` to your password set in the first installation of Gluu. If the below commands are not connecting try changing `localhost` to the nodes explicit IP addresss, here that would be `159.203.126.10` and `138.197.65.243`.
   
   **Run both commands**
   
   ```
   /opt/opendj/bin/dsconfig -h localhost -p 4444 -D 'cn=directory manager' -w <password> -n set-administration-connector-prop --set listen-address:0.0.0.0 -X
   
   ```
   
   ```
   
   /opt/opendj/bin/dsconfig -h localhost -p 4444 -D 'cn=directory manager' -w <password> -n set-connection-handler-prop --handler-name 'LDAPS Connection Handler' --set enabled:true --set listen-address:0.0.0.0 -X
   
   ```
   **This is the end of commands that had to be initiated in all nodes**
   
- Run the commands below in the Gluu container on your first "primary" Gluu server installed , here that would be `idp1.example.org`:   
 
  Utilize this command inside the Gluu container to enable replication changing `<password>`'s to the password of your first installed Gluu server. If the below commands are not connecting try changing your nodes hostnames to, here `idp1.example.org` and `idp2.example.org` to the nodes explicit IP addresss, here that would be `159.203.126.10` and `138.197.65.243`. **You must add all your nodes to this command, here we only have two**

  ```

  /opt/opendj/bin/dsreplication enable --host1 idp1.example.org --port1 4444 --bindDN1 "cn=directory manager" --bindPassword1 <password> --replicationPort1 8989 --host2 idp2.example.org --port2 4444 --bindDN2 "cn=directory manager" --bindPassword2 <password> --replicationPort2 8989 --adminUID admin --adminPassword <password> --baseDN "o=gluu" -X -n

  ```

  You will get a message like this if it works : 

  ```
  Establishing connections ..... Done.
  Checking registration information ..... Done.
  Configuring Replication port on server idp1.example.org:4444 ..... Done.
  Configuring Replication port on server idp2.example.org:4444 ..... Done.
  Updating replication configuration for baseDN o=gluu on server
  idp1.example.org:4444 .....Done.
  Updating replication configuration for baseDN o=gluu on server
  idp2.example.org:4444 .....Done.
  Updating registration configuration on server idp1.example.org:4444 ..... Done.
  Updating registration configuration on server idp2.example.org:4444 ..... Done.
  Updating replication configuration for baseDN cn=schema on server
  idp1.example.org:4444 .....Done.
  Updating replication configuration for baseDN cn=schema on server
  idp2.example.org:4444 .....Done.
  Initializing registration information on server idp2.example.org:4444 with the
  contents of server idp1.example.org:4444 .....Done.
  Initializing schema on server idp2.example.org:4444 with the contents of server
  idp1.example.org:4444 .....Done.

  Replication has been successfully enabled.  Note that for replication to work
  you must initialize the contents of the base DNs that are being replicated
  (use dsreplication initialize to do so).


  See /tmp/opendj-replication-8219363385622666180.log for a detailed log of this
  operation.

  ```

  Now initialize replication. Change <password> to the password of your first installed Gluu server. **You must add all your nodes to this command**:

  ```

  /opt/opendj/bin/dsreplication initialize --baseDN "o=gluu" --adminUID admin --adminPassword <password> --hostSource idp1.example.org --portSource 4444  --hostDestination idp2.gluu.org --portDestination 4444 -X -n

  ```

  You will get a message like this if it works : 

  ```
  Initializing base DN o=gluu with the contents from idp1.example.org:4444:
  3202 entries processed (23 % complete).
  1233321 entries processed (100 % complete).
  Base DN initialized successfully.

  See /tmp/opendj-replication-7940848656437845148.log for a detailed log of this
  operation.


   ```

   Secure the communications to all nodes. **You must add all your nodes to this command**:

   ```
   /opt/opendj/bin/dsconfig -h idp1.example.org -p 4444 -D "cn=Directory Manager" -w <password> --trustAll -n set-crypto-manager-prop    --set ssl-encryption:true
   /opt/opendj/bin/dsconfig -h idp2.example.org -p 4444 -D "cn=Directory Manager" -w <password> --trustAll -n set-crypto-manager-prop --set ssl-encryption:true
   ```

   Now archive the OpenDJ keystore:

   ```
   cd /opt/opendj/config
   
   tar -cf opendj_crts.tar keystore keystore.pin truststore
   
   ```
   

   Transfer it to the other nodes. The `scp` command will most likley not be installed in your gluu container so exit out by just typing `exit`. Then transfer `opendj_crts.tar` to all the other nodes.  
   
   ```
   
    scp /opt/gluu-server-3.1.5/opt/opendj/config/opendj_crts.tar  myuser@idp2.example.org:/opt/gluu-server-3.1.5/opt/opendj/config/
   
   ```
   !!! Note
       If you want to check the status of OpenDJ replication run the following command:

       ```
       
       /opt/opendj/bin/dsreplication status -n -X -h idp1.example.org -p 4444 -I admin -w <password>

       ```
       
       
   **This is the end of commands that had to be initiated in the first "primary" node**
   
   
Run the following commands in all the Gluu container nodes where the archive of OpenDK keystore was sent to:

 ```
 cd /opt/opendj/config/
   
 tar -xf opendj_crts.tar
   
 ```
 
 I

Next (install csync2)[https://linuxaria.com/howto/csync2-a-filesystem-syncronization-tool-for-linux] for file system replication on all nodes outside the gluu container.

```
apt-get install csync2

```
- On the "primary" node, here idp1@example.org, do the following :
  
  Generate key file :
  
  ```
  csync2 -k /etc/csync2.key
  
  ```
  
  Create an SSL certificate Csync2 :
  
  ```
  openssl genrsa -out /etc/csync2_ssl_key.pem 1024
  openssl req -batch -new -key /etc/csync2_ssl_key.pem -out /etc/csync2_ssl_cert.csr
  openssl x509 -req -days 3600 -in /etc/csync2_ssl_cert.csr -signkey /etc/csync2_ssl_key.pem -out /etc/csync2_ssl_cert.pem
  
  ```
  
  Create a `csyn2.conf` file and place all directories to be replicated as in the `csync2.conf` file :
  
  ```
  vi /etc/csync2.conf
  
  ```
  
  Add more `host <hostname>` according to the number of nodes you have.
  
  **`csync2.conf`**
  
  ```
  
  group gluucluster
  {
  host idp1.example.org;
  host idp2.example.org;
 
  key /etc/csync2.key;
  include /opt/gluu-server-3.1.5/opt/gluu/jetty/identity/conf/shibboleth3/idp/;
  include /opt/gluu-server-3.1.5/opt/gluu/jetty/identity/conf/shibboleth3/sp/;
  include /opt/gluu-server-3.1.5/opt/shibboleth-idp/conf;
  include /opt/gluu-server-3.1.5/opt/shibboleth-idp/metadata/;
  include /opt/gluu-server-3.1.5/opt/shibboleth-idp/sp/;
  include /opt/gluu-server-3.1.5/opt/shibboleth-idp/temp_metadata/;
  include /opt/gluu-server-3.1.5/etc/gluu/conf/;
  
  exclude *~ .*;
  }
  
 
  ```
  Copy the contents of `csync2.conf` into the file `csync2.cfg`.
  
  Copy the csync2 configuration file, certifications and keys to the all the other nodes, here only idp2.example.org.
  
  ```
  
  scp /etc/csync2* user@idp2.example.org:/etc/
  
  ```
  Make sure your hostname is set to the FQDN on each node :
  
  **Node 1**
  
  ```
  
  hostname idp1.example.org
  
  ```
  
  **Node 2**
  
  ```
  
  hostname idp2.example.org
  
  ```
  
  Restart inetd on all nodes
  
  ```
  
   /etc/init.d/openbsd-inetd restart
  
  ```
  
  You can test the connection at each node by running :
  
  ```
  
  csync2 -T
  
  ```
  
  - Run the following on **Node 1** `primary` :
  
      Force files to win conflicts
  
      ```
  
      csync2 -fr /
   
      ```
      
      Start the synchronization process :
      
      ```
      
       csync2 -xvvv
       
      ```

  
  - Run the following on **All other nodes** :
  
      Force files to win conflicts
  
      ```
  
      csync2 -fr /
   
      ```
      
      Start the synchronization process :
      
      ```
      
      csync2 -xvvv
       
      ```
  - Add a cron on **all nodes** to do the syncing using `crontab -e` :
  
    You can add a regular cron that runs every 5 mins at all nodes like this :
    
    ```
    */5 * * * * csync2 -x
    
    ```
    or for a more complex add syncronized crons that run in almost a continuous enviorment i.e the first node starts syncing one minuite the other starts the next and so forth. At our two nodes situation we would do the following: (**This is a very effective way in syncing data securely. However, you must know the size of data being moved and hence program the cron accordingly**) 
    
    **Node 1** “At every 10th minute from 0 through 59.”
    
    ```
    
    0-59/10 * * * * csync2 -x
    
    ```
    
    **Node 2** “At every 10th minute from 5 through 59.” 
    
    ```
    
    5-59/10 * * * * csync2 -x
    
    ```
    
    Reload cron :
    
    ```
    
    service cron reload
    
    ```
    

  
### 3. Install NGINX

!!! Warning
    Make sure to use a separate NGINX/Load-balancing server FQDN as hostname.   


**If you have your own load balancer, you can use the following NGINX configuration documentation as a guide for how to proxy with the Gluu Server.**

On loadbalancer.example.org 

```

apt-get install nginx -y

```

- We need the `httpd.crt` and `httpd.key` certs from one of the Gluu servers.   

- From the NGINX server:  

```

mkdir /etc/nginx/ssl/

```

- From the first Gluu Server you installed:

```

scp /opt/gluu-server-3.1.5/etc/certs/httpd.key root@loadbalancer.example.org:/etc/nginx/ssl/
scp /opt/gluu-server-3.1.5/etc/certs/httpd.crt root@loadbalancer.example.org:/etc/nginx/ssl/

```

- And from the server, we created our nginx.conf file (idp1.example.org in my case), to the NGINX server (loadbalancer.example.org)

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

Please adjust the configuration for your IDP (Gluu Servers) and your Load Balancer FQDNs

### 4. Install and Configure Redis

Now you need to install and configure redis-server on one or more servers. 

- Redis-server is an memory caching solution created by redis-labs. It's ideal for clustering solutions but needs additional encryption       
- Mind you, this can not be configured on your NGINX server or you'll get routing issues when attempting to cache
     
- The standard redis-server's configuration file binds to `127.0.0.1`. We need to comment out this entry so that it listens to external requests    

```
vi /etc/redis/redis.conf
```

- Modify this entry:

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

### 5. Modify JSON Entries 

Use JXplorer (or a similar LDAP browser) to modify some of the JSON entries in LDAP for handling accessible caching and multiple authorization servers.      

- In JXplorer, you can connect to your LDAP server using your credentials you configured with setup.py. For example:     

![alt text](https://raw.githubusercontent.com/GluuFederation/cluster-mgr/master/manual_install/images/JXplorer%20config.png)

- What we need to do is open "Gluu" -> "appliances" -> the first inum here will be where all the attributes we need to modify will be

- We have to modify the "oxCacheConfig" attribute to include our redis-server FQDN. Here I installed redis-server outside of one of my Gluu chroots

![alt text](https://raw.githubusercontent.com/GluuFederation/cluster-mgr/master/manual_install/images/ManualCache_ox.png)

- The important things I changed were "cacheProviderType" from "IN_MEMORY" to "REDIS". After that, in the "redisConfiguration" portion of "servers", I added "idp1.example.org:6379" which is the server I installed redis-server. 6379 is the default port redis-server listens and you can add as many servers as you want her, they just need to be comma separated

- We also must make sure that all LDAP servers are utilized for authorization by modifying the "oxIDPAuthentication" attribute.

![alt text](https://raw.githubusercontent.com/GluuFederation/cluster-mgr/master/manual_install/images/ManualCache_auth.png)

- Here all I did was changed the servers from localhost:1636 to the FQDNs of my servers

```

"servers\": [\"idp1.example.org:1636\",\"idp2.example.org:1636\"],

```

- Click `Submit` on the bottom after all your changes 

### 6. Transfer Certificates

You need to transfer certificates from the first server to the other servers.

- It's necessary to copy certificates from the primary server we installed Gluu on and replace the certificates in `/etc/certs/` on the other servers.       

- From the primary server:

```

scp /opt/gluu-server-3.1.5/etc/certs/* root@idp2.example.org:/opt/gluu-server-3.1.5/etc/certs/

```

- We must give ownership of the certs to Gluu, with the exception of `oxauth-keys.j*` which need to be owned by jetty

- On the server, the certificates were just transferred to:

```

Gluu.Root # cd /etc/certs/
Gluu.Root # chown .gluu *
Gluu.Root # chown jetty.jetty oxauth-keys.j*

```

- Next we need to update the keystores in all of our Gluu instances, including the primary server 

- Download this script to **every** server, which automatically removes and adds the necessary certificates to the keystore

```

Gluu.Root # wget https://raw.githubusercontent.com/GluuFederation/cluster-mgr/master/manual_install/keystore_Config.py

```

- Modify the `hostname` to your NGINX/Load-balancer's FQDN

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

- Restart Identity and oxAuth on all servers, then restart all your Gluu servers

```

Gluu.Root # service identity stop && service oxauth restart && service identity start
Gluu.Root # logout
service gluu-server-3.1.5 restart

```

- Now your administrator web UI and oxAuth has some failover redundancy. There are obviously more configurations necessary on the network layer of your topology for true HA failover, but that is outside of the scope for this documentation          

## Support
If you have any questions or run into any issues, please open a ticket on [Gluu Support](https://support.gluu.org).
