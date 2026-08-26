import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class DocumentationContractTests(unittest.TestCase):
    def test_participant_guide_uses_source_specific_controls(self):
        guide = (ROOT / "USER_GUIDE.md").read_text(encoding="utf-8")
        self.assertIn("Lakehouse tables do not have the semantic-model synonym editor", guide)
        self.assertIn("Data agent instructions", guide)
        self.assertIn("add `matter` and `matters` as synonyms for the `Cases` table", guide)
        self.assertNotIn("add one relevant synonym rather than changing", guide)

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


if __name__ == "__main__":
    unittest.main()
