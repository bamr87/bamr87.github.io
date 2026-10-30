"""Site identity, author and date metadata checks for issue #26 (no network, no Jekyll).

Run from the repo root: python -m pytest -q scripts/tests
"""

import re
from datetime import datetime, timezone
from pathlib import Path

import yaml

from scripts.generate_features_index import build_markdown
from scripts.generate_portfolio import render_portfolio_page

ROOT = Path(__file__).resolve().parents[2]
PAGES = ROOT / "pages"
CONFIG = (ROOT / "_config.yml").read_text(encoding="utf-8")
FM = re.compile(r"\A---\s*\n(.*?\n)---\s*(?:\n|\Z)", re.S)
# Posts that once carried a copied template date; their old URLs must keep resolving.
REDATED_POSTS = [
    "2024-03-06-auto-hide-nav-bar.md",
    "2024-04-02-dockering-your-it-journey.md",
    "2024-04-13-sec's-edgar-database.md",
    "2024-10-07-django-on-aws-lambda.md",
    "2024-10-14-aws-database-setup-for-django-lambda-functions.md",
    "2024-10-14-deploy-django-on-aws-lambda-with-sam-a-stepby-step-guide.md",
]


def _config_value(key):
    # _config.yml uses YAML aliases PyYAML rejects (*site_domain), so read keys by line.
    m = re.search(rf'(?m)^{key}\s*:\s*(?:&\w+\s+)?"?([^"#\n]*?)"?\s*(?:#.*)?$', CONFIG)
    return m and m.group(1)


def _front_matter():
    for p in sorted(PAGES.rglob("*")):
        if p.suffix in (".md", ".html", ".markdown") and p.is_file():
            m = FM.match(p.read_text(encoding="utf-8"))
            if m:
                yield p, m.group(1)


def _day(value):
    value = str(value).strip().strip("'\"")
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc).date()


def test_site_identity_is_not_placeholder():
    assert _config_value("title") == "Amr Abdel-Motaleb"
    assert _config_value("name") == "Amr Abdel-Motaleb"
    assert not re.search(r'subtitle(_url)?\s*:\s*"(Dev|localhost)"', CONFIG)


def test_logo_is_a_square_headshot_not_the_triangle():
    logo = _config_value("logo").strip()
    assert logo != "/assets/images/gravatar-small.png"
    png = (ROOT / logo.lstrip("/")).read_bytes()
    # The theme forces the navbar logo into a 30x30 <img>: it must be square and big enough for 2x screens.
    assert png[:8] == b"\x89PNG\r\n\x1a\n"
    width, height = int.from_bytes(png[16:20], "big"), int.from_bytes(png[20:24], "big")
    assert width == height >= 60


def test_home_title_fits_in_60_chars():
    title = yaml.safe_load(FM.match((ROOT / "index.html").read_text(encoding="utf-8")).group(1))["title"]
    # jekyll-seo-tag renders "<page title> | <site title>"
    assert len(f"{title} | {_config_value('title')}") <= 60


def test_every_author_is_the_bamr87_key():
    values = {re.search(r"(?m)^author\s*:(.*)$", fm).group(1).strip()
              for _, fm in _front_matter() if re.search(r"(?m)^author\s*:", fm)}
    assert values == {"bamr87"}
    assert yaml.safe_load((ROOT / "_data/authors.yml").read_text(encoding="utf-8"))["bamr87"]["name"] == "Amr Abdel-Motaleb"
    assert re.search(r"(?m)^\s+author: bamr87\b", CONFIG), "missing site-wide author default"


def test_redated_posts_use_filename_date_and_redirect_old_url():
    assert "jekyll-redirect-from" in CONFIG
    for name in REDATED_POSTS:
        fm = yaml.safe_load(FM.match((PAGES / "_posts" / name).read_text(encoding="utf-8")).group(1))
        assert "date" not in fm, name
        assert any(u.startswith("/posts/2019/08/22/") for u in fm["redirect_from"]), name


def test_collection_docs_are_never_published_after_their_update():
    missing, inverted = [], []
    for p, fm_text in _front_matter():
        rel = p.relative_to(PAGES)
        coll = rel.parts[0]
        if not coll.startswith("_") or coll == "_posts" or p.name.startswith("_"):
            continue
        fm = yaml.safe_load(fm_text) or {}
        if "date" not in fm:
            missing.append(str(rel))
        elif fm.get("lastmod") and _day(fm["date"]) > _day(fm["lastmod"]):
            inverted.append(str(rel))
    assert missing == [] and inverted == []


def test_generated_pages_carry_a_fixed_date():
    for text in (build_markdown([]), render_portfolio_page([], "2030-01-01T00:00:00Z")):
        fm = yaml.safe_load(FM.match(text).group(1))
        assert _day(fm["date"]) <= _day(fm["lastmod"])


def test_favicon_ico_exists():
    assert (ROOT / "favicon.ico").read_bytes()[:4] == b"\x00\x00\x01\x00"


def test_feed_id_posts_are_renamed():
    # jekyll-feed derives <id> from the file name, so it must already look like the permalink slug.
    posts = PAGES / "_posts"
    assert (posts / "2024-05-22-threat-of-women.md").exists()
    assert not (posts / "2024-05-22-Threat-of-women.md").exists()
    renamed = posts / "2024-06-18-aquaaids-devastating-desert-mission.md"
    assert "/posts/2024/06/18/aquaaid-s-devastating-desert-mission/" in yaml.safe_load(
        FM.match(renamed.read_text(encoding="utf-8")).group(1))["redirect_from"]
