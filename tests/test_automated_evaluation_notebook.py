import json
import os
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUTOMATED_NOTEBOOK = ROOT / "NB_Automated_Data_Agent_Evaluation.ipynb"
SDK_NOTEBOOK = ROOT / "NB_Run_SDK_Evaluation.ipynb"


class NotebookContractMixin:
    def assert_notebook_contract(self, path):
        notebook = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(4, notebook["nbformat"])
        identifiers = [cell["id"] for cell in notebook["cells"]]
        self.assertEqual(len(identifiers), len(set(identifiers)))
        for number, cell in enumerate(notebook["cells"], start=1):
            self.assertIn(cell["cell_type"], {"code", "markdown"})
            if cell["cell_type"] == "code":
                compile("".join(cell["source"]), f"{path.name}-cell-{number}", "exec")
        return notebook


class AutomatedEvaluationNotebookTests(NotebookContractMixin, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.notebook = json.loads(AUTOMATED_NOTEBOOK.read_text(encoding="utf-8"))
        cls.code = [
            "".join(cell["source"])
            for cell in cls.notebook["cells"]
            if cell["cell_type"] == "code"
        ]

    def test_notebook_structure_and_compilation(self):
        self.assert_notebook_contract(AUTOMATED_NOTEBOOK)
        self.assertEqual(10, len(self.code))

    def execute_notebook(self, populate=False):
        namespace = {"display": lambda *args, **kwargs: None}
        previous_directory = Path.cwd()
        with tempfile.TemporaryDirectory() as temporary_directory:
            try:
                os.chdir(temporary_directory)
                for index, source in enumerate(self.code):
                    exec(source, namespace)
                    if populate and index == 2:
                        for observation in namespace["OBSERVATIONS"]:
                            expected = namespace["challenge_by_id"][observation["id"]]
                            for phase_name in ("baseline", "final"):
                                phase = observation[phase_name]
                                phase.update(
                                    {
                                        "original_answer": expected["expected_answer"],
                                        "paraphrase_answer": expected["expected_answer"],
                                        "selected_source": expected["expected_source"],
                                        "query_evidence": "EVALUATE copied evidence",
                                        "logic_correct": True,
                                    }
                                )
                exported_report = json.loads(namespace["JSON_PATH"].read_text(encoding="utf-8"))
                return namespace, exported_report
            finally:
                os.chdir(previous_directory)

    def test_blank_inputs_produce_actionable_report(self):
        namespace, report = self.execute_notebook(populate=False)
        self.assertEqual(60, len(namespace["validation_issues"]))
        self.assertEqual(0.0, namespace["baseline_total"])
        self.assertEqual(0.0, namespace["final_total"])
        self.assertEqual(0.0, report["summary"]["final_score"])
        self.assertFalse(namespace["RUN_SDK_AUTOMATION"])

    def test_complete_inputs_score_and_export_24(self):
        namespace, report = self.execute_notebook(populate=True)
        self.assertEqual([], namespace["validation_issues"])
        self.assertEqual(24.0, namespace["baseline_total"])
        self.assertEqual(24.0, namespace["final_total"])
        self.assertEqual(6, len(namespace["scorecard_df"]))
        self.assertEqual(24.0, report["summary"]["baseline_score"])
        self.assertEqual(24.0, report["summary"]["final_score"])
        for check, complete in namespace["artifact_checks"].items():
            if check != "Screenshots or copied run-step evidence attached":
                self.assertTrue(complete, check)


class SdkSnapshotNotebookTests(NotebookContractMixin, unittest.TestCase):
    def test_snapshot_notebook_contract(self):
        notebook = self.assert_notebook_contract(SDK_NOTEBOOK)
        code = [
            "".join(cell["source"])
            for cell in notebook["cells"]
            if cell["cell_type"] == "code"
        ]
        source = "\n".join(code)
        self.assertIn("fabric-data-agent-sdk>=0.1.30a0", code[0])
        self.assertIn("typing_extensions>=4.12.2", code[0])
        self.assertIn("PyJWT>=2.6.0", code[0])
        self.assertIn("notebookutils.session.restartPython()", code[0])
        self.assertIn('import_module("fabric.dataagent.evaluation")', code[1])
        self.assertIn('WORKSPACE_NAME = "Hackathon"', code[1])
        self.assertIn('DATA_AGENT_STAGE = "sandbox"', code[1])
        self.assertIn("valid_data_agent_stages", code[3])
        self.assertIn("data_agent_stage=data_agent_stage", code[3])
        self.assertNotIn('data_agent_stage="sandbox"', code[3])
        markdown = "\n".join(
            "".join(cell["source"])
            for cell in notebook["cells"]
            if cell["cell_type"] == "markdown"
        )
        self.assertIn("default Lakehouse", markdown)
        self.assertIn("Tables", markdown)
        self.assertIn("TABLE_NAME", markdown)
        self.assertIn('SNAPSHOT_NAME = "final"', source)
        self.assertIn("INCLUDE_PARAPHRASES = True", source)
        self.assertIn('"id": f"{item[\'id\']}-P"', source)
        self.assertIn("query_results", (ROOT / "evaluation" / "evaluate_agent.py").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
