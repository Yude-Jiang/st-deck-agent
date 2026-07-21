---
name: st-ppt-brand
description: >-
  Generates and reviews STMicroelectronics (ST) brand-compliant PowerPoint (.pptx)
  slides — official palette, Arial typography, key message bar, Title Only layout,
  13 proven content archetypes (incl. campaign timeline lanes), compliance checklist,
  and python-pptx patterns.
  Use whenever the user asks to make slides, build a deck, create a PPT, turn content
  into a presentation, ST 演示文稿, 品牌合规 PPT, 按 ST 规范做 PPT, or paste ST
  product/marketing content for slides. Optimized for Copilot Chat and any agent
  that must read requirements once and produce an on-brand deck.
---

# ST PowerPoint Brand — Complete Guide

This skill encodes STMicroelectronics internal guidelines (*The art of PowerPoint —
Best practices for brand-compliant slides*, IM&C content team). Follow it end-to-end
whenever generating, editing, or reviewing an ST presentation.

## How this skill should be used (Deck Agent / any agent)

**When the user asks for a PPT/deck/slides:**

1. **Parse the request** — topic, audience (internal leadership / external customer),
   language (default English unless user says 中文/双语), page count, URLs or uploads.
2. **Pick layout archetype(s)** from the Layout Library (section below) — do not invent
   layouts from scratch.
3. **Apply brand rules** — palette, typography, message bar, Title Only layout, 2–3 colors
   per slide, no AI images, no SmartArt.
4. **Build** — prefer official ST template from brand.st.com; if programmatic, use
   python-pptx patterns in this file (or `st_brand.py` if available in workspace).
5. **Self-check** — run Compliance Checklist before delivering.

**Content philosophy:** Slides highlight and clarify; they do not replace the speaker.
Minimal text + strong visuals. **Title** = what the slide is about; **message bar** =
the one thing the audience must remember.

If the user has the official ST template (`.potx`/`.pptx` from brand.st.com), treat it
as authoritative for exact colors/positions. These values are accurate working defaults.

---

## The three cardinal rules (never break)

1. **Use the official ST template look.** Start from brand.st.com template, or reproduce
   its geometry and palette programmatically. Never invent a different visual style.
2. **Protect the ST logo safe zone.** Never place text, images, or shapes inside the clear
   space around the logo (~2.5× logo height/width on every side).
3. **Use color purposefully.** Max **2–3 colors per slide**. Large areas use primary colors.
   **Never white text on yellow** — use ST Dark Blue text on yellow instead.

---

## Color palette

Official names and aliases (use aliases in code/comments for readability):

| Role | Official name (alias) | HEX | RGB | Use |
|---|---|---|---|---|
| Primary dark | **Green Vogue** (ST Dark Blue) | `#03234B` | 3,35,75 | Titles, dark message bars, primary boxes, body headings |
| Accent | **Gold** (ST Yellow) | `#FFD200` | 255,210,0 | Section bars, one critical highlight, card headers |
| Secondary | **Picton Blue** (ST Light Blue) | `#3CB4E6` | 60,180,230 | Message bars, supporting boxes, callouts |
| Light | **White** | `#FFFFFF` | 255,255,255 | Backgrounds, text on dark fills |
| Gray 1 | — | `#EEEFF1` | 238,239,241 | Lightest text-box shade |
| Gray 2 | — | `#DBDEE1` | 219,222,225 | Text-box shade |
| Gray 3 | — | `#C0C8D2` | 192,200,210 | Medium blue-gray shade |

**Dark-blue shading ramp** (graded headers / process steps, darkest first):
`#03234B` → `#425978` (slate, "first shade of dark blue") → `#8091A5` → `#C0C9CE`

**Allowed message-bar fills:** ST Yellow, ST Dark Blue, ST Light Blue, slate `#425978`.

**Contrast rules (mandatory):**
- On **ST Yellow** → **ST Dark Blue** text (never white)
- On **ST Dark Blue** / slate Steps 1–2 → **white** text
- On **ST Light Blue** → ST Dark Blue or white (whichever reads cleanly)
- On **gray shades** / ramp Steps 3–4 → **ST Dark Blue** text
- **Yellow** highlights **one** critical point only — not general fill

