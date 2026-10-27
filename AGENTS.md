<!-- kit: sdlc v0.1.0 · AGENTS.md is the CANONICAL agent instructions file (decision D4, UPS-AGENT-07/08). -->

# bamr87.github.io

> Amr Abdel-Motaleb's GitHub Pages site — profile, résumé and project portfolio plus blog, docs and notes collections — and the rules for changing it.

## What this repo is

A Jekyll site on GitHub Pages, published at <https://bamr87.github.io>. It is both a profile/CV landing page and a blog, docs and notes collection, and it serves visitors (recruiters, clients, collaborators) and Amr as author. A change is done when the scripts tests pass, the prose gate is clean, every generator's `--check` is current, and the site still builds with the production config (`bundle exec jekyll build`). Agent, contributor and data files (`AGENTS.md`, `CLAUDE.md`, `CHANGELOG.md`, `PRD.md`, `scripts/`) are excluded from the build. `docs/` is not, so it is published as plain pages.

## Stack & commands

Jekyll 3.10 via the `github-pages` gem, the remote `bamr87/zer0-mistakes` theme, and Python 3 generators (PyYAML, pytest).

```bash
bundle install                                                  # Ruby deps: github-pages + the theme gem
bundle exec jekyll serve                                        # production-like preview on :4002 (remote theme)
bundle exec jekyll serve --config _config.yml,_config_dev.yml   # dev preview with the local jekyll-theme-zer0 gem
python3 -m pip install -r scripts/requirements.txt              # generator deps (PyYAML, pytest)
python -m pytest -q scripts/tests                               # generator tests — run from the repo root
python3 tools/unwrap-prose.py --check                           # markdown one-paragraph-per-line gate
```

## Layout

| Path | Holds |
| --- | --- |
| `pages/` | All site content (`collections_dir: pages`): one `_<collection>/` per collection — see [docs/reference/collections.md](docs/reference/collections.md) |
| `_data/` | Project registry, generated portfolio data, navigation menus, UI strings — see [_data/README.md](_data/README.md) |
| `_config.yml`, `_config_dev.yml` | Production config, and the dev overlay that swaps in the local theme gem |
| `index.html` | The homepage dashboard (`permalink: /`), built from `site.data.portfolio` |
| `README.md` | The GitHub profile/CV, published at `/profile/` |
| `assets/` | Site images, scripts and SVGs (the theme ships the CSS) |
| `scripts/` | Generators and their tests — see [scripts/README.md](scripts/README.md) |
| `tools/` | Vendored fleet tools: `unwrap-prose.py`, `docs_index.py` (never edit) |
| `docs/` | Repo documentation: [the docs index](docs/README.md), ADRs, generated reference |
| `features/`, `verify/` | Feature index (`features/v1`) and the user-scenario verify kit |
| `.claude/` | The `profile-portfolio` and `verify-feature` skills and the `verifier` agent |

## Conventions

