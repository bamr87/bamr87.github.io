# _data

> The site's data files: the curated project registry, the generated portfolio data the homepage renders, the navigation menus and the theme's UI strings.

| File | What it is | How to change it |
| --- | --- | --- |
| `projects.yml` | Curated registry of the projects the portfolio shows; display order is file order | Edit it, then run `python3 scripts/generate_portfolio.py` |
| `portfolio.yml` | Enriched project data and totals the homepage dashboard renders via `site.data.portfolio` | Never by hand — `scripts/generate_portfolio.py` writes it |
| `navigation/*.yml` | The navbar (`main.yml`) and the sidebar menus a page selects with `sidebar.nav` | Edit; nest items with `children:` (the theme ignores `sublinks:`) |
| `navigation-old.yml` | The previous navigation, still pulled in by `pages/home.md` with `include_relative` | Only together with `pages/home.md` |
| `ui-text.yml` | Theme UI strings per locale, such as `back_to_top` | Edit |
