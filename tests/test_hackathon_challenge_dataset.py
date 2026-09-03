import csv
import json
import unittest
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = ROOT / "evaluation" / "challenge" / "uk-legal.json"


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
        cls.customers = read_rows("sample-data/uk-legal/base/customers.csv")
        cls.cases = read_rows("sample-data/uk-legal/base/cases.csv")
        cls.transactions = read_rows("sample-data/uk-legal/base/transactions.csv")
        cls.interactions = read_rows("sample-data/uk-legal/base/interactions.csv")

    def test_dataset_shape(self):
        self.assertEqual(8, self.dataset["metadata"]["total_queries"])
        for query in self.dataset["evaluation_queries"]:
            self.assertTrue(query["sdk_expected_answer"].strip(), query["id"])
        self.assertEqual(8, len(self.queries))
        self.assertEqual(8, len({query["question"] for query in self.queries.values()}))
        self.assertTrue(all(query.get("paraphrase") for query in self.queries.values()))

    def test_unsupported_question_requires_abstention(self):
        query = self.queries["HC008"]

        self.assertEqual("unsupported_question", query["category"])
        self.assertEqual("none", query["expected_source"])
        self.assertEqual("abstention", query["answer_type"])
        self.assertIsNone(query["ground_truth_sql"])

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

        customer_by_case = {row["case_id"]: row["customer_id"] for row in self.cases}
        unpaid_by_customer = {}
        for row in self.transactions:
            if row["transaction_type"] == "Invoice" and row["payment_status"] == "Unpaid":
                customer_id = customer_by_case[row["case_id"]]
                unpaid_by_customer[customer_id] = (
                    unpaid_by_customer.get(customer_id, 0.0) + float(row["amount_gbp"])
                )

        cutoff = date.today() - timedelta(days=60)
        recent_customers = {
            row["customer_id"]
            for row in self.interactions
            if datetime.strptime(row["interaction_date"], "%d/%m/%Y").date() >= cutoff
        }
        expected["HC007"] = sum(
            amount > 10000 and customer_id not in recent_customers
            for customer_id, amount in unpaid_by_customer.items()
        )

        for query_id, value in expected.items():
            self.assertEqual(value, self.queries[query_id]["ground_truth_answer"])


if __name__ == "__main__":
    unittest.main()
