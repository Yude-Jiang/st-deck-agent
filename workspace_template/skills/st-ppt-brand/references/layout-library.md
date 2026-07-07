# ST Slide Layout Library

> **Special slides** (presentation title, agenda, section title): see
> [`special-slides.md`](special-slides.md) — dedicated layouts, not Title Only.

A catalog of proven, brand-compliant **content** layouts from ST's official slide-layout library.
When building a content slide, **pick the archetype that fits the content shape**, then style
it with the palette in `brand-spec.md`. All of these sit on the **"Title Only"** layout — the
title, corner accent, logo, and slide number come from the template; everything else you place
as shapes.

> Note: the small light-blue **"Example" tag** top-left in the source library is only a library
> marker. **Remove it on real slides.**

## Shared frame (every archetype)
- **Title**: top of slide, ST Dark Blue Arial. Right-aligned for most content slides;
  centered/left also seen. One or two lines.
- **Corner accent**: thin ST Dark Blue block at the top-right edge (from template).
- **Logo**: ST logo bottom-left. **Slide number** bottom-right. (template footer)
- **Content band** starts ~1.5 in from top, below the title.

## How to choose
| If the content is… | Use archetype |
|---|---|
| **Exactly 1 slide** (executive summary / quick intro) | See **Single-slide** below — avoid 3-up cards |
| One use-case told over a hero photo | `app-photo-overlay` |
| One product/tech with 2–3 grouped feature blocks + a hero image | `left-image-feature-boxes` |
| Two products/options compared head-to-head | `product-comparison-2up` |
| 2–4 parallel items, each = image + a few bullets | `cards-Nup` (yellow or graded header) |
| Several items that share one punchline | add a bottom **yellow message bar** (`cards-4up-graded-message-bar`) |
| 4–6 categories each with an icon + label + one fact | `icon-cards-5up` |
| 4 facets of one thing, visual-heavy | `quadrant-2x2-center-badge` |
| A portfolio/overview of 4–6 image tiles | `image-grid-2x3-caption-bars` |
| A sequential N-step process | `process-flow-circles` |
| Rows of label → content → annotation, pointing at a visual | `row-label-table-visual` |
| Evolution over time (era cards + photo strip) | `timeline-era-cards` |
| Product launch / campaign Gantt (organic + paid + product lanes) | `timeline-organic-paid-lanes` |
| MCU activation plan (content assets + promotion lanes) | `timeline-content-promotion-lanes` |
| Left hero + icon tiles + statement rows + punchline | `left-image-icon-rows` |
| Migration / readiness timeline with callout circles | `migration-timeline-circles` |
| Left hero + overlapping message bar + category bullet rows | `left-image-tiered-list` |

### Single-slide (N = 1) — executive summary
When the deck is **one page only**, treat it as a single takeaway — not a multi-topic
deck compressed onto one canvas.

| Goal | Layout | Limits |
|---|---|---|
| Quick topic intro | title + message bar + one gray bullet box | 4–5 bullets, ~60 words body |
| Story with visual hook | `left-image-icon-rows` | 3–4 one-line rows + optional punchline |
| Product / tech spotlight | `left-image-feature-boxes` | ≤ 2 feature blocks |
| One application narrative | `app-photo-overlay` | 4–6 bullets max |

**Avoid** `cards-Nup` with 3+ columns for 1-slide intros — each column wants its own
slide. If the brief spans "what / why / how", pick one angle or ask for more pages.

---

## 1. `app-photo-overlay` — application / use-case
Hero photo fills the left (or full) area; text floats on top.
- **Photo**: left half to full-bleed, behind everything.
- **Message bar**: full-width **ST Dark Blue** band near the top, white 20 pt Arial bold —
  the core statement.
- **Yellow callout**: a benefit sentence, ST Dark Blue text.
- **Gray bullet box** (`#EEEFF1`, slight transparency): the supporting bullet list, dark-blue
  bullets.
- Use when one application is the whole story. Keep to 4–6 bullets.

