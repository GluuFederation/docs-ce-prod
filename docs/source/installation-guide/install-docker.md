# Docker Installation

## Overview
This guide provides instructions for deploying the Gluu Server on a single node VM using Docker.

## Prerequisites

For Docker deployments, provision a VM with: 

- The minimum system requirements, as described in the [VM Preparation Guide](../installation-guide/index.md#system-requirements). 

- Both [Docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-using-the-convenience-script) and [Docker Compose](https://docs.docker.com/compose/install/#install-compose) installed. 

## Instructions

### Obtain files for deployment:

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

### Choose services

The following services are available during deployment:

| Service             | Setting Name           | Mandatory | Enabled by default|
| ------------------- | ---------------------- | --------- | ------- |
| `consul`            | -                      | yes       | always  |
| `registrator`       | -                      | yes       | always  |
| `vault`             | -                      | yes       | always  |
| `nginx`             | -                      | yes       | always  |
| `oxauth`            | `SVC_OXAUTH`           | no        | yes     |
| `oxtrust`           | `SVC_OXTRUST`          | no        | yes     |
| `ldap`              | `SVC_LDAP`             | no        | yes     |
| `oxpassport`        | `SVC_OXPASSPORT`       | no        | yes     |
| `oxshibboleth`      | `SVC_OXSHIBBOLETH`     | no        | yes     |
| `redis`             | `SVC_REDIS`            | no        | no      |
| `radius`            | `SVC_RADIUS`           | no        | no      |
| `vault` auto-unseal | `SVC_VAULT_AUTOUNSEAL` | no        | no      |
| `oxd_server`        | `SVC_OXD_SERVER`       | no        | no      |
| `key_rotation`      | `SVC_KEY_ROTATION`     | no        | no      |
| `cr_rotate`         | `SVC_CR_ROTATE`        | no        | no      |

To enable/disable non-mandatory services listed above, create a file called `settings.sh` and set the value to `"yes"` to enable or set to any other value to disable the service. For example:

```
SVC_LDAP="yes"              # will be enabled
SVC_OXPASSPORT="no"         # will be disabled
SVC_OXSHIBBOLETH=""         # will be disabled
SVC_VAULT_AUTOUNSEAL="yes"  # enable Vault auto-unseal with GCP KMS API
```

Any services not specified in `settings.sh` will follow the default settings.

If `docker-compose.override.yml` exists, this file will be added as the last Compose file. For reference on multiple Compose file, please take a look at https://docs.docker.com/compose/extends/#multiple-compose-files.

### Choose persistence backends

The following persistence backends are supported:

- `PERSISTENCE_TYPE`: choose one of `ldap`, `couchbase`, or `hybrid` (the default is `ldap`)

- **If using a hybrid PERSISTENCE_TYPE:** `PERSISTENCE_LDAP_MAPPING`: choose one of `default`, `user`, `site`, `statistic`, `cache`, `authorization`, `token`, or `client` (default to `default`)

To choose a persistence backend, create a file called `settings.sh` (if it wasn't created in the last step) and set the corresponding option as seen above. For example:

```
PERSISTENCE_TYPE="couchbase"    # Couchbase will be selected
PERSISTENCE_LDAP_MAPPING="user" # store user mapping in LDAP
COUCBASE_USER="admin"           # Couchbase user
COUCHBASE_URL="192.168.100.4"   # Host or IP address of Couchbase
```

If `couchbase` or `hybrid` is selected, there are 2 additional steps required to satisfy dependencies:

- put Couchbase cluster certificate into the `couchbase.crt` file
- put Couchbase password into the `couchbase_password` file

### Set up Vault auto-unseal

In this example, Google Cloud Platform (GCP) KMS is used to automatically unseal Vault. The following is an example of how to obtain [GCP KMS credentials](https://shadow-soft.com/vault-auto-unseal/) JSON file, and save it as `gcp_kms_creds.json` in the same directory where `run_all.sh` is located:

```
{
    "type": "service_account",
    "project_id": "project",
    "private_key_id": "1234abcd",
    "private_key": "-----BEGIN PRIVATE KEY-----\nabcdEFGH==\n-----END PRIVATE KEY-----\n",
    "client_email": "sa@project.iam.gserviceaccount.com",
    "client_id": "1234567890",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/sa%40project.iam.gserviceaccount.com"
}
```

Then, create `gcp_kms_stanza.hcl` in the same directory where `run_all.sh` is located. For example:

```
seal "gcpckms" {
    credentials = "/vault/config/creds.json"
    project     = "<PROJECT_NAME>"
    region      = "<REGION_NAME>"
    key_ring    = "<KEYRING_NAME>"
    crypto_key  = "<KEY_NAME>"
}
```
### Deploy the Gluu Server    

    
Run the following script to install the Gluu Server:

```
./run_all.sh
```
    
Do not be alarmed by any `warning` alerts that may show up unless the script fails. Wait until it prompts you for information or loads the previous configuration found. If this is a fresh install, you may see something like this:
  
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
    
On initial deployment, since Vault has not been configured yet, the `run_all.sh` will generate a root token and key to interact with Vault API, saved as `vault_key_token.txt`. Secure this file, as it contains the recovery key and root token.

## Uninstalling the Gluu Server

Run the following command to delete all objects during the deployment:

```
./run_all.sh down
```

## FAQ

- **How to use ldapsearch**

```
docker exec -ti ldap /opt/opendj/bin/ldapsearch -h localhost -p 1636 -Z -X -D "cn=directory manager" -b "o=gluu" -s base -T "objectClass=*"
```

- **Locked out of your Gluu deployment? This is how Vault can be manually unlocked**

   1. Get Unseal key from `vault_key_token.txt`
   
   1. Log in to the Vault container: `docker exec -it vault sh`
   
   1. Run this command : `vault operator unseal`
   
   1. Wait for about 10 mins for the containers to get back to work. 

## Documentation

Please refer to the [Gluu Server Docker Edition Documentation](https://gluu.org/docs/de/4.0.0) for further reading on Docker image implementations.
