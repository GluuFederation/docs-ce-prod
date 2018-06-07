# Examples

### Single Host using Docker

This an example of running Gluu Server Docker Edition (DE) on a single VM.

[Here](https://github.com/GluuFederation/gluu-docker/tree/3.1.3/examples/single-host) are the instructions to deploy a stand-alone instance with a bash script named `run_all.sh`.
The core concept of this script is to intake some necessary information from the user on initial startup and deploy the containers.

What follows is a thorough explanation of the process we used to make launching a stand-alone instance repeatable, modular and consistent. Adjust the process as needed.

#### Variables

- `CONFIG_DIR=$PWD/volumes/config-init/db`: used to identify the location of the persistence volumes you would like to store the `config.json` file. This location can be changed before first creating your configuration, but if changed after, the script won't be able to load up the previous configuration.

- `HOST_IP=$(ip route get 1 | awk '{print $NF;exit}')`: This variable automatically pulls the current host IP address. This variable, along with `DOMAIN` variable, are used to populate the `/etc/hosts` file of the oxTrust container. This is necessary due to the fact that oxTrust must be able to discover oxAuth's `/.well-known/openid-configuration` to be properly configured. For that reason, NGINX, which is bound on the host network's `eth0` interface in this example, will route oxTrust to the proper location, `https://$DOMAIN/.well-known/openid-configuration`.

- `GLUU_VERSION=<version>`: In the script, this is used to identify which version of `config-init` to run. This must match the version of Gluu Server you're trying to deploy.

- `INIT_CONFIG_CMD=""`: Used to either run the `gluufederation/config-init:<version> generate` configuration command if no previous `config.json` is found in `CONFIG_DIR`, or prompt the user if they want to deploy with the current `config.json` file.

- The following are used for certificates, with the exception of `DOMAIN`, which is also used to modify the `/etc/hosts` file of the oxTrust container, and `ADMIN_PW`, which will be the password for oxTrust and LDAP:

    - `DOMAIN=""`
    - `ADMIN_PW=""`
    - `EMAIL=""`
    - `ORG_NAME=""`
    - `COUNTRY_CODE=""`
    - `STATE=""`
    - `CITY=""`

#### Functions

- `load_services`: deploys all the services in the docker-compose file. Note that `config-init` is run as a separate command.

- `prepare_config`: checks config in Consul KV. If it can't find the required config, this function will load configuration from an existing `config.json` (see `load_config` function below), otherwise users will be prompted to enter the required configuration (see `generate_config` below).

- `load_config`: loads config from a JSON file (`config.json`) stored under `CONFIG_DIR` directory.

- `generate_config`: creates initial configuration and dump saved config into `config.json` stored under `CONFIG_DIR` directory.

### Multi Host using Docker Swarm Mode

This an example of running Gluu Server Docker edition on multiple VMs using Docker Swarm Mode.

[Here](https://github.com/GluuFederation/gluu-docker/tree/3.1.3/examples/multi-hosts) are the instructions to deploy a clustered instances of Gluu Server Docker containers.
This example consists of several shell scripts, and config files (including docker-compose files).

What follows is an explanation of the process we used to deploy clustered Gluu Server Docker containers.

#### Node

As this example uses Docker Swarm Mode, the node refers to a Docker Swarm node (either `manager` or `worker`), basically a host/server.
For simplicity, the clustered Gluu Server is distributed into 3 nodes (called `manager`, `worker-1`, and `worker-2`), with each node has full stack of containers (Consul, Registrator, Redis, Twemproxy, OpenDJ, oxAuth, oxTrust, oxPassport, oxShibboleth, and NGINX).
Given this topology, the Gluu Server still able to serve the request even when one of the nodes is down.
Another interesting case is by using 3 nodes, the possibility of having [issue](https://github.com/GluuFederation/gluu-docker/issues/34) with Consul is minimized.

#### Networking

The cluster operates over native Docker Swarm networking called `overlay`.
To allow container that is running using plain `docker run` command to connect to the network, a custom network called `gluu` is created (based on `overlay` with `--attachable` option).

By having this custom network, we can address our concerns:

- any container that doesn't execute long-running process (e.g. `config-init`) able to access Consul container inside the network
- deploy container that requires fixed IP address/hostname (for example: LDAP replication), but can be reached by other containers inside the network

#### Shared Volume Between Nodes

oxTrust and oxShibboleth rely on mounted volume to share oxShibboleth configuration files. Given there are 3 nodes that need to share same copy of oxShibboleth files, [csync2](http://oss.linbit.com/csync2/) is used. Note, `csync2` is installed as node's OS package, not a container version. The `csync2` setup is executed when running `nodes.sh` script (see section below).

#### Scripts

- `nodes.sh`: provision Swarm nodes and setup `csync2` replication
- `config.sh`: generate, dump, or load configuration required by the cluster
- `cache.sh`: deploy Redis and Twemproxy as cache storage
- `ldap-manager.sh`: deploy OpenDJ including creating initial data
- `ldap-worker-1.sh`: deploy OpenDJ that replicate the data from another OpenDJ container
- `ldap-worker-2.sh`: deploy OpenDJ that replicate the data from another OpenDJ container

#### Docker Compose Files

- `cache.yml`: contains Docker Swarm service definition for Twemproxy container
- `registrator.yml`: contains Docker Swarm service definition for Registrator container
- `consul.yml`: contains Docker Swarm service definition for Consul container
- `web.yml`: contains Docker Swarm service definition for oxAuth, oxTrust, oxShibboleth, oxPassport, and NGINX container

#### Load Balancer

Given 3 nodes that run clustered Gluu Server, it's recommended to deploy external loadbalancer, for example: NGINX or [DigitalOcean loadbalancer](https://www.digitalocean.com/products/load-balancer/).
Note, the process of deploying an external loadbalancer is out of the scope of this document.
