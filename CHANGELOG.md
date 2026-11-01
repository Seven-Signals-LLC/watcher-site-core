# Changelog

## v0.1.1 (November 2026)

Optional settings found while moving FencePostWatcher onto the core. Sites that don't use them build exactly as before (DecorWatcher-style sample checked byte-for-byte, ignoring `?v=` stamps).

- `site.json`: `head` (extra head HTML on every page), `icons` (favicon links), `footer.legal` (bottom links), `organization.logo`.
- `og_image` is now optional; without it the social image tags are left out.
- Page meta: `head` for page-only head HTML (preloads, page styles).

## v0.1.0 (November 2026)

First release, extracted from the DecorWatcher site.

- Shared layout, header with menu and demo button, mobile menu and footer, all driven by `site.json`.
- Watcher family footer links from `family.json`.
- UXWizz and PipelineOn tracking, switched on per site.
- Build script with sitemap, and `templates/build.py` for site repos to fetch a pinned core version.
- Pilot: DecorWatcher builds byte-for-byte the same pages as before.
