# Beit Shawarma website

> A fast, static rebuild of [beitshawarma.com](https://www.beitshawarma.com/home) for Beit Shawarma, 1601 Simpson St, Evanston, IL. The menu, prices and hours live in two JSON files, and one Python script turns them into the whole site. A preview is published at [bamr87.github.io/beit-shawarma](https://bamr87.github.io/beit-shawarma/).

## Quick start

This folder is the source. It lives in `bamr87/bamr87.github.io` under `src/beit-shawarma/`, which Jekyll does not publish. The preview that GitHub Pages serves is generated into `beit-shawarma/` at the repository root. After any change, run from the repository root:

```bash
python3 src/beit-shawarma/build.py --preview https://bamr87.github.io/beit-shawarma --out beit-shawarma
python3 src/beit-shawarma/build.py --check --preview https://bamr87.github.io/beit-shawarma --out beit-shawarma
python3 -m http.server 8000      # then open http://localhost:8000/beit-shawarma/
```

Commit the source and the regenerated `beit-shawarma/` together. Merging to `main` publishes them. Python 3.9 or newer, standard library only: nothing to install.

## Changing the site

| To change | Edit |
| --- | --- |
| A price, dish, description or menu section | `content/menu.json` |
| The party trays on the catering page | the `trays` category in `content/menu.json` |
| Hours, phone, address, email, social links, About text | `content/site.json` |
| The dishes in the home page's "Off the grill" carousel | `featured` in `content/site.json` (menu item ids, each with a photo) |
| The announcement bar above the header | `announcement` in `content/site.json` (text, button label, link) |
| Colors, spacing, layout | `static/css/styles.css` |
| A dish photo | see below |

Then rebuild (Quick start). Never edit the generated `beit-shawarma/` or `site/` folders by hand: the next build overwrites them, and `--check` reports the difference. The build stops with a clear message if a price is not a number, a dish names a photo that doesn't exist, or the announcement or carousel names something missing.

**The page format.** Every page shares the same frame:

- a slim announcement bar over a dark maroon header with uppercase navigation and a saffron "Call to order" button
- full-width bands for the page's sections
- square uppercase buttons
- a four-column dark footer (location, hours, order, contact)
- on phones, a quick-actions bar (Call, Menu, Trays, Directions) fixed to the bottom of the screen

The menu is two columns of cream cards: each has a centred heading, a rule down the left and one row per dish (name, price, description). The catering page has the trays and a request form. Type is Jost for headings and buttons and PT Sans for reading. The colours are the logo's red, darkened to maroon for surfaces, with saffron for actions.

**Adding a dish photo.** Save a cut-out photo (a PNG with the background removed works best), then run, in this folder:

```bash
pip install pillow                                                         # once
python3 tools/optimize_images.py ~/Downloads/new-dish.png static/img/menu/new-dish.webp
```

Then set `"image": "new-dish"` on the item in `content/menu.json`.

**Hours.** `hours` in `site.json` drives the live "Open now · until 10 PM" badge (computed in Chicago time, whatever the visitor's time zone) and Google's opening-hours data. `hoursLabel` is the human-readable line. Change both together. Different hours per day are supported: add one entry per group of days, for example `{"days": ["Fr", "Sa"], "opens": "11:00", "closes": "23:00"}`.

## Deploying

**Today: a preview.** `--preview <url> --out <dir>` builds a copy for an address other than the restaurant's domain:

- links work under `/beit-shawarma/`
- a "Preview" banner on every page
- `noindex` on every page and a `robots.txt` that blocks crawlers
- no sitemap and no `CNAME`

So it can't claim www.beitshawarma.com or compete with it in search. The user site keeps it out of its own `sitemap.xml` too (a `sitemap: false` default in its `_config.yml`).

**Launching on www.beitshawarma.com.** Running `python3 build.py` in this folder writes the production build into `site/`, with canonical URLs, a sitemap and a `CNAME` for www.beitshawarma.com. The domain needs a host of its own, because bamr87.github.io already answers for the profile site.

1. Give the site its own repository: `git subtree split --prefix src/beit-shawarma -b beit-shawarma` keeps its history; push that branch to a new repo. Then publish `site/` with GitHub Pages (Settings → Pages), Netlify or Cloudflare Pages (build command `python3 build.py`, publish directory `site`).
2. At the domain registrar, point `www` at the new host. For GitHub Pages, use a `CNAME` record to `<owner>.github.io`, and `A` records for the bare domain to `185.199.108.153`, `185.199.109.153`, `185.199.110.153` and `185.199.111.153` ([GitHub's guide](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site)). Turn on HTTPS once the certificate is issued.
3. Remove the preview: delete `beit-shawarma/` and `src/beit-shawarma/` from bamr87.github.io.

The old addresses keep working after launch: `/menu`, `/about` and `/contact` exist at the same paths, and `/home` (the old home page address) redirects to `/`. The catering page, `/catering`, is new.

## What's different from the old site

| | Old site (Angular app) | This rebuild |
| --- | --- | --- |
| What Google sees in the HTML | An empty `<app-root>`, title "BeitShawarma" | Full text on every page, real titles and descriptions, Restaurant and Menu structured data |
| Menu page download | 7.0 MB (PNG photos) | 0.9 MB (WebP photos) |
| Home page download | 1.6 MB | 0.4 MB |
| First screen on a phone | The logo | Headline, "See the menu", tap-to-call, open/closed status |
| Hours | Static text | Live "Open now" / "Closed now · opens at 11 AM" |
| Contact form | EmailJS on the previous developer's account | Writes the message into WhatsApp or the visitor's email app; nothing to maintain |
| Map | None | Google Map that loads only when a visitor asks (saves 1.8 MB and keeps visitors' data from Google until they choose) |
| Social icons | Linked to facebook.com and instagram.com home pages | Hidden until real account links are added in `site.json` |
| Accessibility | Not checked | 0 violations in an axe-core WCAG 2.1 AA audit, phone and desktop |

Things the owner should confirm before launch are in [OWNER-REVIEW.md](OWNER-REVIEW.md).

## Layout

| Path | What it is |
| --- | --- |
| `content/` | `site.json` (business details) and `menu.json` (the menu): the only files most changes need |
| `static/` | Stylesheet, script, images, icons; copied into the build as-is |
| `build.py` | Renders every page, the JSON-LD, `sitemap.xml` and `robots.txt`; `--preview URL --out DIR` builds the noindex preview; `--check` reports a stale build |
| `tools/optimize_images.py` | Converts a new photo to WebP (needs Pillow) |
| `site/` | The production build, made at launch with `python3 build.py`; not committed here |
| `../../beit-shawarma/` | The published preview, generated; never edit it by hand |

## Credits

Photos, logo and menu text are Beit Shawarma's own, carried over from the previous site. Fonts: Fraunces and Inter (Google Fonts, SIL Open Font License). Icons are drawn in the style of Lucide (ISC).
