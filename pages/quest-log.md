---
title: The Quest Log
sub-title: Every level and side quest, one deep dive at a time
description: "My repositories, written up as levels and side quests, one per deep dive: what each one is, how it works, and what the daily review found"
author: bamr87
date: 2026-11-02T00:00:00-07:00
lastmod: 2026-11-02T00:00:00-07:00
permalink: /quest-log/
image:                 # the link card: a wide image instead of the square site-wide default
  path: /assets/images/social-preview.png
  width: 1280
  height: 640
  alt: "The bamr87.github.io homepage: Amr Abdel-Motaleb, I build systems."
---

The Quest Log in [Badwill Impairment](https://bamr87.github.io/posts/2026/11/01/badwill-impairment/) drew the map: eight levels, more than thirty side quests.

This is the walkthrough. One repository at a time, with screenshots, the architecture, and a status report nobody has polished for the board.

## How the log is kept

A daily review routine, the deep dive, takes one of my repositories each day, every active one once per 42-day cycle. The first cycle started on 30 October 2026.

An AI agent reviews the repository, scores it out of 100, files issues and opens pull requests. It never merges. I do.

The plan: every repository that gets its deep dive also gets an entry here. What it is, who it is for, how it works, and what the review found, open issues included. Built things are called built. Plans are called plans.

A corporate status report rounds everything to a color. This one gets a score out of 100 once the deep dive records it, and links to the open issues.

## The entries

{% assign quests = site.posts | where_exp: "post", "post.categories contains 'quest-log'" %}
{% if quests.size > 0 %}
Newest first.

<div class="row row-cols-1 row-cols-md-2 g-4 mb-4">
{% for post in quests %}
{% assign img = post.preview %}
{% if img %}{% unless img contains '://' %}{% assign first = img | slice: 0 %}{% if first != '/' %}{% assign img = '/' | append: img %}{% endif %}{% unless img contains '/assets/' %}{% assign img = site.public_folder | append: img %}{% endunless %}{% assign img = img | relative_url %}{% endunless %}{% endif %}
<div class="col">
<article class="card h-100 position-relative">
{% if img %}<img src="{{ img }}" class="card-img-top" alt="" loading="lazy">{% endif %}
<div class="card-body">
<h3 class="h5 card-title"><a class="stretched-link" href="{{ post.url | relative_url }}">{{ post.title | escape }}</a></h3>
<p class="card-text">{{ post.sub-title | default: post.description | escape }}</p>
</div>
<div class="card-footer"><small class="text-body-secondary"><time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%-d %B %Y" }}</time></small></div>
</article>
</div>
{% endfor %}
</div>
{% else %}
No entries yet. The first one appears here the day it is published.
{% endif %}

## Follow along

Each entry is also drafted as a LinkedIn post, and it goes out only after I approve it. To catch them as they land, follow [Amr Abdel-Motaleb on LinkedIn](https://linkedin.com/in/amrabdel).

The whole fleet is public at [github.com/bamr87/bamr87](https://github.com/bamr87/bamr87).
