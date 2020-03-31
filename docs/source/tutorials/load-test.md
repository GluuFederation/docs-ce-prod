# How to reach the one billion authentication per day with Gluu Server

The Gluu server has been optimized with several container strategies that allow scaling micro-services and orchestrating them using kubernetes.

## Overview

This tutorial will walk through installation of Gluu on AWS EKS (Elastic Kuberentes service ) and will detail the results of the most recent load-test done on Gluu.

## How to install

### Setup Cluster

#### Resources

Couchbase needs sufficient resources to run and under higher loads this becomes critical as timeouts in connections can occur resulting in failed authentications or cut offs. 

-  Follow this [guide](https://docs.aws.amazon.com/eks/latest/userguide/getting-started.html)
 to install a cluster with worker nodes. We used `c5.12xlarge`(48 vCPU, 96 Memory(GiB)) instance type. Please make sure that you have all the `IAM` policies for the AWS user that will be creating the cluster and volumes.
 
#### Requirements

-   The above guide should also walk you through installing `kubectl` , `aws-iam-authenticator` and `aws cli` on the VM you will be managing your cluster and nodes from. Check to make sure.

        aws-iam-authenticator help
        aws-cli
        kubectl version
        
#### Resources needed for ROPC flow (Resource Owner Password Credential Grant Flow)

| NAME                                     | # of nodes  | RAM(GiB) | CPU | Total RAM(GiB) | Total CPU |
| ---------------------------------------- | ----------- | -------  | --- | ------------- | --------- |
| Couchbase Index                          | 5           |  40      |  8  | 200           | 40        |
| Couchbase Query                          | 5           |  10      |  10 | 50            | 50        |
| Couchbase Data                           | 7           |  10      |  10 | 70            | 70        |
| Couchbase Search, Eventing and Analytics | 4           |  10      |  6  | 40            | 24        |
| oxAuth                                   | 100         |  2.5     | 2.5 | 250           | 250       |
| Grand Total                              |             |          |     | 610 GB        | 434       |

!!!note
   This hits `/token`. Hence the minimum TPS(Transactions per second) must be 11.5K to achieve one billion authentications in a day.
   
##### Example EKS cluster create command used:

```bash
eksctl create cluster --name gluuloadtest --version 1.15 --nodegroup-name standard-workers --node-type c5.12xlarge --zones eu-central-1a,eu-central-1b,eu-central-1c --nodes 10 --region eu-central-1 --node-ami auto --ssh-public-key "~/.ssh/id_rsa.pub"
```

##### Example `couchbase-cluster.yaml` used with ROPC flow

```yaml
apiVersion: couchbase.com/v1
kind: CouchbaseCluster
metadata:
  name: cbgluu #DO NOT CHANGE THIS LINE
spec:
  baseImage: couchbase/server
  version: enterprise-6.5.0
  antiAffinity: false
  tls:
    static:
      member:
        serverSecret: couchbase-server-tls
      operatorSecret: couchbase-operator-tls
  authSecret: cb-auth
  exposeAdminConsole: true
  dns:
    domain: "cbns.svc.cluster.local"
  adminConsoleServices:
    - data
  exposedFeatures:
    - xdcr
    - client
  exposedFeatureServiceType: LoadBalancer # Be very careful about using LoadBalancer as this will deploy an LB for every CB pod. In production please use NodePort and port-forwad to acess GUI
  serverGroups:
    - eu-central-1a # change to your zone a
    - eu-central-1b # change to your zone b
    - eu-central-1c # change to your zone c
  cluster:
    dataServiceMemoryQuota: 40000
    indexServiceMemoryQuota: 25000
    searchServiceMemoryQuota: 4000
    eventingServiceMemoryQuota: 4000
    analyticsServiceMemoryQuota: 4000
    indexStorageSetting: memory_optimized
    autoFailoverTimeout: 10
    autoFailoverMaxCount: 3
    autoFailoverOnDataDiskIssues: true
    autoFailoverOnDataDiskIssuesTimePeriod: 120
    autoFailoverServerGroup: false
  buckets:
    - name: gluu #DO NOT CHANGE THIS LINE
      type: couchbase
      memoryQuota: 500
      replicas: 1
      ioPriority: high
      evictionPolicy: valueOnly
      conflictResolution: seqno
      enableFlush: false
      enableIndexReplica: false
      compressionMode: passive
    - name: gluu_cache #DO NOT CHANGE THIS LINE
      type: ephemeral
      memoryQuota: 3500
      replicas: 1
      ioPriority: high
      evictionPolicy: nruEviction
      conflictResolution: seqno
      enableFlush: false
      enableIndexReplica: false
      compressionMode: passive
    - name: gluu_site #DO NOT CHANGE THIS LINE
      type: couchbase
      memoryQuota: 100
      replicas: 1
      ioPriority: high
      evictionPolicy: valueOnly
      conflictResolution: seqno
      enableFlush: false
      enableIndexReplica: false
      compressionMode: passive
    - name: gluu_token #DO NOT CHANGE THIS LINE
      type: ephemeral
      memoryQuota: 4500
      replicas: 1
      ioPriority: high
      evictionPolicy: nruEviction
      conflictResolution: seqno
      enableFlush: false
      enableIndexReplica: false
      compressionMode: passive
    - name: gluu_user #DO NOT CHANGE THIS LINE
      type: couchbase
      memoryQuota: 10000
      replicas: 1
      ioPriority: high
      evictionPolicy: valueOnly
      conflictResolution: seqno
      enableFlush: false
      enableIndexReplica: false
      compressionMode: passive

  servers:
    - name: index-eu-central-1a # change name to index-myzone-a
      size: 2
      services:
        - index
      serverGroups:
       - eu-central-1a # change to your zone a
      pod:
        labels:
          couchbase_services: index #DO NOT CHANGE THIS LINE UNLESS SERVER DEF IS REMOVED
        resources:
          limits:
            cpu: 8000m
          requests:
            cpu: 6000m
            memory: 40Gi
        volumeMounts:
          default: pvc-general
          index: pvc-index

    - name: index-eu-central-1c # change name to index-myzone-c
      size: 1
      services:
        - index
      serverGroups:
       - eu-central-1c # change to your zone c
      pod:
        labels:
          couchbase_services: index #DO NOT CHANGE THIS LINE UNLESS SERVER DEF IS REMOVED
        resources:
          limits:
            cpu: 8000m
          requests:
            cpu: 6000m
            memory: 40Gi
        volumeMounts:
          default: pvc-general
          index: pvc-index

    - name: index-eu-central-1b # change name to index-myzone-a
      size: 1
      services:
        - index
      serverGroups:
       - eu-central-1b # change to your zone a
      pod:
        labels:
          couchbase_services: index #DO NOT CHANGE THIS LINE UNLESS SERVER DEF IS REMOVED
        resources:
          limits:
            cpu: 8000m
          requests:
            cpu: 6000m
            memory: 40Gi
        volumeMounts:
          default: pvc-general
          index: pvc-index
          
    - name: analytics-eu-central-1a # change name to analytics-myzone-a
      size: 1
      services:
        - search
        - analytics
        - eventing
      serverGroups:
       - eu-central-1a # change to your zone a
      pod:
        labels:
          couchbase_services: analytics #DO NOT CHANGE THIS LINE UNLESS SERVER DEF IS REMOVED
        resources:
          limits:
            cpu: 6000m
          requests:
            cpu: 4000m
            memory: 10Gi          
        volumeMounts:
          default: pvc-general  
          analytics: 
            - pvc-analytics     
    - name: analytics-eu-central-1b # change name to analytics-myzone-b
      size: 1
      services:
        - search
        - analytics
        - eventing
      serverGroups:
       - eu-central-1b # change to your zone b
      pod:
        labels:
          couchbase_services: analytics #DO NOT CHANGE THIS LINE UNLESS SERVER DEF IS REMOVED
        resources:
          limits:
            cpu: 6000m
          requests:
            cpu: 4000m
            memory: 10Gi   
        volumeMounts:
          default: pvc-general
          analytics: 
            - pvc-analytics
    - name: analytics-eu-central-1c # change name to analytics-myzone-b
      size: 1
      services:
        - search
        - analytics
        - eventing
      serverGroups:
       - eu-central-1c # change to your zone b
      pod:
        labels:
          couchbase_services: analytics #DO NOT CHANGE THIS LINE UNLESS SERVER DEF IS REMOVED
        resources:
          limits:
            cpu: 6000m
          requests:
            cpu: 4000m
            memory: 10Gi
        volumeMounts:
          default: pvc-general
          analytics:
            - pvc-analytics
              
    - name: data-eu-central-1a # change name to data-myzone-a
      size: 1
      services:
        - data
      serverGroups:
       - eu-central-1a # change to your zone a
      pod:
        labels:
          couchbase_services: data #DO NOT CHANGE THIS LINE UNLESS SERVER DEF IS REMOVED
        resources:
          limits:
            cpu: 10000m
          requests:
            cpu: 8000m
            memory: 10Gi  
        volumeMounts:
          default: pvc-general
          data: pvc-data 
    - name: data-eu-central-1c # change name to data-myzone-c
      size: 3
      services:
        - data
      serverGroups:
       - eu-central-1c # change to your zone c
      pod:
        labels:
          couchbase_services: data #DO NOT CHANGE THIS LINE UNLESS SERVER DEF IS REMOVED
        resources:
          limits:
            cpu: 10000m
          requests:
            cpu: 8000m
            memory: 10Gi  
        volumeMounts:
          default: pvc-general  
          data: pvc-data
    - name: data-eu-central-1b # change name to data-myzone-b
      size: 1
      services:
        - data
      serverGroups:
       - eu-central-1b # change to your zone b
      pod:
        labels:
          couchbase_services: data #DO NOT CHANGE THIS LINE UNLESS SERVER DEF IS REMOVED
        resources:
          limits:
            cpu: 10000m
          requests:
            cpu: 8000m
            memory: 10Gi  
        volumeMounts:
          default: pvc-general 
          data: pvc-data     
    - name: data-eu-central-1b2 # change name to data-myzone-b
      size: 1
      services:
        - data
      serverGroups:
       - eu-central-1b # change to your zone b
      pod:
        labels:
          couchbase_services: data #DO NOT CHANGE THIS LINE UNLESS SERVER DEF IS REMOVED
        resources:
          limits:
            cpu: 10000m
          requests:
            cpu: 8000m
            memory: 10Gi
        volumeMounts:
          default: pvc-general
          data: pvc-data

    - name: query-eu-central-1a # change name to query-myzone-c
      size: 1
      services:
        - query
      serverGroups:
       - eu-central-1a # change to your zone c
      pod:
        labels:
          couchbase_services: query #DO NOT CHANGE THIS LINE UNLESS SERVER DEF IS REMOVED
        resources:
          limits:
            cpu: 10000m
          requests:
            cpu: 8000m
            memory: 10Gi        
        volumeMounts:
          default: pvc-general
          query: pvc-query

    - name: query-eu-central-1b # change name to query-myzone-c
      size: 1
      services:
        - query
      serverGroups:
       - eu-central-1b # change to your zone c
      pod:
        labels:
          couchbase_services: query #DO NOT CHANGE THIS LINE UNLESS SERVER DEF IS REMOVED
        resources:
          limits:
            cpu: 10000m
          requests:
            cpu: 8000m
            memory: 10Gi
        volumeMounts:
          default: pvc-general
          query: pvc-query          
          

    - name: query-eu-central-1c # change name to query-myzone-b
      size: 2
      services:
        - query
      serverGroups:
       - eu-central-1c # change to your zone b
      pod:
        labels:
          couchbase_services: query #DO NOT CHANGE THIS LINE UNLESS SERVER DEF IS REMOVED
        resources:
          limits:
            cpu: 10000m
          requests:
            cpu: 8000m
            memory: 10Gi
        volumeMounts:
          default: pvc-general
          query: pvc-query
          
  securityContext:
    fsGroup: 1000
  volumeClaimTemplates:
    - metadata:
        name: pvc-general
      spec:
        storageClassName: couchbase-sc
        resources:
          requests:
            storage: 400Gi
    - metadata:
        name: pvc-data
      spec:
        storageClassName: couchbase-sc
        resources:
          requests:
            storage: 500Gi
    - metadata:
        name: pvc-index
      spec:
        storageClassName: couchbase-sc
        resources:
          requests:
            storage: 250Gi
    - metadata:
        name: pvc-query
      spec:
        storageClassName: couchbase-sc
        resources:
          requests:
            storage: 250Gi
    - metadata:
        name: pvc-analytics
      spec:
        storageClassName: couchbase-sc
        resources:
          requests:
            storage: 200Gi
```

#### Resources needed for Authorization code flow (Non-Implicit Flow)

| NAME                                     | # of nodes  | RAM(GiB) | CPU | Total RAM(GiB) | Total CPU |
| ---------------------------------------- | ----------- | -------  | --- | -------------  | --------- |
| Couchbase Index                          | 13          |  40      |  8  | 520            | 104       |
| Couchbase Query                          | 12          |  10      |  10 | 120            | 120       |
| Couchbase Data                           | 14          |  10      |  10 | 140            | 140       |
| Couchbase Search, Eventing and Analytics | 7           |  10      |  6  | 70             | 42        |
| oxAuth                                   | 500         |  2.5     | 2.5 | 1000           | 1000      |
| Grand Total                              |             |          |     | 1850 GB        | 1406      |

Note!!!
   This needs a lot more resources as it hits  a total of 5 steps, 3 authorization steps `/token` , `/authorize`, `/oxauth/login` and 2 redirects. Hence the minimum TPS(Transactions per second) must be 60K to achieve one billion authentications in a day.

##### Example EKS cluster create command used:

```bash
eksctl create cluster --name gluuloadtest --version 1.15 --nodegroup-name standard-workers --node-type c5.12xlarge --zones eu-central-1a,eu-central-1b,eu-central-1c --nodes 32 --region eu-central-1 --node-ami auto --ssh-public-key "~/.ssh/id_rsa.pub"
```   

##### Example `couchbase-cluster.yaml`  used with Authorization code flow

```yaml
apiVersion: couchbase.com/v1
kind: CouchbaseCluster
metadata:
  name: cbgluu #DO NOT CHANGE THIS LINE
spec:
  baseImage: couchbase/server
  version: enterprise-6.5.0
  antiAffinity: false
  tls:
    static:
      member:
        serverSecret: couchbase-server-tls
      operatorSecret: couchbase-operator-tls
  authSecret: cb-auth
  exposeAdminConsole: true
  dns:
    domain: "cbns.svc.cluster.local"
  adminConsoleServices:
    - data
  exposedFeatures:
    - xdcr
    - client
  exposedFeatureServiceType: LoadBalancer # Be very careful about using LoadBalancer as this will deploy an LB for every CB pod. In production please use NodePort and port-forwad to acess GUI
  serverGroups:
    - eu-central-1a # change to your zone a
    - eu-central-1b # change to your zone b
    - eu-central-1c # change to your zone c
  cluster:
    dataServiceMemoryQuota: 40000
    indexServiceMemoryQuota: 25000
    searchServiceMemoryQuota: 4000
    eventingServiceMemoryQuota: 4000
    analyticsServiceMemoryQuota: 4000
    indexStorageSetting: memory_optimized
    autoFailoverTimeout: 10
    autoFailoverMaxCount: 3
    autoFailoverOnDataDiskIssues: true
    autoFailoverOnDataDiskIssuesTimePeriod: 120
    autoFailoverServerGroup: false
  buckets:
    - name: gluu #DO NOT CHANGE THIS LINE
      type: couchbase
      memoryQuota: 500
      replicas: 1
      ioPriority: high
      evictionPolicy: valueOnly
      conflictResolution: seqno
      enableFlush: false
      enableIndexReplica: false
      compressionMode: passive
    - name: gluu_cache #DO NOT CHANGE THIS LINE
      type: ephemeral
      memoryQuota: 3500
      replicas: 1
      ioPriority: high
      evictionPolicy: nruEviction
      conflictResolution: seqno
      enableFlush: false
      enableIndexReplica: false
      compressionMode: passive
    - name: gluu_site #DO NOT CHANGE THIS LINE
      type: couchbase
      memoryQuota: 100
      replicas: 1
      ioPriority: high
      evictionPolicy: valueOnly
      conflictResolution: seqno
      enableFlush: false
      enableIndexReplica: false
      compressionMode: passive
    - name: gluu_token #DO NOT CHANGE THIS LINE
      type: ephemeral
      memoryQuota: 4500
      replicas: 1
      ioPriority: high
      evictionPolicy: nruEviction
      conflictResolution: seqno
      enableFlush: false
      enableIndexReplica: false
      compressionMode: passive
    - name: gluu_user #DO NOT CHANGE THIS LINE
      type: couchbase
      memoryQuota: 10000
      replicas: 1
      ioPriority: high
      evictionPolicy: valueOnly
      conflictResolution: seqno
      enableFlush: false
      enableIndexReplica: false
      compressionMode: passive

  servers:
    - name: index-eu-central-1a # change name to index-myzone-a
      size: 4
      services:
        - index
      serverGroups:
       - eu-central-1a # change to your zone a
      pod:
        labels:
          couchbase_services: index #DO NOT CHANGE THIS LINE UNLESS SERVER DEF IS REMOVED
        resources:
          limits:
            cpu: 8000m
          requests:
            cpu: 6000m
            memory: 40Gi
        volumeMounts:
          default: pvc-general
          index: pvc-index

    - name: index-eu-central-1c # change name to index-myzone-c
      size: 4
      services:
        - index
      serverGroups:
       - eu-central-1c # change to your zone c
      pod:
        labels:
          couchbase_services: index #DO NOT CHANGE THIS LINE UNLESS SERVER DEF IS REMOVED
        resources:
          limits:
            cpu: 8000m
          requests:
            cpu: 6000m
            memory: 40Gi
        volumeMounts:
          default: pvc-general
          index: pvc-index

    - name: index-eu-central-1b # change name to index-myzone-a
      size: 4
      services:
        - index
      serverGroups:
       - eu-central-1b # change to your zone a
      pod:
        labels:
          couchbase_services: index #DO NOT CHANGE THIS LINE UNLESS SERVER DEF IS REMOVED
        resources:
          limits:
            cpu: 8000m
          requests:
            cpu: 6000m
            memory: 40Gi
        volumeMounts:
          default: pvc-general
          index: pvc-index
          
    - name: analytics-eu-central-1a # change name to analytics-myzone-a
      size: 2
      services:
        - search
        - analytics
        - eventing
      serverGroups:
       - eu-central-1a # change to your zone a
      pod:
        labels:
          couchbase_services: analytics #DO NOT CHANGE THIS LINE UNLESS SERVER DEF IS REMOVED
        resources:
          limits:
            cpu: 6000m
          requests:
            cpu: 4000m
            memory: 10Gi          
        volumeMounts:
          default: pvc-general  
          analytics: 
            - pvc-analytics     
    - name: analytics-eu-central-1b # change name to analytics-myzone-b
      size: 2
      services:
        - search
        - analytics
        - eventing
      serverGroups:
       - eu-central-1b # change to your zone b
      pod:
        labels:
          couchbase_services: analytics #DO NOT CHANGE THIS LINE UNLESS SERVER DEF IS REMOVED
        resources:
          limits:
            cpu: 6000m
          requests:
            cpu: 4000m
            memory: 10Gi   
        volumeMounts:
          default: pvc-general
          analytics: 
            - pvc-analytics
    - name: analytics-eu-central-1c # change name to analytics-myzone-b
      size: 2
      services:
        - search
        - analytics
        - eventing
      serverGroups:
       - eu-central-1c # change to your zone b
      pod:
        labels:
          couchbase_services: analytics #DO NOT CHANGE THIS LINE UNLESS SERVER DEF IS REMOVED
        resources:
          limits:
            cpu: 6000m
          requests:
            cpu: 4000m
            memory: 10Gi
        volumeMounts:
          default: pvc-general
          analytics:
            - pvc-analytics
              
    - name: data-eu-central-1a # change name to data-myzone-a
      size: 2
      services:
        - data
      serverGroups:
       - eu-central-1a # change to your zone a
      pod:
        labels:
          couchbase_services: data #DO NOT CHANGE THIS LINE UNLESS SERVER DEF IS REMOVED
        resources:
          limits:
            cpu: 10000m
          requests:
            cpu: 8000m
            memory: 10Gi  
        volumeMounts:
          default: pvc-general
          data: pvc-data 
    - name: data-eu-central-1c # change name to data-myzone-c
      size: 4
      services:
        - data
      serverGroups:
       - eu-central-1c # change to your zone c
      pod:
        labels:
          couchbase_services: data #DO NOT CHANGE THIS LINE UNLESS SERVER DEF IS REMOVED
        resources:
          limits:
            cpu: 10000m
          requests:
            cpu: 8000m
            memory: 10Gi  
        volumeMounts:
          default: pvc-general  
          data: pvc-data
    - name: data-eu-central-1b # change name to data-myzone-b
      size: 4
      services:
        - data
      serverGroups:
       - eu-central-1b # change to your zone b
      pod:
        labels:
          couchbase_services: data #DO NOT CHANGE THIS LINE UNLESS SERVER DEF IS REMOVED
        resources:
          limits:
            cpu: 10000m
          requests:
            cpu: 8000m
            memory: 10Gi  
        volumeMounts:
          default: pvc-general 
          data: pvc-data     
    - name: data-eu-central-1b2 # change name to data-myzone-b
      size: 3
      services:
        - data
      serverGroups:
       - eu-central-1b # change to your zone b
      pod:
        labels:
          couchbase_services: data #DO NOT CHANGE THIS LINE UNLESS SERVER DEF IS REMOVED
        resources:
          limits:
            cpu: 10000m
          requests:
            cpu: 8000m
            memory: 10Gi
        volumeMounts:
          default: pvc-general
          data: pvc-data

    - name: query-eu-central-1a # change name to query-myzone-c
      size: 4
      services:
        - query
      serverGroups:
       - eu-central-1a # change to your zone c
      pod:
        labels:
          couchbase_services: query #DO NOT CHANGE THIS LINE UNLESS SERVER DEF IS REMOVED
        resources:
          limits:
            cpu: 10000m
          requests:
            cpu: 8000m
            memory: 10Gi        
        volumeMounts:
          default: pvc-general
          query: pvc-query

    - name: query-eu-central-1b # change name to query-myzone-c
      size: 4
      services:
        - query
      serverGroups:
       - eu-central-1b # change to your zone c
      pod:
        labels:
          couchbase_services: query #DO NOT CHANGE THIS LINE UNLESS SERVER DEF IS REMOVED
        resources:
          limits:
            cpu: 10000m
          requests:
            cpu: 8000m
            memory: 10Gi
        volumeMounts:
          default: pvc-general
          query: pvc-query          
          

    - name: query-eu-central-1c # change name to query-myzone-b
      size: 4
      services:
        - query
      serverGroups:
       - eu-central-1c # change to your zone b
      pod:
        labels:
          couchbase_services: query #DO NOT CHANGE THIS LINE UNLESS SERVER DEF IS REMOVED
        resources:
          limits:
            cpu: 10000m
          requests:
            cpu: 8000m
            memory: 10Gi
        volumeMounts:
          default: pvc-general
          query: pvc-query
          
  securityContext:
    fsGroup: 1000
  volumeClaimTemplates:
    - metadata:
        name: pvc-general
      spec:
        storageClassName: couchbase-sc
        resources:
          requests:
            storage: 400Gi
    - metadata:
        name: pvc-data
      spec:
        storageClassName: couchbase-sc
        resources:
          requests:
            storage: 500Gi
    - metadata:
        name: pvc-index
      spec:
        storageClassName: couchbase-sc
        resources:
          requests:
            storage: 250Gi
    - metadata:
        name: pvc-query
      spec:
        storageClassName: couchbase-sc
        resources:
          requests:
            storage: 250Gi
    - metadata:
        name: pvc-analytics
      spec:
        storageClassName: couchbase-sc
        resources:
          requests:
            storage: 200Gi

```

!!!note
   The combination of flows in this case does mean the combination of grand total resources if the authentication is to reach one billion for each flow.

### Install Gluu

### Install Gluu using `pygluu-kubernetes` with Kustomize

1. Download [`pygluu-kubernetes.pyz`](https://github.com/GluuFederation/enterprise-edition/releases). This package can be built [manually](https://github.com/GluuFederation/enterprise-edition/blob/4.1/README.md#build-pygluu-kubernetespyz-manually).

1. Configure `couchbase-cluster.yaml`. The file is used to create the couchbase cluster. Two examples of `couchbase-cluster.yaml` are provided above according to  [ROPC-flow](#example-couchbase-clusteryaml-used-with-ropc-flow) and [Authorization-flow](#example-couchbase-clusteryaml--used-with-authorization-code-flow). Notice that `COUCHBASE_CLUSTER_FILE_OVERRIDE` is set to `Y` [below](#example-settingsjson-used). This file is placed in the same directory as `./pygluu-kubernetes.pyz`

1. Run :

    ```bash
    ./pygluu-kubernetes.pyz install-couchbase
    ```
   
1. Once couchbase is up and running. Open the file `settings.json` and change `"INSTALL_COUCHBASE"` to `"N"` as seen [below](#example-settingsjson-used). Then, install Gluu.  :

    ```bash
    ./pygluu-kubernetes.pyz install
    ```  

!!!note
    Prompts will ask for the rest of the information needed. You may generate the manifests (yaml files) and continue to deployment or just generate the  manifests (yaml files) during the execution of `pygluu-kubernetes.pyz`. `pygluu-kubernetes.pyz` will output a file called `settings.json` holding all the parameters. More information about this file and the vars it holds is [below](../installation-guide/install-kubernetes.md#settingsjson-parameters-file-contents) but  please don't manually create this file as the script can generate it using [`pygluu-kubernetes.pyz generate-settings`](https://github.com/GluuFederation/enterprise-edition/releases). 

#### Example `settings.json` used.

```json
{
  "ACCEPT_GLUU_LICENSE": "Y",
  "GLUU_VERSION": "4.1",
  "GLUU_UPGRADE_TARGET_VERSION": "",
  "GLUU_HELM_RELEASE_NAME": "",
  "NGINX_INGRESS_RELEASE_NAME": "",
  "NGINX_INGRESS_NAMESPACE": "",
  "NODES_IPS": [
    "35.158.241.206",
    "54.93.220.239",
    "18.197.157.35",
    "18.195.51.255",
    "3.127.81.246",
    "3.127.148.123",
    "35.158.113.203",
    "18.196.41.6",
    "3.123.8.76"
  ],
  "NODES_ZONES": [
    "eu-central-1a",
    "eu-central-1a",
    "eu-central-1a",
    "eu-central-1b",
    "eu-central-1b",
    "eu-central-1b",
    "eu-central-1c",
    "eu-central-1c",
    "eu-central-1c"
  ],
  "NODES_NAMES": [
    "ip-192-168-15-156.eu-central-1.compute.internal",
    "ip-192-168-17-29.eu-central-1.compute.internal",
    "ip-192-168-30-121.eu-central-1.compute.internal",
    "ip-192-168-40-84.eu-central-1.compute.internal",
    "ip-192-168-49-244.eu-central-1.compute.internal",
    "ip-192-168-60-3.eu-central-1.compute.internal",
    "ip-192-168-81-120.eu-central-1.compute.internal",
    "ip-192-168-82-150.eu-central-1.compute.internal",
    "ip-192-168-84-51.eu-central-1.compute.internal"
  ],
  "NODE_SSH_KEY": "~/.ssh/id_rsa",
  "HOST_EXT_IP": "22.22.22.22",
  "VERIFY_EXT_IP": "",
  "AWS_LB_TYPE": "clb",
  "USE_ARN": "Y",
  "ARN_AWS_IAM": "arn:aws:acm:XXXX",
  "LB_ADD": "",
  "REDIS_URL": "",
  "REDIS_TYPE": "",
  "REDIS_PW": "",
  "REDIS_USE_SSL": "false",
  "REDIS_SSL_TRUSTSTORE": "",
  "REDIS_SENTINEL_GROUP": "",
  "DEPLOYMENT_ARCH": "eks",
  "PERSISTENCE_BACKEND": "couchbase",
  "INSTALL_COUCHBASE": "N",
  "COUCHBASE_NAMESPACE": "cbns",
  "COUCHBASE_VOLUME_TYPE": "io1",
  "COUCHBASE_CLUSTER_NAME": "cbgluu",
  "COUCHBASE_FQDN": "*.cbns.svc.cluster.local",
  "COUCHBASE_URL": "cbgluu.cbns.svc.cluster.local",
  "COUCHBASE_USER": "admin",
  "COUCHBASE_PASSWORD": "Test1234#",
  "COUCHBASE_CRT": "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURUakNDQWphZ0F3SUJBZ0lVRVRyRlZRWTlYdk5aUzBoLzFKRkRRMzR0WGVvd0RRWUpLb1pJaHZjTkFRRUwKQlFBd0Z6RVZNQk1HQTFVRUF3d01RMjkxWTJoaVlYTmxJRU5CTUI0WERUSXdNRE15TlRFd01URXdOMW9YRFRNdwpNRE15TXpFd01URXdOMW93RnpFVk1CTUdBMVVFQXd3TVEyOTFZMmhpWVhObElFTkJNSUlCSWpBTkJna3Foa2lHCjl3MEJBUUVGQUFPQ0FROEFNSUlCQ2dLQ0FRRUFuZlEyQWVXZnVmVDFySC9DOFpoUlUzREUrTnlxT3FHaTN0bm0KL2RyNzh5Z2Y0aFJ0b2VtUFRNdWhqZFl3MWRCazh6ZmgraU1WYXdHS0dxR04rVGNLZ3UvMVh1WVRJbXZYcjZFVAp6YUVURVhzTEV2ai90NjlTS0Q3dnM2U2s5cnhYQ2d5VjcyZmhRVUNJNUZPdk9IS1BiSUMxYm5jaGp4S29FZlNrCkNJNmVvcjROcytodG05MWFRZnphblgrbkNmZVliSWFScXRYclpyTS9iQ1VHN3NQanBWV3Z1N2tlTWJQcXZxeVUKWXB0U0VMWnFQbnlKYUhJdGdMTXFqaEY4WVRMNE84TUZGRFEzc0NRKzB0NmJrd1k2aWg4ckFzRHphcHM1VGRKdApKZGpWSjdObEx3Ti9iOVc2Ky9nQ2wxVjNoQTdaN21oMUk0eHZWK3ZEUldxZXBPamdNd0lEQVFBQm80R1JNSUdPCk1Bd0dBMVVkRXdRRk1BTUJBZjh3Q3dZRFZSMFBCQVFEQWdFR01CMEdBMVVkRGdRV0JCU0QzMXNZY3kreUJFTnoKbXFqbnV3VExzQ0VrZWpCU0JnTlZIU01FU3pCSmdCU0QzMXNZY3kreUJFTnptcWpudXdUTHNDRWtlcUVicEJrdwpGekVWTUJNR0ExVUVBd3dNUTI5MVkyaGlZWE5sSUVOQmdoUVJPc1ZWQmoxZTgxbExTSC9Va1VORGZpMWQ2akFOCkJna3Foa2lHOXcwQkFRc0ZBQU9DQVFFQVdFQ2pmOW4wb3hHUGJSaXQ4bkxlQ0V1TnNMdDNQdlJuVjdRclZsZ3AKOXF4YjBMZExtKzlQOWl4cUdBZHlQNWg2c0pqdytwMlJZVUxTdXhCYkxXd0orcXJzVEw1QVR6ZWZKWWRJaVl0SgpKUkRwbVBVTzVIWWROQ0xlQ21xdy90QWxvWkVzeThWZGUvbUtyN0x6QnlmWXdXZzBiN2IzZS9ZOEMwS2NwaXcwCnMzNDNIYWoycjVsU3ZVV3JueDVjNkU0aTlXV2I1cG1yVnFNUCtrY1Y1amNtNlVML2V2ak05OTU1dkplbW5pNHQKUzI4SWY4cGZvUlJFRFJ0c1dBVytzMElaMmN3bnJWbHFsMm9FR2NRb0JUQmhmWitMMlZUK3BiUE1SNmpOWnNOOAo5eUthUjdFOXRrdWtSWmlJSmlQTzVEVUxQTXVmS0t6UFJDZzBjdTA5ekN4OFhRPT0KLS0tLS1FTkQgQ0VSVElGSUNBVEUtLS0tLQo=",
  "COUCHBASE_CN": "Couchbase CA",
  "COUCHBASE_SUBJECT_ALT_NAME": [
    "*.cbgluu.cbns.svc",
    "*.cbns.svc",
    "*.cbgluu.*.cbns.svc.cluster.local",
    "*.cbns.testingluuk8.org",
    "*.cbns.svc.cluster.local",
    "cbns.svc.cluster.local",
    "*.cbgluu.cbns.svc.cluster.local",
    "cbgluu.cbns.svc.cluster.local"
  ],
  "COUCHBASE_CLUSTER_FILE_OVERRIDE": "Y",
  "COUCHBASE_USE_LOW_RESOURCES": "N",
  "COUCHBASE_DATA_NODES": "",
  "COUCHBASE_QUERY_NODES": "",
  "COUCHBASE_INDEX_NODES": "",
  "COUCHBASE_SEARCH_EVENTING_ANALYTICS_NODES": "",
  "COUCHBASE_GENERAL_STORAGE": "",
  "COUCHBASE_DATA_STORAGE": "",
  "COUCHBASE_INDEX_STORAGE": "",
  "COUCHBASE_QUERY_STORAGE": "",
  "COUCHBASE_ANALYTICS_STORAGE": "",
  "NUMBER_OF_EXPECTED_USERS": "",
  "EXPECTED_TRANSACTIONS_PER_SEC": "",
  "USING_CODE_FLOW": "",
  "USING_SCIM_FLOW": "",
  "USING_RESOURCE_OWNER_PASSWORD_CRED_GRANT_FLOW": "",
  "DEPLOY_MULTI_CLUSTER": "N",
  "HYBRID_LDAP_HELD_DATA": "cache",
  "LDAP_VOLUME": "io1",
  "LDAP_VOLUME_TYPE": 7,
  "LDAP_STATIC_VOLUME_ID": "",
  "LDAP_STATIC_DISK_URI": "",
  "OXTRUST_OXSHIBBOLETH_SHARED_VOLUME_TYPE": "local_storage",
  "ACCEPT_EFS_NOTES": "",
  "EFS_FILE_SYSTEM_ID": "",
  "EFS_AWS_REGION": "",
  "EFS_DNS": "",
  "GLUU_CACHE_TYPE": "NATIVE_PERSISTENCE",
  "GLUU_NAMESPACE": "gluu",
  "GLUU_FQDN": "gluu.testingluuk8.org",
  "COUNTRY_CODE": "US",
  "STATE": "TX",
  "EMAIL": "support@gluu.org",
  "CITY": "Austin",
  "ORG_NAME": "Gluu",
  "GMAIL_ACCOUNT": "",
  "GOOGLE_NODE_HOME_DIR": "",
  "IS_GLUU_FQDN_REGISTERED": "Y",
  "LDAP_PW": "Test1234#",
  "ADMIN_PW": "Test1234#",
  "OXD_SERVER_PW": "crz7wyEVxVTJ",
  "OXD_APPLICATION_KEYSTORE_CN": "oxd-server",
  "OXD_ADMIN_KEYSTORE_CN": "oxd-server",
  "LDAP_STORAGE_SIZE": "40Gi",
  "OXTRUST_OXSHIBBOLETH_SHARED_STORAGE_SIZE": "4Gi",
  "NFS_STORAGE_SIZE": "4Gi",
  "OXAUTH_REPLICAS": 1,
  "OXTRUST_REPLICAS": 1,
  "LDAP_REPLICAS": 1,
  "OXSHIBBOLETH_REPLICAS": 1,
  "OXPASSPORT_REPLICAS": 1,
  "OXD_SERVER_REPLICAS": 1,
  "CASA_REPLICAS": "1",
  "RADIUS_REPLICAS": 1,
  "ENABLE_OXTRUST_API": "N",
  "ENABLE_OXTRUST_TEST_MODE": "N",
  "ENABLE_CACHE_REFRESH": "Y",
  "ENABLE_OXD": "Y",
  "ENABLE_RADIUS": "Y",
  "ENABLE_OXPASSPORT": "Y",
  "ENABLE_OXSHIBBOLETH": "Y",
  "ENABLE_CASA": "Y",
  "ENABLE_KEY_ROTATE": "Y",
  "ENABLE_OXTRUST_API_BOOLEAN": "true",
  "ENABLE_OXTRUST_TEST_MODE_BOOLEAN": "false",
  "ENABLE_RADIUS_BOOLEAN": "true",
  "ENABLE_OXPASSPORT_BOOLEAN": "true",
  "ENABLE_CASA_BOOLEAN": "true",
  "ENABLE_SAML_BOOLEAN": "true",
  "EDIT_IMAGE_NAMES_TAGS": "N",
  "CASA_IMAGE_NAME": "gluufederation/casa",
  "CASA_IMAGE_TAG": "4.2.0_dev",
  "CONFIG_IMAGE_NAME": "gluufederation/config-init",
  "CONFIG_IMAGE_TAG": "4.1.1_01",
  "CACHE_REFRESH_ROTATE_IMAGE_NAME": "gluufederation/cr-rotate",
  "CACHE_REFRESH_ROTATE_IMAGE_TAG": "4.1.1_01",
  "KEY_ROTATE_IMAGE_NAME": "gluufederation/key-rotation",
  "KEY_ROTATE_IMAGE_TAG": "4.1.1_01",
  "LDAP_IMAGE_NAME": "gluufederation/wrends",
  "LDAP_IMAGE_TAG": "4.1.1_01",
  "OXAUTH_IMAGE_NAME": "gluufederation/oxauth",
  "OXAUTH_IMAGE_TAG": "4.1.1_01",
  "OXD_IMAGE_NAME": "gluufederation/oxd-server",
  "OXD_IMAGE_TAG": "4.1.1_01",
  "OXPASSPORT_IMAGE_NAME": "gluufederation/oxpassport",
  "OXPASSPORT_IMAGE_TAG": "4.1.1_01",
  "OXSHIBBOLETH_IMAGE_NAME": "gluufederation/oxshibboleth",
  "OXSHIBBOLETH_IMAGE_TAG": "4.1.1_01",
  "OXTRUST_IMAGE_NAME": "gluufederation/oxtrust",
  "OXTRUST_IMAGE_TAG": "4.1.1_01",
  "PERSISTENCE_IMAGE_NAME": "gluufederation/persistence",
  "PERSISTENCE_IMAGE_TAG": "4.1.1_01",
  "RADIUS_IMAGE_NAME": "gluufederation/radius",
  "RADIUS_IMAGE_TAG": "4.1.1_01",
  "UPGRADE_IMAGE_NAME": "gluufederation/upgrade",
  "UPGRADE_IMAGE_TAG": "4.1.1_01",
  "CONFIRM_PARAMS": "Y",
  "REDIS_PASSWORD": ""
}
```


### Load-test

Our tests used 50 million users that were loaded to our `gluu_user` bucket. We have created a docker image to load users rapidly using the couchbase client. That same image is also used to load test Gluu using jmeter tests for both `ROPC` and `Authorization code` flows. This image will load users and use the same password for each `topsecret`. Our tests were conducted on users with the same password as well as users with unique passwords for each.

#### Loading users

1. Create a folder called `add_users`.

    ```bash
    mkdir add_users && cd add_users
    ```
1. Copy the following yaml into the folder under the name `load_users.yaml`.

    !!!note
       This job uses parallel jobs and needs at minimum of `18000m` CPU to function at the level needed. 

    ```yaml
    apiVersion: v1
    data:
      COUCHBASE_PW: Test1234#
      COUCHBASE_URL: cbgluu.cbns.svc.cluster.local
      LOAD_USERS_TO_COUCHBASE: "true"
      NUMBERS_OF_USERS_TO_LOAD: "50000000"
    kind: ConfigMap
    metadata:
      labels:
        app: load-users
      name: load-users-cm
    ---
    apiVersion: batch/v1
    kind: Job
    metadata:
      labels:
        app: load-users
      name: load-users
    spec:
      template:
        metadata:
          labels:
            app: load-users
        spec:
          containers:
          - envFrom:
            - configMapRef:
                name: load-users-cm
            image: abudayyehwork/loadtesting:4.0.0_dev
            name: load-users
            resources:
              limits:
                cpu: 19000m
                memory: 5000Mi
              requests:
                cpu: 19000m
                memory: 5000Mi
          restartPolicy: Never
    ```

1. Create a namespace for load-testing.

    ```bash
    kubectl create ns load
    ```
   
1. Create `load_users.yaml`

    ```bash
    kubectl create -f load_users.yaml -n load
    ```
   
!!!note
   It takes around 23 mins to load 50 million users to couchbase `gluu_user` bucket.
   
#### Load testing

##### ROPC client registration

###### Resources needed for ROPC client  jmeter test

| NAME                                     | # of pods   | RAM(GiB) | CPU | Total RAM(GiB) | Total CPU |
| ---------------------------------------- | ----------- | -------  | --- | -------------  | --------- |
| ROPC jmeter test                         | 100         |  4       |  4  | 400            | 400       |
| Grand Total                              |             |          |     | 400 GiB        | 400       |

###### Setup Client

1. Open Gluu GUI , `OpenId Connect -> Clients --> Add New Client`

1.  Create client with the following details:

    ```
    Client Secret: test_ro_client_password
    Client Name: test_ro
    Authentication method for the Token Endpoint:: client_secret_post
    Client Expiration Date: +few years from now
    Grant Types: password
    Response: id_token
    ```

1. Save `Client ID` and `Client Secret` if changed from above.

##### Authorization code client

###### Resources needed for Authorization code client jmeter test

| NAME                                     | # of pods   | RAM(GiB) | CPU | Total RAM(GiB) | Total CPU |
| ---------------------------------------- | ----------- | -------  | --- | -------------  | --------- |
| Authorization code flow jmeter test      | 500         |  4       |  4  | 2000           | 2000      |
| Grand Total                              |             |          |     | 2000 GiB       | 2000       |

###### Setup Client

1. Open Gluu GUI , `OpenId Connect -> Clients -> oxTrust client`

1. Save `Client ID` and `Client Secret`

!!!note
   A seperate client can be created for this test similar to oxTrust client

##### Initiate load test

1. Create a folder called `load_test`.

    ```bash
    mkdir load_test && cd load_test
    ```

1. Copy the following yaml into the folder under the name `load.yaml`.
    
    ```yaml
    apiVersion: v1
    data:
      AUTHZ_CLIENT_ID: 1001.21beb9f2-e8de-4b10-949f-5cf31a28f95b # Saved from steps above
      AUTHZ_CLIENT_SECRET: FWLmNKmVcQZt # Saved from steps above
      # First batch is the users from min - max that login 10% every time
      FIRST_BATCH_MAX: "5000000" 
      FIRST_BATCH_MIN: "0"
      # Second batch is the users from min - max that login 90% every time
      SECOND_BATCH_MAX: "50000000"
      SECOND_BATCH_MIN: "5000001"
      # Regex of Gluu URL demoexample.gluu.org
      GLUU_REGEX_PART1: demoexample
      GLUU_REGEX_PART2: gluu
      GLUU_REGEX_PART3: org
      GLUU_URL: demoexample.gluu.org
      ROPC_CLIENT_ID: c1b9628e-84f5-43e6-bf00-b341543703d9 # Saved from steps above
      ROPC_CLIENT_SECRET: test_ro_client_password # Saved from steps above
      RUN_AUTHZ_TEST: "true" # or "false"
      RUN_ROPC_TEST: "true" # or "false"
    kind: ConfigMap
    metadata:
      labels:
        app: load-testing
      name: load-testing-cm
    ---
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      labels:
        app: load-testing
      name: load-testing
    spec:
      replicas: 1
      selector:
        matchLabels:
          app: load-testing
      template:
        metadata:
          labels:
            app: load-testing
        spec:
          containers:
          - envFrom:
            - configMapRef:
                name: load-testing-cm
            image: abudayyehwork/loadtesting:4.0.0_dev
            imagePullPolicy: Always
            name: load-testing
            resources:
              requests:
                memory: "4000Mi"
                cpu: "4000m"
              limits:
                memory: "4000Mi"
                cpu: "4000m"
    ```
    
1. Create a namespace for load-testing if it hasn't been created yet.

    ```bash
    kubectl create ns load
    ```
   
1. Create `load.yaml`

    ```bash
    kubectl create -f load.yaml -n load
    ```
   
1. Scale oxAuth to the number of pods according to flow. A mix and match if the total number of authentication per day is the same i.e one billion.

    ```bash
    # ROPC Flow
    kubectl scale deploy oxauth -n gluu --replicas=100
    # OR Authorization code Flow
    kubectl scale deploy oxauth -n gluu --replicas=500
    # OR if both flows and both need to reach one billion sepretly. Note the resource tables in the beginning of this tutorial.
    kubectl scale deploy oxauth -n gluu --replicas=600
    ```

1. Scale load test according to flow.

    ```bash
    # ROPC Flow
    kubectl scale deploy load-testing -n load --replicas=100
    # OR Authorization code Flow
    kubectl scale deploy load-testing -n load --replicas=500
    # OR if both flows and both need to reach one billion sepretly. Note the resource tables in the beginning of this tutorial.
    kubectl scale deploy load-testing -n load --replicas=600
    ```

### Install Monitoring tools

!!!note
   This section is used for testing purposes and setup of these tools in production should consult official docs for each tool. 

1. Create a folder called `monitor`.

    ```bash
    mkdir minitor && cd monitor
    ```

1. Copy the following bash script into the folder under the name `setup_helm_prometheus_grafana.sh`. Change the password for user `admin` below as needed. This will install helm v3 , Prometheus and Grafana.

    ```bash
    #!/bin/bash
    echo "Installing Helm V3"
    curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3
    chmod 700 get_helm.sh
    ./get_helm.sh
    echo "Installing Prometheus"
    kubectl create namespace prometheus
    helm install prometheus stable/prometheus \
        --namespace prometheus \
        --set alertmanager.persistentVolume.storageClass="gp2" \
        --set server.persistentVolume.storageClass="gp2"
    sleep 60
    echo "Installing Grafana"
    kubectl create namespace grafana
    helm install grafana stable/grafana \
        --namespace grafana \
        --set persistence.storageClassName="gp2" \
        --set adminPassword='myPasswOrd#' \
        --set datasources."datasources\.yaml".apiVersion=1 \
        --set datasources."datasources\.yaml".datasources[0].name=Prometheus \
        --set datasources."datasources\.yaml".datasources[0].type=prometheus \
        --set datasources."datasources\.yaml".datasources[0].url=http://prometheus-server.prometheus.svc.cluster.local \
        --set datasources."datasources\.yaml".datasources[0].access=proxy \
        --set datasources."datasources\.yaml".datasources[0].isDefault=true \
        --set service.type=LoadBalancer
    sleep 60
    ELB=$(kubectl get svc -n grafana grafana -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
    echo "Grafana URL:"
    echo "http://$ELB"
    ```
   
1. Login into the URL of Grafana or the ip of the loadbalancer created as `admin` and `myPasswOrd` in our example. Several dashboards can be added but the most important one here is pod monitoring. After login, press `+` on the left panel, select `Import`, and enter `6417` for the dashboard id , `Prometheus` as the data source endpoint then press `Import`.

1. Create a dashbord to track requests to pods using the `nginx` metrics in the query section. The metrics are tuned as needed.

### Results

<div>
    <a href="https://plotly.com/~git-gluu/1/?share_key=jqcylzHdH4hoDYwJ1bqy4h" target="_blank" title="load_test" style="display: block; text-align: center;"><img src="https://plotly.com/~git-gluu/1.png?share_key=jqcylzHdH4hoDYwJ1bqy4h" alt="load_test" style="max-width: 100%;width: 600px;"  width="600" onerror="this.onerror=null;this.src='https://plotly.com/404.png';" /></a>
    <script data-plotly="git-gluu:1" sharekey-plotly="jqcylzHdH4hoDYwJ1bqy4h" src="https://plotly.com/embed.js" async></script>
</div>

