"""Crash AFTER a database commit but BEFORE ACK; compare unsafe and safe processing."""
import argparse
import os
import sqlite3
from pathlib import Path
import uuid
from common import connect, queue, publish, consume, log

DB = Path(__file__).with_name('demo1_effects.sqlite3')


def apply_effect(database, event_id, safe):
    """The business effect and deduplication marker share one DB transaction."""
    with sqlite3.connect(database) as db:
        db.execute('CREATE TABLE IF NOT EXISTS processed (event_id TEXT PRIMARY KEY)')
        db.execute('CREATE TABLE IF NOT EXISTS effects (id INTEGER PRIMARY KEY, event_id TEXT)')
        applied = True
        if safe:
            cursor = db.execute('INSERT OR IGNORE INTO processed VALUES (?)', (event_id,))
            applied = cursor.rowcount == 1
        if applied:
            db.execute('INSERT INTO effects(event_id) VALUES (?)', (event_id,))
        total = db.execute('SELECT count(*) FROM effects WHERE event_id=?', (event_id,)).fetchone()[0]
    return applied, total  # Context manager has committed BEFORE we return.


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('role', choices=['publish', 'worker'])
    parser.add_argument('--mode', choices=['unsafe', 'safe'], default='unsafe')
    parser.add_argument('--run', default='class1', help='Use a fresh label for each experiment')
    parser.add_argument('--crash-before-ack', action='store_true')
    args = parser.parse_args()
    name = f'lab.failure.crash.{args.mode}.{args.run}'
    connection = connect()
    channel = connection.channel()
    queue(channel, name)
    if args.role == 'publish':
        try:
            event_id = str(uuid.uuid4())
            publish(channel, '', name, {'action': 'create_order'}, event_id)
        finally:
            connection.close()
        return

    channel.basic_qos(prefetch_count=1)
    def callback(ch, method, properties, body):
        event_id = properties.message_id
        if not event_id:
            ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
            raise ValueError('This demo requires message_id')
        log(f'RECEIVED id={event_id} tag={method.delivery_tag} redelivered={method.redelivered}')
        applied, total = apply_effect(DB, event_id, args.mode == 'safe')
        log(f'DB COMMITTED: applied={applied}, business_effect_count={total}')
        if args.crash_before_ack:
            log('INTENTIONAL CRASH: database committed, ACK NOT SENT (exit code 99)')
            os._exit(99)  # Teaching fault injection: deliberately skip graceful cleanup.
        ch.basic_ack(delivery_tag=method.delivery_tag)
        log('ACK SENT')
        ch.stop_consuming()
    channel.basic_consume(queue=name, on_message_callback=callback, auto_ack=False)
    log(f'READY queue={name}; processes one delivery then exits')
    consume(connection, channel)

if __name__ == '__main__':
    main()
