"""Read-only advisory for Deck Refresh.

Primary path: deterministic Markdown from changelog (no tools, no file writes
beyond the advice file the pipeline creates). Optional LLM call is best-effort
and must never block download of deck-refreshed.pptx.
"""
from __future__ import annotations

from typing import Any


def advice_from_changelog(changelog: dict[str, Any], lang: str = "zh") -> str:
    summary = changelog.get("summary") or {}
    skips = changelog.get("skips") or []
    warnings = changelog.get("warnings") or []
    changes = changelog.get("changes") or []
    n_slides = changelog.get("slide_count", 0)

    if lang == "en":
        lines = [
            "# Deck Refresh report",
            "",
            "## Automatically applied",
            f"- Slides processed: **{n_slides}**",
        ]
        if summary:
            for k, v in sorted(summary.items()):
                lines.append(f"- {k}: **{v}** change(s)")
        else:
            lines.append("- No visual property changes were required (already close to ST baseline).")
        lines += ["", "## Consider (file not modified)", ""]
        if skips:
            reasons: dict[str, int] = {}
            for s in skips:
                reasons[s.get("reason", "?")] = reasons.get(s.get("reason", "?"), 0) + 1
            for r, c in sorted(reasons.items(), key=lambda x: -x[1])[:12]:
                lines.append(f"- Skipped ({c}×): `{r}` — review manually if needed.")
        else:
            lines.append("- No structural skips recorded.")
        lines.append(
            "- Content, narrative, and page count were left unchanged by design."
        )
        if warnings:
            lines += ["", "## Warnings", ""]
            for w in warnings:
                lines.append(f"- {w}")
        lines += [
            "",
            "---",
            "_Keyword / watermark detection is assistive only and does not replace human review._",
        ]
        return "\n".join(lines)

    # zh default
    lines = [
        "# Deck 焕新报告",
        "",
        "## 已自动修正",
        f"- 处理页数：**{n_slides}**",
    ]
    if summary:
        label = {
            "color": "配色",
            "contrast": "对比度",
            "font": "字体",
            "font_size": "字号",
            "font_weight": "字重",
            "align": "对齐",
            "symmetry": "对称",
            "autofit": "Autofit",
            "line": "线条",
            "picture": "图片",
        }
        for k, v in sorted(summary.items()):
            lines.append(f"- {label.get(k, k)}：**{v}** 处")
    else:
        lines.append("- 未发现需强制修正的视觉属性（已接近 ST 基线）。")
    lines += ["", "## 建议您考虑（未改文件）", ""]
    if skips:
        reasons: dict[str, int] = {}
        for s in skips:
            reasons[s.get("reason", "?")] = reasons.get(s.get("reason", "?"), 0) + 1
        for r, c in sorted(reasons.items(), key=lambda x: -x[1])[:12]:
            lines.append(f"- 已跳过（{c}×）：`{r}` — 如需处理请人工调整。")
    else:
        lines.append("- 无结构类跳过项。")
    lines.append("- 文案、数据与页数按产品约束保持不变。")
    if warnings:
        lines += ["", "## 警示", ""]
        for w in warnings:
            lines.append(f"- {w}")
    # Mention densest slides if many font_size/color changes
    by_slide: dict[int, int] = {}
    for c in changes:
        by_slide[c["slide"]] = by_slide.get(c["slide"], 0) + 1
    if by_slide:
        top = sorted(by_slide.items(), key=lambda x: -x[1])[:3]
        lines += ["", "### 变更较多的页", ""]
        for si, cnt in top:
            lines.append(f"- 第 {si} 页：约 {cnt} 处视觉属性调整")
    lines += [
        "",
        "---",
        "_密级关键词检测仅为辅助，不能替代人工保密审查。_",
    ]
    return "\n".join(lines)
