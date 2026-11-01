# Industry report: from a research document to /industry-report/

Every Watcher site can publish an industry report at `/industry-report/`, built the same way on every site. It takes two steps.

1. **Draft (Claude, reviewed in a pull request).** A research document goes into the site repo's `research/` folder. Claude reads it and writes `content/industry-report.json` following the rules below. A person reviews the pull request before it merges.
2. **Build (automatic).** When `content/industry-report.json` exists, the core builds `/industry-report/` from it. The menu link, footer link and sitemap entry come from `site.json` and the page's `meta`, like any other page.

`research/` sits outside `public/`, so research documents are never published.

## Instructions for Claude: drafting the report

Read everything in `research/`, then `site.json` (brand and vertical wording). Write `content/industry-report.json` in the format below.

**Numbers. This matters most.**
- Every figure on the page (in prose, stat strips, charts and tables) must come from the research document, and each one must carry a citation `<sup><a href="#s-N">N</a></sup>` pointing at the numbered source it came from.
- `sources` lists the works cited in the research document, numbered in the order they first appear on the page. Keep each source's title, publisher and URL exactly as the document gives them. Drop sources the page doesn't cite.
- Never invent, round up or combine figures into a new claim. Ranges stay ranges. Estimates are labelled as estimates ("industry estimates", "projected", "typical range").
- If two sources disagree, show the range and cite both.
- Chart `min`/`max` values and axis ticks must match the cited figures.

**Structure.** Aim for 8 to 10 sections, each with an `id` used by the contents list (`toc`). A good order:
1. The market (size, growth, segments)
2. Unit economics (pricing, margins, revenue per staff)
3. How customers find and choose a provider (the buyer journey)
4. Acquisition channels and their costs
5. Lead sources the vertical over-relies on (aggregators, marketplaces)
6. Local and high-value targeting
7. Intake, qualification and conversion
8. A recommended funnel
9. Anything distinctive the research covers (a premium tier, regulation, seasonality)
10. What it means for the business, ending with `<!--core:demo-button-->` on its own line

Include at least one `growth` or `range` chart, one `pullstat` strip and one `table` where the research supports them. Don't force a chart the data can't fill.

**Words.** Plain, direct sentences. Active voice. No emoji, no exclamation marks. Use the vertical's own words for its businesses and customers. The closing section's button comes from the site's `cta` setting; don't write one.

**Before opening the pull request.** Build the site, open `/industry-report/`, and check that every `<sup>` points to a source that exists and that each cited number appears in that part of the research document.

## content/industry-report.json format

```json
{
  "meta":   { "title": "2026 <Vertical> Industry Report | <Brand>", "description": "...", "path": "/industry-report/",
              "nav": "report", "og_type": "article", "priority": "0.9", "schema": [ { "@type": "Article", "...": "..." } ] },
  "hero":   { "eyebrow_no": "2026", "eyebrow": "<Brand> Industry Report", "title": "The <vertical> industry, <em>by the numbers.</em>",
              "lede": "...", "meta_row": ["Published <Month> 2026", "15-minute read", "<N> sources", "No email required"] },
  "toc":    [ { "id": "market", "label": "The market" } ],
  "blocks": [ "...see block types below..." ],
  "sources": [ { "n": 1, "text": "Report title. Publisher.", "url": "https://...", "site": "publisher.com" } ],
  "closing": { "eyebrow_no": "Next", "eyebrow": "Put it to work", "title": "See how your business scores on <em>every signal in this report.</em>",
               "lede": "The free demo shows how we rank every business in your market, in less than five minutes." }
}
```

### Block types

| `type` | Fields | Renders as |
|---|---|---|
| `prose` | `html`: list of lines (HTML: `<h2 id="...">`, `<p>`, `<p class="callout">`, `<p class="dropcap">`). `wrap`: false to skip the reading-width column. Shared sections such as `<!--core:demo-button-->` work here as on any page | Body text |
| `growth` | `id`, `title`, `sub`, `bars`: `label`, `value`, `height` (percent of the tallest), `title`, `forecast` (true for projected bars) | Vertical bar chart |
| `range` | `id`, `title`, `sub`, `axis`: ticks with `label` and `value`; `rows`: `label`, `min`, `max`, `display`, `title` | Range chart (for example cost per lead) |
| `pullstat` | `stats`: `value`, `label` (three work best) | Stat strip |
| `table` | `caption`, `columns`, `rows` (first cell is the row heading; cells may contain citations) | Data table |
| `funnel` | `stages`: `title`, `text`, `tags` | Stepped funnel |

Any block can set `gap: 0` to sit directly under the previous one.

## Styling

The report uses these classes from the site's stylesheet: `page-hero`, `meta-row`, `article`, `toc`, `prose`, `dropcap`, `callout`, `figure-block`, `growth*`, `range*`, `pullstat`, `dtable*`, `funnel*`, `sources`, `band-night`, `closing`, `sec-head`. DecorWatcher's `decor.css` (Report article section) is the reference. Shared base styling for these comes in a later core version.
