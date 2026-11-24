#!/usr/bin/env python3
"""Build the Beit Shawarma website into site/.

Everything a customer reads comes from two files: content/site.json (name, address,
phone, hours, about text) and content/menu.json (every dish and price). Change one of
those, run this script, and every page, the Google business data (JSON-LD) and the
sitemap update together. Standard library only: any Python 3.9+ works.

  python3 build.py           # write site/
  python3 build.py --check   # exit 1 if site/ is out of date with content/ and static/
  python3 build.py --preview https://example.github.io/beit-shawarma --out DIR [--check]
                             # a noindex preview for another address (no CNAME, no sitemap)
"""
from __future__ import annotations

import argparse
import datetime as dt
import filecmp
import html
import json
import shutil
import sys
import tempfile
from pathlib import Path
from urllib.parse import quote_plus, urlparse

ROOT = Path(__file__).resolve().parent
SITE = json.loads((ROOT / "content/site.json").read_text(encoding="utf-8"))
MENU = json.loads((ROOT / "content/menu.json").read_text(encoding="utf-8"))
ITEMS = {i["id"]: i for c in MENU["categories"] for i in c["items"]}
# Where the build will be served. Production is the real domain; --preview retargets a copy
# (for example https://bamr87.github.io/beit-shawarma) that search engines are told to skip.
TARGET = {"url": SITE["url"], "base": "/", "preview": False}
DAY_NAMES = {"Mo": "Monday", "Tu": "Tuesday", "We": "Wednesday", "Th": "Thursday", "Fr": "Friday", "Sa": "Saturday", "Su": "Sunday"}


def e(s: object) -> str:
    return html.escape(str(s), quote=True)


def money(p: str) -> str:
    return f"${float(p):,.2f}"


def address_line() -> str:
    a = SITE["address"]
    tail = f" {a['postalCode']}" if a.get("postalCode") else ""
    return f"{a['street']}, {a['city']}, {a['region']}{tail}"


TEL = f"tel:{SITE['phone']['e164']}"
WA = f"https://wa.me/{SITE['whatsapp']}"
MAIL = f"mailto:{SITE['email']}"
MAP_EMBED = f"https://maps.google.com/maps?q={quote_plus(SITE['mapEmbedQuery'])}&z=16&output=embed"

# ---------------------------------------------------------------- icons (24px, stroke)
ICONS = {
    "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.12.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.58 2.81.7A2 2 0 0 1 22 16.92z"/>',
    "chat": '<path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>',
    "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "leaf": '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/>',
    "flame": '<path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.07-2.14-.22-4.05 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.15.43-2.29 1-3a2.5 2.5 0 0 0 2.5 2.5z"/>',
    "halal": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
    "tray": '<path d="M2 18h20"/><path d="M4 18a8 8 0 0 1 16 0"/><path d="M12 10V7"/><path d="M10 7h4"/>',
    "arrow": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "nav": '<path d="m3 11 19-9-9 19-2-8-8-2z"/>',
    "menu": '<path d="M4 6h16M4 12h16M4 18h16"/>',
    "close": '<path d="M18 6 6 18M6 6l12 12"/>',
    "facebook": '<path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>',
    "instagram": '<rect x="2" y="2" width="20" height="20" rx="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><path d="M17.5 6.5h.01"/>',
}


