---
title: Badwill Impairment
sub-title: Three years since the noise stopped
description: "Three years since the noise stopped: a verdict, a newborn, and the skills to build enterprise software at scale without the corporate idiocracy."
author: bamr87
date: 2026-11-01T16:00:00-07:00
lastmod: 2026-11-01T16:00:00-07:00
tags:
  - badwill-impairment
  - journey
  - open-source
categories:
  - badwill-impairment
---

Three years ago today, the noise stopped, and the crying began.

You know the noise. It radiates and echoes through your PC (as in politically correct) inbox, screaming corporate American idiocracy disguised as “culture.”

We all know that grinding sound. It is us, feeding the beast with honor and devotion to our ominous shareholders, silently dreading the Groundhog Day-jà vu of stand-up after stand-up, week after week, and calling it progress.

Every day, the grown adults cry about budgets, headcount, capacity and data nobody can reach, or insist the system is to blame instead of the incompetence running it.

Then there’s the scariest noise of all, the one that turns Office Space into a horror film: leadership calling an emergency “cash flow imperative” meeting you weren’t invited to.

Flashbacks of interdepartmental warfare and finger-pointing fill every head in the room. Meeting after meeting, everyone rallies to be the savior who increases shareholder value.

Meanwhile, you sit quietly and watch the bookkeepers scramble for the latest GAAP loophole, digging through the data only to discover that no one in corporate accounting actually knows what drives the numbers.

Maybe they should consult an expert in financial systems. Maybe there’s a system design flaw quietly handing out cash discounts nobody meant to give.

But maybe that isn’t the point.

The cash flow imperative was never about the cash. It was about the meeting: who called it, who sat closest to the head of the table, who got credit for the slide that said “action items.” Fixing the flaws would have ended the meeting, and nobody in that room had anywhere better to be.

If corporate America rewarded talent, executives wouldn’t be reacting to a goodwill impairment in a year of record-breaking revenue and profits.

Goodwill is the premium a company pays for an acquisition above everything it can actually count: the brand, the relationships, the hope. An impairment is the company admitting, in writing, that the hope was worth less than the price. In a record year, the business is fine. The mistake is the price, paid years earlier by people who have since been promoted.

The write-down lands, and the fix is always the same line item: people. The ones who understand the systems become a cost to cut. The ones who bought the asset become the leadership. And the books get balanced by impairing the only goodwill the company ever really had.

Which is why corporate idiocracy wins every time, and why there’s no such thing as goodwill.

So the verdict came down. The adults stopped crying. Or I stopped having to watch.

And a baby started.

Different crying. The real kind. The miracle-of-life kind, where a brand-new person announces at full volume that they exist, they’re hungry, and you’re the one. No approval chain. No planned meetings. Only deep human connection that’s worth more than any corporate “imperative.”

Best paternity leave in corporate history.

Then the personal development got out of hand.

It went the way every epic goes, from zer0 to her0: one level at a time, each boss bigger than the last, and no one in the room to tell me which ones were out of scope.

