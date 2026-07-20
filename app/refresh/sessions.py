"""Refresh session workspaces (isolated from Deck Generate; no GCS)."""
from __future__ import annotations

import json
import os
import shutil
import time
import uuid
from datetime import date
from pathlib import Path

from .. import config


def new_refresh_session(filename: str, data: bytes) -> tuple[str, Path]:
    """Create refresh-{sid} workspace with original.pptx. Returns (sid, ws)."""
    sid = uuid.uuid4().hex[:12]
    ws = config.SESSIONS / f"refresh-{sid}"
    if ws.exists():
        shutil.rmtree(ws, ignore_errors=True)
    (ws / "uploads").mkdir(parents=True)
    (ws / "output").mkdir(parents=True)
    original = ws / "uploads" / "original.pptx"
    original.write_bytes(data)
    meta = {
        "mode": "refresh",
        "sid": sid,
        "original_filename": os.path.basename(filename) or "deck.pptx",
        "created": time.time(),
    }
    (ws / "session_meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (ws / ".last_touch").write_text(str(time.time()), encoding="utf-8")
    return sid, ws


def refresh_session_path(sid: str) -> Path:
    return config.SESSIONS / f"refresh-{sid}"


def load_refresh_meta(ws: Path) -> dict:
    p = ws / "session_meta.json"
    if not p.is_file():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def refresh_download_name(ws: Path) -> str:
    meta = load_refresh_meta(ws)
    original = meta.get("original_filename") or "deck.pptx"
    stem = Path(original).stem or "deck"
    # sanitize
    safe = "".join(c for c in stem if c.isalnum() or c in ("-", "_", " ", "."))[:60].strip()
    if not safe:
        safe = "deck"
    return f"{safe}-refreshed-{date.today().isoformat()}.pptx"


def touch_refresh(ws: Path) -> None:
    (ws / ".last_touch").write_text(str(time.time()), encoding="utf-8")
