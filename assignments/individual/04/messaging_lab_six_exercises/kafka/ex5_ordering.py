"""Keyed order events versus deliberate cross-partition routing."""
import argparse
import time
from common import Evidence, ensure_topic, event, publish_events, run_consumer


def records(mode):
    # Broken mode uses one order across three partitions; keyed mode uses several orders.
    orders = ['order-123'] if mode == 'broken' else ['order-123', 'order-456', 'order-789']
    for order in orders:
        for index, action in enumerate(['Created', 'Updated', 'Cancelled']):
            record = event(order, index+1, {'action': action})
            yield record, index if mode == 'broken' else None


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('role', choices=['setup', 'publish', 'consume'])
    p.add_argument('--topic', default='lab.ex5.keyed1')
    p.add_argument('--group', default='lab.ex5.group1')
    p.add_argument('--name', default='C1')
    p.add_argument('--mode', choices=['keyed', 'broken'], default='keyed')
    p.add_argument('--seconds', type=int, default=120)
    p.add_argument('--log')
    a = p.parse_args()
    out = Evidence(a.log)
    try:
        if a.role == 'setup':
            ensure_topic(a.topic, 3)
            out.emit('topic_ready', topic=a.topic, partitions=3)
        elif a.role == 'publish':
            publish_events(a.topic, records(a.mode), out)
        else:
            def process(record, evidence, fields):
                # A single consumer processes its received records sequentially.
                delay = {1: 5, 2: 1, 3: 2}[record['sequence']] if a.mode == 'broken' else 0.05
                evidence.emit('started', **fields)
                time.sleep(delay)
                evidence.emit('completed', **fields)
            run_consumer(a.topic, a.group, a.name, out, process, a.seconds)
    finally:
        out.close()

if __name__ == '__main__':
    main()
