import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from analyze_openrouter_run import aggregate  # noqa: E402
from run_openrouter_arc import extract_answer_grids, usage_cost  # noqa: E402


class OpenRouterRunnerTests(unittest.TestCase):
    def test_extracts_json_answer_from_markdown_fence(self):
        text = "answer:\n```json\n{\"answers\": [[[1, 2], [3, 4]]] }\n```"
        self.assertEqual(extract_answer_grids(text), [[[1, 2], [3, 4]]])

    def test_uses_response_cost_before_catalog(self):
        cost, source = usage_cost(
            {"cost": 0.123, "prompt_tokens": 1000, "completion_tokens": 1000},
            "model/x",
            {"model/x": {"pricing": {"prompt": "1", "completion": "1"}}},
        )
        self.assertEqual(cost, 0.123)
        self.assertEqual(source, "response_usage.cost")

    def test_aggregates_score_and_cost(self):
        rows = [
            {"model": "m", "status": "ok", "task_correct": True, "cost_usd": 0.1, "latency_ms": 100, "usage": {"prompt_tokens": 2, "completion_tokens": 3}},
            {"model": "m", "status": "ok", "task_correct": False, "cost_usd": 0.2, "latency_ms": 200, "usage": {"prompt_tokens": 4, "completion_tokens": 5}},
        ]
        summary = aggregate(rows)[0]
        self.assertEqual(summary["score_pct"], 50.0)
        self.assertEqual(summary["solved_tasks"], 1)
        self.assertAlmostEqual(summary["cost_per_solved_task_usd"], 0.3)


if __name__ == "__main__":
    unittest.main()

