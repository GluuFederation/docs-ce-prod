# Using Datadog and Prometheus with Gluu Cloud Native edition

### Prerequisites

- Datadog Agent 6.5.0+

## Instructions

1. Install Gluu server using one of the following
  - [Kustomize](https://github.com/GluuFederation/enterprise-edition/blob/4.1/pygluu/kubernetes/templates/README.md#install-gluu-using-pygluu-kubernetes-with-kustomize)
  - [Helm](https://github.com/GluuFederation/enterprise-edition/blob/4.1/pygluu/kubernetes/templates/README.md#install-gluu-using-helm)
  
1. Create a directory called monitoring for the manifests needed. 
  
    ```bash
    mkdir monitoring && cd monitoring
    ```

1. Get zip file of manifests and unzip

      ```bash
      wget https://github.com/GluuFederation/enterprise-edition/raw/4.1/monitoring.zip
      unzip monitoring.zip
      ```

1. Create a namespace for Datadog and Prometheus

    ```bash
    kubectl create ns datadog
    kubectl create ns prometheus
    ```

## Using Kubectl commands

1. Configure RBAC permissions for the datadog agent in `datadog` namespace.   

    ```bash
    kubectl create -f "https://raw.githubusercontent.com/DataDog/datadog-agent/master/Dockerfiles/manifests/rbac/clusterrole.yaml" -ns datadog
    kubectl create -f "https://raw.githubusercontent.com/DataDog/datadog-agent/master/Dockerfiles/manifests/rbac/serviceaccount.yaml" -ns datadog
    kubectl create -f "https://raw.githubusercontent.com/DataDog/datadog-agent/master/Dockerfiles/manifests/rbac/serviceaccount.yaml" -ns datadog
   ```
   
1. Create a `Secret` containing datadog API key. It will be used in datadog agent Daemonset.

   !!!warning
       If the name of the secret below is to be changed , change it in the respective `DaemonSet` as well.

    ```bash
    kubectl create secret generic datadog-secret --from-literal api-key="<API-KEY>"
    ```

1. Create a Datadog agent with custom metrics and APM logs collection enabled.

    ```bash
    kubectl apply -f datadog/
    ```
1. Install Prometheus

    ```bash
    kubectl apply -f prometheus/
    ```

    !!!note 
        For datadog and prometheus integration, prometheus deployment has the  annotations that allow datadog autodiscovery feature and gets all the metrics that prometheus collects from the cluster.
        
      ```yaml
            annotations:
                ad.datadoghq.com/prometheus.check_names: |
                  ["openmetrics"]
                ad.datadoghq.com/prometheus.init_configs: |
                  [{}]
                ad.datadoghq.com/prometheus.instances: |
                  [
                    {
                      "prometheus_url": "http://%%host%%:%%port%%/metrics",
                      "namespace": "monitoring",
                      "metrics": [ {"promhttp_metric_handler_requests_total": "prometheus.handler.requests.total"}]
                    }
                  ]
      ```

1. [Optional] Install kube state metrics which exposes all the metrics on /metrics URI. Prometheus can scrape all the metrics exposed by kube state metrics. This will be created in the `kube-system` namespace.

    ```bash
    kubectl apply -f kube-state-metrics/
    ```

    1. Add the following configuration as part of prometheus job configuration.
    
      ```yaml
      - job_name: 'kube-state-metrics'
        static_configs:
          - targets: ['kube-state-metrics.kube-system.svc.cluster.local:8080']
      ```

    !!!note
        This part has been included in by default in [proth-cm](/prometheus/proth-cm.yaml). If it is not being used, it should be removed. If not it will cause health check error in prometheus targets.

## Using helm

### Prerequisites
- Helm 2.10+
- Tiller

### Datadog

1. Install Datadog

    ```bash
    helm install --name datadog-agent-v1 \
      --set datadog.apiKey=<DataDog API Key> \
      --set datadog.apmEnabled=true \
      --set datadog.logsEnabled=true \
      stable/datadog
      --namespace datadog
    
    ```
   
1. Install prometheus

    !!!note
        The custom [`values.yaml`](/helm/prometheus-values.yaml) file above has the annotations needed to integrate datadog with prometheus.
    
    ```bash
    helm install --name prometheus --namespace prometheus -f helm/prometheus-values.yaml stable/prometheus
    ```

    1. Access prometheus UI via port-forwarding or switch prometheus service upon installation to `LoadBalancer`
    
        ```bash
        export PROMETHEUS_POD_NAME=$(kubectl get pods --namespace prometheus -l "app=prometheus,component=server" -o jsonpath="{.items[0].metadata.name}")
        kubectl --namespace prometheus port-forward PROMETHEUS_POD_NAME 9090
        ```    

1. [Optional] Install kube state metrics which exposes all the metrics on /metrics URI. Prometheus can scrape all the metrics exposed by kube state metrics. This will be created in the `kube-system` namespace.

    ```bash
    helm2 install --name kube-state stable/kube-state-metrics
    ```

    1. Add the kube-state metrics job in prometheus serverFiles.
    
      ```yaml
            - job_name: 'kube-state-metrics'
              static_configs:
                - targets: ['kube-state-kube-state-metrics.default.svc.cluster.local:8080']
      ```

!!!note
    All the metrics will be exported to datadog `metrics` -> `summary`