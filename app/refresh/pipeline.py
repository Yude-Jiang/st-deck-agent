"""End-to-end Deck Refresh pipeline (scan → preview → rules → after → advice)."""
from __future__ import annotations

import asyncio
import json
import logging
from collections.abc import Awaitable, Callable
from pathlib import Path

from pptx import Presentation

from .. import config
from .advise import advice_from_changelog
from .compliance import scan_pptx
from .preview_render import render_previews
from .refresh_deck import refresh_presentation
from .sessions import (
    load_refresh_meta,
    new_refresh_session,
    refresh_download_name,
    refresh_session_path,
    touch_refresh,
)

logger = logging.getLogger(__name__)

EmitFn = Callable[[str, str], Awaitable[None]]


def _page_count(path: Path) -> int:
    return len(Presentation(str(path)).slides)


def _collect_refresh_outputs(sid: str, ws: Path) -> dict:
    out = ws / "output"
    deck = out / "deck-refreshed.pptx"
    befores = sorted(out.glob("refresh-before-*.png"))
    afters = sorted(out.glob("refresh-after-*.png"))
    advice = out / "refresh_advice.md"
    changelog = out / "refresh_changelog.json"
    summary = {}
    if changelog.is_file():
        try:
            summary = (json.loads(changelog.read_text(encoding="utf-8"))).get("summary") or {}
        except (json.JSONDecodeError, OSError):
            summary = {}
    return {
        "session": f"refresh-{sid}",
        "deck": f"/file/refresh-{sid}/deck-refreshed.pptx" if deck.is_file() else None,
        "download_name": refresh_download_name(ws) if deck.is_file() else None,
        "befores": [f"/file/refresh-{sid}/{p.name}" for p in befores],
        "afters": [f"/file/refresh-{sid}/{p.name}" for p in afters],
        "advice": advice.read_text(encoding="utf-8") if advice.is_file() else "",
        "summary": summary,
        "mode": "refresh",
    }


async def run_refresh_scan(
    filename: str,
    data: bytes,
) -> dict:
    """Create session, run compliance scan. Does not start rule refresh."""
    if len(data) > config.MAX_UPLOAD_FILE_BYTES:
        mb = config.MAX_UPLOAD_FILE_BYTES // (1024 * 1024)
        return {"error": f"Each file must be under {mb} MB."}
    if not filename.lower().endswith(".pptx"):
        return {"error": "Only .pptx files are accepted."}

    loop = asyncio.get_running_loop()
    sid, ws = await loop.run_in_executor(None, new_refresh_session, filename, data)
    original = ws / "uploads" / "original.pptx"

    try:
        pages = await loop.run_in_executor(None, _page_count, original)
    except Exception:  # noqa: BLE001
        return {
            "error": "Could not open the presentation.",
            "session": f"refresh-{sid}",
        }

    if pages > config.MAX_REFRESH_PAGES:
        return {
            "error": f"At most {config.MAX_REFRESH_PAGES} slides allowed for refresh.",
            "session": f"refresh-{sid}",
            "pages": pages,
        }

    scan = await loop.run_in_executor(
        None, scan_pptx, original, config.CONFIG_DIR
    )
    (ws / "output" / "scan_result.json").write_text(
        json.dumps(scan.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8"
    )
    touch_refresh(ws)
    return {
        "session": f"refresh-{sid}",
        "pages": pages,
        "scan": scan.to_dict(),
        "require_ack": scan.require_ack,
        "blocked": scan.blocked and not scan.require_ack,
    }


async def run_refresh(
    sid: str,
    emit: EmitFn,
    *,
    ack_keywords: bool = False,
    language: str = "zh",
) -> dict:
    """Run full refresh for an existing refresh session."""
    # Accept sid with or without refresh- prefix
    raw = sid.removeprefix("refresh-")
    ws = refresh_session_path(raw)
    if not ws.is_dir():
        await emit("error", "Session not found.")
        return {}

    original = ws / "uploads" / "original.pptx"
    if not original.is_file():
        await emit("error", "Original upload missing.")
        return {}

    loop = asyncio.get_running_loop()
    scan = await loop.run_in_executor(None, scan_pptx, original, config.CONFIG_DIR)
    if scan.blocked and scan.require_ack and not ack_keywords:
        await emit("error", "Compliance confirmation required before refresh.")
        return {}
    if scan.blocked and not scan.require_ack:
        await emit("error", scan.details.get("message") or "File blocked by compliance scan.")
        return {}

    await emit("status", "Rendering before previews…")
    out = ws / "output"
    try:
        await loop.run_in_executor(
            None, render_previews, original, out, "refresh-before"
        )
    except Exception as exc:  # noqa: BLE001
        logger.warning("before preview failed: %s", exc)
        await emit("status", "Before preview skipped (renderer unavailable).")

    await emit("status", "Applying ST visual rules…")
    dest = out / "deck-refreshed.pptx"
    changelog_path = out / "refresh_changelog.json"

    def _refresh():
        return refresh_presentation(original, dest, changelog_path)

    try:
        log = await loop.run_in_executor(None, _refresh)
    except Exception as exc:  # noqa: BLE001
        logger.exception("refresh_deck failed")
        await emit("error", "Refresh rules failed. The original file was not modified.")
        return {}

    await emit(
        "status",
        f"Rules done — {len(log.changes)} change(s), {len(log.skips)} skip(s).",
    )

    await emit("status", "Rendering after previews…")
    try:
        await loop.run_in_executor(
            None, render_previews, dest, out, "refresh-after"
        )
    except Exception as exc:  # noqa: BLE001
        logger.warning("after preview failed: %s", exc)
        await emit("status", "After preview skipped (renderer unavailable).")

    await emit("status", "Writing advisory report…")
    changelog = json.loads(changelog_path.read_text(encoding="utf-8"))
    advice = advice_from_changelog(changelog, lang=language if language in ("zh", "en") else "zh")
    (out / "refresh_advice.md").write_text(advice, encoding="utf-8")

    # Ensure original never overwritten
    assert original.is_file()
    touch_refresh(ws)
    meta = load_refresh_meta(ws)
    meta["completed"] = True
    (ws / "session_meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    await emit("status", "Refresh complete.")
    return _collect_refresh_outputs(raw, ws)
