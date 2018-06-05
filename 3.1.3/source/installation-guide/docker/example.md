# Examples

### Single Host using Docker

This an example of running Gluu Server Docker edition on a single VM.

[Here](https://github.com/GluuFederation/gluu-docker/tree/master/examples/single-host) are the instructions to deploy a stand-alone instance with a bash script named `run_all.sh`.
The core concept of this script is to intake some necessary information from the user on initial startup and deploy the containers.

What follows is a thorough explanation of the process we used to make launching a stand-alone instance repeatable, modular and consistent. Adjust the process as needed.

#### Variables

- `CONFIG_DIR=$PWD/volumes/config-init/db`: used to identify the location of the persistence volumes you would like to store the `config.json` file. This location can be changed before first creating your configuration, but if changed after, the script won't be able to load up the previous configuration.

- `HOST_IP=$(ip route get 1 | awk '{print $NF;exit}')`: This variable automatically pulls the current host IP address. This variable, along with `DOMAIN` variable, are used to populate the `/etc/hosts` file of the oxTrust container. This is necessary due to the fact that oxTrust must be able to discover oxAuth's `/.well-known/openid-configuration` to be properly configured. For that reason, NGINX, which is bound on the host network's `eth0` interface in this example, will route oxTrust to the proper location `https://$DOMAIN/.well-known/openid-configuration`.

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

- `prepare_config`: checks config in Consul KV. If it can't find the required config, this function will load configuration from existing `config.json` (see `load_config` function below), otherwise users will be prompted to enter required configuration (see `generate_config` below).

- `load_config`: loads config from a JSON file (`config.json`) stored under `CONFIG_DIR` directory.

- `generate_config`: creates initial configuration and dump saved config into `config.json` stored under `CONFIG_DIR` directory.

### Multi Host using Docker Swarm

https://github.com/GluuFederation/gluu-docker/tree/master/examples/multi-hosts
