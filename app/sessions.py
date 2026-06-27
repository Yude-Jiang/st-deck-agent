"""Session workspaces: create, persist, restore, TTL cleanup."""
from __future__ import annotations

import asyncio
import glob
import io
import json
import os
import re
import shutil
import tarfile
import time
import uuid
from datetime import date
from pathlib import Path

from . import config

# ---------------------------------------------------------------------------
# sync helpers (run via executor)
# ---------------------------------------------------------------------------

def touch_session(ws: Path) -> None:
    (ws / ".last_touch").write_text(str(time.time()), encoding="utf-8")


SUPPORTED_LANGS = frozenset({"zh", "en", "ja"})


def normalize_lang(raw: str | None) -> str:
    lang = (raw or "zh").strip().lower()
    return lang if lang in SUPPORTED_LANGS else "zh"


def _new_session_sync(
    uploads: list[tuple[str, bytes]], request_text: str, language: str = "zh"
) -> tuple[str, Path]:
    sid = uuid.uuid4().hex[:12]
    ws = config.SESSIONS / sid
    shutil.copytree(config.TEMPLATE, ws)
    (ws / "output").mkdir(exist_ok=True)
    up = ws / "uploads"
    up.mkdir(exist_ok=True)
    for name, data in uploads:
        safe = os.path.basename(name).replace("/", "_").replace("\\", "_")
        (up / safe).write_bytes(data)
    if request_text.strip():
        (ws / "request.txt").write_text(request_text.strip(), encoding="utf-8")
    (ws / "language.txt").write_text(normalize_lang(language), encoding="utf-8")
    touch_session(ws)
    return sid, ws


def _gcs_bucket():
    from google.cloud import storage
    return storage.Client().bucket(config.GCS_BUCKET)


def _save_session_sync(sid: str, ws: Path) -> None:
    if not config.GCS_BUCKET:
        return
    try:
        buf = io.BytesIO()
        with tarfile.open(fileobj=buf, mode="w:gz") as tar:
            tar.add(str(ws), arcname=".")
        buf.seek(0)
        _gcs_bucket().blob(f"sessions/{sid}.tgz").upload_from_file(buf)
    except Exception:
        logger = __import__("logging").getLogger(__name__)
        logger.warning("GCS save failed for session %s", sid, exc_info=True)


def _safe_extractall(tar: tarfile.TarFile, dest: str) -> None:
    try:
        tar.extractall(dest, filter="data")
    except TypeError:
        for member in tar.getmembers():
            parts = Path(member.name).parts
            if member.name.startswith(("/", "\\")) or ".." in parts:
                continue
            tar.extract(member, dest)


def _restore_session_sync(sid: str) -> Path | None:
    ws = config.SESSIONS / sid
    if ws.exists():
        touch_session(ws)
        return ws
    if not config.GCS_BUCKET:
        return None
    try:
        blob = _gcs_bucket().blob(f"sessions/{sid}.tgz")
        if not blob.exists():
            return None
        data = io.BytesIO(blob.download_as_bytes())
        ws.mkdir(parents=True, exist_ok=True)
        with tarfile.open(fileobj=data, mode="r:gz") as tar:
            _safe_extractall(tar, str(ws))
        touch_session(ws)
        return ws
    except Exception:
        return None


def cleanup_expired_sessions(chat_sessions: dict | None = None) -> int:
    if not config.SESSIONS.exists():
        return 0
    cutoff = time.time() - config.SESSION_TTL_HOURS * 3600
    removed = 0
    for p in list(config.SESSIONS.iterdir()):
        if not p.is_dir():
            continue
        touch = p / ".last_touch"
        try:
            mtime = float(touch.read_text(encoding="utf-8")) if touch.exists() else p.stat().st_mtime
        except (ValueError, OSError):
            mtime = p.stat().st_mtime
        if mtime < cutoff:
            shutil.rmtree(p, ignore_errors=True)
            if chat_sessions is not None:
                chat_sessions.pop(p.name, None)
            removed += 1
    return removed


# ---------------------------------------------------------------------------
# async wrappers
# ---------------------------------------------------------------------------

async def new_session(
    uploads: list[tuple[str, bytes]] | None = None,
    request_text: str = "",
    language: str = "zh",
) -> tuple[str, Path]:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(
        None, _new_session_sync, uploads or [], request_text, language
    )


async def save_session(sid: str, ws: Path) -> None:
    touch_session(ws)
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, _save_session_sync, sid, ws)


async def restore_session(sid: str) -> Path | None:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, _restore_session_sync, sid)


# ---------------------------------------------------------------------------
# outputs
# ---------------------------------------------------------------------------

def _slug_filename(subject: str) -> str:
    slug = re.sub(r"[^\w\s\u4e00-\u9fff-]", "", subject, flags=re.UNICODE)
    slug = re.sub(r"[-\s]+", "-", slug).strip("-")[:50]
    if not slug:
        slug = "ST-Deck"
    return f"{slug}-{date.today().isoformat()}.pptx"


def session_language(ws: Path) -> str:
    p = ws / "language.txt"
    if p.exists():
        try:
            return normalize_lang(p.read_text(encoding="utf-8"))
        except OSError:
            pass
    return "zh"


def deck_download_name(ws: Path) -> str:
    meta = ws / "output" / "deck_meta.json"
    if meta.exists():
        try:
            data = json.loads(meta.read_text(encoding="utf-8"))
            fn = data.get("filename") or data.get("download_name")
            if fn and str(fn).endswith(".pptx"):
                return str(fn)
            subj = data.get("subject", "")
            if subj:
                return _slug_filename(str(subj))
        except (json.JSONDecodeError, OSError, TypeError):
            pass
    req = ws / "request.txt"
    subject = (
        req.read_text(encoding="utf-8").strip().split("\n")[0]
        if req.exists()
        else ""
    )
    return _slug_filename(subject or "ST-Deck")


def collect_outputs(sid: str, ws: Path) -> dict:
    deck = ws / "output" / "deck.pptx"
    previews = sorted(glob.glob(str(ws / "output" / "preview-*.png")))
    download_name = deck_download_name(ws) if deck.exists() else None
    return {
        "session": sid,
        "deck": f"/file/{sid}/deck.pptx" if deck.exists() else None,
        "download_name": download_name,
        "previews": [f"/file/{sid}/{Path(p).name}" for p in previews],
    }
