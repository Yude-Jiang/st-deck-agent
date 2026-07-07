# ST Brand Spec — Colors & Typography

## Color palette

Values sampled directly from the official ST guideline deck. If the official template or a
local `st-brand.css` is available, those override these.

### Primary colors
| Official name (alias) | HEX | RGB | Use |
|---|---|---|---|
| **Green Vogue** (ST Dark Blue) | `#03234B` | 3, 35, 75 | Title-slide / section background, dark message bars, numbered tags, body headings, primary boxes |
| **Gold** (ST Yellow) | `#FFD200` | 255, 210, 0 | Section-title bar, highlight of one critical point, header bars, accent. **Text on yellow must be Green Vogue.** |

### Secondary color
| Official name (alias) | HEX | RGB | Use |
|---|---|---|---|
| **Picton Blue** (ST Light Blue) | `#3CB4E6` | 60, 180, 230 | Message bars, supporting boxes, callouts, simple charts |

> Official ST names: **Green Vogue = ST Dark Blue, Gold = ST Yellow, Picton Blue = ST Light
> Blue, White = White.** The short aliases are used elsewhere for readability.

### Neutrals — text-box shading (light gray family)
Shade content boxes in light gray tones to separate blocks of text without adding color.
| Name | HEX | RGB |
|---|---|---|
| White | `#FFFFFF` | 255, 255, 255 |
| Gray 1 (lightest) | `#EEEFF1` | 238, 239, 241 |
| Gray 2 | `#DBDEE1` | 219, 222, 225 |
| Gray 3 (medium, blue-gray) | `#C0C8D2` | 192, 200, 210 |

### ST Dark Blue shading ramp (graded header scale)
Sampled from the official card-header examples. This is the canonical set of tints used when
a layout needs several boxes/headers that read as one family (e.g. 4-up cards, process-flow
circles). Use them in order, darkest first.

| Step | Name | HEX | RGB |
|---|---|---|---|
| 1 | ST Dark Blue | `#03234B` | 3, 35, 75 |
| 2 | Slate (first shade of dark blue) | `#425978` | 66, 89, 120 |
| 3 | Medium blue-gray | `#8091A5` | 128, 145, 165 |
| 4 | Light blue-gray | `#C0C9CE` | 192, 201, 206 |

**"First shading of dark blue" = Step 2 `#425978`.** The four allowed message-bar fills are
therefore: **ST Yellow, ST Dark Blue, ST Light Blue, and the slate `#425978`.** On Steps 1–2
use white text; on Steps 3–4 use ST Dark Blue text.

### Accents (theme only — avoid for normal content)
Magenta (~`#E6007E`) and green exist in the theme color row but are not part of normal
slide styling. Don't introduce them unless the user explicitly asks.

## Color usage rules
- **2–3 colors per slide maximum.** Beyond that the slide stops looking on-brand.
- **Large areas / boxes use primary colors** (Dark Blue, Yellow) or Light Blue.
- **Contrast is mandatory.** Specifically:
  - On **ST Yellow** → use **ST Dark Blue** text (never white).
  - On **ST Dark Blue** → use **white** (or yellow for emphasis).
  - On **ST Light Blue** → use **ST Dark Blue** or white, whichever reads cleanly.
  - On **gray shades** → use ST Dark Blue text.
- Use **yellow to highlight a single critical point** — not as a general fill.

## Typography

### Font family
- **Arial** for all regular content (titles, message bar, body, captions).
- **Do not use Arial Narrow** for regular text. The only exception is text inside
  **block-diagram boxes**, where Arial Narrow is acceptable to fit labels.
- Special title slides (Main title, Section title, Thank you) may carry the template's
  built-in display typeface — preserve it; do not swap it for Arial or anything else.

### Size scale (from Presentation template.potx slideMaster txStyles)
Values are mirrored in `st_brand.py` constants. Layout positions and box geometry are
unchanged — only type sizes were aligned to the master.

| Element | Size | Weight | Notes |
|---|---|---|---|
| Content slide title | **36 pt** | regular | `TITLE_SIZE`, `TITLE_BOLD=False` |
| Key message bar | **20 pt** | bold | `MSG_BAR_SIZE` — no exceptions |
| Body / bullets | **14 pt** | regular | `BODY_SIZE` (12 pt min, 20 pt max) |
| Punchline / L1 emphasis | **24 pt** | bold | `BODY_L1_SIZE` |
| Subtitle / L3 | **18 pt** | regular | `SUBTITLE_SIZE`, `BODY_L3_SIZE` |
| Card / row caption | **13 pt** | varies | `CAPTION_SIZE` |
| Agenda number + topic | **28 pt** | number bold | `AGENDA_TOPIC_SIZE` |
| Section title (yellow bar) | **36 pt** | bold | `SECTION_TITLE_SIZE` |
| Presentation title | **36 pt** | bold | `PRESENTATION_TITLE_SIZE` |
| Closing tagline | **32 pt** | bold | `CLOSING_TAGLINE_SIZE` |
| Footer / axis labels | **11 pt** | varies | `LABEL_SIZE` |
| Closing legal footnote | **8 pt** | regular | `FOOTNOTE_SIZE` |

### Color of type
- Body text: ST Dark Blue on light backgrounds; white on dark backgrounds.
- Message bar text: a **single** color only — white **or** dark blue (never mixed).
