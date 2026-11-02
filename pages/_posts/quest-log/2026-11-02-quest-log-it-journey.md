---
title: "IT-Journey: learn IT as quests you run in your own terminal"
sub-title: "Corporate training ends in a certificate nobody reads. My curriculum sends AI agents through it and publishes its own failing grade."
description: "A tour of Amr Abdel-Motaleb's free IT curriculum: 213 hands-on quests, a generated map, the AI agents that test it, and what a daily AI review found"
author: bamr87
date: 2026-11-02T00:10:00-07:00
lastmod: 2026-11-02T00:10:00-07:00
tags: [badwill-impairment, quest-log, education, gamification, ai-agents, open-source]
categories: [quest-log]
preview: /images/quest-log/quest-log-it-journey/preview.png
---

**Level 0000: the map.** Every hero needs one.

Every company already has one, in principle. It is called the training portal: click-through modules with the sound off, a quiz at the end, and a certificate nobody reads. Beside it sits the onboarding wiki, last edited by someone who has since left.

IT-Journey is the other kind of map. Every lesson is a quest you run in your own terminal, and AI agents play-test the map and report what is broken, in public.

## What it is, and who it is for

[IT-Journey](https://it-journey.dev/) is a free, open-source curriculum for learning IT and software development by doing it.

![The IT-Journey homepage hero. The site navigation bar reads Quests, Epic, Blog, Digs, Notes and About. A pill badge reads Open-source, Gamified, Self-paced. A large IT-JOURNEY wordmark sits over ZER0 → HER0, then the line '> learn the terminal', the promise 'Turn learning IT & software development into an epic adventure. Every concept is a quest, every skill an unlocked power, every level a step from novice to architect.', and two buttons, Begin Your Quest and Enter the Overworld. On the right is an illustration of a wizard on a cliff among floating server racks and clouds.](/assets/images/quest-log/quest-log-it-journey/01-home-hero.jpg)

*The front door at it-journey.dev: the whole pitch fits on one screen.*

The path is numbered in binary. As of 1 November 2026, the Overworld counts 213 quests across 16 levels in 4 tiers: Apprentice (0000 to 0011), Adventurer (0100 to 0111), Warrior (1000 to 1011) and Master (1100 to 1111). Level 0000 is the Apprentice's first terminal and first Git commit. Level 1111, Leadership and Innovation, tops the Master tier.

It is for complete beginners who want to end up doing the work, and for anyone who learns by typing rather than watching. Six character paths chain the levels into a role: Software Developer, System Engineer, Security Specialist, Data Scientist, Digital Artist (UI/UX) and Game Developer.

There is no account. Progress stays in your browser, and the homepage states the terms in four words: "No signup. No paywall."

![The IT-Journey Overworld dashboard. Five stat cards read 213 quests, 16 levels, 4 tiers, 0 completed and 0% done. A Your Progress panel shows 0 / 213 complete and the note 'Progress is stored locally in your browser'. Below it, The Realm Map shows four tier cards: Apprentice (0 / 76 complete), Adventurer (0 / 41), Warrior (0 / 46) and Master (0 / 50). Each card lists four binary levels with their experience-point ranges, from 0000 Foundation & Init World (0-250) to 1111 Leadership & Innovation (9000+).](/assets/images/quest-log/quest-log-it-journey/02-overworld-realm-map.jpg)

*The map itself on 2 November 2026: 213 quests from 0000 to 1111, and your progress lives in your browser, not behind a sign-up form.*

The first commit landed on 30 July 2020; main held 1,667 commits as of 1 November 2026.

## How it works

It is a Jekyll site on GitHub Pages, wearing [zer0-mistakes](https://zer0-mistakes.com), the theme all my sites share, with Python tooling behind it. The curriculum is governed data, not a pile of pages.

**Every quest signs a contract.** A quest is a Markdown file that must declare 12 front-matter fields, from its level and difficulty to its estimated time. It lists objectives to tick off, the commands to run, and the quests it requires, recommends and unlocks.

**The map is generated, never drawn.** One command, `make quest-data`, reads every quest and regenerates the levels, the navigation and the dependency network. Nobody hand-edits the output, and continuous integration (CI) fails a pull request whose generated data has gone stale. As of 1 November 2026 the network holds 574 links: 136 required, 152 recommended and 286 unlocks.

![Level 0000's Quest Network panel with the count '30 quests · 77 links' and a Reset view button. A dark graph shows colored nodes joined by arrows. One dense cluster holds starter quests such as Terminal Fundamentals, Git Basics, VS Code Mastery, Hello macOS and Character Selection. A separate cluster holds the Bashcrawl dungeon chain (Entrance, Cellar, Armoury, Rift, Vault, Workshop). The legend reads Easy (green), Medium (orange), Hard (red), Epic (purple), You are here, required, unlocks and recommended.](/assets/images/quest-log/quest-log-it-journey/03-level-0000-quest-network.jpg)

*Level 0000 is a dependency graph, not a playlist: every arrow is a prerequisite, an unlock or a recommendation.*

**The quest fits the reader.** As of 1 November 2026, 127 published quests carry an environment block. The page detects your operating system, shows only your path (macOS, Windows or Linux; zsh, bash or PowerShell), rewrites every snippet to the folder name you pick, and remembers the choice. With JavaScript off, every path stays visible.

**Gates come before the merge.** A quest validator scores every quest, and CI fails one that scores below 70 percent. Beside it sit a dependency-network validator, a front-matter validator and a brand-voice lint, plus an advisory link checker and accessibility checks on pull requests.

## The testers who actually take the course

Most training is checked by whoever wrote it. This curriculum is checked by agents who take it.

A deterministic planner picks one slice of the map: one character path at one level. The quest-walker agent plays those quests in a disposable sandbox, runs the commands for real, and writes one report. The workflow mints and seals the evidence, so the walker can only read it. The walker never edits a quest and never merges.

A fix arm then repairs what the walk found, and keeps an edit only when a deterministic signal improves: the score holds or rises, the brand lint stays clean, and no sandbox command regresses. In the AI fleet's own README: "never because the model graded its own work up." After three rounds that never reach perfect, a circuit breaker hands the slice to a human.

Every lane is off until its switch and its credential are both set. Content-only fixes ride a label-routed auto-merge lane: a guard that rejects anything but content, then green checks, then a squash-merge, behind a switch I set. Between 6 July and 9 September 2026 it merged 39 of the 40 quest-fix pull requests, and I merged the other.

The loop published 130 walkthrough reports between 29 June and 9 September 2026. They read like a learner who refuses to be polite.

![The Journey table from an AI walkthrough report, with columns #, Verdict, Quest, Type, Score and One-line takeaway. Three quests pass with green checks: API Fundamentals (94), Initiation Rites: Agents in the SDLC (83) and REST Principles (94). Two fail with red crosses. Initiation Rites: Embedding Agents in the SDLC scores 51 because both setup snippets fail ('work/gh-600 doesn't exist anywhere in repo history'). The Three Sigils: Plan, Reason, Act scores 30 because a systemic Markdown fence bug collapses most of the document.](/assets/images/quest-log/quest-log-it-journey/04-walkthrough-report.jpg)

*From the 9 September 2026 walkthrough of the Digital Artist path at Level 0111: an agent ran the commands and wrote down exactly what broke.*

Five quests, scored 94, 83, 94, 51 and 30. One sent learners to a work/gh-600 folder that "doesn't exist anywhere in repo history". Another had a Markdown fence bug that collapsed most of the page into one block. A completion certificate would have been issued for both.

![The Quest Perfection Dashboard. An intro says the autonomous quest-perfection loop walks IT-Journey's quests end to end as a learner and mirrors the committed ledger (.quests/ledger.json). Next come the line 'Ledger generated 2026-09-09T11:31:48+00:00.' and the summary '0/27 slices perfect · 3 stuck (needs human) · 380 open issue(s) outstanding'. Then the first five rows of the Slices table: one warn and four fail verdicts, averages from 62.0 to 71.5, two slices marked stuck and three sweeping, with latest-report dates from July and September 2026.](/assets/images/quest-log/quest-log-it-journey/05-perfection-dashboard.jpg)

*The system publishes its own failing grade: 0 of 27 slices perfect, unchanged since 9 September 2026.*

## What the deep dive found

The deep dive is a daily AI review routine run from my hub repository. At 06:00 Denver time it takes one of my repositories, every non-archived one once per 42-day cycle, reviews it, files what it finds as issues and pull requests labeled deep-dive, and records the run in a ledger with a public [dashboard](https://bamr87.github.io/bamr87/deep-dive/). It never merges, force-pushes or touches a setting or a secret. I merge its fixes. This series rides on it.

Day 1 of cycle 1 was IT-Journey, run a day early on 29 October 2026. **Score: 72 out of 100.** Against the fleet's own standard it passed 45 of 58 checks, with 8 required checks failing. It filed 8 issues and 1 pull request.

**What is solid.** The core: none of the eight issues touched the quest contract, the generated map, the 70 percent gate or the agents' switches.

**What got fixed.** Two findings were bugs, and both were fixed the next day. The site feed had zero entries ([#869](https://github.com/bamr87/it-journey/issues/869)), and `make test` still checked a folder that no longer exists ([#867](https://github.com/bamr87/it-journey/issues/867)). I merged [#888](https://github.com/bamr87/it-journey/pull/888) on 30 October. It fixed both and shipped a quest Atom feed, and both feeds carried 30 entries on 1 November.

**What is open**, as of 2 November 2026:

- [#871](https://github.com/bamr87/it-journey/issues/871): reader feedback on quest pages, priority 1.
- [#870](https://github.com/bamr87/it-journey/issues/870): the quest feed shipped, but the quest hub has no visible subscribe link.
- [#868](https://github.com/bamr87/it-journey/issues/868): the feature catalog still lists retired sections as undecided.
- [#872](https://github.com/bamr87/it-journey/issues/872): issue templates apply no type label.
- [#873](https://github.com/bamr87/it-journey/issues/873): shared fleet workflows are referenced at @main, not a pinned version.
- [#874](https://github.com/bamr87/it-journey/issues/874): a committed npm lockfile, which the fleet standard flags.
- [#875](https://github.com/bamr87/it-journey/pull/875): the deep dive's own docs pull request, partly overtaken by #888.

On 30 October the repository's own issue autopilot routed all six issues to a human: some need workflow edits the agents' rules forbid, and the rest sit outside its content-only scope. The robots did the paperwork, read their own job description, and escalated.

**One more, found while writing this.** The walk loop has been idle since 9 September. Its daily run still ends green with its work jobs skipped, so the dashboard has read 0 of 27 perfect, with 380 open findings, for almost two months. The curriculum maintained itself all summer. The autumn term has not started.

## What is built, and what is still a plan

Built and running: everything above, plus the two feeds and the [Quest Idea Forge](https://it-journey.dev/quests/ideas/), a form that scores a visitor's quest idea out of 100 and checks it for duplicates before filing it as an issue. As of 1 November, nobody has filed one.

Built and not yet used: a video lane that records a quest page beside a replay of its sandbox terminal, uploads it unlisted, and opens a pull request a human reviews. Its catalog is still empty.

Still a plan: reader feedback on quests (#871). The product requirements document lists Community for 2026 Q1 and Certification for 2026 Q2, both as Planned, with an AI tutor as the Vision for 2026 Q4. Both target quarters have come and gone, which makes the roadmap the most corporate document in the repository.

## How to try it

- **Live:** [it-journey.dev](https://it-journey.dev/). Start at Level 0000, or open [the Overworld](https://it-journey.dev/quests/home/) and pick a character.
- **The report cards:** [it-journey.dev/quest-reports](https://it-journey.dev/quest-reports/), failing grades included.
- **Source:** [github.com/bamr87/it-journey](https://github.com/bamr87/it-journey), MIT-licensed. Clone it and run `make serve` with Ruby 3.2 or newer, or use the Docker path in the README.

*Skill unlocked: a curriculum that maintains itself.*

This is Level 0000 of [the Quest Log in Badwill Impairment](https://bamr87.github.io/posts/2026/11/01/badwill-impairment/#the-quest-log). The other levels and side quests arrive one deep dive at a time on the [Quest Log series page](https://bamr87.github.io/quest-log/).
