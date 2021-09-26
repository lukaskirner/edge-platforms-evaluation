import time
import json
import random
from io import BytesIO
from base64 import b64encode
from picamera import PiCamera
from paho.mqtt import client as mqtt_client

# camera config
camera = PiCamera()
camera.rotation = 180
camera.resolution = (320, 320)

# mqtt config
broker = 'master.fritz.box'
port = 1883
topic = "sensor/camera"
client_id = f'sensor-camera-{random.randint(0, 1000)}'

def take_image():
    buffer = BytesIO()
    camera.capture(buffer, format='jpeg')
    return b64encode(buffer.getvalue())

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish_msg(client, msg):
    data = {"id": client_id, "image": msg.decode('ascii'), "encoding": "base64"}    
    result = client.publish(topic, json.dumps(data))
    status = result[0]
    if status == 0:
        print(f"Send message to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")

def main():
    client = connect_mqtt()
    while True:
        base64_image = take_image()
        publish_msg(client, base64_image)
        time.sleep(5)
    

if __name__ == '__main__':
    main()
