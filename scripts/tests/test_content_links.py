"""Static content checks for links fixed in issue #31 (no network).

Run from the repo root: python -m pytest -q scripts/tests
"""

import re
from pathlib import Path

PAGES = Path(__file__).resolve().parents[2] / "pages"

# Hosts or pages verified dead (404 / DNS failure / retired); only Wayback copies may link them.
DEAD = [
    "theochem.ru.nl/~pwormer",
    "collectiveray.com/defer-parsing",
    "amazonwebservices.benchprep.com",
    "wiki.bash-hackers.org",
    "jekyll-sitel",
]


def _pages():
    return [(p, p.read_text(encoding="utf-8")) for p in sorted(PAGES.rglob("*.md"))]


def _strip_archived(text):
    return re.sub(r"https://web\.archive\.org/web/\d+/\S+", "", text)


def test_no_live_links_to_dead_pages():
    hits = [
        f"{p.relative_to(PAGES)}: {dead}"
        for p, text in _pages()
        for dead in DEAD
        if dead in _strip_archived(text)
    ]
    assert hits == []


def test_no_hyperlinks_to_retired_netlify_site():
    # The personal mirror ({{ site.github_user }} / bamr87 .netlify.*) is gone; netlify.com itself is fine.
    pattern = re.compile(r"https?://(\{\{ ?site\.github_user ?\}\}|bamr87)\.netlify\.(com|app)")
    hits = [str(p.relative_to(PAGES)) for p, text in _pages() if pattern.search(text)]
    assert hits == []


def test_no_images_over_plain_http():
    pattern = re.compile(r"!\[[^\]]*\]\(\s*http://|<img[^>]+src=[\"']http://")
    hits = [str(p.relative_to(PAGES)) for p, text in _pages() if pattern.search(text)]
    assert hits == []


def test_markdown_cheatsheet_highlight_example_is_raw_code_once():
    text = (PAGES / "_notes/cheetsheets/markdown.md").read_text(encoding="utf-8")
    assert '{{ "{% highlight' not in text
    assert text.count("Syntax highlighting can be used") == 1
    raw = re.search(r"\{% raw %\}\s*```[a-z]*\n(.*?)```\s*\{% endraw %\}", text, re.S)
    assert raw and "{% highlight javascript %}" in raw.group(1)
    # The rendered demo must be a fence: unwrap-prose joins lines between bare {% highlight %} tags.
    demo = re.search(r"creates\.\.\.\s*```javascript\n(.*?)```", text, re.S)
    assert demo and demo.group(1).splitlines() == [
        "/* Some pointless Javascript */",
        'var rawr = ["r", "a", "w", "r"];',
    ]
