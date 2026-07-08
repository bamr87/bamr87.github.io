---
layout: default
title: "Features Index (Consolidated)"
description: "Automatically generated index of features across the bamr87 repositories."
permalink: /about/features/
sidebar:
  nav: about
lastmod: 2026-07-08T03:08:18Z
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
| Bootstrap 5.3.3 Theme Integration | zer0-mistakes | jekyll, theme, bootstrap, ui, responsive | / |
| Docker-First Development Environment | zer0-mistakes | docker, devops, development, cross-platform | / |
| Modular AI-Powered Installer | zer0-mistakes | ai, automation, installation, error-handling, bash, installer | / |
| AI Preview Image Generator | zer0-mistakes | ai, images, automation, openai, content | /docs/features/preview-image-generator/ |
| AI Agent Integration (Copilot + AGENTS.md) | zer0-mistakes | ai, copilot, agents, development, documentation | https://github.com/bamr87/zer0-mistakes/blob/main/AGENTS.md |
| PostHog Privacy-First Analytics | zer0-mistakes | analytics, privacy, gdpr, ccpa, posthog | / |
| Cookie Consent Management | zer0-mistakes | privacy, gdpr, ccpa, cookies, consent | / |
| Enhanced Sidebar Navigation System | zer0-mistakes | navigation, ui, accessibility, performance, sidebar | / |
| Keyboard Navigation System | zer0-mistakes | accessibility, keyboard, navigation, ux | / |
| Mobile TOC Floating Action Button | zer0-mistakes | mobile, navigation, ui, toc, fab | / |
| Skip-to-Content Accessibility Link | zer0-mistakes | accessibility, wcag, navigation, a11y | / |
| Jupyter Notebook Integration | zer0-mistakes | jupyter, notebooks, python, data-science, content | / |
| Mermaid Diagram Support | zer0-mistakes | mermaid, diagrams, visualization, documentation | / |
| Jekyll Collections System | zer0-mistakes | jekyll, collections, content, organization | / |
| Automated Release Management | zer0-mistakes | release, automation, semver, ci-cd, versioning | / |
| Comprehensive Testing Suite | zer0-mistakes | testing, quality, ci-cd, automation | / |
| CodeQL Security Scanning | zer0-mistakes | security, codeql, scanning, ci-cd | / |
| Comprehensive Layout System | zer0-mistakes | layouts, templates, jekyll, bootstrap | / |
| Modular Include Components | zer0-mistakes | includes, components, modular, jekyll | / |
| Theme Version Display Plugin | zer0-mistakes | plugin, version, jekyll, metadata | / |
| Privacy Policy Page | zer0-mistakes | legal, privacy, gdpr, ccpa, compliance | /privacy-policy/ |
| Terms of Service Page | zer0-mistakes | legal, terms, compliance | /terms-of-service/ |
| Product Requirements Document (PRD) | zer0-mistakes | documentation, prd, product, planning | / |
| Dual Documentation Architecture | zer0-mistakes | documentation, mdx, markdown, workflow | / |
| Automated Dependency Updates | zer0-mistakes | automation, dependencies, github-actions, maintenance | / |
| Continuous Integration (CI) Workflow | zer0-mistakes | ci-cd, testing, automation, github-actions | / |
| Shell Script Automation Library | zer0-mistakes | scripts, automation, bash, utilities | / |
| Back to Top Button | zer0-mistakes | ui, navigation, scroll, accessibility | / |
| Code Copy Button | zer0-mistakes | ui, code, clipboard, developer-experience | / |
| Dark/Light Mode Toggle | zer0-mistakes | ui, theme, dark-mode, accessibility | / |
| GitHub Pages-Compatible Live Search | zer0-mistakes | search, navigation, modal, keyboard | / |
| Auto-hide Navigation | zer0-mistakes | ui, navigation, scroll, mobile | / |
| Particles Background | zer0-mistakes | ui, animation, visual, landing | / |
| Giscus Comments | zer0-mistakes | comments, github, discussions, engagement, claude-code | / |
| MathJax Math Rendering | zer0-mistakes | math, latex, equations, documentation | / |
| Table of Contents | zer0-mistakes | navigation, toc, headings, documentation | / |
| Google Analytics | zer0-mistakes | analytics, google, tracking, metrics | / |
| Google Tag Manager | zer0-mistakes | analytics, gtm, tracking, marketing | / |
| Breadcrumbs Navigation | zer0-mistakes | navigation, breadcrumbs, seo, accessibility | / |
| SEO Optimization | zer0-mistakes | seo, meta, opengraph, twitter-cards | / |
| Sitemap Generation | zer0-mistakes | seo, sitemap, search, indexing | / |
| Statistics Dashboard | zer0-mistakes | dashboard, statistics, metrics, visualization | / |
| Obsidian Vault Integration | zer0-mistakes | obsidian, content, wiki-links, knowledge-base, jekyll | /docs/obsidian/ |
| Obsidian Local Graph Panel | zer0-mistakes | obsidian, graph, visualization, navigation | /docs/obsidian/graph/ |
| Bare-Minimum Remote-Theme Starter | zer0-mistakes | setup, quickstart, remote-theme, github-pages | / |
| Site Configuration Detection & Smart 404 | zer0-mistakes | setup, 404, configuration, ux | /404.html |
| Config-Driven Frontmatter Validation | zer0-mistakes | validation, frontmatter, content, ci-cd, automation | / |
| Dynamic Collection-Based Navigation Fallback | zer0-mistakes | navigation, ui, zero-config, jekyll | / |
| Admin Layout & Configuration Dashboards | zer0-mistakes | admin, dashboard, ui, configuration | /admin/ |
| AGENTS.md Cross-Tool Agent Entry Point | zer0-mistakes | ai, agents, documentation, copilot, cursor | https://github.com/bamr87/zer0-mistakes/blob/main/AGENTS.md |
| Data-Driven Roadmap with Auto-Generated Diagram | zer0-mistakes | roadmap, documentation, mermaid, automation | /roadmap/ |
| Vendored Bootstrap & Icon Assets | zer0-mistakes | bootstrap, assets, vendor, github-pages, performance | / |
| AIEO Structured Data, FAQ & Glossary | zer0-mistakes | seo, aieo, structured-data, faq, glossary, ai | /glossary/ |
| ES6 Modular Navigation Architecture | zer0-mistakes | navigation, javascript, es6, ui, performance | / |
| DevContainer Configuration | zer0-mistakes | devcontainer, codespaces, development, docker | / |
| Notes Collection & Notebook Layout | zer0-mistakes | content, collections, notes, jekyll | /notes/ |
| Performance: Page-URL Cache for Obsidian Resolver | zer0-mistakes | obsidian, performance, jekyll, optimization | /docs/obsidian/performance/ |
| AI Chat Assistant (Claude + GitHub) | zer0-mistakes | ai, chatbot, claude, github, proxy, accessibility | /docs/features/ai-chat-assistant/ |
| Author Profiles System | zer0-mistakes | content, authors, profiles, jekyll | /authors/ |
| News Homepage Layout | zer0-mistakes | layouts, news, homepage, content | / |
| Section Layout | zer0-mistakes | layouts, navigation, content | / |
| Article Layout & Post Types | zer0-mistakes | layouts, content, posts | / |
| Theme Skins & Background Customizer | zer0-mistakes | ui, theme, skins, customization | / |
| Nanobar Progress Bar | zer0-mistakes | ui, performance, loading | / |
| Setup Wizard | zer0-mistakes | setup, onboarding, configuration | /setup/ |
| Table CSV Copy | zer0-mistakes | ui, content, clipboard, developer-experience | / |
| Social Share Actions | zer0-mistakes | ui, social, content, engagement | / |
| Monthly Archives Page | zer0-mistakes | content, navigation, archive | /archives/ |
| Live Component Showcase | zer0-mistakes | ui, documentation, components, bootstrap | / |
| AI Content Review Workflow | zer0-mistakes | ci-cd, ai, content, automation | / |
| Giscus Digest Workflow | zer0-mistakes | ci-cd, comments, community, automation | / |
| Visual Evidence Gate | zer0-mistakes | ci-cd, testing, quality, automation | / |
| Autonomous Issue & CI Pipeline | zer0-mistakes | ci-cd, automation, ai, issues | / |
| Secret Scanning Workflow | zer0-mistakes | ci-cd, security, automation | / |
| Unified Settings Panel | zer0-mistakes | ui, navigation, bootstrap, accessibility | / |


## Requested / Backlog Features


| Title | Repo | Tags | Link |
| --- | --- | --- | --- |
| Automated Version Bump Workflow | zer0-mistakes | github-actions, automation, versioning, ci-cd | / |
| Local Docker Publishing Pipeline | zer0-mistakes | docker, release, ci-cd, gem, automation | / |


---

*This index is generated automatically by `/scripts/generate_features_index.py`.


Last updated: 2026-07-08T03:08:18Z