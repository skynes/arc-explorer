import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from fetch_community import collect_rows  # noqa: E402


class CommunityIngestTests(unittest.TestCase):
    def test_version_models_are_carried_into_score(self):
        data = {
            "name": "A community method",
            "versions": [{
                "date": "2026-10-01",
                "models": [{"name": "GPT-6 Luna"}],
                "scores": [{"benchmark": "arc-agi-2", "set": "semi-private", "score": 59.0, "cost": 0.06}],
            }],
        }
        rows = collect_rows(data, "", "example")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["target_key"], "gpt-6-luna")
        self.assertEqual(rows[0]["verification_status"], "community_self_reported")


if __name__ == "__main__":
    unittest.main()