def icon(name: str, cls: str = "icon") -> str:
    return (f'<svg class="{cls}" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


# ---------------------------------------------------------------- structured data
def restaurant_ld() -> dict:
    a = SITE["address"]
    addr = {"@type": "PostalAddress", "streetAddress": a["street"], "addressLocality": a["city"],
            "addressRegion": a["region"], "addressCountry": a["country"]}
    if a.get("postalCode"):
        addr["postalCode"] = a["postalCode"]
    mains = [float(i["price"]) for c in MENU["categories"] if c["id"] in ("platters", "sandwiches") for i in c["items"]]
    ld = {
        "@context": "https://schema.org", "@type": "Restaurant", "@id": f"{TARGET['url']}/#restaurant",
        "name": SITE["name"], "slogan": SITE["tagline"], "description": SITE["summary"], "url": TARGET["url"] + "/",
        "logo": f"{TARGET['url']}/img/brand/logo.png", "image": [f"{TARGET['url']}/img/og.jpg"],
        "telephone": SITE["phone"]["e164"], "email": SITE["email"], "address": addr, "hasMap": SITE["mapsUrl"],
        "servesCuisine": SITE["cuisine"], "priceRange": f"${round(min(mains))}–${round(max(mains))}",
        "hasMenu": f"{TARGET['url']}/menu/", "acceptsReservations": False,
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification", "dayOfWeek": [DAY_NAMES[d] for d in h["days"]],
             "opens": h["opens"], "closes": h["closes"]} for h in SITE["hours"]],
    }
    same = [u for k, u in SITE["social"].items() if not k.startswith("_") and u]
    if same:
        ld["sameAs"] = same
    return ld


def menu_ld() -> dict:
    sections = []
    for c in MENU["categories"]:
        items = []
        for i in c["items"]:
            diets = ["https://schema.org/HalalDiet"] + (["https://schema.org/VegetarianDiet"] if "Vegetarian" in i.get("tags", []) else [])
            mi = {"@type": "MenuItem", "name": i["name"], "description": i.get("description", ""),
                  "offers": {"@type": "Offer", "price": i["price"], "priceCurrency": "USD"}, "suitableForDiet": diets}
            if i.get("image"):
                mi["image"] = f"{TARGET['url']}/img/menu/{i['image']}.webp"
            items.append(mi)
        sections.append({"@type": "MenuSection", "name": c["name"], "hasMenuItem": items})
    return {"@context": "https://schema.org", "@type": "Menu", "name": f"{SITE['name']} menu",
            "url": f"{TARGET['url']}/menu/", "inLanguage": "en-US", "hasMenuSection": sections,
            "provider": {"@id": f"{TARGET['url']}/#restaurant"}}


def ld_script(data: dict) -> str:
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False).replace("</", "<\\/") + "</script>"


# ---------------------------------------------------------------- layout
CURRENT = ' aria-current="page"'
NOOPENER = ' rel="noopener"'
NAV = [("menu/", "Menu", "menu"), ("menu/#trays", "Catering", "catering"), ("about/", "About", "about"), ("contact/", "Contact", "contact")]


def header(rel: str, current: str) -> str:
    links = "".join(
        f'<li><a href="{rel}{href}"{CURRENT if key == current else ""}>{label}</a></li>'
        for href, label, key in NAV)
    return f"""<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="container header-inner">
    <a class="brand" href="{rel or './'}" aria-label="{e(SITE['name'])}, home">
      <img src="{rel}img/brand/icon.webp" width="40" height="42" alt="">
      <span class="brand-text"><span class="brand-name">{e(SITE['name'])}</span><span class="brand-tag">{e(SITE['tagline'])}</span></span>
    </a>
    <nav class="site-nav" id="site-nav" aria-label="Main">
      <ul>{links}</ul>
    </nav>
    <div class="header-actions">
      <a class="btn btn-primary btn-sm header-call" href="{TEL}" aria-label="Call to order: {e(SITE['phone']['display'])}">{icon('phone')}<span>Call to order</span></a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Open menu">{icon('menu', 'icon icon-open')}{icon('close', 'icon icon-close')}</button>
    </div>
  </div>
</header>"""


