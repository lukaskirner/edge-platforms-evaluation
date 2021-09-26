import random
import pathlib
import pandas as pd
from time import sleep
from paho.mqtt import client as mqtt_client


broker = 'test.mosquitto.org'
port = 1883
topic = "lkirner/flow"
client_id = f'python-mqtt-{random.randint(0, 1000)}'

root = f'{pathlib.Path(__file__).parent.absolute()}/data/march_by_inovex'
transformed_path = f'{root}/transformed'
data_path = f'{transformed_path}/freq_group_2_vals.pkl'


def mqtt_connect():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    
    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def mqtt_publish(client, msg):
    result = client.publish(topic, msg)
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")
         

mqtt_client = mqtt_connect()
df = pd.read_pickle(data_path)

for value in df[df.columns[8]].tolist():
    mqtt_publish(mqtt_client, value)
    sleep(1)