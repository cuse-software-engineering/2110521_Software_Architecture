"""Four partitions, shared consumer groups, independent replay."""
import argparse
from common import Evidence, ensure_topic, event, publish_events, run_consumer


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('role', choices=['setup', 'publish', 'consume'])
    p.add_argument('--topic', default='lab.ex4.groups1')
    p.add_argument('--group', default='lab.ex4.group1')
    p.add_argument('--name', default='C1')
    p.add_argument('--count', type=int, default=40)
    p.add_argument('--seconds', type=int, default=120)
    p.add_argument('--log')
    a = p.parse_args()
    evidence = Evidence(a.log)
    try:
        if a.role == 'setup':
            ensure_topic(a.topic, 4)
            evidence.emit('topic_ready', topic=a.topic, partitions=4)
        elif a.role == 'publish':
            records = [(event(f'order-{i}', 1, {'text': 'group experiment'}), i % 4)
                       for i in range(a.count)]
            publish_events(a.topic, records, evidence)
        else:
            def process(record, out, fields):
                out.emit('completed', **fields)
            run_consumer(a.topic, a.group, a.name, evidence, process, a.seconds)
    finally:
        evidence.close()

if __name__ == '__main__':
    main()
