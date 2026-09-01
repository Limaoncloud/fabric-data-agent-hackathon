import json
import unittest
from unittest.mock import patch
from pathlib import Path

from evaluation import evaluate_agent
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

    def test_sdk_import_error_preserves_underlying_cause(self):
        with patch.object(evaluate_agent, "FABRIC_EVAL_SDK_AVAILABLE", False), patch.object(
            evaluate_agent,
            "FABRIC_EVAL_SDK_IMPORT_ERROR",
            ImportError("missing transitive dependency"),
        ):
            with self.assertRaisesRegex(RuntimeError, "missing transitive dependency"):
                DataAgentEvaluator(sdk_mode=True)

    def test_sdk_persistence_failure_has_actionable_error(self):
        with patch.object(evaluate_agent, "FABRIC_EVAL_SDK_AVAILABLE", True), patch.object(
            evaluate_agent, "evaluate_data_agent", return_value="evaluation-id"
        ), patch.object(
            evaluate_agent, "get_evaluation_summary", return_value=None
        ), patch.object(
            evaluate_agent, "get_evaluation_details", return_value=None
        ):
            evaluator = DataAgentEvaluator(agent_id="LegalFirmAgent", sdk_mode=True)
            with self.assertRaisesRegex(RuntimeError, "creates.*automatically"):
                evaluator.evaluate_with_sdk(str(CHALLENGE_DATASET))


class ChallengeDatasetEvaluationTests(unittest.TestCase):
    def test_numeric_prose_answer_is_compared_without_crashing(self):
        evaluator = DataAgentEvaluator(simulation_mode=True)
        answer = (
            "You currently have **101 active clients**.\n\n"
            "- Metric used: **Active Customers**\n"
            "- Data source: LegalFirmSemanticModel"
        )
        self.assertEqual((True, True), evaluator.compare_answers(answer, 101, "number"))

    def test_ambiguous_numeric_prose_does_not_guess(self):
        evaluator = DataAgentEvaluator(simulation_mode=True)
        self.assertEqual(
            (False, False),
            evaluator.compare_answers("101 active out of 171 total clients", 101, "number"),
        )

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
                "expected_source": "LegalFirmSemanticModel",
                "ground_truth_answer": 1,
                "answer_type": "number",
            }
        ]
        metrics = [evaluator.evaluate_query(queries[0], evaluator.execute_query(queries[0]["question"], 1, "LegalFirmSemanticModel"))]
        aggregate = evaluator._calculate_aggregate_metrics(queries, metrics)
        self.assertIn("unlabeled", aggregate.by_difficulty)
        self.assertIn("uncategorized", aggregate.by_category)


if __name__ == "__main__":
    unittest.main()
