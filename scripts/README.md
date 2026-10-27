# Site generation scripts

> The generators that write the site's portfolio, features index and collections reference from curated sources, how to run each one, and the validator other repos use for their features metadata.

The two GitHub-backed generators follow the same pattern: a small curated source plus live GitHub metadata becomes committed, deterministic Markdown. All three are idempotent: a rerun with no input change writes nothing.

## `generate_portfolio.py` — profile / portfolio landing page

Reads the curated registry `_data/projects.yml`, fetches live metadata for each repo from the GitHub API (stars, language, homepage / GitHub Pages URL, topics, license, last commit), and writes three outputs:

- `_data/portfolio.yml` — enriched data and totals the homepage dashboard (`index.html`) renders via `site.data.portfolio`.
- `pages/_about/portfolio/index.md` — the full showcase, grouped by category.
- the `<!-- AUTO:portfolio:start -->…<!-- AUTO:portfolio:end -->` span in `README.md` — the featured table on the GitHub profile and the `/profile/` page.

```bash
python3 scripts/generate_portfolio.py            # regenerate (writes only what changed)
python3 scripts/generate_portfolio.py --check    # CI drift gate: exit 1 if output is stale
python3 scripts/generate_portfolio.py --owner bamr87 --token "$GH_TOKEN"
```

To add / reorder / feature a project, edit `_data/projects.yml` (display order = file order) and rerun — do not hand-edit the generated files. A token resolves from `--token`, then `FEATURES_GITHUB_TOKEN`/`GITHUB_TOKEN`/`GH_TOKEN`, then `gh auth token`; public repos work without one but share a low rate limit. Output is timestamp-stable, so a no-op rerun produces no diff. See `.claude/skills/profile-portfolio/SKILL.md` for the full workflow.

## `generate_features_index.py` — consolidated features index

This script scans sibling repos in the workspace (local mode) or fetches feature metadata from GitHub (remote mode) and generates `pages/_about/features/index.md` that consolidates features across all repositories.

Supported metadata sources (per repo):

- `features/features.yml` or `features/features.yaml` (preferred)
- `FEATURES.yml` or `FEATURES.yaml`
- `FEATURES.md`, `features.md` (Markdown with YAML frontmatter defining `features:` key)
- `pages/_about/features/index.md` (if repo exposes such a page with features metadata in frontmatter)

Metadata YAML format:

```yaml
features:
  - id: FR-0001
    title: "Auto-generated feature list"
    description: "Short description"
    implemented: true
    link: "/path/to/detail"
    tags: [site, automation]
    date: 2025-11-01
```

Running locally:

```bash
# Install script dependencies (PyYAML, pytest for tests)
python3 -m pip install -r scripts/requirements.txt

# Local mode (workspace contains sibling repos):
python3 scripts/generate_features_index.py --mode=local --root=/path/to/repos
```

Running remotely (GitHub API):

```bash
# Requires a token for private repo fetching (or public content is fine):
FEATURES_GITHUB_TOKEN=$GH_TOKEN python3 scripts/generate_features_index.py --mode=remote --owner=bamr87
```

The script writes to `pages/_about/features/index.md` by default — make sure the repository has commit access if you plan to have a scheduled GitHub Action commit updates automatically.

Automation: `.github/workflows/generate-features-index.yml` ("Regenerate site indexes") runs both GitHub-backed generators nightly at 02:00 UTC and on `workflow_dispatch` (the features index in remote mode), with the `FEATURES_GITHUB_TOKEN` secret. It runs `scripts/tests` first (non-blocking) and commits any change with `[skip ci]`. Each repo declares its features in a short `features/features.yml` (this repo's is the example).

If you'd like, the script can be extended to fetch additional context (issues, PRs, changelog, release tags) or render richer tables, badges and links.

Validator: a minimal validator is available at `scripts/validate_features.py`. Repositories can copy `scripts/feature-validator-template.yml` into `.github/workflows/` to run it on pull requests, so their `features` metadata is checked before changes are merged.

## `generate_collections_reference.py` — collections reference

Reads `_config.yml` (`collections_dir`, `collections:`, `defaults:`) and writes [`docs/reference/collections.md`](../docs/reference/collections.md): every declared collection with its directory, whether that directory exists, its permalink, and the layout and sidebar its front-matter defaults resolve to. No network, no token.

```bash
python3 scripts/generate_collections_reference.py           # rewrite the reference
python3 scripts/generate_collections_reference.py --check   # exit 1 if it is stale
```

`scripts/tests/test_generate_collections_reference.py` runs the same check, so editing a collection or a default without regenerating fails the tests.

## Tests

`python -m pytest -q scripts/tests` from the repo root. Besides the generator unit tests, `tests/test_content_links.py` is an offline guard over `pages/`: hosts verified dead may only be linked through a `web.archive.org` snapshot, the retired `{{ site.github_user }}.netlify.*` mirror is never hyperlinked, no image loads over plain `http://` (mixed content), and the Markdown cheat sheet's Liquid example stays a single raw code block. When a link dies, replace it with a Wayback snapshot if one exists (otherwise unlink it and keep the text), and add the host to `DEAD` there.
