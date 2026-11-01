# Use cases: the standard /use-cases/ page

Every Watcher site has a "Use cases" page at `/use-cases/`: seven plays a business runs with its Watcher data (expansion map, SWOT battle card, ads engine, website leakage, lead responsiveness, content engine, voice of the customer). The layout and styling live in the core, so every site looks and reads the same. Each site supplies only its own words in `content/use-cases.json`.

- When `content/use-cases.json` exists, the core builds `/use-cases/` from it and adds it to the sitemap.
- The standard menu (`defaults.json`) includes **Use cases**. On a site with no use-cases page, the core drops that menu item and any footer link with `"key": "usecases"`, so nothing links to a missing page.
- A site that still has a hand-written `src/pages/use-cases.html` (DecorWatcher today) keeps it. Having both files stops the build.

## Styling

The page carries its own CSS (`partials/use-cases.css`, scoped to `.core-uc`). It only needs `.wrap` and `.btn` from the site stylesheet. It picks up the site's palette and fonts from `core_theme` in `site.json`; any key left out uses a neutral default:

```json
"core_theme": {
  "bg": "var(--paper)", "band": "var(--paper-2)", "card": "var(--card)", "line": "var(--line)",
  "text": "var(--text)", "muted": "var(--muted)", "ink": "var(--ink)",
  "accent": "var(--copper)", "accent_text": "#fff", "good": "var(--signal-dk)", "bad": "#b4483a",
  "dark": "var(--slate)", "on_dark": "#e6ece8", "dark_muted": "#a9b8b0",
  "serif": "var(--serif)", "sans": "var(--sans)", "mono": "var(--mono)", "radius": "var(--radius)"
}
```

## Instructions for Claude: drafting content/use-cases.json

Start from an existing site's file (FencePostWatcher's is the reference) and rewrite it for the vertical in `site.json`.

- Keep the seven cases, their order, ids and `signals`. Rewrite `intro`, `question`, `outcome`, `steps` and the example visuals in the vertical's own words (homeowners vs. patients vs. clients; estimates vs. appointments; crews vs. staff).
- **Example** visuals (`"tag": "example"`) use fictional competitors and plausible numbers. The closing `fine` line must say so.
- **Real data** visuals (`"tag": "real"`) and the `proof` strip must use numbers from the Watcher database only, copied exactly, and their `note` must say which market the numbers come from ("In the window treatment market: …"). Never relabel another vertical's numbers as this vertical's.
- Plain, direct sentences. No emoji, no exclamation marks. HTML entities (`&amp;`) in JSON strings.

## Format

| Key | What it is |
|---|---|
| `meta` | Page meta as for any page (`title`, `description`, optional `og_title`, `priority`). `path` defaults to `/use-cases/`, `nav` to `usecases` |
| `hero` | `eyebrow`, `title` (may contain `<em>`), `lede` |
| `proof` | Optional platform stats strip: `title`, `stats` (`value`, `label`), `note` |
| `cases` | List of use cases: `id`, `short` (index label), `kicker`, `title`, `intro`, `question`, `outcome`, `steps` (three), `signals`, `visuals`, optional `plays` (`title`, `text`) shown full width under the case |
| `closing` | `eyebrow`, `title`, `lede`, optional `button` (default: the site's long CTA label), `secondary` (links to Contact), `fine` |

Visual types (each has `type`, `title`, `tag`, optional `note`):

| `type` | Extra keys |
|---|---|
| `heatmap` | `grid` (rows of levels 0–4), `you` `[row, col]`, `open` list of `[row, col]`, `alt` |
| `battlecard` | `quads` (`label`, `tone`: good/bad/accent/neutral, `items`), `talk` |
| `adgap` | `left` and `right` (`label`, `items`), optional `ad` (`url`, `headline`, `text`) |
| `bars` | `rows` (`label`, `value`), `max`, optional `benchmark` and `legend` (`avg`, `bench`) |
| `stats` | `stats` (`value`, `label`) |
| `table` | `columns`, `rows` (`cells`, optional `you: true`). Cells `yes`, `no`, `has`, `none`, `gap`, `open` render as chips |
| `themes` | `rows` (`label`, `value`, `kind`: praise/complaint) |
| `quote` | `text`, `source` |
