#!/usr/bin/env python3
"""
generate_features_index.py
Collects feature metadata from sibling repos or via the GitHub API and generates a consolidated
`pages/_about/features/index.md` for the site. Supports a local scan mode and a remote GitHub mode.

Usage:
  python scripts/generate_features_index.py --mode=local --root=/path/to/workspace
  python scripts/generate_features_index.py --mode=remote --owner=bamr87 --token=$GITHUB_TOKEN

This script expects a per-repo feature metadata file at one of these locations:
- features/features.yml
- FEATURES.yml
- FEATURES.md (with YAML frontmatter)
- pages/_about/features/ (md files with frontmatter)

Feature metadata YAML format (features/features.yml):
---
features:
  - id: FR-0001
    title: "Auto-generated feature list"
    description: "Short description"
    implemented: true
    link: "/path/to/detail"
    tags: [site, automation]
    date: 2025-11-01
---

The script is intentionally conservative about parsing — it will ignore unknown formats but will
attempt to present what it can find in a readable index. The page is regenerated and committed
by a periodic GitHub Actions workflow.
"""

import argparse
import os
import re
import sys
import json
from datetime import datetime

try:
    import yaml
except Exception:
    yaml = None

import base64
import urllib.request
from typing import List, Dict, Optional


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUTPUT_FILE = os.path.join(REPO_ROOT, 'pages', '_about', 'features', 'index.md')


def read_yaml_bytes(raw_bytes: bytes) -> Optional[dict]:
    if yaml is None:
        print("PyYAML not installed. Install it to parse YAML files: pip install pyyaml", file=sys.stderr)
        return None
    try:
        return yaml.safe_load(raw_bytes)
    except Exception:
        return None


def simple_parse_yaml_like(raw: str) -> Optional[dict]:
    # Simple fallback parser for files like features: - id: ...
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
            # new item
            # create blank
            item = {}
            data['features'].append(item)
            current = item
            # check for inline ' - id: value' style
            m = re.match(r'^-\s+(\w+):\s*(.*)', s)
            if m and current is not None:
                key = m.group(1)
                val = m.group(2).strip(' "\'')
                current[key] = val
        elif ':' in s and current is not None:
            k, v = s.split(':', 1)
            current[k.strip()] = v.strip().strip('"\'')
    return data


def parse_frontmatter_from_md_bytes(b: bytes) -> Optional[dict]:
    s = b.decode('utf-8', errors='ignore')
    m = re.match(r'^---\s*\n(.*?)\n---\s*\n', s, re.S)
    if m:
        block = m.group(1)
        return read_yaml_bytes(block.encode('utf-8'))
    return None


def collect_from_local(root: str) -> List[dict]:
    repos = []
    features = []
    # Look for directories in root (non-hidden)
    for name in sorted(os.listdir(root)):
        path = os.path.join(root, name)
        if not os.path.isdir(path):
            continue
        if name.startswith('.'):
            continue
        # search for possible feature files
        candidates = [
            os.path.join(path, 'features', 'features.yml'),
            os.path.join(path, 'features', 'features.yaml'),
            os.path.join(path, 'FEATURES.yml'),
            os.path.join(path, 'FEATURES.yaml'),
            os.path.join(path, 'FEATURES.md'),
            os.path.join(path, 'features.md'),
        ]
        # pages/_about/features folder
        feat_dir = os.path.join(path, 'pages', '_about', 'features')
        if os.path.isdir(feat_dir):
            for f in os.listdir(feat_dir):
                fp = os.path.join(feat_dir, f)
                if os.path.splitext(f)[1] in ('.md', '.markdown'):
                    try:
                        with open(fp, 'rb') as fh:
                            md_meta = parse_frontmatter_from_md_bytes(fh.read())
                        if md_meta and 'features' in md_meta:
                            for item in md_meta['features']:
                                item['repo'] = name
                                features.append(item)
                    except Exception:
                        pass
        for candidate in candidates:
            if os.path.exists(candidate):
                try:
                    with open(candidate, 'rb') as fh:
                        data = fh.read()
                    if candidate.endswith(('.md',)):
                        meta = parse_frontmatter_from_md_bytes(data)
                        if meta and 'features' in meta:
                            for item in meta['features']:
                                item['repo'] = name
                                features.append(item)
                    else:
                        meta = read_yaml_bytes(data)
                        if meta is None:
                            try:
                                meta = simple_parse_yaml_like(data.decode('utf-8', errors='ignore'))
                            except Exception:
                                meta = None
                        if meta and 'features' in meta:
                            for item in meta['features']:
                                item['repo'] = name
                                features.append(item)
                except Exception:
                    pass
    return features


def fetch_github_file(owner: str, repo: str, path: str, token: Optional[str] = None) -> Optional[bytes]:
    # Use the GitHub contents API to fetch a file
    url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'
    headers = { 'Accept': 'application/vnd.github.v3.raw' }
    if token:
        headers['Authorization'] = f'token {token}'
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.read()
    except Exception as e:
        # print('Failed to fetch', repo, path, e)
        return None


