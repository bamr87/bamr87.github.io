---
layout: default
title: "Features Index (Consolidated)"
description: "Automatically generated index of features across the bamr87 repositories."
permalink: /about/features/
sidebar:
  nav: about
lastmod: 2026-10-06T02:23:22Z
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
| Portfolio + dashboard from the registry | bamr87 | dash, registry, jekyll | /dashboard/ |
| Monitor board | bamr87 | dash, monitoring | /monitor/ |
| Fleet triage inbox | bamr87 | dash, triage, fleet-pulse | /triage/ |
| Issue pipeline board | bamr87 | dash, issues, agents | /issue-pipeline/ |
| AI harnesses inventory board | bamr87 | dash, harness, schedule | /harnesses/ |
| Six-layer harness scorecard | bamr87 | dash, harness, scorecard | /harness/ |
| Fleet features index | bamr87 | dash, verification, coverage, agents | /features/ |
| Harness Console (local control plane UI) | bamr87 | console, local, fastapi | /bamr87/tools/console/ |
| Roadmap | bamr87 | dash, roadmap | /roadmap/ |
| Engagements ledger | bamr87 | dash, finance | /engagements/ |
| Actions usage analytics | bamr87 | dash, actions, cost | /actions/ |
| Drift gate | bamr87 | gate, ci, drift | /bamr87/tools/check-drift.sh |
| Fan-out engine | bamr87 | fanout, kits, standardization | /bamr87/tools/fanout.sh |
| Agent verification kit + fleet-verify gate | bamr87 | verification, kits, agents, playwright | /bamr87/templates/verify/ |
| Repo evolution loop | bamr87 | loop, evolution, agents | /bamr87/.github/workflows/repo-evolution.yml |
| Fleet pulse + remediation doctor | bamr87 | loop, remediation, agents | /bamr87/.github/workflows/fleet-pulse.yml |
| Local data lake + Phoenix traces | bamr87 | lake, traces, local | /bamr87/.github/scripts/dash-gen/fleet_lake.py |
| Registry reconciliation | bamr87 | loop, registry | /bamr87/.github/workflows/reconcile-registry.yml |
| Schema vendor loop | bamr87 | loop, schema, vendoring | /bamr87/.github/workflows/schema-vendor.yml |
| Terminal command center | bamr87 | dash, tui, monitoring | /bamr87/tools/tui/app.py |
| CV projection | bamr87 | cv, projection | /bamr87/.github/scripts/dash-gen/cv_fragment.py |
| OpenAI service integration | barodybroject | openai, api | /src/services/openai_service.py |
| Django feature testing and CI | barodybroject | ci, django, testing | /.github/workflows/feature-test.yml |


## Requested / Backlog Features


*No backlog items found.*


---

*This index is generated automatically by `/scripts/generate_features_index.py`.


Last updated: 2026-10-06T02:23:22Z