

### How to build ARM images on x86 ([Source](https://www.docker.com/blog/getting-started-with-docker-for-arm-on-linux/))
1. Add new builder
    ```
    docker buildx create --name multiarch
    ```
2. Switch to `multiarch` builder
    ```
    docker buildx use multiarch
    ```
3. Build image
    ```
    docker buildx build --platform linux/arm/v8 -t registry.inovex.de:4567/lkirner/edge-platforms-evaluation/detector:latest --push .
    ```



### Deployment
```
{
  "accessControl": {
    "aws.greengrass.ipc.pubsub": {
      "de.inovex.lkirner.detector:pubsub:1": {
        "operations": [
          "aws.greengrass#PublishToTopic",
          "aws.greengrass#SubscribeToTopic"
        ],
        "policyDescription": "Allows access to publish to all topics.",
        "resources": [
          "*"
        ]
      }
    }
  }
}
```


### Also important
- enable IPC in docker container [link](https://docs.aws.amazon.com/greengrass/v2/developerguide/run-docker-container.html#docker-container-ipc)
