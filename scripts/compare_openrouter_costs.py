"""Compare OpenRouter catalog costs under repeatable agent token profiles."""

from __future__ import annotations

import argparse
import time
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

from common import DATA, PROCESSED, ROOT, read_json, write_json


MODELS = [
    ("DeepSeek V4 Flash 0731", "deepseek/deepseek-v4-flash-0731"),
    ("GLM-5.3-Flash", "z-ai/glm-5.3-flash"),
    ("GPT-6 Luna", "openai/gpt-6-luna"),
    ("GPT-5.6 Luna", "openai/gpt-5.6-luna"),
    ("GPT-6.1 Sol", "openai/gpt-6.1-sol"),
    ("GPT-6.1 Sol Pro", "openai/gpt-6.1-sol-pro"),
    ("GPT-6 Astra", "openai/gpt-6-astra"),
    ("Dots3-Note Preview free", "dots-studio/dots-3-note-preview:free"),
]

SCENARIOS = {
    "arc_short": {"label": "ARC-like short answer", "input_tokens": 12000, "output_tokens": 1000},
    "agent_normal": {"label": "Agent normal loop", "input_tokens": 20000, "output_tokens": 4000},
    "agent_reasoning": {"label": "Agent reasoning-heavy loop", "input_tokens": 20000, "output_tokens": 10000},
    "long_context": {"label": "Long context, short action", "input_tokens": 100000, "output_tokens": 4000},
}


def decimal(value: Any) -> Decimal:
    try:
        return Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        return Decimal("0")


def load_catalog(path: Path | None = None) -> dict[str, dict[str, Any]]:
    candidates = [path] if path else [DATA / "processed" / "openrouter_models.json", DATA / "raw" / "openrouter_models.json"]
    for candidate in candidates:
        if candidate and candidate.exists():
            payload = read_json(candidate)
            records = payload.get("records", payload.get("data", [])) if isinstance(payload, dict) else payload
            return {row["id"]: row for row in records if isinstance(row, dict) and row.get("id")}
    raise SystemExit("OpenRouter catalog not found; run scripts/fetch_openrouter.py --all first")


def model_cost(record: dict[str, Any], input_tokens: int, output_tokens: int, cache_read_ratio: Decimal) -> Decimal:
    pricing = record.get("pricing") or {}
    prompt = decimal(pricing.get("prompt"))
    completion = decimal(pricing.get("completion"))
    cache_read = decimal(pricing.get("input_cache_read")) if pricing.get("input_cache_read") is not None else prompt
    ratio = min(Decimal("1"), max(Decimal("0"), cache_read_ratio))
    input_cost = Decimal(input_tokens) * (Decimal("1") - ratio) * prompt
    input_cost += Decimal(input_tokens) * ratio * cache_read
    return input_cost + Decimal(output_tokens) * completion


def fmt_usd(value: Decimal) -> str:
    return f"${value:.6f}"


def build_report(catalog: dict[str, dict[str, Any]], scenarios: dict[str, dict[str, int]], cache_read_ratio: Decimal, multiplier: int) -> dict[str, Any]:
    prices: list[dict[str, Any]] = []
    results: dict[str, list[dict[str, Any]]] = {}
    for display_name, model_id in MODELS:
        record = catalog.get(model_id)
        if not record:
            prices.append({"model": display_name, "model_id": model_id, "status": "not_found"})
            continue
        pricing = record.get("pricing") or {}
        prices.append({
            "model": display_name,
            "model_id": model_id,
            "status": "ok",
            "input_per_million": float(decimal(pricing.get("prompt")) * Decimal("1000000")),
            "output_per_million": float(decimal(pricing.get("completion")) * Decimal("1000000")),
            "cache_read_per_million": float(decimal(pricing.get("input_cache_read")) * Decimal("1000000")) if pricing.get("input_cache_read") is not None else None,
            "context_length": record.get("context_length"),
        })
    for scenario_id, scenario in scenarios.items():
        rows: list[dict[str, Any]] = []
        for display_name, model_id in MODELS:
            record = catalog.get(model_id)
            if not record:
                continue
            cost = model_cost(record, scenario["input_tokens"], scenario["output_tokens"], cache_read_ratio)
            rows.append({
                "model": display_name,
                "model_id": model_id,
                "input_tokens": scenario["input_tokens"],
                "output_tokens": scenario["output_tokens"],
                "cost_per_request_usd": float(cost),
                "cost_per_multiplier_usd": float(cost * multiplier),
            })
        results[scenario_id] = sorted(rows, key=lambda row: row["cost_per_request_usd"])
    return {
        "retrieved_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "source": "OpenRouter catalog pricing",
        "cache_read_ratio": float(cache_read_ratio),
        "multiplier": multiplier,
        "models": prices,
        "scenarios": results,
    }


