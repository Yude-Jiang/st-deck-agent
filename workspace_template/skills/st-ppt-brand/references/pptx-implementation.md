# python-pptx Implementation Patterns

Copy-paste patterns that bake the ST brand into generated `.pptx` files. Read the public
`pptx` skill for general mechanics; these snippets layer the ST rules on top. If you have the
official ST template, prefer `Presentation("ST_template.pptx")` and its layouts over building
from scratch — then just apply the palette/typography below.

## Palette & helpers

```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_AUTO_SIZE, PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ST palette (official names: Green Vogue / Gold / Picton Blue / White)
ST_DARK_BLUE = RGBColor(0x03, 0x23, 0x4B)   # Green Vogue
ST_YELLOW    = RGBColor(0xFF, 0xD2, 0x00)   # Gold
ST_LIGHT_BLUE= RGBColor(0x3C, 0xB4, 0xE6)   # Picton Blue
WHITE        = RGBColor(0xFF, 0xFF, 0xFF)   # White
GRAY_1       = RGBColor(0xEE, 0xEF, 0xF1)   # lightest
GRAY_2       = RGBColor(0xDB, 0xDE, 0xE1)
GRAY_3       = RGBColor(0xC0, 0xC8, 0xD2)   # medium blue-gray

# Typography — import from st_brand.py (sampled from Presentation template.potx):
# TITLE_SIZE=36, TITLE_BOLD=False, MSG_BAR_SIZE=20, BODY_SIZE=14, CAPTION_SIZE=13,
# BODY_L1_SIZE=24, AGENDA_TOPIC_SIZE=28, LABEL_SIZE=11, FOOTNOTE_SIZE=8
# Always use these constants; never hard-code Pt() in build scripts.

# Dark-blue shading ramp (graded headers / process circles). Darkest first.
RAMP = [RGBColor(0x03,0x23,0x4B),   # 1 ST Dark Blue
        RGBColor(0x42,0x59,0x78),   # 2 slate = "first shade of dark blue"
        RGBColor(0x80,0x91,0xA5),   # 3 medium blue-gray
        RGBColor(0xC0,0xC9,0xCE)]   # 4 light blue-gray
def ramp_text(step):  # white on dark steps, dark blue on light steps
    return WHITE if step < 2 else ST_DARK_BLUE

FONT = "Arial"

def fill(shape, color):
    shape.fill.solid(); shape.fill.fore_color.rgb = color
    shape.line.fill.background()  # no border by default

def no_autofit(tf):
    # The ST rule: never autofit; size boxes manually.
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE

def style_runs(tf, color, size_pt, bold=False, font=FONT):
    for p in tf.paragraphs:
        for r in p.runs:
            r.font.name = font; r.font.size = Pt(size_pt)
            r.font.bold = bold; r.font.color.rgb = color
```

## 16:9 deck
```python
prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)
```

## Key message bar (the signature element)
Geometry derived from the template guides. Fill must be one of: ST Yellow, ST Dark Blue,
ST Light Blue. Text is 20 pt Arial, single color, contrast-matched.

```python
def add_message_bar(slide, text, fill_color=ST_LIGHT_BLUE):
    bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        left=Inches(0), top=Inches(1.43),
        width=Inches(9.8), height=Inches(0.84))
    fill(bar, fill_color)
    tf = bar.text_frame; no_autofit(tf)
    tf.margin_left = Inches(0.3); tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.text = text
    # contrast: dark-blue text on yellow/light-blue, white on dark blue
    txt = WHITE if fill_color == ST_DARK_BLUE else ST_DARK_BLUE
    style_runs(tf, txt, 20, bold=True)   # 20 pt Arial, no exceptions
    return bar
```

## Title-Only content slide
```python
def add_content_slide(prs, title):
    # Title Only layout is index 5 in the default template; with the official ST
    # template, select the layout named "Title Only".
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    t = slide.shapes.title
    t.text = title
    style_runs(t.text_frame, ST_DARK_BLUE, 36, bold=False)
    return slide
```

