#!/usr/bin/env python3
"""Minimal validation of per-repo features metadata.

This simple validator ensures the `features` key exists and each item has an `id` and `title` at minimum.
Exit codes:
 - 0: valid
 - 1: invalid or missing file
"""

import argparse
import os
import sys
import json
import re
try:
    import yaml
except Exception:
    yaml = None


def simple_parse_yaml_like(raw: str):
    # reuse a simple fallback used by generate script
    lines = raw.splitlines()
    data = {'features': []}
    current = None
    for line in lines:
        s = line.strip()
        if not s:
            continue
        if s.startswith('features:'):
            current = None
            continue
        if s.startswith('-'):
            item = {}
            data['features'].append(item)
            current = item
            m = re.match(r'^-\s+(\w+):\s*(.*)', s)
            if m and current is not None:
                current[m.group(1)] = m.group(2).strip(' \"\'')
        elif ':' in s and current is not None:
            k, v = s.split(':', 1)
            current[k.strip()] = v.strip().strip('"\'')
    return data


def load_yaml(path):
    with open(path, 'rb') as fh:
        data = fh.read()
    if yaml is not None:
        try:
            return yaml.safe_load(data)
        except Exception:
            pass
    try:
        # fallback attempt
        return simple_parse_yaml_like(data.decode('utf-8', errors='ignore'))
    except Exception:
        return None


def validate(path: str) -> int:
    if not os.path.exists(path):
        print(f'Missing features file at {path}', file=sys.stderr)
        return 1
    meta = load_yaml(path)
    if not meta or 'features' not in meta:
        print('Invalid or missing `features:` top-level key', file=sys.stderr)
        return 1
    for item in meta['features']:
        if 'id' not in item or 'title' not in item:
            print('Each feature must include an `id` and `title`:', item, file=sys.stderr)
            return 1
    print('features metadata OK')
    return 0


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('path', nargs='?', default='features/features.yml')
    args = parser.parse_args()
    rc = validate(args.path)
    sys.exit(rc)


if __name__ == '__main__':
    main()
