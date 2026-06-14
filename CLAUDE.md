# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

`bamr87.github.io` — Amr Abdel-Motaleb's personal **GitHub Pages site**: a Jekyll site that is simultaneously a profile/CV landing page and a blog/docs/notes collection. It is published at https://bamr87.github.io.

This repo is also a **submodule of the `bamr87/bamr87` monorepo** (checked out under `projects/bamr87.github.io`). The monorepo's root `CLAUDE.md` (the "dash" / `_data/projects.yml` registry, `tools/dash`, etc.) describes the *parent* — none of that tooling applies here. Treat this as a standalone Jekyll repo with its own `main` branch and release cycle.

## The theme is remote — layouts/includes/CSS are NOT in this repo

`_config.yml` sets `remote_theme: bamr87/zer0-mistakes`. There is **no `_layouts/`, `_includes/`, or `_sass/` directory here.** Every layout referenced in front matter (`root`, `default`, `journals`, `collection`) and every include (e.g. the `setup-banner.html` that uses the `include_cached` tag) lives in the **[bamr87/zer0-mistakes](https://github.com/bamr87/zer0-mistakes)** theme repo.

Consequences:
- To change page markup, styling, navigation rendering, or fix a Liquid/layout error, edit the **theme repo**, not this one. This repo only supplies content, `_config.yml`, `_data/`, and `assets/`.
- Theme tags require their plugin to be registered in `_config.yml`'s `plugins:` list (e.g. `include_cached` needs `jekyll-include-cache`). A missing plugin surfaces as `Liquid syntax error … Unknown tag` at build time.

## Production vs. dev theme split (important build gotcha)

There are two build modes that resolve the theme differently:

| Mode | Config | Theme source | Jekyll |
|------|--------|--------------|--------|
| **Production (GitHub Pages)** | `_config.yml` | `remote_theme: bamr87/zer0-mistakes` (downloaded at build) | `github-pages` gem (Jekyll 3.9.x) |
| **Local / Docker dev** | `_config.yml` + `_config_dev.yml` | `_config_dev.yml` sets `remote_theme: false` and `theme: jekyll-theme-zer0` (local gem) | local bundle |

So local dev does **not** exercise the remote theme — it uses the `jekyll-theme-zer0` gem instead. A change that works locally can still break the published site if it depends on theme behavior, and vice versa.

## Deployment

GitHub Pages builds and deploys **automatically from the `main` branch** (the "pages build and deployment" check in Actions — GitHub's built-in Pages pipeline, not a workflow file in `.github/workflows/`). There is no custom deploy workflow. Pushing to `main` publishes the site.

## Content model

All content lives under `pages/` (`collections_dir: pages` in `_config.yml`). Collections:

| Dir | Collection | Notes |
|-----|-----------|-------|
| `pages/_posts/` | `posts` | Blog/journal. Filename convention `year-month-day-title.md`. Subfolders (`gpt/`, `recipies/`, `reflections/`, `reports/`) are categories. |
| `pages/_docs/` | `docs` | Documentation library. |
| `pages/_notes/` | `notes` | Personal notes/cheatsheets/snippets. |
| `pages/_hobbies/` | `hobbies` | |
| `pages/_notebooks/` | `notebooks` | |
| `pages/_about/` | `about` | Includes the auto-generated `features/index.md` (see below). |

Per-path **`defaults`** in `_config.yml` assign each collection its `layout`, `sidebar.nav`, and permalink — set defaults there rather than repeating front matter in every file. **`README.md` at the repo root is the site homepage** (`permalink: /`, `layout: default`) and also holds the profile + CV content; editing it changes the live home page.

Sidebar navigation is data-driven: `_data/navigation/*.yml` files (`main`, `about`, `docs`, `hobbies`, `posts`, `home`) are selected by the `sidebar.nav` key wired up in `_config.yml` `defaults`.

## Generated content (registries → generators → pages)

Two parts of the site are **generated from data, not hand-written**. Edit the source registry and rerun the generator; never edit the rendered output (it gets overwritten). Both are committed to the repo and refreshed nightly by [`.github/workflows/generate-features-index.yml`](.github/workflows/generate-features-index.yml) (workflow display name "Regenerate site indexes", cron `0 2 * * *`, commits with `[skip ci]`). This is the **only** workflow file in the repo.

**Portfolio / profile landing page** — `scripts/generate_portfolio.py` reads the curated registry [`_data/projects.yml`](_data/projects.yml), fetches live GitHub metadata (stars, language, homepage/Pages URL, topics), and writes both `pages/_about/portfolio/index.md` (full showcase) and the `<!-- AUTO:portfolio:start -->…<!-- AUTO:portfolio:end -->` span in `README.md` (featured table on the homepage). Output is idempotent — a rerun with no upstream change writes nothing (timestamps are stripped when diffing). `--check` is a drift gate (exit 1 if stale). Token resolves from `--token` → `FEATURES_GITHUB_TOKEN`/`GITHUB_TOKEN`/`GH_TOKEN` → `gh auth token`. There is a dedicated skill for this in [`.claude/skills/profile-portfolio/`](.claude/skills/profile-portfolio/SKILL.md).

**Features index** — `scripts/generate_features_index.py` aggregates `features:` metadata across the user's repos into `pages/_about/features/index.md`. Sources per repo (priority order): `features/features.yml`, `FEATURES.yml`/`.yaml`, `FEATURES.md`, then the repo's own `pages/_about/features/`.
- Remote mode (CI default): `python3 scripts/generate_features_index.py --mode=remote --owner=bamr87 --token=$GH_TOKEN`.
- Local mode: `--mode=local --root=/path/to/workspace` scans sibling repos on disk.
- `scripts/validate_features.py` is a standalone validator other repos can run in PR CI.
- YAML `tags` may contain non-strings (e.g. a bare year) — coerce to `str` before joining in the table-rendering code, or it raises `TypeError` in CI.

## Common commands

**Jekyll (Ruby):**
```bash
bundle install
bundle exec jekyll serve                                   # production-like: remote theme, port 4002
bundle exec jekyll serve --config _config.yml,_config_dev.yml   # dev: local jekyll-theme-zer0 gem
```
`_config.yml` is **not** auto-reloaded — restart the server after editing it. Site serves on port **4002** (`port:` in `_config.yml`; `EXPOSE 4002` in the Dockerfile).

**Docker** (uses the local-theme dev config, serves on 4002):
```bash
docker build -t bamr87.github.io .
docker run -d -p 4002:4002 -v "$PWD":/app --name bamr87.github.io-container bamr87.github.io
```
(There is no `docker-compose.yml` in this repo despite the README mention; only the `Dockerfile`.)

**Features script (Python):**
```bash
python3 -m pip install -r scripts/requirements.txt
python -m pytest -q scripts/tests                                              # run tests
pytest scripts/tests/test_generate_features_index.py::test_build_markdown -v   # single test
```
Tests import `from scripts.generate_features_index import …`, so **run pytest from the repo root** (not from inside `scripts/`).

## Conventions

- **Commits**: Conventional Commits (`type(scope): description`). CI-authored commits append `[skip ci]`.
- **Front matter**: prefer setting shared values (`layout`, `sidebar.nav`, permalink) via `_config.yml` `defaults` by path; use `draft: true` for unpublished content; posts carry `date` + `lastmod`.
- Do not commit `_site/`, `Gemfile.lock`, `vendor/`, or `.jekyll-cache/` (see `.gitignore`).