Accents (magenta ~`#E6007E`, green) exist in theme but **avoid** for normal content.

---

## Typography

| Element | Font | Size | Color |
|---|---|---|---|
| Slide title | Arial | ~32–40 pt (template default) | ST Dark Blue |
| **Key message bar** | Arial | **20 pt — no exceptions** | white OR dark blue (single color only) |
| Body / bullets | Arial | 12 pt min, **prefer 14 pt**, 20 pt max | ST Dark Blue on light; white on dark |
| Footnote | Arial | template footer default | per template |

- **Do not use Arial Narrow** for regular text (OK only inside block-diagram boxes).
- Special slides (Main title / Section / Thank you) may keep template display font — do not substitute.

---

## Slide geometry (16:9 = 13.333 in × 7.5 in)

### Key message bar (signature element)
- **Position:** x = 0, y ≈ 1.43 in, width ≈ 9.8 in, height ≈ 0.84 in
- **Fill:** ST Yellow, ST Dark Blue, ST Light Blue, or slate `#425978`
- **Text:** 20 pt Arial bold, single color, contrast-matched to fill
- Do not resize, reposition, or restyle beyond allowed fills/text colors

### Shared frame (every content slide)
- **Title:** top, ST Dark Blue Arial; right-aligned for most content slides
- **Corner accent:** thin ST Dark Blue block, top-right (from template)
- **Logo:** bottom-left; **slide number** bottom-right (template footer)
- **Content band** starts ~1.5 in from top, below title

---

## Layout selection

| Slide type | Layout |
|---|---|
| All normal content slides | **Title Only** — place shapes/boxes yourself in body area |
| Main title (with/without picture) | Dedicated Main title layout |
| Section break | Section title layout |
| Agenda | Agenda layout |
| Closing | Thank you / trademark layout |
| **Avoid** | Title and contents, Title and two contents, Empty |

### Title area rules
- No graphical elements in title zone except sub-brand logo or longevity stamp

### Text-box rules
1. **Do not Autofit** — size boxes manually; keeps font uniform across deck
2. **Embed text in shapes** — never stack a text box on a colored rectangle
3. **Shade with Gray 1/2/3** to organize blocks; yellow for one highlight only

### Footer / footnotes
- Use Insert → Header & Footer predefined field; do not draw manual footnote boxes

### Images
- **Lock aspect ratio** always (Shift + corner drag)
- Source from **brand.st.com** (ST-owned assets only)
- **Never AI-generated images** (company policy, incl. ST ChatGPT output)
- **Never SmartArt** — build from shapes; prefer SVG for logos/icons

---

## Layout library — pick by content shape

All archetypes use **Title Only** + **2–3 color rule**. Remove the library "Example" tag
(top-left light-blue marker) on real slides.

| If the content is… | Archetype |
|---|---|
| One use-case over a hero photo | `app-photo-overlay` |
| One product/tech + 2–3 feature blocks + image | `left-image-feature-boxes` |
| Two products compared | `product-comparison-2up` |
| 2–4 parallel items (image + bullets each) | `cards-Nup` |
| Parallel items → one punchline | `cards-4up-graded-message-bar` |
| 4–6 categories with icon + fact | `icon-cards-5up` |
| 4 visual facets of one thing | `quadrant-2x2-center-badge` |
| Portfolio / 4–6 image tiles | `image-grid-2x3-caption-bars` |
| Sequential N-step process | `process-flow-circles` |
| Label → asset → annotation toward visual | `row-label-table-visual` |
| Evolution over time (era cards + photo strip) | `timeline-era-cards` |
| Product launch / campaign Gantt (organic + paid + product lanes) | `timeline-organic-paid-lanes` |
| MCU activation plan (content assets + promotion lanes) | `timeline-content-promotion-lanes` |

### 1. `app-photo-overlay`
Hero photo left/full-bleed; ST Dark Blue message bar (white 20 pt bold) near top; yellow
callout (dark-blue text); gray bullet box `#EEEFF1` with 4–6 bullets.

