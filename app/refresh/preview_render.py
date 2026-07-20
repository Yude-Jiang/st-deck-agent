"""Render pptx → PNG previews for Deck Refresh (LibreOffice + poppler)."""
from __future__ import annotations

import glob
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path


def _natural_png_key(path: Path) -> tuple[int, str]:
    m = re.search(r"-(\d+)\.png$", path.name)
    return (int(m.group(1)) if m else 10**9, path.name)


def render_previews(pptx: Path, outdir: Path, prefix: str) -> list[Path]:
    """Write outdir/{prefix}-1.png … Return sorted paths.

    Clears previous files with the same prefix.
    """
    outdir.mkdir(parents=True, exist_ok=True)
    for old in glob.glob(str(outdir / f"{prefix}-*.png")):
        os.remove(old)

    if shutil.which("soffice") is None or shutil.which("pdftoppm") is None:
        raise RuntimeError("LibreOffice (soffice) and pdftoppm are required for previews")

    with tempfile.TemporaryDirectory(prefix="refresh-prev-") as tmp:
        tmp_path = Path(tmp)
        subprocess.run(
            [
                "soffice",
                "--headless",
                "--convert-to",
                "pdf",
                "--outdir",
                str(tmp_path),
                str(pptx),
            ],
            check=True,
            capture_output=True,
        )
        pdfs = list(tmp_path.glob("*.pdf"))
        if not pdfs:
            raise RuntimeError("LibreOffice did not produce a PDF")
        pdf = pdfs[0]
        stem = outdir / prefix
        subprocess.run(
            ["pdftoppm", "-png", "-r", "120", str(pdf), str(stem)],
            check=True,
            capture_output=True,
        )

    pngs = sorted(outdir.glob(f"{prefix}-*.png"), key=_natural_png_key)
    return pngs
