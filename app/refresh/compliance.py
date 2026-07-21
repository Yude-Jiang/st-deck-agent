"""Deck Refresh — compliance scan pipeline.

v1: file integrity always on; keyword layer when keyword_enabled;
Purview GUID reserved (skip).
"""
from __future__ import annotations

import json
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

from .keywords import find_keyword_hits

LayerStatus = Literal["pass", "fail", "skip", "warn"]

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
    require_ack: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "blocked": self.blocked,
            "reason": self.reason,
            "require_ack": self.require_ack,
            "details": self.details,
            "layers": [
                {"id": layer.id, "status": layer.status, "note": layer.note}
                for layer in self.layers
            ],
        }


def _load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def load_compliance_settings(config_dir: Path) -> dict[str, Any]:
    return _load_json(config_dir / "compliance.json")


def scan_pptx(path: Path, config_dir: Path) -> ComplianceScanResult:
    """Run compliance pipeline."""
    settings = load_compliance_settings(config_dir)
    layers: list[LayerResult] = []

    # Layer 1: file integrity
    if not zipfile.is_zipfile(path):
        layers.append(LayerResult(_LAYER_FILE_INTEGRITY, "fail", "not a zip/pptx container"))
        return ComplianceScanResult(
            blocked=bool(settings.get("block_on_protected_file", True)),
            reason="protected_file",
            details={
                "message": "File cannot be opened as a standard .pptx (may be encrypted or corrupted)."
            },
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

    # Layer 2: Purview GUID — reserved
    if settings.get("purview_enabled"):
        layers.append(
            LayerResult(_LAYER_PURVIEW_GUID, "skip", "enabled but not implemented")
        )
    else:
        layers.append(LayerResult(_LAYER_PURVIEW_GUID, "skip", "disabled in v1"))

    # Layer 3: keyword fallback
    if not settings.get("keyword_enabled"):
        layers.append(LayerResult(_LAYER_KEYWORD, "skip", "disabled in v1"))
        return ComplianceScanResult(blocked=False, layers=layers)

    try:
        hits = find_keyword_hits(path, config_dir)
    except Exception as exc:  # noqa: BLE001
        layers.append(LayerResult(_LAYER_KEYWORD, "fail", str(exc)))
        return ComplianceScanResult(
            blocked=True,
            reason="scan_error",
            details={"message": "Keyword scan failed."},
            layers=layers,
        )

    if hits:
        layers.append(
            LayerResult(
                _LAYER_KEYWORD,
                "warn",
                f"{len(hits)} hit(s): " + ", ".join(h["phrase"] for h in hits[:8]),
            )
        )
        return ComplianceScanResult(
            blocked=bool(settings.get("block_on_keyword_hit", True)),
            reason="keyword_hit",
            require_ack=True,
            details={
                "message": (
                    "Possible confidentiality markers detected. "
                    "This check is keyword-based and does not replace human review."
                ),
                "hits": hits,
            },
            layers=layers,
        )

    layers.append(LayerResult(_LAYER_KEYWORD, "pass"))
    return ComplianceScanResult(blocked=False, layers=layers)
