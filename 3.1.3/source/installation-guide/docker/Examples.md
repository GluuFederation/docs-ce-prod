# Examples

### Single Host using Docker

This in an example of running Gluu Server Docker edition on a single VM.

(Here)[https://github.com/GluuFederation/gluu-docker/tree/master/examples/single-host] are the instructions on how to deploy a stand-alone instance with a bash script.

What follows is a thorough explanation of the process we used to make launching a stand-alone instance repeatable, modular and consistent. Adjustments can be made on your part.

#### run_all.sh

The core concept of this script is to intake some necessary information from the user on initial start up

- CONFIG_DIR=$PWD/volumes/config-init/db: used to identify the location of the persistence volumes you would like to store the `config.json` file. This location can be changed before first creating your configuration, but if changed after, the script won't be able to load up the previous configuration. Further explanation of the importance of the `config.json` file can be found in the [Technical Documentation](/path/to/technical/docs).

- HOST_IP=$(ip route get 1 | awk '{print $NF;exit}'): This variable automatically pulls the current host IP address. This variable along with DOMAIN variable are used to populate the `/etc/hosts` file of the oxTrust container. This is necessary due to the fact that oxTrust must be able to discover oxAuth's `/.well-known/openid-configuration` to be properly configured. For that reason, NGINX, which is bound on the host networks eth0 in this example, will route oxTrust to the proper location `https://$DOMAIN/.well-known/openid-configuration`.

- GLUU_VERSION=<version>: In the script, this is used to identify which version of `config-init` to run. This must match the version of Gluu Server you're trying to deploy.

- INIT_CONFIG_CMD="": Used to either run the `gluufederation/config-init:<version> generate` configuration command if no previous `config.json` is found in `CONFIG_DIR`, or prompt the user if they want to deploy with the current `config.json` file.

- The following are used for certificates, with the exception of `DOMAIN` which is also used to modify the `/etc/hosts` file of the oxTrust container and `ADMIN_PW` which will be the password for oxTrust and LDAP:

    - DOMAIN=""
    - ADMIN_PW=""
    - EMAIL=""
    - ORG_NAME=""
    - COUNTRY_CODE=""
    - STATE=""
    - CITY=""

- load_services(): 

    - This loads all the services in the docker-compose file. Note that config-init is run as a separate command.

- prepare_config():
    
    - This will check that consul is up. If it is, it will look in it's KV store for the DOMAIN we've entered before. If it

##### FAQ:

1) What network is Gluu Server Docker Edition running on?

    In this script, it launches consul using the `docker-compose up consul` command, where docker-compose creates a custom bridge network, based on the name of your current directory. So, for example, the network would be named `dockergluuserver_bridge`. You can assign a custom network in the `docker-compose.yaml`. Please see [the Docker-compose official documentation](https://docs.docker.com/compose/networking/#specify-custom-networks) for further understanding.
    
    All other containers in the docker-compose file are connected to that same network as well. The only container not included in the `docker-compose.yaml` file is the `config-init`. We left them disconnected as it must finish loading the necessary configuration files into consul before any other container can launch. As can be seen in the following `docker run` command, it connects to the same network as consul with the `--network container:consul` option. 
    
        docker run --rm \
            --network container:consul \
            gluufederation/config-init:3.1.2_dev \
            generate \
            --kv-host "${GLUU_KV_HOST}" \
            --ldap-type "${GLUU_LDAP_TYPE}" \
            --domain $domain \
            --admin-pw $adminPw \
            --org-name "$orgName" \
            --email $email \
            --country-code $countryCode \
            --state $state \
            --city $city

    - Note this command is to create the initial configuration and is slightly different than the `load` or `dump` option of config-init. Please see [the API](/path/to/config-init/API/docs) for more information.
 
1) What is the launch process for the containers?
 
    There are a couple containers which have to be launched first to successfully launch the dependent Gluu Server containers.
    
    Firstly, [consul](https://www.consul.io/), which is our key value store, as well as service discovery container.
    
    Secondly, [config-init](https://github.com/GluuFederation/docker-config-init/tree/3.1.2), which will load all of the necessary keys, configuration settings, templates and other requirements, into consul. This container will run to completion and then exit and remove itself. All services hereinafter will use consul to pull their necessary configuration.
    
    Next is our OpenDJ container. OpenDJ will install and configure itself inside the container as well as create volumes inside of the current directory as `/volumes/` for necessary persistent data, like db, schema, etc..
    
    After that oxAuth, NGINX, then oxTrust, which relies on the `/.well-known/openid-configuration/` to properly set it's own configuration. These containers can be restarted at any time from that point on.
    
    Currently all of the images, with the exception of the `config-init` and hashicorp `consul` container, have wait-for-it scripts designed to prevent them from trying to start, before the necessary launch procedure is accomplished. This mitigates failure during the build process.


### Multi Host using Docker Swarm

https://github.com/GluuFederation/gluu-docker/tree/master/examples/multi-hosts