def footer(rel: str) -> str:
    social = "".join(
        f'<a class="social" href="{e(u)}" rel="noopener" aria-label="{e(SITE["name"])} on {k.title()}">{icon(k)}</a>'
        for k, u in SITE["social"].items() if not k.startswith("_") and u)
    return f"""<footer class="site-footer">
  <div class="container footer-grid">
    <div class="footer-brand">
      <a class="brand brand-light" href="{rel or './'}"><img src="{rel}img/brand/icon.webp" width="40" height="42" alt=""><span class="brand-text"><span class="brand-name">{e(SITE['name'])}</span><span class="brand-tag">{e(SITE['tagline'])}</span></span></a>
      <p>{e(SITE['summary'])}</p>
      <p class="halal-line"><img src="{rel}img/brand/halal.webp" width="40" height="42" alt="">100% halal</p>
    </div>
    <div>
      <h2 class="footer-h">Visit</h2>
      <p><a href="{e(SITE['mapsUrl'])}" rel="noopener">{e(address_line())}</a></p>
      <p>{e(SITE['hoursLabel'])}</p>
      <p class="open-status" data-open-status><span class="dot" aria-hidden="true"></span><span class="status-text">{e(SITE['hoursLabel'])}</span></p>
    </div>
    <div>
      <h2 class="footer-h">Order &amp; contact</h2>
      <ul class="footer-list">
        <li><a href="{TEL}">{icon('phone')}{e(SITE['phone']['display'])}</a></li>
        <li><a href="{WA}" rel="noopener">{icon('chat')}WhatsApp</a></li>
        <li><a href="{MAIL}">{icon('mail')}{e(SITE['email'])}</a></li>
      </ul>
      {f'<div class="social-row">{social}</div>' if social else ''}
    </div>
    <div>
      <h2 class="footer-h">Explore</h2>
      <ul class="footer-list">
        <li><a href="{rel or './'}">Home</a></li>
        <li><a href="{rel}menu/">Menu</a></li>
        <li><a href="{rel}menu/#trays">Party trays</a></li>
        <li><a href="{rel}about/">About</a></li>
        <li><a href="{rel}contact/">Contact</a></li>
      </ul>
    </div>
  </div>
  <div class="container footer-base">
    <p>© <span data-year>{dt.date.today().year}</span> {e(SITE['name'])}. Prices and hours may change; call to confirm.</p>
  </div>
</footer>"""


def page(path: str, title: str, description: str, body: str, *, current: str = "", rel: str | None = None,
         ld: list[dict] | None = None, robots: str = "index,follow", body_class: str = "") -> str:
    depth = path.count("/")
    rel = ("../" * depth) if rel is None else rel
    canonical = f"{TARGET['url']}/{path}"
    full_title = title if SITE["name"] in title else f"{title} | {SITE['name']}"
    hours_attr = e(json.dumps(SITE["hours"], separators=(",", ":")))
    ld_html = "\n".join(ld_script(x) for x in (ld or []))
    if TARGET["preview"]:
        robots = "noindex,nofollow"
    banner = (f'<p class="preview-bar" role="note">Preview of the new {e(SITE["name"])} website. '
              f'It is not live yet, so call {e(SITE["phone"]["display"])} to confirm prices and hours.</p>\n') if TARGET["preview"] else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>document.documentElement.classList.add('js')</script>
