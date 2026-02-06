---
layout: default
title: "Features Index (Consolidated)"
lastmod: 2026-02-06T03:03:31Z
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
| Bootstrap 5.3.3 Theme Integration | zer0-mistakes | jekyll, theme, bootstrap, ui, responsive | / |
| Docker-First Development Environment | zer0-mistakes | docker, devops, development, cross-platform | / |
| AI-Powered Installation System | zer0-mistakes | ai, automation, installation, error-handling, bash | / |
| AI Preview Image Generator | zer0-mistakes | ai, images, automation, openai, content | /docs/features/preview-image-generator/ |
| GitHub Copilot Integration | zer0-mistakes | ai, copilot, development, documentation | https://github.com/bamr87/zer0-mistakes/blob/main/.github/copilot-instructions.md |
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
| Automated Version Bump Workflow | zer0-mistakes | github-actions, automation, versioning, ci-cd | / |
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
| Site Search | zer0-mistakes | search, navigation, modal, keyboard | / |
| Auto-hide Navigation | zer0-mistakes | ui, navigation, scroll, mobile | / |
| Particles Background | zer0-mistakes | ui, animation, visual, landing | / |
| Giscus Comments | zer0-mistakes | comments, github, discussions, engagement | / |
| MathJax Math Rendering | zer0-mistakes | math, latex, equations, documentation | / |
| Table of Contents | zer0-mistakes | navigation, toc, headings, documentation | / |
| Google Analytics | zer0-mistakes | analytics, google, tracking, metrics | / |
| Google Tag Manager | zer0-mistakes | analytics, gtm, tracking, marketing | / |
| Breadcrumbs Navigation | zer0-mistakes | navigation, breadcrumbs, seo, accessibility | / |
| SEO Optimization | zer0-mistakes | seo, meta, opengraph, twitter-cards | / |
| Sitemap Generation | zer0-mistakes | seo, sitemap, search, indexing | / |
| Statistics Dashboard | zer0-mistakes | dashboard, statistics, metrics, visualization | / |


## Requested / Backlog Features


*No backlog items found.*


---

*This index is generated automatically by `/scripts/generate_features_index.py`.


Last updated: 2026-02-06T03:03:31Z