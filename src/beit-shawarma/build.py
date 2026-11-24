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

Page format (2026-11-24): a dark maroon header under a slim announcement bar, full-width
photo bands, menus as two columns of cream cards, square uppercase buttons, a four-column
dark footer and a quick-actions bar on phones.
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
CATS = {c["id"]: c for c in MENU["categories"]}
# Where the build will be served. Production is the real domain; --preview retargets a copy
# (for example https://bamr87.github.io/beit-shawarma) that search engines are told to skip.
TARGET = {"url": SITE["url"], "base": "/", "preview": False}
DAY_NAMES = {"Mo": "Monday", "Tu": "Tuesday", "We": "Wednesday", "Th": "Thursday", "Fr": "Friday", "Sa": "Saturday", "Su": "Sunday"}
TRAYS = "trays"  # the menu category that gets its own page (catering/)


def e(s: object) -> str:
    return html.escape(str(s), quote=True)


def money(p: str) -> str:
    return f"${float(p):,.2f}"


def address_line() -> str:
    a = SITE["address"]
    tail = f" {a['postalCode']}" if a.get("postalCode") else ""
    return f"{a['street']}, {a['city']}, {a['region']}{tail}"


def address_lines() -> str:
    a = SITE["address"]
    tail = f" {a['postalCode']}" if a.get("postalCode") else ""
    return f"{e(a['street'])}<br>{e(a['city'])}, {e(a['region'])}{e(tail)}"


TEL = f"tel:{SITE['phone']['e164']}"
WA = f"https://wa.me/{SITE['whatsapp']}"
MAIL = f"mailto:{SITE['email']}"
MAP_EMBED = f"https://maps.google.com/maps?q={quote_plus(SITE['mapEmbedQuery'])}&z=16&output=embed"
CURRENT = ' aria-current="page"'
NOOPENER = ' rel="noopener"'

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
    "utensils": '<path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2"/><path d="M7 2v20"/><path d="M21 15V2a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3Zm0 0v7"/>',
    "star": '<path d="m12 2 3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01z"/>',
    "arrow": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "left": '<path d="m15 18-6-6 6-6"/>',
    "right": '<path d="m9 18 6-6-6-6"/>',
    "nav": '<path d="m3 11 19-9-9 19-2-8-8-2z"/>',
    "menu": '<path d="M4 6h16M4 12h16M4 18h16"/>',
    "close": '<path d="M18 6 6 18M6 6l12 12"/>',
    "facebook": '<path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>',
    "instagram": '<rect x="2" y="2" width="20" height="20" rx="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><path d="M17.5 6.5h.01"/>',
}