<title>{e(full_title)}</title>
<meta name="description" content="{e(description)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#860E10">
<meta property="og:type" content="restaurant.restaurant">
<meta property="og:site_name" content="{e(SITE['name'])}">
<meta property="og:title" content="{e(full_title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{TARGET['url']}/img/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{rel}favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="{rel}favicon-32.png">
<link rel="apple-touch-icon" href="{rel}apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&amp;family=Inter:wght@400;500;600;700&amp;display=swap">
<link rel="stylesheet" href="{rel}css/styles.css">
<script src="{rel}js/main.js" defer></script>
{ld_html}
</head>
<body class="{body_class}" data-hours="{hours_attr}" data-tz="{e(SITE['timezone'])}">
{banner}{header(rel, current)}
<main id="main">
{body}
</main>
{footer(rel)}
</body>
</html>
"""


# ---------------------------------------------------------------- components
def webp_size(path: Path) -> tuple[int, int]:
    """Width and height from a WebP header, so <img> reserves the right space (no layout jump)."""
    b = path.read_bytes()[:30]
    if b[:4] != b"RIFF" or b[8:12] != b"WEBP":
        raise ValueError(f"{path} is not a WebP file")
    kind = b[12:16]
    if kind == b"VP8X":
        return 1 + int.from_bytes(b[24:27], "little"), 1 + int.from_bytes(b[27:30], "little")
    if kind == b"VP8L":
        bits = int.from_bytes(b[21:25], "little")
        return (bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1
    if kind == b"VP8 ":
        return int.from_bytes(b[26:28], "little") & 0x3FFF, int.from_bytes(b[28:30], "little") & 0x3FFF
    raise ValueError(f"{path}: unknown WebP chunk {kind!r}")


def dish_img(rel: str, item: dict, eager: bool = False) -> str:
    w, h = webp_size(ROOT / f"static/img/menu/{item['image']}.webp")
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (f'<img src="{rel}img/menu/{item["image"]}.webp" width="{w}" height="{h}" '
            f'alt="{e(item["name"])}" {load}>')


def dish_card(rel: str, item: dict) -> str:
    media = f'<div class="dish-media">{dish_img(rel, item)}</div>' if item.get("image") else ""
    serves = f'<p class="dish-serves">Serves {e(item["serves"])}</p>' if item.get("serves") else ""
    opts = ""
    if item.get("options"):
        opts = '<ul class="dish-options" aria-label="Options">' + "".join(
            f'<li>{e(o["name"])} <b>{"+" if o.get("addon") else ""}{money(o["price"])}</b></li>' for o in item["options"]) + "</ul>"
    tags = "".join(f'<span class="tag">{e(t)}</span>' for t in item.get("tags", []))
    return f"""<article class="dish{'' if media else ' dish--text'}" id="{e(item['id'])}">
  {media}
  <div class="dish-body">
    <div class="dish-head"><h3>{e(item['name'])}</h3><span class="price">{money(item['price'])}</span></div>
    {serves}<p class="dish-desc">{e(item.get('description', ''))}</p>
    {opts}{f'<div class="tags">{tags}</div>' if tags else ''}
  </div>
</article>"""


def price_list(items: list[dict]) -> str:
    rows = "".join(
        f'<li id="{e(i["id"])}"><span class="pl-name">{e(i["name"])}<small>{e(i.get("description", ""))}</small></span>'
        f'<span class="pl-dots" aria-hidden="true"></span><span class="price">{money(i["price"])}</span></li>' for i in items)
    return f'<ul class="price-list">{rows}</ul>'


def order_buttons(extra_cls: str = "") -> str:
    return f"""<div class="cta-row {extra_cls}">
  <a class="btn btn-primary" href="{TEL}">{icon('phone')}Call {e(SITE['phone']['display'])}</a>
  <a class="btn btn-ghost" href="{WA}" rel="noopener">{icon('chat')}Message on WhatsApp</a>
</div>"""


def visit_section(rel: str, heading_level: str = "h2") -> str:
    h = heading_level
    return f"""<section class="section visit" aria-labelledby="visit-h">
  <div class="container visit-grid">
    <div class="visit-card">
      <p class="eyebrow">Find us</p>
      <{h} id="visit-h" class="section-title">Come hungry</{h}>
      <ul class="info-list">
        <li>{icon('pin')}<div><strong>{e(address_line())}</strong><a class="link-arrow" href="{e(SITE['mapsUrl'])}" rel="noopener">Get directions {icon('arrow')}</a></div></li>
        <li>{icon('clock')}<div><strong>{e(SITE['hoursLabel'])}</strong><span class="open-status" data-open-status><span class="dot" aria-hidden="true"></span><span class="status-text">Dine in or take out</span></span></div></li>
        <li>{icon('phone')}<div><strong><a href="{TEL}">{e(SITE['phone']['display'])}</a></strong><span>Call ahead and we'll have it ready.</span></div></li>
      </ul>
    </div>
    <div class="map-frame" data-map-src="{e(MAP_EMBED)}" data-map-title="Map showing {e(SITE['name'])} at {e(address_line())}">
      <div class="map-facade">
        {icon('pin', 'icon map-pin')}
        <p class="map-address">{e(address_line())}</p>
        <div class="cta-row">
          <button class="btn btn-primary btn-sm" type="button" data-load-map hidden>Show map</button>
          <a class="btn btn-ghost btn-sm" href="{e(SITE['mapsUrl'])}" rel="noopener">Open in Google Maps</a>
        </div>
        <p class="map-note">The map loads from Google only when you ask for it.</p>
      </div>
    </div>
  </div>
