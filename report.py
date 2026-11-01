"""Industry report page: renders content/industry-report.json into /industry-report/.

The JSON is drafted from the research document in the site's research/ folder
(see docs/industry-report.md). This module only lays it out; every word and
number comes from the JSON.
"""
import json, math

I8 = " " * 8


def _pct(value, axis_max):
    """Position on a 0..axis_max scale as a percentage, rounded down to 0.1 ("66.6", "25")."""
    p = math.floor(value / axis_max * 1000) / 10
    return f"{p:g}"


def _prose(b):
    lines = [(I8 + l) if l else "" for l in b["html"]]
    if b.get("wrap", True):
        return f'{I8}<div style="max-width:68ch">\n' + "\n".join(lines) + f"\n{I8}</div>"
    return "\n".join(lines)


def _growth(b):
    cols = []
    for bar in b["bars"]:
        cls = "growth__bar fc" if bar.get("forecast") else "growth__bar"
        cols.append(f'            <div class="growth__col"><span class="growth__val">{bar["value"]}</span>'
                    f'<span class="{cls}" style="--h:{bar["height"]}%" title="{bar["title"]}"></span></div>')
    years = "".join(f'<span class="growth__yr" style="flex:1;max-width:140px">{bar["label"]}</span>' for bar in b["bars"])
    return "\n".join([
        f'{I8}<div class="figure-block" role="figure" aria-labelledby="{b["id"]}">',
        f'          <h3 id="{b["id"]}">{b["title"]}</h3>',
        f'          <p class="sub">{b["sub"]}</p>',
        '          <div class="growth">', *cols, '          </div>',
        f'          <div style="display:flex;gap:clamp(18px,4vw,48px);max-width:560px">{years}</div>',
        f"{I8}</div>"])


def _range(b):
    axis_max = b["axis"][-1]["value"]
    rows = []
    for r in b["rows"]:
        a, z = _pct(r["min"], axis_max), _pct(r["max"], axis_max)
        rows.append(f'            <span class="range__label">{r["label"]}</span>')
        rows.append(f'            <span class="range__track"><span class="range__bar" style="--a:{a}%;--b:{z}%" tabindex="0" '
                    f'title="{r["title"]}"><span>{r["display"]}</span></span></span>')
    axis = "".join(f'<span>{t["label"]}</span>' for t in b["axis"])
    return "\n".join([
        f'{I8}<div class="figure-block" role="figure" aria-labelledby="{b["id"]}">',
        f'          <h3 id="{b["id"]}">{b["title"]}</h3>',
        f'          <p class="sub">{b["sub"]}</p>',
        '          <div class="range">', *rows,
        f'            <span class="range__axis">{axis}</span>',
        '          </div>', f"{I8}</div>"])


def _pullstat(b):
    items = [f'          <div><strong>{s["value"]}</strong><span>{s["label"]}</span></div>' for s in b["stats"]]
    return "\n".join([f'{I8}<div class="pullstat">', *items, f"{I8}</div>"])


def _table(b):
    head = "".join(f'<th scope="col">{h}</th>' for h in b["columns"])
    rows = [f'              <tr><th scope="row">{r[0]}</th>' + "".join(f"<td>{c}</td>" for c in r[1:]) + "</tr>" for r in b["rows"]]
    return "\n".join([
        f'{I8}<div class="dtable-wrap">', '          <table class="dtable">',
        f'            <caption>{b["caption"]}</caption>',
        f'            <thead><tr>{head}</tr></thead>', '            <tbody>', *rows, '            </tbody>',
        '          </table>', f"{I8}</div>"])


def _funnel(b):
    stages = []
    for s in b["stages"]:
        tags = "".join(f"<li>{t}</li>" for t in s["tags"])
        stages.append(f'          <div class="funnel__stage"><div><h3>{s["title"]}</h3>'
                      f'<p class="small" style="margin-bottom:12px">{s["text"]}</p><ul>{tags}</ul></div></div>')
    return "\n".join([f'{I8}<div class="funnel">', *stages, f"{I8}</div>"])


def _sources(sources):
    items = [f'          <li id="s-{s["n"]}">{s["text"]} <a href="{s["url"]}" rel="noopener">{s["site"]}</a></li>' for s in sources]
    return "\n".join([f'{I8}<h2 id="sources">Works cited</h2>', f'{I8}<ol class="sources">', *items, f"{I8}</ol>"])


BLOCKS = {"prose": _prose, "growth": _growth, "range": _range, "pullstat": _pullstat,
          "table": _table, "funnel": _funnel}


def render(report, site):
    """Return (meta, body) for the industry report page."""
    hero, close = report["hero"], report["closing"]
    cta = site["cta"]
    parts = []
    for i, b in enumerate(report["blocks"]):
        html = BLOCKS[b["type"]](b)
        if i:
            parts.append("\n" * (b.get("gap", 1) + 1))
        parts.append(html)
    parts.append("\n\n" + _sources(report["sources"]))
    toc = "\n".join(f'          <li><a href="#{t["id"]}">{t["label"]}</a></li>' for t in report["toc"])
    meta_row = "".join(f"<span>{m}</span>" for m in hero["meta_row"])
    body = f"""<section class="page-hero" aria-labelledby="rep-title">
  <div class="wrap">
    <p class="eyebrow"><span class="no">{hero["eyebrow_no"]}</span> {hero["eyebrow"]}</p>
    <h1 class="display" id="rep-title">{hero["title"]}</h1>
    <p class="lede">{hero["lede"]}</p>
    <div class="meta-row">{meta_row}</div>
  </div>
</section>

<section class="section" style="padding-top:clamp(56px,7vw,104px)">
  <div class="wrap">
    <div class="article">
      <nav class="toc" aria-label="Report contents">
        <span class="label">Contents</span>
        <ol>
{toc}
        </ol>
      </nav>

      <article class="prose" style="max-width:none">
{"".join(parts)}
      </article>
    </div>
  </div>
</section>

<section class="section band-night on-night closing" style="text-align:left">
  <div class="wrap">
    <div class="sec-head" style="margin-bottom:0">
      <div>
        <p class="eyebrow"><span class="no">{close["eyebrow_no"]}</span> {close["eyebrow"]}</p>
        <h2 class="h2">{close["title"]}</h2>
      </div>
      <div>
        <p class="lede" style="margin:0 0 32px">{close["lede"]}</p>
        <a class="btn btn--light" href="{cta["href"]}"{' rel="noopener"' if cta["href"].startswith("http") else ""}>{cta.get("label_long", cta["label"])} <span class="arr" aria-hidden="true"></span></a>
      </div>
    </div>
  </div>
</section>
"""
    return report["meta"], body


def load(path):
    return json.loads(path.read_text())
