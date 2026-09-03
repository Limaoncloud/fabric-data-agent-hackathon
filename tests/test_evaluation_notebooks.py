import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SDK_NOTEBOOK = ROOT / "NB_Run_SDK_Evaluation.ipynb"


class NotebookContractMixin:
    def assert_notebook_contract(self, path):
        notebook = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(4, notebook["nbformat"])
        identifiers = [cell["id"] for cell in notebook["cells"]]
        self.assertEqual(len(identifiers), len(set(identifiers)))
        self.assertEqual("python", notebook["metadata"]["language_info"]["name"])
        for number, cell in enumerate(notebook["cells"], start=1):
            self.assertIn(cell["cell_type"], {"code", "markdown"})
            if cell["cell_type"] == "code":
                compile("".join(cell["source"]), f"{path.name}-cell-{number}", "exec")
        return notebook


class SdkSnapshotNotebookTests(NotebookContractMixin, unittest.TestCase):
    def test_review_notebook_is_removed(self):
        self.assertFalse((ROOT / "NB_Review_And_Score_Data_Agent.ipynb").exists())

    def test_snapshot_notebook_contract(self):
        notebook = self.assert_notebook_contract(SDK_NOTEBOOK)
        code = [
            "".join(cell["source"])
            for cell in notebook["cells"]
            if cell["cell_type"] == "code"
        ]
        source = "\n".join(code)
        self.assertIn("fabric-data-agent-sdk==0.1.30a0", code[0])
        self.assertIn("typing_extensions>=4.12.2", code[0])
        self.assertIn("PyJWT>=2.6.0", code[0])
        self.assertIn("notebookutils.session.restartPython()", code[0])
        self.assertIn('import_module("fabric.dataagent.evaluation")', code[1])
        self.assertIn('import_module("fabric.dataagent._fabric_runtime")', code[1])
        self.assertIn('import_module("fabric.dataagent.evaluation._storage")', code[1])
        self.assertIn('fabric_context.get("trident.lakehouse.id")', code[1])
        self.assertIn('fabric_context.get("fs.defaultFS")', code[1])
        self.assertIn('WORKSPACE_NAME = "Hackathon"', code[1])
        self.assertIn('DATA_AGENT_STAGE = "sandbox"', code[1])
        self.assertIn("valid_data_agent_stages", code[3])
        self.assertIn('"data_agent_stage": data_agent_stage', code[3])
        self.assertIn("fabric_evaluation.evaluate_data_agent", code[3])
        self.assertIn("fabric_evaluation.get_evaluation_summary", code[3])
        self.assertIn("fabric_evaluation.get_evaluation_details", code[3])
        self.assertIn('item.get("sdk_expected_answer", item["ground_truth_answer"])', code[2])
        self.assertIn('"expected_answer": [item["sdk_expected_answer"]', code[3])
        self.assertNotIn("DataAgentEvaluator", source)
        self.assertNotIn("evaluate_agent.py", source)
        markdown = "\n".join(
            "".join(cell["source"])
            for cell in notebook["cells"]
            if cell["cell_type"] == "markdown"
        )
        self.assertIn("default Lakehouse", markdown)
        self.assertIn("LegalFirmDemo", markdown)
        self.assertIn("TABLE_NAME", markdown)
        self.assertIn("you do not create it manually", markdown)
        self.assertIn('SNAPSHOT_NAME = "step1_baseline"', source)
        for snapshot_name in (
            "step1_baseline",
            "step2_prep_ai",
            "step3_lakehouse_added",
            "step4_lakehouse_tuned",
            "step5_final",
            "step5_routing",
        ):
            self.assertIn(f'"{snapshot_name}"', source)
        self.assertIn('INCLUDE_PARAPHRASES = DATASET_NAME == "challenge"', source)
        self.assertIn('"id": f"{item[\'id\']}-P"', source)
        self.assertIn('evaluation_storage._get_data(f"{TABLE_NAME}_steps")', source)
        self.assertIn('"official_details":', source)
        self.assertIn('"official_steps":', source)
        self.assertIn('"snapshot_name"', source)
        self.assertIn('"selected_source"', source)
        self.assertIn('"query_type"', source)
        self.assertIn('"generated_query"', source)
        self.assertIn('"thread_link"', source)
        self.assertIn("WARNING: SQL/DAX/KQL was unavailable", source)
        self.assertIn("Question-by-step SDK judgement", source)
        self.assertIn("judgement_matrix_df", source)


if __name__ == "__main__":
    unittest.main()
