# Owner review before launch

> Everything on the new site that differs from the old one, or that only the restaurant can confirm. Each item says what the old site said, what the rebuild says, and where to change it.

## Please confirm: corrections made in the rebuild

| # | Item | Old site said | Rebuild says | Why |
| --- | --- | --- | --- | --- |
| 1 | Beef Kofta over Rice / Kabab over Rice | Kofta: "Chargrilled marinated beef cubes." Kabab: "Grilled spiced ground beef kababs." | The two descriptions swapped | Kofta is ground meat and kabab is cubes, and Chicken Kofta already says "ground". Swap back in `menu.json` if the old text was right. |
| 2 | Water | "Hot brewed coffee" (copied from Coffee) | "Bottled water." | A copy-paste slip |
| 3 | Kufta / Kofta spelling | Both spellings used | "Kofta" everywhere | One spelling helps customers searching the menu |
| 4 | "Tray 2" | "Tray 2" | "Party Tray 2" | Matches "Party Tray 1" |
| 5 | "baba ghanoug" in tray contents | "baba ghanoug" | "baba ghanoush" | Matches the Baba Ghanoush side |
| 6 | Home page photo descriptions | Alt text "Drink 2" and "Drink 3" on the plate photos | The dish names | Screen readers and Google read these |

## Please confirm: text the rebuild added

| # | Where | Added text |
| --- | --- | --- |
| 7 | Baklava | "Layered filo pastry with nuts and syrup." |
| 8 | Harissa | "Sweet semolina cake." In the US, "harissa" usually means chili paste, so a short description avoids surprises. |
| 9 | Home, About | "Beit is Arabic for home." |
| 10 | Home | "Every plate on our menu is halal." This rests on the old site's "100% Halal" badge. |
| 11 | Menu | "Vegetarian" tags on falafel, hummus, baba ghanoush and the salads; "Most filling" on the Mix Grill. Remove any that aren't right. |
| 12 | Address | ZIP code 60201, taken from the restaurant's Google Maps listing |

## Please check: prices that look inconsistent (published as-is)

- **Beef Shawarma sandwich:** $16.99, but "Double: $14.99". A double usually costs more than a single. The Chicken Shawarma sandwich is $9.99, with Double at $15.99.

## Needed from the restaurant

- **Facebook and Instagram links.** The old icons pointed to facebook.com and instagram.com, not to the restaurant's pages. Add the real addresses to `social` in `content/site.json` and the icons appear.
- **Higher-resolution photos.** The current photos are remove.bg free previews, 250–580 px wide, so they look soft when shown large. File names such as `BeitShawarma_BabaGhanoush_2880x2304` suggest originals exist. Run them through `tools/optimize_images.py --max 1200` to replace the ones in `static/img/menu/`.
- **Online ordering.** If you're on DoorDash, Uber Eats, Grubhub or Toast, the "Call to order" buttons can link there as well.
- **Hosting and domain access.** Who controls the DNS for beitshawarma.com, so the domain can point at the new host?
- **Google Business Profile.** Its hours, phone and website should match `site.json`. Google already shows 5.0 stars from 262 reviews, so linking "Read our reviews" to the listing is an easy addition.
- **Photo rights.** Confirm the restaurant owns the food photos and logo carried over from the old site.
