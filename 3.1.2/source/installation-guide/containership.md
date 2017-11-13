# Deploying the Gluu Server on Containership.io 

The following documentation provides instructions for deploying the Gluu Server on [Containership.io](https://containership.io).

Containership is a containers-as-a-service platform providing users with a single pane of glass to easily deploy, manage and scale their containerized applications on any public or private cloud. Containership provides both developers and operators with the simplest possible solution for managing applications from development through production, while facilitating self-service. 

## Prerequisites

1. [Containership.io](https://containership.io) account
2. A resolveable public domain
3. SSL certificate and key for the domain

## Create a cluster in containership

Navigate to the containership interface and perform the following:

1. Choose a cloud provider
2. Choose “Containership” as cluster orchestration framework
3. Choose cloud region
4. Choose Ubuntu OS
5. Choose your SSH key (for admin)
6. Create 1 leader host with at least 1GB RAM
7. Create 2 follower hosts with 4 CPUs and 8GB RAM
8, Choose a name and environment  ( Example, Name: gluu, Environment: dev/test/prod )

## Add firewall rule:

Go to cluster Firewall tab, add following rule for SSH connection:

Description: SSH for admin
Target: Host
Target Hosts: All
Protocol: TCP
Port: 22
Source: CIDR
IP address (CIDR format): click "Use My IP" button

Wait until cluster has been provisioned; all hosts are created and connected each other, all builtin containers has been deployed.

## Initialize Configuration

1. Add Consul application using Containership Marketplace
2. After Consul is deployed in cluster, install Docker in local machine and pull config-init image.

`# docker pull gluufederation/config-init:3.0.1_rev1.0.0-beta3`

Now go back to Containership cluster. Choose Applications tab and consul box. In Containers tab, click one of the container. That will show us Host information. Copy the Public IP and Private IP. We will need it for connecting config-init to remote Consul KV.

Consul application in Containership uses private IP and port 8314 to listen to client connection. Hence we need to do SSH tunneling to expose the port in our local machine.

`# ssh -L 0.0.0.0:8500:<REMOTE-PRIVATE-IP>:8314 <SSH-USER>@<REMOTE-PUBLIC-IP>`

After tunneling established, in another terminal, we can start generating initial config in our local machine for our Gluu Server cluster.

Prepare following steps before generating initial config:

1. Use resolvable public domain
2. Use SSL certificate and key for the domain (create them if we don't have one yet; self-signed is possible)

Here's an example on how to run config-init container:

```
# docker run --rm \
    -v /path/to/org_ssl.crt:/etc/certs/gluu_https.crt \
    -v /path/to/org_ssl.key:/etc/certs/gluu_https.key \
    gluufederation/config-init:3.0.1_rev1.0.0-beta3 \
    --admin-pw my-password \
    --email 'my-email@my.domain.com' \
    --domain my.domain.com \
    --org-name 'My Organization' \
    --kv-host <LOCAL-IP> \
    --kv-port 8500 \
    --save
```

Wait until the process finished.

Note: for self-signed, just remove the volume mapping from the above cmd.

Now base data for gluu server is generated and saved in consul.
You can close ssh tunnel now.

## Deploy Gluu from the Marketplace

Select Gluu Server from cluster application and deploy it by following instruction provided by application page.

[Some screenshot here after CS team create marketplace icon]


This application will deploy following containers:

- openldap-init   
- openldap    
- keyrotation    
- oxAuth    
- oxTrust    
- nginx    

## Managing Public Domain

Add CNAME record to domain, the value should be the gluu-nginx DNS entry.
