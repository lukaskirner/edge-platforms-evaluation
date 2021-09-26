import sys
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

# IPC
ipc_client = awsiot.greengrasscoreipc.connect()

# Constants
PUBLISH_TOPIC = "actor/ventilation"
TIMEOUT = 10

def lambda_handler(event, context):
    logger.info("Received message!")
    if 'temperature' in event and event['temperature'] > 30.0:
        try:
            message = { "isOn": True }
            message_json = json.dumps(message).encode('utf-8')
            request = PublishToTopicRequest()
            request.topic = PUBLISH_TOPIC
            publish_message = PublishMessage()
            publish_message.json_message = JsonMessage()
            publish_message.json_message.message = message
            request.publish_message = publish_message
            operation = ipc_client.new_publish_to_topic()
            operation.activate(request)
            future = operation.get_response()
            future.result(TIMEOUT)
            logger.info(f'Triggering publish to topic "{PUBLISH_TOPIC}" with ON state')
        except Exception as e:
            logger.error(f'Failed to trigger publish to topic "{PUBLISH_TOPIC}" with ON state: {repr(e)}')
