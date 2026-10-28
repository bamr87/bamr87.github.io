---
layout: default
title: "Features Index (Consolidated)"
description: "Automatically generated index of features across the bamr87 repositories."
permalink: /about/features/
sidebar:
  nav: about
lastmod: 2026-10-28T02:13:49Z
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
| Reusable workflows: release-please.yml, publish.yml | .github |  | /.github/.github/workflows/release-please.yml |
| Composite actions under .github/actions/ | .github |  | /.github/.github/actions |
| Starter workflow workflow-templates/release.yml | .github |  | /.github/workflow-templates/release.yml |
| Issue/PR templates | .github |  | /.github/.github/ISSUE_TEMPLATE |
| Portfolio + dashboard from the registry | bamr87 | dash, registry, portfolio | /portfolio |
| Projects board | bamr87 | dash, monitoring | /projects |
| Fleet triage inbox | bamr87 | dash, triage, fleet-pulse | /inbox |
| Issue pipeline board | bamr87 | dash, issues, agents | /loops/issue_pipeline |
| AI harnesses inventory board | bamr87 | dash, harness, schedule | /harnesses |
| Six-layer harness scorecard | bamr87 | dash, harness, scorecard | /harnesses/health |
| Fleet features index | bamr87 | dash, verification, coverage, agents | /features |
| Harness Console (local control plane UI) | bamr87 | console, local, fastapi | /bamr87/tools/console/ |
| The public site is the console (GitHub Pages) | bamr87 | dash, console, pages, portfolio, github | /connect |
| Roadmap | bamr87 | dash, roadmap | /roadmap |
| Engagements ledger | bamr87 | dash, finance | /engagements |
| Actions usage analytics | bamr87 | dash, actions, cost | /costs |
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
| Governance kit: constitution, amendments, PRD and feature link | bamr87 | governance, features, prd, fan-out | /bamr87/tools/governance_lint.py |
| Backlog fan-out routine | bamr87 | fan-out, backlog, automation, activity-log | /bamr87/.github/workflows/backlog-fanout.yml |
| Profile & résumé page | bamr87.github.io |  | /bamr87.github.io/README.md |
| Featured projects table and portfolio pages under pages/ | bamr87.github.io |  | /bamr87.github.io/pages |
| Dockerfile for local preview | bamr87.github.io |  | /bamr87.github.io/Dockerfile |
| Scripts/tools for site maintenance | bamr87.github.io |  | /bamr87.github.io/scripts |
| Web app (bamr87.github.io/bashcrawl) | bashcrawl |  | /bashcrawl/web/index.html |
| Classic terminal dungeon | bashcrawl |  | /bashcrawl/entrance |
| XP/score persistence across modes | bashcrawl |  |  |
| Content data | bashcrawl |  | /bashcrawl/src/help/data/rooms.yaml |
| /sh command | bashos |  | /bashos/.claude/commands/sh.md |
| /explain command | bashos |  | /bashos/.claude/commands/explain.md |
| /script command | bashos |  | /bashos/.claude/commands/script.md |
| /debug command | bashos |  | /bashos/.claude/commands/debug.md |
| /sys command | bashos |  | /bashos/.claude/commands/sys.md |
| /health command | bashos |  | /bashos/.claude/commands/health.md |
| /dash command | bashos |  | /bashos/.claude/commands/dash.md |
| /pipe command | bashos |  | /bashos/.claude/commands/pipe.md |
| /regex command | bashos |  | /bashos/.claude/commands/regex.md |
| /cron command | bashos |  | /bashos/.claude/commands/cron.md |
| /port command | bashos |  | /bashos/.claude/commands/port.md |
| /audit command | bashos |  | /bashos/.claude/commands/audit.md |
| Desktop scene: Overview | bashos |  | /bashos/src/bashos/gui |
| Desktop scene: Console | bashos |  | /bashos/src/bashos/gui |
| Desktop scene: Commands | bashos |  | /bashos/src/bashos/gui |
| Desktop scene: Runs | bashos |  | /bashos/src/bashos/gui |
| Desktop scene: Health | bashos |  | /bashos/src/bashos/gui |
| Desktop scene: Engine | bashos |  | /bashos/src/bashos/gui |
| Desktop scene: Side by side | bashos |  | /bashos/src/bashos/gui |
| Desktop scene: Desktop | bashos |  | /bashos/src/bashos/gui |
| One-shot CLI and terminal desktop | bashos |  | /bashos/src/bashos |
| Claude Code OAuth wiring | bashos |  | /bashos/src/bashos |
| Safety model | bashos |  | /bashos/src/bashos |
| Optional Docker services | bashos |  | /bashos/docker-compose.yml |
| chui terminal environment (macOS) | bashos |  | /bashos/chui |
| Window list and layout serialization | bashos |  | /bashos/src/bashos/gui |
| CV data management | cv-pro |  | /cv-pro/app/src/components/cv |
| LaTeX template system | cv-pro |  | /cv-pro/app/src/lib/latex-templates.ts |
| AI CV parser | cv-pro |  | /cv-pro/app/src/components/cv/AIParser.tsx |
| Multi-format export | cv-pro |  | /cv-pro/app/src/components/cv/ExportSection.tsx |
| TODO: the first thing a user does here | djangoerp | todo | / |
| TODO: the first thing a user does here | fredgar-ai | todo | / |
| TODO: the first thing a user does here | githubai | todo | / |
| Drag-and-drop canvas | gitorio |  | /gitorio/app/src/canvas |
| Blueprint → Actions workflow compiler with vitest invariant tests | gitorio |  | /gitorio/app/src/compiler |
| Demo mode ?demo=1 on a fixture-backed three-repo fleet | gitorio |  | /gitorio/app/src/demo |
| Fleet Ops cockpit and telemetry views | gitorio |  | /gitorio/app/src/fleet |
| Packages absorbed under packages/ | gitorio |  | /gitorio/packages |
| Docker and VS Code task/debug workflows | gitorio |  | /gitorio/.vscode/tasks.json |
| Framework addon with zero-dependency test runner | godotgo |  | /godotgo/framework/addons |
| Sample games: orb-run, leap, swarm, shift, cascade | godotgo |  | /godotgo/games |
| Tools: install_godot, verify, run, export, new_game | godotgo |  | /godotgo/tools |
| Generated placeholder sprites/sounds/meshes | godotgo |  | /godotgo/tools/gen_assets.py |
| Docker image and CI verifying every project in parallel | godotgo |  | /godotgo/docker/Dockerfile |
| Claude Code settings | godotgo |  | /godotgo/.claude/settings.json |
| Jekyll site generation | it-journey | site, jekyll, build | / |
| Algolia Search indexing | it-journey | search, algolia | /search/ |
| Auto features index generation | it-journey | automation, features | /about/features/ |
| Quest collection | it-journey |  | /quests/ |
| Interactive terminal interface | it-journey |  | /it-journey/journey.sh |
| Docker development and quest validation | it-journey |  | /it-journey/docker-compose.yml |
| Quest validation workflow | it-journey |  | /it-journey/.github/workflows/quest-validation.yml |
| Front matter validation | it-journey |  | /it-journey/.github/workflows/frontmatter-validation.yml |
| Link health check | it-journey |  | /it-journey/scripts/validation/link-checker.py |
| PRD synchronization (prd-machine) | it-journey |  | /it-journey/scripts/prd-machine |
| Data ingestion and knowledge graph foundation | law-ai |  | /law-ai/backend/law_ai/ingestionapp |
| Core agent crews | law-ai |  | /law-ai/backend/law_ai/agents_runtime |
| LSAT Learning Lab | law-ai |  | /law-ai/backend/law_ai/lsat |
| Provenance and audit log | law-ai |  | /law-ai/backend/law_ai/audit |
| LegalBench evaluation harness | law-ai |  | /law-ai/backend/law_ai/eval |
| News sections Hacks / Tools / Field notes / Wire under pages/_posts/ | lifehacker.dev |  | /lifehacker.dev/pages/_posts |
| Machine-readable brand in _data/brand/ | lifehacker.dev |  | /lifehacker.dev/_data/brand |
| Content backlog _data/backlog.yml with a custom merge driver | lifehacker.dev |  | /lifehacker.dev/_data/backlog.yml |
| Wire assignment editor _data/wire/sources.yml | lifehacker.dev |  | /lifehacker.dev/_data/wire/sources.yml |
| Offline-generated cover art | lifehacker.dev |  | /lifehacker.dev/scripts/preview |
| CI harness: Pages safe-mode build plus front-matter,… | lifehacker.dev |  | /lifehacker.dev/.github/workflows/ci.yml |
| Author personas in _data/authors.yml | lifehacker.dev |  | /lifehacker.dev/_data/authors.yml |
| CLI: scan, ingest | ocrmd |  | /ocrmd/ocrmd/cli.py |
| Local OCR: Apple Vision + RapidOCR voting (Tesseract… | ocrmd |  | /ocrmd/ocrmd/ocr.py |
| Vision-model providers: Anthropic (default) and xAI | ocrmd |  | /ocrmd/ocrmd/llm.py |
| Corpus per document | ocrmd |  | /ocrmd/ocrmd/store.py |
| Exports: md, txt, json, jsonl | ocrmd |  | /ocrmd/ocrmd/export |
| Structured-data ETL pipelines and destinations | ocrmd |  | /ocrmd/ocrmd/etl.py |
| Agents: scout (env/clock), claimant-a (fast), claimant-b… | outbox |  | /outbox/agents |
| CLI: run, watch, suite | outbox |  | /outbox/src/outbox/cli.py |
| Task families: stale_fact, ambiguous, deadline | outbox |  | /outbox/tasks |
| Relay to inboxes + ledger.jsonl | outbox |  | /outbox/src/outbox/mailbox.py |
| Scoring: winner, correctness, confidence inversion, retracts | outbox |  | /outbox/src/outbox/score.py |
| Belt profile: handoff messages through one gapless, crash-repairable relay | outbox |  | /outbox/src/outbox/belt.py |
| Claim desk: race a draft's claims, resolve later, calibrate | outbox |  | /outbox/src/outbox/claimdesk.py |
| Local end-to-end proof of the platform plan across the sibling repos | outbox |  | /outbox/e2e/run.py |
| Crawl | README |  | /README/scripts |
| Extract | README |  | /README/context |
| Navigate | README |  | /README/context |
| Synthesize | README |  | /README/context |
| Assemble | README |  | /README/context |
| Index | README |  | /README/context |
| Serve | README |  | /README/mcp |
| Evolve | README |  | /README/hooks.d |
| arcade/: React + canvas + Web Audio games | rewind-arcade |  | /rewind-arcade/arcade |
| emulate/ / retro-pi/ | rewind-arcade |  | /rewind-arcade/emulate |
| catalog/: cartridge-index (stdlib Python): dumps,… | rewind-arcade |  | /rewind-arcade/catalog |
| systems/registry.yaml + docs encyclopedia | rewind-arcade |  | /rewind-arcade/systems/registry.yaml |
| Tests that enforce the system-id map across pillars | rewind-arcade |  | /rewind-arcade/catalog/tests |
| Generate challenges by bits or digits | rsa-challenge |  | /rsa-challenge/rsa_challenge/cli.py |
| Public challenge file with commitments | rsa-challenge |  | /rsa-challenge/challenges/challenges.json |
| Secrets kept out of git | rsa-challenge |  | /rsa-challenge/scripts/check_no_secrets.py |
| Verify submissions from the CLI | rsa-challenge |  | /rsa-challenge/rsa_challenge/challenge.py |
| Client-side verification site | rsa-challenge |  | /rsa-challenge/site/index.html |
| Seeded challenge ladder | rsa-challenge |  | /rsa-challenge/challenges/challenges.json |
| tools/schema_lint.py | SCHEMA |  | /SCHEMA/tools/schema_lint.py |
| Federation checks across submodule seams | SCHEMA |  | /SCHEMA/tools/schema_lint.py |
| DISTRIBUTION.yml + tools/schema_dist.py | SCHEMA |  | /SCHEMA/DISTRIBUTION.yml |
| CLAUDE.md protocol snippet | SCHEMA |  | /SCHEMA/protocol |
| Seed templates and lint-green example fixture repos | SCHEMA |  | /SCHEMA/templates/SCHEMA.template.md |
| Scenario test suite | SCHEMA |  | /SCHEMA/tests/test_schema_lint.py |
| Project initialization wizard | scripts | scaffolding | /scripts/project-init.sh |
| ForkMe repository forking/cloning | scripts | github | /scripts/FORKME/forkme.sh |
| StashMe multi-repo cloud stash | scripts | multi-repo, backup | /scripts/STASHME/stashme.sh |
| Git + GitHub repository creator | scripts | github, scaffolding | /scripts/git_init.sh |
| Safe directory rename | scripts | filesystem | /scripts/rename-directory.sh |
| Python package bootstrap | scripts | scaffolding, python | /scripts/create_package.sh |
| Markdown prose unwrapper | scripts | docs, lint | /scripts/tools/unwrap-prose.py |
| install.sh standalone installer | scripts |  | /scripts/install.sh |
| Run code | vs-sonic-pi |  | /vs-sonic-pi/src |
| Stop all | vs-sonic-pi |  | /vs-sonic-pi/src |
| Log / output panel | vs-sonic-pi |  | /vs-sonic-pi/src |
| Syntax highlighting | vs-sonic-pi |  | /vs-sonic-pi/src |
| Server detection | vs-sonic-pi |  | /vs-sonic-pi/src |
| Keep-alive heartbeat | vs-sonic-pi |  | /vs-sonic-pi/src |
| Configuration | vs-sonic-pi |  | /vs-sonic-pi/src |
| Run / Stop commands | vs-sonic-pi |  | /vs-sonic-pi/src |
| Examples | vs-sonic-pi |  | /vs-sonic-pi/src |
| Run selection | vs-sonic-pi |  | /vs-sonic-pi/src |
| Recording | vs-sonic-pi |  | /vs-sonic-pi/src |
| Beautify / Align | vs-sonic-pi |  | /vs-sonic-pi/src |
| Tutorial webview | vs-sonic-pi |  | /vs-sonic-pi/src |


## Requested / Backlog Features


| Title | Repo | Tags | Link |
| --- | --- | --- | --- |
| Fleet activity log (proposed) | bamr87 | fleet, observability, governance, prd |  |
| Harness pipeline map (proposed) | bamr87 | harness, console, diagrams, activity-log | /bamr87/docs/prd/HARNESS-PIPELINE-MAP.md |
| GitHub workflow nodes on the pipeline map (proposed) | bamr87 | harness, console, github, workflows | /bamr87/docs/prd/HARNESS-PIPELINE-MAP.md |
| Template gallery | cv-pro |  | /cv-pro/app/src/lib/latex-templates.ts |
| Blog posts | it-journey |  | /posts/ |
| Documentation section | it-journey |  | /docs/ |
| Jupyter notebooks | it-journey |  | /notebooks/ |
| Interactive knowledge graph explorer | law-ai |  | /law-ai/backend/law_ai/graph |
| Analysis Studio | law-ai |  | /law-ai/backend/law_ai/analysis |
| Matters workspace | law-ai |  | /law-ai/backend/law_ai/matters |
| Multi-agent collaboration and GraphRAG (Phase 2) | law-ai |  |  |
| Expansion (Phase 3) | law-ai |  |  |
| Autocomplete | vs-sonic-pi |  | /vs-sonic-pi/src |
| Hover documentation | vs-sonic-pi |  | /vs-sonic-pi/src |
| Error reporting | vs-sonic-pi |  | /vs-sonic-pi/src |
| Status bar | vs-sonic-pi |  | /vs-sonic-pi/src |
| Daemon auto-start | vs-sonic-pi |  | /vs-sonic-pi/src |
| Cue log | vs-sonic-pi |  | /vs-sonic-pi/src |
| MIDI monitor | vs-sonic-pi |  | /vs-sonic-pi/src |
| Audio scope | vs-sonic-pi |  | /vs-sonic-pi/src |
| Multi-buffer workspaces | vs-sonic-pi |  | /vs-sonic-pi/src |


---

*This index is generated automatically by `/scripts/generate_features_index.py`.


Last updated: 2026-10-28T02:13:49Z