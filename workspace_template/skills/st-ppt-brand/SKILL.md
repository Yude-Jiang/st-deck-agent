---
name: st-ppt-brand
description: >-
  Make PowerPoint (.pptx) slides compliant with STMicroelectronics (ST) brand
  guidelines — official template, logo safe zone, ST color palette, Arial type
  scale, the key message bar, "Title Only" layout rule, text-box and image
  handling, and pre-share housecleaning. Use this skill WHENEVER generating,
  editing, restyling, or reviewing an ST presentation or any internal ST deck —
  even if the user only says "make slides", "build a deck", "ST PPT",
  "品牌合规 PPT", "ST 演示文稿", "按 ST 规范做 PPT", or pastes ST product/marketing
  content to turn into slides. Pair it with the pptx skill, which handles the
  file mechanics; this skill governs how the result must look to be on-brand.
---

# ST PowerPoint Brand Compliance

This skill encodes STMicroelectronics' internal PowerPoint guidelines ("The art of
PowerPoint — Best practices for brand-compliant slides", IM&C content team) so that
generated decks pass ST brand review.

## How to use this skill

This skill is the **brand layer**. It does not build the file by itself — it tells you
what an on-brand slide must look like. Workflow:

1. **Read the `pptx` skill first** (`/mnt/skills/public/pptx/SKILL.md`) for the mechanics
   of creating/editing the `.pptx` (python-pptx, layouts, saving).
2. **Apply this skill's rules** to every slide you produce.
3. If the user has the **official ST template** (`.potx`/`.pptx` from brand.st.com) or
   their own `st-brand.css`, treat those as the authoritative source for exact
   colors/positions and let them override the values here (these values were
   reconstructed from the guideline deck and are accurate working defaults).
4. Before finishing, run the **pre-share checklist** in
   `references/compliance-checklist.md`.

For copy/tone of newsletter-style content, defer to the `st-newsletter-copywriter` skill.

## The three cardinal rules (never break these)

1. **Use the official ST template.** Start from the latest template on brand.st.com.
   If building programmatically without it, reproduce the template's geometry and the
   palette below. Never invent a different look.
2. **Protect the ST logo safe zone.** Never place text, images, or shapes inside the
   clear space around the logo (≈ 2.5× the logo height/width on every side). The logo
   is ST's most important brand asset.
3. **Use color purposefully.** Limit a slide to **2–3 colors**. Large color areas /
   boxes use the **primary** colors. Ensure contrast — **never white text on yellow**
   (use ST Dark Blue text on yellow instead).

## Quick reference

### Palette (official ST color names; hex verified against the guideline deck)

| Role | Official name (alias used below) | HEX | RGB |
|---|---|---|---|
| Primary dark | **Green Vogue** (ST Dark Blue) | `#03234B` | 3, 35, 75 |
| Accent | **Gold** (ST Yellow) | `#FFD200` | 255, 210, 0 |
| Brand secondary | **Picton Blue** (ST Light Blue) | `#3CB4E6` | 60, 180, 230 |
| Light | **White** | `#FFFFFF` | 255, 255, 255 |
| Text-box shade (lightest) | Gray 1 | `#EEEFF1` | 238, 239, 241 |
| Text-box shade | Gray 2 | `#DBDEE1` | 219, 222, 225 |
| Text-box shade (medium) | Gray 3 | `#C0C8D2` | 192, 200, 210 |

Throughout this skill the short aliases **ST Dark Blue = Green Vogue**, **ST Yellow = Gold**,
**ST Light Blue = Picton Blue** are used for readability.

Dark-blue **shading ramp** for graded headers / process steps (darkest first):
`#03234B` (Green Vogue) → `#425978` → `#8091A5` → `#C0C9CE`. The slate `#425978` is the
"first shade of dark blue" allowed as a message-bar fill.

Accent colors (magenta/green) exist in the theme but are rarely used; do not reach for
them for normal content. Full detail and usage rules: `references/brand-spec.md`.

### Typography
- **Font: Arial** for all content. Do **not** use Arial Narrow for regular text
  (only exception: text inside block-diagram boxes).
- **Content size: 12 pt minimum (prefer 14 pt) to 20 pt maximum.**
- **Message bar: 20 pt Arial, no exceptions**, single font color (white **or** dark blue).
- Special title slides (Main title / Section / Thank you) may use the template's built-in
  display font — keep whatever the template defines; don't substitute.

