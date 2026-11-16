<!-- kit: governance v0.1.0 -->
# 0002 — Missions

- **Status:** proposed
- **Date:** 2026-11-16
- **Proposed by:** Grok Bot (agent), at the maintainer's request
- **Ratified by:**
- **Affects:** constitution §1; PRD.md §1.1; PROFILE-006
- **Supersedes:** none
- **Related:** [PRD.md](../../PRD.md) §1.1

## Context

Constitution §1 was a single mission sentence or short paragraph, not one direction statement with exactly three numbered missions. The fleet rule is that every repo's constitution §1 uses that form, adopted through a numbered amendment the maintainer ratifies by merging. Mission 1 is the maintainer's own wording, adapted to this repo: provide data, tools, resources and transparency for all stakeholders, practitioners in the domain, and the general public. The ambition is the direction, not a claim that the work is already finished.

The earlier §1 text was:

> Amr Abdel-Motaleb's personal profile, résumé and project portfolio site, built with Jekyll on GitHub Pages (https://bamr87.github.io/). The README itself is the profile/résumé page.

## Amendment

Retitle constitution §1 **Missions**. Replace the body of §1 with the following. Any invariants or other normative rules that already lived outside §1 are unchanged.

This site's direction is to become the ultimate open home for this practitioner's public profile, résumé and work — data, tools, resources and transparency, gathered in one place that anyone can inspect and reuse.

1. **Provide data, tools, resources and transparency for all stakeholders, collaborators and the general public.** Visitors, collaborators, future employers, and the general public are first-class audiences. The aim is a shared, open record: the same profile, the same portfolio, and the same trail of how the site is built for everyone.
2. **Keep a clear, current public profile, résumé and project portfolio that anyone can read.** The path is a Jekyll site on GitHub Pages, so the work and how it is presented stay inspectable. The README itself remains a profile and résumé page.
3. **Put that record in every visitor's and collaborator's hands.** Serve the profile, the portfolio dashboard, and the posts, docs and notes collections — an open home for this practitioner's public work.

These missions set the course; they do not claim the work is finished. They serve the existing constitution and PRD: Amr Abdel-Motaleb's personal profile, résumé and project portfolio site. The earlier mission paragraph is absorbed into these three. Every feature must trace to them.

_Source: [../PRD.md](../PRD.md) §1.1._

## Consequences

Agents and reviewers judge fit against these three missions before inventing scope, treating them as the direction of the repo rather than a description of what already ships. The same text is added as PRD.md §1.1 so the constitution's `_Source:` line stays accurate. The PRD purpose, goals, feature catalog and invariants outside this addition are unchanged except for a new catalog entry (PROFILE-006) and a regenerated feature-catalog block where the repo already has one. This PR also aligns the README and AGENTS.md one-liners with the missions and links them to constitution §1.
