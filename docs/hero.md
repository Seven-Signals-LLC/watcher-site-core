# The standard hero: `<!--core:hero-->`

Every Watcher home page opens the same way: a full-bleed photograph of the trade's own work behind the first screen, an ink scrim on the text side, and the headline, one line and the demo action set low-left. GroutWatcher is the reference.

Put `<!--core:hero-->` at the top of `src/pages/home.html` and add a `hero` block to `site.json`. The core builds the section, preloads the photo in the page `<head>` and ships the section's styles. Pages without the marker build exactly as before.

## site.json

```json
"hero": {
  "title": "Every tile showroom near you, ranked.",
  "lead": "See where your tile business stands on the seven signals buyers judge.",
  "image": {
    "src": "/assets/img/hero-1600.webp",
    "srcset": [
      {"src": "/assets/img/hero-960.webp", "w": 960},
      {"src": "/assets/img/hero-1600.webp", "w": 1600},
      {"src": "/assets/img/hero-2400.webp", "w": 2400}
    ],
    "width": 2400, "height": 1340,
    "alt": "What the photo shows, in plain words",
    "position": "72% 55%"
  },
  "secondary": {"label": "See the seven signals", "href": "#signals"}
}
```

| Key | What it is |
|---|---|
| `title` | The headline: seven words or fewer, the trade's own nouns |
| `lead` | One sentence, twelve words or fewer |
| `image` | The photo: `src`, optional `srcset` (`src`, `w`), `width`, `height`, `alt`, optional `position` (CSS `object-position`, to keep the subject clear of the text) |
| `secondary` | Optional second button beside **See the demo for free** |

The primary button and the trust line under it are the shared `demo-button` and `demo-trust` sections.

## The photo

- The trade's real work, landscape, 2400px wide or more, with a darker or calmer side for the text. Export 960, 1600 and 2400px WebP versions.
- Use `position` to move the subject away from the text side (the text sits on the left on desktop, at the bottom on phones).
- Never a stock photo of people standing in for customers, and never text baked into the image.

## A card on the photo (optional)

Put HTML in `src/partials/hero-aside.html` and the core places it bottom-right on desktop and under the actions on phones (GroutWatcher puts its sample market ranking there). The card's styles live in the site's stylesheet. Leave the file out for a text-only hero.

## Styling

The section is scoped to `.core-hero` and takes its colours and fonts from `core_theme` in `site.json`:

| `core_theme` key | Used for |
|---|---|
| `dark` | Background behind the photo and the scrim |
| `on_dark` | Headline and buttons |
| `dark_muted` | Lead line and trust line |
| `accent` | Reserved for site accents |
| `serif` | Headline face |
| `sans` | Lead line face |

The site's `.btn` and `.btn--ghost` are reused and inverted for the dark photo. If the site's sticky header is not 74px tall, set `.core-hero{--ch-header:<height>}` in the site stylesheet so the hero fills exactly one screen.

## With Hallmark

The hero is the core's standard, so a Hallmark run on a Watcher site keeps it: stamp `hero: Poster (core standard)` and answer the theme's photo rules against it. Hallmark still decides the rest of the page.
