# ST Special Slide Templates

Dedicated layouts for deck openers, navigation, and section breaks. **Do not** use the
Title-Only content frame or the 20 pt message bar on these slides — each has its own
geometry from the official ST template.

Reference images are in this folder.

## When to use

| Slide role | Archetype | Builder (`st_brand.py`) |
|---|---|---|
| Deck opening / cover | `presentation-title` | `presentation_title_slide(...)` |
| Table of contents | `agenda` | `agenda_slide(...)` |
| Chapter / section break | `section-title` | `section_title_slide(...)` |
| Mandatory external close | Thank you / trademark | `closing_slide(...)` |

---

## 1. `presentation-title` — Main / presentation title

**Reference:** [presentation-title.png](presentation-title.png)

**Use for:** first slide of the deck — presentation name, event, or campaign title.

**Structure:**
- **Full-bleed ST Dark Blue** background (`#03234B`).
- **Left accent:** thin vertical **ST Yellow** bar along the left edge (full height).
- **Title:** large **white** Arial bold (~36 pt), left area (~x 1.1 in, y ~2.6 in).
- **Presenter / subtitle:** smaller **white** Arial (~18 pt) directly below the title.
- **ST logo:** top-right (from brand.st.com asset or `logo_path`).

**No** message bar, corner accent, or slide-number styling from content slides.

---

## 2. `agenda` — Table of contents

**Reference:** [agenda.png](agenda.png)

**Use for:** listing sections or topics (typically after the presentation title).

**Structure:**
- **White** background.
- **Title** “Agenda” (or localized equivalent): top-right, **ST Dark Blue** Arial bold (~32 pt).
- **Topic list:** 2 columns × up to 4 rows each (8 topics max recommended).
  - Each row = **ST Yellow** square tile (~0.42 in) with a **dark-blue bold number** +
    topic label to the right in ST Dark Blue ~14 pt.
- **ST logo:** bottom-left.

**No** message bar on this slide.

---

## 3. `section-title` — Section divider

**Reference:** [section-title.png](section-title.png) *(visual may lag code; follow rules below)*

**Use for:** breaking the deck into chapters (before a group of content slides).

**Structure:**
- **Full-bleed ST Dark Blue** background.
- **Yellow bar vertically centered** (not top-aligned / 顶格): height ~1.15 in, spans from
  ~¼ slide width to the right edge.
  - **Section name** in **ST Dark Blue** bold Arial (~32 pt), left-aligned inside the bar.
- **No** thin horizontal rule under the yellow bar / above the footer.
- **Optional hero image:** lower band below the centered bar; lock aspect ratio.
- **ST logo:** bottom-left.

**No** message bar.

---

## Applying programmatically

```python
from st_brand import new_deck, presentation_title_slide, agenda_slide, section_title_slide

prs = new_deck()
presentation_title_slide(prs, "STM32 Ecosystem Overview", presenter="Jane Doe", logo_path="st_logo.png")
agenda_slide(prs, ["Market context", "Platform", "Roadmap", "Q&A"], logo_path="st_logo.png")
section_title_slide(prs, "Platform deep dive", image_path="hero.jpg", logo_path="st_logo.png")
```

Full patterns: `references/pptx-implementation.md`.