## 2. `left-image-feature-boxes` — product / technology highlight
- **Left image**: full-height product/beauty shot, ~⅓ width.
- **Feature boxes** (2–3): each a filled rectangle with a bold heading + 1–2 short paragraphs.
  Color them from the dark-blue ramp + one gray box (e.g. box 1 = `#03234B`, box 2 = `#425978`,
  side box = `#EEEFF1`). White text on the blue boxes, dark-blue text on gray.
- Title can be two lines, right-aligned.

## 3. `product-comparison-2up` — two products side by side
- **Two equal columns.** Each column:
  - **Header bar**: product name (bold) + one-line descriptor. Differentiate the two with
    **ST Dark Blue** (left) and **ST Light Blue** (right) headers (white text).
  - **Photo** of the application.
  - **Gray box** (`#EEEFF1`) with 2–3 spec bullets, plus a small product (package) shot.
- Great for "low voltage vs high voltage", "entry vs premium", etc.

## 4. `cards-Nup` — N parallel cards (2, 3 or 4 across)
The workhorse. N equal columns, each card = **header bar + image + gray bullet box**.
- **Header bar** options:
  - **Yellow** header, ST Dark Blue text (clean, high-energy) — see High-power example.
  - **Graded** headers from the dark-blue ramp (Step 1→4 across the columns) when you want the
    set to read as a sequence/intensity — see the 4-up example.
- **Image** sits directly under the header.
- **Gray box** (`#EEEFF1`) holds the bullets/short text (centered text works for 1–3 lines).
- Keep all cards the same width/height; align tops and bottoms (use Shift/Ctrl+Shift).

