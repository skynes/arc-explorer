"""Aggregate an OpenRouter ARC run into JSON and Markdown results."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from common import read_json, write_json


def load_rows(run_dir: Path) -> list[dict[str, Any]]:
    path = run_dir / "results.ndjson"
    if not path.exists():
        raise SystemExit(f"Missing run file: {path}")
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def aggregate(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[row.get("model", "unknown")].append(row)
    output: list[dict[str, Any]] = []
    for model, items in grouped.items():
        successful = [row for row in items if row.get("status") == "ok"]
        labeled = [row for row in successful if row.get("task_correct") is not None]
        solved = sum(1 for row in labeled if row.get("task_correct") is True)
        cost = sum(float(row["cost_usd"]) for row in successful if row.get("cost_usd") is not None)
        input_tokens = sum((row.get("usage") or {}).get("prompt_tokens", 0) or 0 for row in successful)
        output_tokens = sum((row.get("usage") or {}).get("completion_tokens", 0) or 0 for row in successful)
        latency_values = [row["latency_ms"] for row in successful if row.get("latency_ms") is not None]
        total_latency_seconds = sum(latency_values) / 1000
        score_pct = (100 * solved / len(labeled)) if labeled else None
        output.append({
            "model": model,
            "requests": len(items),
            "successful_requests": len(successful),
            "errors": len(items) - len(successful),
            "scorable_tasks": len(labeled),
            "solved_tasks": solved,
            "score_pct": score_pct,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cost_usd": cost,
            "cost_per_solved_task_usd": (cost / solved) if solved else None,
            "score_per_dollar": (score_pct / cost) if score_pct is not None and cost > 0 else None,
            "avg_latency_ms": (sum(latency_values) / len(latency_values)) if latency_values else None,
            "output_tokens_per_sec": (output_tokens / total_latency_seconds) if total_latency_seconds > 0 else None,
        })
    return sorted(output, key=lambda row: (row["score_pct"] is not None, row["score_pct"] or -1), reverse=True)


def markdown(summary: list[dict[str, Any]], run_meta: dict[str, Any]) -> str:
    lines = [
        "# OpenRouter ARC run",
        "",
        f"Dataset: `{run_meta.get('dataset', 'unknown')}`  ",
        f"Started: `{run_meta.get('started_at', 'unknown')}`  ",
        "",
        "| Model | Score | Solved | Cost | $/solved | score/$ | Avg latency | Output tok/s | Errors |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in summary:
        score = f"{row['score_pct']:.2f}%" if row["score_pct"] is not None else "n/a"
        cost = f"${row['cost_usd']:.6f}"
        cost_solved = f"${row['cost_per_solved_task_usd']:.6f}" if row["cost_per_solved_task_usd"] is not None else "n/a"
        score_dollar = f"{row['score_per_dollar']:.2f}" if row["score_per_dollar"] is not None else "n/a"
        latency = f"{row['avg_latency_ms']:.0f} ms" if row["avg_latency_ms"] is not None else "n/a"
        throughput = f"{row['output_tokens_per_sec']:.1f}" if row["output_tokens_per_sec"] is not None else "n/a"
        lines.append(
            f"| `{row['model']}` | {score} | {row['solved_tasks']}/{row['scorable_tasks']} | {cost} | {cost_solved} | {score_dollar} | {latency} | {throughput} | {row['errors']} |"
        )
    lines += [
        "",
        "Score is computed only for tasks with visible expected outputs. Hidden ARC test labels cannot be scored by this local runner.",
        "Costs prefer `usage.cost` returned by OpenRouter and otherwise use the catalog price multiplied by token usage.",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, required=True)
    args = parser.parse_args()
    rows = load_rows(args.run_dir)
    meta_path = args.run_dir / "run.json"
    meta = read_json(meta_path) if meta_path.exists() else {}
    summary = aggregate(rows)
    write_json(args.run_dir / "summary.json", {"run": meta, "models": summary})
    (args.run_dir / "results.md").write_text(markdown(summary, meta), encoding="utf-8")
    print(f"Summary saved: {args.run_dir / 'summary.json'}")
    print(f"Markdown saved: {args.run_dir / 'results.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
