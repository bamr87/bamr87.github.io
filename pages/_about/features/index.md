---
layout: default
title: "Features Index (Consolidated)"
lastmod: 2025-12-31T02:42:24Z
---


---
title: "Consolidated Feature Index"
description: "Automatically generated index of features implemented or in backlog across all of the org's repositories."
type: default
permalink: /about/features/
---

# Consolidated Features Index

This page is a consolidated list of site features, project-level feature entries and backlog items across repositories owned in the `bamr87` organization. The list is generated automatically by the site-level generator script (`/scripts/generate_features_index.py`).

## How features are discovered

1. Each repository should include a short feature metadata file at one of these locations:
   - `features/features.yml` (preferred)
   - `FEATURES.yml`
   - `FEATURES.md` / `features.md` (Markdown with YAML front matter that includes a `features:` list)
   - `pages/_about/features/index.md` (if the repo exposes such a page with YAML frontmatter)
2. The generator supports both local and remote modes (GitHub API). See `/scripts/README.md` for details.

## The per-repo metadata standard

Minimal example (YAML):

```yaml
features:
  - id: FR-0001
    title: "Human-friendly feature name"
    description: "Short description"
    implemented: true
    link: "/pages/xxx/"
    tags: [site, jekyll]
    date: 2025-11-11
```

## Automation & validation

The site runbook contains a validator `scripts/validate_features.py` and a workflow template `scripts/feature-validator-template.yml` that repository maintainers can adopt to ensure PRs validate the `features` metadata before merge.

---

## Current Features


| Title | Repo | Tags | Link |
| --- | --- | --- | --- |
| OpenAI service integration | barodybroject | openai, api | /src/services/openai_service.py |
| Django feature testing and CI | barodybroject | ci, django, testing | /.github/workflows/feature-test.yml |


## Requested / Backlog Features


*No backlog items found.*


---

*This index is generated automatically by `/scripts/generate_features_index.py`.


Last updated: 2025-12-31T02:42:24Z