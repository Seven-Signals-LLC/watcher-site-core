"""Use cases page: renders content/use-cases.json into /use-cases/.

Same layout on every Watcher site: hero, platform proof strip, an index of the
plays, one block per use case (question, outcome, three steps, signals and a
visual), and a closing demo section. Every word and number comes from the JSON
(see docs/use-cases.md). Styling ships with the page (partials/use-cases.css)
and picks up the site's colours and fonts through site.json "core_theme".
"""
import html, json, pathlib

CORE = pathlib.Path(__file__).resolve().parent
ESC = lambda s: html.escape(str(s), quote=True)

# site.json "core_theme" key -> CSS custom property the page styling reads.
THEME_VARS = {
    "bg": "--uc-bg", "band": "--uc-band", "card": "--uc-card", "line": "--uc-line",
    "text": "--uc-text", "muted": "--uc-muted", "ink": "--uc-ink",
    "accent": "--uc-accent", "accent_text": "--uc-accent-text", "good": "--uc-good", "bad": "--uc-bad",
    "dark": "--uc-dark", "on_dark": "--uc-on-dark", "dark_muted": "--uc-dark-muted",
    "serif": "--uc-serif", "sans": "--uc-sans", "mono": "--uc-mono", "radius": "--uc-radius",
}


def _tag(kind):
    if kind == "real":
        return '<span class="uc-tag uc-tag--real">Real data</span>'
    return '<span class="uc-tag">Example</span>'


def _chip(v):
    """Table cells: yes / no / gap / open become chips; anything else is plain text."""
    m = {"yes": ("Yes", "ok"), "no": ("No", "no"), "has": ("Has page", "ok"), "none": ("No page", "no"),
         "gap": ("Gap", "gap"), "open": ("Open", "open")}
    if isinstance(v, str) and v.lower() in m:
        label, cls = m[v.lower()]
        return f'<span class="uc-chip uc-chip--{cls}">{label}</span>'
    return str(v)


def _note(v):
    return f'\n          <p class="uc-note">{v["note"]}</p>' if v.get("note") else ""


def _head(v):
    return (f'          <div class="uc-vis__head"><h4>{v.get("title", "")}</h4>{_tag(v.get("tag", "example"))}</div>')


def _heatmap(v):
    you, opens = tuple(v.get("you", [-1, -1])), {tuple(o) for o in v.get("open", [])}
    cells = []
    for r, row in enumerate(v["grid"]):
        for c, lvl in enumerate(row):
            mark = ""
            if (r, c) == you:
                mark = ' uc-heat__cell--you'
            elif (r, c) in opens:
                mark = ' uc-heat__cell--open'
            cells.append(f'<span class="uc-heat__cell{mark}" data-l="{lvl}"></span>')
    cols = len(v["grid"][0])
    legend = ('<div class="uc-heat__legend"><span>Low</span><span class="uc-heat__scale" aria-hidden="true"></span><span>High</span>'
              '<span class="uc-heat__key uc-heat__key--open">Open ground</span><span class="uc-heat__key uc-heat__key--you">Your location</span></div>')
    return "\n".join([
        _head(v),
        f'          <div class="uc-heat" style="--cols:{cols}" role="img" aria-label="{ESC(v.get("alt", v.get("title", "")))}">{"".join(cells)}</div>',
        f"          {legend}"]) + _note(v)


def _battlecard(v):
    quads = []
    for q in v["quads"]:
        items = "".join(f"<li>{i}</li>" for i in q["items"])
        quads.append(f'            <div class="uc-quad uc-quad--{q.get("tone", "neutral")}"><p class="uc-label">{q["label"]}</p><ul>{items}</ul></div>')
    talk = (f'\n          <blockquote class="uc-talk"><p class="uc-label">Talk track</p><p>{v["talk"]}</p></blockquote>'
            if v.get("talk") else "")
    return "\n".join([_head(v), '          <div class="uc-quads">', *quads, "          </div>"]) + talk + _note(v)


def _adgap(v):
    def col(c, cls):
        items = "".join(f"<li>{i}</li>" for i in c["items"])
        return f'<div class="uc-gap__col uc-gap__col--{cls}"><p class="uc-label">{c["label"]}</p><ul>{items}</ul></div>'
    ad = v.get("ad")
    ad_html = ""
    if ad:
        ad_html = ("\n          <div class=\"uc-ad\"><p class=\"uc-ad__spon\">Sponsored</p>"
                   f"<p class=\"uc-ad__url\">{ad['url']}</p><p class=\"uc-ad__h\">{ad['headline']}</p><p class=\"uc-ad__t\">{ad['text']}</p></div>")
    return "\n".join([_head(v), f'          <div class="uc-gap">{col(v["left"], "same")}{col(v["right"], "open")}</div>']) + ad_html + _note(v)


