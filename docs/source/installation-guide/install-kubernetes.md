# The Kubernetes recipes

1.  If deploying on the cloud make sure to take a look at the cloud specific notes before continuing.

    * [Amazon Web Services (AWS) - EKS](#amazon-web-services-aws---eks)
    * [GCE (Google Cloud Engine) - GKE](#gce-google-cloud-engine---gke)
    * [Azure - AKS](#azure---aks) ![CDNJS](https://img.shields.io/badge/status-pending-yellow.svg)

    If deploying locally make sure to take a look at the specific notes bellow before continuing.
    
      * [Minikube](#minikube)
      * [MicroK8s](#microk8s)

1. Install using one of the following :

     * [Kustomize](#install-gluu-using-pygluu-kubernetes-with-kustomize)
     * [Helm](#install-gluu-using-helm)
     
# Amazon Web Services (AWS) - EKS
  
## Setup Cluster

-  Follow this [guide](https://docs.aws.amazon.com/eks/latest/userguide/getting-started.html)
 to install a cluster with worker nodes. Please make sure that you have all the `IAM` policies for the AWS user that will be creating the cluster and volumes.

## Requirements

-   The above guide should also walk you through installing `kubectl` , `aws-iam-authenticator` and `aws cli` on the VM you will be managing your cluster and nodes from. Check to make sure.

        aws-iam-authenticator help
        aws-cli
        kubectl version

> **_NOTE:_**  ![CDNJS](https://img.shields.io/badge/CLB--green.svg) Following any AWS deployment will install a classic load balancer with an `IP` that is not static. Don't worry about the `IP` changing. All pods will be updated automatically with our script when a change in the `IP` of the load balancer occurs. However, when deploying in production, **DO NOT** use our script. Instead, assign a CNAME record for the LoadBalancer DNS name, or use Amazon Route 53 to create a hosted zone. More details in this [AWS guide](https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/using-domain-names-with-elb.html?icmpid=docs_elb_console).

## EFS notes

1. EFS is created

1. EFS must be inside the same region as the EKS cluster

1. VPC of EKS and EFS are the same

1. Security group of EFS allows all connections from the EKS nodes
  
# GCE (Google Cloud Engine) - GKE

## Setup Cluster

1.  Install [gcloud](https://cloud.google.com/sdk/docs/quickstarts)

1.  Install kubectl using `gcloud components install kubectl` command

1.  Create cluster:

        gcloud container clusters create CLUSTER_NAME --zone ZONE_NAME

    where `CLUSTER_NAME` is the name you choose for the cluster and `ZONE_NAME` is the name of [zone](https://cloud.google.com/compute/docs/regions-zones/) where the cluster resources live in.

1.  Configure `kubectl` to use the cluster:

        gcloud container clusters get-credentials CLUSTER_NAME --zone ZONE_NAME

    where `CLUSTER_NAME` is the name you choose for the cluster and `ZONE_NAME` is the name of [zone](https://cloud.google.com/compute/docs/regions-zones/) where the cluster resources live in.

    Afterwards run `kubectl cluster-info` to check whether `kubectl` is ready to interact with the cluster.
    
1.  If a connection is not made to google consul using google account the call to the api will fail. Either connect to google consul using an associated google account and run any `kubectl` command like `kubectl get pod` or create a service account using a json key [file](https://cloud.google.com/docs/authentication/getting-started).


# Azure - AKS
![CDNJS](https://img.shields.io/badge/status-pending-yellow.svg)

## Requirements

-  Follow this [guide](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest) to install Azure CLI on the VM that will be managing the cluster and nodes. Check to make sure.

-  Follow this [section](https://docs.microsoft.com/en-us/azure/aks/kubernetes-walkthrough#create-a-resource-group) to create the resource group for the AKS setup.

-  Follow this [section](https://docs.microsoft.com/en-us/azure/aks/kubernetes-walkthrough#create-aks-cluster) to create the AKS cluster

-  Follow this [section](https://docs.microsoft.com/en-us/azure/aks/kubernetes-walkthrough#connect-to-the-cluster) to connect to the AKS cluster

# Minikube

## Requirements

1. Install [minikube](https://github.com/kubernetes/minikube/releases).

1. Install [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/).

1. Create cluster:

    ```bash
    minikube start
    ```
        
1. Configure `kubectl` to use the cluster:

        kubectl config use-context minikube
1. Enable ingress on minikube

    ```bash
    minikube addons enable ingress
    ```


# MicroK8s

## Requirements

1. Install [MicroK8s](https://microk8s.io/)

1. Make sure all ports are open for [microk8s](https://microk8s.io/docs/)

1. Enable `helm3`, `storage`, `ingress` and `dns`.

    ```bash
    sudo microk8s.enable helm3 storage ingress dns
    ```


# Install Gluu using `pygluu-kubernetes` with Kustomize

1. Download [`pygluu-kubernetes.pyz`](https://github.com/GluuFederation/enterprise-edition/releases). This package can be built [manually](https://github.com/GluuFederation/enterprise-edition/blob/4.1/README.md#build-pygluu-kubernetespyz-manually).

1. Run :

    ```bash
    ./pygluu-kubernetes.pyz install
    ```
    
 > **_NOTE:_**  Prompts will ask for the rest of the information needed. You may generate the manifests (yaml files) and continue to deployment or just generate the  manifests (yaml files) during the execution of `pygluu-kubernetes.pyz`. `pygluu-kubernetes.pyz` will output a file called `previous-settings.json` holding all the parameters and can be used for a non-interactive setup by changing its name to `settings.json`. More information about this file and the vars it holds is [below](#settingsjson-parameters-file-contents) but  please don't manually create this file as the script can generate it using [`pygluu-kubernetes.pyz generate-settings`](https://github.com/GluuFederation/enterprise-edition/releases). 

## `settings.json` parameters file contents

 > **_NOTE:_** Please generate this file using [`pygluu-kubernetes.pyz generate-settings`](https://github.com/GluuFederation/enterprise-edition/releases).

| Parameter                                       | Description                                                                      | Options                                                                                     |
| ----------------------------------------------- | -------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| `ACCEPT_GLUU_LICENSE`                           | Accept the [License](https://www.gluu.org/license/enterprise-edition/)           | `"Y"` or `"N"`                                                                              |
| `GLUU_VERSION`                                  | Gluu version to be installed                                                     | `"4.0"` or `"4.1"`                                                                              |
| `GLUU_HELM_RELEASE_NAME`                        | Gluu Helm release name                                                           | `"<name>"`                                                                                  |
| `NGINX_INGRESS_RELEASE_NAME`                    | Nginx Ingress release name                                                       | `"<name>"`                                                                                  |
| `NODES_IPS`                                     | List of kubernetes cluster node ips                                              | `["<ip>", "<ip2>", "<ip3>"]`                                                                |
| `NODES_ZONES`                                   | List of kubernetes cluster node zones                                            | `["<node1_zone>", "<node2_zone>", "<node3_zone>"]`                                          |
| `NODES_NAMES`                                   | List of kubernetes cluster node names                                            | `["<node1_name>", "<node2_name>", "<node3_name>"]`                                          |
| `NODE_SSH_KEY`                                  | nodes ssh key path location                                                      | `"<pathtosshkey>"`                                                                          |
| `HOST_EXT_IP`                                   | Minikube or Microk8s vm ip                                                       | `"<ip>"`                                                                                    |
| `VERIFY_EXT_IP`                                 | Verify the Minikube or Microk8s vm ip placed                                     | `"Y"` or `"N"`                                                                              |
| `AWS_LB_TYPE`                                   | AWS loadbalancer type                                                            | `""` , `"clb"` or `"nlb"`                                                                   |
| `USE_ARN`                                       | Use ssl provided from ACM AWS                                                    | `""`, `"Y"` or `"N"`                                                                        |
| `ARN_AWS_IAM`                                   | The arn string                                                                   | `""` or `"<arn:aws:acm:us-west-2:XXXXXXXX:certificate/XXXXXX-XXXXXXX-XXXXXXX-XXXXXXXX>"`    |
| `LB_ADD`                                        | AWS loadbalancer address                                                         | `"<loadbalancer_address>"`                                                                  |
| `DEPLOYMENT_ARCH`                               | Deployment architecture                                                          | `"microk8s"`, `"minikube"`, `"eks"`, `"gke"` or `"aks"`                                     |
| `PERSISTENCE_BACKEND`                           | Backend persistence type                                                         | `"ldap"`, `"couchbase"` or `"hybrid"`                                                       |
| `INSTALL_COUCHBASE`                             | Install couchbase                                                                | `"Y"` or `"N"`                                                                              |
| `COUCHBASE_NAMESPACE`                           | Couchbase namespace                                                              | `"<name>"`                                                                                  |
| `COUCHBASE_VOLUME_TYPE`                         | Persistence Volume type                                                          | `"io1"`,`"ps-ssd"`, `"Premium_LRS"`                                                         |
| `COUCHBASE_CLUSTER_NAME`                        | Couchbase cluster name                                                           | `"<name>"`                                                                                  |
| `COUCHBASE_FQDN`                                | Couchbase FQDN                                                                   | `""` or i.e `"<clustername>.<namespace>.gluu.org"`                                          |
| `COUCHBASE_URL`                                 | Couchbase internal address to the cluster                                        | `""` or i.e `"<clustername>.<namespace>.cluster.local"`                                     |
| `COUCHBASE_USER`                                | Couchbase username                                                               | `""` or i.e `"admin"`                                                                       |
| `COUCHBASE_CRT`                                 | Couchbase CA certification                                                       | `""` or i.e `<crt content not encoded>`                                                     |
| `COUCHBASE_CN`                                  | Couchbase certificate common name                                                | `""`                                                                                        |
| `COUCHBASE_SUBJECT_ALT_NAME`                    | Couchbase SAN                                                                    | `""` or i.e `"cb.gluu.org"`                                                                 |
| `COUCHBASE_CLUSTER_FILE_OVERRIDE`               | Override `couchbase-cluster.yaml` with a custom `couchbase-cluster.yaml`         | `"Y"` or `"N"`                                                                              |
| `COUCHBASE_USE_LOW_RESOURCES`                   | Use very low resources for Couchbase deployment. For demo purposes               | `"Y"` or `"N"`                                                                              |
| `COUCHBASE_DATA_NODES`                          | Number of Couchbase data nodes                                                   | `""` or i.e `"4"`                                                                           |
| `COUCHBASE_QUERY_NODES`                         | Number of Couchbase query nodes                                                  | `""` or i.e `"3"`                                                                           |
| `COUCHBASE_INDEX_NODES`                         | Number of Couchbase index nodes                                                  | `""` or i.e `"3"`                                                                           | 
| `COUCHBASE_SEARCH_EVENTING_ANALYTICS_NODES`     | Number of Couchbase search, eventing and analytics nodes                         | `""` or i.e `"2"`                                                                           |
| `COUCHBASE_GENERAL_STORAGE`                     | Couchbase general storage size                                                   | `""` or i.e `"2"`                                                                           |
| `COUCHBASE_DATA_STORAGE`                        | Couchbase data storage size                                                      | `""` or i.e `"5Gi"`                                                                         |
| `COUCHBASE_INDEX_STORAGE`                       | Couchbase index storage size                                                     | `""` or i.e `"5Gi"`                                                                         |
| `COUCHBASE_QUERY_STORAGE`                       | Couchbase query storage size                                                     | `""` or i.e `"5Gi"`                                                                         |
| `COUCHBASE_ANALYTICS_STORAGE`                   | Couchbase search, eventing and analytics storage size                            | `""` or i.e `"5Gi"`                                                                         |
| `NUMBER_OF_EXPECTED_USERS`                      | Number of expected users [couchbase-resource-calc-alpha]                         | `""` or i.e `"1000000"`                                                                     |
| `EXPECTED_TRANSACTIONS_PER_SEC`                 | Expected transactions per second [couchbase-resource-calc-alpha]                 | `""` or i.e `"2000"`                                                                        |
| `USING_CODE_FLOW`                               | If using code flow [couchbase-resource-calc-alpha]                               | `""`, `"Y"` or `"N"`                                                                        |
| `USING_SCIM_FLOW`                               | If using SCIM flow [couchbase-resource-calc-alpha]                               | `""`, `"Y"` or `"N"`                                                                        |
| `USING_RESOURCE_OWNER_PASSWORD_CRED_GRANT_FLOW` | If using password flow [couchbase-resource-calc-alpha]                           | `""`, `"Y"` or `"N"`                                                                        |
| `DEPLOY_MULTI_CLUSTER`                          | Deploying a Multi-cluster [alpha]                                                | `"Y"` or `"N"`                                                                              |
| `HYBRID_LDAP_HELD_DATA`                         | Type of data to be held in LDAP with a hybrid installation of couchbase and LDAP | `""`, `"default"`, `"user"`, `"site"`, `"cache"` or `"token"`                               |
| `LDAP_VOLUME`                                   | LDAP  Volume type                                                                | `""`, `"io1"`,`"ps-ssd"`, `"Premium_LRS"`                                                   |
| `LDAP_VOLUME_TYPE`                              | Volume type for LDAP persistence                                                 | [options](#ldap_volume_type-options)                                                        |
| `LDAP_STATIC_VOLUME_ID`                         | LDAP static volume id (AWS EKS)                                                  | `""` or `"<static-volume-id>"`                                                              |
| `LDAP_STATIC_DISK_URI`                          | LDAP static disk uri (GCE GKE or Azure)                                          | `""` or `"<disk-uri>"`                                                                      |
| `OXTRUST_OXSHIBBOLETH_SHARED_VOLUME_TYPE`       | LDAP  Volume type                                                                | `""`, `"io1"`,`"ps-ssd"`, `"Premium_LRS"`                                                   |
| `ACCEPT_EFS_NOTES`                              | Auto accept EFS [notes](#efs-notes)                                              |  `""` or `"Y"` or `"N"`                                                                     |
| `EFS_FILE_SYSTEM_ID`                            | EFS file system id                                                               | `""` or `<id>`                                                                              |
| `EFS_AWS_REGION`                                | EFS aws region                                                                   | `""`or `"<aws-region>"`                                                                     |
| `EFS_DNS`                                       | EFS DNS                                                                          | `""` or `"<efs-dns>"`                                                                       |
| `GLUU_CACHE_TYPE`                               | Cache type to be used                                                            | `"IN_MEMORY"`, `"REDIS"` or `"NATIVE_PERSISTENCE"`                                          |
| `GLUU_NAMESPACE`                                | Namespace to deploy Gluu in                                                      | `"<name>"`                                                                                  |
| `GLUU_FQDN`                                     | Gluu FQDN                                                                        | `"<FQDN>"` i.e `"demoexample.gluu.org"`                                                     |
| `COUNTRY_CODE`                                  | Gluu country code                                                                | `"<country code>"` i.e `"US"`                                                               |
| `STATE`                                         | Gluu state                                                                       | `"<state>"` i.e `"TX"`                                                                      |
| `EMAIL`                                         | Gluu email                                                                       | `"<email>"` i.e `"support@gluu.org"`                                                        |
| `CITY`                                          | Gluu city                                                                        | `"<city>"` i.e `"Austin"`                                                                   |
| `ORG_NAME`                                      | Gluu organization name                                                           | `"<org-name>"` i.e `"Gluu"`                                                                 |
| `GMAIL_ACCOUNT`                                 | Gmail account for GKE installation                                               | `""` or`"<gmail>"` i.e                                                                      |
| `GMAIL_ACCOUNT`                                 | Gmail account for GKE installation                                               | `""` or`"<gmail>"` i.e                                                                      |
| `GOOGLE_NODE_HOME_DIR`                          | User node home directory, used if the hosts volume is used                       | `"Y"` or `"N"`                                                                              |
| `IS_GLUU_FQDN_REGISTERED`                       | Is Gluu FQDN globally resolvable                                                 | `"Y"` or `"N"`                                                                              |
| `OXD_APPLICATION_KEYSTORE_CN`                   | OXD application keystore common name                                             | `"<name>"` i.e `"oxd_server"`                                                               |
| `OXD_ADMIN_KEYSTORE_CN`                         | OXD admin keystore common name                                                   | `"<name>"` i.e `"oxd_server"`                                                               |
| `LDAP_STORAGE_SIZE`                             | LDAP volume storage size                                                         | `""` i.e `"4Gi"`                                                                            |
| `OXTRUST_OXSHIBBOLETH_SHARED_STORAGE_SIZE`      | oxShibboleth and oxTrust shared volume storage size                              | `""` i.e `"4Gi"`                                                                            |
| `NFS_STORAGE_SIZE`                              | NFS volume storage size                                                          | `""` i.e `"4Gi"`                                                                            |
| `OXAUTH_REPLICAS`                               | Number of oxAuth replicas                                                        | min `"1"`                                                                                   |
| `OXTRUST_REPLICAS`                              | Number of oxTrust replicas                                                       | min `"1"`                                                                                   |
| `LDAP_REPLICAS`                                 | Number of LDAP replicas                                                          | min `"1"`                                                                                   |
| `OXSHIBBOLETH_REPLICAS`                         | Number of oxShibboleth replicas                                                  | min `"1"`                                                                                   |
| `OXPASSPORT_REPLICAS`                           | Number of oxPassport replicas                                                    | min `"1"`                                                                                   |
| `OXD_SERVER_REPLICAS`                           | Number of oxdServer replicas                                                     | min `"1"`                                                                                   |
| `CASA_REPLICAS`                                 | Number of Casa replicas [alpha]                                                  | min `"1"`                                                                                   |
| `RADIUS_REPLICAS`                               | Number of Radius replica                                                         | min `"1"`                                                                                   |
| `ENABLE_OXTRUST_API`                            | Enable oxTrust-api                                                               | `"Y"` or `"N"`                                                                              |
| `ENABLE_OXTRUST_TEST_MODE`                      | Enable oxTrust Test Mode                                                         | `"Y"` or `"N"`                                                                              |
| `ENABLE_CACHE_REFRESH`                          | Enable cache refresh rotate installation                                         | `"Y"` or `"N"`                                                                              |
| `ENABLE_OXD`                                    | Enable oxd server installation                                                   | `"Y"` or `"N"`                                                                              |
| `ENABLE_RADIUS`                                 | Enable Radius installation                                                       | `"Y"` or `"N"`                                                                              |
| `ENABLE_OXPASSPORT`                             | Enable oxPassport installation                                                   | `"Y"` or `"N"`                                                                              |
| `ENABLE_OXSHIBBOLETH`                           | Enable oxShibboleth installation                                                 | `"Y"` or `"N"`                                                                              |
| `ENABLE_CASA`                                   | Enable Casa installation [alpha]                                                 | `"Y"` or `"N"`                                                                              |
| `ENABLE_KEY_ROTATE`                             | Enable key rotate installation                                                   | `"Y"` or `"N"`                                                                              |
| `ENABLE_OXTRUST_API_BOOLEAN`                    | Used by `pygluu-kubernetes`                                                      | `"false"`                                                                                   |
| `ENABLE_OXTRUST_TEST_MODE_BOOLEAN`              | Used by `pygluu-kubernetes`                                                      | `"false"`                                                                                   |
| `ENABLE_RADIUS_BOOLEAN`                         | Used by `pygluu-kubernetes`                                                      | `"false"`                                                                                   |
| `ENABLE_OXPASSPORT_BOOLEAN`                     | Used by `pygluu-kubernetes`                                                      | `"false"`                                                                                   |
| `ENABLE_CASA_BOOLEAN`                           | Used by `pygluu-kubernetes`                                                      | `"false"`                                                                                   |
| `ENABLE_SAML_BOOLEAN`                           | Used by `pygluu-kubernetes`                                                      | `"false"`                                                                                   |
| `EDIT_IMAGE_NAMES_TAGS`                         | Manually place the image source and tag                                          | `"Y"` or `"N"`                                                                              |
| `CASA_IMAGE_NAME`                               | Casa image repository name                                                       | i.e `"gluufederation/casa"`                                                                 |
| `CASA_IMAGE_TAG`                                | Casa image tag                                                                   | i.e `"4.1.0_01"`                                                                            |
| `CONFIG_IMAGE_NAME`                             | Config image repository name                                                     | i.e `"gluufederation/config-init"`                                                          |
| `CONFIG_IMAGE_TAG`                              | Config image tag                                                                 | i.e `"4.1.0_01"`                                                                            |
| `CACHE_REFRESH_ROTATE_IMAGE_NAME`               | Cache refresh image repository name                                              | i.e `"gluufederation/cr-rotate"`                                                            |
| `CACHE_REFRESH_ROTATE_IMAGE_TAG`                | Cache refresh  image tag                                                         | i.e `"4.1.0_01"`                                                                            |
| `KEY_ROTATE_IMAGE_NAME`                         | Key rotate image repository name                                                 | i.e `"gluufederation/key-rotation"`                                                         |
| `KEY_ROTATE_IMAGE_TAG`                          | Key rotate image tag                                                             | i.e `"4.1.0_01"`                                                                            |
| `LDAP_IMAGE_NAME`                               | LDAP image repository name                                                       | i.e `"gluufederation/wrends"`                                                               |
| `LDAP_IMAGE_TAG`                                | LDAP image tag                                                                   | i.e `"4.1.0_01"`                                                                            |
| `OXAUTH_IMAGE_NAME`                             | oxAuth image repository name                                                     | i.e `"gluufederation/oxauth"`                                                               |
| `OXAUTH_IMAGE_TAG`                              | oxAuth image tag                                                                 | i.e `"4.1.0_01"`                                                                            |
| `OXD_IMAGE_NAME`                                | oxd image repository name                                                        | i.e `"gluufederation/oxd-server"`                                                           |
| `OXD_IMAGE_TAG`                                 | oxd image tag                                                                    | i.e `"4.1.0_01"`                                                                            |
| `OXPASSPORT_IMAGE_NAME`                         | oxPassport image repository name                                                 | i.e `"gluufederation/oxpassport"`                                                           |
| `OXPASSPORT_IMAGE_TAG`                          | oxPassport image tag                                                             | i.e `"4.1.0_01"`                                                                            |
| `OXSHIBBOLETH_IMAGE_NAME`                       | oxShibboleth image repository name                                               | i.e `"gluufederation/oxshibboleth"`                                                         |
| `OXSHIBBOLETH_IMAGE_TAG`                        | oxShibboleth image tag                                                           | i.e `"4.1.0_01"`                                                                            |
| `OXTRUST_IMAGE_NAME`                            | oxTrust image repository name                                                    | i.e `"gluufederation/oxtrust"`                                                              |
| `OXTRUST_IMAGE_TAG`                             | oxTrust image tag                                                                | i.e `"4.1.0_01"`                                                                            |
| `PERSISTENCE_IMAGE_NAME`                        | Persistence image repository name                                                | i.e `"gluufederation/persistence"`                                                          |
| `PERSISTENCE_IMAGE_TAG`                         | Persistence image tag                                                            | i.e `"4.1.0_01"`                                                                            |
| `RADIUS_IMAGE_NAME`                             | Radius image repository name                                                     | i.e `"gluufederation/radius"`                                                               |
| `RADIUS_IMAGE_TAG`                              | Radius image tag                                                                 | i.e `"4.1.0_01"`                                                                            |
| `UPGRADE_IMAGE_NAME`                            | Gluu upgrade image repository name                                               | i.e `"gluufederation/upgrade"`                                                              |
| `UPGRADE_IMAGE_TAG`                             | Gluu upgrade image tag                                                           | i.e `"4.1.0_01"`                                                                            |
| `CONFIRM_PARAMS`                                | Confirm using above options                                                      | `"Y"` or `"N"`                                                                              |

### `LDAP_VOLUME_TYPE`-options

`LDAP_VOLUME_TYPE=""` but if `PERSISTENCE_BACKEND` is `WrenDS` options are :

| Options  | Deployemnt Architecture  | Volume Type                                   |
| -------- | ------------------------ | --------------------------------------------- |
| `1`      | Microk8s                 | LDAP volumes on host                          |
| `2`      | Minikube                 | LDAP volumes on host                          |
| `6`      | EKS                      | LDAP volumes on host                          |
| `7`      | EKS                      | LDAP EBS volumes dynamically provisioned      |
| `8`      | EKS                      | LDAP EBS volumes statically provisioned       |
| `9`      | EKS                      | LDAP EFS volume                               |
| `11`     | GKE                      | LDAP volumes on host                          |
| `12`     | GKE                      | LDAP Persistent Disk  dynamically provisioned |
| `13`     | GKE                      | LDAP Persistent Disk  statically provisioned  |
| `16`     | Azure                    | LDAP volumes on host                          |
| `17`     | Azure                    | LDAP Persistent Disk  dynamically provisioned |
| `18`     | Azure                    | LDAP Persistent Disk  statically provisioned  |

## Uninstall Gluu using Kustomize

1. Run :

    ```bash
    ./pygluu-kubernetes.pyz uninstall
    ```
    
# Install Gluu using Helm

## Prerequisites

- Kubernetes 1.x
- Persistent volume provisioner support in the underlying infrastructure
- Install [Helm3](https://helm.sh/docs/using_helm/)

## Quickstart

1) Download [`pygluu-kubernetes.pyz`](https://github.com/GluuFederation/enterprise-edition/releases). This package can be built [manually](https://github.com/GluuFederation/enterprise-edition/blob/4.1/README.md#build-pygluu-kubernetespyz-manually).

1) Run :

  ```bash
  ./pygluu-kubernetes.pyz helm-install
  ```
### Installing Gluu using Helm manually

1) Install [nginx-ingress](https://github.com/kubernetes/ingress-nginx) Helm [Chart](https://github.com/helm/charts/tree/master/stable/nginx-ingress).

   ```bash
   helm repo add stable https://kubernetes-charts.storage.googleapis.com
   helm repo update
   helm install <nginx-release-name> stable/nginx-ingress --namespace=<nginx-namespace>
   ```

1)  - If the FQDN for gluu i.e `demoexample.gluu.org` is registered and globally resolvable, forward it to the loadbalancers address created in the previous step by nginx-ingress. A record can be added on most cloud providers to forward the domain to the loadbalancer. Forexample, on AWS assign a CNAME record for the LoadBalancer DNS name, or use Amazon Route 53 to create a hosted zone. More details in this [AWS guide](https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/using-domain-names-with-elb.html?icmpid=docs_elb_console). Another example on [GCE](https://medium.com/@kungusamuel90/custom-domain-name-mapping-for-k8s-on-gcp-4dc263b2dabe).

    - If the FQDN is not registered acquire the loadbalancers ip if on **GCE**, or **Azure** using `kubectl get svc <release-name>-nginx-ingress-controller --output jsonpath='{.status.loadBalancer.ingress[0].ip}'` and if on **AWS** get the loadbalancers addresss using `kubectl -n ingress-nginx get svc ingress-nginx \--output jsonpath='{.status.loadBalancer.ingress[0].hostname}'`.

1)  - If deploying on the cloud make sure to take a look at the helm cloud specific notes before continuing.

      * [EKS](#eks-helm-notes)
      * [GKE](#gke-helm-notes)

    - If deploying locally make sure to take a look at the helm specific notes bellow before continuing.

      * [Minikube](#minikube-helm-notes)
      * [MicroK8s](#microk8s-helm-notes)

1)  **Optional:** If using couchbase as the persistence backend.
    
    1) Download [`pygluu-kubernetes.pyz`](https://github.com/GluuFederation/enterprise-edition/releases). This package can be built [manually](https://github.com/GluuFederation/enterprise-edition/blob/4.1/README.md#build-pygluu-kubernetespyz-manually).
    
    1) Run:
       ```bash
       ./pygluu-kubernetes.pyz couchbase-install
       ```
    1) Open `settings.json` file generated from the previous step and copy over the values of `COUCHBASE_URL` and `COUCHBASE_USER`   to `global.gluuCouchbaseUrl` and `global.gluuCouchbaseUser` in `values.yaml` respectively. 

1)  Make sure you are in the same directory as the `values.yaml` file and run:

   ```bash
   helm install <release-name> -f values.yaml -n <namespace> .
   ```

  ## EKS helm notes
  ### Required changes to the `values.yaml`

  Inside the global `values.yaml` change the marked keys with `CHANGE-THIS`  to the appropriate values :

  ```yaml
  #global values to be used across charts
  global:
      awsLocalStorage: true #CHANGE-THIS if not in production ,hence not using EFS set awsLocalStorage to true to use for shared shibboleth files.
    provisioner: kubernetes.io/aws-ebs #CHANGE-THIS
    lbAddr: "" #CHANGE-THIS to the address recieved in the previous step axx-109xx52.us-west-2.elb.amazonaws.com
    domain: demoexample.gluu.org #CHANGE-THIS to the FQDN used for Gluu
    isDomainRegistered: "false" # CHANGE-THIS  "true" or "false" to specify if the domain above is registered or not.

  # If using EFS change the marked values from your EFS below:
  efs-provisioner:
    efsProvisioner:

      # Change the following:
      dnsName: "" #CHANGE-THIS if efs is used to fs-xxxxxx.efs.us-east-1.amazonaws.com
      efsFileSystemId: "" #CHANGE-THIS if efs is used to  fs-xxx
      awsRegion: "" #CHANGE-THIS if efs is used to us-east-1
      path: /opt/shared-shibboleth-idp
      provisionerName: example.com/gcp-efs
      storageClass:
        name: gcp-efs
        isDefault: false
      persistentVolume:
        accessModes: ReadWriteMany
        storage: 5Gi

  nginx:
    ingress:
      enabled: true
      path: /
      hosts:
        - demoexample.gluu.org #CHANGE-THIS to the FQDN used for Gluu
      tls:
        - secretName: tls-certificate
          hosts:
            - demoexample.gluu.org #CHANGE-THIS to the FQDN used for Gluu
  ```    

  Tweak the optional [parameters](#configuration) in `values.yaml` to fit the setup needed.

  ## GKE helm notes

  ### Required changes to the `values.yaml`

  Inside the global `values.yaml` change the marked keys with `CHANGE-THIS`  to the appopriate values :

  ```yaml
  #global values to be used across charts
  global:
      awsLocalStorage: true
    provisioner: kubernetes.io/gce-pd #CHANGE-THIS
    lbAddr: ""
    domain: demoexample.gluu.org #CHANGE-THIS to the FQDN used for Gluu
      # Networking configs
    nginxIp: "" #CHANGE-THIS  to the IP recieved from the previous step
    isDomainRegistered: "false" # CHANGE-THIS  "true" or "false" to specify if the domain above is registered or not.
  nginx:
    ingress:
      enabled: true
      path: /
      hosts:
        - demoexample.gluu.org #CHANGE-THIS to the FQDN used for Gluu
      tls:
        - secretName: tls-certificate
          hosts:
            - demoexample.gluu.org #CHANGE-THIS to the FQDN used for Gluu
  nfs: 
    enabled: true
  ```

  Tweak the optional [parameteres](#configuration) in `values.yaml` to fit the setup needed.

  ## Minikube helm notes

  ### Required changes to the `values.yaml`

  Inside the global `values.yaml` change the marked keys with `CHANGE-THIS`  to the appopriate values :

  ```yaml
  #global values to be used across charts
  global:
      awsLocalStorage: true
    provisioner: k8s.io/minikube-hostpath #CHANGE-THIS
    lbAddr: ""
    domain: demoexample.gluu.org #CHANGE-THIS to the FQDN used for Gluu
    nginxIp: "" #CHANGE-THIS  to the IP of minikube <minikube ip>

  nginx:
    ingress:
      enabled: true
      path: /
      hosts:
        - demoexample.gluu.org #CHANGE-THIS to the FQDN used for Gluu
      tls:
        - secretName: tls-certificate
          hosts:
            - demoexample.gluu.org #CHANGE-THIS to the FQDN used for Gluu
  ```

  Tweak the optional [parameters](#configuration) in `values.yaml` to fit the setup needed.

  - Map gluus FQDN at `/etc/hosts` file  to the minikube IP as shown below.

  ```bash
  ##
  # Host Database
  #
  # localhost is used to configure the loopback interface
  # when the system is booting.  Do not change this entry.
  ##
  192.168.99.100	demoexample.gluu.org #minikube IP and example domain
  127.0.0.1	localhost
  255.255.255.255	broadcasthost
  ::1             localhost
  ```

  ## Microk8s helm notes
  
  ### Required changes to the `values.yaml`

  Inside the global `values.yaml` change the marked keys with `CHANGE-THIS`  to the appopriate values :

  ```yaml
  #global values to be used across charts
  global:
      awsLocalStorage: true
    provisioner: microk8s.io/hostpath #CHANGE-THIS
    lbAddr: ""
    domain: demoexample.gluu.org #CHANGE-THIS to the FQDN used for Gluu
    nginxIp: "" #CHANGE-THIS  to the IP of the microk8s vm

  nginx:
    ingress:
      enabled: true
      path: /
      hosts:
        - demoexample.gluu.org #CHANGE-THIS to the FQDN used for Gluu
      tls:
        - secretName: tls-certificate
          hosts:
            - demoexample.gluu.org #CHANGE-THIS to the FQDN used for Gluu
  ```

  Tweak the optional [parameteres](#configuration) in `values.yaml` to fit the setup needed.

  - Map gluus FQDN at `/etc/hosts` file  to the microk8s vm IP as shown below.

  ```bash
  ##
  # Host Database
  #
  # localhost is used to configure the loopback interface
  # when the system is booting.  Do not change this entry.
  ##
  192.168.99.100	demoexample.gluu.org #microk8s IP and example domain
  127.0.0.1	localhost
  255.255.255.255	broadcasthost
  ::1             localhost
  ```
  
## Uninstalling the Chart

To uninstall/delete `my-release` deployment:

`helm delete <my-release>`

If during installation the release was not defined, release name is checked by running `$ helm ls` then deleted using the previous command and the default release name.

## Configuration

| Parameter                                          | Description                                                                                                                      | Default                             |
| -------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------- |
| `global.cloud.enabled`                             | Whether to enable cloud provisioning.                                                                                            | `false`                             |
| `global.provisioner`                               | Which cloud provisioner to use when deploying                                                                                    | `k8s.io/minikube-hostpath`          |
| `global.cloud.awsLocalStorage`                     | Deploy to AWS cloud but use localstorage                                                                                         | `true`                              |
| `global.ldapServiceName`                           | ldap service name. Used to connect other services to ldap                                                                        | `opendj`                            |
| `global.nginxIp`                                   | IP address to be used with a FQDN                                                                                                | `192.168.99.100` (for minikube)     |
| `global.oxAuthServiceName`                         | `oxauth` service name - should not be changed                                                                                    |  `oxauth`                           |
| `global.oxTrustServiceName`                        | `oxtrust` service name - should not be changed                                                                                   | `oxtrust`                           |
| `global.domain`                                    | DNS domain name                                                                                                                  | `demoexample.gluu.org`              |
| `global.isDomainRegistered`                        | Whether the domain to be used is registered or not                                                                               | `false`                             |
| `global.gluuLdapUrl`                               | wrends/ldap server url. Port and service name of opendj server - should not be changed                                           |  `opendj:1636`                      |
| `global.gluuMaxFraction`                           | Controls how much of total RAM is up for grabs in containers running Java apps                                                   |  `1`                                |
| `global.configAdapterName`                         | The config backend adapter                                                                                                       | `Kubernetes`                        |
| `global.configSecretAdapter`                       | The secrets adapter                                                                                                              | `Kubernetes`                        |
| `global.gluuPersistenceType`                       | Which database backend to use                                                                                                    | `ldap`                              |
| `global.gluuCouchbaseUrl`                          | Couchbase URL. Used only when `global.gluuPersistenceType` is `hybrid` or `couchbase`                                            | `cbgluu.cbns.svc.cluster.local`     |
| `global.gluuCouchbaseUser`                         | Couchbase user. Used only when `global.gluuPersistenceType` is `hybrid` or `couchbase`                                           | `admin`                             |
| `global.gluuCouchbasePassFile`                     | Location of `couchbase_password` file                                                                                            | `/etc/gluu/conf/couchbase_password` |
| `global.gluuCouchbaseCertFile`                     | Location of `couchbase.crt` used by cb for tls termination                                                                       | `/etc/gluu/conf/couchbase.crt`      |
| `global.oxshibboleth.enabled`                      | Whether to allow installation of oxshibboleth chart                                                                              | `false`                             |
| `global.key-rotation.enabled`                      | Allow key rotation                                                                                                               | `false`                             |
| `global.cr-rotate.enabled`                         | Allow cache rotation deployment                                                                                                  | `false`                             |
| `global.radius.enabled`                            | Enabled radius installation                                                                                                      | `false`                             |
| `global.redis.enabled`                             | Whether to allow installation of redis chart.                                                                                    | `false`                             |
| `global.shared-shib.enabled`                       | Allow installation of shared volumes. They are shared between `oxtrust` and `oxshibboleth` services.                             | `true`                              |
| `global.oxtrust.enabled`                           | Allow installation of oxtrust                                                                                                    |  `true`                             |
| `global.nginx.enabled`                             | Allow installation of nginx. Should be allowed unless another nginx is being deployed                                            |  `true`                             |
| `global.config.enabled`                            | Either to install config chart or not.                                                                                           | `true`                              |   
| `efs-provisioner.enabled`                          | Enable EFS provisioning for AWS deployments ONLY                                                                                 | `false`                             |
| `efs-provisioner.efsProvisioner.dnsName`           | EFS DNS name. Usually, fs-xxxxxx.efs.aws-region.amazonaws.com                                                                    | `" "`                               |
| `efs-provisioner.efsProvisioner.efsFileSystemId`   | EFS id                                                                                                                           | `" "`                               |
| `efs-provisioner.efsProvisioner.awsRegion`         | AWS region which the deployment is taking place                                                                                  | `us-west-2`                         |
| `config.orgName`                                   | Organisation Name                                                                                                                | `Gluu`                              |
| `config.email`                                     | Email to be registered with ssl                                                                                                  | `support@gluu.org`                  |
| `config.adminPass`                                 | Admin password to log in to the UI                                                                                               | `P@ssw0rd`                          |
| `config.domain`                                    | FQDN                                                                                                                             | `demoexample.gluu.org`              |
| `config.countryCode`                               | Country code of where the Org is located                                                                                         | `US`                                |
| `config.state`                                     | State                                                                                                                            | `TX`                                |
| `config.ldapType`                                  | Type of LDAP server to use.                                                                                                      | `opendj`                            |
| `global.oxauth.enabled`                            | Whether to allow installation of oxauth subchart. Should be left as true                                                         |  `true`                             |
| `global.opendj.enabled`                            | Allow installation of ldap Should left as true                                                                                   | `true`                              |
| `global.gluuCacheType`                             | Options `REDIS` or `NATIVE_PERSISTENCE` If `REDIS` is used redis chart must be enabled and `gluuRedisEnabled` config set to true | `NATIVE_PERSISTENCE`                |
| `opendj.gluuRedisEnabled`                          | Used if cache type is redis                                                                                                      | `false`                             |
| `global.persistence.enabled`                       | Whether to enable persistence layer. Must ALWAYS remain true                                                                     | `true`                              |
| `persistence.configmap.gluuCasaEnabled`            | Enable auto install of casa chart/service while installing Gluu server chart                                                     | `false`                             |
| `persistence.configmap.gluuPassportEnabled`        | Auto install passport service chart                                                                                              | `false`                             |
| `persistence.configmap.gluuRadiusEnabled`          | Auto install radius service chart                                                                                                | `false`                             |
| `persistence.configmap.gluuSamlEnabled`            | Auto enable SAML in oxshibboleth. This should be true whether or not `oxshibboleth` is installed or not.                         | `true`                              |
| `oxd-server.enabled`                               | Enable or disable installation of OXD server                                                                                     | `false`                             |
| `oxd-server.configmap.adminKeystorePassword`       | Admin keystore password                                                                                                          | `examplePass`                       |
| `oxd-server.configmap.applicationKeystorePassword` | Password used to decrypt the keystore                                                                                            | `examplePass`                       |  
| `nginx.ingress.enabled`                            | Set routing rules to different services                                                                                          | `true`                              |
| `nginx.ingress.hosts`                              | Gluu FQDN                                                                                                                        | `demoexample.gluu.org`              |

## Persistence

**_NOTE_** Enabling support of `oxtrust API` and `oxtrust TEST_MODE`
 To enable `oxtrust API` support and or `oxtrust TEST_MODE` , set  `gluuOxtrustApiEnabled`  and `gluuOxtrustApiTestMode` true respectively.

 ```yaml
 # persistence layer
 persistence:
   configmap:
      gluuOxtrustApiEnabled: true

 ```

 Consequently, to enable `oxtrust TEST_MODE` set the variable `gluuOxtrustApiTestMode` in the same persistence service to true

 ```yaml
# persistence layer
persistence:
  configmap:
     gluuOxtrustApiTestMode: true

```

## Instructions on how to install different services

Enabling the following services automatically install the corresponding associated chart. To enable/disable them set `true` or `false` in the persistence configs as shown below.  

```yaml
# persistence layer
persistence:
  enabled: true
  configmap:
    # Auto install other services. If enabled the respective service chart will be installed
    gluuPassportEnabled: false
    gluuCasaEnabled: false
    gluuRadiusEnabled: false
    gluuSamlEnabled: false
```

### OXD-server

> **_NOTE:_** If these two are not provided `oxd-server` will fail to start.   
> **_NOTE:_** For these passwords, stick to digits and numbers only.

```yaml
oxd-server:
  configmap:
    adminKeystorePassword: admin-example-password
    applicationKeystorePassword: app-example-pass

```

### Casa

- Casa is dependant on `oxd-server`. To install it `oxd-server` must be enabled.

### Redis

To enable usage of Redis, change the following values.

```yaml
opendj:
  # options REDIS/NATIVE_PERSISTENCE
  gluuCacheType: REDIS
  # options true/false : must be enabled if cache type is REDIS
  gluuRedisEnabled: true

# redis should be enabled only when cacheType is REDIS
global:
  redis:
    enabled: true

```


### Other optional services

Other optional services like `key-rotation`, `cr-rotation`, and `radius` are enabled by setting their corresponding values to `true` under the global block.

For example, to enable `cr-rotate` set

```yaml
global:
  cr-rotate:
    enabled: true
```

# Use Couchbase solely as the persistence layer
![CDNJS](https://img.shields.io/badge/AWS-supported-green.svg)
![CDNJS](https://img.shields.io/badge/GKE-supported-green.svg)
![CDNJS](https://img.shields.io/badge/microk8s-supported-green.svg)
![CDNJS](https://img.shields.io/badge/minikube-supported-green.svg)

## Requirements
  - If you are installing on microk8s or minikube please ignore the below notes as a low resource `couchbase-cluster.yaml` will be applied automatically, however the VM being used must at least have 8GB RAM and 2 cpu available .
  
  - An `m5.xlarge` EKS cluster with 3 nodes at the minimum or `n2-standard-4` GKE cluster with 3 nodes. We advice contacting Gluu regarding production setups.

- [Install couchbase kubernetes](https://www.couchbase.com/downloads) and place the tar.gz file inside the same directory as the `pygluu-kubernetes.pyz`.

- A modified `couchbase/couchbase-cluster.yaml` will be generated but in production it is likely that this file will be modified.
  * To override the `couchbase-cluster.yaml` place the file inside `/couchbase` folder after running `./pygluu-kubernetes.pyz`. More information on the properties [couchbase-cluster.yaml](https://docs.couchbase.com/operator/1.2/couchbase-cluster-config.html).

> **_NOTE:_** Please note the `couchbase/couchbase-cluster.yaml` file must include at least three defined `spec.servers` with the labels `couchbase_services: index`, `couchbase_services: data` and `couchbase_services: analytics`

**If you wish to get started fast just change the values of `spec.servers.name` and `spec.servers.serverGroups` inside `couchbase/couchbase-cluster.yaml` to the zones of your EKS nodes and continue.**

- Run `./pygluu-kubernetes.pyz install-couchbase` and follow the prompts to install couchbase solely with Gluu.


# Use remote Couchbase as the persistence layer

- [Install couchbase](https://docs.couchbase.com/server/current/install/install-intro.html)

- Obtain the Public DNS or FQDN of the couchbase node.

- Head to the FQDN of the couchbase node to [setup](https://docs.couchbase.com/server/current/manage/manage-nodes/create-cluster.html) your couchbase cluster. When setting up please use the FQDN as the hostname of the new cluster.

- Couchbase URL base , user, and password will be needed for installation when running `pygluu-kubernetes.pyz`


## How to expand EBS volumes

1. Make sure the `StorageClass` used in your deployment has the `allowVolumeExpansion` set to true. If you have used our EBS volume deployment strategy then you will find that this property has already been set for you.

1. Edit your persistent volume claim using `kubectl edit pvc <claim-name> -n <namespace> ` and increase the value found for `storage:` to the value needed. Make sure the volumes expand by checking the `kubectl get pvc <claim-name> -n <namespace> `.

1. Restart the associated services


## Scaling pods

> **_NOTE:_** When using Mircok8s substitute  `kubectl` with `microk8s.kubectl` in the below commands.

To scale pods, run the following command:

```
kubectl scale --replicas=<number> <resource> <name>
```

In this case, `<resource>` could be Deployment or Statefulset and `<name>` is the resource name.

Examples:

-   Scaling oxAuth:

    ```
    kubectl scale --replicas=2 deployment oxauth
    ```

-   Scaling oxTrust:

    ```
    kubectl scale --replicas=2 statefulset oxtrust
    ```
# Build pygluu-kubernetes installer

## Overview
[`pygluu-kubernetes.pyz`](https://github.com/GluuFederation/enterprise-edition/releases) is periodically released and does not need to be built manually. However, the process of building the installer package is listed [below](#build-pygluu-kubernetespyz-manually).

## Build `pygluu-kubernetes.pyz` manually

## Prerequisites

1.  Python 3.6+.
1.  Python `pip3` package.

## Installation

### Standard Python package

1.  Create virtual environment and activate:

    ```sh
    python3 -m venv .venv
    source .venv/bin/activate
    ```

1.  Install the package:

    ```
    make install
    ```

    This command will install executable called `pygluu-kubernetes` available in virtual environment `PATH`.

### Python zipapp

1.  Install [shiv](https://shiv.readthedocs.io/) using `pip3`:

    ```sh
    pip3 install shiv
    ```

1.  Install the package:

    ```sh
    make zipapp
    ```

    This command will generate executable called `pygluu-kubernetes.pyz` under the same directory.

# Build pygluu-kubernetes installer

## Overview
[`pygluu-kubernetes.pyz`](https://github.com/GluuFederation/enterprise-edition/releases) is periodically released and does not need to be built manually. However, the process of building the installer package is listed [below](#build-pygluu-kubernetespyz-manually).

## Build `pygluu-kubernetes.pyz` manually

## Prerequisites

1.  Python 3.6+.
1.  Python `pip3` package.

## Installation

### Standard Python package

1.  Create virtual environment and activate:

    ```sh
    python3 -m venv .venv
    source .venv/bin/activate
    ```

1.  Install the package:

    ```
    make install
    ```

    This command will install executable called `pygluu-kubernetes` available in virtual environment `PATH`.

### Python zipapp

1.  Install [shiv](https://shiv.readthedocs.io/) using `pip3`:

    ```sh
    pip3 install shiv
    ```

1.  Install the package:

    ```sh
    make zipapp
    ```

    This command will generate executable called `pygluu-kubernetes.pyz` under the same directory.

### Known bug

- Bug in line 101   File `/Library/Frameworks/Python.framework/Versions/3.8/lib/python3.8/site-packages/kubernetes/client/models/v1beta1_custom_resource_definition_status.py`, line 101, in conditions. The error will look similar to the following:
  
  ```bash
    File "/root/.shiv/pygluu-kubernetes_3e5bddf4d309be28790a1b035ab5d72d0b9f33dfaade59da1bb9ec0bcd0165a4/site-packages/kubernetes/client/models/v1beta1_custom_resource_definition_status.py", line 54, in __init__
    self.conditions = conditions
  File "/root/.shiv/pygluu-kubernetes_3e5bddf4d309be28790a1b035ab5d72d0b9f33dfaade59da1bb9ec0bcd0165a4/site-packages/kubernetes/client/models/v1beta1_custom_resource_definition_status.py", line 101, in conditions
    ValueError: Invalid value for `conditions`, must not be `None`
  ```
  To fix this error just rerun the installation command `./pygluu-kubernetes.pyz <command>` again.
