


## AWS Setup

aws.greengrass.clientdevices.Auth:
```
{
  "deviceGroups": {
    "formatVersion": "2021-03-05",
    "definitions": {
      "MyDeviceGroup": {
        "selectionRule": "thingName: *",
        "policyName": "MyPermissivePolicy"
      }
    },
    "policies": {
      "MyPermissivePolicy": {
        "AllowAll": {
          "statementDescription": "Allow client devices to perform all actions.",
          "operations": [
            "*"
          ],
          "resources": [
            "*"
          ]
        }
      }
    }
  }
}
```

aws.greengrass.clientdevices.mqtt.Bridge:
```
{
  "mqttTopicMapping": {
    "SensorMapping": {
      "source": "LocalMqtt",
      "target": "Pubsub",
      "topic": "sensor/#"
    },
    "ActorMapping": {
      "source": "Pubsub",
      "target": "IotCore",
      "topic": "actor/#"
    },
    "ActorMappingLocalMqtt": {
      "source": "Pubsub",
      "target": "LocalMqtt",
      "topic": "actor/#"
    }
  }
}
```

S3 Bucket acces policy for ThingGroup (docker-compose files for components)
```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "s3:GetObject",
      "Resource": "*",
      "Effect": "Allow"
    }
  ]
}
```
