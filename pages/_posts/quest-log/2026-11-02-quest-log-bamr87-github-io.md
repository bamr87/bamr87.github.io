---
title: "bamr87.github.io: a portfolio that runs on data, not memory"
sub-title: "One tile on my portfolio's stats strip is typed by hand: years building. The rest are generated nightly; one failed fetch stops the run."
description: "A tour of Amr Abdel-Motaleb's profile site: one project list, a nightly generator that fails closed, a features index, and what a daily AI review found"
author: bamr87
date: 2026-11-02T00:30:00-07:00
lastmod: 2026-11-02T00:30:00-07:00
tags: [badwill-impairment, quest-log, developer-portfolio, jekyll, github-pages, github-actions]
categories: [quest-log]
preview: /images/quest-log/quest-log-bamr87-github-io/preview.png
---

**Side quest: the personnel file.** Every company keeps a file on you. Once a year it is updated by self-review: part memory, part template, part negotiation.

I keep mine myself. It is rebuilt every night from one list of projects and GitHub's own records, and if a single number fails to load, that night's update writes nothing at all.

Most annual reviews would not survive that rule.

## What it is, and who it is for

[bamr87.github.io](https://bamr87.github.io/) is my GitHub Pages site. The repository was created on 24 July 2022, and its first commit is titled, with real ambition, "first commit".

It does three jobs: a homepage dashboard of my projects, a résumé that is the repository's README published as a page, and a blog with docs, notes and notebook collections.

It is for the people who look someone up before a call: recruiters, clients and collaborators. It is also for me: a record whose numbers update themselves.

Four repositories are left out of the showcase by name. One is the site itself, with the comment "linked from the profile, not the showcase". Modesty, enforced in a YAML file.

## How it works

**The theme is borrowed.** Jekyll 3.10 builds it on GitHub Pages, wearing zer0-mistakes, the theme from the same Quest Log. The repository holds content, configuration and data, and no layouts of its own.

**One list decides.** The registry, `_data/projects.yml`, names twelve projects as of 1 November 2026, three of them featured, each with a category. Ten carry a one-line blurb that overrides the GitHub description.

**A generator does the rest.** `scripts/generate_portfolio.py`, 461 lines of Python, reads the list and asks the GitHub API about each repository: stars, language, homepage, Pages address, topics, license and last push. From that one source it writes three outputs: the data behind the homepage dashboard, the long-form portfolio page, and the featured block inside the résumé. With `--check`, it fails when any output has drifted.

**It fails closed.** If a single GitHub request fails, the generator exits before it writes anything. That rule has a history. The site audit of 17 October found the homepage showing three different repository counts at once, which [#35](https://github.com/bamr87/bamr87.github.io/pull/35) fixed. Its follow-up found the nightly run overwriting fixed links with degraded ones whenever GitHub rate-limited it ([#24](https://github.com/bamr87/bamr87.github.io/issues/24)). An agent's pull request made the generator fail closed ([#43](https://github.com/bamr87/bamr87.github.io/pull/43)), and I merged it.

**A robot keeps it current.** A workflow called "Regenerate site indexes" runs at 02:00 UTC every night, reruns the generators and commits the result to main. As of 1 November 2026, 141 of the repository's 425 commits are that robot: about one in three.

**The browser double-checks.** When the homepage loads, it asks the GitHub API for the current repository and follower counts and replaces the numbers baked in at build time, on a best-effort basis.

**The fleet reports in.** The same nightly run builds a [features index](https://bamr87.github.io/about/features/) from the feature files the fleet's repositories declare. The run of 1 November (Denver time; 02:12 UTC on 2 November) lists 203 current features across 28 repositories, plus 78 backlog items. It is a capability inventory nobody has to fill in by Friday.

## The tour

The front door. Even the count in the pill above the name is generated.

![The bamr87.github.io homepage in dark mode, with the site navigation bar (Projects, Journey, Library, Notebook, About, Search) at the top. Below it are a pill reading Available for collaboration, 42 public repos, the name Amr Abdel-Motaleb in large gradient type, the line I build systems, a two-line tagline about weaving business operations with financial precision, and three buttons: Explore the work, GitHub and Résumé.](/assets/images/quest-log/quest-log-bamr87-github-io/01-homepage-hero.jpg)

*The repository count in the pill is the same generated number the stats strip uses (1 November 2026).*

The stats strip has six tiles. Five are generated. The sixth, "14+ years building", is a literal in the page's HTML, and it is the only number on the strip no machine checks.

![A strip of six stat tiles reading 42 Public Repos, 52 Stars Earned, 20 Followers, 12 Showcased, 5 Languages and 14+ Years Building. Below it are the Flagship work eyebrow, the Featured Projects heading and two project cards, it-journey and zer0-mistakes, each with a description, a language, a star count, topic chips, and Repo and Live buttons.](/assets/images/quest-log/quest-log-bamr87-github-io/02-stats-and-featured.jpg)

*Five tiles come from the generator and the GitHub API, as of 1 November 2026. The stars are the total across the twelve showcased projects.*

Every card in the catalog comes from the registry plus GitHub.

![The All Projects section with the Apps and AI filter chip selected, among chips for All 12, Learning and Docs, Jekyll and Web, Infrastructure, Editor Tooling and Data, plus a Search projects box. Three cards remain: githubai, ai-seed and wtd, each with a description, Python, a star count, the Apps and AI category, topic chips and a Repo button.](/assets/images/quest-log/quest-log-bamr87-github-io/03-catalog-filter.jpg)

*The catalog filtered to Apps and AI: client-side interaction on GitHub Pages, with no server or database behind it.*

The same registry in long form, written by the same generator.

![The Portfolio page in dark mode. A pixel-art mountain banner carries the title Portfolio, the author Amr Abdel-Motaleb and the dates Published Jun 14, 2026 and Updated Oct 28, 2026. Below it are the line Curated in _data/projects.yml and refreshed automatically with live repository metadata, a Featured heading and the it-journey entry with stars, last-commit and Python badges. An On this page outline at the right groups the projects by category.](/assets/images/quest-log/quest-log-bamr87-github-io/04-portfolio-page.jpg)

*One curated file drives three outputs: the dashboard data, this page and the résumé's portfolio block.*

And the inventory, collected every night.

![The Current Features heading above a table with Title, Repo, Tags and Link columns and a Copy CSV button. The visible rows list .github entries (reusable workflows, composite actions, a starter workflow, issue and PR templates) and bamr87 entries: Portfolio + dashboard from the registry, Projects board, Fleet triage inbox and Issue pipeline board, each with tags and a path such as /portfolio or /inbox.](/assets/images/quest-log/quest-log-bamr87-github-io/05-features-index.jpg)

*203 current features across 28 repositories, plus 78 backlog items, as of 1 November 2026. The Link column is still plain text.*

## What the deep dive found

The deep dive is a daily AI review routine run from my hub repository. At 06:00 Denver time it takes one of my repositories, every non-archived one once per 42-day cycle, reviews it, files what it finds as issues and pull requests labeled deep-dive, and records the run in a ledger with a public [dashboard](https://bamr87.github.io/bamr87/deep-dive/). It never merges, force-pushes or touches a setting or a secret. I merge its fixes. This series rides on it.

Day 3 of cycle 1, scheduled for 1 November 2026, was this site.

**No score yet.** As of 2 November 2026 the ledger still lists day 3 as pending, with no score recorded, so there is no number out of 100 to print here. I am not going to invent one. Inventing the number is the self-review's job.

**What it filed.** Three issues on 1 November, each labeled needs-amr, which is the polite way of saying the decision is mine. It opened no pull requests.

- [#47](https://github.com/bamr87/bamr87.github.io/issues/47): the AI-ready layer the fleet's constitution asks of a content site is missing. There is no llms.txt, no manifest, no static JSON API and no local Model Context Protocol (MCP) server. The structured data for search engines is already on the pages. It waits on my call about scope.
- [#48](https://github.com/bamr87/bamr87.github.io/issues/48): the workflows pin third-party actions to floating version tags instead of commit hashes, and the hub's shared workflows and actions are referenced partly at `@main` and partly at `@v2`. The policy is mine to pick.
- [#49](https://github.com/bamr87/bamr87.github.io/issues/49): secret scanning and push protection are switched off on a public repository. That is a setting, and no agent may change a setting, so the finding is a note addressed to me.

**What is solid.** Before the deep dive, a site audit on 17 October filed fourteen issues, #19 to #32. Agent pull requests closed four of them, and I merged all four by 30 October: dead links ([#41](https://github.com/bamr87/bamr87.github.io/pull/41)), site metadata ([#42](https://github.com/bamr87/bamr87.github.io/pull/42)), the fail-closed generator ([#43](https://github.com/bamr87/bamr87.github.io/pull/43)) and navigation, with an internal link check added to continuous integration ([#44](https://github.com/bamr87/bamr87.github.io/pull/44)).

The metadata finding is my favorite. Every page carried the site name "Prod" ([#26](https://github.com/bamr87/bamr87.github.io/issues/26)). The author field said null 27 times, and elsewhere ChatGPT, GitHub Copilot, Apple and, in one post, a timestamp. An agent gave all 57 bylines back to one author key: a credit dispute settled in one diff, with no calibration meeting.

**What is open**, as of 2 November 2026: 14 issues and 2 pull requests. Besides the three above, there is [#50](https://github.com/bamr87/bamr87.github.io/issues/50), adopting the fleet's shared frontend platform, queued for an agent, and ten audit issues, among them light-mode contrast and an orphaned featured card ([#30](https://github.com/bamr87/bamr87.github.io/issues/30)) and page weight ([#32](https://github.com/bamr87/bamr87.github.io/issues/32)). The pull requests are the next release and the Badwill Impairment post itself.

**One more, found while writing this.** The site's own test suite is red on main: the nightly run of 1 November reported 31 passed and 1 failed. The failure is real: two index pages from a pull request merged on 30 October have no date. Nothing blocks on it: the shared continuous integration skips Python tests in a repository without a root requirements or package file, and the nightly job runs them with continue-on-error. A test suite no gate enforces is a performance review with no consequences.

## What is built, and what is still a plan

Built and running: the dashboard, the registry and its generator, the nightly regeneration, the features index, the résumé page, and nine workflows, among them an internal link check and release-please releases (the latest, v0.2.1, on 30 October). As of 1 November, the feature catalog lists four features, all shipped.

The requirements document still lists the success metric, profile visits and contact inquiries, as "TBD (no analytics source identified)", although a Google Analytics tag already loads on the live site. The measuring exists; the target does not. Plenty of quarterly plans have it the other way round.

Still a plan: the AI-ready layer ([#47](https://github.com/bamr87/bamr87.github.io/issues/47)), the shared frontend platform ([#50](https://github.com/bamr87/bamr87.github.io/issues/50)), the light-mode polish ([#30](https://github.com/bamr87/bamr87.github.io/issues/30)), a workflow that runs the existing drift check, and a test suite that blocks a merge when it fails. The site is also meant to be the home of this series, one showcase per deep dive.

## How to try it

- **Live:** [bamr87.github.io](https://bamr87.github.io/). Try the category chips and the search box under All Projects.
- **Source:** [github.com/bamr87/bamr87.github.io](https://github.com/bamr87/bamr87.github.io).
- **Run it:** `bundle install`, then `bundle exec jekyll serve` for a production-like preview on port 4002.

*Skill unlocked: a résumé with a build pipeline.*

This is a side quest from [the Quest Log in Badwill Impairment](https://bamr87.github.io/posts/2026/11/01/badwill-impairment/#the-quest-log), listed under The sites. The other levels and side quests arrive one deep dive at a time on the [Quest Log series page](https://bamr87.github.io/quest-log/).
