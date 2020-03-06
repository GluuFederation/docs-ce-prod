# Docker Installation

## Overview
This guide provides instructions for deploying the Gluu Server on a single node VM using Docker.

## Prerequisites

For Docker deployments, provision a VM with:

### Linux users

- The minimum system requirements, as described in the [VM Preparation Guide](../installation-guide/index.md#system-requirements).

- [Docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-using-the-convenience-script) is installed

### Mac users

- The minimum system requirements for [Docker for Mac](https://docs.docker.com/docker-for-mac/install/)

- [Docker Desktop for Mac](https://hub.docker.com/editions/community/docker-ce-desktop-mac)

## Instructions

### Obtain files for deployment

```
wget https://github.com/GluuFederation/community-edition-containers/releases/download/v1.0.0/pygluu-compose.pyz
mv pygluu-compose.pyz pygluu-compose
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
| `oxpassport`        | `SVC_OXPASSPORT`       | no        | no     |
| `oxshibboleth`      | `SVC_OXSHIBBOLETH`     | no        | no     |
| `redis`             | `SVC_REDIS`            | no        | no      |
| `radius`            | `SVC_RADIUS`           | no        | no      |
| `vault` auto-unseal | `SVC_VAULT_AUTOUNSEAL` | no        | no      |
| `oxd_server`        | `SVC_OXD_SERVER`       | no        | no      |
| `key_rotation`      | `SVC_KEY_ROTATION`     | no        | no      |
| `cr_rotate`         | `SVC_CR_ROTATE`        | no        | no      |

To enable/disable non-mandatory services listed above, create a file called `settings.py` and set the value to `True` to enable or set to `False` to disable the service. For example:

```python
SVC_LDAP = True                 # will be enabled
SVC_OXPASSPORT = False          # will be disabled
SVC_VAULT_AUTOUNSEAL = True     # enable Vault auto-unseal with GCP KMS API
```

Any services not specified in `settings.py` will follow the default settings.

To override manifests (i.e. changing oxAuth service definition), add `ENABLE_OVERRIDE=yes` in `settings.sh`, for example:

```python
ENABLE_OVERRIDE = True
```

Then define overrides in `docker-compose.override.yml` (create the file if not exists):

```yaml
version: "2.4"

services:
  oxauth:
    container_name: my-oxauth
```

If `docker-compose.override.yml` exists, this file will be added as the last Compose file. For reference on multiple Compose file, please take a look at [https://docs.docker.com/compose/extends/#multiple-compose-files](https://docs.docker.com/compose/extends/#multiple-compose-files).

### Choose persistence backends

Supported backends are LDAP, Couchbase, or mix of both (hybrid). The following config control which persistence backend is selected:

- `PERSISTENCE_TYPE`: choose one of `ldap`, `couchbase`, or `hybrid` (the default is `ldap`)
- `PERSISTENCE_LDAP_MAPPING`: choose one of `default`, `user`, `site`, `cache`, or `token` (default to `default`)

To choose a persistence backend, create a file called `settings.py` (if it wasn't created in the last step) and set the corresponding option as seen above. For example:

```python
PERSISTENCE_TYPE = "couchbase"      # Couchbase will be selected
PERSISTENCE_LDAP_MAPPING = "user"   # store user mapping in LDAP
COUCHBASE_USER = "admin"            # Couchbase user
COUCHBASE_URL = "192.168.100.4"     # Host or IP address of Couchbase
```

If `couchbase` or `hybrid` is selected, there are 2 additional steps required to satisfy dependencies:

- put Couchbase cluster certificate into the `couchbase.crt` file
- put Couchbase password into the `couchbase_password` file
- the Couchbase cluster must have `data`, `index`, and `query` services at minimum

### Set up Vault auto-unseal

In this example, Google Cloud Platform (GCP) KMS is used to automatically unseal Vault. The following is an example of how to obtain [GCP KMS credentials](https://shadow-soft.com/vault-auto-unseal/) JSON file, and save it as `gcp_kms_creds.json` in the same directory where `run_all.sh` is located:

```json
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


Run the following command to install the Gluu Server:

```sh
./pygluu-compose up
```

The startup process may take some time. You can keep track of the deployment by using the following command:

```sh
./pygluu-compose logs -f
```

On initial deployment, since Vault has not been configured yet, the `run_all.sh` will generate a root token and key to interact with Vault API, saved as `vault_key_token.txt`. Secure this file, as it contains the recovery key and root token.

### Uninstall the Gluu Server

Run the following command to delete all objects during the deployment:

```sh
./pygluu-compose down
```

## FAQ

### **How to use ldapsearch**

```sh
docker exec -ti ldap /opt/opendj/bin/ldapsearch \
    -h localhost \
    -p 1636 \
    -Z \
    -X \
    -D "cn=directory manager" \
    -b "o=gluu" \
    -s base \
    -T "objectClass=*"
```

### **Locked out of your Gluu deployment? This is how Vault can be manually unlocked**

1. Get Unseal key from `vault_key_token.txt`

1. Log in to the Vault container: `docker exec -it vault sh`

1. Run this command : `vault operator unseal`

1. Wait for about 10 mins for the containers to get back to work.
