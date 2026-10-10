"""Shared connection and publishing helpers for the three classroom demos."""
import json
import os
from datetime import datetime, timezone
import pika


def log(message):
    print(f"{datetime.now(timezone.utc).isoformat(timespec='milliseconds')} {message}", flush=True)


def connect():
    # Set RABBITMQ_URL for a different broker. Do not commit real credentials.
    params = pika.URLParameters(os.getenv('RABBITMQ_URL', 'amqp://guest:guest@localhost:5673/%2F'))
    params.heartbeat = 60
    params.blocked_connection_timeout = 30
    params.socket_timeout = 10
    return pika.BlockingConnection(params)


def queue(channel, name):
    channel.queue_declare(queue=name, durable=True,
                          arguments={'x-queue-type': 'classic'})


def publish(channel, exchange, routing_key, payload, message_id):
    # Blocking publish waits for confirmation once confirm_delivery is enabled.
    channel.confirm_delivery()
    channel.basic_publish(exchange=exchange, routing_key=routing_key,
        body=json.dumps(dict(event_id=message_id, order_id=payload.get('order_id', 'order-demo'), sequence=payload.get('sequence', 1), payload=payload)).encode(), mandatory=True,
        properties=pika.BasicProperties(content_type='application/json',
            delivery_mode=2, message_id=message_id))
    log(f'CONFIRMED id={message_id} payload={payload}')


def consume(connection, channel):
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        log('Stopping consumer')
    finally:
        if connection.is_open:
            connection.close()
