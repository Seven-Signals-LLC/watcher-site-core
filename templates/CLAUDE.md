# Working on this Watcher site

This site builds on [watcher-site-core](https://github.com/Seven-Signals-LLC/watcher-site-core). Shared layout, header, footer, sections, `/use-cases/` and `/industry-report/` come from the core; this repo owns the look, pages and content.

## Design with Hallmark

Before you design or build anything for this site (a new site, a new page, a new section or a restyle), invoke the `/hallmark` skill and follow it. Use `/hallmark redesign <path>` to rework an existing page and `/hallmark audit <path>` to check one.

- It applies to what this repo owns: `public/` styles and assets, `src/pages/*.html` and `src/partials/`. Don't restyle or work around core-built markup to satisfy it; if its lint flags core output, note it in the pull request.
- Run its lint on the built `public/` pages before opening a pull request, and list the theme and the lint result in the pull request description.
- The home page opens with the core's standard hero, `<!--core:hero-->` (full-bleed photo, ink scrim, headline low-left; see watcher-site-core `docs/hero.md`). Keep it, stamp `hero: Poster (core standard)`, and design the rest of the page with Hallmark.
- Never invent metrics, testimonials, logos or customer counts.
- If the `/hallmark` skill isn't available in your session, stop and say so instead of designing without it.

## Building

`python3 tools/build.py` builds `public/` with the core version in `core.version`. Never commit secrets or API keys.
