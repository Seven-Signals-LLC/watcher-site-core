#!/usr/bin/env python3
"""watcher-site-core: the shared build for every Watcher marketing site.

A site repo holds its own pages, styling and settings. This script wraps each
page in the shared layout, header and footer, then writes the finished site
into the site's public/ folder along with sitemap.xml.

Site layout it expects (paths relative to the site root):
    site.json            brand, menu, footer, tracking and other settings
    src/pages/*.html     each page starts with a <!--meta {...} --> JSON block
    src/partials/        optional site extras (see README: mark-light.html)
    public/              static files (css, js, images); built HTML lands here

Usage:  python3 build.py --site /path/to/site
Needs only the Python 3 standard library.
"""
import argparse, datetime, html, json, pathlib, re, sys, time

CORE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(CORE))
import report  # noqa: E402  (core/report.py: the industry report page)
import usecases  # noqa: E402  (core/usecases.py: the use cases page)
import hero  # noqa: E402  (core/hero.py: the standard home page hero)
META_RE = re.compile(r"^\s*<!--meta\s+(\{.*?\})\s*-->\s*", re.S)
INCLUDE_RE = re.compile(r"<!--core:([\w-]+)-->\n?")


def load_site(root):
    """site.json on top of the shared defaults.json. A key the site sets wins;
    "words" and "pricing" are merged one level deep so a site can change a single entry."""
    defaults = json.loads((CORE / "defaults.json").read_text())
    site = json.loads((root / "site.json").read_text())
    merged = {**defaults, **site}
    for key in ("words", "pricing"):
        merged[key] = {**defaults.get(key, {}), **site.get(key, {})}
    return merged


def href_for(site, item):
    """A site can repoint a standard link by key, e.g. "hrefs": {"report": "/#report"}."""
    return site.get("hrefs", {}).get(item.get("key"), item["href"])


def drop_link(site, key):
    """Remove every menu and footer link with this key (used when the page it points to doesn't exist)."""
    site["nav"] = [i for i in site["nav"] if i.get("key") != key]
    for column in site["footer"]["columns"]:
        for group in column:
            if "links" in group:
                group["links"] = [l for l in group["links"] if l.get("key") != key]


def render(tpl, ctx):
    return re.sub(r"\{\{(\w+)\}\}", lambda m: str(ctx.get(m.group(1), "")), tpl)


def rel_for(href):
    """External links open with rel="noopener"; on-site, tel: and mailto: links don't."""
    return ' rel="noopener"' if href.startswith(("http://", "https://")) else ""


def brand_word(site):
    prefix = site.get("brand_prefix") or site["brand"].removesuffix("Watcher")
    return f"{prefix}<i>Watcher</i>"


def nav_html(site, current):
    desk, mobile = [], []
    for item in site["nav"]:
        href, label = href_for(site, item), item["label"]
        cur = ' aria-current="page"' if current and item.get("key") == current and not href.startswith("/#") else ""
        desk.append(f'        <li><a href="{href}"{cur}>{label}</a></li>')
        mobile.append(f'    <li><a href="{href}">{label}</a></li>')
    return "\n".join(desk), "\n".join(mobile)


def family_links(site):
    me = site["brand"]
    fam = json.loads((CORE / "family.json").read_text())
    return [{"label": f["brand"], "href": f["url"]} for f in fam if f["brand"] != me]


def footer_columns_html(site):
    out = []
    for column in site["footer"]["columns"]:
        out.append('      <div class="footer__col">')
        for i, group in enumerate(column):
            style = ' style="margin-top:30px"' if i else ""
            out.append(f'        <h2{style}>{group["title"]}</h2>')
            out.append("        <ul>")
            links = family_links(site) if group.get("family") else group.get("links", [])
            for link in links:
                if "href" in link:
                    href = href_for(site, link)
                    out.append(f'          <li><a href="{href}"{rel_for(href)}>{link["label"]}</a></li>')
                else:
                    out.append(f'          <li><span>{link["text"]}</span></li>')
            out.append("        </ul>")
        out.append("      </div>")
    return "\n".join(out)


def org_schema(site, url):
    org = site["organization"]
    return {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": org["name"],
        "url": url,
        "logo": url + org.get("logo", "/icon-512.png"),
        "parentOrganization": {"@type": "Organization", "name": "7 Signals LLC", "url": "https://7signals.io"},
        "address": {"@type": "PostalAddress", **org["address"]},
        "email": org["email"],
        "telephone": org["telephone"],
    }


DEFAULT_ICONS = [
    {"href": "/favicon.ico", "sizes": "32x32"},
    {"href": "/favicon.svg", "type": "image/svg+xml"},
    {"rel": "apple-touch-icon", "href": "/apple-touch-icon.png"},
]
DEFAULT_LEGAL = [
    {"label": "Privacy Policy", "href": "/privacy-policy/"},
    {"label": "Terms &amp; Conditions", "href": "/terms/"},
]


