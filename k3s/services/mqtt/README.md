# Install MQTT Broker

### Prerequisites
- Kubernetes
- kubectl configured
- Helm

### Installing the Helm Chart
1. Add emqx to helm repo
    ```
    helm repo add emqx https://repos.emqx.io/charts
    ```
2. Install with configuration file
    ```
    helm install mqtt -f ./emqx.yaml -n mqtt emqx/emqx --version 4.2.7
    ```

### Update values
```
helm upgrade --recreate-pods -f ./emqx.yaml -n mqtt mqtt emqx/emqx --version 4.2.7
```

### Uninstalling the Helm Chart
```
helm del mqtt
```

#### EMQ Dashboard
Can be accessed from your browser via `<ip_of_one_node>:18083`

Default credentials are:
- username: `admin`
- password: `public`


#### Source:
https://www.emqx.io/blog/rapidly-deploy-emqx-clusters-on-kubernetes-via-helm
