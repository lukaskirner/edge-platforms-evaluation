import sys
import time
import json
import logging
import awsiot.greengrasscoreipc
import awsiot.greengrasscoreipc.client as client
from awsiot.greengrasscoreipc.model import (
    SubscribeToTopicRequest,
    SubscriptionResponseMessage
)

# Setup logging to stdout
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

TIMEOUT = 10
ipc_client = awsiot.greengrasscoreipc.connect()
topic = "ping/topic"


class StreamHandler(client.SubscribeToTopicStreamHandler):
    def __init__(self):
        super().__init__()

    def on_stream_event(self, event: SubscriptionResponseMessage) -> None:
        message_string = event.json_message.message
        now = time.time_ns()
        before = message_string["timestamp"]
        logger.info(f'Received message at [{now} - {before}] = {now - before}')

    def on_stream_error(self, error: Exception) -> bool:
        return True

    def on_stream_closed(self) -> None:
        pass


request = SubscribeToTopicRequest()
request.topic = topic
handler = StreamHandler()
operation = ipc_client.new_subscribe_to_topic(handler)
future = operation.activate(request)

while True:
    time.sleep(1)