</section>"""


# ---------------------------------------------------------------- pages
def home() -> str:
    rel = ""
    hero_item = ITEMS["mix-grill-over-rice"]
    sig = "".join(
        f"""<li class="sig-card">
  <a href="menu/#{e(i['id'])}">
    <div class="sig-media">{dish_img(rel, i)}</div>
    <h3>{e(i['name'])}</h3>
    <p>{e(i['description'])}</p>
    <span class="price">{money(i['price'])}</span>
  </a>
</li>""" for i in (ITEMS[x] for x in SITE["signature"]))
    values = "".join(
        f'<li class="value">{icon(v["icon"], "icon icon-lg")}<h3>{e(v["title"])}</h3><p>{e(v["text"])}</p></li>' for v in SITE["values"])
    trays = [ITEMS["party-tray-1"], ITEMS["party-tray-2"]]
    tray_cards = "".join(
        f"""<li class="tray-card">
  {dish_img(rel, t)}
  <div><h3>{e(t['name'])}</h3><p class="dish-serves">Serves {e(t['serves'])}</p><span class="price">{money(t['price'])}</span></div>
</li>""" for t in trays)
    body = f"""<section class="hero">
  <div class="container hero-grid">
    <div class="hero-copy">
      <p class="eyebrow eyebrow-badge"><img src="img/brand/halal.webp" width="28" height="29" alt="">100% halal · {e(SITE['address']['city'])}, {e(SITE['address']['region'])}</p>
      <h1>Tastes like home.</h1>
      <p class="lead">Authentic Middle Eastern shawarma, kabab and falafel, made fresh every day at {e(SITE['address']['street'])} in {e(SITE['address']['city'])}.</p>
      <div class="cta-row">
        <a class="btn btn-primary btn-lg" href="menu/">See the menu {icon('arrow')}</a>
        <a class="btn btn-ghost btn-lg" href="{TEL}">{icon('phone')}{e(SITE['phone']['display'])}</a>
      </div>
      <p class="open-status hero-status" data-open-status><span class="dot" aria-hidden="true"></span><span class="status-text">{e(SITE['hoursLabel'])}</span></p>
    </div>
    <div class="hero-art">
      <div class="arch" aria-hidden="true"></div>
      {dish_img(rel, hero_item, eager=True)}
      <p class="hero-tag"><span>{e(hero_item['name'])}</span><strong>{money(hero_item['price'])}</strong></p>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="sig-h">
  <div class="container">
    <div class="section-head">
      <p class="eyebrow">House favorites</p>
      <h2 id="sig-h" class="section-title">Off the grill, over rice</h2>
      <p class="section-lead">Every platter comes over our seasoned Mediterranean rice.</p>
    </div>
    <ul class="sig-grid">{sig}</ul>
    <p class="center"><a class="link-arrow" href="menu/">See all {len(ITEMS)} items on the menu {icon('arrow')}</a></p>
  </div>
</section>

<section class="section section-tint" aria-labelledby="why-h">
  <div class="container">
    <div class="section-head">
      <p class="eyebrow">Why Beit Shawarma</p>
      <h2 id="why-h" class="section-title">Beit means home</h2>
      <p class="section-lead">Beit is Arabic for home. That is the promise on every plate.</p>
    </div>
    <ul class="values">{values}</ul>
  </div>
</section>

<section class="catering" aria-labelledby="cater-h">
  <div class="container catering-grid">
    <div>
      <p class="eyebrow eyebrow-light">Catering</p>
      <h2 id="cater-h" class="section-title">Feeding a crowd?</h2>
      <p class="section-lead">Party trays come loaded with kofta, kabab, beef and chicken shawarma over rice, salad, hummus, baba ghanoush and grilled vegetables. Trays need at least 45 minutes, so call ahead.</p>
      {order_buttons('cta-light')}
    </div>
    <ul class="tray-list">{tray_cards}</ul>
  </div>
</section>

