"""Run ARC tasks through OpenRouter and record per-task quality/cost telemetry.

The runner intentionally accepts a local ARC task directory instead of downloading a
benchmark. This keeps dataset licensing, split choice and hidden-test handling explicit.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Iterable

from common import DATA, ROOT, load_config, number, read_json, timestamp, write_json


OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_TIMEOUT = 180


def is_grid(value: Any) -> bool:
    return (
        isinstance(value, list)
        and bool(value)
        and all(isinstance(row, list) and bool(row) for row in value)
        and len({len(row) for row in value}) == 1
        and all(not isinstance(cell, (list, dict)) for row in value for cell in row)
    )


def normalize_grid(value: Any) -> list[list[int]] | None:
    if not is_grid(value):
        return None
    try:
        grid = [[int(cell) for cell in row] for row in value]
    except (TypeError, ValueError):
        return None
    if any(cell < 0 or cell > 9 for row in grid for cell in row):
        return None
    return grid


def _json_candidates(text: str) -> Iterable[Any]:
    stripped = text.strip()
    if stripped:
        try:
            yield json.loads(stripped)
        except json.JSONDecodeError:
            pass

    for fenced in re.findall(r"```(?:json)?\s*(.*?)```", text, flags=re.IGNORECASE | re.DOTALL):
        try:
            yield json.loads(fenced.strip())
        except json.JSONDecodeError:
            pass

    decoder = json.JSONDecoder()
    for index, char in enumerate(text):
        if char not in "[{":
            continue
        try:
            value, _ = decoder.raw_decode(text[index:])
        except json.JSONDecodeError:
            continue
        yield value


def extract_answer_grids(text: str, expected_count: int = 1) -> list[list[list[int]]]:
    """Extract `answer`, `answers`, or a bare grid from a model response."""
    for candidate in _json_candidates(text):
        values: list[Any] = []
        if isinstance(candidate, dict):
            for key in ("answers", "answer", "outputs", "output", "prediction", "predictions", "grid"):
                if key in candidate:
                    values = candidate[key] if key in {"answers", "outputs", "predictions"} else [candidate[key]]
                    break
        elif is_grid(candidate):
            values = [candidate]
        elif isinstance(candidate, list) and all(is_grid(item) for item in candidate):
            values = candidate

        grids = [grid for value in values if (grid := normalize_grid(value)) is not None]
        if grids:
            return grids[:expected_count]
    return []


def load_tasks(path: Path) -> list[dict[str, Any]]:
    """Load ARC JSON files or a JSON mapping of task id to task."""
    paths = [path] if path.is_file() else sorted(path.rglob("*.json"))
    tasks: list[dict[str, Any]] = []
    for json_path in paths:
        payload = read_json(json_path)
        candidates = payload.items() if isinstance(payload, dict) and not {"train", "test"}.issubset(payload) else [(json_path.stem, payload)]
        for task_id, task in candidates:
            if not isinstance(task, dict) or not isinstance(task.get("train"), list) or not isinstance(task.get("test"), list):
                continue
            tasks.append({"task_id": str(task_id), "path": str(json_path), "task": task})
    return tasks


def grid_text(grid: Any) -> str:
    return json.dumps(grid, ensure_ascii=False, separators=(",", ":"))


def build_prompt(task: dict[str, Any]) -> str:
    train_lines: list[str] = []
    for index, example in enumerate(task["train"], start=1):
        train_lines.append(
            f"Training {index}: input={grid_text(example['input'])}; output={grid_text(example['output'])}"
        )
    test_lines = [f"Test {index}: input={grid_text(example['input'])}" for index, example in enumerate(task["test"], start=1)]
    return (
        "Solve this ARC task. Infer the exact transformation from the training pairs and apply it to every test input.\n"
        "Return ONLY valid JSON, with no markdown and no explanation, in this exact shape: "
        '{"answers": [[[0]]]} where answers contains one 2D integer grid per test input.\n\n'
        + "\n".join(train_lines)
        + "\n"
        + "\n".join(test_lines)
    )


def post_json(url: str, payload: dict[str, Any], api_key: str, timeout: int) -> tuple[dict[str, Any], dict[str, str]]:
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://arcprize.org",
            "X-Title": "arc-explorer",
            "User-Agent": "arc-explorer/0.1",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        response_body = json.loads(response.read().decode("utf-8"))
        return response_body, dict(response.headers.items())


def response_text(response: dict[str, Any]) -> str:
    choices = response.get("choices") or []
    if not choices:
        return ""
    message = choices[0].get("message") or {}
    content = message.get("content", "")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(str(part.get("text", "")) for part in content if isinstance(part, dict))
    return str(content)


def pricing_map() -> dict[str, dict[str, Any]]:
    for path in (DATA / "raw" / "openrouter_models.json", DATA / "processed" / "openrouter_models.json"):
        if not path.exists():
            continue
        payload = read_json(path)
        records = payload.get("data", payload.get("records", [])) if isinstance(payload, dict) else payload
        return {row.get("id"): row for row in records if isinstance(row, dict) and row.get("id")}
    return {}


def usage_cost(usage: dict[str, Any], model: str, prices: dict[str, dict[str, Any]]) -> tuple[float | None, str]:
    direct = number(usage.get("cost"))
    if direct is not None:
        return direct, "response_usage.cost"
    record = prices.get(model, {})
    pricing = record.get("pricing", {}) if isinstance(record, dict) else {}
    prompt_price = number(pricing.get("prompt"))
    completion_price = number(pricing.get("completion"))
    prompt_tokens = number(usage.get("prompt_tokens"))
    completion_tokens = number(usage.get("completion_tokens"))
    if prompt_price is None or completion_price is None or prompt_tokens is None or completion_tokens is None:
        return None, "unavailable"
    return prompt_price * prompt_tokens + completion_price * completion_tokens, "catalog_pricing"


def score_prediction(predicted: list[list[list[int]]], task: dict[str, Any]) -> tuple[bool | None, int | None]:
    expected = [example.get("output") for example in task.get("test", [])]
    if not expected or any(normalize_grid(grid) is None for grid in expected):
        return None, None
    if len(predicted) != len(expected):
        return False, len(expected)
    correct = sum(1 for actual, wanted in zip(predicted, expected) if actual == wanted)
    return correct == len(expected), len(expected)


def parse_models(values: list[str] | None) -> list[str]:
    if values:
        models = [item.strip() for value in values for item in value.split(",") if item.strip()]
    else:
        models = [model_id for target in load_config()["targets"] for model_id in target.get("openrouter_ids", [])]
    return list(dict.fromkeys(models))


def request_with_retry(payload: dict[str, Any], api_key: str, args: argparse.Namespace) -> tuple[dict[str, Any], dict[str, str], int]:
    last_error: Exception | None = None
    for attempt in range(args.max_retries + 1):
        try:
            return (*post_json(OPENROUTER_URL, payload, api_key, args.timeout), attempt)
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            last_error = exc
            if attempt >= args.max_retries:
                break
            time.sleep(min(60, args.retry_delay * (2 ** attempt)))
    raise RuntimeError(str(last_error))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, required=True, help="ARC task JSON file or directory")
    parser.add_argument("--model", dest="models", action="append", help="OpenRouter model ID; repeat or comma-separate")
    parser.add_argument("--run-dir", type=Path, help="Existing/new output directory; default is data/runs/<timestamp>")
    parser.add_argument("--limit", type=int, help="Run only the first N tasks")
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--delay", type=float, default=0.0, help="Seconds between requests")
    parser.add_argument("--max-retries", type=int, default=3)
    parser.add_argument("--retry-delay", type=float, default=2.0)
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    parser.add_argument("--max-output-tokens", type=int, default=32768)
    parser.add_argument("--reasoning-effort", choices=("low", "medium", "high", "xhigh", "max"))
    parser.add_argument("--resume", action="store_true", help="Skip model/task pairs already present in results.ndjson")
    args = parser.parse_args()

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise SystemExit("OPENROUTER_API_KEY is not set")
    if not args.dataset.exists():
        raise SystemExit(f"Dataset path does not exist: {args.dataset}")

    run_dir = args.run_dir or (DATA / "runs" / f"openrouter_arc_{time.strftime('%Y%m%d_%H%M%S', time.gmtime())}")
    run_dir.mkdir(parents=True, exist_ok=True)
    results_path = run_dir / "results.ndjson"
    tasks = load_tasks(args.dataset)[args.offset:]
    if args.limit is not None:
        tasks = tasks[:args.limit]
    models = parse_models(args.models)
    if not models:
        raise SystemExit("No OpenRouter models selected")

    completed: set[tuple[str, str]] = set()
    if args.resume and results_path.exists():
        for line in results_path.read_text(encoding="utf-8").splitlines():
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            completed.add((row.get("model"), row.get("task_id")))

    metadata = {
        "benchmark": "ARC-AGI-2-compatible-local-tasks",
        "dataset": str(args.dataset.resolve()),
        "models": models,
        "started_at": timestamp(),
        "openrouter_url": OPENROUTER_URL,
        "reasoning_effort": args.reasoning_effort,
        "temperature": 0,
    }
    write_json(run_dir / "run.json", metadata)
    prices = pricing_map()
    with results_path.open("a", encoding="utf-8") as output:
        for model in models:
            for item in tasks:
                task_id = item["task_id"]
                if (model, task_id) in completed:
                    continue
                prompt = build_prompt(item["task"])
                payload: dict[str, Any] = {
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0,
                    "max_tokens": args.max_output_tokens,
                }
                if args.reasoning_effort:
                    payload["reasoning"] = {"effort": args.reasoning_effort}
                started = time.perf_counter()
                record: dict[str, Any] = {
                    "model": model,
                    "task_id": task_id,
                    "task_path": item["path"],
                    "started_at": timestamp(),
                }
                try:
                    response, headers, retry_count = request_with_retry(payload, api_key, args)
                    elapsed_ms = round((time.perf_counter() - started) * 1000, 1)
                    text = response_text(response)
                    predicted = extract_answer_grids(text, len(item["task"].get("test", [])))
                    task_correct, labeled_count = score_prediction(predicted, item["task"])
                    usage = response.get("usage") or {}
                    cost, cost_source = usage_cost(usage, model, prices)
                    completion_tokens = number(usage.get("completion_tokens"))
                    record.update({
                        "status": "ok",
                        "retry_count": retry_count,
                        "latency_ms": elapsed_ms,
                        "provider": response.get("provider") or headers.get("x-openrouter-provider"),
                        "returned_model": response.get("model"),
                        "usage": usage,
                        "output_tokens_per_sec": round(completion_tokens / (elapsed_ms / 1000), 3) if completion_tokens is not None and elapsed_ms > 0 else None,
                        "cost_usd": cost,
                        "cost_source": cost_source,
                        "assistant_text": text,
                        "predicted_answers": predicted,
                        "task_correct": task_correct,
                        "labeled_test_count": labeled_count,
                    })
                except Exception as exc:  # Keep the run resumable after one failed request.
                    record.update({
                        "status": "error",
                        "latency_ms": round((time.perf_counter() - started) * 1000, 1),
                        "error": str(exc),
                    })
                output.write(json.dumps(record, ensure_ascii=False) + "\n")
                output.flush()
                if args.delay:
                    time.sleep(args.delay)
    print(f"Run saved: {run_dir}")
    print(f"Analyze: python scripts/analyze_openrouter_run.py --run-dir {run_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