def collect_from_github(owner: str, token: Optional[str] = None, repos: Optional[List[str]] = None) -> List[dict]:
    features = []
    if repos is None:
        # collect list of public repos from owner
        url = f'https://api.github.com/users/{owner}/repos?per_page=100'
        headers = {}
        if token:
            headers['Authorization'] = f'token {token}'
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req) as resp:
                repos_data = json.load(resp)
                repos = [r['name'] for r in repos_data]
        except Exception as e:
            print('Error listing repos for owner', owner, e, file=sys.stderr)
            return features

    # For each repo, attempt to fetch features file
    candidate_paths = [
        'features/features.yml',
        'features/features.yaml',
        'FEATURES.yml',
        'FEATURES.yaml',
        'FEATURES.md',
        'features.md',
        'pages/_about/features/index.md'
    ]

    for repo in repos:
        for path in candidate_paths:
            data = fetch_github_file(owner, repo, path, token)
            if not data:
                continue
            # If Markdown, attempt to parse frontmatter
            if path.endswith('.md'):
                meta = parse_frontmatter_from_md_bytes(data)
                if meta and 'features' in meta:
                    for item in meta['features']:
                        item['repo'] = repo
                        features.append(item)
                    break
                # Else maybe a plain list? skip
            else:
                meta = read_yaml_bytes(data)
                if meta and 'features' in meta:
                    for item in meta['features']:
                        item['repo'] = repo
                        features.append(item)
                    break
    return features


def build_markdown(features: List[dict], header_template: Optional[str] = None) -> str:
    header = header_template or ''
    now = datetime.utcnow().replace(microsecond=0).isoformat() + 'Z'
    title = "Features Index (Consolidated)"
    front = f"---\nlayout: default\ntitle: \"{title}\"\nlastmod: {now}\n---\n\n"
    content_lines = [front]
    if header:
        content_lines.append(header)

    # Group features by implemented status
    implemented = [f for f in features if str(f.get('implemented', '')).lower() in ('1','true','yes')]
    pending = [f for f in features if str(f.get('implemented', '')).lower() not in ('1','true','yes')]

    content_lines.append('## Current Features')
    content_lines.append('\n')
    if implemented:
        content_lines.append('| Title | Repo | Tags | Link |')
        content_lines.append('| --- | --- | --- | --- |')
        for f in implemented:
            title = f.get('title', f.get('id', 'untitled'))
            repo = f.get('repo', '')
            tags_val = f.get('tags', []) or []
            if isinstance(tags_val, str):
                # convert simple string list formats like "[a, b]" into real list
                tags_val = [t.strip() for t in tags_val.strip('[]').split(',') if t.strip()]
            tags = ', '.join(tags_val)
            link = f.get('link', '')
            if link and not (link.startswith('http') or link.startswith('/')):
                link = f"/{repo}/{link.lstrip('/') }"
            content_lines.append(f"| {title} | {repo} | {tags} | {link} |")
    else:
        content_lines.append('*No implemented features found.*')

    content_lines.append('\n\n## Requested / Backlog Features')
    content_lines.append('\n')
    if pending:
        content_lines.append('| Title | Repo | Tags | Link |')
        content_lines.append('| --- | --- | --- | --- |')
        for f in pending:
            title = f.get('title', f.get('id', 'untitled'))
            repo = f.get('repo', '')
            tags_val = f.get('tags', []) or []
            if isinstance(tags_val, str):
                tags_val = [t.strip() for t in tags_val.strip('[]').split(',') if t.strip()]
            tags = ', '.join(tags_val)
            link = f.get('link', '')
            if link and not (link.startswith('http') or link.startswith('/')):
                link = f"/{repo}/{link.lstrip('/') }"
            content_lines.append(f"| {title} | {repo} | {tags} | {link} |")
    else:
        content_lines.append('*No backlog items found.*')

    content_lines.append('\n\n---\n')
    content_lines.append('*This index is generated automatically by `/scripts/generate_features_index.py`.')
    content_lines.append('\n')
    content_lines.append(f'Last updated: {now}')
    return '\n'.join(content_lines)


def save_file(content: str, path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(content)
    print('Wrote consolidated features index to', path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['local', 'remote'], default='local')
    parser.add_argument('--root', default=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
    parser.add_argument('--owner', default='bamr87')
    parser.add_argument('--repos', default=None, help='Comma-separated list of repos in remote mode')
    parser.add_argument('--token', default=os.environ.get('FEATURES_GITHUB_TOKEN') or os.environ.get('GITHUB_TOKEN'))
    parser.add_argument('--output', default=OUTPUT_FILE)
    args = parser.parse_args()

    features = []
    if args.mode == 'local':
        features = collect_from_local(args.root)
    else:
        repos = args.repos.split(',') if args.repos else None
        features = collect_from_github(args.owner, token=args.token, repos=repos)

    # Normalize simple entries if they are strings
    normalized = []
    for f in features:
        if isinstance(f, str):
            normalized.append({'title': f, 'description': '', 'implemented': False})
        else:
            normalized.append(f)

    # Attempt to read a template for page header
    template_path = os.path.join(REPO_ROOT, 'pages', '_about', 'features', '_template.md')
    header_template = None
    if os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as tfh:
            header_template = tfh.read()

    content = build_markdown(normalized, header_template=header_template)
    save_file(content, args.output)


if __name__ == '__main__':
    main()
