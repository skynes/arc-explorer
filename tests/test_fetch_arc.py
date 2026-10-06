import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from fetch_arc import extract_official_rows  # noqa: E402


class OfficialIngestTests(unittest.TestCase):
    def test_nested_evaluation_is_normalized(self):
        models = {"models": [{"id": "openai-gpt-6-luna-max", "name": "GPT-6 Luna (Max)"}]}
        evaluations = [{
            "modelId": "openai-gpt-6-luna-max",
            "display": True,
            "evaluationResults": [{
                "datasetId": "v2_Semi_Private",
                "score": 0.593,
                "costPerTask": 0.062,
                "reasoningEffort": "Max",
            }],
        }]
        targets = [{"key": "gpt-6-luna", "name": "GPT-6 Luna", "aliases": ["GPT-6 Luna"]}]
        rows = extract_official_rows(evaluations, models, targets)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["target_key"], "gpt-6-luna")
        self.assertAlmostEqual(rows[0]["score_pct"], 59.3)
        self.assertAlmostEqual(rows[0]["cost_per_task_usd"], 0.062)


if __name__ == "__main__":
    unittest.main()

