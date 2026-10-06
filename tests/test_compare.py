import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from compare_arc import apply_pareto, official_best  # noqa: E402


class CompareTests(unittest.TestCase):
    def test_best_variant_and_efficiency(self):
        targets = [
            {"key": "a", "name": "A", "aliases": ["A"]},
            {"key": "b", "name": "B", "aliases": ["B"]},
        ]
        rows = [
            {"target_key": "a", "model_name": "A", "variant": "low", "score_pct": 50, "cost_per_task_usd": 0.1},
            {"target_key": "a", "model_name": "A", "variant": "max", "score_pct": 60, "cost_per_task_usd": 0.2},
            {"target_key": "b", "model_name": "B", "variant": "max", "score_pct": 55, "cost_per_task_usd": 0.5},
        ]
        best = official_best(rows, targets)
        self.assertEqual(best[0]["variant"], "max")
        for row in best:
            if row.get("score_pct") and row.get("cost_per_task_usd"):
                row["score_per_dollar"] = row["score_pct"] / row["cost_per_task_usd"]
        apply_pareto(best)
        self.assertTrue(best[0]["pareto_optimal"])
        self.assertFalse(best[1]["pareto_optimal"])


if __name__ == "__main__":
    unittest.main()

