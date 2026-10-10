"""Compare an existing durable queue with a temporary queue bound after publication."""
import argparse
import uuid
from common import connect, queue, publish, consume, log


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('role', choices=['setup', 'publish', 'durable', 'temporary'])
    parser.add_argument('--run', default='class1')
    parser.add_argument('--message', default='Hello')
    args = parser.parse_args()
    exchange = f'lab.failure.fanout.{args.run}'
    durable_name = exchange + '.saved'
    connection = connect()
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange, exchange_type='fanout', durable=True)
    if args.role == 'setup':
        queue(channel, durable_name)
        channel.queue_bind(exchange=exchange, queue=durable_name)
        log(f'SETUP: durable queue {durable_name} exists and is bound; no consumer yet')
        connection.close()
        return
    if args.role == 'publish':
        try:
            # Does NOT create a queue or binding: run setup first.
            publish(channel, exchange, '', {'text': args.message}, str(uuid.uuid4()))
        finally:
            connection.close()
        return
    if args.role == 'durable':
        # Passive declaration checks that setup created it; does not create it late.
        channel.queue_declare(queue=durable_name, passive=True)
        name = durable_name
    else:
        result = channel.queue_declare(queue='', exclusive=True, auto_delete=True)
        name = result.method.queue
        channel.queue_bind(exchange=exchange, queue=name)
    channel.basic_qos(prefetch_count=1)
    def callback(ch, method, properties, body):
        log(f'{args.role.upper()} RECEIVED id={properties.message_id} body={body.decode()}')
        ch.basic_ack(delivery_tag=method.delivery_tag)
    channel.basic_consume(queue=name, on_message_callback=callback, auto_ack=False)
    log(f'READY {args.role} queue={name}; Ctrl+C to stop')
    consume(connection, channel)

if __name__ == '__main__':
    main()
