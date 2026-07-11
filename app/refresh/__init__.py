"""Deck Refresh module (incremental; does not replace Deck Generate)."""

from .compliance import ComplianceScanResult, scan_pptx

__all__ = ["ComplianceScanResult", "scan_pptx"]
