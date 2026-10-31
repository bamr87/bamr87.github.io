---
layout: default
title: "Features Index (Consolidated)"
description: "Automatically generated index of features across the bamr87 repositories."
permalink: /about/features/
sidebar:
  nav: about
date: 2024-12-08T14:08:06-07:00
lastmod: 2026-10-31T02:11:38Z
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
| Work board: rebalance the loops' work by drag and drop | bamr87 | console, issue-pipeline, roadmap, spec-driven, prioritisation | /work |
| Daily repo deep dive: one repo a day, every repo once per cycle | bamr87 | deep-dive, routine, console, dashboard, automation | /deep-dive |
| Real-time bot activity dashboard | bamr87 | console, dashboard, live, sse, observability | /live |
| Harness Console MCP layer: the console's API for any AI agent | bamr87 | console, mcp, agents, ai-layer, integration | /bamr87/tools/console/mcp_layer/server.py |
| Claude spend accounting: every CI run priced, estimated or proved free | bamr87 | ai, cost, budget, ledger, transparency, dashboard | /bamr87/.github/scripts/dash-gen/ai_usage_collector.py |
| The fleet's one release-please workflow, degrading to a warning without a PR credential | bamr87 | release, loop, workflows, kits | /bamr87/.github/workflows/release-please.yml |
| Workflow atlas: maintain and design the hub's GitHub Actions | bamr87 | console, workflows, ci, standards, lint, mcp | /workflows |
| JEV: conflict-free numbering + tiered PR conflict triage | bamr87 | jev, governance, numbering, conflicts, ai, cost, automation | /bamr87/tools/jev/README.md |
| Claude Code OTel telemetry in the console and MCP | bamr87 | console, observability, claude-code, otel, mcp | /bamr87/tools/console/claude_telemetry.py |
| Claude subscription shown as a discounted rate off API list prices | bamr87 | console, cost, claude, observability | /bamr87/tools/console/subscription.py |
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
| Python package with an EDGAR User-Agent config and tests | edgar-pipeline | phase-1 | /edgar-pipeline/pyproject.toml |
| Standard CI gate | edgar-pipeline | ci | /edgar-pipeline/.github/workflows/ci.yml |
| Terraform root module validates and plans with no cloud credentials (l | fleet-infra | phase-1 | /fleet-infra/main.tf |
| Standard CI gate | fleet-infra | ci | /fleet-infra/.github/workflows/ci.yml |
| Shared Kotlin module with a fleet status model and unit tests (JVM tar | fleet-mobile | phase-1 | /fleet-mobile/settings.gradle.kts |
| Standard CI gate | fleet-mobile | ci | /fleet-mobile/.github/workflows/ci.yml |
| docker compose stack (otel-collector, prometheus, grafana) validates a | fleet-observe | phase-1 | /fleet-observe/compose.yml |
| Standard CI gate | fleet-observe | ci | /fleet-observe/.github/workflows/ci.yml |
| SEC EDGAR sync and ingest | fredgar-ai |  | /fredgar-ai/src/sec_edgar |
| Financial data warehouse | fredgar-ai |  | /fredgar-ai/src/warehouse |
| REST API v1 | fredgar-ai |  | /fredgar-ai/src/api |
| React dashboard | fredgar-ai |  | /fredgar-ai/frontend/src |
| Versioned reference data | fredgar-ai |  | /fredgar-ai/data/reference |
| Leadership narrative analyzer (optional AI) | fredgar-ai |  | /fredgar-ai/src/warehouse/services/leadership_ai.py |
| Core finance formulas and ratio metrics | fredgar-ai | metrics, ratios, valuation | /fredgar-ai/src/warehouse/services/finance_formulas.py |
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
| Quest Atom feed | it-journey | feed, atom, quests | /quests/feed.xml |
| In-memory get/put/delete API with unit tests | kvlite | phase-1 | /kvlite/Cargo.toml |
| Standard CI gate | kvlite | ci | /kvlite/.github/workflows/ci.yml |
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
| TCP connect probe for host:port with timeout, exposed as a CLI subcomm | netprobe | phase-1 | /netprobe/go.mod |
| Standard CI gate | netprobe | ci | /netprobe/.github/workflows/ci.yml |
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


## Requested / Backlog Features


| Title | Repo | Tags | Link |
| --- | --- | --- | --- |
| Fleet activity log (proposed) | bamr87 | fleet, observability, governance, prd |  |
| Harness pipeline map (proposed) | bamr87 | harness, console, diagrams, activity-log | /bamr87/docs/prd/HARNESS-PIPELINE-MAP.md |
| GitHub workflow nodes on the pipeline map (proposed) | bamr87 | harness, console, github, workflows | /bamr87/docs/prd/HARNESS-PIPELINE-MAP.md |
| Fleet work-tracking framework on GitHub Projects (proposed) | bamr87 | governance, projects, labels, fleet | /bamr87/templates/projects/framework.yml |
| Projects coverage gate: every open issue/PR tracked with required fields (proposed) | bamr87 | governance, lint, projects | /bamr87/tools/projects_lint.py |
| Features/PRD ↔ project sync and console Projects panel (proposed) | bamr87 | governance, projects, console, mcp |  |
| GitHub Projects in the console: cross-owner aggregation, linked view and guarded write-back | bamr87 | projects, console, github | /bamr87/tools/console/gh_projects.py |
| Template gallery | cv-pro |  | /cv-pro/app/src/lib/latex-templates.ts |
| Fetch company submissions JSON with rate limiting (10 req/s cap) | edgar-pipeline | phase-1 |  |
| Dagster assets for raw submissions and company facts | edgar-pipeline | phase-2 |  |
| dbt project on DuckDB with staging and mart models | edgar-pipeline | phase-2 |  |
| MLflow-tracked baseline model on filing features | edgar-pipeline | phase-3 |  |
| Export marts consumed by fredgar-ai and law-ai | edgar-pipeline | phase-3 |  |
| A base Helm chart lints cleanly and renders a namespace + deployment | fleet-infra | phase-1 |  |
| k3s cluster provisioning module for a local VM (multipass/libvirt) | fleet-infra | phase-2 |  |
| GitOps controller bootstrap that reconciles charts/ from main | fleet-infra | phase-2 |  |
| Per-service Helm charts for fleet apps (ragio-ai, fredgar-ai) | fleet-infra | phase-3 |  |
| Secrets management via SOPS/age, never plaintext in git | fleet-infra | phase-3 |  |
| Gradle build of the shared module in CI | fleet-mobile | phase-1 |  |
| Ktor client fetching hub fleet data | fleet-mobile | phase-2 |  |
| Android app shell with a repo status list | fleet-mobile | phase-2 |  |
| iOS target and Compose Multiplatform UI | fleet-mobile | phase-3 |  |
| Notifications for failing CI and review requests | fleet-mobile | phase-3 |  |
| Prometheus scrapes the collector's own metrics | fleet-observe | phase-1 |  |
| Grafana datasource and a fleet overview dashboard provisioned from fil | fleet-observe | phase-2 |  |
| OTLP instrumentation guide and example for a fleet service | fleet-observe | phase-2 |  |
| Alerting rules for service availability | fleet-observe | phase-3 |  |
| Helm deployment onto fleet-infra | fleet-observe | phase-3 |  |
| Core product roadmap | fredgar-ai |  |  |
| Advanced / growth features | fredgar-ai |  |  |
| PerfectPixel Studio sprite-sheet import | godotgo |  | /godotgo/framework/addons |
| Blog posts | it-journey |  | /posts/ |
| Documentation section | it-journey |  | /docs/ |
| Jupyter notebooks | it-journey |  | /notebooks/ |
| Write-ahead log with crash recovery | kvlite | phase-1 |  |
| SSTable flush and point lookups across levels | kvlite | phase-2 |  |
| Background compaction and bloom filters | kvlite | phase-2 |  |
| Raft leader election and log replication | kvlite | phase-3 |  |
| Network API (gRPC) and a CLI client | kvlite | phase-3 |  |
| Interactive knowledge graph explorer | law-ai |  | /law-ai/backend/law_ai/graph |
| Analysis Studio | law-ai |  | /law-ai/backend/law_ai/analysis |
| Matters workspace | law-ai |  | /law-ai/backend/law_ai/matters |
| Multi-agent collaboration and GraphRAG (Phase 2) | law-ai |  |  |
| Expansion (Phase 3) | law-ai |  |  |
| Concurrent port range scan with rate limiting | netprobe | phase-1 |  |
| DNS lookup subcommand (A/AAAA/MX/TXT) | netprobe | phase-2 |  |
| Traceroute view | netprobe | phase-2 |  |
| Bubble Tea TUI dashboard combining probes | netprobe | phase-3 |  |
| JSON output for scripting | netprobe | phase-3 |  |


---

*This index is generated automatically by `/scripts/generate_features_index.py`.


Last updated: 2026-10-31T02:11:38Z