### 2. `left-image-feature-boxes`
Left ~⅓ product photo; 2–3 feature boxes using dark-blue ramp + one gray box; white text
on blue boxes, dark-blue on gray.

### 3. `product-comparison-2up`
Two equal columns: left header ST Dark Blue, right ST Light Blue (white text); photo +
gray spec box each.

### 4. `cards-Nup` (workhorse)
N equal columns: **header bar** (yellow + dark-blue text, OR graded ramp) + **image** +
**gray bullet box** `#EEEFF1`. Align all card tops/bottoms.

### 5. `cards-4up-graded-message-bar`
Same as cards-Nup (4 graded headers) + full-width **ST Yellow bottom bar** with single
takeaway (dark-blue bold text).

### 6. `icon-cards-5up`
Top ST Dark Blue message bar (white text); 5 columns with yellow icon tile + gray fact box.

### 7. `quadrant-2x2-center-badge`
2×2 grid alternating photo and colored panels (`#03234B`, `#425978`); white circle center
badge with product logo.

### 8. `image-grid-2x3-caption-bars`
6 tiles (2×3): caption header alternating ST Dark Blue / ST Yellow + photo each.

### 9. `process-flow-circles`
N circles alternating `#03234B` / `#8091A5`, white labels; dotted connector; ST Yellow step
markers with "Step N" captions. Max ~6 steps.

### 10. `row-label-table-visual`
Stack of dark-blue label boxes + gray content cells; large arrow to supporting visual;
light-blue URL button bottom.

### 11. `timeline-era-cards`
Yellow-header era cards + gray bullets; navy arrow timeline `#03234B` with yellow circle
markers and year labels; photo strip bottom.

### 12. `timeline-organic-paid-lanes`
**Use for:** product-launch or annual campaign roadmaps with distinct organic, paid, and
product-focus tracks (e.g. Stellar P3E 2026 plan).

**Reference:** [references/timeline-organic-paid-lanes.png](references/timeline-organic-paid-lanes.png)

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

### 13. `timeline-content-promotion-lanes`
**Use for:** MCU / software activation plans with parallel content-asset and promotion
tracks (e.g. STM32C5 activation plan).

**Reference:** [references/timeline-content-promotion-lanes.png](references/timeline-content-promotion-lanes.png)

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

---

## Compliance checklist

### Do
- Official ST template; logo safe zone clear
- 2–3 colors/slide; Arial; message bar 20 pt; Title Only for content
- Embed text in shapes; Do not Autofit; lock image aspect ratio
- ST-owned assets only; SVG for icons/shapes

### Don't
- White text on yellow; AI images; SmartArt; Arial Narrow (except diagram boxes)
- Autofit/shrink-to-fit; >3 colors/slide; graphics in title area (except sub-brand stamp)
- Restyle message bar beyond allowed fills/colors

### Pre-share housecleaning (external decks)
1. Set document classification (SMS decks = Public)
2. File → Info → Inspect Document → remove metadata, cropped image data, internal notes
3. Add fresh metadata (Title, Tags)
4. Review in Slide Sorter + Slide Show

### Mandatory closing slide (external)
ST Dark Blue "Our technology starts with You" + yellow trademark footer band + ST logo.
Footer text:

```
© STMicroelectronics - All rights reserved.
ST logo is a trademark or a registered trademark of STMicroelectronics International NV
or its affiliates in the EU and/or other countries.
For additional information about ST trademarks, please refer to www.st.com/trademarks.
All other product or service names are the property of their respective owners.
```

**Resources:** brand.st.com (template, assets, layout library); SMS portal (300+ approved decks).

---

## python-pptx implementation (programmatic generation)

Use when building `.pptx` with code. Prefer `Presentation("ST_template.pptx")` if available.

### Palette constants

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_AUTO_SIZE, PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

ST_DARK_BLUE  = RGBColor(0x03, 0x23, 0x4B)   # Green Vogue
ST_YELLOW     = RGBColor(0xFF, 0xD2, 0x00)   # Gold
ST_LIGHT_BLUE = RGBColor(0x3C, 0xB4, 0xE6)   # Picton Blue
WHITE         = RGBColor(0xFF, 0xFF, 0xFF)
GRAY_1        = RGBColor(0xEE, 0xEF, 0xF1)
GRAY_2        = RGBColor(0xDB, 0xDE, 0xE1)
GRAY_3        = RGBColor(0xC0, 0xC8, 0xD2)
RAMP = [ST_DARK_BLUE, RGBColor(0x42,0x59,0x78), RGBColor(0x80,0x91,0xA5), RGBColor(0xC0,0xC9,0xCE)]
FONT = "Arial"

