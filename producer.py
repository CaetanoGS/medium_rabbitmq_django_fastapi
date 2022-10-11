import json

import pika

credentials = pika.PlainCredentials('admin', 'test')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        'localhost',
        heartbeat=600,
        blocked_connection_timeout=300,
        credential=credentials
    )
)

channel = connection.channel()

def publish(method: str, body: str = None):
    properties = pika.BasicProperties(method)
    channel.basic_publish(
        exchange='notification.exchange',
        routing_key='',
        body=json.dumps(body),
        properties=properties
    )