# Technical Documentation

### Build Logic

#### Operating System

- Size was a major consideration in the base Docker image we used for our containers. Because of that, we use Alpine Linux which comes in at a whopping 5 MB by default. Based on comparisons between other base images, we've roughly saved 50-70% of space utilizing Alpine. The average size of each of our containers is about 269 MB due to dependencies.

#### Consul

- The Gluu Server Docker containers were built to be centralized around a configuration KV store. For our use case, we've used [Consul](https://www.consul.io/) as our KV store. The reasoning behind this decision was to allow the containers to be as modular as possible. Services can be replaced without concern for losing any of the default configuration. This isn't to say that there won't need to be persistence using volumes (see [here](https://github.com/GluuFederation/gluu-docker/blob/master/examples/single-host/docker-compose.yml#L42) and [here](https://github.com/GluuFederation/gluu-docker/blob/master/examples/single-host/docker-compose.yml#L55)) for custom files and long standing data requirements.

- That being said, Consul stores all it's configuration in-memory. This is remedied by saving all configuration with a `dump` which will write to a JSON file titled `config.json` for ease of access. You can then reinitialize the configuration in the event of the previous consul container failing by using the `load` command. Please see [the documentation](#variable-explanation) below on how to achieve this.

#### Startup

- Docker containers generally have entrypoint scripts to prepare templates, configure files, run services, etc. Anything you need to run to properly initialize a container and run the process. For our containers, this where we pull most of our files and certificates from Consul. 

- Because there is a heirarchy of function to Gluu Server, wait-for-it scripts were designed, thanks to contributions from Torstein Krause Johansen (@skybert), to try and make sure the containers don't begin their launch processes until the services superior to the container are fully started. However, there is a time limit, so a container dependent upon another container could fail as the wait-for-it "health checks" aren't being met.

#### oxShibboleth