def icon(name: str, cls: str = "icon") -> str:
    return (f'<svg class="{cls}" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


# ---------------------------------------------------------------- images
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


def img(rel: str, path: str, alt: str, *, cls: str = "", eager: bool = False, priority: bool = False) -> str:
    """An <img> for static/<path>, with its real width and height. Lazy unless it is on the first screen
    (eager); `priority` marks the one image the first screen is built around."""
    w, h = webp_size(ROOT / "static" / path)
    load = 'fetchpriority="high"' if priority else ("" if eager else 'loading="lazy" decoding="async"')
    klass = f' class="{cls}"' if cls else ""
    return f'<img{klass} src="{rel}{path}" width="{w}" height="{h}" alt="{e(alt)}" {load}>'


def dish_img(rel: str, item: dict, *, cls: str = "", eager: bool = False, priority: bool = False,
             decorative: bool = False) -> str:
    return img(rel, f"img/menu/{item['image']}.webp", "" if decorative else item["name"], cls=cls,
               eager=eager, priority=priority)


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


# ---------------------------------------------------------------- shell: announcement, header, footer
NAV = [("menu/", "Menu", "menu"), ("catering/", "Catering", "catering"), ("about/", "About", "about"), ("contact/", "Contact", "contact")]


def announcement(rel: str) -> str:
    a = SITE["announcement"]
    if TARGET["preview"]:
        text = (f'<strong class="announce-tag">Preview</strong> The new {e(SITE["name"])} website is not live yet. '
                f'Call {e(SITE["phone"]["display"])} to confirm prices and hours.')
        cls = " announce--preview"
    else:
        text, cls = e(a["text"]), ""
    return (f'<aside class="announce{cls}" aria-label="Announcement"><div class="container announce-inner"><p>{text}</p>'
            f'<a class="announce-btn" href="{rel}{e(a["href"])}">{e(a["label"])}</a></div></aside>')


def header(rel: str, current: str) -> str:
    links = "".join(
        f'<li><a href="{rel}{href}"{CURRENT if key == current else ""}>{label}</a></li>' for href, label, key in NAV)
    return f"""<a class="skip-link" href="#main">Skip to content</a>
{announcement(rel)}
<header class="site-header">
  <div class="container header-inner">
    <a class="brand" href="{rel or './'}" aria-label="{e(SITE['name'])}, home">
      {img(rel, 'img/brand/icon-cream.webp', '', cls='brand-icon', eager=True)}
      <span class="brand-text"><span class="brand-name">{e(SITE['name'])}</span><span class="brand-tag">{e(SITE['tagline'])}</span></span>
    </a>
    <nav class="site-nav" id="site-nav" aria-label="Main">
      <ul>{links}</ul>
    </nav>
    <a class="btn btn-accent btn-sm header-order" href="{TEL}" aria-label="Call to order: {e(SITE['phone']['display'])}">{icon('phone')}<span>Call to order</span></a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Open menu">{icon('menu', 'icon icon-open')}{icon('close', 'icon icon-close')}</button>
  </div>
</header>"""


def social_links() -> str:
    return "".join(
        f'<a class="social" href="{e(u)}" rel="noopener" aria-label="{e(SITE["name"])} on {k.title()}">{icon(k)}</a>'
        for k, u in SITE["social"].items() if not k.startswith("_") and u)


def footer(rel: str) -> str:
    social = social_links()
    return f"""<footer class="site-footer">
  <div class="container footer-grid">
    <div>
      <h2 class="footer-h">Location</h2>
      <p>{e(SITE['name'])}<br>{address_lines()}</p>
      <p><a class="footer-link" href="{e(SITE['mapsUrl'])}" rel="noopener">{icon('pin')}Get directions</a></p>
    </div>
    <div>
      <h2 class="footer-h">Hours</h2>
      <p>{e(SITE['hoursLabel'])}</p>
      <p class="open-status" data-open-status><span class="dot" aria-hidden="true"></span><span class="status-text">{e(SITE['hoursLabel'])}</span></p>
    </div>
    <div>
      <h2 class="footer-h">Order</h2>
      <ul class="footer-list">
        <li><a class="footer-link" href="{TEL}">{icon('phone')}Call {e(SITE['phone']['display'])}</a></li>
        <li><a class="footer-link" href="{WA}" rel="noopener">{icon('chat')}WhatsApp</a></li>
        <li><a class="footer-link" href="{rel}catering/">{icon('tray')}Party trays</a></li>
      </ul>
      {f'<div class="social-row">{social}</div>' if social else ''}
    </div>
    <div>
      <h2 class="footer-h">Contact us</h2>
      <ul class="footer-list">
        <li><a class="footer-link" href="{MAIL}">{icon('mail')}{e(SITE['email'])}</a></li>
        <li><a class="footer-link" href="{rel}contact/">{icon('chat')}Send a message</a></li>
      </ul>
      <p class="halal-line">{img(rel, 'img/brand/halal.webp', '')}100% halal</p>
    </div>
  </div>
  <div class="footer-base">
    <div class="container footer-base-inner">
      <p>© <span data-year>{dt.date.today().year}</span> {e(SITE['name'])}. Prices and hours may change; call to confirm.</p>
      <ul class="footer-nav">
        <li><a href="{rel or './'}">Home</a></li>{''.join(f'<li><a href="{rel}{href}">{label}</a></li>' for href, label, _ in NAV)}
      </ul>
    </div>
  </div>
</footer>
<nav class="quickbar" aria-label="Quick actions">
  <a href="{TEL}">{icon('phone')}<span>Call</span></a>
  <a href="{rel}menu/">{icon('utensils')}<span>Menu</span></a>
  <a href="{rel}catering/">{icon('tray')}<span>Trays</span></a>
  <a href="{e(SITE['mapsUrl'])}" rel="noopener">{icon('nav')}<span>Directions</span></a>
</nav>"""


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
<meta name="theme-color" content="#3a0e10">
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
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Jost:wght@400;500;600;700&amp;family=PT+Sans:ital,wght@0,400;0,700;1,400&amp;display=swap">
<link rel="stylesheet" href="{rel}css/styles.css">
<script src="{rel}js/main.js" defer></script>
{ld_html}
</head>
<body class="{body_class}" data-hours="{hours_attr}" data-tz="{e(SITE['timezone'])}">
{header(rel, current)}
<main id="main">
{body}
</main>
{footer(rel)}
</body>
</html>
"""


# ---------------------------------------------------------------- components
def buttons(*items: tuple[str, str, str, str]) -> str:
    """(style, href, icon name or '', label) -> a row of square uppercase buttons."""
    out = []
    for style, href, ic, label in items:
        ext = NOOPENER if href.startswith("http") else ""
        out.append(f'<a class="btn btn-{style}" href="{e(href)}"{ext}>{icon(ic) if ic else ""}{label}</a>')
    return '<div class="cta-row">' + "".join(out) + "</div>"


def page_head(title: str, lead: str = "", extra: str = "", eyebrow: str = "") -> str:
    """The light, centred title band that opens every inner page."""
    eb = f'<p class="eyebrow">{eyebrow}</p>' if eyebrow else ""
    ld = f'<p class="lead">{lead}</p>' if lead else ""
    return f"""<section class="page-head">
  <div class="container narrow">
    {eb}<h1>{title}</h1>
    {ld}{extra}
  </div>
</section>"""


def options_html(item: dict) -> str:
    if not item.get("options"):
        return ""
    return '<ul class="mi-options" aria-label="Options">' + "".join(
        f'<li>{e(o["name"])} <b>{"+" if o.get("addon") else ""}{money(o["price"])}</b></li>' for o in item["options"]) + "</ul>"


def tags_html(item: dict) -> str:
    tags = "".join(f'<span class="tag">{e(t)}</span>' for t in item.get("tags", []))
    return f'<div class="tags">{tags}</div>' if tags else ""


def menu_item(rel: str, item: dict) -> str:
    thumb = f'<div class="mi-thumb">{dish_img(rel, item, decorative=True)}</div>' if item.get("image") else ""
    desc = f'<p class="mi-desc">{e(item["description"])}</p>' if item.get("description") else ""
    return f"""<li class="menu-item{'' if thumb else ' menu-item--text'}" id="{e(item['id'])}">
  {thumb}<div class="mi-body">
    <div class="mi-head"><h3 class="mi-name">{e(item['name'])}</h3><span class="price">{money(item['price'])}</span></div>
    {desc}{options_html(item)}{tags_html(item)}
  </div>
</li>"""


def menu_card(rel: str, cat: dict) -> str:
    blurb = f'<p class="card-blurb">{e(cat["blurb"])}</p>' if cat.get("blurb") else ""
    rows = "".join(menu_item(rel, i) for i in cat["items"])
    return f"""<section class="menu-card" id="{e(cat['id'])}" aria-labelledby="{e(cat['id'])}-h">
  <h2 id="{e(cat['id'])}-h">{e(cat['name'])}</h2>{blurb}
  <ul class="menu-list">{rows}</ul>
</section>"""


def tray_card(rel: str, item: dict, level: str = "h3") -> str:
    contents = "".join(f"<li>{e(part.strip().rstrip('.'))}</li>" for part in item["description"].split(","))
    return f"""<article class="tray-card" id="{e(item['id'])}">
  <div class="tray-media">{dish_img(rel, item)}</div>
  <div class="tray-body">
    <div class="mi-head"><{level} class="tray-name">{e(item['name'])}</{level}><span class="price">{money(item['price'])}</span></div>
    <p class="tray-serves">Serves {e(item['serves'])}</p>
    <ul class="tray-contents" aria-label="What's in {e(item['name'])}">{contents}</ul>
  </div>
</article>"""


def open_status(text: str) -> str:
    return f'<p class="open-status" data-open-status><span class="dot" aria-hidden="true"></span><span class="status-text">{e(text)}</span></p>'


def visit_section(rel: str) -> str:
    return f"""<section class="visit" aria-labelledby="visit-h">
  <div class="visit-info">
    <div class="visit-inner">
      <p class="eyebrow">Find us</p>
      <h2 id="visit-h" class="section-title">Come hungry</h2>
      <ul class="info-list">
        <li>{icon('pin')}<div><strong>{e(address_line())}</strong><span>Dine in or take out</span></div></li>
        <li>{icon('clock')}<div><strong>{e(SITE['hoursLabel'])}</strong>{open_status(SITE['hoursLabel'])}</div></li>
        <li>{icon('phone')}<div><strong><a href="{TEL}">{e(SITE['phone']['display'])}</a></strong><span>Call ahead and we'll have it ready.</span></div></li>
      </ul>
      {buttons(('accent', SITE['mapsUrl'], 'nav', 'Get directions'), ('outline', TEL, 'phone', 'Call us'))}
    </div>
  </div>
  <div class="map-frame">
    <template data-map-template><iframe src="{e(MAP_EMBED)}" title="Map showing {e(SITE['name'])} at {e(address_line())}" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></template>
    <div class="map-facade">
      {icon('pin', 'icon map-pin')}
      <p class="map-address">{e(address_line())}</p>
      <div class="cta-row">
        <button class="btn btn-dark btn-sm" type="button" data-load-map hidden>Show map</button>
        <a class="btn btn-outline btn-sm" href="{e(SITE['mapsUrl'])}" rel="noopener">Open in Google Maps</a>
      </div>
      <p class="map-note">The map loads from Google only when you ask for it.</p>
    </div>
  </div>
</section>"""


def reviews_band(rel: str) -> str:
    return f"""<section class="band band-dark reviews" aria-labelledby="reviews-h">
  <div class="container narrow center">
    <p class="stars" aria-hidden="true">{icon('star')}{icon('star')}{icon('star')}{icon('star')}{icon('star')}</p>
    <h2 id="reviews-h" class="section-title">Reviews</h2>
    <p class="kicker">On Google</p>
    <p class="section-lead">Ate with us? Read what other diners say, and tell them what you thought.</p>
    {buttons(('accent', SITE['mapsUrl'], '', 'Read our reviews'))}
  </div>
</section>"""


def composer_form(form_id: str, fields: str, *, note: str) -> str:
    """A form whose message is sent with WhatsApp or the visitor's email app (main.js); nothing is stored."""
    return f"""<form class="composer" id="{form_id}" action="{MAIL}" method="post" enctype="text/plain" data-composer>
  {fields}
  <div class="cta-row">
    <button class="btn btn-accent" type="submit" name="via" value="whatsapp">{icon('chat')}Send on WhatsApp</button>
    <button class="btn btn-outline" type="submit" name="via" value="email">{icon('mail')}Send by email</button>
  </div>
  <p class="form-note">{note}</p>
  <p class="form-status" role="status" aria-live="polite"></p>
</form>"""


def contact_constant() -> str:
    # Where the message forms send, as a JavaScript constant written at build time. main.js reads
    # this rather than URLs kept in HTML attributes (CodeQL js/xss-through-dom).
    contact = json.dumps({"mail": SITE["email"], "wa": WA}).replace("</", "<\\/")
    return f"<script>window.BEIT_CONTACT = Object.freeze({contact});</script>"


# ---------------------------------------------------------------- pages
def home() -> str:
    rel = ""
    hero = [ITEMS["mix-grill-over-rice"], ITEMS["chicken-shawarma-over-rice"], ITEMS["beef-shawarma-over-rice"]]
    spread = "".join(dish_img(rel, it, cls=f"plate plate-{n}", eager=True, priority=(n == 1)) for n, it in enumerate(hero, 1))
    slides = "".join(f"""<li class="slide">
  <a href="menu/#{e(i['id'])}">
    <div class="slide-media">{dish_img(rel, i, decorative=True)}</div>
    <h3>{e(i['name'])}</h3>
    <p>{e(i['description'])}</p>
    <span class="price">{money(i['price'])}</span>
  </a>
</li>""" for i in (ITEMS[x] for x in SITE["featured"]))
    values = "".join(
        f'<li class="value">{icon(v["icon"], "icon icon-lg")}<h3>{e(v["title"])}</h3><p>{e(v["text"])}</p></li>' for v in SITE["values"])
    trays = "".join(f"""<li class="tray-mini">
  {dish_img(rel, t)}
  <div><h3>{e(t['name'])}</h3><p>Serves {e(t['serves'])}</p><span class="price">{money(t['price'])}</span></div>
</li>""" for t in CATS[TRAYS]["items"])
    soup = ITEMS["lentil-soup"]
    body = f"""<section class="hero" aria-labelledby="hero-h">
  <div class="container hero-grid">
    <div class="hero-copy">
      <p class="eyebrow eyebrow-light">{img(rel, 'img/brand/halal.webp', '', cls='halal-mini', eager=True)}100% halal · {e(SITE['address']['city'])}, {e(SITE['address']['region'])}</p>
      <h1 id="hero-h">Tastes like home.</h1>
      <p class="lead">Authentic Middle Eastern shawarma, kabab and falafel, made fresh every day at {e(SITE['address']['street'])} in {e(SITE['address']['city'])}.</p>
      {buttons(('accent', 'menu/', '', 'See the menu'), ('outline-light', TEL, 'phone', 'Call ' + e(SITE['phone']['display'])))}
      {open_status(SITE['hoursLabel'])}
    </div>
    <div class="hero-spread" aria-hidden="true">{spread}</div>
  </div>
</section>

<section class="band band-maroon order-band" aria-labelledby="order-h">
  <div class="container order-grid">
    <div>
      <h2 id="order-h" class="section-title">Order for pickup</h2>
      <p class="kicker">Call ahead and it's ready when you arrive</p>
      {buttons(('accent', TEL, 'phone', 'Call ' + e(SITE['phone']['display'])), ('accent', WA, 'chat', 'Order on WhatsApp'))}
    </div>
    <div class="order-art">{dish_img(rel, soup, decorative=True)}</div>
  </div>
</section>

<section class="featured" aria-labelledby="featured-h">
  <div class="band band-dark strip">
    <h2 id="featured-h" class="section-title">Off the grill, over rice</h2>
  </div>
  <div class="carousel" data-carousel>
    <button class="carousel-btn carousel-prev" type="button" aria-label="Previous dishes" hidden>{icon('left')}</button>
    <ul class="carousel-track" tabindex="0" aria-label="Featured dishes">{slides}</ul>
    <button class="carousel-btn carousel-next" type="button" aria-label="Next dishes" hidden>{icon('right')}</button>
  </div>
  <div class="center featured-cta">{buttons(('dark', 'menu/', '', 'Our menu'))}</div>
</section>

<section class="band band-light catering-teaser" aria-labelledby="cater-h">
  <div class="container catering-grid">
    <div>
      <p class="eyebrow">Catering</p>
      <h2 id="cater-h" class="section-title">Feeding a crowd?</h2>
      <p class="section-lead">Party trays come loaded with kofta, kabab, beef and chicken shawarma over rice, salad, hummus, baba ghanoush and grilled vegetables. Trays need at least 45 minutes, so call ahead.</p>
      {buttons(('dark', 'catering/', '', 'See party trays'), ('outline', TEL, 'phone', 'Call to order'))}
    </div>
    <ul class="tray-minis">{trays}</ul>
  </div>
</section>

<section class="band values-band" aria-labelledby="why-h">
  <div class="container">
    <div class="section-head">
      <h2 id="why-h" class="section-title">Beit means home</h2>
      <p class="section-lead">Beit is Arabic for home. That is the promise on every plate.</p>
    </div>
    <ul class="values">{values}</ul>
  </div>
</section>

{reviews_band(rel)}

{visit_section(rel)}
"""
    return page("", f"{SITE['name']} | Halal Shawarma & Middle Eastern Food in {SITE['address']['city']}, {SITE['address']['region']}",
                f"{SITE['name']} serves authentic, 100% halal Middle Eastern food in {SITE['address']['city']}, {SITE['address']['region']}: shawarma, kabab, falafel and party trays. Open {SITE['hoursLabel'].lower()}.",
                body, current="home", ld=[restaurant_ld()], body_class="page-home")


def menu_page() -> str:
    rel = "../"
    cats = [c for c in MENU["categories"] if c["id"] != TRAYS]
    chips = "".join(f'<li><a href="#{e(c["id"])}">{e(c["name"])}</a></li>' for c in cats)
    tabs = (f'<nav class="tabs" aria-label="Menu pages"><a class="tab is-active" href="./" aria-current="page">Menu</a>'
            f'<a class="tab" href="../catering/">Party trays</a></nav>')
    body = f"""{page_head('Our Menu', e(MENU['note']), tabs)}
<nav class="menu-nav" aria-label="Menu sections">
  <div class="container"><ul class="chips">{chips}</ul></div>
</nav>
<div class="menu-body">
  <div class="container menu-columns">
    {''.join(menu_card(rel, c) for c in cats)}
  </div>
  <div class="container">
    <aside class="menu-cta">
      <h2>Ready to order?</h2>
      <p>Call us and your food will be ready when you arrive. {e(SITE['hoursLabel'])}.</p>
      {buttons(('accent', TEL, 'phone', 'Call ' + e(SITE['phone']['display'])), ('outline', WA, 'chat', 'Order on WhatsApp'))}
    </aside>
  </div>
</div>
"""
    return page("menu/", "Menu: Shawarma, Kabab, Falafel & More",
                f"The full {SITE['name']} menu with prices: shawarma and kabab platters over rice, sandwiches, hummus, salads, drinks and desserts. 100% halal.",
                body, current="menu", ld=[menu_ld()], body_class="page-menu")


def catering_page() -> str:
    rel = "../"
    cat = CATS[TRAYS]
    tabs = (f'<nav class="tabs" aria-label="Menu pages"><a class="tab" href="../menu/">Menu</a>'
            f'<a class="tab is-active" href="./" aria-current="page">Party trays</a></nav>')
    tray_options = "".join(f"<option>{e(t['name'])} (serves {e(t['serves'])})</option>" for t in cat["items"])
    fields = f"""<label for="c-name">Full name</label>
  <input id="c-name" name="name" autocomplete="name" required>
  <label for="c-phone">Phone</label>
  <input id="c-phone" name="phone" type="tel" autocomplete="tel" required>
  <label for="c-tray">Tray</label>
  <select id="c-tray" name="tray">{tray_options}<option>Not sure yet</option></select>
  <div class="field-row">
    <div><label for="c-people">Number of people</label><input id="c-people" name="people" type="number" min="1" inputmode="numeric" required></div>
    <div><label for="c-date">Pickup date</label><input id="c-date" name="date" type="date" required></div>
    <div><label for="c-time">Pickup time</label><input id="c-time" name="time" type="time" required></div>
  </div>
  <label for="c-notes">Requests (optional)</label>
  <textarea id="c-notes" name="notes" rows="4"></textarea>"""
    body = f"""{page_head('Catering', 'Party trays for groups, made to order. Tell us which tray, how many people and when you want it. Trays need at least 45 minutes.', tabs)}
<section class="band band-light" aria-label="Party trays">
  <div class="container tray-grid">
    {''.join(tray_card(rel, t, 'h2') for t in cat['items'])}
  </div>
</section>
<section class="band" aria-labelledby="req-h">
  <div class="container form-wrap">
    <h2 id="req-h" class="section-title center">Request a tray</h2>
    <p class="section-lead center">Fill this in and send it with WhatsApp or your email app. We'll confirm the order and the pickup time. Prefer to talk? Call <a href="{TEL}">{e(SITE['phone']['display'])}</a>.</p>
    {composer_form('catering-form', fields, note='Nothing is stored on this website: the message opens in WhatsApp or your email app for you to send.')}
    {contact_constant()}
  </div>
</section>
"""
    return page("catering/", "Catering: Party Trays for 4–10 People",
                f"{SITE['name']} party trays for 4–5 or 8–10 people: kofta, kabab, beef and chicken shawarma over rice, salad, hummus and baba ghanoush. Order at least 45 minutes ahead.",
                body, current="catering", ld=[restaurant_ld()], body_class="page-catering")


def about_page() -> str:
    rel = "../"
    paras = "".join(f"<p>{e(p)}</p>" for p in SITE["about"])
    values = "".join(
        f'<li class="value">{icon(v["icon"], "icon icon-lg")}<h3>{e(v["title"])}</h3><p>{e(v["text"])}</p></li>' for v in SITE["values"])
    gallery = "".join(f'<li>{dish_img(rel, ITEMS[x])}</li>' for x in ("shish-tawook-over-rice", "hummus", "fattoush", "falafel-sandwich"))
    body = f"""{page_head('Beit means home', f'Beit is Arabic for home, and &ldquo;{e(SITE["tagline"])}&rdquo; is the standard we cook to.', eyebrow='About us')}
<section class="band band-light">
  <div class="container about-grid">
    <div class="prose">
      {img(rel, 'img/brand/logo.webp', SITE['name'] + ' logo: a shawarma spit inside an arched doorway, with the words Tastes Like Home', cls='about-logo')}
      {paras}
      {buttons(('accent', TEL, 'phone', 'Call ' + e(SITE['phone']['display'])), ('outline', '../menu/', '', 'See the menu'))}
    </div>
    <ul class="gallery">{gallery}</ul>
  </div>
</section>
<section class="band values-band" aria-labelledby="values-h">
  <div class="container">
    <div class="section-head"><h2 id="values-h" class="section-title">What we stand for</h2></div>
    <ul class="values">{values}</ul>
  </div>
</section>
{reviews_band(rel)}
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
    fields = """<label for="f-name">Your name</label>
  <input id="f-name" name="name" autocomplete="name" required>
  <label for="f-topic">Topic</label>
  <select id="f-topic" name="topic">
    <option>General question</option>
    <option>Party tray / catering</option>
    <option>Feedback</option>
  </select>
  <label for="f-msg">Message</label>
  <textarea id="f-msg" name="message" rows="5" required></textarea>"""
    body = f"""{page_head('Contact', f'Questions, catering orders or feedback: call, message or stop by. {e(SITE["hoursLabel"])}.', open_status(SITE['hoursLabel']))}
<section class="band band-light">
  <div class="container">
    <ul class="contact-cards">{card_html}</ul>
  </div>
</section>
<section class="band" aria-labelledby="msg-h">
  <div class="container form-wrap">
    <h2 id="msg-h" class="section-title center">Send us a message</h2>
    <p class="section-lead center">Write it here and send it with WhatsApp or your email app. Ordering a party tray? The <a href="../catering/">catering page</a> asks for everything we need.</p>
    {composer_form('contact-form', fields, note='Nothing is stored on this website: the message opens in WhatsApp or your email app for you to send.')}
    {contact_constant()}
  </div>
</section>
{visit_section(rel)}
"""
    return page("contact/", "Contact & Directions", f"Contact {SITE['name']} at {address_line()}. Call {SITE['phone']['display']}, message us on WhatsApp or email {SITE['email']}. Open {SITE['hoursLabel'].lower()}.",
                body, current="contact", ld=[restaurant_ld()], body_class="page-contact")


def not_found() -> str:
    base = TARGET["base"]
    body = f"""{page_head('This page left the grill', "The page you were looking for isn't here, but the food still is.",
                     buttons(('accent', base + 'menu/', '', 'See the menu'), ('outline', base, '', 'Go home')), eyebrow='Page not found')}"""
    return page("404.html", "Page not found", f"This page could not be found. See the {SITE['name']} menu.", body, rel=base, robots="noindex")


def legacy_redirect() -> str:
    # The old Angular site lived at /home; keep that link (on Google, menus, flyers) working.
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>{e(SITE['name'])}</title>
<meta name="robots" content="noindex"><link rel="canonical" href="{TARGET['url']}/">
<meta http-equiv="refresh" content="0; url=../"></head>
<body><p><a href="../">Continue to {e(SITE['name'])}</a></p></body></html>
"""


PAGES = {"index.html": home, "menu/index.html": menu_page, "catering/index.html": catering_page,
         "about/index.html": about_page, "contact/index.html": contact_page, "404.html": not_found,
         "home/index.html": legacy_redirect}


def build(out: Path) -> None:
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(ROOT / "static", out)
    for rel_path, fn in PAGES.items():
        dest = out / rel_path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(fn(), encoding="utf-8")
    urls = ["", "menu/", "catering/", "about/", "contact/"]
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
    for sid in SITE.get("featured", []):
        if sid not in ITEMS:
            problems.append(f"site.json featured: no menu item with id {sid!r}")
        elif not ITEMS[sid].get("image"):
            problems.append(f"site.json featured: {sid!r} has no photo")
    if TRAYS not in CATS:
        problems.append(f"menu.json: no {TRAYS!r} category for the catering page")
    for key in ("text", "label", "href"):
        if not SITE.get("announcement", {}).get(key):
            problems.append(f"site.json announcement: missing {key!r}")
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
