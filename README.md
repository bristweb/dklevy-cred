# DKLEVY — reviews data

Reviews and testimonials for **[DKLEVY](https://dklevy.com/)** (DKLEVY PLLC, architecture and design, Knoxville TN), plus the settings and theme for its reviews widget. The widget code lives in **[bristweb/cred](https://github.com/bristweb/cred)**. This repo is only DKLEVY data. Nothing in it is from another client's reviews.

GitHub Pages, once this folder is the root of `bristweb/dklevy-cred` and Pages is set to branch `main` / `/`, serves the files at `https://dklevy-cred.pages.dev/`. `.github/workflows/deploy.yml` can also publish to Cloudflare Pages when the repo secrets `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`, and `CF_PAGES_PROJECT` are set. Without those secrets the Cloudflare job is skipped.

- **Settings:** [`config.js`](config.js) · **Reviews:** [`reviews/`](reviews/) · **Testimonials:** `testimonials` in `config.js`

## Embed on dklevy.com

The homepage Testimonials block is three quotes (Tracy Sneed, Ray Heath, Jaime Goldenberg). Replace that block with the widget so the same quotes, plus later reviews, stay in this repo.

```html
<script src="https://cred.bristleconeweb.com/assets/js/cred.js"
        data-source="https://dklevy-cred.pages.dev/" defer></script>
```

dklevy.com is a Framer site. On the homepage, select the Testimonials section and use Insert → Embed → HTML, then paste the snippet. If the embed frame has a fixed height, add `data-constrained="true"` and make the frame about 420px tall.

Iframe and other options: [cred README](https://github.com/bristweb/cred#options).

`index.html` in this folder is a noindex preview. It loads the widget from whatever host the page itself is on, so `python3 -m http.server` in this directory previews the data before Pages is turned on. The snippet above is what dklevy.com should use after Pages (or Cloudflare) is live.

## What's here

```
config.js             business, platforms, links, display, schema, testimonials, reviews.years
reviews/<year>.json   Google reviews whose full text was copied from a page that showed it (2025, 2023, 2020)
images/reviewers/     initials avatars, plus the two logos the homepage shows beside Ray Heath and Jaime Goldenberg
icons/                platform and social marks (see icons/ATTRIBUTION.md)
theme/                theme.css (colors taken from dklevy.com) + self-hosted Inter
scripts/              sync tooling (never loaded by the widget)
.github/workflows/    validate.yml on every push; deploy.yml for Cloudflare Pages
```

Record shape: [cred data repo format](https://github.com/bristweb/cred#data-repo-format).

JSON-LD is built by the widget. `schema.type` is `ProfessionalService`. `schema.extra["@id"]` is `https://dklevy.com/#organization`, which overrides the widget's default `{website}#business`. `legalName` is DKLEVY PLLC, `telephone` is `+18654749264`, and the address is 3523 Maloney Rd, Knoxville TN 37920. The widget only injects that block when at least one stored review has a 1–5 rating (the five Google rows below). Unrated testimonials are not in the aggregate.

## Testimonials

The live homepage shows these three quotes and no star ratings. Quotation marks and the double spaces in Ray Heath's quote are as published. The Framer record for Tracy Sneed has no date; the card date is the day the quote was read (2026-11-05), called out in `date_note`. Ray Heath and Jaime Goldenberg use `datePublished` from their archived testimonial posts. Kennon Rymer is an additional testimonial from that archive, not one of the three on the homepage.

| Name | Role | Where the words were read |
|---|---|---|
| Tracy Sneed | Co-Founder/Owner, Remember Me Senior Care | https://dklevy.com/ |
| Jaime Goldenberg | Senior Pastor, The Church at Knoxville | https://dklevy.com/ (date from the 2019 archived post) |
| Ray Heath | President, Hiram Group | https://dklevy.com/ (date from the 2017 archived post) |
| Kennon Rymer | President, Infinity Construction, LLC | archived post, captured 2022-08-19 |

## Reviews stored

Five Google reviews. Each full text, calendar date, and five filled stars were on [the Exa place page](https://exa.ai/library/place/5fkd9vzs52b). The author name was not on that page; it is the name [localitybiz](https://localitybiz.com/32206082/dklevy-architecture-and-design-knoxville) shows next to the same text. `platform_review_id` values start with `PLACEHOLDER-` because no Google review id was available. Cards link to the Maps place, not to a per-review URL.

| Author | Date shown on Exa | Rating shown |
|---|---|---|
| Robert Muirhead | 2025-05-01 | 5 |
| Kris King | 2023-09-16 | 5 |
| Shane Hornbuckle | 2023-09-13 | 5 |
| Kenneth | 2020-05-12 | 5 |
| Mike Wilhoit | 2020-02-05 | 5 |

Logged-out Google Maps HTML for this place contained no review text, so these rows were not copied from Google itself.

## Sources checked (2026-11-05)

People named on dklevy.com (about page and `/people/*`): Daniel Levy, Kendel Levy, Chris Morris, Rodney Calvin, Ethan Guthrie, Ribhav Murria, Hunter Tisdale.

| Source | Result |
|---|---|
| https://dklevy.com/ | Three testimonials, no ratings, no dates in the CMS. Organization JSON-LD matches the schema in `config.js`. Maps short link `https://maps.app.goo.gl/z8MPeJbStNsYzGt4A`. |
| Google Maps place `0x885c16b509efcc2d:0x9248c2c2650e244b` (cid `10540889068035515467`, `/g/126300z5t`) | Place page loaded. Review text was not in the logged-out HTML, and no review count was in that HTML. **Place id (`ChIJ…`) was not present — `PLACEHOLDER_GOOGLE_PLACE_ID`.** |
| https://exa.ai/library/place/5fkd9vzs52b | Says 5.0 (18 reviews) and shows 8 review cards, all with five filled stars. One card (2025-05-02) is cut off at "guiding the…". One full card (2023-08-02) and one full card (2023-03-03, text ends with the name Brenda Skinner) have no separate author. Those three were not stored. |
| https://localitybiz.com/32206082/dklevy-architecture-and-design-knoxville | A reader fetch showed 5.0 from 18 ratings and 8 review texts with author names and relative dates ("1 year ago"), not calendar dates. A direct curl later returned HTTP 403. Names from that reader fetch were kept only when the full text matched the Exa card. Jack Llewellyn Jr., Joshua Crisp, and willie russell were on that page and were **not** stored: Jack's Exa copy is truncated, and the other two had no calendar date on a page whose HTML was saved. |
| https://ecohome.co/business/dklevy-architecture-and-design | Says 5.0 based on 15 reviews. The 10 visible bodies are cut off ("Create account to read full review"). Initials shown include J M, Brenda S, Mike W, Kenneth, Cynthia J, Tracy S, Kennon R, Scott H. Not stored. |
| Houzz profile `…/dklevy-architecture-and-design-pfvwus-pf~914757148` | Page content said a visitor could be the first review (0). Direct fetch hit a bot challenge. |
| https://www.yelp.com/search?find_desc=DKLEVY&find_loc=Knoxville%2C+TN | HTTP 403. No listing confirmed. |
| https://www.facebook.com/dklevydesign/ and `/reviews` | Profile URL is in the homepage JSON-LD. `/reviews` returned HTTP 400; the page URL redirected to login. Count unknown. |
| https://www.bbb.org/search?find_text=DKLEVY&find_loc=Knoxville%2C+TN | Search page title: no results found. |
| https://www.angi.com/search?q=DKLEVY&l=Knoxville%2C%20TN | HTTP 403. |
| https://www.linkedin.com/company/dklevy-architecture-firm/ | HTTP 403. No recommendations readable for the company or the people listed above. |
| Nextdoor | No DKLEVY listing turned up in web search. |
| https://dklevy.com/testimonial-cat/testimonials/ | Live URL is HTTP 404. Wayback (2026-02-08) still has Brenda Skinner, Kennon Rymer, Jaime Goldenberg, and Ray Heath. Brenda's paragraph is complete on that archive and has no date; her individual post was not archived. Not stored, so a date would not be invented. |
| https://dklevy.com/journal/historic-knoxville-high-wins-national-award | Dated Dec 18, 2018. The page says "national award" and does not name it. |
| https://dklevy.com/people/daniel-levy | The bio names the ACHP National Preservation Chairman's Honor (Guest House at Alexander Inn) and a Best Senior Living Project of the Year (Historic Knoxville High) without years. Not stored as accolades, because a year and a name were not on the same page. |

## Placeholders that need real values

- `platforms.google.place_id` (`PLACEHOLDER_GOOGLE_PLACE_ID`) and the write-a-review URL that depends on it (`platforms.google.write_url` currently opens the Maps place).
- `platform_review_id` on every file in `reviews/` (`PLACEHOLDER-…`), and a real per-review Google URL if you want cards to open the review rather than the place.
- Google's own reported rating and count (left unset; Exa says 18, Ecohome says 15).
- Tracy Sneed's publication date (`testimonials[0].date` is the collection time).
- Facebook review count, a Yelp or Angi listing if one exists, LinkedIn recommendations, and whether Houzz's "first review" line is still current.
- Cloudflare Pages secrets, after the GitHub repo `bristweb/dklevy-cred` exists. This folder is the repo root to publish. It is not a fork of another reviews repo.

## Sync tooling

`scripts/` collects later reviews (Python 3, no packages; Node reads `config.js`). The widget never loads it. A platform whose `scrape_url` contains `PLACEHOLDER`, or that has no `scrape_url`, is skipped. Google's `scrape_url` is the Maps place URL above.

```bash
python3 scripts/pull_reviews.py --print-inputs
# save the actor's dataset items to the printed path, then:
python3 scripts/pull_reviews.py --from-raw
node ../cred/scripts/validate.mjs .
```

`APIFY_TOKEN=… python3 scripts/pull_reviews.py` calls the Apify API. Each run is capped at $0.50 and only asks for reviews newer than the newest stored review on that platform, minus 30 days. New rows go into `reviews/<year>.json`. If any stored review is dated or collected after `summary.generated_at`, the script prints `SUMMARY STALE` and writes `.pull/summary_input.txt`. Rewrite `summary.text` from that file (only themes that are actually in the text, no invented facts, no attributed quotes, no star claims) and set `summary.generated_at` to the current UTC time.

## Look and feel

[`theme/theme.css`](theme/theme.css). Measured on dklevy.com: ink `#191a1a`, body `#3e4041`, muted `#808284`, accent `#7eb338` (also `#73b338`). Card chrome (line, tint, radius) is there so the widget has a full set of tokens. Typeface is Inter ([OFL](theme/fonts/OFL.txt)).

## Credits

Platform marks: see [`icons/ATTRIBUTION.md`](icons/ATTRIBUTION.md). Review text belongs to its authors. The five Google rows link back to the Maps place and record the Exa and localitybiz URLs the words and names were read from.
