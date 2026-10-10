"""Three workers receive A/B/C, but B and C can finish before A."""
import argparse
import json
import time
import uuid
from common import connect, queue, publish, consume, log


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('role', choices=['publish', 'worker'])
    parser.add_argument('--run', default='class1')
    parser.add_argument('--name', default='worker')
    args = parser.parse_args()
    name = f'lab.failure.order.{args.run}'
    connection = connect()
    channel = connection.channel()
    queue(channel, name)
    if args.role == 'publish':
        try:
            for task, delay in [('A', 5), ('B', 1), ('C', 2)]:
                publish(channel, '', name, {'task': task, 'seconds': delay, 'sequence': 'ABC'.index(task)+1}, str(uuid.uuid4()))
        finally:
            connection.close()
        return
    channel.basic_qos(prefetch_count=1)
    def callback(ch, method, properties, body):
        task = json.loads(body)['payload']
        start = time.monotonic()
        log(f"{args.name} START {task['task']} delay={task['seconds']}s redelivered={method.redelivered}")
        # Pumps the connection while simulating work so heartbeat handling continues.
        connection.sleep(task['seconds'])
        log(f"{args.name} DONE {task['task']} elapsed={time.monotonic()-start:.2f}s")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    channel.basic_consume(queue=name, on_message_callback=callback, auto_ack=False)
    log(f'READY {args.name} queue={name}; Ctrl+C to stop')
    consume(connection, channel)

if __name__ == '__main__':
    main()