def fill(shape, color):
    shape.fill.solid(); shape.fill.fore_color.rgb = color; shape.line.fill.background()

def no_autofit(tf):
    tf.word_wrap = True; tf.auto_size = MSO_AUTO_SIZE.NONE

def style_runs(tf, color, size_pt, bold=False):
    for p in tf.paragraphs:
        for r in p.runs:
            r.font.name = FONT; r.font.size = Pt(size_pt)
            r.font.bold = bold; r.font.color.rgb = color
```

### Deck + message bar + content slide

```python
prs = Presentation()
prs.slide_width = Inches(13.333); prs.slide_height = Inches(7.5)

def add_message_bar(slide, text, fill_color=ST_LIGHT_BLUE):
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.43),
                                   Inches(9.8), Inches(0.84))
    fill(bar, fill_color)
    tf = bar.text_frame; no_autofit(tf)
    tf.margin_left = Inches(0.3); tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.text = text
    txt = WHITE if fill_color in (ST_DARK_BLUE, RAMP[1]) else ST_DARK_BLUE
    style_runs(tf, txt, 20, bold=True)
    return bar

def add_content_slide(prs, title):
    slide = prs.slides.add_slide(prs.slide_layouts[5])  # Title Only
    slide.shapes.title.text = title
    style_runs(slide.shapes.title.text_frame, ST_DARK_BLUE, 36)
    return slide
