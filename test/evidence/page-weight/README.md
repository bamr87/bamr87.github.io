# The heavy pages load a fraction of the bytes and look the same — evidence

> **Issue:** #32 · **Pages:** `/notes/`, `/pages/` (and every page that falls back to the default header) · **Captured by:** an agent with Playwright (headless Chrome 157) against production builds of `main` and the fix branch on 2026-11-16

A visitor opening `/notes/` downloaded about 8 MB, almost all of it images: three cat photos stored as 1–1.6 MB PNGs, a 1.5 MB screen-recording GIF and a 0.6 MB header. `/pages/` downloaded about 4 MB, because the fallback card image (`site.teaser`) was a 1.85 MB PNG and one Quest Log card preview was 845 KB. After the fix the same pages transfer about 2 MB and 1.6 MB, and the images on them look the same.

## How it was run

Both sites were built with the production config (`JEKYLL_ENV=production bundle exec jekyll build` in `ruby:3.4`, `github-pages` gem, Jekyll 3.10, the remote theme as published at build time) and served locally with `python3 -m http.server`. Before is `main` @ 6538202 (the `before-*.png` images); after is the fix branch (every other image and [`report.json`](report.json)). Each page was loaded at 390×844 and 1366×768, scrolled to the screencast and to the photo gallery on `/notes/`, and captured after the lazy images had loaded. The transfer numbers come from a separate pass at 1366×900 with the cache disabled, counting every response's encoded length.

| Page | Transferred before | Transferred after | Images before | Images and video after |
| --- | --- | --- | --- | --- |
| `/notes/` | 8.05 MB | 2.04 MB | 6.71 MB | 0.20 MB images (the rest lazy-load) + 0.50 MB video |
| `/pages/` | 4.20 MB | 1.63 MB | 3.03 MB | 0.47 MB |
| `/docs/jekyll/` (default header) | 1.81 MB | 1.49 MB | 0.64 MB | 0.20 MB |
| `/` | 1.21 MB | 1.21 MB | 13 KB | 13 KB (the homepage uses none of these files) |

Counting every image or video a built page references, lazy or not, `/notes/` goes from 8.55 MB to 1.41 MB and `/pages/` from 3.03 MB to 466 KB. The local server does not gzip, so CSS and HTML weigh more here than on GitHub Pages; the images and the video are the same size either way. `report.json` has the per-file and per-page numbers.

## What changed in each file

| File | Before | After |
| --- | --- | --- |
| `favicon_gpt_computer_retro.png` (`site.teaser`) | 1,848,372 B, 1024×1024 | 142,790 B, 600×600 palette PNG |
| `info-banner-mountain-wizard.png` (`site.info_banner`) | 623,172 B, 1792×1024 | 189,424 B, 1600×915 |
| `wizard-on-journey.png` (`site.og_image`) | 485,640 B, 1024×1024 | 158,586 B, 1024×1024 |
| `nubi-son.png` → `nubi-son.jpg` | 1,601,437 B | 178,745 B, JPEG q80, 1000 px wide |
| `nubi-yawn.png` → `nubi-yawn.jpg` | 1,452,094 B | 164,309 B, JPEG q80, 1000 px wide |
| `nubi-sink.png` → `nubi-sink.jpg` | 994,273 B | 100,097 B, JPEG q80, 1000 px wide |
| `markdown_paste.gif` → `markdown_paste.mp4` | 1,548,702 B, 1278×934, 338 frames | 497,503 B, 900×658 H.264, same frames and timing |
| `penrose-hard.png` | 308,881 B | 75,097 B, 16-colour PNG |
| `hover-note.png` | 162,666 B | 53,858 B, palette PNG |
| `jekyll-seo-preview.png` | 2,024,085 B, 1024×1024 | 372,519 B, 800×800 palette PNG |
| `jekyll-seo-snippet.png` (not referenced) | 1,572,726 B | 371,565 B, palette PNG |
| `sharex-imgur.png` | 626,594 B, 2736×1580 | 143,311 B, 1600×924 palette PNG |
| `quest-log/quest-log-it-journey/preview.png` | 845,131 B | 191,011 B, palette PNG, same 1200×627 |
| `quest-log/quest-log-bamr87-github-io/preview.png` | 186,990 B | 86,061 B, palette PNG |
| `quest-log/quest-log-bamr87/preview.png` | 140,006 B | 34,074 B, palette PNG |

In all, 14.4 MB of files became 2.8 MB. `info-banner-mountain-wizard.png` and `wizard-on-journey.png` already held WebP data under a `.png` name; they were re-encoded as WebP (`cwebp -q 60` and `-q 75`) so that no reference changes. Browsers sniff the format, so they display as before; renaming them to `.webp` would also fix the `image/png` content type GitHub Pages sends for them.

The recipe, run in `alpine` with `pngquant oxipng gifsicle libwebp-tools imagemagick ffmpeg`: `pngquant --quality 50-70` (teaser, Quest Log previews) or `65-85` (screenshots) then `oxipng -o 4 --strip safe`; `magick -resize '1000x>' -quality 80 -sampling-factor 4:2:0 -interlace Plane` for the photos; `ffmpeg -fps_mode vfr -c:v libx264 -preset veryslow -tune animation -crf 35 -pix_fmt yuv420p -movflags +faststart -vf scale=900:-2` for the screencast.

## What each image shows

| Image | Viewport | What to look at |
| --- | --- | --- |
| `before-mobile-pages.png`, `mobile-pages.png` | 390×844 | `/pages/`: the first Quest Log card; same picture |
| `before-desktop-1366-pages.png`, `desktop-1366-pages.png` | 1366×768 | `/pages/`: three Quest Log cards and the teaser cards below; same pictures |
| `before-mobile-notes-top.png`, `mobile-notes-top.png` | 390×844 | `/notes/` header: the default banner, now 1600 px wide WebP |
| `before-desktop-1366-notes-top.png`, `desktop-1366-notes-top.png` | 1366×768 | The same header at desktop width |
| `before-mobile-notes-screencast.png`, `mobile-notes-screencast.png` | 390×844 | "Paste images in Markdown": the GIF, then the MP4 at the same size and frame |
| `before-desktop-1366-notes-screencast.png`, `desktop-1366-notes-screencast.png` | 1366×768 | The same; the video autoplays muted and loops like the GIF, and has controls to pause it |
| `before-mobile-notes-gallery.png`, `mobile-notes-gallery.png` | 390×844 | "Examples": the cat photos, now JPEG and lazy-loaded |
| `before-desktop-1366-notes-gallery.png`, `desktop-1366-notes-gallery.png` | 1366×768 | The same at desktop width |

In headless Chrome the video reported `readyState` 4, was playing, and decoded at 900×658; the three photos loaded (`naturalWidth` > 0) once scrolled into view. Not covered: lazy-loading the `/pages/` cards (#23) and the `<iframe>` on `/about/theme/` (#27 decides that page's future). The screenshots were compressed with `pngquant` after capture.