def icon_links(site):
    out = []
    for i in site.get("icons", DEFAULT_ICONS):
        attrs = f' href="{i["href"]}"'
        attrs += f' sizes="{i["sizes"]}"' if i.get("sizes") else ""
        attrs += f' type="{i["type"]}"' if i.get("type") else ""
        out.append(f'<link rel="{i.get("rel", "icon")}"{attrs}>')
    return "\n".join(out)


def og_image_meta(site, url):
    """Social image tags. Left out when the site has no og_image yet."""
    if not site.get("og_image"):
        return "", ""
    img = f"{url}{site['og_image']}"
    alt = html.escape(site.get("og_image_alt", site["brand"]), quote=True)
    og = (f'\n<meta property="og:image" content="{img}">'
          '\n<meta property="og:image:width" content="1200">'
          '\n<meta property="og:image:height" content="630">'
          f'\n<meta property="og:image:alt" content="{alt}">')
    return og, f'\n<meta name="twitter:image" content="{img}">'


def legal_href(site, word, default):
    for link in site["footer"].get("legal", DEFAULT_LEGAL):
        if word in link["label"]:
            return link["href"]
    return default


def section_context(site):
    """Values the shared sections (partials/sections/*.html) are filled with."""
    words, pricing = site["words"], site["pricing"]
    ctx = {**words, "brand": site["brand"], "demo_url": site["demo_url"], "lead_endpoint": site["lead_endpoint"],
           "report_href": href_for(site, {"key": "report", "href": "/industry-report/"}),
           "privacy_href": legal_href(site, "Privacy", "/privacy-policy/"),
           "terms_href": legal_href(site, "Terms", "/terms/")}
    checkout = pricing.get("checkout_url") or "/contact/?plan=subscription"
    ctx.update({
        "plan_name": pricing["plan_name"], "price": pricing["price"], "price_note": pricing["price_note"],
        "checkout_url": checkout, "checkout_rel": rel_for(checkout), "checkout_label": pricing["checkout_label"],
        "checkout_fine": "Secure checkout by Stripe" if pricing.get("checkout_url") else "We'll set up your account with you",
    })
    item = lambda t: "          <li>" + render(t, ctx) + "</li>"
    ctx["plan_items"] = "\n".join(item(t) for t in pricing["plan_items"])
    ctx["custom_items"] = "\n".join(item(t) for t in pricing["custom_items"])
    return ctx


def expand_includes(body, ctx, page_name):
    """Swap each <!--core:NAME--> in a page for the shared section partials/sections/NAME.html."""
    def one(m):
        f = CORE / "partials/sections" / f"{m.group(1)}.html"
        if not f.exists():
            raise SystemExit(f"{page_name}: unknown shared section <!--core:{m.group(1)}-->")
        return render(f.read_text(), ctx)
    return INCLUDE_RE.sub(one, body)


def head_extra(*parts):
    """Raw HTML added at the end of <head>: the site's first, then the page's own."""
    return "".join("\n" + p.strip() for p in parts if p and p.strip())


def tracking_html(site):
    t = site.get("tracking", {})
    lines = []
    if t.get("uxwizz"):
        lines.append('<script>UST_CT = [];UST = { s: Date.now(), addTag: function(tag) { UST_CT.push(tag) } };UST.addEvent = UST.addTag;</script>')
        lines.append('<script src="https://analytics.marketscore.agency/userTrack/server/ust.min.js?v=10.3.0" async></script>')
    if t.get("pipelineon_tag"):
        lines.append(f'<script async defer src="https://pp-n.com/p.js" data-po-tag="{t["pipelineon_tag"]}"></script>')
    return "\n".join(lines)