```

### Section divider + closing

```python
def add_section_slide(prs, title):
    """Navy field + vertically centered yellow bar. No top-flush bar, no bottom rule."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid(); slide.background.fill.fore_color.rgb = ST_DARK_BLUE
    bar_h = 1.15
    bar_top = (7.5 - bar_h) / 2  # vertically centered — never pin to top edge
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(3.35), Inches(bar_top),
                                  Inches(13.333 - 3.35), Inches(bar_h))
    fill(bar, ST_YELLOW)
    tf = bar.text_frame; no_autofit(tf)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Inches(0.35)
    tf.text = title
    style_runs(tf, ST_DARK_BLUE, 32, bold=True)
    # Do NOT add a horizontal rule under the yellow bar / above the footer.
```

**Section divider rules:** yellow bar **vertically centered** (not top-aligned / 顶格);
**no** thin horizontal line below the bar.

### Bilingual diagnosis decks (China management style)

Use when building **internal China diagnostic / competitive** decks (CN primary, EN secondary).
Preserve this expression pattern (from ST Community traffic diagnosis):

**1. Title block**
- CN title: Arial Bold ~36pt, ST Dark Blue
- EN subtitle immediately under: Arial Italic ~14pt, slate `#425978`

**2. Yellow message bar (full takeaway)**
- One bilingual-capable punchline in **ST Yellow** bar, **ST Dark Blue** text
- CN conclusion first; may include short EN on same bar or rely on stacked cards for EN

**3. Stacked insight rows (`insight_stack`)**
- Full-width gray row + **navy left accent strip**
- Each row: bold CN label + statement; EN translation on next line in slate
- Typical triad for exec summary: **横向 / 纵向 / 合并图景** (Horizontal / Vertical / Combined)

**4. Referral + Gen AI page**
- Left/main: comparison table (Source | Flows to | Role)
- Right or below: **Gen AI callout** (light header) — volume caveat + ST vs TI split + directional read
- Bottom shared observation: both sites self-referential; weak third-party discovery

**5. Data-anomaly page (mandatory when AA + SimilarWeb mixed)**
- State what was filtered (e.g. Chrome 134.0)
- State residual risk / which KPI windows to trust
- Cross-check note (cleaned Bing YoY direction vs validated H1)
- Do **not** digress into multi-quarter incident timelines unless the brief asks

```python
from st_brand import bilingual_title, insight_stack, callout_panel, add_message_bar

bilingual_title(slide, "核心结论", "Executive summary")
add_message_bar(slide, "TI 体量更大（约1.75×），ST 质量更好且 H1 在收复份额", ST_YELLOW)
insight_stack(slide, [
    {"zh_title": "横向", "zh": "…", "en": "Horizontal (vs TI): …"},
    {"zh_title": "纵向", "zh": "…", "en": "Vertical (YoY): …"},
    {"zh_title": "合并图景", "zh": "…", "en": "Combined picture: …"},
])
callout_panel(slide, 8.5, 2.4, 4.4, 2.8, "Gen AI 引荐（体量小，方向性信号）",
              ["占比 <0.05%", "ST 71.5% vs TI 28.5%", "与百度格局相反"])
```

For `cards-Nup`, `product-comparison-2up`, `process-flow-circles` builders, see full
patterns in workspace `st_brand.py` or original `pptx-implementation.md`.

### Campaign timeline lanes (sketch)

```python
def add_timeline_axis(slide, y_in, x0=0.8, x1=12.5):
    """ST Dark Blue arrow axis with yellow date markers."""
    arrow = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(x0), Inches(y_in),
                                   Inches(x1 - x0), Inches(0.18))
    fill(arrow, ST_DARK_BLUE)
    return arrow

def add_date_marker(slide, x_in, y_in, label, r=0.12):
    c = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x_in - r), Inches(y_in - r),
                               Inches(2*r), Inches(2*r))
    fill(c, ST_YELLOW)
    # label box below marker — Arial 12 pt ST Dark Blue
```

For `timeline-organic-paid-lanes`: place organic boxes above `y_in`, paid span bars
~0.3 in below, product-focus segmented arrow at bottom (~6.5 in). For
`timeline-content-promotion-lanes`: duplicate axis pattern with two labeled lanes and a
legend row; use `add_shape(RECTANGLE)` + `fill()` for yellow/gray milestone boxes.

---

## Agent workflow checklist

Before delivering any deck, verify:

```
- [ ] Correct layout archetype chosen for each slide's content shape
- [ ] Title Only for content slides; message bar on every content slide (20 pt Arial)
- [ ] 2–3 colors per slide; contrast correct (no white on yellow)
- [ ] Arial throughout; body 12–20 pt (prefer 14 pt)
- [ ] Text embedded in shapes; Do not Autofit
- [ ] Real ST assets / user screenshots only — no AI images, no SmartArt
- [ ] Logo safe zone respected; images aspect-ratio locked
- [ ] External deck: classification, inspect document, closing trademark slide
```

**Diagram / ecosystem slides:** use `cards-Nup`, `process-flow-circles`, or layered
boxes + arrows + dashed "Planned/Future" container — all built from shapes, not SmartArt.

**Campaign / activation timelines:** use `timeline-organic-paid-lanes` for launch campaigns
with organic + paid + product tracks; use `timeline-content-promotion-lanes` for MCU/software
activation plans with content-asset vs promotion lanes. Build from rectangles, arrows, and
circles — never SmartArt or external Gantt chart screenshots.


---

## Workspace extras (this Deck Agent template)

Brand helpers live in workspace root `st_brand.py`. Prefer them over re-implementing
palette / message-bar / timeline builders. Additional content archetypes still available
in `references/layout-library.md` and `st_brand.py` (beyond the 13 above):

| Archetype | Builder |
|---|---|
| `left-image-icon-rows` | `left_image_icon_rows_slide` |
| `migration-timeline-circles` | `migration_timeline_circles_slide` |
| `left-image-tiered-list` | `left_image_tiered_list_slide` |
| Special: presentation / agenda / section / closing | `presentation_title_slide`, `agenda_slide`, `section_title_slide`, `closing_slide` |
| Bilingual diagnosis rows | `bilingual_title`, `insight_stack`, `callout_panel` |

Also read when needed: `references/brand-spec.md`, `references/special-slides.md`,
`references/layout-rules.md`, `references/compliance-checklist.md`,
`references/pptx-implementation.md`. Preview with `python tools/preview.py`.
