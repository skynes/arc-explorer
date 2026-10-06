"""Shared helpers. Keep the ingestion scripts dependency-light and auditable."""

from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Iterable, Iterator


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
RAW = DATA / "raw"
PROCESSED = DATA / "processed"
CONFIG = ROOT / "config"


def ensure_dirs() -> None:
    for path in (RAW, PROCESSED, DATA / "snapshots"):
        path.mkdir(parents=True, exist_ok=True)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def fetch_bytes(url: str, *, headers: dict[str, str] | None = None, timeout: int = 60) -> bytes:
    request_headers = {"User-Agent": "arc-explorer/0.1 (+https://arcprize.org)"}
    request_headers.update(headers or {})
    request = urllib.request.Request(url, headers=request_headers)
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def fetch_first(urls: Iterable[str], *, headers: dict[str, str] | None = None) -> tuple[str, bytes]:
    errors: list[str] = []
    for url in urls:
        try:
            return url, fetch_bytes(url, headers=headers)
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as exc:
            errors.append(f"{url}: {exc}")
    raise RuntimeError("All source URLs failed:\n" + "\n".join(errors))


def fetch_json(url: str, *, headers: dict[str, str] | None = None) -> Any:
    return json.loads(fetch_bytes(url, headers=headers).decode("utf-8"))


def load_config() -> dict[str, Any]:
    return read_json(CONFIG / "models.json")


def normalized_text(value: Any) -> str:
    text = str(value or "").casefold().replace("ё", "е")
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def number(value: Any) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip().replace(",", "")
    if not text or text.lower() in {"n/a", "na", "null", "none", "-", "—"}:
        return None
    text = text.replace("$", "").replace("%", "")
    try:
        return float(text)
    except ValueError:
        return None


def percent_score(value: Any) -> float | None:
    parsed = number(value)
    if parsed is None:
        return None
    return parsed * 100 if 0 <= parsed <= 1 else parsed


def walk_dicts(value: Any, context: dict[str, Any] | None = None) -> Iterator[tuple[dict[str, Any], dict[str, Any]]]:
    """Yield dicts with inherited model/dataset context for schema drift tolerance."""
    context = dict(context or {})
    if isinstance(value, dict):
        local = dict(context)
        for key in (
            "modelId", "model_id", "raw_model_id", "modelName", "model_name", "name",
            "displayName", "display_name", "datasetId", "dataset_id", "dataset",
            "resultsUrl", "results_url", "costPerTask", "cost_per_task",
        ):
            if key in value and value[key] not in (None, ""):
                local[key] = value[key]
        yield value, local
        for child in value.values():
            yield from walk_dicts(child, local)
    elif isinstance(value, list):
        for child in value:
            yield from walk_dicts(child, context)


def first_value(data: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        if key in data and data[key] not in (None, ""):
            return data[key]
    return None


def match_target(text: str, targets: list[dict[str, Any]]) -> dict[str, Any] | None:
    haystack = normalized_text(text)
    ranked: list[tuple[int, dict[str, Any]]] = []
    for target in targets:
        for alias in target.get("aliases", []):
            needle = normalized_text(alias)
            if needle and needle in haystack:
                ranked.append((len(needle), target))
    return max(ranked, key=lambda item: item[0])[1] if ranked else None


def timestamp() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

