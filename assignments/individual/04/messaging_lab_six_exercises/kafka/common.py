"""Kafka lab helpers: confirmed publishing, manual progress, structured evidence."""
import json
import os
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from confluent_kafka import Producer, Consumer, KafkaException
from confluent_kafka.admin import AdminClient, NewTopic

BOOTSTRAP = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:19092')


def event(order_id, sequence, payload):
    return dict(event_id=str(uuid.uuid4()), order_id=order_id,
                sequence=sequence, payload=payload)


class Evidence:
    def __init__(self, path=None):
        self.stream = None
        if path:
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            self.stream = open(path, 'a', encoding='utf-8')

    def emit(self, kind, **fields):
        item = dict(timestamp=datetime.now(timezone.utc).isoformat(), kind=kind, **fields)
        line = json.dumps(item)
        print(line, flush=True)
        if self.stream:
            self.stream.write(line + '\n')
            self.stream.flush()

    def close(self):
        if self.stream:
            self.stream.close()


def ensure_topic(topic, partitions):
    admin = AdminClient({'bootstrap.servers': BOOTSTRAP})
    metadata = admin.list_topics(timeout=15)
    if topic not in metadata.topics:
        futures = admin.create_topics([NewTopic(topic, num_partitions=partitions,
            replication_factor=1, config={'retention.ms': '86400000'})], request_timeout=15)
        for future in futures.values():
            future.result()
    else:
        existing = metadata.topics[topic]
        if existing.error:
            raise KafkaException(existing.error)
        if len(existing.partitions) != partitions:
            raise ValueError(f'{topic}: expected {partitions} partitions, found {len(existing.partitions)}. Use a fresh topic.')


def publish_events(topic, records, evidence):
    """records = iterable of (event, explicit_partition_or_None)."""
    producer = Producer({'bootstrap.servers': BOOTSTRAP,
        'enable.idempotence': True, 'acks': 'all', 'delivery.timeout.ms': 15000})
    failures = []
    def delivered(error, msg):
        if error:
            failures.append(str(error))
        else:
            evidence.emit('published', event_id=json.loads(msg.value())['event_id'],
                          topic=msg.topic(), partition=msg.partition(), offset=msg.offset())
    for record, partition in records:
        options = dict(topic=topic, key=str(record['order_id']).encode(),
            value=json.dumps(record).encode(), on_delivery=delivered)
        if partition is not None:
            options['partition'] = partition
        producer.produce(**options)
        producer.poll(0)
    remaining = producer.flush(20)
    if failures or remaining:
        raise RuntimeError(f'Publishing failed or uncertain: {failures}, pending={remaining}')


def make_consumer(topic, group, name, evidence):
    consumer = Consumer({'bootstrap.servers': BOOTSTRAP, 'group.id': group,
        'client.id': name, 'enable.auto.commit': False,
        'enable.auto.offset.store': False, 'auto.offset.reset': 'earliest',
        'partition.assignment.strategy': 'range', 'session.timeout.ms': 10000})
    def assigned(c, partitions):
        evidence.emit('assigned', consumer=name, group=group,
                      partitions=[p.partition for p in partitions])
    def revoked(c, partitions):
        evidence.emit('revoked', consumer=name, group=group,
                      partitions=[p.partition for p in partitions])
    consumer.subscribe([topic], on_assign=assigned, on_revoke=revoked)
    return consumer


def commit_completed(consumer, message):
    # commit(message=...) commits message.offset()+1, not the current offset.
    committed = consumer.commit(message=message, asynchronous=False)
    for partition in committed or []:
        if partition.error:
            raise KafkaException(partition.error)


def run_consumer(topic, group, name, evidence, handler, seconds=120, one=False):
    consumer = make_consumer(topic, group, name, evidence)
    deadline = time.monotonic() + seconds
    seen = set()
    try:
        while time.monotonic() < deadline:
            message = consumer.poll(1)
            if message is None:
                continue
            if message.error():
                raise KafkaException(message.error())
            record = json.loads(message.value())
            fields = dict(consumer=name, group=group, topic=topic,
                partition=message.partition(), offset=message.offset(),
                key=message.key().decode() if message.key() else None, **record)
            evidence.emit('received', **fields)
            handler(record, evidence, fields)  # Crash demo exits here before commit.
            commit_completed(consumer, message)
            seen.add(record['event_id'])
            evidence.emit('committed', consumer=name, group=group,
                partition=message.partition(), next_offset=message.offset()+1)
            if one:
                break
    except KeyboardInterrupt:
        evidence.emit('interrupted', consumer=name)
    finally:
        consumer.close()  # auto commit is disabled, including on close.
        evidence.emit('summary', consumer=name, unique_completed=len(seen))
