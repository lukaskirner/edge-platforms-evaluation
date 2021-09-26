import sys
import time
import json
import logging
import pathlib
from PIL import Image
from io import BytesIO
from base64 import b64decode
from pycoral.adapters import classify
from pycoral.adapters import common
from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter
import awsiot.greengrasscoreipc
from awsiot.greengrasscoreipc.model import PublishToTopicRequest, PublishMessage, JsonMessage
from flask import Flask, request
app = Flask(__name__)

# Setup logging to stdout
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

# IPC PubSub
ipc_client = awsiot.greengrasscoreipc.connect()
SUB_TOPIC = "sensor/camera"
PUB_TOPIC = "actor/detector"

# Google Coral USB accelerator config
root = f'{pathlib.Path(__file__).parent.absolute()}'
labels = read_label_file(f'{root}/data/labels.txt')
interpreter = make_interpreter(f'{root}/data/model.tflite')
interpreter.allocate_tensors()
size = common.input_size(interpreter)

TIMEOUT = 10

@app.route('/images', methods = ['POST'])
def process_image():
    logger.info("Received message!")
    request_data = request.get_json()
    img = Image.open(BytesIO(b64decode(request_data['image']))).convert('RGB').resize(size, Image.ANTIALIAS)
    
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
    
    logger.info(f'Received ML results: {results}')

    try:
        message = {"results": results}
        message_json = json.dumps(message).encode('utf-8')
        pub_request = PublishToTopicRequest()
        pub_request.topic = PUB_TOPIC
        publish_message = PublishMessage()
        publish_message.json_message = JsonMessage()
        publish_message.json_message.message = message
        pub_request.publish_message = publish_message
        operation = ipc_client.new_publish_to_topic()
        operation.activate(pub_request)
        future = operation.get_response()
        future.result(TIMEOUT)
        logger.info(f'Triggering publish to topic "{PUB_TOPIC}" with payload {message}')
    except Exception as e:
        logger.error(f'Failed to trigger publish to topic "{PUB_TOPIC}" with with payload {message}: {repr(e)}')
        return json.dumps({"status": 500})
    
    return json.dumps({"status": 200})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