{visit_section(rel)}
"""
    return page("", f"{SITE['name']} | Halal Shawarma & Middle Eastern Food in {SITE['address']['city']}, {SITE['address']['region']}",
                f"{SITE['name']} serves authentic, 100% halal Middle Eastern food in {SITE['address']['city']}, {SITE['address']['region']}: shawarma, kabab, falafel and party trays. Open {SITE['hoursLabel'].lower()}.",
                body, current="home", ld=[restaurant_ld()], body_class="page-home")


def menu_page() -> str:
    rel = "../"
    chips = "".join(f'<li><a href="#{e(c["id"])}">{e(c["name"])}</a></li>' for c in MENU["categories"])
    sections = []
    for c in MENU["categories"]:
        blurb = f'<p class="menu-blurb">{e(c["blurb"])}</p>' if c.get("blurb") else ""
        inner = price_list(c["items"]) if c.get("compact") else '<div class="dish-grid">' + "".join(dish_card(rel, i) for i in c["items"]) + "</div>"
        sections.append(f"""<section class="menu-section" id="{e(c['id'])}" aria-labelledby="{e(c['id'])}-h">
  <div class="menu-section-head"><h2 id="{e(c['id'])}-h">{e(c['name'])}</h2>{blurb}</div>
  {inner}
</section>""")
    body = f"""<section class="page-hero">
  <div class="container">
    <p class="eyebrow eyebrow-badge"><img src="../img/brand/halal.webp" width="28" height="29" alt="">100% halal</p>
    <h1>Our menu</h1>
    <p class="lead">{e(MENU['note'])}</p>
    {order_buttons()}
  </div>
</section>
<nav class="menu-nav" aria-label="Menu sections">
  <div class="container"><ul class="chips">{chips}</ul></div>
</nav>
<div class="container menu-body">
{''.join(sections)}
<aside class="menu-cta">
  <h2>Ready to order?</h2>
  <p>Call us and your food will be ready when you arrive. {e(SITE['hoursLabel'])}.</p>
  {order_buttons()}
</aside>
</div>
"""
    return page("menu/", f"Menu: Shawarma, Kabab, Falafel & Party Trays",
                f"The full {SITE['name']} menu with prices: shawarma and kabab platters over rice, sandwiches, hummus, salads, party trays for 4–10 people, drinks and desserts. 100% halal.",
                body, current="menu", ld=[menu_ld()], body_class="page-menu")


def about_page() -> str:
    rel = "../"
    paras = "".join(f"<p>{e(p)}</p>" for p in SITE["about"])
    values = "".join(
        f'<li class="value">{icon(v["icon"], "icon icon-lg")}<h3>{e(v["title"])}</h3><p>{e(v["text"])}</p></li>' for v in SITE["values"])
    gallery = "".join(f'<li>{dish_img(rel, ITEMS[x])}</li>' for x in ("shish-tawook-over-rice", "hummus", "fattoush", "falafel-sandwich"))
    body = f"""<section class="page-hero">
  <div class="container narrow">
    <p class="eyebrow">About us</p>
    <h1>Beit means home</h1>
    <p class="lead">Beit is Arabic for home, and &ldquo;{e(SITE['tagline'])}&rdquo; is the standard we cook to.</p>
  </div>
</section>
<section class="section">
  <div class="container about-grid">
    <div class="prose">
      <img class="about-logo" src="../img/brand/logo.webp" width="382" height="414" alt="{e(SITE['name'])} logo: a shawarma spit inside an arched doorway, with the words Tastes Like Home">
      {paras}
      {order_buttons()}
    </div>
    <ul class="gallery">{gallery}</ul>
  </div>
</section>
<section class="section section-tint" aria-labelledby="values-h">
  <div class="container">
    <div class="section-head"><h2 id="values-h" class="section-title">What we stand for</h2></div>
    <ul class="values">{values}</ul>
  </div>
