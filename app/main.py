"""FastAPI service: shareable ST deck generator on Cloud Run.

Modes:
  One-shot (default):  POST /generate (multipart)  +  POST /edit (json)
  Conversational:      POST /chat/start (multipart) +  POST /chat/send (json)

Set ACCESS_TOKEN to require X-Access-Token (or ?access_token= for file URLs) on
mutating routes and file downloads.
Conversational mode keeps a live agent in memory — pin to --max-instances 1.
"""
from __future__ import annotations

import asyncio
import json
import logging
import re
from contextlib import asynccontextmanager
from pathlib import Path

from cursor_sdk import AsyncClient
from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.responses import (
    FileResponse,
    HTMLResponse,
    JSONResponse,
    Response,
    StreamingResponse,
)

from . import config
from .runner import (
    chat_send,
    chat_start,
    chat_sessions,
    run_edit,
    run_generate,
)
from .security import guard_request, user_facing_error
from .sessions import (
    cleanup_expired_sessions,
    deck_download_name,
    new_session,
    normalize_lang,
)

TEMPLATES = Path(__file__).resolve().parent / "templates"
FILE_RE = re.compile(r"^(deck\.pptx|preview-\d+\.png)$")
logger = logging.getLogger(__name__)


async def _cleanup_loop() -> None:
    while True:
        await asyncio.sleep(config.SESSION_CLEANUP_INTERVAL_SEC)
        loop = asyncio.get_running_loop()
        removed = await loop.run_in_executor(
            None, cleanup_expired_sessions, chat_sessions
        )
        if removed:
            logger.info("cleaned up %d expired session(s)", removed)


@asynccontextmanager
async def lifespan(app: FastAPI):
    config.SESSIONS.mkdir(parents=True, exist_ok=True)
    loop = asyncio.get_running_loop()
    removed = await loop.run_in_executor(
        None, cleanup_expired_sessions, chat_sessions
    )
    if removed:
        logger.info("startup: removed %d expired session(s)", removed)
    cleanup_task = asyncio.create_task(_cleanup_loop())
    async with await AsyncClient.launch_bridge(workspace=str(config.SESSIONS)) as client:
        app.state.client = client
        yield
    cleanup_task.cancel()
    try:
        await cleanup_task
    except asyncio.CancelledError:
        pass


app = FastAPI(title="ST Deck Agent", lifespan=lifespan)


@app.get("/", response_class=HTMLResponse)
async def index():
    return HTMLResponse(
        (TEMPLATES / "index.html").read_text(encoding="utf-8"),
        headers={"Cache-Control": "no-store"},
    )


@app.get("/api/config")
async def api_config():
    return JSONResponse(
        {
            "max_pages": config.MAX_PAGES,
            "auth_required": bool(config.ACCESS_TOKEN),
            "max_upload_files": config.MAX_UPLOAD_FILES,
            "max_upload_file_mb": config.MAX_UPLOAD_FILE_BYTES // (1024 * 1024),
            "languages": ["zh", "en", "ja"],
            "refresh_enabled": config.REFRESH_ENABLED,
            "refresh_implemented": config.REFRESH_IMPLEMENTED,
            "max_refresh_pages": config.MAX_REFRESH_PAGES,
        },
        headers={"Cache-Control": "no-store"},
    )


@app.get("/favicon.ico")
async def favicon():
    return Response(status_code=204)


def _sse(obj: dict) -> str:
    return f"data: {json.dumps(obj, ensure_ascii=False)}\n\n"


def _reject(request: Request) -> JSONResponse | None:
    err = guard_request(request)
    if err:
        code = 401 if "Unauthorized" in err else 429
        return JSONResponse({"error": err}, status_code=code)
    return None


async def _stream(coro_factory):
    """Run an agent coroutine, flushing events via asyncio.Queue."""
    q: asyncio.Queue = asyncio.Queue()
    result: dict = {}

    async def emit(kind: str, text: str):
        await q.put({"kind": kind, "text": text})

    async def drive():
        try:
            r = await coro_factory(emit)
            if r:
                result.update(r)
        except Exception as exc:  # noqa: BLE001
            await q.put({"kind": "error", "text": user_facing_error(exc)})
        finally:
            await q.put(None)

    task = asyncio.create_task(drive())
    while True:
        item = await q.get()
        if item is None:
            break
        yield _sse(item)
    await task
    yield _sse({"kind": "result", "text": json.dumps(result, ensure_ascii=False)})


