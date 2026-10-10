"""Crash after committing a business effect but before committing Kafka progress."""
import argparse
import os
from pathlib import Path
from common import Evidence, ensure_topic, event, publish_events, run_consumer
from effects import apply_effect


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('role', choices=['setup', 'publish', 'consume'])
    p.add_argument('--topic', default='lab.ex6.unsafe1')
    p.add_argument('--group', default='lab.ex6.unsafe1')
    p.add_argument('--mode', choices=['unsafe', 'safe'], default='unsafe')
    p.add_argument('--crash-before-commit', action='store_true')
    p.add_argument('--db', default=str(Path(__file__).with_name('ex6_effects.sqlite3')))
    p.add_argument('--seconds', type=int, default=90)
    p.add_argument('--log')
    a = p.parse_args()
    out = Evidence(a.log)
    try:
        if a.role == 'setup':
            ensure_topic(a.topic, 1)
            out.emit('topic_ready', topic=a.topic, partitions=1)
        elif a.role == 'publish':
            publish_events(a.topic, [(event('order-123', 1, {'action': 'create_order'}), 0)], out)
        else:
            def process(record, evidence, fields):
                applied, count = apply_effect(a.db, record['event_id'], a.mode == 'safe')
                evidence.emit('db_committed', applied=applied, business_effect_count=count, **fields)
                if a.crash_before_commit:
                    evidence.emit('intentional_crash', reason='DB committed, Kafka offset NOT committed')
                    os._exit(99)
                evidence.emit('completed', **fields)
            run_consumer(a.topic, a.group, 'ex6-worker', out, process, a.seconds, one=True)
    finally:
        out.close()

if __name__ == '__main__':
    main()