### Slide & message bar geometry (16:9 = 13.333 in × 7.5 in)
- The **key message bar** sits below the title: left edge of the slide → ~4th vertical
  guide; ~3rd → ~5th horizontal guide. Working values: **x = 0, y ≈ 1.43 in,
  w ≈ 9.8 in, h ≈ 0.84 in**. Fill = ST Yellow, ST Dark Blue, or ST Light Blue.
- Full layout/positioning rules: `references/layout-rules.md`.

## Content philosophy
Slides **highlight, support, and clarify** — they do not replace the speaker. Minimal text
paired with strong visuals improves retention ("less is more"). Use the title to explain
the slide; use the message bar for the one thing the audience should remember.

## Choosing a content layout
**Single-slide decks (N = 1):** one executive-summary slide — one message bar takeaway,
4–5 bullets max. Do not use 3-up `cards-Nup` to cram multiple topics; see
`references/layout-library.md` § Single-slide.

For **special slides** (presentation title, agenda, section title, closing), use the dedicated
templates in `references/special-slides.md` and `st_brand.py` builders — not Title Only.

For any **content slide**, pick a proven archetype from the **layout library** rather than
inventing one — they are already brand-compliant. Quick menu (full detail + anatomy in
`references/layout-library.md`):

| Content shape | Archetype |
|---|---|
| One use-case over a hero photo | `app-photo-overlay` |
| One product/tech + 2–3 feature blocks + image | `left-image-feature-boxes` |
| Two products compared | `product-comparison-2up` |
| 2–4 parallel items (image + bullets each) | `cards-Nup` (yellow or graded header) |
| Parallel items building to one punchline | `cards-4up-graded-message-bar` |
| 4–6 categories with icon + fact | `icon-cards-5up` |
| 4 visual facets of one thing | `quadrant-2x2-center-badge` |
| Portfolio / overview of image tiles | `image-grid-2x3-caption-bars` |
| Sequential N-step process | `process-flow-circles` |
| Label → asset → annotation toward a visual | `row-label-table-visual` |
| Evolution over time (era cards + photo strip) | `timeline-era-cards` |
| Product launch / campaign Gantt (organic + paid + product lanes) | `timeline-organic-paid-lanes` |
| MCU activation plan (content assets + promotion lanes) | `timeline-content-promotion-lanes` |
| Left hero + icon tiles + statement rows + punchline | `left-image-icon-rows` |
| Migration / readiness timeline with callout circles | `migration-timeline-circles` |
| Left hero + overlapping message bar + category bullet rows | `left-image-tiered-list` |

**Special slides** (not Title Only): `presentation-title`, `agenda`, `section-title` —
see `references/special-slides.md`.

All archetypes sit on the **"Title Only"** layout and obey the 2–3 color rule. Builders for the
recurring families are in `references/pptx-implementation.md` and `st_brand.py`.

## Visuals — hard constraints
- **Never use AI-generated images** (company policy — including ST ChatGPT output). Use
  ST-owned assets from brand.st.com (product/application beauty shots, logos, sub-brands,
  icons, stock visuals, ST flyers/brochures).
- **Never use SmartArt.** Build diagrams from shapes; prefer **SVG** for logos/shapes
  (scalable, portable).
- **Always lock aspect ratio** when resizing images.

## Reference files (read when relevant)
- `references/brand-spec.md` — full color table (incl. shading ramp/contrast rules) and the
  complete typography spec.
- `references/special-slides.md` — presentation title, agenda, section title (when to use,
  anatomy, reference images). **Use for deck openers and section breaks.**
- `references/layout-library.md` — the 16 content-layout archetypes (when to use, anatomy,
  color spec) plus a layout picker. **Read this whenever choosing how to lay out a content slide.**
  Reference images for campaign timelines: `references/timeline-organic-paid-lanes.png`,
  `references/timeline-content-promotion-lanes.png`.
  PQC-style layouts: `references/left-image-icon-rows.png`,
  `references/migration-timeline-circles.png`, `references/left-image-tiered-list.png`.
- `references/layout-rules.md` — layout selection ("Title Only" everywhere except special
  slides), message bar, title area, footer/footnotes, text-box best practices, images.
- `references/compliance-checklist.md` — do/don't summary + pre-share housecleaning
  (classification, metadata, inspect document, slide-sorter review) + the mandatory
  trademark/closing slide text.
- `references/pptx-implementation.md` — copy-paste python-pptx patterns (palette constants,
  message bar, Title-Only content slide, section divider, closing slide).
