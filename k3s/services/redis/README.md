# Install Redis

### Prerequisites
- Kubernetes
- kubectl configured
- Helm

### What is getting installed?
1. redis (database) -> https://github.com/bitnami/charts/tree/master/bitnami/redis

### Installing the Helm Chart
1. Add emqx to helm repo
    ```
    helm repo add bitnami https://charts.bitnami.com/bitnami
    ```
2. Install influxdb with configuration file
    ```
    helm install redis -f ./redis.yaml bitnami/redis
    ```

### Update values
```
helm upgrade --recreate-pods redis -f ./redis.yaml bitnami/redis
```

### Accessing redis with local machine
```
kubectl port-forward svc/redis-master 6379:6379

# Get Redis password
export REDIS_PASSWORD=$(kubectl get secret --namespace default redis -o jsonpath="{.data.redis-password}" | base64 --decode)
echo $REDIS_PASSWORD
```

### Uninstalling the Helm Charts
```
helm del redis
```
