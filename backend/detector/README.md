

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
    docker buildx build --platform linux/arm/v7 -t registry.inovex.de:4567/lkirner/edge-platforms-evaluation/detector:latest --push .
    ```