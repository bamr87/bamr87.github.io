---
name: profile-portfolio
description: >-
  Build and maintain the profile/portfolio landing page for the bamr87.github.io
  site — the curated showcase of GitHub repos, sites, and projects (badges,
  descriptions, live links, topics). Use this skill whenever the user wants to
  add, remove, reorder, feature, or refresh a project on their portfolio, profile,
  homepage, or "project dashboard"; when they mention showcasing a repo, updating
  project badges/stars/descriptions, or regenerating the projects list; or after
  shipping a new repo they'd want listed — even if they don't say the word
  "portfolio". Edits flow through _data/projects.yml and the generator script,
  never by hand-editing the rendered pages.
---

# Profile / Portfolio landing page

This site (`bamr87.github.io`) is the user's profile + portfolio landing page. The
showcase of their GitHub work is **data-driven**: a curated registry plus live
GitHub metadata, rendered into two surfaces by one generator. Editing the rendered
output by hand is a dead end — it gets overwritten on the next run. Always change
the source and regenerate.

## The pipeline at a glance

```
_data/projects.yml   →   scripts/generate_portfolio.py   →   pages/_about/portfolio/index.md   (full showcase page)
(curated registry)       (fetches live GitHub metadata)  →   README.md  AUTO:portfolio span     (featured table on homepage)
```

`README.md` is the site homepage (`permalink: /`), so the featured table appears on
the landing page; the full grouped showcase lives at `/about/portfolio/`.

This is the sibling of `scripts/generate_features_index.py` (which aggregates
*feature* metadata across repos). Same philosophy: a registry + the GitHub API +
deterministic, committable output.

## The registry: `_data/projects.yml`

This is the **single source of truth**. Display order follows file order. Schema:

```yaml
owner: bamr87            # GitHub owner the repos belong to
exclude:                 # repos that must never appear (clones, scratch, WIP)
  - some-clone
projects:
  - repo: it-journey     # required — the repo name under `owner`
    featured: true       # optional — show in homepage table + "Featured" section
    category: "Apps & AI" # optional — grouping heading on the portfolio page (default "Projects")
    blurb: "..."         # optional — overrides the GitHub description when it's weak/empty
```

Only `repo` is required. Everything else (stars, language, homepage/Pages URL,
topics, license, last commit) is fetched live from GitHub at generation time, so the
registry stays small and the page stays current without manual edits.

## Common tasks

**Add or feature a project** — append (or move) an entry in `_data/projects.yml`,
set `featured:`/`category:`/`blurb:` as desired, then regenerate. Put featured
projects where you want them in the homepage table; order matters.

**Remove a project from the showcase** — delete its entry, or add it to `exclude:`
if it keeps reappearing from some auto-source.

**Refresh metadata** (stars/descriptions/links changed upstream) — just rerun the
generator; no registry edit needed.

**Regenerate:**
```bash
python3 scripts/generate_portfolio.py          # writes only what actually changed
python3 scripts/generate_portfolio.py --check  # CI drift gate: exit 1 if output is stale
```

The generator resolves a GitHub token from `--token`, then `FEATURES_GITHUB_TOKEN`/
`GITHUB_TOKEN`/`GH_TOKEN`, then `gh auth token`. Public repos work without a token but
share a low unauthenticated rate limit, so a token is preferred. Output is
deterministic and timestamp-stable — a rerun with no upstream changes writes nothing,
which keeps diffs and CI clean.

## Conventions to preserve

- **Don't hand-edit** `pages/_about/portfolio/index.md` or the
  `<!-- AUTO:portfolio:start -->…<!-- AUTO:portfolio:end -->` span in `README.md`.
  Both carry a "generated — edit the registry instead" banner. Change
  `_data/projects.yml` and regenerate.
- A repo that fails to fetch (network off, renamed, private) renders from registry
  data alone and logs a warning — fix the `repo:` name if you see a 404 warning.
- After regenerating, review the diff, then commit registry + generated files
  together so the source and output never drift apart.
- If you add a fully new automation (e.g. a nightly refresh), mirror the existing
  `.github/workflows/generate-features-index.yml` workflow and commit with `[skip ci]`.

## Why this design

The user wants the site to be the definitive, low-maintenance showcase of their
work. A hand-maintained project list rots — stars go stale, links break, new repos
never get added. By curating *intent* (which repos, in what order, how described) in
a tiny YAML file and pulling *facts* (stars, language, live URL) from GitHub on every
build, the page stays accurate with near-zero upkeep, and the homepage + portfolio
page can never disagree because one generator writes both.