## Shaded text box (embed text in the shape — don't stack a text box)
```python
def add_shaded_box(slide, x, y, w, h, lines, shade=GRAY_1, heading=None):
    box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                                 Inches(x), Inches(y), Inches(w), Inches(h))
    fill(box, shade)
    tf = box.text_frame; no_autofit(tf); tf.margin_left = Inches(0.2)
    tf.margin_top = Inches(0.15)
    if heading:
        tf.text = heading
        style_runs(tf, ST_DARK_BLUE, 14, bold=True)
        first = False
    else:
        first = True
    for ln in lines:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.text = "• " + ln
        for r in p.runs:
            r.font.name = FONT; r.font.size = Pt(14); r.font.color.rgb = ST_DARK_BLUE
    return box
```

## Section divider (navy bg + yellow bar)
```python
def add_section_slide(prs, title):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg = slide.background.fill; bg.solid(); bg.fore_color.rgb = ST_DARK_BLUE
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                                 Inches(2.2), Inches(0.9), Inches(9.0), Inches(1.2))
    fill(bar, ST_YELLOW); tf = bar.text_frame; no_autofit(tf); tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Inches(0.4); tf.text = title
    style_runs(tf, ST_DARK_BLUE, 32, bold=True)
    return slide
```
**Deprecated** — use `section_title_slide` in `st_brand.py` (top yellow bar per template).

## Special slides (`st_brand.py`)
See `references/special-slides.md` for reference images and anatomy.

```python
from st_brand import presentation_title_slide, agenda_slide, section_title_slide

presentation_title_slide(prs, "Presentation title", presenter="Presenter name", logo_path="st_logo.png")
agenda_slide(prs, ["Topic 1", "Topic 2", "Topic 3", "Topic 4"], title="Agenda", logo_path="st_logo.png")
section_title_slide(prs, "Section title", image_path="optional_hero.jpg", logo_path="st_logo.png")
```

- **`presentation-title`**: full navy, left yellow accent, white title + presenter, logo top-right.
- **`agenda`**: white field, “Agenda” top-right, 2-column yellow numbered tiles, logo bottom-left.
- **`section-title`**: navy field, top yellow bar with section name, optional centered image, logo bottom-left.

## Closing / trademark slide
```python
TRADEMARK = ("© STMicroelectronics - All rights reserved.\n"
    "ST logo is a trademark or a registered trademark of STMicroelectronics "
    "International NV or its affiliates in the EU and/or other countries.\n"
    "For additional information about ST trademarks, please refer to "
    "www.st.com/trademarks.\n"
    "All other product or service names are the property of their respective owners.")
```
Put "Our technology starts with You" in white on an ST Dark Blue background, with a yellow
footer band carrying `TRADEMARK` (small white Arial) and the ST logo bottom-right.

