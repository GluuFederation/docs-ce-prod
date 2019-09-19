# Test Drive Demo

## Overview

Follow the instructions below to quickly deploy a single-node Gluu Server demo using Docker. 

!!! Note
    "Test drive" is perfect for *testing* the Gluu Server. For production deployments, follow instructions for your [OS of choice](./index.md#supported-operating-systems), e.g. [Docker](./install-docker.md).  

## Requirements

### Linux Requirements

For Docker deployments, provision a VM with: 

- The minimum system requirements, as described in the [VM Preparation Guide](../installation-guide/index.md#system-requirements). 

- Both [Docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-using-the-convenience-script) and [Docker Compose](https://docs.docker.com/compose/install/#install-compose) installed. 

### OS X (Mac) Requirements

1)  Meet the [system requirements](https://docs.docker.com/docker-for-mac/install/)

1)  Install [Docker Desktop for Mac](https://hub.docker.com/editions/community/docker-ce-desktop-mac)

## Instructions

1. Log in as root:

    ```
    sudo su -
    ```

1. Obtain the files for deployment:
    
    ```
    wget https://github.com/GluuFederation/community-edition-containers/archive/4.0.0.zip \
        && unzip 4.0.0.zip
    ```
    
    ```
    cd community-edition-containers-4.0.0/examples/single-host
    ```
    
    ```
    chmod +x run_all.sh
    ```   
<!--
    1. For this Test Drive, we recommend continuing with the default settings. If a more customized deployment is needed, see the [Custom Installation Options](#custom-installation-options) section at the bottom of the page.

    ### Deploying Gluu Server
-->

1.  Run the following command and follow the prompts:

    ```
    ./run_all.sh
    ```
    
    Do not be alarmed about the `warning` alerts that may show up. Wait until it prompts you for information or loads the previous configuration found. If this is a fresh install, the output will look like this :

    ```
    ./run_all.sh
    [I] Determining OS Type and Attempting to Gather External IP Address
    Host is detected as Linux
    Is this the correct external IP Address: 172.189.222.111 [Y/n]? y
    [I] Preparing cluster-wide config and secrets
    WARNING: The DOMAIN variable is not set. Defaulting to a blank string.
    WARNING: The HOST_IP variable is not set. Defaulting to a blank string.
    Pulling consul (consul:)...
    latest: Pulling from library/consul
    bdf0201b3a05: Pull complete
    af3d1f90fc60: Pull complete
    d3a756372895: Pull complete
    54efc599d7c7: Pull complete
    73d2c234fe14: Pull complete
    cbf8018e609a: Pull complete
    Digest: sha256:bce60e9bf3e5bbbb943b13b87077635iisdksdf993579d8a6d05f2ea69bccd
    Status: Downloaded newer image for consul:latest
    Creating consul ... done
    [I] Checking existing config in Consul
    [W] Unable to get config in Consul; retrying ...
    [W] Unable to get config in Consul; retrying ...
    [W] Unable to get config in Consul; retrying ...
    [W] Configuration not found in Consul
    [I] Creating new configuration, please input the following parameters
    Enter Domain:                 yourdomain
    Enter Country Code:           US
    Enter State:                  TX
    Enter City:                   Austin
    Enter Email:                  email@example.com
    Enter Organization:           Gluu Inc
    Enter Admin/LDAP Password:
    Confirm Admin/LDAP Password:
    Continue with the above settings? [Y/n]y
    ```

    The startup process may take some time. You can keep track of the deployment by using the following command:
    
    ```
    ./run_all.sh logs -f
    ```
    
## Uninstall the Gluu demo

To remove all deployed objects, run the following command inside `community-edition-containers-4.0.0/examples/single-host`: 
    
    ```
    ./run_all.sh down
    ```

## FAQ

- **How to use ldapsearch**

```
docker exec -ti ldap /opt/opendj/bin/ldapsearch -h localhost -p 1636 -Z -X -D "cn=directory manager" -b "o=gluu" -s base -T "objectClass=*"
```

- **Locked out of your Gluu demo? This is how Vault can be manually unlocked**

   1. Get Unseal key from `vault_key_token.txt`
   
   1. Log into vault container: `docker exec -it vault sh`
   
   1. Run this command : `vault operator unseal`
   
   1. Wait for about 10 mins for the containers to get back to work. 