- Mounting the volume from host to container, as seen in the `-v $PWD/shared-shibboleth-idp:/opt/shared-shibboleth-idp` option, is required to ensure oxShibboleth can load the configuration correctly. This can [also be seen here](https://github.com/GluuFederation/gluu-docker/blob/master/examples/single-host/docker-compose.yml#L90) in the standalone docker-compose yaml file or [here](https://github.com/GluuFederation/gluu-docker/blob/master/examples/multi-hosts/web.yml#L88) in the multi-host docker-compose yaml file.

- By design, each time a Trust Relationship entry is added/updated/deleted via the oxTrust GUI, some Shibboleth-related files will be generated/modified by oxTrust and saved to `/opt/shibboleth-idp` directory inside the oxTrust container. A background job in oxTrust container ensures those files are copied to `/opt/shared-shibboleth-idp` directory (also inside the oxTrust container, which must be mounted from container to host).

- After those Shibboleth-related files are copied to `/opt/shared-shibboleth`, a background job in oxShibboleth copies them to the `/opt/shibboleth-idp` directory inside oxShibboleth container. To ensure files are synchronized between oxTrust and oxShibboleth, both containers must use a same mounted volume `/opt/shared-shibboleth-idp`.

- The `/opt/shibboleth-idp` directory is not mounted directly into the container, as there are two known issues with this approach. First, oxShibboleth container has its own default `/opt/shibboleth-idp` directory requirements to start the app itself. By mounting `/opt/shibboleth-idp` directly from the host, the directory will be replaced and the oxShibboleth app won't run correctly. Secondly, oxTrust renames the metadata file, which unfortunately didn't work as expected in the mounted volume.

#### oxPassport

- A blurb about how to add new strategies to Passport.
    
### Networking Considerations

- By default, the Gluu Server Java applications deploy inside their containers on port 8080. You'll need to be mask them appropriately to 8081 (oxauth), 8082(oxtrust), 8086(oxshibboleth) if you are using the host network. If you're using a docker virtual network, this mapping isn't required.

- oxTrust is an OpenID Connect client so its container is dependent upon oxAuth's `/.well-known/openid-configuration` endpoint, which is only accessible if NGINX is started. So if the oxTrust container cannot navigate to `https://<hostname>/.well-known/openid-configuration`, it will fail to finish initialization. The container will most likely not exit.

### Variable Explanation

For examples of these environment variables in practice, please refer to the [examples documentation](./examples.md) for docker-compose files and scripts, or [the basic wiki](https://github.com/GluuFederation/gluu-docker/wiki/Simple-Docker-Deployment) for docker run commands.

- config-init

    - API:

        - generate: The generate command will generate all the initial configuration files for the Gluu Server components. The following are required to launch:
            
            - --email: The email address of the administrator usually. Used for certificate creation.
            - --domain: The domain name where the Gluu Server resides. Used for certificate creation.
            - --country-code: The country where the organization is located. User for certificate creation.
            - --state: The state where the organization is located. Used for certificate creation.
            - --city: The city where the organization is located. Used for certificate creation.
            - --org-name: The organization using the Gluu Server. Used for certificate creation.
            - --kv-host: The IP address or hostname of the KV store (Consul). Default is localhost.
            - --kv-port: The port used to access consul. Default is 8500.
            - --admin-pw: The administrator password for oxTrust and LDAP
            - --ldap-type: Either OpenDJ or OpenLDAP. If you're looking to use LDAP replication, we recommend OpenDJ.

        - dump: The dump command will dump all the configuration from inside Consul's KV store into stdout as well as `/opt/config-init/db/config.json` inside the container. The following is required to launch:

            - --kv-host: The IP address or hostname of the KV store (Consul). Default is localhost.
            - --kv-port: The port used to access Consul. Default is 8500.

            Optional:

            - --path: Absolute path to JSON file inside the container. Default is `/opt/config-init/db/config.json`.

                - Please note that to access this file from the host, you'll either need to map a mounted volume to the `--path` directory or pipe the stdout to a file. For example:

                        docker run \
                        --rm \
                        --network container:consul \
                        gluufederation/config-init:$GLUU_VERSION \
                        dump \
                        --kv-host <consul address> > /where/you/want/to/save/config.json

                - Be aware if you're using rkt, that it will not output to stdout directly, so piping to a file will not work properly. You'll have to use the volume mapping method.
                
                        rkt run \
                        --insecure-options=image \
                        --volume volume-consul-config,kind=host,source=/path/to/host/volume,readOnly=false \
                        --mount volume=volume-consul-config,target=/opt/config-init/db/ \
                        docker://gluufederation/config-init:3.1.2_dev \
                        --"exec=python" \
                        -- entrypoint.py dump \
                        --kv-host=<consul address>
                
                - Your configuration file will be inside wherever you mapped the `/path/to/host/volume` directory.

        - load: The load command will load a `config.json` into the Consul KV store. The following are required to launch:
        
            - --kv-host: The IP address or hostname of the KV store (Consul). Default is localhost.
            - --kv-port: The port used to access Consul. Default is 8500.

            Optional:

            - --path: Absolute path to JSON file inside the container. Default is `/opt/config-init/db/config.json`

                - Please note that to load this file from the host, you'll need to place your `config.json` in a mounted volume that links to the `--path` directory. [Example](https://github.com/GluuFederation/gluu-docker/blob/master/examples/single-host/run_all.sh#L81) or:
                    
                        docker run --rm \
                        -v /path/to/config/:/opt/config-init/db/ \
                        gluufederation/config-init:3.1.2_dev \
                        load \
                        --kv-host <consul address>

- OpenDJ

    -

- oxAuth

    - GLUU_LDAP_URL: The IP address or hostname of the LDAP database. Default is localhost:1636. Multiple URLs can be used using comma-separated values (i.e. 192.168.100.1:1636,192.168.100.2:1636).
    - GLUU_KV_HOST: The IP address or hostname of the KV store (Consul). Default is localhost. 
    - GLUU_KV_PORT: The port used to access Consul. Default is 8500.
    - GLUU_MAX_RAM_FRACTION: Used in conjunction with Docker memory limitations (docker run -m <mem>) to identify the fraction of the maximum amount of heap memory you want the JVM to use.
    - GLUU_CUSTOM_OXAUTH_URL: URL to downloadable custom oxAuth files packed using .tar.gz format. Please see the [Gluu documentation](https://www.gluu.org/docs/ce/operation/custom-design/) on how to configure this.

- oxTrust

    - GLUU_LDAP_URL: The IP address or hostname of the LDAP database. Default is localhost:1636. Multiple URLs can be used using comma-separated values (i.e. 192.168.100.1:1636,192.168.100.2:1636).
    - GLUU_KV_HOST: The IP address or hostname of the KV store (Consul). Default is localhost. 
    - GLUU_KV_PORT: The port used to access Consul. Default is 8500.
    - GLUU_MAX_RAM_FRACTION: Used in conjunction with Docker memory limitations (docker run -m <mem>) to identify the fraction of the maximum amount of heap memory you want the JVM to use.
    - GLUU_CUSTOM_OXTRUST_URL: URL to downloadable custom oxTrust files packed using .tar.gz format. Please see the [Gluu documentation](https://gluu.org/docs/ce/operation/custom-design/) on how to configure this. Please be aware that you have to

- oxPassport

    - GLUU_KV_HOST: The IP address or hostname of the KV store (Consul). Default is localhost. 
    - GLUU_KV_PORT: The port used to access Consul. Default is 8500.
    - GLUU_LDAP_URL: The IP address or hostname of the LDAP database. Default is localhost:1636. Multiple URLs can be used using comma-separated values (i.e. 192.168.100.1:1636,192.168.100.2:1636).

- oxShibboleth

    - GLUU_KV_HOST: The IP address or hostname of the KV store (Consul). Default is localhost. 
    - GLUU_KV_PORT: The port used to access Consul. Default is 8500.
    - GLUU_MAX_RAM_FRACTION: Used in conjunction with Docker memory limitations (docker run -m <mem>) to identify the fraction of the maximum amount of heap memory you want the JVM to use.
    - GLUU_LDAP_URL: The IP address or hostname of the LDAP database. Default is localhost:1636. Multiple URLs can be used using comma-separated values (i.e. 192.168.100.1:1636,192.168.100.2:1636).

- NGINX

    - GLUU_KV_HOST: The IP address or hostname of the KV store (Consul). Default is localhost. 
    - GLUU_KV_PORT: The port used to access Consul. Default is 8500.
    - GLUU_OXAUTH_BACKEND: Host and port of oxAuth backend, i.e. oxauth.domain.com:8081. Multiple backends are supported (separate each backend with comma character, i.e. oxauth1.domain.com:8081,oxauth2.domain.com:8081).
    - GLUU_OXTRUST_BACKEND: Host and port of oxTrust backend, i.e. oxtrust.domain.com:8082. Multiple backends are supported (separate each backend with comma character, i.e. oxtrust1.domain.com:8082,oxtrust2.domain.com:8082).
    - GLUU_OXSHIBBOLETH_BACKEND: Host and port of oxTrust backend, i.e. oxtrust.domain.com:8086.
    - GLUU_OXPASSPORT_BACKEND: Host and port of oxTrust backend, i.e. oxtrust.domain.com:8090.