def _bars(v):
    mx = v.get("max", 5)
    rows = []
    for r in v["rows"]:
        w = round(r["value"] / mx * 100, 1)
        rows.append(f'            <div class="uc-bar"><span class="uc-bar__label">{r["label"]}</span>'
                    f'<span class="uc-bar__track"><span class="uc-bar__fill" style="width:{w:g}%"></span></span>'
                    f'<span class="uc-bar__val">{r["value"]:g}</span></div>')
    bench = v.get("benchmark")
    bench_style = f' style="--bench:{round(bench / mx * 100, 1):g}%"' if bench else ""
    legend = ""
    if v.get("legend"):
        legend = '\n          <div class="uc-legend">' + "".join(
            f'<span class="uc-legend__{k}">{t}</span>' for k, t in v["legend"].items()) + "</div>"
    return "\n".join([_head(v), f'          <div class="uc-bars{" uc-bars--bench" if bench else ""}"{bench_style}>', *rows, "          </div>"]) + legend + _note(v)


def _stats(v):
    items = "".join(f'<div><dd>{s["value"]}</dd><dt>{s["label"]}</dt></div>' for s in v["stats"])
    return "\n".join([_head(v), f'          <dl class="uc-stats">{items}</dl>']) + _note(v)


def _table(v):
    head = "".join(f'<th scope="col">{c}</th>' for c in v["columns"])
    rows = []
    for r in v["rows"]:
        cls = ' class="uc-row--you"' if r.get("you") else ""
        cells = r["cells"]
        rows.append(f'              <tr{cls}><th scope="row">{cells[0]}</th>' + "".join(f"<td>{_chip(c)}</td>" for c in cells[1:]) + "</tr>")
    return "\n".join([_head(v), '          <div class="uc-table-wrap"><table class="uc-table">',
                      f"            <thead><tr>{head}</tr></thead>", "            <tbody>", *rows,
                      "            </tbody>", "          </table></div>"]) + _note(v)


def _themes(v):
    mx = max(r["value"] for r in v["rows"])
    rows = []
    for r in v["rows"]:
        kind = r.get("kind", "praise")
        sub = ' <small>(complaint)</small>' if kind == "complaint" else ""
        rows.append(f'            <div class="uc-bar uc-bar--{kind}"><span class="uc-bar__label">{r["label"]}{sub}</span>'
                    f'<span class="uc-bar__track"><span class="uc-bar__fill" style="width:{round(r["value"] / mx * 100, 1):g}%"></span></span>'
                    f'<span class="uc-bar__val">{r["value"]}</span></div>')
    legend = '\n          <div class="uc-legend"><span class="uc-legend__praise">Praise</span><span class="uc-legend__complaint">Complaints</span></div>'
    return "\n".join([_head(v), '          <div class="uc-bars">', *rows, "          </div>"]) + legend + _note(v)


def _quote(v):
    return (f'          <figure class="uc-quote"><blockquote>{v["text"]}</blockquote>'
            f'<figcaption>{v["source"]} {_tag(v.get("tag", "real"))}</figcaption></figure>')


VISUALS = {"heatmap": _heatmap, "battlecard": _battlecard, "adgap": _adgap, "bars": _bars,
           "stats": _stats, "table": _table, "themes": _themes, "quote": _quote}


def _case(i, c):
    flip = " uc-case--flip" if i % 2 else ""
    steps = "".join(f"<li>{s}</li>" for s in c["steps"])
    signals = "".join(f"<li>{s}</li>" for s in c["signals"])
    visuals = "\n".join(
        f'        <div class="uc-vis{" uc-vis--bare" if v["type"] == "quote" else ""}">\n{VISUALS[v["type"]](v)}\n        </div>'
        for v in c.get("visuals", []))
    plays = ""
    if c.get("plays"):
        items = "".join(f'<div class="uc-play"><h4>{p["title"]}</h4><p>{p["text"]}</p></div>' for p in c["plays"])
        plays = f'\n    <div class="uc-plays">{items}</div>'
    outcome = (f'\n        <div class="uc-outcome"><p class="uc-label">What you walk away with</p><p>{c["outcome"]}</p></div>'
               if c.get("outcome") else "")
    stepblock = (f'\n        <div class="uc-steps"><p class="uc-label">How to use it</p><ol>{steps}</ol></div>' if steps else "")
    return f"""<section class="uc-case{flip}" id="{c["id"]}" aria-labelledby="{c["id"]}-title">
  <div class="wrap">
    <div class="uc-case__grid">
      <div class="uc-case__text">
        <p class="uc-kicker"><span class="uc-num">{i + 1:02d}</span> Use case · {c["kicker"]}</p>
        <h2 class="uc-h2" id="{c["id"]}-title">{c["title"]}</h2>
        <p class="uc-intro">{c["intro"]}</p>
        <p class="uc-question">{c["question"]}</p>{outcome}{stepblock}
        <div class="uc-signals"><p class="uc-label">Signals used</p><ul>{signals}</ul></div>
      </div>
      <div class="uc-case__visual">
{visuals}
      </div>
    </div>{plays}
  </div>
</section>"""