def build(root):
    root = pathlib.Path(root).resolve()
    src, out = root / "src", root / "public"
    site = load_site(root)
    url = site["site_url"].rstrip("/")
    version = time.strftime("%Y%m%d%H%M")

    layout = (CORE / "partials/layout.html").read_text()
    header = (CORE / "partials/header.html").read_text()
    footer = (CORE / "partials/footer.html").read_text()

    mark = site["mark"]
    mark_light_file = src / "partials/mark-light.html"
    mark_light = (mark_light_file.read_text().strip() if mark_light_file.exists()
                  else f'<img class="brand__mark" src="{mark["src"]}" alt="" width="{mark["width"]}" height="{mark["height"]}">')
    cta = site["cta"]
    common = {
        "brand": site["brand"], "brand_word": brand_word(site),
        "mark_src": mark["src"], "mark_width": mark["width"], "mark_height": mark["height"],
        "mark_light": mark_light, "login_url": site["login_url"],
        "cta_href": cta["href"], "cta_rel": rel_for(cta["href"]),
        "cta_label": cta["label"], "cta_label_long": cta.get("label_long", cta["label"]),
        "footer_blurb": site["footer"]["blurb"], "year": datetime.date.today().year,
        "legal_links": "".join(f'<a href="{l["href"]}">{l["label"]}</a>' for l in site["footer"].get("legal", DEFAULT_LEGAL)),
    }
    preloads = "\n".join(f'<link rel="preload" href="{f}" as="font" type="font/woff2" crossorigin>' for f in site.get("preload_fonts", []))
    og_meta, twitter_meta = og_image_meta(site, url)
    icons = icon_links(site)
    sections = section_context(site)
    scripts = "\n".join(f'<script src="{s["src"]}?v={version}"{" defer" if s.get("defer") else ""}></script>' for s in site.get("scripts", []))

    pages = []
    for page in (src / "pages").glob("*.html"):
        raw = page.read_text()
        m = META_RE.match(raw)
        if not m:
            raise SystemExit(f"{page.name}: missing <!--meta {{...}} --> block")
        pages.append((page.name, json.loads(m.group(1)), raw[m.end():]))

    # Industry report: built from content/industry-report.json when the site has one (docs/industry-report.md).
    report_json = root / "content/industry-report.json"
    if report_json.exists():
        if any(name == "industry-report.html" for name, _, _ in pages):
            raise SystemExit("Both content/industry-report.json and src/pages/industry-report.html exist; keep one.")
        pages.append(("industry-report.html", *report.render(report.load(report_json), site)))

    # Use cases: built from content/use-cases.json when the site has one (docs/use-cases.md).
    uc_json = root / "content/use-cases.json"
    if uc_json.exists():
        if any(name == "use-cases.html" for name, _, _ in pages):
            raise SystemExit("Both content/use-cases.json and src/pages/use-cases.html exist; keep one.")
        pages.append(("use-cases.html", *usecases.render(usecases.load(uc_json), site)))

    # The standard "Use cases" menu and footer links only show on sites that have the page.
    if not any(meta["path"] == "/use-cases/" for _, meta, _ in pages) and "usecases" not in site.get("hrefs", {}):
        drop_link(site, "usecases")
    footer_html = render(footer, {**common, "footer_columns": footer_columns_html(site)})

    sitemap = []
    for name, meta, raw_body in sorted(pages, key=lambda p: p[0]):
        page_head = meta.get("head", "")
        if hero.MARKER in raw_body:
            # Standard hero (docs/hero.md): needs a "hero" block in site.json.
            if "hero" not in site:
                raise SystemExit(f"{name}: <!--core:hero--> needs a \"hero\" block in site.json (see docs/hero.md)")
            raw_body = re.sub(re.escape(hero.MARKER) + r"\n?", lambda _m: hero.render(site, root), raw_body)
            page_head = head_extra(page_head, hero.head(site)).lstrip("\n")
        body = expand_includes(raw_body, sections, name)
        path = meta["path"]
        nav_links, mobile_links = nav_html(site, meta.get("nav", ""))
        schemas = [org_schema(site, url)] if path == "/" else []
        schemas += meta.get("schema", [])
        schema_html = "\n".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schemas)
        ctx = {
            **common,
            "title": meta["title"], "description": meta["description"],
            "og_title": meta.get("og_title", meta["title"]), "og_type": meta.get("og_type", "website"),
            "robots": meta.get("robots", "index, follow"), "site": url, "path": path,
            "theme_light": site["theme_color"]["light"], "theme_dark": site["theme_color"]["dark"],
            "og_image_meta": og_meta, "twitter_image_meta": twitter_meta, "icon_links": icons,
            "head_extra": head_extra(site.get("head", ""), page_head),
            "font_preloads": preloads, "stylesheet": site["stylesheet"], "version": version,
            "schema": schema_html, "tracking": tracking_html(site), "scripts": scripts,
            "body_class": meta.get("body_class", ""),
            "header": render(header, {**common, "nav_links": nav_links, "mobile_links": mobile_links}),
            "footer": footer_html, "content": body,
        }
        page_html = render(layout, ctx)
        dest = out / ("404.html" if path == "/404" else (path.strip("/") + "/index.html" if path != "/" else "index.html"))
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(page_html)
        if meta.get("sitemap", True) and "noindex" not in ctx["robots"]:
            sitemap.append((path, meta.get("priority", "0.7")))
        print(f"built {dest.relative_to(root)}")

    today = datetime.date.today().isoformat()
    urls = "\n".join(f"  <url><loc>{url}{p}</loc><lastmod>{today}</lastmod><priority>{pr}</priority></url>" for p, pr in sitemap)
    (out / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n')
    print("built public/sitemap.xml")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--site", default=".", help="path to the site repo (default: current folder)")
    build(ap.parse_args().site)
