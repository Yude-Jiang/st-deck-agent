# Troubleshooting

## Cloud Shell: `No space left on device` during `pip install`

Cloud Shell home storage is small (often ~5 GB). Installing `cursor-sdk` (~57 MB wheel) plus Playwright browsers can fill the disk. If install fails mid-way, you may get a **corrupt** `cursor-sdk` package and errors like:

```
SyntaxError: unterminated string literal (detected at line 172)
  File ".../site-packages/cursor_sdk/__init__.py", line 172
```

That syntax error is a symptom of a **partial install**, not a bug in the app.

### Fix: free space, remove broken package, reinstall

```bash
# 1. See what is full
df -h $HOME

# 2. Free pip / package cache
pip cache purge
rm -rf ~/.cache/pip

# 3. Remove broken cursor-sdk (partial wheel extract)
pip uninstall cursor-sdk -y 2>/dev/null || true
rm -rf ~/.local/lib/python3.12/site-packages/cursor_sdk*
rm -rf ~/.local/lib/python3.12/site-packages/cursor_sdk-*

# 4. Optional: reclaim more space
docker system prune -af 2>/dev/null || true
rm -rf /tmp/* 2>/dev/null || true

# 5. Reinstall without writing a second copy to cache
cd ~/st-deck-agent   # or your clone path
pip install --no-cache-dir -r requirements.txt

# 6. Verify import before starting uvicorn
python3 -c "from cursor_sdk import AsyncClient; print('cursor_sdk OK')"
```

If step 5 still fails with errno 28, **do not run uvicorn** until install succeeds — a half-installed `cursor-sdk` will always crash on import.

### Playwright needs extra space

Chromium for slide previews is large:

```bash
playwright install chromium
```

If disk is still tight, skip local preview testing and use **Cloud Run** instead (image already includes Chromium).

### Prefer Cloud Run over local uvicorn in Cloud Shell

For scaffold / API checks you do not need a full local stack:

```bash
# Already built image (example tag)
gcloud run deploy st-deck-agent \
  --image asia-east1-docker.pkg.dev/st-china-ai-force/cloud-run-source-deploy/st-deck-agent:refresh-scaffold \
  --project st-china-ai-force \
  --region asia-east1 \
  --memory 2Gi --cpu 2 --timeout 600 \
  --concurrency 4 --max-instances 1 \
  --set-secrets CURSOR_API_KEY=CURSOR_API_KEY:latest,ACCESS_TOKEN=ST_DECK_ACCESS_TOKEN:latest
```

Local unit tests that do not import `cursor_sdk` (e.g. compliance scan) can run without reinstalling the SDK:

```bash
cd ~/st-deck-agent
python3 -m pytest app/refresh/ -q   # when tests exist on branch
```

---

## Cloud Run: container did not listen on PORT 8080

Common causes:

1. **Missing `CURSOR_API_KEY`** — startup runs `AsyncClient.launch_bridge()` in the app lifespan; without a valid key the bridge may hang or fail before the server binds.
2. **Startup timeout** — bridge launch can take longer than the default probe window on a cold start. Check logs for the failing revision:

```bash
gcloud run services logs read st-deck-agent \
  --project st-china-ai-force \
  --region asia-east1 \
  --limit 100
```

3. **Traffic on a bad revision** — roll back to the last healthy revision in the console or:

```bash
gcloud run revisions list --service st-deck-agent \
  --project st-china-ai-force --region asia-east1
```

Ensure deploy includes secrets:

```bash
--set-secrets CURSOR_API_KEY=CURSOR_API_KEY:latest,ACCESS_TOKEN=ST_DECK_ACCESS_TOKEN:latest
```

---

## `gcloud run deploy --source` stuck at "Uploading sources"

Some org networks block regional upload endpoints (Regional Access Boundary). Use **Cloud Build + image deploy** instead:

```bash
gcloud builds submit --tag asia-east1-docker.pkg.dev/st-china-ai-force/cloud-run-source-deploy/st-deck-agent:TAG .
gcloud run deploy st-deck-agent --image ... --project st-china-ai-force --region asia-east1 ...
```