**Level 0000: the map.** Every hero needs one. **[IT-Journey](https://it-journey.dev/)** ([source](https://github.com/bamr87/it-journey)) turns learning IT into quests on a binary level path, from Level 0000, the Apprentice’s first terminal and first Git commit, to Level 1111, the Legend. It started years before the noise stopped. Since then it has grown validation tooling that scores every quest, and opt-in AI agents that walk the curriculum, review it and repair it through pull requests a human merges.

**Level 0001: the dungeon.** Then the first fight, in the terminal. **[bashcrawl](https://bamr87.github.io/bashcrawl/)** ([source](https://github.com/bamr87/bashcrawl)) teaches real shell skills as a fantasy dungeon crawl where the filesystem is the game: directories are rooms, scrolls are the lessons and scripts are the encounters. It now has a second door, a browser trainer with courses, mini-games and cheatsheets built from the same content. Credit where it is due: it is built on Seth Kenlon’s original bashcrawl, under the same GPL.

**Level 0010: the spreadsheet.** Then the thing that wastes the most hours in any office. **[csv-vscoode](https://apps.bash-365.com/csv-vscode/)** ([source](https://github.com/bash-365/csv-vscoode)) puts the spreadsheet inside the editor, on top of the file itself, so you never leave the scene to fix a column and nothing quietly reformats your dates on the way out. It shipped. It is finished. It is archived. Achievement unlocked: done, a status corporate project reports rarely offer.

**Level 0011: the newsroom.** Next, a publication that writes itself. **[lifehacker.dev](https://lifehacker.dev/)** ([source](https://github.com/bamr87/lifehacker.dev)) is drafted by a robot, reviewed by a human and published with the mistakes left in. The mistakes are the evidence. Three hundred posts in, the robot is on leave. Unlike mine, its leave needed a configuration change.

**Level 0100: the analyst.** Then the numbers. **[fredgar-ai](https://bamr87.github.io/fredgar-ai/)** ([source](https://github.com/bamr87/fredgar-ai)) reads SEC filings and FRED data, and every Monday a site of company financials publishes itself. A machine that actually reads cash flow statements, which already puts it ahead of the imperative.

**Level 0101: the lawyer.** Then the risk. **[law-ai](https://bamr87.github.io/law-ai/)** ([source](https://github.com/bamr87/law-ai)) keeps a lawyer on retainer who never sleeps: research agents over a graph of cases and citations, a person approving everything that comes in, and one switch that keeps every prompt on a local model, so nothing leaves the building. It is still in training. The cross-examination of every pull request is written and waiting for its first case.

**Level 0110: the platform.** Then the content itself. **[zer0-CMS](https://github.com/bamr87/zer0-CMS)** was cut loose from a Front Matter fork and rebuilt on Django and Wagtail. SQLite or Postgres. Ships in a container. No Rails left in the body. AI suggests, a person approves, and only then does anything publish, to a site, to LinkedIn or to X, with a ledger that remembers so nothing goes out twice.

**Level 1111: the control plane.** I skipped a few levels. This is the thing they wouldn’t let me build. **[bamr87/bamr87](https://bamr87.github.io/bamr87/)** ([source](https://github.com/bamr87/bamr87)) runs a fleet of forty-four repositories from one registry. The README regenerates itself after every merge, a drift check fails any pull request that disagrees with the registry, and agents triage, build and review, with CI checking every change. The rest of the map (eyes on every service, infrastructure reconciled from git, a phone in my pocket that watches the fleet) is the next level. Unlike a corporate roadmap, each item on it already has a repository.

Those are the boss fights. In between came the side quests, more than thirty of them:

- **The tools that build the tools.** [githubai](https://github.com/bamr87/githubai) packages the agents that triage issues, implement the work and review the pull requests as reusable GitHub Actions. [gitorio](https://bamr87.github.io/gitorio/) ([source](https://github.com/bamr87/gitorio)) is a Factorio-style factory builder whose blueprints compile into GitHub Actions workflows. [SCHEMA](https://github.com/bamr87/SCHEMA) is a protocol and a linter that let an AI agent look up a repository’s structure instead of guessing it. [bashos](https://github.com/bamr87/bashos) routes Claude’s slash commands through a LangGraph kernel. [scripts](https://github.com/bamr87/scripts) is where every chore I did twice went to become a command.
- **The extensions.** [zpl-viewer](https://github.com/bamr87/zpl-viewer) reads, builds and sends thermal-printer labels from inside VS Code, offline. [vs-sonic-pi](https://github.com/bamr87/vs-sonic-pi) lets you write and perform Sonic Pi music live from the editor.
- **AI that reads and races.** [ocrmd](https://github.com/bamr87/ocrmd) turns scanned books into Markdown, checking a local OCR read against a Claude vision read. [outbox](https://github.com/bamr87/outbox) races three agents through a mailbox protocol, with lag injected and confidence scored. [djangoerp](https://github.com/bamr87/djangoerp) is a modular ERP in Django, double-entry accounting first, still an experiment.
- **The sites.** [zer0-mistakes](https://zer0-mistakes.com) ([source](https://github.com/bamr87/zer0-mistakes)), the Jekyll theme every one of these sites wears, published as a Ruby gem. [Year of AI](https://year-of-ai.github.io/) ([source](https://github.com/year-of-ai/year-of-ai.github.io)) and [AI World View](https://ai-world-view.github.io/) ([source](https://github.com/ai-world-view/ai-world-view.github.io)), the front doors of two content networks. [cv-pro](https://github.com/bamr87/cv-pro), my CV as code. [This site](https://bamr87.github.io/) ([source](https://github.com/bamr87/bamr87.github.io)). And [bash-365.com](https://www.bash-365.com/) ([source](https://github.com/bash-365/bash-365.com)), where all of this becomes a business.
- **Play.** [godotgo](https://github.com/bamr87/godotgo) is a Godot 4 workspace with one shared framework and five sample games. [rewind-arcade](https://bamr87.github.io/rewind-arcade/) ([source](https://github.com/bamr87/rewind-arcade)) is a retro gaming workspace, down to a catalog of the physical shelf.
- **The backlog.** A key-value store in Rust, a network toolkit in Go, a passkey identity provider, a hobby operating-system kernel, ESP32 sensor firmware, a security practice lab, a blueprint compiler, an EDGAR data pipeline and a fully local search engine over a radio show’s archive. Each exists today as a repository with a README and a plan: the levels I haven’t played yet.
- **The plumbing.** [Shared workflows](https://github.com/bamr87/.github) for every repository, [a context engine](https://bamr87.github.io/README/) ([source](https://github.com/bamr87/README)) that builds the docs for every project, a redirect that keeps bash-365.com pointed at its front door, a personal fork of the Omarchy desktop, a self-evolving template I retired, and two agent-skill libraries borrowed from other people’s repositories.

Add it up and it stops looking like personal development. Eight levels and more than thirty side quests, and every boss is a system a corporation would staff with a department, a budget cycle and somebody’s permission. Now I have the skills to design and build enterprise software and systems at scale, on my own terms, without the corporate idiocracy.

[github.com/bamr87/bamr87](https://github.com/bamr87/bamr87)

