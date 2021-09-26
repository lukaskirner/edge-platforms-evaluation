# CoreDNS - Home
This docker images provides a local DNS server which resolves to the testing machines

### How to use
Simply build and run the docker image
```
docker build --pull --rm -f "Dockerfile" -t thesis-coredns:latest
docker run --rm -d -p 53:53/tcp -p 53:53/udp thesis-coredns:latest
```

### Configuration
The docker images uses [CoreDNS](https://coredns.io/). Configure the `edge.home` zone with your ip adress