# Working on watcher-site-core

This repo is public. Never add secrets, API keys, customer data or market numbers.

- Changes here reach every Watcher site once they update `core.version`, so keep output stable. Before releasing, build at least one site against your local copy (`WATCHER_CORE_PATH=... python3 tools/build.py` in the site repo) and diff its `public/` HTML against the previous build. Ignore only the `?v=` cache-busting stamps.
- Site-specific things (look, fonts, logo, copy, pages, data) belong in the site repo, not here. If a site needs something different, add a `site.json` setting rather than a special case.
- Use only the Python 3 standard library in `build.py` and `templates/build.py`; Cloudflare builds run them as-is.
- Record every release in `CHANGELOG.md` and tag it (`v0.x.y`).
- To draft a site's industry report from its research document, follow `docs/industry-report.md`.

## New sites are designed with Hallmark

Whenever you build a new Watcher site, or design new pages or a new look for one, invoke the `/hallmark` skill before you write any HTML or CSS, and follow it for everything the site owns: `public/` stylesheet, fonts, logo use, `src/pages/*.html` and site partials. Run its lint on the built pages before you open the pull request, and put the theme it dealt and the lint result in the pull request description.

- Hallmark applies to the site repo, not to this repo. Don't change the core's shared layout, header, footer, sections or the built `/use-cases/` and `/industry-report/` pages to satisfy it, and don't add special cases here for it. If its lint flags core-built output, note that in the pull request and leave it.
- Hallmark's floor still applies to the copy: no invented metrics, testimonials or logos.
- Home pages open with the standard hero, `<!--core:hero-->` (`docs/hero.md`). It is a core standard, so a Hallmark run keeps it and designs the rest of the page.
- If the `/hallmark` skill isn't available in your session, stop and say so instead of designing without it.
- New site repos get [`templates/CLAUDE.md`](templates/CLAUDE.md) copied to their root, so this rule follows the site.