- **Backlog of record:** GitHub Issues with the fleet labels (`.github/sdlc.yml`: `backlog.mode: issues`).
- **Definition of Done:** the pull request checklist inherited from bamr87/.github (no template in this tree), plus the "done" bar above.
- **Decisions:** ADRs in `docs/adr/NNNN-slug.md`, indexed in `docs/adr/README.md`.
- **Commits:** Conventional Commits (`type(scope): description`); the PR title is the squash subject. CI-authored commits append `[skip ci]`.
- **Branches:** `feature/`, `fix/`, `docs/`, `refactor/`, `test/` or `chore/` off `main`.
- **Changelog:** `CHANGELOG.md` is written by release-please (`release.yml` → the hub's `release-please.yml@v2`, release type `simple`). Never edit it by hand.
- **Front matter:** set shared values (`layout`, `sidebar.nav`, permalink) through `_config.yml` `defaults:` by path, not per file. Use `draft: true` for unpublished content. Posts carry `date` and `lastmod`.
- **Never:** push to `main` directly, hand-edit a generated file, or commit `_site/`, `Gemfile.lock`, `vendor/` or `.jekyll-cache/`.

## The theme is remote

- `_config.yml` sets `remote_theme: bamr87/zer0-mistakes`, so there is no `_layouts/`, `_includes/` or `_sass/` here. Every layout (`root`, `default`, `article`, `home`, …) and include lives in [bamr87/zer0-mistakes](https://github.com/bamr87/zer0-mistakes): fix markup, styling, navigation rendering and Liquid/layout errors there. This repo supplies content, `_config.yml`, `_data/` and `assets/`.
- A theme tag needs its plugin in `_config.yml` `plugins:` (`include_cached` needs `jekyll-include-cache`); a missing one fails the build with `Liquid syntax error … Unknown tag`.
- The two build modes resolve the theme differently, so a change that works locally can still break the published site:

| Mode | Config | Theme source |
| --- | --- | --- |
| Production (GitHub Pages) | `_config.yml` | `remote_theme`, downloaded at build (`github-pages` gem, Jekyll 3.10) |
| Local / Docker dev | `_config.yml,_config_dev.yml` | `remote_theme: false` + the local `jekyll-theme-zer0` gem |

## Content and navigation

- Collections, their directories, permalinks and resolved defaults are generated into [docs/reference/collections.md](docs/reference/collections.md) from `_config.yml`. Posts are named `YYYY-MM-DD-title.md`; subfolders of `pages/_posts/` (`gpt/`, `recipies/`, `reflections/`, `reports/`) are categories.
- `index.html` is the homepage: a full-bleed dashboard over `site.data.portfolio`, with inline CSS/JS scoped under `.dash` and its JS wrapped in a Liquid `raw`/`endraw` block so Liquid leaves it alone.
- `README.md` is a Jekyll page (`permalink: /profile/`), so its links are rendered on the site. Relative links to excluded files 404 there; link those by GitHub URL.
- Navigation is `_data/navigation/*.yml`: the navbar reads `main.yml`, and a page picks its sidebar with `sidebar.nav`. The theme's navbar and `nav-tree` read `children:`, not `sublinks:`; with `sublinks:` the dropdowns silently do not render.

## Generated content

Edit the source, rerun the generator, never edit the output.

- **Portfolio:** `scripts/generate_portfolio.py` reads `_data/projects.yml`, adds live GitHub metadata, and writes `_data/portfolio.yml`, `pages/_about/portfolio/index.md` and the `AUTO:portfolio` span in `README.md`. `--check` is its drift gate. It needs a token (from `--token`, then `FEATURES_GITHUB_TOKEN`/`GITHUB_TOKEN`/`GH_TOKEN`, then `gh auth token`) or public rate limits. A project's `live_url` overrides the Live link (`false`/`none` hides it). Skill: `.claude/skills/profile-portfolio/`.
- **Features index:** `scripts/generate_features_index.py --mode=remote --owner=bamr87` (or `--mode=local --root=<workspace>`) writes `pages/_about/features/index.md` from each repo's `features/features.yml` and its fallbacks. YAML `tags` may be non-strings (a bare year): coerce to `str` before joining. `scripts/validate_features.py` is the standalone validator.
- **Collections reference:** `python3 scripts/generate_collections_reference.py` writes `docs/reference/collections.md`. A test in `scripts/tests` fails when it is stale.
- **Docs index:** `python3 tools/docs_index.py --write` regenerates the span in `docs/README.md` from each document's summary line (`--check`, `--lint`).
- The nightly `generate-features-index.yml` ("Regenerate site indexes", 02:00 UTC) reruns the portfolio and features generators and commits with `[skip ci]`.

## Build and CI gotchas

- GitHub Pages builds and deploys from `main` with its built-in pipeline; no workflow here deploys. Pushing to `main` publishes.
- Workflows: `ci.yml` (hub `standard-ci.yml@v2`), `markdown-oneline.yml` (pushes the unwrap fix back to a PR), `site-quality.yml`, `link-check.yml` (htmlproofer on the built `_site`: no internal link to a missing page), `verify.yml`, `conformance.yml`, `release.yml`, `claude.yml` (`@claude`), and the nightly `generate-features-index.yml`.
- `_config.yml` is not auto-reloaded: restart `jekyll serve` after editing it. The site serves on port 4002 (`port:` in `_config.yml`; `EXPOSE 4002` in the `Dockerfile`).
- In a POSIX locale the theme's Sass fails with `Invalid US-ASCII character`; build with `LANG=C.UTF-8`.
- Docker uses the dev config: `docker build -t bamr87.github.io .` then `docker run -d -p 4002:4002 -v "$PWD":/app --name bamr87.github.io-container bamr87.github.io`. There is no `docker-compose.yml`.
- The scripts tests import `scripts.*`, so run pytest from the repo root, not from inside `scripts/`.

## Fleet context

Member of the bamr87 fleet, mounted in the hub as the submodule `projects/bamr87.github.io`. Commit and push here first; the hub only bumps its pointer. The hub's own tooling (`tools/dash`, its registry) does not run in this repo. Standards: <https://github.com/bamr87/bamr87/tree/main/specs>. The loops that act on this repo are the hub's shared gates (`standard-ci`, `fleet-conformance`, `fleet-verify`, `site-quality`), the hub's fan-out kits (which seeded `tools/unwrap-prose.py`, the SDLC files and the verify kit), the `@claude` handler and the nightly index regeneration.

## Standard deviations

- UPS-DOC-08: `README.md` is over the 2,000-word budget because it is the published résumé at `/profile/`; its length is the CV itself, not repo documentation.
- UPS-DOC-10: `README.md` keeps the résumé's own order (front-matter title, About Me, dashboard, CV) instead of the portfolio skeleton's H1, tagline, Overview and Features, because it is a published CV page. It ends with **Working with this repo** and **License**, and links the docs index.

## Governance

Read [`docs/constitution.md`](docs/constitution.md) before changing anything: it is the highest-precedence rule set here and wins over this file when they disagree. It changes only through a numbered record in [`docs/amendments/`](docs/amendments/), ratified by the maintainer merging the PR; agents propose, never merge. Every user-facing feature has a stable id in [`features/features.yml`](features/features.yml) with `status`, location and the PRD requirement ids it serves; the PRD's "Feature catalog" block is generated from it (`python3 <bamr87/bamr87>/tools/governance_lint.py prd-sync . --write`; check with `… check .`). Never hand-edit that block or `CHANGELOG.md`.