def markdown(payload: dict[str, Any], scenarios: dict[str, dict[str, int]]) -> str:
    lines = [
        "# OpenRouter cost test",
        "",
        f"Retrieved: `{payload['retrieved_at']}`  ",
        f"Pricing source: `{payload['source']}`  ",
        f"Cache-read ratio: `{payload['cache_read_ratio']:.2f}`  ",
        f"Multiplier: `{payload['multiplier']}` requests  ",
        "",
        "This is a deterministic token-cost simulation. It does not measure model quality or actual provider routing cost returned by a request.",
        "",
        "## Catalog prices",
        "",
        "| Model | OpenRouter ID | Input / M | Output / M | Cache read / M | Status |",
        "|---|---|---:|---:|---:|---|",
    ]
    for row in payload["models"]:
        if row["status"] != "ok":
            lines.append(f"| {row['model']} | `{row['model_id']}` | — | — | — | not found |")
            continue
        cache = f"${row['cache_read_per_million']:.6f}" if row["cache_read_per_million"] is not None else "—"
        lines.append(f"| {row['model']} | `{row['model_id']}` | ${row['input_per_million']:.6f} | ${row['output_per_million']:.6f} | {cache} | ok |")
    lines += ["", "## Cost scenarios", ""]
    for scenario_id, rows in payload["scenarios"].items():
        scenario = scenarios[scenario_id]
        lines += [
            f"### {scenario['label']}",
            f"Input: `{scenario['input_tokens']:,}` tokens; output: `{scenario['output_tokens']:,}` tokens.",
            "",
            "| Rank | Model | $/request | $/multiplier |",
            "|---:|---|---:|---:|",
        ]
        for rank, row in enumerate(rows, start=1):
            lines.append(f"| {rank} | `{row['model']}` | {fmt_usd(Decimal(str(row['cost_per_request_usd'])))} | {fmt_usd(Decimal(str(row['cost_per_multiplier_usd'])))} |")
        if rows:
            lines += ["", f"Winner by cost: **{rows[0]['model']}** ({fmt_usd(Decimal(str(rows[0]['cost_per_request_usd'])))} per request).", ""]
    lines += [
        "## Interpretation",
        "",
        "For a production decision, combine this table with the runner's actual `usage`, `cost_usd`, latency and task correctness. OpenRouter provider discounts and routing can make the effective cost differ from the catalog field.",
        "",
        "Source: [OpenRouter Models API](https://openrouter.ai/docs/api/api-reference/models/get-models).",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path)
    parser.add_argument("--cache-read-ratio", type=Decimal, default=Decimal("0"), help="Fraction of input billed at cache-read price")
    parser.add_argument("--multiplier", type=int, default=1000, help="Number of equivalent requests to price")
    parser.add_argument("--input-tokens", type=int, help="Replace defaults with one custom scenario")
    parser.add_argument("--output-tokens", type=int, help="Replace defaults with one custom scenario")
    args = parser.parse_args()
    if (args.input_tokens is None) != (args.output_tokens is None):
        raise SystemExit("--input-tokens and --output-tokens must be provided together")
    scenarios = {"custom": {"label": "Custom", "input_tokens": args.input_tokens, "output_tokens": args.output_tokens}} if args.input_tokens is not None else SCENARIOS
    payload = build_report(load_catalog(args.catalog), scenarios, args.cache_read_ratio, args.multiplier)
    date_stamp = time.strftime("%Y-%m-%d", time.gmtime())
    json_path = PROCESSED / "openrouter_cost_comparison.json"
    md_path = ROOT / "results" / f"openrouter_cost_test_{date_stamp}.md"
    write_json(json_path, payload)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text(markdown(payload, scenarios), encoding="utf-8")
    print(f"JSON saved: {json_path}")
    print(f"Markdown saved: {md_path}")
    for scenario_id, rows in payload["scenarios"].items():
        if rows:
            print(f"{scenario_id}: {rows[0]['model']} {fmt_usd(Decimal(str(rows[0]['cost_per_request_usd'])))} per request")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

