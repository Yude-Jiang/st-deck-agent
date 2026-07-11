"""Deck Refresh — compliance scan scaffold (v1: file integrity only).

Purview GUID and keyword layers are reserved via config; disabled by default.
Does not modify existing Deck Generate routes or workspace_template.
"""
from __future__ import annotations

import json
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

LayerStatus = Literal["pass", "fail", "skip"]

_LAYER_FILE_INTEGRITY = "file_integrity"
_LAYER_PURVIEW_GUID = "purview_guid"
_LAYER_KEYWORD = "keyword"


@dataclass
class LayerResult:
    id: str
    status: LayerStatus
    note: str = ""


@dataclass
class ComplianceScanResult:
    blocked: bool
    reason: str | None = None
    details: dict[str, Any] = field(default_factory=dict)
    layers: list[LayerResult] = field(default_factory=list)


def _load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def load_compliance_settings(config_dir: Path) -> dict[str, Any]:
    return _load_json(config_dir / "compliance.json")


def scan_pptx(path: Path, config_dir: Path) -> ComplianceScanResult:
    """Run compliance pipeline. v1 scaffold: file integrity only; other layers skip."""
    settings = load_compliance_settings(config_dir)
    layers: list[LayerResult] = []

    # Layer 1: file integrity (always on when block_on_protected_file)
    if not zipfile.is_zipfile(path):
        layers.append(LayerResult(_LAYER_FILE_INTEGRITY, "fail", "not a zip/pptx container"))
        return ComplianceScanResult(
            blocked=bool(settings.get("block_on_protected_file", True)),
            reason="protected_file",
            details={"message": "File cannot be opened as a standard .pptx (may be encrypted or corrupted)."},
            layers=layers,
        )
    try:
        with zipfile.ZipFile(path, "r") as zf:
            zf.namelist()
    except (zipfile.BadZipFile, OSError) as exc:
        layers.append(LayerResult(_LAYER_FILE_INTEGRITY, "fail", str(exc)))
        return ComplianceScanResult(
            blocked=bool(settings.get("block_on_protected_file", True)),
            reason="protected_file",
            details={"message": "File appears protected or corrupted."},
            layers=layers,
        )
    layers.append(LayerResult(_LAYER_FILE_INTEGRITY, "pass"))

    # Layer 2: Purview GUID — reserved, v1 disabled
    if settings.get("purview_enabled"):
        layers.append(LayerResult(_LAYER_PURVIEW_GUID, "skip", "enabled but not implemented in scaffold"))
    else:
        layers.append(LayerResult(_LAYER_PURVIEW_GUID, "skip", "disabled in v1"))

    # Layer 3: keyword fallback — reserved, v1 disabled unless keyword_enabled + phrases
    if settings.get("keyword_enabled"):
        layers.append(LayerResult(_LAYER_KEYWORD, "skip", "enabled but not implemented in scaffold"))
    else:
        layers.append(LayerResult(_LAYER_KEYWORD, "skip", "disabled in v1"))

    return ComplianceScanResult(blocked=False, layers=layers)
