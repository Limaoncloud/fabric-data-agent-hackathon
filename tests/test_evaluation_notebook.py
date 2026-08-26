import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = ROOT / "NB_Evaluate_Data_Agent_Hackathon.ipynb"
CHALLENGE_PATH = ROOT / "evaluation" / "hackathon_challenge_dataset.json"


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self.payload


class EvaluationNotebookTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.notebook = json.loads(NOTEBOOK_PATH.read_text(encoding="utf-8"))
        cls.cells = cls.notebook["cells"]
        cls.challenge = json.loads(CHALLENGE_PATH.read_text(encoding="utf-8"))
        cls.code = [
            "".join(cell["source"])
            for cell in cls.cells
            if cell["cell_type"] == "code"
        ]

    def test_structure_and_code_compilation(self):
        self.assertEqual(19, len(self.cells))
        identifiers = [cell["id"] for cell in self.cells]
        self.assertEqual(len(identifiers), len(set(identifiers)))
        for number, cell in enumerate(self.cells, start=1):
            self.assertIn(cell["cell_type"], {"code", "markdown"})
            expected_language = "python" if cell["cell_type"] == "code" else "markdown"
            self.assertEqual(expected_language, cell["metadata"]["language"])
            if cell["cell_type"] == "code":
                compile("".join(cell["source"]), f"cell-{number}", "exec")

    @unittest.skipUnless(importlib.util.find_spec("pandas"), "pandas is not installed")
    def test_perfect_submission_scores_24(self):
        namespace = {}
        exec(self.code[0], namespace)
        exec(self.code[1], namespace)
        exec(self.code[2], namespace)

        challenge_by_id = {
            item["id"]: item for item in self.challenge["evaluation_queries"]
        }
        for result in namespace["TEST_RESULTS"]:
            expected = challenge_by_id[result["id"]]
            result.update(
                {
                    "baseline_answer": expected["ground_truth_answer"],
                    "baseline_source": expected["expected_source"],
                    "baseline_logic_correct": True,
                    "baseline_paraphrase_answer": expected["ground_truth_answer"],
                    "final_answer": expected["ground_truth_answer"],
                    "final_source": expected["expected_source"],
                    "final_logic_correct": True,
                    "paraphrase_answer": expected["ground_truth_answer"],
                }
            )

        namespace["requests"].get = lambda *args, **kwargs: FakeResponse(self.challenge)
        for cell_code in self.code[3:7]:
            exec(cell_code, namespace)

        self.assertEqual(24.0, namespace["baseline_total"])
        self.assertEqual(24.0, namespace["final_total"])
        self.assertEqual("Pass", namespace["overall_status"])
        self.assertEqual("Strong and robust", namespace["final_rating"])
        self.assertEqual(6, namespace["passed_tests"])

        with tempfile.TemporaryDirectory() as output_directory:
            export_code = self.code[7].replace(
                'OUTPUT_DIRECTORY = Path(".")',
                f"OUTPUT_DIRECTORY = Path({output_directory!r})",
            )
            exec(export_code, namespace)
            exec(self.code[8], namespace)
            self.assertTrue(namespace["csv_path"].is_file())
            self.assertTrue(namespace["json_path"].is_file())
            exported = json.loads(namespace["json_path"].read_text(encoding="utf-8"))
            self.assertEqual(24.0, exported["summary"]["final_score"])

    @unittest.skipUnless(importlib.util.find_spec("pandas"), "pandas is not installed")
    def test_blank_final_inputs_are_rejected(self):
        namespace = {}
        exec(self.code[0], namespace)
        exec(self.code[1], namespace)
        exec(self.code[2], namespace)
        namespace["requests"].get = lambda *args, **kwargs: FakeResponse(self.challenge)
        with self.assertRaisesRegex(ValueError, "blank final fields"):
            exec(self.code[3], namespace)


if __name__ == "__main__":
    unittest.main()