</section>
{visit_section(rel)}
"""
    return page("about/", "About Us", f"About {SITE['name']}: authentic Middle Eastern food in {SITE['address']['city']}, {SITE['address']['region']}, made fresh daily with high-quality, 100% halal ingredients.",
                body, current="about", ld=[restaurant_ld()], body_class="page-about")


def contact_page() -> str:
    rel = "../"
    cards = [
        ("phone", "Call", SITE["phone"]["display"], TEL, "Fastest way to order"),
        ("chat", "WhatsApp", SITE["phone"]["display"], WA, "Message us any time"),
        ("mail", "Email", SITE["email"], MAIL, "For catering and questions"),
        ("nav", "Visit", address_line(), SITE["mapsUrl"], "Get directions"),
    ]
    card_html = "".join(
        f'<li><a class="contact-card" href="{e(href)}"{NOOPENER if href.startswith("http") else ""}>{icon(ic, "icon icon-lg")}'
        f'<span class="cc-label">{e(label)}</span><span class="cc-value">{e(value)}</span><span class="cc-note">{e(note)}</span></a></li>'
        for ic, label, value, href, note in cards)
    body = f"""<section class="page-hero">
  <div class="container narrow">
    <p class="eyebrow">Contact</p>
    <h1>Get in touch</h1>
    <p class="lead">Questions, catering orders or feedback: call, message or stop by. {e(SITE['hoursLabel'])}.</p>
    <p class="open-status" data-open-status><span class="dot" aria-hidden="true"></span><span class="status-text">{e(SITE['hoursLabel'])}</span></p>
  </div>
</section>
<section class="section section-tight">
  <div class="container">
    <ul class="contact-cards">{card_html}</ul>
  </div>
</section>
<section class="section section-tint" aria-labelledby="msg-h">
  <div class="container form-grid">
    <div>
      <h2 id="msg-h" class="section-title">Send us a message</h2>
      <p class="section-lead">Write your message here and send it with WhatsApp or your email app. Nothing is stored on this website.</p>
      <p class="section-lead">Ordering a party tray? Tell us which tray, how many people and the pickup time. Trays need at least 45 minutes.</p>
    </div>
    <form class="composer" action="{MAIL}" method="post" enctype="text/plain" data-composer data-wa="{WA}" data-mail="{SITE['email']}">
      <label for="f-name">Your name</label>
      <input id="f-name" name="name" autocomplete="name" required>
      <label for="f-topic">Topic</label>
      <select id="f-topic" name="topic">
        <option>General question</option>
        <option>Party tray / catering</option>
        <option>Feedback</option>
      </select>
      <label for="f-msg">Message</label>
      <textarea id="f-msg" name="message" rows="5" required></textarea>
      <div class="cta-row">
        <button class="btn btn-primary" type="submit" name="via" value="whatsapp">{icon('chat')}Send on WhatsApp</button>
        <button class="btn btn-ghost" type="submit" name="via" value="email">{icon('mail')}Send by email</button>
      </div>
      <p class="form-status" role="status" aria-live="polite"></p>
    </form>
  </div>
</section>
{visit_section(rel)}
"""
    return page("contact/", "Contact & Directions", f"Contact {SITE['name']} at {address_line()}. Call {SITE['phone']['display']}, message us on WhatsApp or email {SITE['email']}. Open {SITE['hoursLabel'].lower()}.",
                body, current="contact", ld=[restaurant_ld()], body_class="page-contact")


def not_found() -> str:
    body = f"""<section class="page-hero page-404">
  <div class="container narrow">
    <p class="eyebrow">Page not found</p>
    <h1>This page left the grill</h1>
    <p class="lead">The page you were looking for isn't here, but the food still is.</p>
    <div class="cta-row"><a class="btn btn-primary" href="{TARGET['base']}menu/">See the menu</a><a class="btn btn-ghost" href="{TARGET['base']}">Go home</a></div>
  </div>
</section>"""
    return page("404.html", "Page not found", f"This page could not be found. See the {SITE['name']} menu.", body, rel=TARGET["base"], robots="noindex")


def legacy_redirect() -> str:
    # The old Angular site lived at /home; keep that link (on Google, menus, flyers) working.
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>{e(SITE['name'])}</title>
<meta name="robots" content="noindex"><link rel="canonical" href="{TARGET['url']}/">
<meta http-equiv="refresh" content="0; url=../"></head>
<body><p><a href="../">Continue to {e(SITE['name'])}</a></p></body></html>
"""


