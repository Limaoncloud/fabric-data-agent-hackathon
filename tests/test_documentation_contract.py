import csv
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class DocumentationContractTests(unittest.TestCase):
    def test_participant_guide_uses_source_specific_controls(self):
        guide = (ROOT / "USER_GUIDE.md").read_text(encoding="utf-8")
        self.assertIn("Lakehouse tables do not have the semantic-model synonym editor", guide)
        self.assertIn("Data agent instructions", guide)
        self.assertIn("add `matter` and `matters` as synonyms for the `Cases` table", guide)
        self.assertIn("How many payment transactions were recorded?", guide)
        self.assertIn("WHERE transaction_type = 'Payment'", guide)
        self.assertIn("not for the `LegalFirmBasic` or `LegalFirmOptimized`", guide)
        self.assertNotIn("add one relevant synonym rather than changing", guide)

    def test_lakehouse_sql_example_matches_current_data(self):
        with (ROOT / "sample-data" / "uk-legal" / "base" / "transactions.csv").open(
            encoding="utf-8", newline=""
        ) as handle:
            rows = list(csv.DictReader(handle))
        payment_count = sum(row["transaction_type"] == "Payment" for row in rows)
        self.assertEqual(199, payment_count)

    def test_facilitator_guide_separates_lakehouse_and_model_controls(self):
        guide = (ROOT / "evaluation" / "FACILITATOR_GUIDE.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("## Controls By Source Type", guide)
        self.assertIn("Do not tell participants to add synonyms to Lakehouse tables", guide)
        self.assertIn("not Power BI semantic-model sources", guide)

    def test_operator_skill_preserves_untuned_baseline(self):
        skill = (
            ROOT / "skills" / "fabric-data-agent-hackathon" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "Leave Data Agent instructions and example queries empty for the first baseline run",
            skill,
        )
        self.assertIn(
            "do not describe this as adding table synonyms",
            skill,
        )

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
            ["LegalFirmOptimized", "LegalFirmDemo"],
            [source["name"] for source in reference["dataSources"]],
        )
        profile_lakehouse_tables = profile["agent"]["sources"][1]["objects"]
        reference_lakehouse_tables = reference["dataSources"][1]["selectedTables"]
        self.assertEqual(profile_lakehouse_tables, reference_lakehouse_tables)

        user_guide = (ROOT / "USER_GUIDE.md").read_text(encoding="utf-8")
        self.assertIn("one Data Agent with two complementary sources", user_guide)
        self.assertNotIn("Add at least 4-5 data sources", user_guide)


if __name__ == "__main__":
    unittest.main()
