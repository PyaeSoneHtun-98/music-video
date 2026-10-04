"""Apply or undo the audited video names without overwriting or deleting any clip."""
import argparse
import csv
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def digest(path):
    with path.open('rb') as source:
        return hashlib.file_digest(source, 'sha256').hexdigest()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true', help='Rename; otherwise only check and preview.')
    parser.add_argument('--undo', action='store_true', help='Restore original download names.')
    args = parser.parse_args()
    with (ROOT / 'production/video-audit.csv').open(encoding='utf-8', newline='') as manifest:
        rows = list(csv.DictReader(manifest))
    pending = []
    for row in rows:
        old, new = row['original_name'], row['renamed_name']
        if args.undo:
            old, new = new, old
        if Path(old).name != old or Path(new).name != new:
            raise ValueError('Manifest names must be plain filenames.')
        source, target = ROOT / 'videos' / old, ROOT / 'videos' / new
        if source.exists():
            if target.exists():
                raise FileExistsError(target)
            if digest(source) != row['sha256']:
                raise ValueError(f'Content changed: {source}')
            pending.append((source, target, row['sha256']))
        elif not target.exists() or digest(target) != row['sha256']:
            raise FileNotFoundError(f'Expected content absent: {source}')
    # All source contents and destinations are checked before the first mutation.
    for source, target, expected in pending:
        print(f'{source.name} -> {target.name}')
        if args.apply:
            source.rename(target)
            if digest(target) != expected:
                raise ValueError(f'Post-rename verification failed: {target}')
    print(f'{len(pending)} renames {"applied and verified" if args.apply else "planned"}.')

if __name__ == '__main__':
    main()
