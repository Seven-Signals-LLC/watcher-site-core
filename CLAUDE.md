# Working on watcher-site-core

This repo is public. Never add secrets, API keys, customer data or market numbers.

- Changes here reach every Watcher site once they update `core.version`, so keep output stable. Before releasing, build at least one site against your local copy (`WATCHER_CORE_PATH=... python3 tools/build.py` in the site repo) and diff its `public/` HTML against the previous build. Ignore only the `?v=` cache-busting stamps.
- Site-specific things (look, fonts, logo, copy, pages, data) belong in the site repo, not here. If a site needs something different, add a `site.json` setting rather than a special case.
- Use only the Python 3 standard library in `build.py` and `templates/build.py`; Cloudflare builds run them as-is.
- Record every release in `CHANGELOG.md` and tag it (`v0.x.y`).
- To draft a site's industry report from its research document, follow `docs/industry-report.md`.
