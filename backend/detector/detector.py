import os
import json
import random
import pathlib
from PIL import Image
from io import BytesIO
from base64 import b64decode
from paho.mqtt import client as mqtt_client
from pycoral.adapters import classify
from pycoral.adapters import common
from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter

# Google Coral USB accelerator config
root = f'{pathlib.Path(__file__).parent.absolute()}'
labels = read_label_file(f'{root}/data/labels.txt')
interpreter = make_interpreter(f'{root}/data/model.tflite')
interpreter.allocate_tensors()
size = common.input_size(interpreter)

# mqtt config
broker = os.getenv('MQTT_HOST', 'elb-emqx-service.mqtt.svc.cluster.local')
port = 1883
topic = "sensor/camera"
pub_topic = "actor/detector"
client_id = f'detector-{random.randint(0, 1000)}'

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

def on_message(client, userdata, msg):
    print(f"Received message from `{msg.topic}` topic")
    data = json.loads(msg.payload.decode())
    img = Image.open(BytesIO(b64decode(data['image']))).convert('RGB').resize(size, Image.ANTIALIAS)

    # classification
    common.set_input(interpreter, img)
    interpreter.invoke()
    classes = classify.get_classes(interpreter, 3, 0.0)

    results = []
    for c in classes:
        results.append({
            "label": "%s2" % labels.get(c.id, c.id),
            "score": "%.5f" % c.score
        })
    
    publish_msg(client, results)

def publish_msg(client, msg):
    data = {"id": client_id, "results": msg}    
    result = client.publish(pub_topic, json.dumps(data))
    status = result[0]
    if status == 0:
        print(f"Send message to topic `{pub_topic}`")
    else:
        print(f"Failed to send message to topic {pub_topic}")

def base64_to_image(data):
    b64decode(data, validate=True)
    return Image.open(BytesIO(b64decode(data)))

def main():
    client = connect_mqtt()
    client.subscribe(topic)
    client.on_message = on_message
    client.loop_forever()

if __name__ == '__main__':
    main()
