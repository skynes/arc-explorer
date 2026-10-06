"""Fetch OpenRouter's public model catalog for later price cross-checks."""

from __future__ import annotations

import argparse
from typing import Any

from common import PROCESSED, RAW, ensure_dirs, fetch_json, load_config, timestamp, write_json


URL = "https://openrouter.ai/api/v1/models"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true", help="save all models instead of selected targets")
    args = parser.parse_args()
    ensure_dirs()
    payload = fetch_json(URL)
    write_json(RAW / "openrouter_models.json", payload)
    items = payload.get("data", payload) if isinstance(payload, dict) else payload
    wanted_ids = {model_id for target in load_config()["targets"] for model_id in target.get("openrouter_ids", [])}
    rows: list[dict[str, Any]] = []
    for item in items if isinstance(items, list) else []:
        if args.all or item.get("id") in wanted_ids:
            rows.append({
                "source": "openrouter",
                "retrieved_at": timestamp(),
                "id": item.get("id"),
                "name": item.get("name"),
                "created": item.get("created"),
                "context_length": item.get("context_length"),
                "architecture": item.get("architecture"),
                "pricing": item.get("pricing"),
                "top_provider": item.get("top_provider"),
                "canonical_slug": item.get("canonical_slug"),
            })
    write_json(PROCESSED / "openrouter_models.json", {"source_url": URL, "retrieved_at": timestamp(), "records": rows})
    print(f"OpenRouter records saved: {len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

