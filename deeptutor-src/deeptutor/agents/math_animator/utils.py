"""Utility helpers for the math animator pipeline."""

from __future__ import annotations

import json
import re
from typing import Any


def extract_json_object(text: str) -> dict[str, Any]:
    """Extract a JSON object from raw model output."""
    raw = (text or "").strip()
    if not raw:
        return {}

    fenced = re.findall(r"```(?:json)?\s*([\s\S]*?)\s*```", raw)
    candidates = fenced + [raw]

    for candidate in candidates:
        try:
            parsed = json.loads(candidate)
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            parsed = _decode_first_json_object(candidate)
            if parsed is not None:
                return parsed

    start = raw.find("{")
    end = raw.rfind("}")
    if start != -1 and end != -1 and end > start:
        snippet = raw[start : end + 1]
        try:
            return json.loads(snippet)
        except json.JSONDecodeError:
            parsed = _decode_first_json_object(snippet)
            if parsed is not None:
                return parsed

    raise json.JSONDecodeError("No JSON object found", raw, 0)


def _decode_first_json_object(text: str) -> dict[str, Any] | None:
    decoder = json.JSONDecoder()
    stripped = (text or "").lstrip()
    if not stripped:
        return None

    starts = [0]
    brace_index = stripped.find("{")
    if brace_index > 0:
        starts.append(brace_index)

    for start in starts:
        try:
            parsed, _end = decoder.raw_decode(stripped[start:])
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            return parsed
    return None


def slugify_filename(value: str, fallback: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9._-]+", "-", (value or "").strip()).strip("-")
    return cleaned or fallback


def trim_error_message(stderr: str, limit: int = 1200) -> str:
    text = (stderr or "").strip()
    if len(text) <= limit:
        return text
    return text[-limit:]


def build_repair_error_message(error_message: str) -> str:
    text = (error_message or "").strip()
    lowered = text.lower()
    hints: list[str] = []

    if "append_points" in lowered and "shape (1,2)" in lowered and "shape (1,3)" in lowered:
        hints.append(
            "Detected a 2D-to-3D point mismatch in Manim. Every point array passed into "
            "Line/Polygon/VMobject/set_points_as_corners/append_points must be 3D."
        )
        hints.append(
            "Replace points like [x, y] or np.array([x, y]) with [x, y, 0] or np.array([x, y, 0])."
        )
        hints.append(
            "If coordinates come from axes or planes, prefer axes.c2p(...) / plane.c2p(...) so Manim receives 3D points."
        )
        hints.append(
            "Check any custom point lists, helper lines, braces, polygons, or manually assembled VMobject paths."
        )

    if not hints:
        return text

    return text + "\n\nTargeted repair hints:\n- " + "\n- ".join(hints)


__all__ = [
    "build_repair_error_message",
    "extract_json_object",
    "slugify_filename",
    "trim_error_message",
]
