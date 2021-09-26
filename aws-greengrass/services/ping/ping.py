import sys
import time
import json
import logging
import awsiot.greengrasscoreipc
from awsiot.greengrasscoreipc.model import (
    PublishToTopicRequest,
    PublishMessage,
    JsonMessage
)

# Setup logging to stdout
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

TIMEOUT = 10
publish_rate = 1.0
ipc_client = awsiot.greengrasscoreipc.connect()
topic = "ping/topic"

while True:
    message = {"timestamp": time.time_ns()}
    message_json = json.dumps(message).encode('utf-8')
    request = PublishToTopicRequest()
    request.topic = topic
    publish_message = PublishMessage()
    publish_message.json_message = JsonMessage()
    publish_message.json_message.message = message
    request.publish_message = publish_message
    operation = ipc_client.new_publish_to_topic()
    operation.activate(request)
    future = operation.get_response()
    future.result(TIMEOUT)

    logger.info(f'Message sent to {topic}: {message}')
    time.sleep(1/publish_rate)
