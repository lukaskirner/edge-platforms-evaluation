# Install ping-pong services

1. ping backend
2. pong backend


#### Add docker registrry pull credentials to cluster
```
kubectl create secret docker-registry gitlab-pull-secrets -n default --docker-server=registry.inovex.de:4567 --docker-username=k3s --docker-password=${CONTAINER_REGISTRY_TOKEN}
```
