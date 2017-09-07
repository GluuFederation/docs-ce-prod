
# Manual Gluu Server Clustering 

## Introduction
If you have requirements for high availability (HA) or failover, you can configure your Gluu Server for multi-master replication by following the instructions below.

## Prerequisites

Some prerequisites are necessary for setting up Gluu with delta-syncrepl MMR:

- A minimum of three (3) servers or VMs--two (2) for Gluu Servers and one (1) for load balancing (in our example, NGINX);     
- To create the following instructions we used Ubuntu 14 Trusty, but the process should not be OS specific;        
- To create the following instructions we used an Nginx load balancer, however if you have your own load balancer, like F5 or Cisco, you can use that instead and disregard the bottom instructions about configuring Nginx.      
- Gluu Server 3.x using OpenLDAP.    

## Instructions

1. [Install Gluu](https://gluu.org/docs/ce/3.1.0/installation-guide/install/) on one server making sure to use a separate NGINX server FQDN as hostname. 

- A separate NGINX server is recommended, but not necessary, since replicating a Gluu server to a different hostname breaks the functionality of the Gluu webpage, when using a hostname other than what is in the certificates. For example, if I used c1.gluu.info as my host and another install of gluu as c2.gluu.info, the process of accessing the site on c2.gluu.info, even with replication, will fail authentication. So if c1 failed, you couldn't access the Gluu web GUI anymore.

- The other servers should [install the Gluu Server Package](https://gluu.org/docs/ce/3.1.0/installation-guide/install/#install-gluu-server-package) but not run setup.py. This will install the necessary init.d scripts for us.

2. Copy the Gluu install environment to the other servers. 

```
Gluu.Root # logout
# service gluu-server-3.1.0 stop
```

- Now tar the `/opt/gluu-server-3.1.0/ folder`, copy it to the other servers and extract it in the /opt/ folder.

```
tar -cvf gluu.gz /opt/gluu-server-3.1.0/
scp gluu.gz root@server2.com:/opt/
...
```

Server 2

```
service gluu-server-3.0.2 stop
cd /opt/
rm -rf /opt/gluu-server-3.1.0/
tar -xvf gluu.gz
```

- Make sure the file structure here is /opt/gluu-server-3.1.0/

- For CentOS, it is necessary to copy the /etc/gluu/keys/ files to the new servers, as the /sbin/gluu-serverd-3.1.0/ login function requires them to SSH into the Gluu instal @ localhost

3. Start Gluu, login and modify the `/etc/hosts/` inside the chroot to point the FQDN of the NGINX server to the current servers IP address

- For example my node 2 server's (c2.gluu.info) ip address is `138.197.100.101` so on server 2:

```
127.0.0.1       localhost
::1             ip6-localhost ip6-loopback
ff02::1         ip6-allnodes
ff02::2         ip6-allrouters
138.197.100.101         c3.gluu.info
```

- Note that my c3 NGINX server FQDN is pointing to my c2 ip.

- Repeat this for every server that Gluu is unpacked on.

- This is necessary to deal with internal routing of NGINX to Apache2 and Apache2 to NGINX. So even though my ip of my FQDN is different, this process still works.

4. There needs to be primary server to replicate from initially for delta-syncrepl to inject data from. After the initial sync, all servers will be exactly the same, as delta-syncrepl will fill the newly created database. 

- So choose one server as a base and then on every other server:

```
rm /opt/gluu/data/main_db/*.mdb
```

- Now make accesslog directories on every servers and give ldap ownership:

```
mkdir /opt/gluu/data/accesslog_db
chown -R ldap. /opt/gluu/data/
```

5. Now is where we will set servers to associate with each other for MMR by editing the slapd.conf, ldap.conf and symas-openldap.conf files.

- Creating the slapd.conf file is relatively easy, but can be prone to errors if done manually. Attached is a script and template files for creating multiple slapd.conf files for every server. Download git and clone the necessary files:

```
apt-get update && apt-get install git && cd /tmp/ && git clone https://github.com/GluuFederation/cluster-mgr.git && cd /tmp/cluster-mgr/manual_install/slapd_conf_script/
```

- We need to change the configuration file for our own specific needs:

```
vi syncrepl.cfg
```

- Here we want to change the `ip_address`, `fqn_hostname`, `ldap_password` to our specific server instances. For example:

```
[server_1]
ip_address = 192.168.30.133
fqn_hostname = server1.com
ldap_password = (your password)
enable = Yes

[server_2]
ip_address = 192.168.30.130
fqn_hostname = server2.com
ldap_password = (your password)
enable = Yes

[server_3]
...
```

- The hostname should be the FQDN of the servers, not the NGINX server.

- If required, you can change the `/tmp/cluster-mgr/manual_install/slapd_conf_script/ldap_templates/slapd.conf` to fit your specific needs to include different schemas, indexes, etc. Avoid changing any of the `{#variables#}`.

- Now run the python script `create_slapd_conf.py`:

```
# python /tmp/cluster-mgr/manual_install/slapd_conf_script/create_slapd_conf.py
```

- This will output multiple `.conf` files in your current directory named to match your server FQDN:

```
# ls
... server1_com.conf  server2_com.conf ...
```

- Move each .conf file to their respective server @:

`/opt/gluu-server-3.0.2/opt/symas/etc/openldap/slapd.conf`

- Now create and modify the ldap.conf:

```
vi /opt/symas/etc/openldap/ldap.conf
```

- Add these lines

```
TLS_CACERT /etc/certs/openldap.pem
TLS_REQCERT never
``` 

- Modify the HOST_LIST entry of symas-openldap.conf:

```
vi /opt/symas/etc/openldap/symas-openldap.conf
```

- Replace: 

```
HOST_LIST="ldaps://127.0.0.1:1636/"
```

With: 

```
HOST_LIST="ldaps://0.0.0.0:1636/ ldaps:///"
```

6. It is important that our servers times are synchronized so we must install ntp outside of the Gluu chroot and set ntp to update by the minute (necessary for delta-sync log synchronization). If time gets out of sync, the entries will conflict and their could be issues with replication.

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

7. Force-reload solserver on every server
```
# service gluu-server-3.0.2 login
# service solserver force-reload
```

8. Delta-sync multi-master replication should be initializing and running. Check the logs for confirmation. It might take a moment for them to sync, but you should end up see something like the following:

```
# tail -f /var/log/openldap/ldap.log | grep sync

Aug 23 22:40:29 dc4 slapd[79544]: do_syncrep2: rid=001 cookie=rid=001,sid=001,csn=20170823224029.216104Z#000000#001#000000
Aug 23 22:40:29 dc4 slapd[79544]: syncprov_matchops: skipping original sid 001
Aug 23 22:40:29 dc4 slapd[79544]: syncrepl_message_to_op: rid=001 be_modify
```

9. **If you have your own load balancer, you are done here.** If not, let's configure your NGINX server for oxTrust and oxAuth web failover. 

- We need the httpd.crt and httpd.key certs from one of the Gluu servers.   

- From the NGINX server:  

```
mkdir /etc/nginx/ssl/
scp root@server1.com:/opt/gluu-server-3.0.2/etc/certs/httpd.key /etc/nginx/ssl/
scp root@server1.com:/opt/gluu-server-3.0.2/etc/certs/httpd.crt /etc/nginx/ssl/
```

- Next we install and configure NGINX to proxy-pass connections.  

```
apt-get install nginx -y
cd /etc/nginx/
>nginx.conf
vi nginx.conf
```

- Put the following template in it's place. Make sure to change the `{serverX_ip_or_FQDN}` portion to your servers IP addresses or FQDN under the upstream section. Add as many servers as exist in your replication setup. The `server_name` needs to be your NGINX servers FQDN.    

```
user www-data;
worker_processes 4;
pid /run/nginx.pid;

events {
        worker_connections 768;
        # multi_accept on;
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
        proxy_pass https://backend_id/.well-known;
    }
    location /oxauth {
        proxy_pass https://backend_id/oxauth;
    }
    location /identity {
        proxy_pass https://backend_id/identity;
    }

  }
}

```

- Now all traffic for the Gluu web GUI will route through one address i.e. `nginx.gluu.info`. This gives us fail-over redundancy for our Gluu web GUI if any server goes down, as NGINX automatically does passive health checks.   

## Support 
If you have any questions or run into any issues, please open a ticket on [Gluu Support](https://support.gluu.org).
