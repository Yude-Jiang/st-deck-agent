# ST Deck Agent

Internal Cloud Run tool that generates ST-brand-compliant PowerPoint decks via the Cursor SDK.

## Quick start (local)

```bash
export CURSOR_API_KEY=your_key
export ACCESS_TOKEN=choose-a-shared-secret   # optional but recommended
pip install -r requirements.txt
playwright install chromium
uvicorn app.main:app --reload --port 8080
```

Open http://localhost:8080

> **Cloud Shell:** Home disk is limited. If `pip install` fails with `No space left on device`, or `cursor_sdk` shows `SyntaxError: unterminated string literal`, see [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) — remove the partial install and use `pip install --no-cache-dir`.

## Deploy (Cloud Run)

Cloud Run **service name:** `st-deck-agent` (keep this name — do not rename when redeploying).

```bash
cd st-deck-agent
gcloud run deploy st-deck-agent \
  --source . \
  --project YOUR_PROJECT \
  --region asia-east1 \
  --allow-unauthenticated \
  --memory 2Gi --cpu 2 --timeout 600 \
  --concurrency 4 --max-instances 1 \
  --set-secrets CURSOR_API_KEY=CURSOR_API_KEY:latest,ACCESS_TOKEN=ST_DECK_ACCESS_TOKEN:latest \
  --set-env-vars CURSOR_MODEL=composer-2.5
```

> **Note:** Even with `--allow-unauthenticated`, set `ACCESS_TOKEN` (via Secret Manager or env) so only colleagues with the token can generate decks. Cloud Run IAP is an alternative.

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `CURSOR_API_KEY` | — | Required. Cursor API key (use Secret Manager in prod). |
| `CURSOR_MODEL` | `composer-2.5` | Model for the agent. |
| `ACCESS_TOKEN` | *(empty)* | If set, all generate/edit/chat/file routes require `X-Access-Token` header. |
| `RATE_LIMIT_PER_MINUTE` | `10` | Per-IP rate limit for API routes. |
| `MAX_PAGES` | `6` | Maximum slides per request. |
| `MAX_UPLOAD_FILES` | `5` | Max reference files per request. |
| `MAX_UPLOAD_FILE_BYTES` | `10485760` (10 MB) | Per-file upload limit. |
| `MAX_UPLOAD_TOTAL_BYTES` | `31457280` (30 MB) | Total upload limit per request. |
| `SESSION_TTL_HOURS` | `24` | Auto-delete session workspaces after this age. |
| `SESSION_CLEANUP_INTERVAL_SEC` | `3600` | How often to sweep expired sessions. |
| `RUN_TIMEOUT_SEC` | `540` | Max seconds per agent run. |
| `GCS_BUCKET` | *(empty)* | Optional. Persist session tarballs for restore after instance restart. **Not used for refresh sessions.** |
| `REFRESH_ENABLED` | `false` | Expose Deck Refresh UI/API (independent module; default off). |
| `REFRESH_IMPLEMENTED` | `false` | End-to-end refresh available when true. |
| `MAX_REFRESH_PAGES` | `20` | Max slides per refresh request. |
| `REFRESH_GCS_BACKUP` | `false` | If `GCS_BUCKET` set, refresh sessions still skip backup when false. |
| `SESSIONS_DIR` | `/tmp/sessions` | Workspace root (tmpfs on Cloud Run). |

## Modes

- **One-shot (default):** `POST /generate` → deck + previews in one unattended run.
- **Edit:** `POST /edit` with `{session, instruction}` after a one-shot run.
- **对话模式（Beta）**：首轮只出大纲与追问，用户**明确确认后**才 BUILD；后续可继续对话修改。需 `--max-instances 1`；重启后对话上下文丢失。

## Outputs

Each session produces:

- `output/deck.pptx` — download served with a friendly name from `deck_meta.json` or the request subject.
- `output/preview-*.png` — rendered slide previews for self-check.
- `build.py` — reproducible build script for edits.

## Brand compliance

Agent rules live in `workspace_template/AGENTS.md` and `workspace_template/skills/st-ppt-brand/`.  
Python helpers in `workspace_template/st_brand.py` include `text_on()` for contrast and `closing_slide()` for external decks.

## Preview fonts

The Docker image uses Liberation Sans as an Arial metric substitute for LibreOffice preview rendering. Generated `.pptx` files still declare Arial; final rendering on machines with real Arial may differ slightly.

## Security notes

- Set `ACCESS_TOKEN` before sharing the URL widely.
- Session IDs are 12 hex chars — not a secret; token auth is required for production.
- Upload limits and rate limiting are enabled by default.
