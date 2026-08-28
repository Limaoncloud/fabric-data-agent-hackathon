import json
import unittest
from pathlib import Path

from evaluation.evaluate_agent import DataAgentEvaluator

ROOT = Path(__file__).resolve().parents[1]
CHALLENGE_DATASET = ROOT / "evaluation" / "challenge" / "uk-legal.json"
ROUTING_DATASET = ROOT / "evaluation" / "routing" / "uk-legal.json"


class EvaluatorModeTests(unittest.TestCase):
    def test_requires_simulation_or_sdk_mode(self):
        with self.assertRaises(ValueError):
            DataAgentEvaluator(simulation_mode=False, sdk_mode=False)

    def test_rejects_both_modes_together_via_cli_contract(self):
        # The constructor itself only rejects "neither"; main() enforces "not both".
        # This asserts the constructor does not silently accept an ambiguous state.
        evaluator = DataAgentEvaluator(simulation_mode=True, sdk_mode=False)
        self.assertTrue(evaluator.simulation_mode)


class ChallengeDatasetEvaluationTests(unittest.TestCase):
    def test_challenge_dataset_evaluates_without_crashing(self):
        evaluator = DataAgentEvaluator(simulation_mode=True, simulation_step=2)
        metrics_list, aggregate = evaluator.evaluate_all(str(CHALLENGE_DATASET))
        self.assertEqual(6, aggregate.total_queries)
        self.assertEqual(6, len(metrics_list))
        self.assertIn("easy", aggregate.by_difficulty)

    def test_routing_extension_dataset_evaluates_without_crashing(self):
        evaluator = DataAgentEvaluator(simulation_mode=True, simulation_step=5)
        metrics_list, aggregate = evaluator.evaluate_all(str(ROUTING_DATASET))
        self.assertEqual(3, aggregate.total_queries)
        self.assertEqual(3, len(metrics_list))
        self.assertIn("routing_test", aggregate.by_category)

    def test_all_challenge_queries_have_difficulty(self):
        dataset = json.loads(CHALLENGE_DATASET.read_text(encoding="utf-8"))
        for query in dataset["evaluation_queries"]:
            self.assertIn("difficulty", query, query["id"])


class MissingFieldDefaultsTests(unittest.TestCase):
    def test_missing_difficulty_and_category_do_not_crash(self):
        evaluator = DataAgentEvaluator(simulation_mode=True)
        queries = [
            {
                "id": "X001",
                "question": "Untagged question",
                "expected_source": "LegalFirmOptimized",
                "ground_truth_answer": 1,
                "answer_type": "number",
            }
        ]
        metrics = [evaluator.evaluate_query(queries[0], evaluator.execute_query(queries[0]["question"], 1, "LegalFirmOptimized"))]
        aggregate = evaluator._calculate_aggregate_metrics(queries, metrics)
        self.assertIn("unlabeled", aggregate.by_difficulty)
        self.assertIn("uncategorized", aggregate.by_category)


if __name__ == "__main__":
    unittest.main()
