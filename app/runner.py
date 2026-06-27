"""Cursor SDK orchestration for the ST deck tool.

Two modes share one persistent AsyncClient (created in main.py lifespan):

* One-shot (default): /generate builds in a single unattended run (no questions);
  /edit re-runs in the same workspace to apply a change.
* Conversational (optional): /chat/start + /chat/send keep ONE live agent per
  session in memory, so the agent can ask, propose, build, and revise across turns
  (like a normal chat). Requires the service pinned to a single instance.

Produced files: <session>/output/deck.pptx and preview-1..N.png.
"""
from __future__ import annotations

import asyncio
import os
from pathlib import Path

from cursor_sdk import LocalAgentOptions

from . import config
from .sessions import collect_outputs, new_session, restore_session, save_session, session_language

# Live conversational sessions: sid -> {ws, agent, pages}
chat_sessions: dict[str, dict] = {}

_LANG_LABELS = {
    "zh": "Simplified Chinese (简体中文)",
    "en": "English",
    "ja": "Japanese (日本語)",
}


def _lang_instruction(lang: str) -> str:
    label = _LANG_LABELS.get(lang, _LANG_LABELS["en"])
    return (
        f"Slide language: {label}. Write ALL slide text (titles, message bars, body copy, "
        f"labels, footnotes) in {label}. Do not mix languages unless the user explicitly "
        f"requests bilingual content."
    )


_COMMON = """Build EXACTLY {pages} slide(s). Follow skills/st-ppt-brand/SKILL.md for \
palette, typography, contrast, and layout. Prefer st_brand.py helpers \
(text_on, closing_slide for external decks). Never use AI images. {uploads}{language} \
When you build: save build.py, write output/deck_meta.json with \
{{"subject":"<deck title>","filename":"<Subject-Line-YYYY-MM-DD>.pptx"}}, run \
`python tools/preview.py output/deck.pptx output`, OPEN every preview PNG, fix \
contrast/size issues, re-render until clean."""

GEN_PROMPT = """You are generating a deck for an internal STMicroelectronics (ST) \
audience. Follow AGENTS.md.

MODE = ONE-SHOT, UNATTENDED. There is NO human to answer you.
- Do NOT ask questions, do NOT wait for confirmation, do NOT stop at a draft.
- Make reasonable assumptions, state them in one short line, then BUILD.
- You are NOT done until output/deck.pptx and the preview PNG(s) exist.

{common}

User request:
{request}
"""

EDIT_PROMPT = """Edit the EXISTING deck in this workspace (build.py + \
output/deck.pptx). MODE = ONE-SHOT, UNATTENDED: do NOT ask questions. Apply the \
change, rebuild by running build.py, run `python tools/preview.py output/deck.pptx \
output`, OPEN every output/preview-*.png to verify. Keep everything else unchanged \
and ST-brand-compliant. Done only when deck.pptx + preview PNG(s) are updated.

{language}

Requested change:
{instruction}
"""

CHAT_FIRST = """You are an ST (STMicroelectronics) deck-designer assistant in a \
CHAT with a user. Follow AGENTS.md.

MODE = CONVERSATIONAL — **FIRST TURN = PLANNING ONLY**. A human is on the other side.
- Do NOT run build.py, do NOT write output/deck.pptx, and do NOT run preview.py on \
this turn. No building yet.
- Read the request{uploads_hint}and reflect it in your plan.
- Reply with a structured **slide-by-slide outline** (slide #, title, 20pt message-bar \
text, main visual / bullets per slide).
- Ask **1–3 short clarifying questions** if audience, language, external vs internal, \
or key data is unclear.
- End by asking the user to **confirm or refine** (e.g. reply 「确认」/ OK / build to \
proceed). State clearly that you will build only after they confirm.

{common}

User: {request}
"""

CHAT_REMINDER = """MODE = CONVERSATIONAL (follow-up). Rules:
- If the user has NOT yet explicitly confirmed the outline (确认 / OK / build / 生成 / \
go ahead), keep discussing or refining the outline — do NOT build yet.
- Once the user explicitly confirms, run the full build loop (build.py → deck.pptx → \
preview PNGs) per AGENTS.md.
- If output/deck.pptx already exists, treat messages as edit requests: update build.py, \
re-render previews, keep other slides unchanged unless asked.
"""


def _uploads_note(has_uploads: bool) -> str:
    return (
        "Reference documents are in ./uploads/ — read them first for context, "
        "data and terminology, and reflect them in the slides. "
        if has_uploads
        else ""
    )


