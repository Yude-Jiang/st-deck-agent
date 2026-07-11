FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    SESSIONS_DIR=/tmp/sessions \
    PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers \
    DEBIAN_FRONTEND=noninteractive

# System deps for: LibreOffice preview, poppler, fonts, Playwright/Chromium
RUN apt-get update && apt-get install -y --no-install-recommends \
        libreoffice-impress \
        poppler-utils \
        fonts-liberation \
        fonts-noto-cjk \
        ca-certificates \
        curl \
        wget \
        gnupg \
        # Playwright Chromium runtime deps (install manually — avoid --with-deps apt conflicts)
        libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 \
        libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 \
        libgbm1 libpango-1.0-0 libcairo2 libasound2 libatspi2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /srv

COPY requirements.txt .
# Split pip + playwright so build logs show which step failed
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

RUN playwright install chromium

COPY app ./app
COPY config ./config
COPY workspace_template ./workspace_template

EXPOSE 8080
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}"]