async def _read_uploads(files: list[UploadFile]) -> tuple[list[tuple[str, bytes]], str | None]:
    if len(files) > config.MAX_UPLOAD_FILES:
        return [], f"At most {config.MAX_UPLOAD_FILES} files allowed."
    uploads: list[tuple[str, bytes]] = []
    total = 0
    for f in files:
        if not f.filename:
            continue
        data = await f.read()
        if len(data) > config.MAX_UPLOAD_FILE_BYTES:
            mb = config.MAX_UPLOAD_FILE_BYTES // (1024 * 1024)
            return [], f"Each file must be under {mb} MB."
        total += len(data)
        if total > config.MAX_UPLOAD_TOTAL_BYTES:
            mb = config.MAX_UPLOAD_TOTAL_BYTES // (1024 * 1024)
            return [], f"Total upload size must be under {mb} MB."
        uploads.append((f.filename, data))
    return uploads, None


# ---------------- one-shot mode ----------------

@app.post("/generate")
async def generate(
    http_request: Request,
    request: str = Form(...),
    pages: int = Form(1),
    language: str = Form("zh"),
    files: list[UploadFile] = File(default=[]),
):
    if rej := _reject(http_request):
        return rej
    request = (request or "").strip()
    if not request and not files:
        return JSONResponse({"error": "empty request"}, status_code=400)
    uploads, up_err = await _read_uploads(files)
    if up_err:
        return JSONResponse({"error": up_err}, status_code=400)
    lang = normalize_lang(language)
    sid, ws = await new_session(uploads, request, language=lang)
    client = app.state.client

    async def factory(emit):
        return await run_generate(
            client, request, pages, ws, sid, emit, bool(uploads), language=lang
        )

    async def gen():
        yield _sse({"kind": "session", "text": sid})
        async for chunk in _stream(factory):
            yield chunk

    return StreamingResponse(gen(), media_type="text/event-stream")


@app.post("/edit")
async def edit(req: Request):
    if rej := _reject(req):
        return rej
    body = await req.json()
    sid = (body.get("session") or "").strip()
    instruction = (body.get("instruction") or "").strip()
    if not sid or not instruction:
        return JSONResponse(
            {"error": "session and instruction required"}, status_code=400
        )
    client = app.state.client

    async def factory(emit):
        return await run_edit(client, sid, instruction, emit)

    return StreamingResponse(_stream(factory), media_type="text/event-stream")


# ---------------- conversational mode ----------------

@app.post("/chat/start")
async def chat_start_ep(
    http_request: Request,
    request: str = Form(...),
    pages: int = Form(1),
    language: str = Form("zh"),
    files: list[UploadFile] = File(default=[]),
):
    if rej := _reject(http_request):
        return rej
    request = (request or "").strip()
    if not request and not files:
        return JSONResponse({"error": "empty request"}, status_code=400)
    uploads, up_err = await _read_uploads(files)
    if up_err:
        return JSONResponse({"error": up_err}, status_code=400)
    lang = normalize_lang(language)
    sid, ws = await new_session(uploads, request, language=lang)
    client = app.state.client

    async def factory(emit):
        return await chat_start(
            client, request, pages, ws, sid, emit, bool(uploads), language=lang
        )

    async def gen():
        yield _sse({"kind": "session", "text": sid})
        async for chunk in _stream(factory):
            yield chunk

    return StreamingResponse(gen(), media_type="text/event-stream")


@app.post("/chat/send")
async def chat_send_ep(req: Request):
    if rej := _reject(req):
        return rej
    body = await req.json()
    sid = (body.get("session") or "").strip()
    message = (body.get("message") or "").strip()
    if not sid or not message:
        return JSONResponse(
            {"error": "session and message required"}, status_code=400
        )
    client = app.state.client

    async def factory(emit):
        return await chat_send(client, sid, message, emit)

    return StreamingResponse(_stream(factory), media_type="text/event-stream")


# ---------------- file serving ----------------

@app.get("/file/{sid}/{name}")
async def get_file(request: Request, sid: str, name: str):
    if rej := _reject(request):
        return rej
    if not re.match(r"^[a-f0-9]{12}$", sid):
        return JSONResponse({"error": "not found"}, status_code=404)
    if not FILE_RE.match(name):
        return JSONResponse({"error": "not allowed"}, status_code=403)
    path = config.SESSIONS / sid / "output" / name
    if not path.exists():
        return JSONResponse({"error": "not found"}, status_code=404)
    media = (
        "application/vnd.openxmlformats-officedocument.presentationml.presentation"
        if name.endswith(".pptx")
        else "image/png"
    )
    filename = deck_download_name(config.SESSIONS / sid) if name == "deck.pptx" else name
    return FileResponse(str(path), media_type=media, filename=filename)
