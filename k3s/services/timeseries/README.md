# Install Influx with chronograf web GUI

### Prerequisites
- Kubernetes
- kubectl configured
- Helm

### What is getting installed?
1. influxdb (database) -> https://artifacthub.io/packages/helm/influxdata/influxdb
2. telegraf (collector) -> https://artifacthub.io/packages/helm/influxdata/telegraf

### Installing the Helm Charts
1. Add emqx to helm repo
    ```
    helm repo add influxdata https://helm.influxdata.com/
    ```
2. Install influxdb with configuration file
    ```
    helm install influxdb -f ./influxdb.yaml -n timeseries influxdata/influxdb --version 4.9.14
    ```
3. Install telegraf with configuration file
    ```
    helm install telegraf -f ./telegraf.yaml -n timeseries influxdata/telegraf --version 1.7.38
    ```

### Update values
```
helm upgrade --recreate-pods influxdb -f ./influxdb.yaml -n timeseries influxdata/influxdb --version 4.9.14
helm upgrade --recreate-pods telegraf -f ./telegraf.yaml -n timeseries influxdata/telegraf --version 1.7.38
```

### Uninstalling the Helm Charts
```
helm del influxdb -n timeseries
helm del telegraf -n timeseries
```