## 5. `cards-4up-graded-message-bar` — cards + bottom punchline
Same as `cards-Nup` (4 graded-header cards) **plus** a **full-width ST Yellow message bar**
across the bottom with the single takeaway (e.g. the part number + "Efficient, flexible, and
available!"), ST Dark Blue text, bold key words. Use when the cards build to one conclusion.

## 6. `icon-cards-5up` — categories with icons
- **Top message bar**: ST Dark Blue full-width band, white text — the umbrella statement.
- **5 columns** (4–6 works), each:
  - **Yellow icon tile** (square) with a dark-blue **monochrome icon** (SVG pictogram, not
    SmartArt, not AI art).
  - **Gray box** (`#EEEFF1`) with a bold heading, a standard/label line, and a short
    description — all ST Dark Blue, centered.
- Ideal for certifications, pillars, capability families.

## 7. `quadrant-2x2-center-badge` — four facets, visual
- **2×2 grid.** Cells alternate **photo** and **colored text panel**; panels use `#03234B`
  and `#425978` (white headings + short body).
- **Center badge**: a white circle straddling the four cells holding the product/tool **logo**.
- Title top-right. Use for a tool/product with four selling points and strong imagery.

## 8. `image-grid-2x3-caption-bars` — portfolio / overview grid
- **6 tiles** in 2 rows × 3 columns (also works 1×N or 2×2). Each tile = **caption header bar +
  photo**.
- **Alternate header colors** tile-to-tile between **ST Dark Blue** (white text) and
  **ST Yellow** (dark-blue text) for rhythm.
- Use for "our product families", "our markets", a visual table of contents.

## 9. `process-flow-circles` — sequential steps
- **N circles** in a row (5 shown), **alternating `#03234B` and `#8091A5`**, white text inside
  (short label per step).
- **Dotted connector** weaving through the circles; an arrowhead on the last.
- **Step markers**: small **ST Yellow** dots on short lines above/below alternating circles,
  each with "**Step N**" (bold) + a label, ST Dark Blue.
- Use for workflows/pipelines. Don't exceed ~6 steps.

## 10. `row-label-table-visual` — labelled rows pointing to a visual
- **Left stack of rows**: each row = **ST Dark Blue label box** (white bold) + **gray content
  cell** (`#EEEFF1`, holds a logo/diagram/text) + optional right-side annotation text.
- **Large gray arrow** pointing right from the rows to a **supporting visual** (e.g. a product
  screenshot / device render).
- **Light-blue URL button** (`#3CB4E6`) bottom with a globe pictogram for the call-to-action link.
- Use to map "capability → asset → where it lives".

## 11. `timeline-era-cards` — evolution over time
- **N era cards** across the top: each = **ST Yellow header** (era name, dark-blue bold) +
  **gray box** (`#EEEFF1`) with bullets.
- **Navy arrow timeline** beneath them (`#03234B`, arrowhead at right) with **ST Yellow circle
  markers** (white ring) at each era and a **year label** (dark-blue bold) under each marker.
- **Photo strip**: one image per era aligned to the columns at the bottom.
- Use for market evolution, roadmap history, generational progress.

## 12. `timeline-organic-paid-lanes` — campaign / launch Gantt
**Use for:** product-launch or annual campaign roadmaps with distinct organic, paid, and
product-focus tracks (e.g. Stellar P3E 2026 plan).

**Reference:** [timeline-organic-paid-lanes.png](timeline-organic-paid-lanes.png)

**Structure (top → bottom, 3 horizontal lanes):**

1. **Organic lane** — activity boxes above the axis, each linked to a date marker by a thin
   ST Dark Blue vertical connector. Box = ST Dark Blue header (white bold) + gray `#EEEFF1`
   body (dark-blue bullets). One box per milestone; larger box for major launch events.
2. **Central timeline axis** — thick ST Dark Blue right-pointing arrow spanning the slide;
   **yellow circle** markers on the axis at each date; date labels below markers (Arial 12–14 pt,
   ST Dark Blue). Use **double vertical white break lines** when the timeline skips months
   (e.g. Jan–Mar → December).
3. **Paid lane** — ST Light Blue horizontal bar(s) below the axis showing campaign duration
   spans (e.g. "Paid Social 11-Feb→10-Mar"); light-blue caption for always-on channels below.
4. **Product-focus bar** — bottom segmented ST Light Blue arrow; each segment = one product
   focus period; separate segments with double vertical break lines.

**Colors:** ST Dark Blue (axis, connectors, organic headers), ST Yellow (date markers),
ST Light Blue (paid bars, product-focus arrow), Gray 1 (box bodies). Max 3 colors per region.

**Message bar:** e.g. "2026 campaign timeline — organic, paid, and product focus."

## 13. `timeline-content-promotion-lanes` — MCU / activation plan
**Use for:** MCU / software activation plans with parallel content-asset and promotion
tracks (e.g. STM32C5 activation plan).

**Reference:** [timeline-content-promotion-lanes.png](timeline-content-promotion-lanes.png)

**Structure (top → bottom, 2 horizontal lanes + legend):**

1. **Legend row** (top-right or below title) — small swatches:
   - ST Yellow fill = highlighted track item (e.g. Cube2-related)
   - Gray 2 `#DBDEE1` = TBC / unconfirmed
   - Green accent marker = key milestone (e.g. MML)
2. **Content Assets lane** — left column: vertical list of deliverables (press release, webpages,
   blog, video, flyer, etc.) with small icons; right: milestone boxes on timeline — yellow boxes
   for gated publications (e.g. "Cube2 ready: Community developer news"); week labels (W11, W23)
   for delivery vs publication.
3. **Central timeline axis** — ST Dark Blue horizontal line with month/date tick labels
   (Feb 10th, Mar 5th, Mar 10th … June); vertical tick marks at each date.
4. **Promotion lane** — event items below axis: icon + label per activity (blog, banner, webinar,
   enews, e-store, ads). Group by month. **Duration campaigns** = long horizontal bar/arrow
   (ST Light Blue or approved accent) spanning start→end months (e.g. Google + Social ads
   Apr→Jun). Yellow-background items = same highlight as legend.

**Lane labels:** "CONTENT ASSETS" and "PROMOTION" in ST Dark Blue bold, left-aligned above
each lane.

**Colors:** ST Dark Blue (axis, labels), ST Yellow (highlight boxes/items), Gray 1–2 (TBC items),
ST Light Blue (campaign duration bars). Avoid magenta/green except the single MML marker.

**Message bar:** e.g. "STM32C5 activation plan — content assets and promotion timeline."

**Builder:** prefer `st_brand.add_activation_timeline(...)` or `timeline_template_slide(...)` —
see `pptx-implementation.md`.

## 14. `left-image-icon-rows` — icon tiles + statement rows
**Use for:** 3–5 parallel reasons, drivers, or facts each with a pictogram and a one-line
statement, plus an optional closing punchline (e.g. "Why PQC matters?").

**Reference:** [left-image-icon-rows.png](left-image-icon-rows.png)

**Structure:**
1. **Left hero image** — full-height panel (~1/3 slide width). ST logo bottom-left on the image.
   Pass `img_path` for a real ST-owned photo; omit for a gray **placeholder** labelled "Image".
2. **Title** — top-right on the white band, ST Dark Blue Arial 24–28 pt.
3. **Rows** (repeat 3–5×) — **ST Yellow** square tile (optional `icon_path` pictogram centred
   inside) + **Gray 1** `#EEEFF1` bar with one dark-blue sentence (bold key phrases inline).
4. **Punchline** — large dark-blue statement bottom-right (optional).

**Colors:** ST Dark Blue, Gray 1, ST Yellow accent. No standard message bar on this archetype.

**Builder:** `st_brand.left_image_icon_rows_slide(...)`.

## 15. `migration-timeline-circles` — wave timeline with callouts
**Use for:** phased migration or readiness roadmaps where each phase is a labelled circle and
supporting detail sits above or below (e.g. "PQC migration: How much time do you have?").

**Reference:** [migration-timeline-circles.png](migration-timeline-circles.png)

**Structure:**
1. **Title + subtitle** — top-right, ST Dark Blue.
2. **Dotted baseline** — horizontal dashed connector across the slide.
3. **Circles** (3–6) — alternating ST Dark Blue and slate ramp fill; white/yellow label text
   centred inside each circle.
4. **Yellow callout ticks** — short vertical ST Yellow bar above or below each circle, with a
   caption text block (10–11 pt dark blue).
5. **Logo** — bottom-left.

**Colors:** ST Dark Blue, slate ramp, ST Yellow markers. Distinct from `process-flow-circles`
(step numbers + arrows) and lane-based timelines (#12–13).

**Builder:** `st_brand.migration_timeline_circles_slide(...)`.

## 16. `left-image-tiered-list` — hero + category bullet rows
**Use for:** one product/technology with 2–4 grouped capability areas (Software / Hardware /
Trusted, etc.) and a strong top message (e.g. "Smooth and reliable PQC transition").

**Reference:** [left-image-tiered-list.png](left-image-tiered-list.png)

**Structure:**
1. **Title** — top-right, ST Dark Blue.
2. **Navy message bar** — full-width ST Dark Blue band overlapping the top of the left image;
   white 16–18 pt bold statement inside.
3. **Left hero image** — ~40% width below the bar; logo bottom-left. `img_path` or gray
   placeholder.
4. **Category rows** (2–4) — **ST Yellow** narrow header box (category name) + **Gray 1**
   bullet box for details, stacked on the right.

**Builder:** `st_brand.left_image_tiered_list_slide(...)`.

---

## Applying any of these
1. Confirm it's a **"Title Only"** slide.
2. Build with **shapes that embed their own text** (don't stack text boxes on rectangles);
   set every text frame to **Do not Autofit**.
3. Respect the **2–3 color** rule per slide — these archetypes already do (blue ramp + gray +
   one yellow accent).
4. Source photos from brand.st.com; icons as **SVG pictograms**; **no AI imagery, no SmartArt**.
5. Maintain image **aspect ratio**; align card edges with the grid/guides.

Parametrized python-pptx builders for the recurring families (`cards-Nup`,
`product-comparison-2up`, `process-flow-circles`, `timeline-content-promotion-lanes`,
`timeline-organic-paid-lanes`, `left-image-icon-rows`, `migration-timeline-circles`,
`left-image-tiered-list`) are in `pptx-implementation.md` and `st_brand.py`.
