"""Compare official ARC-AGI-2 results, community rows and optional Kaggle matches."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Any

from common import PROCESSED, ensure_dirs, load_config, match_target, number, percent_score, read_json, write_json


def load_records(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    payload = read_json(path)
    return payload.get("records", payload) if isinstance(payload, dict) else payload


def official_best(rows: list[dict[str, Any]], targets: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for target in targets:
        matches = [row for row in rows if row.get("target_key") == target["key"]]
        if not matches:
            output.append({"target_key": target["key"], "model_name": target["name"], "official_status": "not_found"})
            continue
        for row in matches:
            row["score_pct"] = percent_score(row.get("score_pct"))
            row["cost_per_task_usd"] = number(row.get("cost_per_task_usd"))
            if row["score_pct"] is not None and row["cost_per_task_usd"] not in (None, 0):
                row["score_per_dollar"] = row["score_pct"] / row["cost_per_task_usd"]
                row["cost_per_score_point"] = row["cost_per_task_usd"] / row["score_pct"]
        chosen = max(matches, key=lambda row: (row.get("score_pct") if row.get("score_pct") is not None else -1, -(row.get("cost_per_task_usd") or 1e99)))
        output.append({
            **chosen,
            "official_status": "official_verified",
            "all_variants": [
                {
                    "variant": row.get("variant"),
                    "score_pct": row.get("score_pct"),
                    "cost_per_task_usd": row.get("cost_per_task_usd"),
                    "score_per_dollar": row.get("score_per_dollar"),
                }
                for row in sorted(matches, key=lambda r: (r.get("score_pct") is not None, r.get("score_pct") or -1), reverse=True)
            ],
        })
    return output


def apply_pareto(rows: list[dict[str, Any]]) -> None:
    available = [row for row in rows if row.get("score_pct") is not None and row.get("cost_per_task_usd") not in (None, 0)]
    for row in rows:
        score, cost = row.get("score_pct"), row.get("cost_per_task_usd")
        row["pareto_optimal"] = False
        if score is None or cost in (None, 0):
            continue
        dominated = any(
            other is not row
            and (other.get("score_pct") or -1) >= score
            and (other.get("cost_per_task_usd") or 1e99) <= cost
            and ((other.get("score_pct") or -1) > score or (other.get("cost_per_task_usd") or 1e99) < cost)
            for other in available
        )
        row["pareto_optimal"] = not dominated


def community_summary(rows: list[dict[str, Any]], targets: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    result: dict[str, list[dict[str, Any]]] = {target["key"]: [] for target in targets}
    for row in rows:
        if row.get("target_key") in result:
            result[row["target_key"]].append(row)
    return result


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields = [
        "model_name", "variant", "score_pct", "cost_per_task_usd", "score_per_dollar",
        "cost_per_score_point", "pareto_optimal", "official_status", "verification_status", "results_url",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-score", type=float, default=0.0, help="only show official score >= this percent")
    parser.add_argument("--snapshot", type=Path, help="use a saved snapshot when live processed data is absent")
    args = parser.parse_args()
    ensure_dirs()
    config = load_config()
    official = load_records(PROCESSED / "official_records.json")
    official_source = "live_processed"
    if not official and args.snapshot:
        official = load_records(args.snapshot)
        official_source = "explicit_snapshot"
    elif not official:
        default_snapshot = PROCESSED.parent / "snapshots" / "arc_agi2_selected_2026-10-06.json"
        if default_snapshot.exists():
            official = load_records(default_snapshot)
            official_source = "bundled_snapshot"
    community = load_records(PROCESSED / "community_records.json")
    best = official_best(official, config["targets"])
    best = [row for row in best if row.get("score_pct") is None or row.get("score_pct") >= args.min_score]
    apply_pareto(best)
    ranked = sorted(best, key=lambda row: (row.get("score_pct") is not None, row.get("score_pct") or -1), reverse=True)
    for index, row in enumerate(ranked, start=1):
        row["quality_rank"] = index
    efficiency_ranked = sorted(
        [row for row in best if row.get("score_per_dollar") is not None],
        key=lambda row: row["score_per_dollar"], reverse=True,
    )
    for index, row in enumerate(efficiency_ranked, start=1):
        row["efficiency_rank"] = index

    payload = {
        "benchmark": "ARC-AGI-2",
        "dataset_id": config["dataset_id"],
        "official_records_present": bool(official),
        "official_source": official_source,
        "official_best": ranked,
        "community_by_target": community_summary(community, config["targets"]),
        "kaggle_note": "Kaggle is kept separate because its rows are competition submissions/teams, not equivalent model runs.",
    }
    write_json(PROCESSED / "arc_agi2_comparison.json", payload)
    write_csv(PROCESSED / "arc_agi2_comparison.csv", ranked)

    print("Model                                      ARC-AGI-2   $/task   pp/$    Pareto")
    print("-" * 82)
    for row in ranked:
        score = f"{row['score_pct']:.1f}%" if row.get("score_pct") is not None else "n/a"
        cost = f"${row['cost_per_task_usd']:.3f}" if row.get("cost_per_task_usd") is not None else "n/a"
        value = f"{row['score_per_dollar']:.1f}" if row.get("score_per_dollar") is not None else "n/a"
        print(f"{row['model_name'][:40]:40} {score:>9} {cost:>8} {value:>8} {str(row.get('pareto_optimal', False)):>7}")
    print(f"\nSaved: {PROCESSED / 'arc_agi2_comparison.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
