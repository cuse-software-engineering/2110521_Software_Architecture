"""Combine Kafka JSONL evidence into a CSV ordered by host timestamps."""
import argparse
import csv
import json
from pathlib import Path


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('files', nargs='+')
    p.add_argument('--out', required=True)
    a = p.parse_args()
    rows = []
    for source in a.files:
        with open(source, encoding='utf-8') as stream:
            for line in stream:
                if line.strip():
                    row = json.loads(line)
                    row['source_file'] = source
                    for key, value in list(row.items()):
                        if isinstance(value, (dict, list)):
                            row[key] = json.dumps(value)
                    rows.append(row)
    fields = sorted({key for row in rows for key in row})
    rows.sort(key=lambda row: row.get('timestamp', ''))
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    with open(a.out, 'w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(f'Wrote {len(rows)} rows to {a.out}')

if __name__ == '__main__':
    main()
