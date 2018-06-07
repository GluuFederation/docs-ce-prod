# FAQ

We'll continue to add FAQs as they arise. Feel free to help us by forking these docs and submitting a merge request! 

## On which network is Gluu Server DE running?

    For the single-host example, `run_all.sh` script executes the `docker-compose up -d` command, where docker-compose creates a custom bridge network based on the name of your current directory. So, for example, the network would be named `dockergluuserver_bridge`. You can assign a custom network in the `docker-compose.yaml`. Please see [the Docker-compose official documentation](https://docs.docker.com/compose/networking/#specify-custom-networks) for further information.

    All other containers in the docker-compose file are connected to that same network as well. The only container not included in the `docker-compose.yaml` file is the `config-init`. We left them disconnected, as `config-init` shouldn't be daemonized to avoid rerunning the command when the container is restarted.
    As can be seen in the following `docker run` command, it connects to the same network as Consul with the `--network container:consul` option.

        docker run --rm \
            --network container:consul \
            gluufederation/config-init:3.1.3_dev \
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

    For the multi-host example, we're using native Docker Swarm `overlay` network, but slightly customized to allow connecting any container outside of the network. See the [Networking](./example.md#Networking) section for a multi-host example.
