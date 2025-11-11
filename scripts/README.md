# Feature index generation script

This folder contains a small utility to generate a consolidated features index page for the
site. The script scans sibling repos in the workspace (local mode) or fetches feature metadata
from GitHub (remote mode) and generates `pages/_about/features/index.md` that consolidates
features across all repositories.

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

The script writes to `pages/_about/features/index.md` by default — make sure the repository has
commit access if you plan to have a scheduled GitHub Action commit updates automatically.

Automation idea:

- Add a GitHub Action in this repo to run the script nightly or via `workflow_dispatch`.
- The action requires a `FEATURES_GITHUB_TOKEN` (Personal Access Token) if it needs to access
  private repos; otherwise the default `GITHUB_TOKEN` works for public content.
- Each repo should adopt a short `features/features.yml` file to declare features — see sample
  `examples` directory.

If you'd like, the script can be extended to fetch additional context (issues, PRs, changelog,
release tags) or render richer tables, badges and links.

Validator:
  A minimal validator is available at `scripts/validate_features.py`. Repositories can add a
  workflow to run this file during PRs to ensure they publish and maintain good `features` metadata
  before changes are merged.
