import sys
import unittest
from decimal import Decimal
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from compare_openrouter_costs import model_cost  # noqa: E402


class OpenRouterCostTests(unittest.TestCase):
    def test_cost_uses_input_and_output_rates(self):
        record = {"pricing": {"prompt": "0.0000001", "completion": "0.0000005"}}
        self.assertEqual(model_cost(record, 1_000_000, 1_000_000, Decimal("0")), Decimal("0.6"))

    def test_cache_ratio_changes_input_cost(self):
        record = {"pricing": {"prompt": "0.000001", "completion": "0", "input_cache_read": "0.0000001"}}
        self.assertEqual(model_cost(record, 1_000_000, 0, Decimal("1")), Decimal("0.1"))


if __name__ == "__main__":
    unittest.main()

