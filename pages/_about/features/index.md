---
layout: default
title: "Features Index (Consolidated)"
description: "Automatically generated index of features across the bamr87 repositories."
permalink: /about/features/
sidebar:
  nav: about
date: 2024-12-08T14:08:06-07:00
lastmod: 2026-11-21T02:11:29Z
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
| Constitution missions | .github |  | /.github/docs/constitution.md |
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
| GitHub Projects in the console: cross-owner aggregation, linked view and guarded write-back | bamr87 | projects, console, github | /bamr87/tools/console/gh_projects.py |
| Agentic design patterns map | bamr87 | docs, agents, ai | /bamr87/docs/agentic-patterns/patterns.json |
| JEV: loop step specs — one spec per agent step, rendered the same in CI and locally | bamr87 | jev, ai, loops, specs | /bamr87/tools/jev/steps/README.md |
| JEV: run a loop's agent step locally (the loop runner) | bamr87 | jev, ai, loops, local, sandbox | /bamr87/tools/jev/loop.py |
| JEV: ratification, acceptance and completion recorded after the maintainer merges | bamr87 | governance, jev, amendments, adr | /bamr87/tools/jev/ratify.py |
| Fleet frontend platform: registry frontend: block, tiers and UPS-FE-70..73 | bamr87 | frontend, design, conformance, registry | /bamr87/tools/frontend_registry.py |
| JEV: the loop runner's context pack — the fleet's planes, read on the host for a sealed agent | bamr87 | jev, ai, loops, local, context | /bamr87/tools/jev/context.py |
| In-flight job status for agents: state, ages and slowness diagnostics | bamr87 | console, mcp, jobs, observability, agents | /bamr87/tools/console/mcp_layer/server.py |
| Fleet PR review workflow with one sticky summary | bamr87 | ci, governance, review | /bamr87/.github/workflows/pr-review.yml |
| Quest Log showcase: every deep-dived repo gets an article, two LinkedIn drafts and a better first screen | bamr87 | deep-dive, showcase, linkedin, content, routine | /bamr87/.claude/skills/deep-dive-showcase/SKILL.md |
| The editor is a front door: every harness surface from VS Code through tools/dash | bamr87 | vscode, editor, dash, debug, developer-experience | /bamr87/.vscode/launch.json |
| Workloads placed across fleet nodes, with OpenTofu for node infrastructure | bamr87 | platform, nodes, forge, opentofu, iac, docker, placement, offload, console, mcp, tui | /bamr87/tools/fleetcore/nodes.py |
| Run a loop's agent step locally from the console, the TUI and the MCP (loop-run) | bamr87 | console, tui, mcp, jev, loops, local | /loops/repo_scout |
| JEV: the fleet doctor's step spec and local dry run (P3, step 1) | bamr87 | jev, ai, loops, local, fleet-pulse | /bamr87/tools/jev/steps/fleet-pulse/doctor.yml |
| JEV: the evolution agent's step spec and local dry run (P3, step 2) | bamr87 | jev, ai, loops, local, repo-evolution | /bamr87/tools/jev/steps/repo-evolution/evolve.yml |
| JEV: the fan-out agent fill's step specs and local dry run (P3, step 3) | bamr87 | jev, ai, loops, local, fanout | /bamr87/tools/jev/steps/fanout/agent-fill-standardize.yml |
| Recursive harness refinement (Harness²): the surface check, the Propose–Probe–Compose plan and evidence tree, the experience library, the console's Refine page and review queue, the assistant | bamr87 | jev, harness, refinement, loops, sensor | /refine |
| The topic loop read back: directive → issue → pull request → merged, on the Content page | bamr87 | content, editorial, loop | /bamr87/.github/scripts/dash-gen/content_atlas.py |
| The routine PM review: project, roadmap and release alignment | bamr87 | pm, projects, roadmap, releases, loops | /bamr87/tools/pm_review.py |
| The app portal: every fleet frontend opened inside the Harness Console, at its live address or its local stack | bamr87 | console, frontend, portal, registry, launcher, cli | /apps |
| The bashOS desktop: an icon for every fleet app, each opened in a window that shares one App Shell | bamr87 | console, frontend, bashos, desktop, portal, registry | /desktop |
| The generated repo app: every repo in the fleet opens as an app, with or without a frontend of its own | bamr87 | console, frontend, portal, registry, desktop | /apps/kvlite |
| Fleet security posture from a weekly OpenSSF Scorecard sweep | bamr87 | security, conformance, loop | /bamr87/tools/scorecard_snapshot.py |
| JEV: roadmap FF ids assigned at merge | bamr87 | jev, governance, numbering, roadmap | /bamr87/tools/jev/number.py |
| The console's frame: a sidebar that folds, live counts, and pages that fail one at a time | bamr87 | console, navigation, accessibility, resilience | /bamr87/tools/console/web/src/components/Shell.tsx |
| Scoped MCP write access: approved report jobs and Work-board prioritisation for remote agents | bamr87 | console, mcp, agents, work-board, guardrails, audit | /bamr87/tools/console/mcp_layer/server.py |
| The agent inventory: every AI agent registered, graded against the efficacy contract, and held complete by the drift gate | bamr87 | harness, governance, agents, efficacy, drift | /bamr87/.github/scripts/dash-gen/agent_inventory.py |
| The incident reflector: a week of agent incidents into candidate lessons for the experience library, on a local schedule | bamr87 | jev, harness, refinement, loops, schedule | /bamr87/tools/jev/reflect.py |
| The fleet graph: what the control plane manages and how it relates, as one model | bamr87 | graph, fleetcore, harness, mcp, console, parity | /bamr87/tools/fleetcore/graph.py |
| Outcome learning (shadow): what happened to each loop's output and where its next slots would pay | bamr87 | learning, bandit, outcomes, loops, lake, fleetcore, shadow | /bamr87/tools/fleetcore/learn.py |
| The harness standard: every AI workflow found by any route, graded, with the lever that rebuilds it | bamr87 | dash, harness, standard, console | /harnesses |
| Decision index: what waits on the maintainer across the fleet, in one call | bamr87 | decisions, console, mcp, github, review-gate, ratification, dependabot, cache | /bamr87/tools/console/decision_index.py |
| Run the harness and its loops one stage at a time from Claude Code: /harness, /loops and /console slash commands over the console's operation allowlist | bamr87 | harness, loops, console, claude-code, slash-commands | /bamr87/tools/console/ops_cli.py |
| The weekly routine: Friday closes the week, Saturday checks next week's schedule can run, Sunday plans it | bamr87 | routine, backup, planning, chronicle, close-out, schedule, grok | /bamr87/tools/weekly/cli.py |
| Weekly close-out and weekend-prep loops, scheduled and maintained from the Harness Console | bamr87 | console, loops, schedule, ai-lane | /bamr87/.github/workflows/weekly-closeout.yml |
| PR queue: every open pull request, who moves it next, and bulk actions an agent carries out once Amr confirms | bamr87 | console, pull-requests, decisions, bulk-actions, fleetcore, mcp, governance | /bamr87/tools/console/web/src/pages/PrQueue.tsx |
| Fleet workflow model: every repo's workflows, linted, with check states you can trust | bamr87 | workflows, ci, lake, mcp, studio | /bamr87/tools/fleetcore/workflows.py |
| Lake recall: past local sessions by keyword | bamr87 | lake, memory, mcp, local | /bamr87/.github/scripts/dash-gen/fleet_lake.py |
| Merge readiness: what is left before a pull request merges, on the pull request and in the queue | bamr87 | pull-requests, review, ci | /bamr87/tools/fleetcore/prqueue.py |
| Telemetry query tools: prom_query, logs_search and traces_query, read-only and capped | bamr87 | console, mcp, observability, claude-code, otel, telemetry | /bamr87/tools/console/telemetry_query.py |
| The Voices editor: the fleet voice model edited in the console and filed back as a draft PR | bamr87 | console, content, voices, write-back | /bamr87/tools/console/web/src/pages/Voices.tsx |
| The docked assistant: Claude Code beside every console page, able to see the page a person has open and, in the mode they choose, use it | bamr87 | console, assistant, mcp, page-bridge, claude-code | /assist |
| The Overview tells the fleet's story: health, budget direction, what waits on the maintainer, the harness standard, flow, and one freshness timeline | bamr87 | console, overview, dataviz, trends | /overview |
| The fleet assistant baseline: any fleet page can be shared with a Claude Code session, through one page bridge with an adapter per platform | bamr87 | assistant, kit, page-bridge, mcp, claude-code, fleet | /bamr87/templates/assistant/README.md |
| Profile & résumé page | bamr87.github.io |  | /bamr87.github.io/README.md |
| Featured projects table and portfolio pages under pages/ | bamr87.github.io |  | /bamr87.github.io/pages |
| Dockerfile for local preview | bamr87.github.io |  | /bamr87.github.io/Dockerfile |
| Scripts/tools for site maintenance | bamr87.github.io |  | /bamr87.github.io/scripts |
| The Quest Log series page | bamr87.github.io |  | /bamr87.github.io/pages/quest-log.md |
| Improve-this-page feedback widget | bamr87.github.io |  | /bamr87.github.io/_config.yml |
| Paginated post index | bamr87.github.io |  | /bamr87.github.io/pages/index.html |
| Web app (bamr87.github.io/bashcrawl) | bashcrawl |  | /bashcrawl/web/index.html |
| Classic terminal dungeon | bashcrawl |  | /bashcrawl/entrance |
| XP/score persistence across modes | bashcrawl |  |  |
| Content data | bashcrawl |  | /bashcrawl/src/help/data/rooms.yaml |
| Learn courses | bashcrawl |  | /bashcrawl/courses |
| Course labs | bashcrawl |  | /bashcrawl/bin/bashcrawl |
| Skills map | bashcrawl |  | /bashcrawl/termforge/core/mastery.js |
| Spaced-repetition review | bashcrawl |  | /bashcrawl/termforge/core/mastery.js |
| Offline command explainer | bashcrawl |  | /bashcrawl/termforge/core/explain.js |
| Story mode quests and hidden rooms | bashcrawl |  | /bashcrawl/entrance |
| Hints and fog-of-war map | bashcrawl |  | /bashcrawl/web/assets/js/runtime.js |
| Practice Arcade mini-games | bashcrawl |  | /bashcrawl/web/assets/js/arcade.js |
| Vim Catacombs | bashcrawl |  | /bashcrawl/web/src/arcade/VimStage.tsx |
| Reference cheatsheets | bashcrawl |  | /bashcrawl/web/src/screens/ReferenceScreen.tsx |
| 16-bit RPG web UI | bashcrawl |  | /bashcrawl/web/src/app/App.tsx |
| Training Arena and speed run | bashcrawl |  | /bashcrawl/web/assets/js/plugins/arena.js |
| Progression: ranks, achievements, daily challenge, bestiary | bashcrawl |  | /bashcrawl/web/assets/js/plugins |
| Save and load | bashcrawl |  | /bashcrawl/web/assets/js/storage.js |
| Launcher bin/bashcrawl | bashcrawl |  | /bashcrawl/bin/bashcrawl |
| TermForge terminal framework and TTY HUD | bashcrawl |  | /bashcrawl/termforge |
| Telnet server and shared hub | bashcrawl |  | /bashcrawl/termforge/node/host-telnet.js |
| Context help | bashcrawl |  | /bashcrawl/help.sh |
| Dungeon reset | bashcrawl |  | /bashcrawl/lib/reset.sh |
| AI playtest harness | bashcrawl |  | /bashcrawl/src/playtest |
| Effects layer and chiptune SFX | bashcrawl |  | /bashcrawl/web/src/fx |
| Feedback widget | bashcrawl |  | /bashcrawl/web/src/chrome/Feedback.tsx |
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
| OS layer: bashos os install / update / uninstall | bashos |  | /bashos/os/install.sh |
| Bootable bashOS image (mkosi) | bashos |  | /bashos/os/image/build.sh |
| Console on the physical monitor | bashos |  | /bashos/os/bin/bashos-console |
| Harness Console service | bashos |  | /bashos/os/bin/bashos-harness |
| Managed OpenCode engine, always latest and verified | bashos |  | /bashos/os/install/engine.sh |
| one-os: a multiboot stick built from a manifest | bashos |  | /bashos/one-os/manifest.yaml |
| one-os: install an OS onto another drive | bashos |  | /bashos/one-os/lightos/config/includes.chroot/usr/local/bin/oneos-install |
| one-os: network boot server | bashos |  | /bashos/one-os/netboot/server.py |
| one-os: deploy SteamOS onto a desktop | bashos |  | /bashos/one-os/lightos/config/includes.chroot/usr/local/bin/oneos-steamos |
| one-os: VMs you can drive (oneos-vm) | bashos |  | /bashos/one-os/scripts/oneos-vm |
| one-os: remote sessions (oneos-remote) | bashos |  | /bashos/one-os/scripts/oneos-remote |
| amrchy: the framework under bashOS | bashos |  | /bashos/os/amrchy/sync.sh |
| bashOS on Amrchy: the OS layer on Arch | bashos |  | /bashos/os/install/console.sh |
| The bashOS ISO, its unattended seed and first boot | bashos |  | /bashos/os/iso/build.sh |
| one-os: machine profiles | bashos |  | /bashos/one-os/scripts/oneos-machine |
| CV data management | cv-pro |  | /cv-pro/app/src/components/cv |
| LaTeX template system | cv-pro |  | /cv-pro/app/src/lib/latex-templates.ts |
| AI CV parser | cv-pro |  | /cv-pro/app/src/components/cv/AIParser.tsx |
| Multi-format export | cv-pro |  | /cv-pro/app/src/components/cv/ExportSection.tsx |
| Page feedback widget | cv-pro |  | /cv-pro/app/index.html |
| Constitution missions | cv-pro |  | /cv-pro/docs/constitution.md |
| Apps: accounts, coa, company, core, journal, invoices,… | djangoerp |  | /djangoerp/djangoerp/urls.py |
| Multi-warehouse stock ledger with moving-average costing | djangoerp |  | /djangoerp/inventory/models.py |
| BOMs, work orders and an MRP planning engine | djangoerp |  | /djangoerp/mrp/engine.py |
| Async financial reports via Celery | djangoerp |  | /djangoerp/djangoerp/celery.py |
| Swagger/ReDoc API docs | djangoerp |  | /djangoerp/djangoerp/urls.py |
| Docker / docker-compose with PostgreSQL | djangoerp |  | /djangoerp/docker-compose.yml |
| Reversing entries for posted journal entries | djangoerp |  | /djangoerp/journal/services.py |
| Constitution missions | djangoerp |  | /djangoerp/docs/constitution.md |
| Landing page with setup steps, API map and feedback widget | djangoerp |  | / |
| Python package with an EDGAR User-Agent config and tests | edgar-pipeline | phase-1 | /edgar-pipeline/pyproject.toml |
| Standard CI gate | edgar-pipeline | ci | /edgar-pipeline/.github/workflows/ci.yml |
| Constitution missions | edgar-pipeline |  | /edgar-pipeline/docs/constitution.md |
| Terraform root module validates and plans with no cloud credentials | fleet-infra | phase-1 | /fleet-infra/main.tf |
| A base Helm chart lints cleanly and renders a namespace + deployment | fleet-infra | phase-1 | /fleet-infra/charts/fleet-base |
| Standard CI gate | fleet-infra | ci | /fleet-infra/.github/workflows/ci.yml |
| Shared Kotlin module with a fleet status model and JVM unit tests | fleet-mobile | phase-1 | /fleet-mobile/settings.gradle.kts |
| Gradle build of the shared module in CI | fleet-mobile | phase-1 | /fleet-mobile/.github/workflows/ci.yml |
| Standard CI gate | fleet-mobile | ci | /fleet-mobile/.github/workflows/ci.yml |
| docker compose stack (otel-collector, prometheus, grafana) | fleet-observe | phase-1 | /fleet-observe/compose.yml |
| Standard CI gate | fleet-observe | ci | /fleet-observe/.github/workflows/ci.yml |
| SEC EDGAR sync and ingest | fredgar-ai |  | /fredgar-ai/src/sec_edgar |
| Financial data warehouse | fredgar-ai |  | /fredgar-ai/src/warehouse |
| REST API v1 | fredgar-ai |  | /fredgar-ai/src/api |
| React dashboard | fredgar-ai |  | /fredgar-ai/frontend/src |
| Versioned reference data | fredgar-ai |  | /fredgar-ai/data/reference |
| Leadership narrative analyzer (optional AI) | fredgar-ai |  | /fredgar-ai/src/warehouse/services/leadership_ai.py |
| Core finance formulas and ratio metrics | fredgar-ai | metrics, ratios, valuation | /fredgar-ai/src/warehouse/services/finance_formulas.py |
| FRED transforms and vintages | fredgar-ai | macro, fred, transforms, vintages | /fredgar-ai/src/public_data/services/transforms.py |
| Company metric vs macro overlay | fredgar-ai | macro, fred, charts | /fredgar-ai/src/warehouse/services/macro_overlay.py |
| One-command install of the Claude lanes | githubai |  | /githubai/setup |
| Repo-type profiles | githubai |  | /githubai/profiles |
| Issue triage | githubai |  | /githubai/.github/workflows/claude-triage.yml |
| Implement and auto-merge lanes | githubai |  | /githubai/.github/workflows/claude-implement.yml |
| PR review, maintenance and release lanes | githubai |  | /githubai/.github/workflows/claude-review.yml |
| GitHub App relay and org policy | githubai |  | /githubai/app |
| Constitution missions | githubai |  | /githubai/docs/constitution.md |
| Drag-and-drop canvas | gitorio |  | /gitorio/app/src/canvas |
| Blueprint → Actions workflow compiler with vitest invariant tests | gitorio |  | /gitorio/app/src/compiler |
| Demo mode ?demo=1 on a fixture-backed three-repo fleet | gitorio |  | /gitorio/app/src/demo |
| Fleet Ops cockpit and telemetry views | gitorio |  | /gitorio/app/src/fleet |
| Packages absorbed under packages/ | gitorio |  | /gitorio/packages |
| Docker and VS Code task/debug workflows | gitorio |  | /gitorio/.vscode/tasks.json |
| Constitution missions | gitorio |  | /gitorio/docs/constitution.md |
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
| Quest page feedback | it-journey | feedback, quests, issues | /quests/ |
| In-memory get/put/delete API with unit tests | kvlite | phase-1 | /kvlite/src/main.rs |
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
| Page feedback: Improve this page | lifehacker.dev |  | /lifehacker.dev/_config.yml |
| Constitution missions | lifehacker.dev |  | /lifehacker.dev/docs/constitution.md |
| TCP connect probe for host:port with timeout, exposed as a CLI subcommand | netprobe | phase-1 | /netprobe/main.go |
| Standard CI gate | netprobe | ci | /netprobe/.github/workflows/ci.yml |
| CLI: scan, ingest | ocrmd |  | /ocrmd/ocrmd/cli.py |
| Local OCR: Apple Vision + RapidOCR voting (Tesseract… | ocrmd |  | /ocrmd/ocrmd/ocr.py |
| Vision-model providers: Anthropic (default) and xAI | ocrmd |  | /ocrmd/ocrmd/llm.py |
| Corpus per document | ocrmd |  | /ocrmd/ocrmd/store.py |
| Exports: md, txt, json, jsonl | ocrmd |  | /ocrmd/ocrmd/export |
| Structured-data ETL pipelines and destinations | ocrmd |  | /ocrmd/ocrmd/etl.py |
| Component identification in figures | ocrmd |  | /ocrmd/ocrmd/pipelines/components.yaml |
| Constitution missions | ocrmd |  | /ocrmd/docs/constitution.md |
| Agents: scout (env/clock), claimant-a (fast), claimant-b… | outbox |  | /outbox/agents |
| CLI: init, run, watch, score, suite, relay | outbox |  | /outbox/src/outbox/cli.py |
| Task families: stale_fact, ambiguous, deadline | outbox |  | /outbox/tasks |
| Relay to inboxes + ledger.jsonl | outbox |  | /outbox/src/outbox/mailbox.py |
| Scoring: winner, correctness, confidence inversion, retracts | outbox |  | /outbox/src/outbox/score.py |
| Belt profile: handoff messages through one gapless, crash-repairable relay | outbox |  | /outbox/src/outbox/belt.py |
| Claim desk: race a draft's claims, resolve later, calibrate | outbox |  | /outbox/src/outbox/claimdesk.py |
| Local end-to-end proof of the platform plan across the sibling repos | outbox |  | /outbox/e2e/run.py |
| Constitution missions | outbox |  | /outbox/docs/constitution.md |
| Episode catalog | ragio-ai | pipeline | /ragio-ai/ragio/catalog.py |
| Local Whisper transcription | ragio-ai | pipeline, whisper | /ragio-ai/ragio/transcribe.py |
| Segment chunking | ragio-ai | pipeline | /ragio-ai/ragio/chunk.py |
| Vector index and episode summaries | ragio-ai | pipeline, qdrant, llamaindex | /ragio-ai/ragio/index.py |
| Hybrid RAG with citations | ragio-ai | rag, ollama | /ragio-ai/ragio/rag.py |
| Audio clips | ragio-ai | audio | /ragio-ai/ragio/clips.py |
| Deep listen | ragio-ai | audio, optional | /ragio-ai/ragio/clips.py |
| Retrieval evaluation | ragio-ai | eval | /ragio-ai/ragio/evaluate.py |
| Web app | ragio-ai | fastapi, ui | /ragio-ai/app.py |
| Health, readiness and version probes | ragio-ai | fastapi, ops | /ragio-ai/app.py |
| Crawl | README |  | /README/scripts |
| Extract | README |  | /README/context |
| Navigate | README |  | /README/context |
| Synthesize | README |  | /README/context |
| Assemble | README |  | /README/context |
| Index | README |  | /README/context |
| Serve | README |  | /README/mcp |
| Evolve | README |  | /README/hooks.d |
| Published fleet documentation site | README | site, mkdocs, navigation | / |
| MCP get_doc tool | README | mcp, retrieval | /README/mcp/server.py |
| Fleet survey and docs review | README | survey, docs-review | /README/scripts/context_engine/survey.py |
| Collect | README |  | /README/scripts/context_engine/collect.py |
| Obsidian vault | README |  | /README/scripts/context_engine/vault.py |
| Second brain notes | README |  | /README/scripts/context_engine/brain.py |
| Obsidian views on the site | README | site, mkdocs, obsidian, graph | /brain/ |
| Vault reads for agents | README |  | /README/mcp/server.py |
| arcade/: React + canvas + Web Audio games | rewind-arcade |  | /rewind-arcade/arcade |
| emulate/ / retro-pi/ | rewind-arcade |  | /rewind-arcade/emulate |
| catalog/: cartridge-index (stdlib Python): dumps,… | rewind-arcade |  | /rewind-arcade/catalog |
| systems/registry.yaml + docs encyclopedia | rewind-arcade |  | /rewind-arcade/systems/registry.yaml |
| Tests that enforce the system-id map across pillars | rewind-arcade |  | /rewind-arcade/catalog/tests |
| Arcade front-end baseline: skip link, not-found pages, meta, tokens, feedback | rewind-arcade |  | /rewind-arcade/arcade/src/App.tsx |
| Generate challenges by bits or digits | rsa-challenge |  | /rsa-challenge/rsa_challenge/cli.py |
| Public challenge file with commitments | rsa-challenge |  | /rsa-challenge/challenges/challenges.json |
| Secrets kept out of git | rsa-challenge |  | /rsa-challenge/scripts/check_no_secrets.py |
| Verify submissions from the CLI | rsa-challenge |  | /rsa-challenge/rsa_challenge/challenge.py |
| Client-side verification site | rsa-challenge |  | /rsa-challenge/site/index.html |
| Seeded challenge ladder | rsa-challenge |  | /rsa-challenge/challenges/challenges.json |
| Constitution missions | rsa-challenge |  | /rsa-challenge/docs/constitution.md |
| tools/schema_lint.py | SCHEMA |  | /SCHEMA/tools/schema_lint.py |
| Federation checks across submodule seams | SCHEMA |  | /SCHEMA/tools/schema_lint.py |
| DISTRIBUTION.yml + tools/schema_dist.py | SCHEMA |  | /SCHEMA/DISTRIBUTION.yml |
| CLAUDE.md protocol snippet | SCHEMA |  | /SCHEMA/protocol |
| Seed templates and lint-green example fixture repos | SCHEMA |  | /SCHEMA/templates/SCHEMA.template.md |
| Scenario test suite | SCHEMA |  | /SCHEMA/tests/test_schema_lint.py |
| Lexer tokenizing identifiers, strings and punctuation, with spans and errors | schema-lang | phase-1 | /schema-lang/Cargo.toml |
| CLI that reads a .schema file and prints tokens | schema-lang | phase-1 | /schema-lang/src/main.rs |
| Standard CI gate | schema-lang | ci | /schema-lang/.github/workflows/ci.yml |
| Constitution missions | schema-lang |  | /schema-lang/docs/constitution.md |
| Project initialization wizard | scripts | scaffolding | /scripts/project-init.sh |
| ForkMe repository forking/cloning | scripts | github | /scripts/FORKME/forkme.sh |
| StashMe multi-repo cloud stash | scripts | multi-repo, backup | /scripts/STASHME/stashme.sh |
| Git + GitHub repository creator | scripts | github, scaffolding | /scripts/git_init.sh |
| Safe directory rename | scripts | filesystem | /scripts/rename-directory.sh |
| Python package bootstrap | scripts | scaffolding, python | /scripts/create_package.sh |
| Markdown prose unwrapper | scripts | docs, lint | /scripts/tools/unwrap-prose.py |
| install.sh standalone installer | scripts |  | /scripts/install.sh |
| install.sh --uninstall | scripts | install | /scripts/install.sh |
| Shell completions for the toolbelt | scripts | dx, completions | /scripts/completions/ |
| Minimal app binds to 127.0.0.1 only and serves a health route, with te | sec-lab | phase-1 | /sec-lab/pyproject.toml |
| Standard CI gate | sec-lab | ci | /sec-lab/.github/workflows/ci.yml |
| Constitution missions | sec-lab |  | /sec-lab/docs/constitution.md |


## Requested / Backlog Features


| Title | Repo | Tags | Link |
| --- | --- | --- | --- |
| detect-stack resolved at the caller's pinned ref | .github |  | /.github/.github/workflows/publish.yml |
| Reusable PyPI build with caller-side trusted publishing | .github |  | /.github/.github/workflows/publish.yml |
| Reusable-workflow self-test with publish dry-run | .github |  | /.github/.github/workflows/publish.yml |
| Fleet activity log (proposed) | bamr87 | fleet, observability, governance, prd |  |
| Harness pipeline map (proposed) | bamr87 | harness, console, diagrams, activity-log | /bamr87/docs/prd/HARNESS-PIPELINE-MAP.md |
| GitHub workflow nodes on the pipeline map (proposed) | bamr87 | harness, console, github, workflows | /bamr87/docs/prd/HARNESS-PIPELINE-MAP.md |
| Fleet work-tracking framework on GitHub Projects (proposed) | bamr87 | governance, projects, labels, fleet | /bamr87/templates/projects/framework.yml |
| Projects coverage gate: every open issue/PR tracked with required fields (proposed) | bamr87 | governance, lint, projects | /bamr87/tools/projects_lint.py |
| Features/PRD ↔ project sync and console Projects panel (proposed) | bamr87 | governance, projects, console, mcp |  |
| Docs site conformance: site exists, index complete, links resolve | bamr87 | governance, docs, conformance | /bamr87/tools/conformance.py |
| Public docs site: every fleet repo publishes all its documentation | bamr87 | governance, docs, pages | /bamr87/docs/constitution.md |
| Architecture research harness: literature-grounded fleet architecture review and research papers | bamr87 | harness, architecture, research |  |
| Review gate: needs-amr label holds a PR from agent merge | bamr87 | governance, merge | /bamr87/docs/constitution.md |
| Evidence conformance: checks major/frontend PRs for tests, visuals and review | bamr87 | governance, verification, conformance | /bamr87/tools/conformance.py |
| Major-change evidence: JEV-judged major PRs, tests, visual before/after, JEV + QA Lead review | bamr87 | governance, verification, review | /bamr87/docs/constitution.md |
| Eval baseline: per-role eval sets, pinned models, run tracing | bamr87 | governance, ai, evals | /bamr87/docs/constitution.md |
| Risk tiers: reversible/external/money tags gate agent actions | bamr87 | governance, ai, safety | /bamr87/docs/constitution.md |
| AI-ready foundation: API layer, MCP, agent docs and metadata in every repo | bamr87 | governance, ai, mcp, api | /bamr87/docs/constitution.md |
| AIEO AI-readiness check: scores every repo's AI foundation | bamr87 | governance, ai, conformance, aieo | /bamr87/tools/aieo/ |
| Backstage catalog-info.yaml export of the registry | bamr87 | registry, catalog, interop | /bamr87/.github/scripts/dash-gen |
| Fan-out campaigns page: per-repo PR, CI and merge state per kit rollout | bamr87 | fanout, console, campaigns | /bamr87/tools/fanout.sh |
| Tag selectors for --target | bamr87 | fanout, cli, selectors | /bamr87/tools/fanout.sh |
| Copier-style 3-way kit upgrade for hand-edited files | bamr87 | fanout, kits, upgrade | /bamr87/tools/fanout.sh |
| Governance records lint: amendment status, constitution order, doc links | bamr87 | governance, lint | /bamr87/tools/governance_lint.py |
| Centrally managed loop kill switches | bamr87 | loops, kill-switch, console, governance | /bamr87/_data/fleet.yml |
| Fleet activity replay: live and historical animated view of agents, harnesses and containers (proposed) | bamr87 | console, otel, phoenix, epic, observability, activity-log, replay, timeline, docker, storage, visualization | /bamr87/docs/prd/FLEET-ACTIVITY-REPLAY.md |
| Common harness protocol and platform: one agent-loop contract for console, CI, local and JEV harnesses (proposed) | bamr87 | harness, protocol, agent-loop, mcp, otel, phoenix, a2a, uhp, jev, epic | /bamr87/docs/prd/HARNESS-PROTOCOL.md |
| Visual evidence standard: screenshots and front-end evidence for tutorials, guides and setup docs | bamr87 | docs, guides, evidence, console, lint, standards | /bamr87/tools/guides_visual_lint.py |
| Fleet activity replay: live and historical animated view of agents, harnesses and containers (proposed) | bamr87 | console, observability, activity-log, replay, timeline, docker, storage, visualization | /bamr87/docs/prd/FLEET-ACTIVITY-REPLAY.md |
| Expedite sprints: one accelerated, monitored pilot at a time run by the fleet's agentic loops | bamr87 | harness, loops, governance, devops, dora, standards | /bamr87/docs/EXPEDITE-SPRINTS.md |
| Expedite sprints: one accelerated, monitored pilot at a time run by the fleet's agentic loops | bamr87 | harness, loops, governance, devops, dora, standards | /bamr87/docs/EXPEDITE-SPRINTS.md |
| Typed decisions gate the pipeline: a decision lockfile, traces and replay, the trim and verify loops | bamr87 | ci, jev, decisions, optimization, governance | /bamr87/docs/prd/AGENTIC-SDLC.md |
| MCP server lifecycle: centralized registry, config schema, lint and fan-out | bamr87 | mcp, agents, ai-layer, standards, lint, console | /bamr87/tools/mcp_servers_lint.py |
| Grok ↔ Claude Code governance: handoff, audit trail, roles, escalation | bamr87 | governance, agents, claude-code, grok, traceability, lint | /bamr87/tools/governance_trace_lint.py |
| Claude Code executes; Grok bots set direction only | bamr87 | governance, agents, claude-code, grok, standards, lint | /bamr87/tools/claude_code_executes_lint.py |
| Shared functional specification library | bamr87 | specs, library, governance, prd | /bamr87/docs/prd/FUNCTIONAL-SPEC-LIBRARY.md |
| Per-repo functional spec manifest | bamr87 | specs, manifest, governance | /bamr87/docs/prd/FUNCTIONAL-SPEC-LIBRARY.md |
| Functional spec override ratification | bamr87 | specs, governance, amendments | /bamr87/docs/prd/FUNCTIONAL-SPEC-LIBRARY.md |
| Functional spec resolver, CI gate and docs parity | bamr87 | specs, ci, docs, resolver | /bamr87/docs/prd/FUNCTIONAL-SPEC-LIBRARY.md |
| Agentic loops history and statistics | bamr87 | dashboard, agents, loops, statistics, history | /bamr87/docs/prd/AGENTIC-LOOPS-DASHBOARD.md |
| Agentic loops dashboard | bamr87 | dashboard, agents, loops, harness, observability | /bamr87/docs/prd/AGENTIC-LOOPS-DASHBOARD.md |
| Agentic loops dashboard as the Bash 365 foundation | bamr87 | dashboard, bash-365, showcase, agents, wizard | /bamr87/docs/prd/AGENTIC-LOOPS-DASHBOARD.md |
| Automatic credential rotation: started by a secret-scanning alert, a schedule or a failing credential, for the credentials the weekly loop does not reach | bamr87 | security, tokens, rotation, secrets, secret-scanning, backlog | /bamr87/docs/prd/CREDENTIAL-ROTATION.md |
| Red-main resolver: every red default branch found, resolved where fleet rules allow, and handed over where they do not (proposed) | bamr87 | loops, harness, ci, merge, review-gate | /bamr87/docs/prd/RED-MAIN-RESOLVER.md |
| CI review loop: each failed run on a red default branch traced through its workflow, judged for selectivity, and answered with a minimal diff (proposed) | bamr87 | loops, harness, ci, workflows, review | /bamr87/docs/prd/RED-MAIN-RESOLVER.md |
| Agent news feed reactions | bamr87 | feed, agents, github, discussions | /bamr87/docs/prd/AGENT-NEWS-FEED.md |
| Agent news feed threads | bamr87 | feed, agents, github, discussions | /bamr87/docs/prd/AGENT-NEWS-FEED.md |
| Agent news feed | bamr87 | feed, agents, github, discussions | /bamr87/docs/prd/AGENT-NEWS-FEED.md |
| On-premise compute node: local LLMs and Claude Code sessions on Amr's own machine (planned) | bamr87 | platform, nodes, local-llm, claude-code, weekly, housekeeping, cost | /bamr87/docs/ONPREM-COMPUTE.md |
| Repository about section: a consistent public site map in every repo | bamr87 | governance, docs, readme, portfolio, standards | /bamr87/docs/ABOUT-SECTION.md |
| Fleet-wide mission statements: one direction and three missions in constitution § 1 | bamr87 | governance, mission, constitution, standards | /bamr87/docs/constitution.md |
| Missions in constitution §1 | bamr87.github.io |  |  |
| Missions in constitution §1 | bashcrawl |  |  |
| one-os: bashOS and Amrchy as bootable systems | bashos |  | /bashos/one-os/docs/epics/0001-bashos-and-amrchy.md |
| Missions in constitution §1 | bashos |  |  |
| Template gallery | cv-pro |  | /cv-pro/app/src/lib/latex-templates.ts |
| Fiscal periods, lock dates and period-close entry | djangoerp |  | /djangoerp/journal/models.py |
| Fetch company submissions JSON with rate limiting (10 req/s cap) | edgar-pipeline | phase-1 |  |
| Dagster assets for raw submissions and company facts | edgar-pipeline | phase-2 |  |
| dbt project on DuckDB with staging and mart models | edgar-pipeline | phase-2 |  |
| MLflow-tracked baseline model on filing features | edgar-pipeline | phase-3 |  |
| Export marts consumed by fredgar-ai and law-ai | edgar-pipeline | phase-3 |  |
| k3s cluster provisioning module for a local VM (multipass/libvirt) | fleet-infra | phase-2 |  |
| GitOps controller bootstrap that reconciles charts/ from main | fleet-infra | phase-2 |  |
| Per-service Helm charts for fleet apps (ragio-ai, fredgar-ai) | fleet-infra | phase-3 |  |
| Secrets management via SOPS/age, never plaintext in git | fleet-infra | phase-3 |  |
| Missions in constitution §1 | fleet-infra |  |  |
| Ktor client fetching hub fleet data | fleet-mobile | phase-2 |  |
| Android app shell with a repo status list | fleet-mobile | phase-2 |  |
| iOS target and Compose Multiplatform UI | fleet-mobile | phase-3 |  |
| Notifications for failing CI and review requests | fleet-mobile | phase-3 |  |
| Missions in constitution §1 | fleet-mobile |  |  |
| Prometheus scrapes the collector's own metrics | fleet-observe | phase-1 |  |
| Grafana datasource and a fleet overview dashboard provisioned from fil | fleet-observe | phase-2 |  |
| OTLP instrumentation guide and example for a fleet service | fleet-observe | phase-2 |  |
| Alerting rules for service availability | fleet-observe | phase-3 |  |
| Helm deployment onto fleet-infra | fleet-observe | phase-3 |  |
| Missions in constitution §1 | fleet-observe |  |  |
| Core product roadmap | fredgar-ai |  |  |
| Advanced / growth features | fredgar-ai |  |  |
| Institutional holdings (13F) | fredgar-ai |  |  |
| Watchlist and new-filing alerts | fredgar-ai |  |  |
| Harness Studio live map (Observe over fleetgraph/v1) | gitorio |  | /gitorio/app/src/map |
| Design fragments from the blueprint editor | gitorio |  | /gitorio/app/src/canvas |
| Manage via confirm-gated hub console ops | gitorio |  | /gitorio/app/src/fleet |
| Console embed of the live map | gitorio |  | /gitorio/app/src/state |
| JEV numbering and main-only generated files | gitorio |  | /gitorio/features |
| Engine/API layer over fleetgraph/v1 | gitorio |  | /gitorio/app/src |
| Plugin SDK: node types, engine adapters, config-driven behavior | gitorio |  | /gitorio/app/src/machines |
| Community release 1.0 | gitorio |  | /gitorio/release-please-config.json |
| PerfectPixel Studio sprite-sheet import | godotgo |  | /godotgo/framework/addons |
| Missions in constitution §1 | godotgo |  |  |
| Blog posts | it-journey |  | /posts/ |
| Documentation section | it-journey |  | /docs/ |
| Jupyter notebooks | it-journey |  | /notebooks/ |
| Quest editorial charter | it-journey | governance, editorial, quests |  |
| Editorial charter CI checks | it-journey | governance, ci, quests |  |
| Missions in constitution §1 | it-journey |  |  |
| Write-ahead log with crash recovery | kvlite | phase-1 |  |
| SSTable flush and point lookups across levels | kvlite | phase-2 |  |
| Background compaction and bloom filters | kvlite | phase-2 |  |
| Raft leader election and log replication | kvlite | phase-3 |  |
| Network API (gRPC) and a CLI client | kvlite | phase-3 |  |
| Missions in constitution §1 | kvlite |  |  |
| Interactive knowledge graph explorer | law-ai |  | /law-ai/backend/law_ai/graph |
| Analysis Studio | law-ai |  | /law-ai/backend/law_ai/analysis |
| Matters workspace | law-ai |  | /law-ai/backend/law_ai/matters |
| Multi-agent collaboration and GraphRAG (Phase 2) | law-ai |  |  |
| Expansion (Phase 3) | law-ai |  |  |
| Global norm taxonomy and ontology | law-ai |  |  |
| Open legal corpus adoption plan | law-ai |  |  |
| AI governance register | law-ai |  |  |
| Obligation and control crosswalk | law-ai |  |  |
| Bounded rules-as-code pilots | law-ai |  |  |
| Temporal validity and horizon scanning | law-ai |  |  |
| Governance-as-code fleet worked example | law-ai |  |  |
| LSAT Section (exam) mode | law-ai |  |  |
| LSAT performance by question type | law-ai |  |  |
| External citation verification | law-ai |  |  |
| GraphRAG retrieval benchmark | law-ai |  |  |
| lawmode legal-risk review for code (folded in) | law-ai |  | /law-ai/backend/law_ai/lawmode |
| Hub-originated publishing in character voice | lifehacker.dev |  | /lifehacker.dev/_data/hub_intake.yml |
| Concurrent port range scan with rate limiting | netprobe | phase-1 |  |
| DNS lookup subcommand (A/AAAA/MX/TXT) | netprobe | phase-2 |  |
| Traceroute view | netprobe | phase-2 |  |
| Bubble Tea TUI dashboard combining probes | netprobe | phase-3 |  |
| JSON output for scripting | netprobe | phase-3 |  |
| Missions in constitution §1 | netprobe |  |  |
| On-machine vision pass (local VLM cross-check) | ocrmd |  | /ocrmd/ocrmd/llm.py |
| Structure-aware digital-PDF path | ocrmd |  | /ocrmd/ocrmd/pdfsrc.py |
| Table-structure reconstruction for camera scans | ocrmd |  | /ocrmd/ocrmd/ocr.py |
| index the full archive and reach eval hit@5 ≥ 0.85 on eval/questions.j | ragio-ai | roadmap, phase-1 |  |
| route questions to candidate episodes via the summary collection befor | ragio-ai | roadmap, phase-2 |  |
| GPU deep-listen mode re-transcribing cited ranges with a larger Whispe | ragio-ai | roadmap, phase-3 |  |
| creative modes and an episode/people/themes knowledge graph | ragio-ai | roadmap, phase-4 |  |
| speaker diarization attached to transcript segments | ragio-ai | roadmap, phase-5 |  |
| Export pipeline metrics and traces over OTLP to bamr87/fleet-observe | ragio-ai | roadmap, phase-5 |  |
| Missions in constitution §1 | ragio-ai |  |  |
| MCP provenance and trust markers | README | mcp, security, provenance | /README/mcp/server.py |
| Missions in constitution §1 | README |  |  |
| Neutral schemas and the single monthly number | recon-engine | build-step-1, core |  |
| Six-bucket decomposition, gross not net, with transfer logging | recon-engine | build-step-2, core |  |
| Django ERP adapter and a minimal period view | recon-engine | build-step-3, adapter |  |
| Learned expectation: one regression per GL account | recon-engine | build-step-4, statistical-layer |  |
| Anomaly detection on standardized residuals | recon-engine | build-step-5, statistical-layer |  |
| File and API adapters for standalone use | recon-engine | build-step-6, adapter |  |
| Missions in constitution §1 | recon-engine |  |  |
| Missions in constitution §1 | rewind-arcade |  |  |
| Missions in constitution §1 | SCHEMA |  |  |
| schema_lint check --json | SCHEMA |  | /SCHEMA/tools/schema_lint.py |
| AGENTS.md protocol snippet | SCHEMA |  | /SCHEMA/protocol |
| Recursive-descent parser producing an AST | schema-lang | phase-2 |  |
| Semantic checks with span-based diagnostics | schema-lang | phase-2 |  |
| Emit SCHEMA.md contracts and gitorio blueprints | schema-lang | phase-3 |  |
| Language server (LSP) for editors | schema-lang | phase-3 |  |
| Missions in constitution §1 | scripts |  |  |
| Safety guard: refuses to start on a non-loopback bind without an expli | sec-lab | phase-1 |  |
| First challenge set: SQL injection and XSS with flags | sec-lab | phase-2 |  |
| SAST workflow (Semgrep + Bandit) publishing SARIF | sec-lab | phase-2 |  |
| DAST baseline scan with OWASP ZAP in CI against a container | sec-lab | phase-3 |  |
| Fix write-ups linked per challenge | sec-lab | phase-3 |  |


---

*This index is generated automatically by `/scripts/generate_features_index.py`.


Last updated: 2026-11-21T02:11:29Z