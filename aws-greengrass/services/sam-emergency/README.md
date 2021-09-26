# sam-emergency

## Deployment

### Build
```
make build
```

### Deploy Lambda
```
make deploy
```
AWS Console > Lambda > this lambda > Publish Version


### Deploy to Greengrass Core
1. Create component (IoT Core > Greengrass > components)
    - Select lambda
    - timeout 10s
    - Memory 128 MB or more
    - Greengrass container
    - Event sources
        - `sensor/#`
2. Deploy
    - add to deployment
    - configure Lambda deployment
        - Access control -  Add the following policy during the deployment (replace `<any-uniquename>`):
            ```
            {
                "accessControl": {
                    "aws.greengrass.ipc.pubsub": {
                    "<any-uniquename>:1": {
                        "operations": [
                        "aws.greengrass#PublishToTopic"
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

## Important Notes
The topic `sensor/#` needs to be mapped to the PubSub therefor configuration needs to be done at the MQTT Bridge
- aws.greengrass.clientdevices.mqtt.Bridge:
    ```
    {
        "mqttTopicMapping": {
            "SensorMapping": {
                "topic": "sensor/#",
                "source": "LocalMqtt",
                "target": "PubSub" <----- this one is important
            },
            ...
        }
    }
    ```