## Layout-library builders
These cover the recurring families in `layout-library.md`. The others (quadrant, image grid,
`timeline-era-cards`, row-label table) compose from the same primitives: `fill`, `add_shape`, a card =
header bar + image + gray box. Campaign timelines (#12–#13) use `st_brand.py` helpers.

### `cards-Nup` — N cards: header + image + bullet box (covers #4, #5, #6, #11 card rows)
```python
def add_cards_row(slide, cards, top=2.2, height=4.6, gap=0.3,
                  left_margin=0.4, header="yellow", with_image=True):
    """cards = [{"title":str, "bullets":[...], "img":path|None}]
    header: 'yellow' (yellow bar, dark-blue text) or 'ramp' (graded dark-blue ramp)."""
    n = len(cards)
    total_w = 13.333 - 2*left_margin
    w = (total_w - gap*(n-1)) / n
    hdr_h, img_h = 0.7, 2.2 if with_image else 0
    for i, c in enumerate(cards):
        x = left_margin + i*(w+gap)
        # header bar
        if header == "yellow":
            hfill, htext = ST_YELLOW, ST_DARK_BLUE
        else:
            hfill, htext = RAMP[min(i,3)], ramp_text(min(i,3))
        hb = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(top),
                                    Inches(w), Inches(hdr_h))
        fill(hb, hfill); tf = hb.text_frame; no_autofit(tf)
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE; tf.margin_left = Inches(0.15)
        tf.text = c["title"]; style_runs(tf, htext, 14, bold=True)
        y = top + hdr_h
        # image
        if with_image and c.get("img"):
            slide.shapes.add_picture(c["img"], Inches(x), Inches(y),
                                     width=Inches(w), height=Inches(img_h))
            y += img_h
        # gray bullet box fills remaining height
        gb = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y),
                                    Inches(w), Inches(top+height-y))
        fill(gb, GRAY_1); tf = gb.text_frame; no_autofit(tf)
        tf.margin_left = Inches(0.15); tf.margin_top = Inches(0.12)
        first = True
        for b in c.get("bullets", []):
            p = tf.paragraphs[0] if first else tf.add_paragraph(); first = False
            p.text = "• " + b
            for r in p.runs:
                r.font.name = FONT; r.font.size = Pt(14); r.font.color.rgb = ST_DARK_BLUE
```
For `cards-4up-graded-message-bar` (#5): call `add_cards_row(..., header="ramp")` then a
full-width yellow `add_message_bar`-style bar pinned to the bottom.

### `product-comparison-2up` (covers #3)
```python
def add_comparison(slide, left, right, top=1.7):
    """left/right = {"name","desc","img","bullets"}; left header dark blue, right light blue."""
    for col, data, hdr in [(0,left,ST_DARK_BLUE), (1,right,ST_LIGHT_BLUE)]:
        x = 0.5 + col*6.4; w = 5.9
        hb = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(top),
                                    Inches(w), Inches(0.9))
        fill(hb, hdr); tf = hb.text_frame; no_autofit(tf); tf.margin_left = Inches(0.2)
        tf.text = data["name"]; style_runs(tf, WHITE, 16, bold=True)
        p = tf.add_paragraph(); p.text = data["desc"]
        for r in p.runs: r.font.name=FONT; r.font.size=Pt(13); r.font.color.rgb=WHITE
        if data.get("img"):
            slide.shapes.add_picture(data["img"], Inches(x), Inches(top+0.9),
                                     width=Inches(w), height=Inches(2.6))
        gb = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(top+3.5),
                                    Inches(w), Inches(1.8))
        fill(gb, GRAY_1); tf = gb.text_frame; no_autofit(tf); tf.margin_left=Inches(0.2)
        first=True
        for b in data.get("bullets", []):
            p = tf.paragraphs[0] if first else tf.add_paragraph(); first=False
            p.text = "• " + b
            for r in p.runs: r.font.name=FONT; r.font.size=Pt(14); r.font.color.rgb=ST_DARK_BLUE
```

### `process-flow-circles` (covers #9)
```python
def add_process_flow(slide, steps, cy=4.1, d=1.9):
    """steps = [{"label":circle text, "step":'Step 1', "caption":below/above text}]"""
    n = len(steps); span = 13.333 - 1.2
    gap = (span - d*n) / (n-1) if n > 1 else 0
    for i, s in enumerate(steps):
        x = 0.6 + i*(d+gap)
        circ = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(cy-d/2),
                                      Inches(d), Inches(d))
        col = RAMP[0] if i % 2 == 0 else RAMP[2]
        fill(circ, col); tf = circ.text_frame; no_autofit(tf)
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE; tf.word_wrap = True
        tf.text = s["label"]
        style_runs(tf, ramp_text(0 if i%2==0 else 2), 12, bold=True)
        for p in tf.paragraphs: p.alignment = PP_ALIGN.CENTER
        # yellow marker dot above (even) / below (odd)
        my = cy - d/2 - 0.55 if i % 2 == 0 else cy + d/2 + 0.35
        dot = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x+d/2-0.12), Inches(my),
                                     Inches(0.24), Inches(0.24))
        fill(dot, ST_YELLOW)
```
Add the connecting dotted line and "Step N" caption text boxes alongside as needed.

### `timeline-content-promotion-lanes` (covers #13)
Use the ready-made builder in `st_brand.py`:

```python
from st_brand import new_deck, title_only_slide, corner_accent, add_title, add_message_bar
from st_brand import add_activation_timeline, timeline_template_slide

# One-call slide: title + message bar + 2-lane timeline
timeline_template_slide(
    prs,
    title="STM32C5 activation plan",
    message="Content assets and promotion timeline",
    checkpoints=[{"x": 2.4, "label": "Mar 5"}, {"x": 5.2, "label": "Apr 1"}],
    top_items=[{"x": 2.6, "title": "Cube2 ready", "note": "Community news", "color": ST_YELLOW}],
    bottom_items=[{"x": 4.8, "title": "Webinar", "note": "Apr launch"}],
)
```

`add_activation_timeline` draws the ST Dark Blue axis, lane labels ("CONTENT" / "PROMO"),
date checkpoints, and milestone boxes above/below the axis. Yellow boxes = highlighted items;
gray boxes = TBC or secondary items.

### `timeline-organic-paid-lanes` (covers #12)
Compose from `st_brand` primitives (`arrow`, `box`, `label`, `bullet_box`):

```python
def add_timeline_axis(slide, y_in, x0=0.8, x1=12.5):
    """ST Dark Blue arrow axis with yellow date markers."""
    arrow(slide, x0, y_in, x1, y_in, color=ST_DARK_BLUE, width=2.2)

def add_date_marker(slide, x_in, y_in, date_label, r=0.12):
    c = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x_in - r), Inches(y_in - r),
                               Inches(2*r), Inches(2*r))
    fill(c, ST_YELLOW)
    label(slide, x_in - 0.35, y_in + 0.12, 0.8, date_label, color=ST_DARK_BLUE, size=12)
```

For `timeline-organic-paid-lanes`: place organic boxes above `y_in`, paid span bars
~0.3 in below, product-focus segmented arrow at bottom (~6.5 in). Use double vertical
white break lines when the timeline skips months. Build from rectangles, arrows, and
circles — never SmartArt or external Gantt screenshots.

### `left-image-icon-rows` (covers #14)
Left hero with optional image or gray placeholder; yellow icon tiles + gray statement rows.

```python
from st_brand import new_deck, left_image_icon_rows_slide

prs = new_deck()
left_image_icon_rows_slide(
    prs,
    title="Why PQC matters?",
    rows=[
        {"text": "Quantum computers threaten today's public-key cryptography.", "icon_path": "icons/key.png"},
        {"text": "Harvest-now, decrypt-later attacks are already a risk."},
        {"text": "Longevity commitments require crypto agility now."},
        {"text": "Regulators and standards bodies are mandating migration."},
    ],
    punchline="The transition starts TODAY, before the risk turns real.",
    img_path=None,           # omit → gray placeholder; or path to ST-owned photo
    img_placeholder="Image",
    logo_path="logo_st.png",
)
```

### `migration-timeline-circles` (covers #15)
Alternating navy/slate circles on a dashed baseline with yellow callout ticks.

```python
from st_brand import migration_timeline_circles_slide

migration_timeline_circles_slide(
    prs,
    title="PQC migration",
    subtitle="How much time do you have?",
    steps=[
        {"label": "Awareness", "callout": "Assess exposure", "callout_pos": "above"},
        {"label": "Hybrid", "callout": "Dual-stack crypto", "callout_pos": "below"},
        {"label": "Pilot", "callout": "Field trials", "callout_pos": "above"},
        {"label": "Rollout", "callout": "Product updates", "callout_pos": "below"},
        {"label": "Full migration", "callout": "Deprecate legacy", "callout_pos": "above"},
    ],
)
```

### `left-image-tiered-list` (covers #16)
Overlapping navy message bar + left hero + yellow/gray category rows.

```python
from st_brand import left_image_tiered_list_slide

left_image_tiered_list_slide(
    prs,
    title="Smooth and reliable PQC transition",
    message="We make PQC practical and ready for deployment with ML-KEM and ML-DSA.",
    categories=[
        {"title": "Software", "bullets": ["Crypto libraries", "Middleware integration"]},
        {"title": "Hardware", "bullets": ["Secure elements", "MCU acceleration"]},
        {"title": "Trusted", "bullets": ["Key provisioning", "Lifecycle management"]},
    ],
    img_path="lab_photo.jpg",  # or None for placeholder
)
```

Shared helper `_place_image_or_placeholder(slide, image_path, x, y, w, h, label="Image")`
inserts a real picture when `image_path` is set; otherwise draws a gray box for manual swap.

## Reminders the code can't enforce — verify by eye
- **2–3 colors per slide**; large areas use primary colors.
- **Logo safe zone** kept clear.
- **No AI images, no SmartArt**; images keep aspect ratio.
- Run the **pre-share housecleaning** (`compliance-checklist.md`) before delivery.
