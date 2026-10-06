"""Fetch and normalize community leaderboard submissions from GitHub."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from common import RAW, PROCESSED, ensure_dirs, fetch_json, fetch_bytes, load_config, match_target, number, percent_score, timestamp, write_json


API_URL = "https://api.github.com/repos/arcprize/ARC-AGI-Community-Leaderboard/contents/submissions?ref=main"
RAW_BASE = "https://raw.githubusercontent.com/arcprize/ARC-AGI-Community-Leaderboard/main/submissions"


def parse_yaml(text: str) -> Any:
    try:
        import yaml  # type: ignore
        return yaml.safe_load(text) or {}
    except ImportError:
        # Fallback is deliberately conservative; install requirements.txt for nested YAML.
        result: dict[str, Any] = {}
        for line in text.splitlines():
            if not line.strip() or line.lstrip().startswith("#") or line.startswith((" ", "-")):
                continue
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            value = value.strip().strip("'\"")
            result[key.strip()] = value
        return result


def scalar(data: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        if key in data and data[key] not in (None, ""):
            return data[key]
    return None


def collect_rows(value: Any, target_hint: str, submission_id: str, inherited: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    inherited = dict(inherited or {})
    rows: list[dict[str, Any]] = []
    if isinstance(value, dict):
        local = dict(inherited)
        for key in ("name", "description", "model", "model_name", "modelName", "benchmark", "dataset", "score", "cost", "cost_per_task", "costPerTask", "date", "verified"):
            if key in value and value[key] not in (None, ""):
                local[key] = value[key]
        version_models = value.get("models")
        if isinstance(version_models, list):
            names = [
                str(model.get("name")) if isinstance(model, dict) else str(model)
                for model in version_models
                if model not in (None, "")
            ]
            if names:
                local["_model_text"] = " ".join(names)
        benchmark = str(scalar(value, "benchmark", "dataset") or local.get("benchmark") or target_hint)
        model_text = " ".join(
            str(local.get(key, ""))
            for key in ("model", "model_name", "modelName", "_model_text", "name", "description")
        )
        if "arc-agi-2" in benchmark.casefold() or "arc_agi_2" in benchmark.casefold() or "arc-agi-2" in target_hint.casefold():
            score_value = scalar(value, "score")
            score_value = local.get("score") if score_value is None else score_value
            cost_value = scalar(value, "cost", "cost_per_task", "costPerTask")
            if cost_value is None:
                cost_value = local.get("cost") or local.get("cost_per_task") or local.get("costPerTask")
            score = percent_score(score_value)
            cost = number(cost_value)
            target = match_target(model_text, load_config()["targets"])
            if score is not None or cost is not None:
                rows.append({
                    "source": "arcprize-community",
                    "verification_status": "community_self_reported",
                    "benchmark": "ARC-AGI-2",
                    "dataset_id": benchmark,
                    "submission_id": submission_id,
                    "target_key": target["key"] if target else None,
                    "model_name": target["name"] if target else (model_text or None),
                    "score_pct": score,
                    "cost_per_task_usd": cost,
                    "date": scalar(value, "date") or local.get("date"),
                    "verified": scalar(value, "verified") or local.get("verified"),
                    "retrieved_at": timestamp(),
                })
        for child in value.values():
            rows.extend(collect_rows(child, target_hint, submission_id, local))
    elif isinstance(value, list):
        for child in value:
            rows.extend(collect_rows(child, target_hint, submission_id, inherited))
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--keep-going", action="store_true")
    args = parser.parse_args()
    ensure_dirs()
    raw_dir = RAW / "community"
    raw_dir.mkdir(parents=True, exist_ok=True)
    entries = fetch_json(API_URL, headers={"Accept": "application/vnd.github+json"})
    submissions = [entry for entry in entries if entry.get("type") == "dir"]
    records: list[dict[str, Any]] = []
    errors: list[str] = []

    for entry in submissions:
        submission_id = entry["name"]
        yaml_url = f"{RAW_BASE}/{submission_id}/submission.yaml"
        try:
            body = fetch_bytes(yaml_url)
            (raw_dir / f"{submission_id}.yaml").write_bytes(body)
            data = parse_yaml(body.decode("utf-8"))
            records.extend(collect_rows(data, str(data.get("benchmark", "")) if isinstance(data, dict) else "", submission_id))
        except Exception as exc:
            errors.append(f"{submission_id}: {exc}")
            if not args.keep_going:
                raise

    write_json(PROCESSED / "community_records.json", {
        "source_url": "https://github.com/arcprize/ARC-AGI-Community-Leaderboard",
        "retrieved_at": timestamp(),
        "submissions_seen": len(submissions),
        "errors": errors,
        "records": records,
    })
    print(f"Community submissions: {len(submissions)}; ARC-AGI-2 rows: {len(records)}")
    if errors:
        print(f"Warnings: {len(errors)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
