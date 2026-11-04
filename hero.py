"""Standard Watcher hero: renders <!--core:hero--> from site.json "hero".

A full-bleed photograph behind the home page's first screen, an ink scrim on the
text side, and the headline, one line and the demo action set low-left. A site can
place one card on the photo (src/partials/hero-aside.html), for example a sample
market ranking. Styling ships with the section (partials/hero.css) and picks up
the site's colours and fonts through site.json "core_theme" (see docs/hero.md).
"""
import html, pathlib

CORE = pathlib.Path(__file__).resolve().parent
ESC = lambda s: html.escape(str(s), quote=True)
MARKER = "<!--core:hero-->"

# site.json "core_theme" key -> CSS custom property the hero styling reads.
THEME_VARS = {
    "dark": "--ch-dark", "on_dark": "--ch-on-dark", "dark_muted": "--ch-on-dark-muted",
    "accent": "--ch-accent", "serif": "--ch-display", "sans": "--ch-sans",
}


def _srcset(img):
    return ", ".join(f"{s['src']} {s['w']}w" for s in img.get("srcset", []))


def head(site):
    """Preload for the hero photo and the section's styles, for the page <head>."""
    img = site["hero"]["image"]
    srcset = _srcset(img)
    pre = (f'<link rel="preload" as="image" href="{img["src"]}"'
           + (f' imagesrcset="{srcset}" imagesizes="100vw"' if srcset else "")
           + ' fetchpriority="high">')
    css = (CORE / "partials/hero.css").read_text().strip()
    theme = site.get("core_theme", {})
    decls = ";".join(f"{THEME_VARS[k]}:{v}" for k, v in theme.items() if k in THEME_VARS)
    return pre + f"\n<style>{css}" + (f".core-hero{{{decls}}}" if decls else "") + "</style>"


def render(site, root):
    """The hero section's HTML. Shared markers inside it (demo button, trust line) are expanded by the build."""
    h = site["hero"]
    img = h["image"]
    srcset = _srcset(img)
    pos = f' style="object-position:{img["position"]}"' if img.get("position") else ""
    img_tag = (f'<img src="{img["src"]}"' + (f' srcset="{srcset}" sizes="100vw"' if srcset else "")
               + f' width="{img["width"]}" height="{img["height"]}" alt="{ESC(img["alt"])}"{pos}'
               + ' fetchpriority="high" decoding="async">')
    sec = h.get("secondary")
    secondary = f'\n        <a class="btn btn--ghost" href="{sec["href"]}">{sec["label"]}</a>' if sec else ""
    aside_file = pathlib.Path(root) / "src/partials/hero-aside.html"
    aside = f'\n    <div class="core-hero__aside">\n{aside_file.read_text().rstrip()}\n    </div>' if aside_file.exists() else ""
    return f"""<section class="core-hero" aria-labelledby="hero-title">
  <figure class="core-hero__photo" data-slot="hero-image">
    {img_tag}
  </figure>
  <div class="core-hero__scrim" aria-hidden="true"></div>
  <div class="wrap core-hero__grid">
    <div class="core-hero__text">
      <h1 id="hero-title">{h["title"]}</h1>
      <p class="core-hero__lead">{h["lead"]}</p>
      <div class="core-hero__actions">
        <!--core:demo-button-->{secondary}
      </div>
      <!--core:demo-trust-->
    </div>{aside}
  </div>
</section>
"""
