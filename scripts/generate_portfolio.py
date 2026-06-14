#!/usr/bin/env python3
"""
generate_portfolio.py
Builds and maintains the profile/portfolio landing page for bamr87.github.io.

It reads a curated registry (`_data/projects.yml`), fetches live metadata for each
repo from the GitHub API (description, stars, language, homepage, GitHub Pages URL,
topics, license, last push), merges the two, and renders:

  1. A full showcase page  -> pages/_about/portfolio/index.md
  2. A featured subset      -> the AUTO:portfolio span inside README.md (the homepage)

This is the sibling of `generate_features_index.py`: same urllib + optional-token
approach so it runs unchanged in CI, but it falls back to `gh auth token` locally.

Usage:
  python3 scripts/generate_portfolio.py                       # uses _data/projects.yml owner
  python3 scripts/generate_portfolio.py --owner bamr87 --token "$GH_TOKEN"
  python3 scripts/generate_portfolio.py --check               # exit 1 if output would change (CI drift gate)

Design notes:
- Deterministic output: repos render in registry order, so reruns produce clean diffs.
- Network-tolerant: a repo that fails to fetch is rendered from registry data alone
  (and noted on stderr) rather than aborting the whole run.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from typing import Dict, List, Optional

try:
    import yaml
except Exception:  # pragma: no cover - import guard mirrors generate_features_index.py
    yaml = None

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
REGISTRY_FILE = os.path.join(REPO_ROOT, '_data', 'projects.yml')
PORTFOLIO_PAGE = os.path.join(REPO_ROOT, 'pages', '_about', 'portfolio', 'index.md')
# Enriched, committed data the homepage dashboard reads via `site.data.portfolio`.
PORTFOLIO_DATA = os.path.join(REPO_ROOT, '_data', 'portfolio.yml')
README_FILE = os.path.join(REPO_ROOT, 'README.md')

# Markers delimiting the auto-generated featured block in README.md.
README_BEGIN = '<!-- AUTO:portfolio:start -->'
README_END = '<!-- AUTO:portfolio:end -->'

API = 'https://api.github.com'


# --------------------------------------------------------------------------- #
# Data loading
# --------------------------------------------------------------------------- #
def load_registry(path: str) -> dict:
    if yaml is None:
        sys.exit("PyYAML not installed. Run: pip install -r scripts/requirements.txt")
    if not os.path.exists(path):
        sys.exit(f"Registry not found: {path}. Create _data/projects.yml first.")
    with open(path, 'r', encoding='utf-8') as fh:
        data = yaml.safe_load(fh) or {}
    if not isinstance(data, dict) or 'projects' not in data:
        sys.exit("_data/projects.yml must define a top-level `projects:` list.")
    return data


def resolve_token(cli_token: Optional[str]) -> Optional[str]:
    """Prefer an explicit token, then common env vars, then the local `gh` CLI."""
    if cli_token:
        return cli_token
    for var in ('FEATURES_GITHUB_TOKEN', 'GITHUB_TOKEN', 'GH_TOKEN'):
        if os.environ.get(var):
            return os.environ[var]
    try:
        out = subprocess.run(['gh', 'auth', 'token'], capture_output=True, text=True, timeout=10)
        if out.returncode == 0 and out.stdout.strip():
            return out.stdout.strip()
    except Exception:
        pass
    return None


def _get_json(url: str, token: Optional[str], label: str) -> Optional[dict]:
    req = urllib.request.Request(url)
    req.add_header('Accept', 'application/vnd.github+json')
    if token:
        req.add_header('Authorization', f'Bearer {token}')
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        print(f"warn: {label} -> HTTP {e.code}", file=sys.stderr)
    except Exception as e:  # network off, timeout, etc.
        print(f"warn: {label} -> {e}", file=sys.stderr)
    return None


def fetch_repo(owner: str, repo: str, token: Optional[str]) -> Optional[dict]:
    return _get_json(f"{API}/repos/{owner}/{repo}", token, f"{owner}/{repo}")


def fetch_user(owner: str, token: Optional[str]) -> Optional[dict]:
    return _get_json(f"{API}/users/{owner}", token, f"user {owner}")


# --------------------------------------------------------------------------- #
# Field merging
# --------------------------------------------------------------------------- #
def pages_url(owner: str, repo: str, meta: dict) -> Optional[str]:
    """Resolve the best 'live site' URL: explicit homepage, else GitHub Pages."""
    home = (meta.get('homepage') or '').strip()
    if home:
        return home if home.startswith('http') else f"https://{home}"
    if meta.get('has_pages'):
        # The user/org site lives at the bare domain; project pages are nested.
        if repo.lower() == f"{owner.lower()}.github.io":
            return f"https://{repo}"
        return f"https://{owner}.github.io/{repo}/"
    return None


def resolve_site_url(owner: str, repo: str, entry: dict, meta: dict) -> Optional[str]:
    """Registry `live_url` overrides the auto-derived link.

    - key absent           -> auto-derive from GitHub homepage / Pages
    - live_url: false/none  -> suppress the Live link (e.g. a dead custom domain)
    - live_url: "https://…" -> use that URL verbatim (repoint)
    """
    if 'live_url' in entry:
        val = entry['live_url']
        if val in (False, None, '', 'none', 'false'):
            return None
        return str(val)
    return pages_url(owner, repo, meta)


def merge_project(owner: str, entry: dict, meta: Optional[dict]) -> dict:
    """Combine a registry entry (curated overrides) with live GitHub metadata."""
    repo = entry['repo']
    meta = meta or {}
    return {
        'repo': repo,
        'owner': owner,
        'featured': bool(entry.get('featured')),
        'category': entry.get('category', 'Projects'),
        # Registry `blurb` wins over the GitHub description so the showcase reads well.
        'description': entry.get('blurb') or meta.get('description') or '',
        'stars': meta.get('stargazers_count', 0),
        'language': meta.get('language') or '',
        'topics': meta.get('topics') or [],
        'issues': meta.get('open_issues_count', 0),
        'license': ((meta.get('license') or {}).get('spdx_id') or '').replace('NOASSERTION', ''),
        'pushed_at': meta.get('pushed_at', ''),
        'repo_url': meta.get('html_url') or f"https://github.com/{owner}/{repo}",
        'site_url': resolve_site_url(owner, repo, entry, meta),
    }


# --------------------------------------------------------------------------- #
# Rendering
# --------------------------------------------------------------------------- #
def badges(p: dict) -> str:
    o, r = p['owner'], p['repo']
    b = [
        f"[![Stars](https://img.shields.io/github/stars/{o}/{r}?style=flat-square)](https://github.com/{o}/{r}/stargazers)",
        f"[![Last commit](https://img.shields.io/github/last-commit/{o}/{r}?style=flat-square)](https://github.com/{o}/{r}/commits)",
        f"![Top language](https://img.shields.io/github/languages/top/{o}/{r}?style=flat-square)",
    ]
    return ' '.join(b)


def links(p: dict) -> str:
    parts = [f"[Repo]({p['repo_url']})"]
    if p['site_url']:
        parts.append(f"[Live]({p['site_url']})")
    return ' · '.join(parts)


def card(p: dict) -> List[str]:
    """A single project rendered as a heading + badges + blurb + links block."""
    title = p['repo']
    lines = [f"### [{title}]({p['repo_url']})", '', badges(p), '']
    if p['description']:
        lines.append(p['description'])
        lines.append('')
    if p['topics']:
        lines.append('`' + '` `'.join(p['topics'][:8]) + '`')
        lines.append('')
    lines.append(links(p))
    lines.append('')
    return lines


def render_portfolio_page(projects: List[dict], now: str) -> str:
    front = (
        "---\n"
        "layout: default\n"
        'title: "Portfolio"\n'
        'description: "A showcase of the GitHub projects, sites, and experiments I build and maintain."\n'
        "permalink: /about/portfolio/\n"
        "sidebar:\n"
        "  nav: about\n"
        f"lastmod: {now}\n"
        "---\n\n"
        "<!-- This page is generated by scripts/generate_portfolio.py. "
        "Edit _data/projects.yml and rerun the generator instead of editing here. -->\n\n"
        "# Portfolio\n\n"
        "A living showcase of the projects, themes, and experiments I build across GitHub. "
        "Curated in [`_data/projects.yml`](https://github.com/bamr87/bamr87.github.io/blob/main/_data/projects.yml) "
        "and refreshed automatically with live repository metadata.\n\n"
    )
    lines = [front]

    featured = [p for p in projects if p['featured']]
    if featured:
        lines.append("## ⭐ Featured\n")
        for p in featured:
            lines.extend(card(p))
        lines.append("---\n")

    # Group the remainder by category, preserving first-seen category order.
    rest = [p for p in projects if not p['featured']]
    seen: List[str] = []
    for p in rest:
        if p['category'] not in seen:
            seen.append(p['category'])
    for cat in seen:
        lines.append(f"## {cat}\n")
        for p in [x for x in rest if x['category'] == cat]:
            lines.extend(card(p))

    lines.append("---\n")
    lines.append(f"*Generated by `scripts/generate_portfolio.py` · last updated {now}*\n")
    return '\n'.join(lines).rstrip() + '\n'


def render_readme_block(projects: List[dict]) -> str:
    """A compact featured table for the README homepage."""
    featured = [p for p in projects if p['featured']]
    rows = ["| Project | Description | Links |", "|---|---|---|"]
    for p in featured:
        link_cell = links(p).replace(' · ', ' • ')
        desc = (p['description'] or '').replace('|', '\\|')
        rows.append(f"| **[{p['repo']}]({p['repo_url']})** | {desc} | {link_cell} |")
    body = '\n'.join(rows)
    # The blank line before the table is REQUIRED: kramdown only parses a GFM
    # table when it's preceded by a blank line. Without it the table sits
    # directly under the HTML comment, kramdown treats the whole thing as a
    # paragraph, and smart-typography mangles the `---` separator into em-dashes
    # — so the homepage shows raw `| Project | … |` pipes instead of a table.
    return (
        f"{README_BEGIN}\n"
        "<!-- Generated by scripts/generate_portfolio.py from _data/projects.yml. Do not edit by hand. -->\n"
        f"\n{body}\n\n"
        "_See the full [portfolio](/about/portfolio/) for every project._\n"
        f"{README_END}"
    )


def splice_readme(readme: str, block: str) -> str:
    """Replace the AUTO span if present; otherwise append it under a heading."""
    if README_BEGIN in readme and README_END in readme:
        pre = readme.split(README_BEGIN)[0]
        post = readme.split(README_END, 1)[1]
        return pre + block + post
    addition = f"\n\n## Portfolio\n\n{block}\n"
    return readme.rstrip() + addition + '\n'


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def build_portfolio_data(owner: str, projects: List[dict], user: Optional[dict], now: str) -> dict:
    """The enriched dataset the homepage dashboard renders from (`site.data.portfolio`)."""
    from collections import Counter
    langs = Counter(p['language'] for p in projects if p['language'])
    user = user or {}
    return {
        'owner': owner,
        'generated_at': now,
        'totals': {
            'public_repos': user.get('public_repos'),
            'followers': user.get('followers'),
            'shown': len(projects),
            'featured': sum(1 for p in projects if p['featured']),
            'stars': sum(p['stars'] for p in projects),
            'languages': dict(langs.most_common()),
        },
        'projects': [
            {
                'repo': p['repo'], 'featured': p['featured'], 'category': p['category'],
                'description': p['description'], 'stars': p['stars'], 'language': p['language'],
                'topics': p['topics'][:8], 'pushed_at': p['pushed_at'], 'license': p['license'],
                'repo_url': p['repo_url'], 'site_url': p['site_url'],
            }
            for p in projects
        ],
    }


def render_portfolio_data_yaml(data: dict) -> str:
    header = (
        "# GENERATED by scripts/generate_portfolio.py — do not edit by hand.\n"
        "# Enriched project data + totals the homepage dashboard reads via site.data.portfolio.\n"
        "# Curate projects in _data/projects.yml and rerun the generator.\n"
    )
    return header + yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=10000)


def build(owner: str, token: Optional[str], registry: dict) -> Dict[str, str]:
    exclude = set(registry.get('exclude', []) or [])
    entries = [e for e in registry['projects'] if e.get('repo') not in exclude]
    projects = []
    for entry in entries:
        meta = fetch_repo(owner, entry['repo'], token)
        projects.append(merge_project(owner, entry, meta))
    user = fetch_user(owner, token)
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')
    page = render_portfolio_page(projects, now)
    readme_block = render_readme_block(projects)
    data_yaml = render_portfolio_data_yaml(build_portfolio_data(owner, projects, user, now))
    return {'page': page, 'readme_block': readme_block, 'data_yaml': data_yaml}


def _strip_volatile(text: str) -> str:
    """Drop the regenerated timestamps so we compare substance, not run time.

    Without this, the `lastmod:` line and footer change on every run, so the
    generator would churn the file (and `--check` would always report drift)
    even when no repository metadata actually changed.
    """
    text = re.sub(r'(?m)^lastmod:.*$', 'lastmod:', text)
    text = re.sub(r'(?m)^\*Generated by .*$', '*generated*', text)
    text = re.sub(r'(?m)^generated_at:.*$', 'generated_at:', text)
    return text


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--owner', help='GitHub owner (defaults to registry `owner:` or bamr87)')
    parser.add_argument('--token', help='GitHub token (else env or `gh auth token`)')
    parser.add_argument('--check', action='store_true',
                        help='Exit non-zero if generated output differs from on-disk (CI drift gate)')
    args = parser.parse_args()

    registry = load_registry(REGISTRY_FILE)
    owner = args.owner or registry.get('owner') or 'bamr87'
    token = resolve_token(args.token)

    out = build(owner, token, registry)
    existing_page = _read(PORTFOLIO_PAGE)
    existing_readme = _read(README_FILE)
    existing_data = _read(PORTFOLIO_DATA)
    new_readme = splice_readme(existing_readme, out['readme_block'])

    # Compare substance (timestamps stripped) so a no-op rerun is a clean no-op.
    page_changed = _strip_volatile(existing_page) != _strip_volatile(out['page'])
    readme_changed = existing_readme != new_readme
    data_changed = _strip_volatile(existing_data) != _strip_volatile(out['data_yaml'])

    if args.check:
        changed = [n for n, c in (('portfolio page', page_changed),
                                  ('README block', readme_changed),
                                  ('portfolio data', data_changed)) if c]
        if changed:
            print(f"drift: {', '.join(changed)} stale; run scripts/generate_portfolio.py", file=sys.stderr)
            return 1
        print("ok: portfolio is up to date")
        return 0

    wrote = []
    if page_changed:
        os.makedirs(os.path.dirname(PORTFOLIO_PAGE), exist_ok=True)
        _write(PORTFOLIO_PAGE, out['page'])
        wrote.append(os.path.relpath(PORTFOLIO_PAGE, REPO_ROOT))
    if readme_changed:
        _write(README_FILE, new_readme)
        wrote.append('README.md portfolio block')
    if data_changed:
        _write(PORTFOLIO_DATA, out['data_yaml'])
        wrote.append(os.path.relpath(PORTFOLIO_DATA, REPO_ROOT))
    print(f"wrote {', '.join(wrote)}" if wrote else "no changes — portfolio already up to date")
    return 0


def _read(path: str) -> str:
    if not os.path.exists(path):
        return ''
    with open(path, 'r', encoding='utf-8') as fh:
        return fh.read()


def _write(path: str, content: str) -> None:
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(content)


if __name__ == '__main__':
    raise SystemExit(main())
