"""Offline checks only. Does not start or connect to brokers."""
import ast
import importlib.util
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent


def load_function(path, name, namespace):
    tree = ast.parse(path.read_text())
    node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name)
    exec(compile(ast.Module(body=[node], type_ignores=[]), str(path), 'exec'), namespace)
    return namespace[name]


def test_effect(path):
    apply = load_function(path, 'apply_effect', {'sqlite3': sqlite3})
    with tempfile.TemporaryDirectory() as tmp:
        db = str(Path(tmp)/'effects.db')
        assert apply(db, 'unsafe', False) == (True, 1)
        assert apply(db, 'unsafe', False) == (True, 2)
        assert apply(db, 'safe', True) == (True, 1)
        assert apply(db, 'safe', True) == (False, 1)
        with sqlite3.connect(db) as connection:
            connection.execute("CREATE TRIGGER fail_effect BEFORE INSERT ON effects WHEN NEW.event_id='fail' BEGIN SELECT RAISE(ABORT, 'injected'); END")
        try:
            apply(db, 'fail', True)
        except sqlite3.IntegrityError:
            pass
        else:
            raise AssertionError('Expected injected failure')
        with sqlite3.connect(db) as connection:
            assert connection.execute("SELECT count(*) FROM processed WHERE event_id='fail'").fetchone()[0] == 0
    print('PASS effect/deduplication/rollback:', path.name)


def main():
    for path in ROOT.rglob('*.py'):
        if '.venv' not in path.parts:
            ast.parse(path.read_text(), filename=str(path))
    print('PASS Python syntax')
    for filename in ['rabbitmq/demo1_crash_ack.py', 'kafka/effects.py']:
        test_effect(ROOT/filename)
    scripts = ['rabbitmq/demo1_crash_ack.py', 'rabbitmq/demo2_late_subscriber.py',
        'rabbitmq/demo3_completion_order.py', 'kafka/ex4_groups.py',
        'kafka/ex5_ordering.py', 'kafka/ex6_crash_commit.py', 'evidence_to_csv.py']
    for script in scripts:
        subprocess.run([sys.executable, str(ROOT/script), '--help'], check=True, stdout=subprocess.DEVNULL)
    print('PASS seven command-line entry points')
    # Check that the commit helper passes the message for offset+1 semantics and surfaces errors.
    class FakeKafkaError(Exception):
        pass
    commit = load_function(ROOT/'kafka/common.py', 'commit_completed', {'KafkaException': FakeKafkaError})
    class Partition:
        error = None
    class Consumer:
        def commit(self, **kwargs):
            assert kwargs == {'message': 'message-object', 'asynchronous': False}
            return [Partition()]
    commit(Consumer(), 'message-object')
    Partition.error = 'injected commit error'
    try:
        commit(Consumer(), 'message-object')
    except FakeKafkaError:
        pass
    else:
        raise AssertionError('Commit error must propagate')
    print('PASS commit helper error handling')
    # Ordering producer plan, without calling Kafka.
    sys.path.insert(0, str(ROOT/'kafka'))
    spec = importlib.util.spec_from_file_location('ordering_check', ROOT/'kafka/ex5_ordering.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    keyed = list(module.records('keyed'))
    broken = list(module.records('broken'))
    assert len(keyed) == 9 and all(partition is None for _, partition in keyed)
    assert [partition for _, partition in broken] == [0, 1, 2]
    assert len({record['order_id'] for record, _ in broken}) == 1
    assert [record['sequence'] for record, _ in broken] == [1, 2, 3]
    assert len({record['event_id'] for record, _ in keyed}) == 9
    print('PASS keyed and deliberately broken event plans')
    print('Offline checks passed. Live broker integration is NOT tested here.')

if __name__ == '__main__':
    main()