PAGES = {"index.html": home, "menu/index.html": menu_page, "about/index.html": about_page,
         "contact/index.html": contact_page, "404.html": not_found, "home/index.html": legacy_redirect}


def build(out: Path) -> None:
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(ROOT / "static", out)
    for rel_path, fn in PAGES.items():
        dest = out / rel_path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(fn(), encoding="utf-8")
    urls = ["", "menu/", "about/", "contact/"]
    (out / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{TARGET['url']}/{u}</loc></url>\n" for u in urls) + "</urlset>\n", encoding="utf-8")
    if TARGET["preview"]:
        (out / "robots.txt").write_text("User-agent: *\nDisallow: /\n", encoding="utf-8")
        (out / "sitemap.xml").unlink()
        return  # no CNAME: a preview must not claim the restaurant's domain
    (out / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {TARGET['url']}/sitemap.xml\n", encoding="utf-8")
    if SITE["url"].startswith("https://www."):
        (out / "CNAME").write_text(SITE["url"].removeprefix("https://") + "\n", encoding="utf-8")


def validate() -> list[str]:
    """Content mistakes that would ship a broken page."""
    problems = []
    for c in MENU["categories"]:
        for i in c["items"]:
            try:
                float(i["price"])
            except (KeyError, ValueError):
                problems.append(f"{i.get('id')}: price must be a number like \"9.99\"")
            if i.get("image") and not (ROOT / f"static/img/menu/{i['image']}.webp").exists():
                problems.append(f"{i['id']}: image static/img/menu/{i['image']}.webp not found")
    for sid in SITE["signature"]:
        if sid not in ITEMS:
            problems.append(f"site.json signature: no menu item with id {sid!r}")
    return problems


def same_tree(a: Path, b: Path) -> list[str]:
    diffs = []
    cmp = filecmp.dircmp(a, b)
    def walk(d: filecmp.dircmp, prefix: str = "") -> None:
        diffs.extend(prefix + n for n in d.left_only + d.right_only + d.diff_files)
        _, mismatch, errors = filecmp.cmpfiles(d.left, d.right, d.common_files, shallow=False)
        diffs.extend(prefix + n for n in mismatch + errors if prefix + n not in diffs)
        for name, sub in d.subdirs.items():
            walk(sub, f"{prefix}{name}/")
    walk(cmp)
    return sorted(set(diffs))


def main() -> int:
    ap = argparse.ArgumentParser(description="Build the Beit Shawarma site into site/.")
    ap.add_argument("--check", action="store_true", help="fail if site/ (or the --preview --out folder) is stale")
    ap.add_argument("--preview", metavar="BASE_URL",
                    help="build a noindex preview served at BASE_URL (e.g. https://bamr87.github.io/beit-shawarma) into --out")
    ap.add_argument("--out", type=Path, help="output folder for --preview (never site/)")
    args = ap.parse_args()
    if args.preview:
        if not args.out or args.out.resolve() == (ROOT / "site").resolve():
            ap.error("--preview needs --out pointing somewhere other than site/ (site/ is the production build)")
        url = args.preview.rstrip("/")
        TARGET.update(url=url, base=(urlparse(url).path.rstrip("/") + "/"), preview=True)
    problems = validate()
    if problems:
        print("Content problems:\n  " + "\n  ".join(problems), file=sys.stderr)
        return 1
    out = args.out if args.preview else ROOT / "site"
    if args.check:
        with tempfile.TemporaryDirectory() as tmp:
            fresh = Path(tmp) / "out"
            build(fresh)
            diffs = same_tree(fresh, out) if out.exists() else [f"{out} missing"]
        if diffs:
            fix = "python3 build.py" + (f" --preview {TARGET['url']} --out {args.out}" if TARGET["preview"] else "")
            print(f"{out} is out of date; run: {fix}\n  " + "\n  ".join(diffs), file=sys.stderr)
            return 1
        print(f"{out} is up to date.")
        return 0
    build(out)
    print(f"Built {len(PAGES)} pages and {len(ITEMS)} menu items into {out}"
          + (f" (preview for {TARGET['url']})" if TARGET["preview"] else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
