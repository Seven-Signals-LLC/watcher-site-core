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
import argparse, datetime, html, json, pathlib, re, time

CORE = pathlib.Path(__file__).resolve().parent
META_RE = re.compile(r"^\s*<!--meta\s+(\{.*?\})\s*-->\s*", re.S)


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
        href, label = item["href"], item["label"]
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
                    out.append(f'          <li><a href="{link["href"]}"{rel_for(link["href"])}>{link["label"]}</a></li>')
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
        "logo": f"{url}/icon-512.png",
        "parentOrganization": {"@type": "Organization", "name": "7 Signals LLC", "url": "https://7signals.io"},
        "address": {"@type": "PostalAddress", **org["address"]},
        "email": org["email"],
        "telephone": org["telephone"],
    }


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
    site = json.loads((root / "site.json").read_text())
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
    }
    footer_html = render(footer, {**common, "footer_columns": footer_columns_html(site)})
    preloads = "\n".join(f'<link rel="preload" href="{f}" as="font" type="font/woff2" crossorigin>' for f in site.get("preload_fonts", []))
    scripts = "\n".join(f'<script src="{s["src"]}?v={version}"{" defer" if s.get("defer") else ""}></script>' for s in site.get("scripts", []))

    sitemap = []
    for page in sorted((src / "pages").glob("*.html")):
        raw = page.read_text()
        m = META_RE.match(raw)
        if not m:
            raise SystemExit(f"{page.name}: missing <!--meta {{...}} --> block")
        meta = json.loads(m.group(1))
        body = raw[m.end():]
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
            "og_image": site["og_image"], "og_image_alt": html.escape(site["og_image_alt"], quote=True),
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
