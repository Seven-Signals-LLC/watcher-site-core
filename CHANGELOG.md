# Changelog

## Unreleased

- Docs only, no build change: new Watcher sites are designed with the `/hallmark` skill. `CLAUDE.md` has the rule, and new site repos copy `templates/CLAUDE.md` so it follows each site.
- `family.json`: GroutWatcher (groutwatcher.com) added to the Watcher family footer list. Other sites pick it up when they move to the next core version; GroutWatcher never lists itself.

## v0.4.0 (November 2026)

- Use cases: when a site has `content/use-cases.json`, the core builds `/use-cases/` from it with the same layout on every site (hero, platform proof strip, index, seven use case blocks with example and real-data visuals, closing demo section). The page ships its own scoped CSS and takes the site's colours and fonts from the new optional `core_theme` setting. `docs/use-cases.md` has the format and drafting rules.
- `defaults.json`: **Use cases** added to the standard menu after Solutions, matching DecorWatcher. Sites without a use-cases page don't show it, and footer links with `"key": "usecases"` are dropped there too.
- Pilot: FencePostWatcher, which was missing the page. Sites without `content/use-cases.json` and without a footer link keyed `usecases` build exactly as on v0.3.0 (ignoring `?v=` stamps). DecorWatcher keeps its hand-written page.

## v0.3.0 (November 2026)

- Industry report: when a site has `content/industry-report.json`, the core builds `/industry-report/` from it, with the same layout on every site (contents list, stat strips, charts, tables, funnel, numbered sources, closing demo section). `docs/industry-report.md` has the rules Claude follows to draft that file from the research document in the site's `research/` folder.
- Pilot: DecorWatcher's report moved from a hand-written page to `content/industry-report.json`; every page builds byte-for-byte the same (ignoring `?v=` stamps). Sites without the file build exactly as on v0.2.1.

## v0.2.1 (November 2026)

- Every site's **Subscribe** button now goes to one shared Stripe payment link (`pricing.checkout_url` in `defaults.json`), so the checkout is changed in one place. A site can still set its own in `site.json`.

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
