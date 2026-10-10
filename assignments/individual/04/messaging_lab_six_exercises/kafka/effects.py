"""Atomic database effect and event-ID deduplication for exercise 6."""
import sqlite3


def apply_effect(database, event_id, safe):
    with sqlite3.connect(database) as db:
        db.execute('CREATE TABLE IF NOT EXISTS processed(event_id TEXT PRIMARY KEY)')
        db.execute('CREATE TABLE IF NOT EXISTS effects(id INTEGER PRIMARY KEY,event_id TEXT)')
        applied = True
        if safe:
            applied = db.execute('INSERT OR IGNORE INTO processed VALUES (?)',
                                 (event_id,)).rowcount == 1
        if applied:
            db.execute('INSERT INTO effects(event_id) VALUES (?)', (event_id,))
        count = db.execute('SELECT count(*) FROM effects WHERE event_id=?',
                           (event_id,)).fetchone()[0]
    return applied, count
