# watcher-site-core

The shared framework for every **Watcher** marketing site by 7 Signals (DecorWatcher, GarageWatcher, PlumbWatcher and the rest). It holds the parts that should be the same on every site, so a change made here reaches all of them:

- the page layout: head tags, social cards, canonical URL, structured data
- the header, menu, mobile menu and "Try the demo" button
- the footer, including the Watcher family links (`family.json`)
- tracking (UXWizz, PipelineOn), set per site in `site.json`
- the build script and `sitemap.xml`
- the industry report at `/industry-report/`, built from each vertical's research document (see [docs/industry-report.md](docs/industry-report.md))

Each site keeps its own **look** (stylesheet, fonts, logo), **pages** and **content** in its own repo. This repo holds no secrets, customer data or market numbers, which is why it can be public.

## How a site uses it

A site repo contains:

| File | What it is |
|---|---|
| `core.version` | One line: the core release (for example `v0.1.0`) or commit SHA the site builds with |
| `site.json` | Brand, menu, button, footer, tracking, stylesheet and fonts. Start from [`templates/site.example.json`](templates/site.example.json) |
| `tools/build.py` | Copy of [`templates/build.py`](templates/build.py). Downloads the pinned core and runs it |
| `src/pages/*.html` | The site's pages. Each starts with a `<!--meta {...} -->` JSON block (title, description, path, nav, schema) |
| `research/` | Research documents for the industry report. Never published |
| `content/industry-report.json` | The industry report's content, drafted from `research/` by Claude and reviewed in a pull request. The core builds `/industry-report/` from it |
| `src/partials/mark-light.html` | Optional: the logo mark for the dark footer. Without it, the header logo is reused |
| `public/` | Static files (css, js, images, fonts). Built HTML is written here |

Cloudflare build settings for each site: **build command** `python3 tools/build.py`, **deploy command** `npx wrangler deploy`.

## Updating a site to a newer core

1. A new core version is released here (see below).
2. In the site repo, change `core.version` to the new version and open a pull request.
3. Check the Cloudflare preview link on the pull request, then merge.

Sites stay on their pinned version until someone changes that line, so one core change can never break every site at once. Update one site first, check it, then the rest.

## Releasing a new core version

1. Merge the change into `main` here through a pull request.
2. On GitHub: **Releases → Draft a new release → Choose a tag**, type the next version (for example `v0.2.0`), **Create new tag**, add a line on what changed, **Publish release**.
3. Add the change to `CHANGELOG.md`.

## Working on the core locally

```bash
# from a site repo, build against a local checkout of this repo
WATCHER_CORE_PATH=../watcher-site-core python3 tools/build.py
```

## site.json reference

| Key | Used for |
|---|---|
| `brand`, `brand_prefix` | Name in titles and social cards; the logo word renders as `{prefix}<i>Watcher</i>` |
| `site_url` | Canonical URLs, sitemap, structured data |
| `login_url` | "Log in" links |
| `mark` | Header logo file and size |
| `theme_color` | Browser theme colours (light and dark) |
| `og_image`, `og_image_alt` | Social share image. Optional: leave out until the site has one and the image tags are skipped |
| `icons` | Optional. Favicon links as a list of `{"href", "rel", "type", "sizes"}`. Default: `/favicon.ico`, `/favicon.svg`, `/apple-touch-icon.png` |
| `head` | Optional. Extra HTML at the end of `<head>` on every page, for example a Google Fonts link |
| `stylesheet`, `preload_fonts`, `scripts` | The site's own styling and scripts |
| `tracking` | `uxwizz` (true/false) and `pipelineon_tag` |
| `nav` | Menu items: `key`, `label`, `href`. A page whose meta `nav` matches a `key` shows that item as current |
| `cta` | The menu button: `label` (desktop), `label_long` (mobile menu), `href` |
| `footer` | `blurb`, and `columns`: each column is a list of groups with a `title` and `links`, or `"family": true` for the Watcher family list. Optional `legal`: the bottom links as `{"label", "href"}` (default Privacy Policy `/privacy-policy/`, Terms `/terms/`) |
| `organization` | Structured data on the home page. Optional `logo` path (default `/icon-512.png`) |

## Shared defaults (`defaults.json`)

Every site starts from `defaults.json`, the DecorWatcher standard. Anything a site sets in `site.json` wins, so a site only lists what's different.

| Key | Default |
|---|---|
| `nav` | Why Us, The Signals, Solutions, Industry Report, Pricing, Contact |
| `cta` | **Try the demo** (mobile menu: **See the demo for free**) → the Watcher demo |
| `login_url`, `demo_url`, `lead_endpoint` | Watcher login, the demo, the shared watcher-leads Worker |
| `words` | The site's nouns for the shared sections: `business`, `businesses`, `Business`, `payoff`, `email_placeholder`, `site_placeholder` |
| `pricing` | `plan_name`, `price`, `price_note`, `checkout_label`, `checkout_url` (the shared Stripe payment link every site's **Subscribe** button uses; change it here to update all sites, or set it in a site's `site.json` to give that site its own), `plan_items`, `custom_items` |

`words` and `pricing` merge entry by entry, so `"pricing": {"plan_name": "Contractor"}` changes only the plan name.

`hrefs` repoints a standard link by its `key` everywhere it appears (menu, footer, shared sections). For example, a site without an `/industry-report/` page sets `"hrefs": {"report": "/#report"}`. Footer links can carry a `key` too.

## Shared sections

Put a marker in a page and the build swaps in the shared section from `partials/sections/`, filled with the site's `words` and `pricing`:

| Marker | What it is |
|---|---|
| `<!--core:demo-button-->` | "See the demo for free" button (`.btn.btn--demo`) |
| `<!--core:demo-trust-->` | 5-minute demo · No credit card · No client data needed (`.demo-trust`) |
| `<!--core:demo-ps-->` | "P.S. The demo is free…" line (`.demo-ps`) |
| `<!--core:get-started-->` | "I want to get started" section with the client set-up form, posting to the watcher-leads Worker (works without JavaScript too; lands on `/thank-you/`) |
| `<!--core:pricing-->` | Pricing: free demo, subscription plan, custom services |

The wording lives here so it changes once for every site. Each site styles the section classes (`core-pricing`, `plan`, `core-start`, `core-form`, …) in its own stylesheet.

## Page meta reference

Each `src/pages/*.html` starts with `<!--meta {...} -->`. Keys: `title`, `description`, `path` (required); `og_title`, `og_type`, `nav`, `robots`, `body_class`, `schema` (list of JSON-LD objects), `priority`, `sitemap` (false to leave the page out), and `head` (extra HTML for this page's `<head>`, such as a hero image preload or a page `<style>` block). Pages whose `robots` contains `noindex` are left out of the sitemap.

## Roadmap

- **v0.1**: shared layout, header, footer, tracking, build and sitemap. Pilot: DecorWatcher. v0.1.1 adds the optional settings needed by the second site, FencePostWatcher.
- **v0.2**: shared menu and demo button defaults, shared demo wording, pricing and get-started sections. Pilot: FencePostWatcher.
- **v0.3** (this): industry report built from each vertical's research document. Pilot: DecorWatcher.
- **v0.4**: automatic "Update core" pull requests in every site repo when a version is released; shared base styling (including the report's charts and tables) and consent banner.
- **v0.5**: shared standard pages (use cases, contact, thank-you, privacy, terms, 404) driven by each site's words and data.
