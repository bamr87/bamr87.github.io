# Site generation scripts

This folder holds the data-driven generators for the site. Both follow the same pattern: a small curated source + live GitHub metadata → committed, deterministic Markdown.

## `generate_portfolio.py` — profile / portfolio landing page

Reads the curated registry `_data/projects.yml`, fetches live metadata for each repo from the GitHub API (stars, language, homepage / GitHub Pages URL, topics, license, last commit), and renders two surfaces:

- `pages/_about/portfolio/index.md` — the full showcase, grouped by category.
- the `<!-- AUTO:portfolio:start -->…<!-- AUTO:portfolio:end -->` span in `README.md` — the
  featured table on the homepage.

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

Automation idea:

- Add a GitHub Action in this repo to run the script nightly or via `workflow_dispatch`.
- The action requires a `FEATURES_GITHUB_TOKEN` (Personal Access Token) if it needs to access
  private repos; otherwise the default `GITHUB_TOKEN` works for public content.
- Each repo should adopt a short `features/features.yml` file to declare features — see sample
  `examples` directory.

If you'd like, the script can be extended to fetch additional context (issues, PRs, changelog, release tags) or render richer tables, badges and links.

Validator: A minimal validator is available at `scripts/validate_features.py`. Repositories can add a workflow to run this file during PRs to ensure they publish and maintain good `features` metadata before changes are merged.
