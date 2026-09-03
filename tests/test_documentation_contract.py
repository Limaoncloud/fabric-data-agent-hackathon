import csv
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class DocumentationContractTests(unittest.TestCase):
    def test_participant_guide_uses_source_specific_controls(self):
        guide = (ROOT / "USER_GUIDE.md").read_text(encoding="utf-8")
        self.assertIn("Required staged evaluation:", guide)
        self.assertIn("only required participant evaluation notebook", guide)
        self.assertNotIn("NB_Review_And_Score_Data_Agent.ipynb", guide)
        self.assertIn('SNAPSHOT_NAME = "step1_baseline"', guide)
        self.assertIn('SNAPSHOT_NAME = "step5_routing"', guide)
        self.assertIn("16 prompts", guide)
        self.assertIn("Step 6 ontology remains an optional qualitative exercise", guide)
        self.assertIn("Lakehouse tables do not have the semantic-model synonym editor", guide)
        self.assertIn("Data agent instructions", guide)
        self.assertIn("add `matter` and `matters` as synonyms for the `Cases` table", guide)
        self.assertIn("Find transaction TXN000001 and show all its available details.", guide)
        self.assertIn("Show the detailed case record for CASE0001.", guide)
        self.assertIn("Find interaction INT000001 and show all its available details.", guide)
        self.assertIn("WHERE transaction_id = 'TXN000001'", guide)
        self.assertIn("WHERE case_id = 'CASE0001'", guide)
        self.assertIn("WHERE interaction_id = 'INT000001'", guide)
        self.assertIn("not for the `LegalFirmSemanticModel` Power BI semantic-model source", guide)
        self.assertNotIn("add one relevant synonym rather than changing", guide)

    def test_lakehouse_sql_examples_match_current_data(self):
        examples = (
            ("transactions.csv", "transaction_id", "TXN000001"),
            ("cases.csv", "case_id", "CASE0001"),
            ("interactions.csv", "interaction_id", "INT000001"),
        )
        base_dir = ROOT / "sample-data" / "uk-legal" / "base"
        for filename, identifier_column, identifier in examples:
            with self.subTest(identifier=identifier):
                with (base_dir / filename).open(encoding="utf-8", newline="") as handle:
                    matches = [
                        row
                        for row in csv.DictReader(handle)
                        if row[identifier_column] == identifier
                    ]
                self.assertEqual(1, len(matches))

    def test_facilitator_guide_separates_lakehouse_and_model_controls(self):
        guide = (ROOT / "FACILITATOR_GUIDE.md").read_text(encoding="utf-8")
        self.assertIn("## How To Use This Guide", guide)
        self.assertIn("## Facilitator Solution Checkpoints", guide)
        self.assertIn("### Step 2: Prep For AI And Agent Instructions", guide)
        self.assertIn("### Step 5: Prepared Tables And Multi-Source Routing", guide)
        self.assertIn("NB_Run_SDK_Evaluation.ipynb", guide)
        self.assertNotIn("NB_Review_And_Score_Data_Agent.ipynb", guide)
        self.assertIn('SNAPSHOT_NAME = "step2_prep_ai"', guide)
        self.assertIn('SNAPSHOT_NAME = "step3_lakehouse_added"', guide)
        self.assertIn('SNAPSHOT_NAME = "step4_lakehouse_tuned"', guide)
        self.assertIn('SNAPSHOT_NAME = "step5_final"', guide)
        self.assertIn('SNAPSHOT_NAME = "step5_routing"', guide)
        self.assertIn("## Controls By Source Type", guide)
        self.assertIn("Do not tell participants to add synonyms to Lakehouse tables", guide)
        self.assertIn("not Power BI semantic-model sources", guide)
        self.assertNotIn("base_* tables for detailed records", guide)
        self.assertFalse((ROOT / "evaluation" / "FACILITATOR_GUIDE.md").exists())

        model_reference = (
            ROOT / "semantic-model" / "optimized" / "uk-legal" / "README.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Artifact Reference", model_reference)
        self.assertIn("FACILITATOR_GUIDE.md", model_reference)
        self.assertNotIn("## 5. Create a report for verified answers", model_reference)

    def test_generation_prompt_preserves_untuned_baseline(self):
        prompt = (
            ROOT / ".github" / "prompts" / "generate-hackathon-domain.prompt.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "Leave Data Agent instructions and example queries empty for the first baseline run",
            prompt,
        )
        self.assertIn(
            "do not describe this as adding table synonyms",
            prompt,
        )
        self.assertIn("never ask them to create, open, or edit JSON", prompt)
        self.assertFalse(
            (ROOT / "skills" / "fabric-data-agent-hackathon" / "SKILL.md").exists()
        )

    def test_reuse_guide_is_json_free_and_time_bounded(self):
        guide = (ROOT / "REUSE_FOR_NEW_INDUSTRY.md").read_text(encoding="utf-8")
        for expected in (
            "# Reuse This Hackathon Without Editing JSON",
            "less than one hour of CSA time",
            "Generate Hackathon Domain",
            "Copy-Paste Example: Water Utilities",
            "guides/<domain>/USER_GUIDE.md",
            "guides/<domain>/FACILITATOR_GUIDE.md",
            "six scored challenge questions and three routing questions",
            "expected answers calculated from the generated CSVs",
            'DOMAIN_PROFILE = "water-utilities"',
        ):
            self.assertIn(expected, guide)
        self.assertNotIn("Edit `config/domain-briefs/", guide)

    def test_step6_reference_matches_two_source_profile(self):
        profile = json.loads(
            (ROOT / "config" / "domains" / "uk-legal.json").read_text(
                encoding="utf-8"
            )
        )
        reference = json.loads(
            (ROOT / "agent-configuration" / "routing" / "uk-legal" / "data-agent-configuration.json").read_text(
                encoding="utf-8"
            )
        )["dataAgentConfiguration"]

        self.assertEqual(
            ["LegalFirmSemanticModel", "LegalFirmDemo"],
            [source["name"] for source in reference["dataSources"]],
        )
        profile_lakehouse_tables = profile["agent"]["sources"][1]["objects"]
        reference_lakehouse_tables = reference["dataSources"][1]["selectedTables"]
        self.assertEqual(profile_lakehouse_tables, reference_lakehouse_tables)

        user_guide = (ROOT / "USER_GUIDE.md").read_text(encoding="utf-8")
        self.assertIn("one Data Agent with two complementary sources", user_guide)
        self.assertIn("[FACILITATOR_GUIDE.md](FACILITATOR_GUIDE.md)", user_guide)
        self.assertNotIn("evaluation/FACILITATOR_GUIDE.md", user_guide)
        self.assertNotIn("raw base_* Lakehouse tables", user_guide)
        self.assertNotIn("Add at least 4-5 data sources", user_guide)
        self.assertNotIn("step6_", user_guide)
        self.assertIn("Deselect the five `base_*` tables", user_guide)

        root_readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("## Start Here", root_readme)
        self.assertNotIn("The three routing folders are intentionally separate", root_readme)

        self.assertFalse((ROOT / "README_MULTITABLE.md").exists())
        self.assertNotIn("step6_", root_readme)
        self.assertNotIn("final Step 5 configuration", root_readme)
        self.assertNotIn("## Multi-Table Architecture", root_readme)
        self.assertIn("The three routing folders are intentionally separate", user_guide)
        self.assertIn("## Multi-Table Architecture", user_guide)

        facilitator_guide = (ROOT / "FACILITATOR_GUIDE.md").read_text(encoding="utf-8")
        self.assertIn("The three routing folders are intentionally separate", facilitator_guide)
        self.assertIn("final Step 5 configuration", facilitator_guide)
        self.assertIn("## Multi-Table Architecture", facilitator_guide)


if __name__ == "__main__":
    unittest.main()
