---
title: Tags
description: Posts, docs, and notes grouped by tag and category.
layout: default
permalink: /tags/
sitemap: true
---

{% assign all_terms = "" %}
{% for doc in site.documents %}{% for t in doc.tags %}{% assign all_terms = all_terms | append: "|" | append: t | downcase %}{% endfor %}{% for c in doc.categories %}{% assign all_terms = all_terms | append: "|" | append: c | downcase %}{% endfor %}{% endfor %}
{% assign terms = all_terms | split: "|" | uniq | sort_natural %}

<ul class="list-inline">
{% for term in terms %}{% if term != "" %}<li class="list-inline-item"><a href="#{{ term | slugify }}">{{ term }}</a></li>{% endif %}{% endfor %}
</ul>

{% for term in terms %}{% if term != "" %}
<h2 id="{{ term | slugify }}">{{ term }}</h2>
<ul>
{% for doc in site.documents %}{% assign hit = false %}{% for t in doc.tags %}{% assign tl = t | downcase %}{% if tl == term %}{% assign hit = true %}{% endif %}{% endfor %}{% for c in doc.categories %}{% assign cl = c | downcase %}{% if cl == term %}{% assign hit = true %}{% endif %}{% endfor %}{% if hit %}<li><a href="{{ doc.url | relative_url }}">{{ doc.title | default: doc.url }}</a></li>{% endif %}{% endfor %}
</ul>
{% endif %}{% endfor %}