def theme_style(site):
    """Inline :root-level variables mapping the site's palette onto the page styling."""
    theme = site.get("core_theme", {})
    decls = ";".join(f"{THEME_VARS[k]}:{v}" for k, v in theme.items() if k in THEME_VARS)
    return f".core-uc{{{decls}}}" if decls else ""


def render(uc, site):
    """Return (meta, body) for the use cases page."""
    hero, proof, close = uc["hero"], uc.get("proof"), uc["closing"]
    cta = site["cta"]
    cta_rel = ' rel="noopener"' if cta["href"].startswith("http") else ""
    contact = site.get("hrefs", {}).get("contact", "/contact/")

    css = (CORE / "partials/use-cases.css").read_text().strip()
    meta = dict(uc["meta"])
    meta.setdefault("path", "/use-cases/")
    meta.setdefault("nav", "usecases")
    meta["head"] = "\n".join(p for p in [meta.get("head", ""), f"<style>{css}{theme_style(site)}</style>"] if p)

    proof_html = ""
    if proof:
        stats = "".join(f'<div><dt>{s["label"]}</dt><dd>{s["value"]}</dd></div>' for s in proof["stats"])
        proof_html = f"""
<section class="uc-proof" aria-labelledby="uc-proof-title">
  <div class="wrap">
    <div class="uc-proof__head"><h2 class="uc-label" id="uc-proof-title">{proof["title"]}</h2>{_tag("real")}</div>
    <dl class="uc-proof__grid">{stats}</dl>
    <p class="uc-note">{proof["note"]}</p>
  </div>
</section>
"""
    index = "".join(f'<li><a href="#{c["id"]}">{c.get("short", c["title"])}</a></li>' for c in uc["cases"])
    cases = "\n\n".join(_case(i, c) for i, c in enumerate(uc["cases"]))
    fine = f'\n    <p class="uc-fine">{close["fine"]}</p>' if close.get("fine") else ""

    body = f"""<div class="core-uc">
<section class="uc-hero" aria-labelledby="uc-title">
  <div class="wrap uc-hero__grid">
    <div>
      <p class="uc-kicker">{hero["eyebrow"]}</p>
      <h1 class="uc-h1" id="uc-title">{hero["title"]}</h1>
      <p class="uc-lede">{hero["lede"]}</p>
    </div>
    <aside class="uc-howto" aria-label="How to read this page">
      <p class="uc-label">How to read this page</p>
      <p>Each block names <strong>the question it answers</strong>, <strong>what you walk away with</strong>, and <strong>the signals that feed it</strong>. Then three steps your team can run this week.</p>
      <p>Visuals marked {_tag("example")} show the shape of the output. Blocks marked {_tag("real")} come from our live database.</p>
    </aside>
  </div>
</section>
{proof_html}
<nav class="uc-index" aria-label="Use cases on this page">
  <div class="wrap"><ol>{index}</ol></div>
</nav>

{cases}

<section class="uc-closing" aria-labelledby="uc-close-title">
  <div class="wrap">
    <p class="uc-kicker">{close["eyebrow"]}</p>
    <h2 class="uc-h2" id="uc-close-title">{close["title"]}</h2>
    <p class="uc-lede">{close["lede"]}</p>
    <div class="uc-closing__ctas">
      <a class="btn uc-btn" href="{cta["href"]}"{cta_rel}>{close.get("button", cta.get("label_long", cta["label"]))}</a>
      <a class="uc-btn-line" href="{contact}">{close.get("secondary", "Talk to the team")}</a>
    </div>{fine}
  </div>
</section>
</div>
"""
    return meta, body


def load(path):
    return json.loads(path.read_text())
