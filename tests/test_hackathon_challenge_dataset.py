import csv
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = ROOT / "evaluation" / "hackathon_challenge_dataset.json"


def read_rows(relative_path):
    with (ROOT / relative_path).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


class HackathonChallengeDatasetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dataset = json.loads(DATASET_PATH.read_text(encoding="utf-8"))
        cls.queries = {
            query["id"]: query for query in cls.dataset["evaluation_queries"]
        }
        cls.customers = read_rows("step1/step1_cleaned_customers.csv")
        cls.cases = read_rows("step1/step1_cleaned_cases.csv")
        cls.transactions = read_rows("step1/step1_cleaned_transactions.csv")

    def test_dataset_shape(self):
        self.assertEqual(6, self.dataset["metadata"]["total_queries"])
        self.assertEqual(6, len(self.queries))
        self.assertEqual(6, len({query["question"] for query in self.queries.values()}))
        self.assertTrue(all(query.get("paraphrase") for query in self.queries.values()))

    def test_ground_truth_matches_current_csvs(self):
        expected = {
            "HC001": sum(row["status"] == "Active" for row in self.customers),
            "HC002": sum(float(row["case_value_gbp"]) for row in self.cases),
            "HC003": sum(
                float(row["amount_gbp"])
                for row in self.transactions
                if row["transaction_type"] == "Invoice"
            ),
            "HC004": sum(
                row["transaction_type"] == "Invoice"
                and row["payment_status"] == "Unpaid"
                for row in self.transactions
            ),
            "HC005": sum(row["case_status"] == "Open" for row in self.cases),
            "HC006": len(self.customers),
        }
        for query_id, value in expected.items():
            self.assertEqual(value, self.queries[query_id]["ground_truth_answer"])


if __name__ == "__main__":
    unittest.main()
