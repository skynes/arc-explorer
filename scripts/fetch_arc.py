"""Fetch ARC Prize's public static data pack and normalize ARC-AGI-2 rows."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from common import (
    RAW,
    PROCESSED,
    ensure_dirs,
    fetch_first,
    first_value,
    load_config,
    match_target,
    number,
    percent_score,
    read_json,
    timestamp,
    walk_dicts,
    write_json,
)


URL_CANDIDATES = {
    "models": [
        "https://arcprize.org/media/data/models.json",
        "https://arcprize.org/media/data/leaderboard/models.json",
    ],
    "evaluations": [
        "https://arcprize.org/media/data/evaluations.json",
        "https://arcprize.org/media/data/leaderboard/evaluations.json",
    ],
}


def build_model_lookup(models: Any) -> dict[str, dict[str, Any]]:
    lookup: dict[str, dict[str, Any]] = {}
    for item, _ in walk_dicts(models):
        model_id = first_value(item, "id", "modelId", "model_id", "raw_model_id")
        if model_id is None:
            continue
        for key in ("id", "modelId", "model_id", "raw_model_id", "slug", "name"):
            value = item.get(key)
            if value not in (None, ""):
                lookup[str(value)] = item
    return lookup


def extract_official_rows(evaluations: Any, models: Any, targets: list[dict[str, Any]]) -> list[dict[str, Any]]:
    model_lookup = build_model_lookup(models)
    rows: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str, str]] = set()

    for item, context in walk_dicts(evaluations):
        dataset_id = first_value(item, "datasetId", "dataset_id", "dataset") or first_value(context, "datasetId", "dataset_id", "dataset")
        if str(dataset_id) != "v2_Semi_Private":
            continue
        display = first_value(item, "display", "isDisplayed", "visible")
        if display is not None and str(display).casefold() in {"false", "0", "no"}:
            continue

        details = item.get("details") if isinstance(item.get("details"), dict) else {}
        score_details = item.get("scoreDetails") if isinstance(item.get("scoreDetails"), dict) else {}
        nested_details = score_details.get("details") if isinstance(score_details.get("details"), dict) else {}
        model_id = first_value(item, "raw_model_id", "modelId", "model_id", "model_id_raw")
        model_id = model_id or first_value(details, "raw_model_id", "modelId", "model_id")
        model_id = model_id or first_value(nested_details, "raw_model_id", "modelId", "model_id")
        model_id = model_id or first_value(context, "raw_model_id", "modelId", "model_id")

        model_obj = model_lookup.get(str(model_id), {})
        model_text = " ".join(
            str(value)
            for value in (
                first_value(item, "name", "modelName", "model_name", "displayName"),
                first_value(context, "name", "modelName", "model_name", "displayName"),
                first_value(details, "name", "modelName", "model_name", "displayName"),
                model_id,
                model_obj.get("name"), model_obj.get("displayName"), model_obj.get("slug"),
            )
            if value not in (None, "")
        )
        target = match_target(model_text, targets)
        if target is None:
            continue

        score_value = first_value(item, "score", "scoreValue", "accuracy", "value")
        if score_value is None:
            score_value = first_value(score_details, "score", "value")
        if score_value is None:
            score_value = first_value(nested_details, "score", "value")
        score = percent_score(score_value)
        cost_value = first_value(item, "costPerTask", "cost_per_task", "cost")
        cost_value = cost_value or first_value(details, "costPerTask", "cost_per_task", "cost")
        cost_value = cost_value or first_value(nested_details, "costPerTask", "cost_per_task", "cost")
        cost = number(cost_value)
        if score is None and cost is None:
            continue

        variant = first_value(item, "variant", "reasoningEffort", "reasoning_effort", "effort")
        if variant is None:
            variant = first_value(details, "variant", "reasoningEffort", "reasoning_effort", "effort")
        row_key = (target["key"], str(variant or ""), str(score), str(cost))
        if row_key in seen:
            continue
        seen.add(row_key)
        rows.append({
            "source": "arcprize",
            "verification_status": "official_verified",
            "benchmark": "ARC-AGI-2",
            "dataset_id": "v2_Semi_Private",
            "target_key": target["key"],
            "model_name": target["name"],
            "raw_model_id": model_id,
            "variant": variant,
            "score_pct": score,
            "cost_per_task_usd": cost,
            "results_url": first_value(item, "resultsUrl", "results_url") or first_value(context, "resultsUrl", "results_url"),
            "retrieved_at": timestamp(),
        })

    return sorted(rows, key=lambda row: (row["target_key"], -(row["score_pct"] or -1)))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="re-download raw JSON")
    args = parser.parse_args()
    ensure_dirs()
    raw_dir = RAW / "arcprize"
    raw_dir.mkdir(parents=True, exist_ok=True)

    payloads: dict[str, Any] = {}
    source_urls: dict[str, str] = {}
    for name, candidates in URL_CANDIDATES.items():
        raw_path = raw_dir / f"{name}.json"
        if raw_path.exists() and not args.force:
            payloads[name] = read_json(raw_path)
            source_urls[name] = "cached"
            continue
        source_url, body = fetch_first(candidates)
        raw_path.write_bytes(body)
        payloads[name] = __import__("json").loads(body.decode("utf-8"))
        source_urls[name] = source_url

    rows = extract_official_rows(payloads["evaluations"], payloads["models"], load_config()["targets"])
    write_json(PROCESSED / "official_records.json", {
        "source_urls": source_urls,
        "retrieved_at": timestamp(),
        "records": rows,
    })
    print(f"Official records: {len(rows)}")
    print(f"Saved: {PROCESSED / 'official_records.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
