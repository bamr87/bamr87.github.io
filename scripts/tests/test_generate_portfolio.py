"""Unit tests for the portfolio generator's pure (no-network) logic.

Run from the repo root: python -m pytest -q scripts/tests
"""

from scripts.generate_portfolio import (
    merge_project,
    pages_url,
    render_readme_block,
    render_portfolio_page,
    splice_readme,
    _strip_volatile,
    README_BEGIN,
    README_END,
)


def test_pages_url_prefers_homepage():
    assert pages_url('bamr87', 'foo', {'homepage': 'https://example.com'}) == 'https://example.com'
    # bare domain gets https:// prefix
    assert pages_url('bamr87', 'foo', {'homepage': 'example.com'}) == 'https://example.com'


def test_pages_url_falls_back_to_github_pages():
    assert pages_url('bamr87', 'proj', {'has_pages': True}) == 'https://bamr87.github.io/proj/'
    # the user/org site lives at the bare domain, not nested
    assert pages_url('bamr87', 'bamr87.github.io', {'has_pages': True}) == 'https://bamr87.github.io'
    # no homepage and no pages -> no live link
    assert pages_url('bamr87', 'proj', {}) is None


def test_merge_project_blurb_overrides_description():
    entry = {'repo': 'foo', 'featured': True, 'category': 'X', 'blurb': 'curated text'}
    meta = {'description': 'github text', 'stargazers_count': 5, 'language': 'Python'}
    p = merge_project('bamr87', entry, meta)
    assert p['description'] == 'curated text'   # blurb wins
    assert p['stars'] == 5 and p['language'] == 'Python' and p['featured'] is True


def test_merge_project_handles_missing_metadata():
    # A repo that failed to fetch (meta=None) still renders from registry data.
    p = merge_project('bamr87', {'repo': 'foo'}, None)
    assert p['repo'] == 'foo' and p['stars'] == 0 and p['featured'] is False
    assert p['repo_url'] == 'https://github.com/bamr87/foo'


def test_render_readme_block_only_includes_featured():
    projects = [
        merge_project('bamr87', {'repo': 'feat', 'featured': True, 'blurb': 'A'}, {}),
        merge_project('bamr87', {'repo': 'plain', 'blurb': 'B'}, {}),
    ]
    block = render_readme_block(projects)
    assert README_BEGIN in block and README_END in block
    assert 'feat' in block and 'plain' not in block


def test_splice_readme_replaces_existing_span():
    readme = f"intro\n{README_BEGIN}\nOLD\n{README_END}\noutro"
    out = splice_readme(readme, f"{README_BEGIN}\nNEW\n{README_END}")
    assert 'OLD' not in out and 'NEW' in out
    assert out.startswith('intro') and out.endswith('outro')


def test_splice_readme_appends_when_no_span():
    out = splice_readme('just intro', f"{README_BEGIN}\nNEW\n{README_END}")
    assert 'just intro' in out and 'NEW' in out and '## Portfolio' in out


def test_strip_volatile_ignores_timestamps():
    a = render_portfolio_page([], '2026-01-01T00:00:00Z')
    b = render_portfolio_page([], '2099-12-31T23:59:59Z')
    assert a != b                                   # timestamps differ
    assert _strip_volatile(a) == _strip_volatile(b)  # ...but substance is identical
