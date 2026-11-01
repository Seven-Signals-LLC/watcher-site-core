# Changelog

## v0.2.0 (November 2026)

The DecorWatcher menu, demo wording and pricing become the shared standard, so every Watcher site says the same thing. Pilot: FencePostWatcher.

- `defaults.json`: standard menu (Why Us, The Signals, Solutions, Industry Report, Pricing, Contact), **Try the demo** button, login, demo and lead Worker links, and the default `words` and `pricing`. A site's own `site.json` keys still win.
- Shared sections a page pulls in with a marker: `<!--core:demo-button-->`, `<!--core:demo-trust-->`, `<!--core:demo-ps-->`, `<!--core:get-started-->` (client set-up form → watcher-leads Worker) and `<!--core:pricing-->`.
- `hrefs` in `site.json` repoints a standard link by key (for example the industry report).
- Sites that set their own `nav`, `cta` and `login_url` and use no markers build exactly as on v0.1.1 (checked on the sample site and FencePostWatcher).

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
