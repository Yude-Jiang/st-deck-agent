"""Thresholds and ST palette for Deck Refresh rule engine (standard tier)."""
from __future__ import annotations

from pptx.dml.color import RGBColor

# Import brand constants without pulling layout builders into refresh logic.
import sys
from pathlib import Path

_BRAND = Path(__file__).resolve().parents[2] / "workspace_template"
if str(_BRAND) not in sys.path:
    sys.path.insert(0, str(_BRAND))

from st_brand import (  # noqa: E402
    BODY_SIZE,
    FONT,
    GRAY_1,
    GRAY_2,
    GRAY_3,
    LABEL_SIZE,
    MSG_BAR_SIZE,
    RAMP,
    SLATE,
    ST_DARK_BLUE,
    ST_LIGHT_BLUE,
    ST_YELLOW,
    TITLE_SIZE,
    WHITE,
    text_on,
)

# Alignment: ignore deltas smaller than this (inches)
ALIGN_TOLERANCE_IN = 0.05

# Snap column/gap spacing to these inches when close
SPACING_STEPS_IN = (0.12, 0.14, 0.18, 0.25, 0.3)

# Color distance (0–441 Euclidean RGB): below → keep; above → snap to nearest ST
COLOR_SNAP_MIN_DIST = 45.0

ALLOWED_FILLS: tuple[RGBColor, ...] = (
    ST_DARK_BLUE,
    ST_YELLOW,
    ST_LIGHT_BLUE,
    WHITE,
    GRAY_1,
    GRAY_2,
    GRAY_3,
    SLATE,
    RAMP[2],
    RAMP[3],
)

ALLOWED_SIZES_PT = frozenset(
    {
        TITLE_SIZE,
        MSG_BAR_SIZE,
        BODY_SIZE,
        LABEL_SIZE,
        8,
        11,
        12,
        13,
        14,
        16,
        17,
        18,
        20,
        24,
        28,
        32,
        36,
    }
)

# Role heuristics (inches / pt)
TITLE_TOP_MAX_IN = 1.2
TITLE_SIZE_MIN_PT = 28
MSG_BAR_HEIGHT_MAX_IN = 0.55
FOOTER_TOP_MIN_IN = 6.8

__all__ = [
    "ALIGN_TOLERANCE_IN",
    "ALLOWED_FILLS",
    "ALLOWED_SIZES_PT",
    "BODY_SIZE",
    "COLOR_SNAP_MIN_DIST",
    "FONT",
    "FOOTER_TOP_MIN_IN",
    "LABEL_SIZE",
    "MSG_BAR_HEIGHT_MAX_IN",
    "MSG_BAR_SIZE",
    "SPACING_STEPS_IN",
    "ST_DARK_BLUE",
    "ST_LIGHT_BLUE",
    "ST_YELLOW",
    "TITLE_SIZE",
    "TITLE_SIZE_MIN_PT",
    "TITLE_TOP_MAX_IN",
    "WHITE",
    "text_on",
]