def _common(pages: int, has_uploads: bool, language: str) -> str:
    pages = max(1, min(config.MAX_PAGES, int(pages or 1)))
    lang_block = _lang_instruction(language) + " "
    return _COMMON.format(
        pages=pages,
        uploads=_uploads_note(has_uploads),
        language=lang_block,
    )


# ---------------- agent plumbing ----------------

async def _create_agent(client, ws: Path):
    return await client.agents.create(
        model=config.CURSOR_MODEL,
        api_key=os.environ.get("CURSOR_API_KEY"),
        local=LocalAgentOptions(cwd=str(ws), setting_sources=["project"]),
    )


async def _stream_run(run, emit) -> bool:
    async def consume():
        async for msg in run.messages():
            t = getattr(msg, "type", None)
            if t == "assistant":
                for block in msg.message.content:
                    if getattr(block, "type", None) == "text":
                        await emit("text", block.text)
            elif t == "thinking":
                await emit("thinking", getattr(msg, "text", ""))
            elif t == "tool_call":
                await emit("tool", f"{msg.name} [{msg.status}]")
            elif t == "status":
                await emit("status", getattr(msg, "status", ""))
        return await run.wait()

    try:
        result = await asyncio.wait_for(consume(), timeout=config.RUN_TIMEOUT_SEC)
    except asyncio.TimeoutError:
        await emit("error", "Agent run timed out. Try fewer pages or a simpler brief.")
        return False

    if result.status != "finished":
        await emit("error", f"run {result.status}")
        return False
    return True


def _need_key() -> bool:
    return not os.environ.get("CURSOR_API_KEY")


# ---------------- one-shot mode ----------------

async def run_generate(
    client,
    request_text: str,
    pages: int,
    ws: Path,
    sid: str,
    emit,
    has_uploads: bool,
    language: str = "zh",
):
    if _need_key():
        await emit("error", "CURSOR_API_KEY is not set on the server.")
        return collect_outputs(sid, ws)
    lang = session_language(ws)
    prompt = GEN_PROMPT.format(
        common=_common(pages, has_uploads, lang), request=request_text
    )
    agent = await _create_agent(client, ws)
    try:
        run = await agent.send(prompt)
        await _stream_run(run, emit)
    finally:
        await agent.close()
    await save_session(sid, ws)
    await emit("done", "ok")
    return collect_outputs(sid, ws)


async def run_edit(client, sid: str, instruction: str, emit):
    ws = await restore_session(sid)
    if ws is None:
        await emit("error", "session not found (it may have expired)")
        return {"session": sid, "deck": None, "previews": [], "download_name": None}
    agent = await _create_agent(client, ws)
    try:
        lang = session_language(ws)
        run = await agent.send(
            EDIT_PROMPT.format(
                language=_lang_instruction(lang), instruction=instruction
            )
        )
        await _stream_run(run, emit)
    finally:
        await agent.close()
    await save_session(sid, ws)
    await emit("done", "ok")
    return collect_outputs(sid, ws)


# ---------------- conversational mode ----------------

async def chat_start(
    client,
    request_text: str,
    pages: int,
    ws: Path,
    sid: str,
    emit,
    has_uploads: bool,
    language: str = "zh",
):
    if _need_key():
        await emit("error", "CURSOR_API_KEY is not set on the server.")
        return collect_outputs(sid, ws)
    lang = session_language(ws)
    agent = await _create_agent(client, ws)
    chat_sessions[sid] = {"ws": ws, "agent": agent, "pages": pages}
    prompt = CHAT_FIRST.format(
        common=_common(pages, has_uploads, lang),
        request=request_text,
        uploads_hint=" and ./uploads/ " if has_uploads else " ",
    )
    run = await agent.send(prompt)
    await _stream_run(run, emit)
    await save_session(sid, ws)
    await emit("done", "ok")
    return collect_outputs(sid, ws)


async def chat_send(client, sid: str, message: str, emit):
    s = chat_sessions.get(sid)
    if s is None:
        await emit(
            "error",
            "chat session not found (server may have restarted; start a new conversation)",
        )
        return {"session": sid, "deck": None, "previews": [], "download_name": None}
    run = await s["agent"].send(
        f"{CHAT_REMINDER}\n\n{_lang_instruction(session_language(s['ws']))}\n\nUser: {message}"
    )
    await _stream_run(run, emit)
    await save_session(sid, s["ws"])
    await emit("done", "ok")
    return collect_outputs(sid, s["ws"])
