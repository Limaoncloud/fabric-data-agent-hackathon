import json
import unittest
from pathlib import Path

from deployment.create_domain_package import render_prompt, starter_brief, validate_brief

ROOT = Path(__file__).resolve().parents[1]
NETWORK_RAIL_BRIEF = json.loads(
    (ROOT / "config" / "domain-briefs" / "network-rail.json").read_text(encoding="utf-8")
)


class DomainPackageTests(unittest.TestCase):
    def test_workspace_prompt_is_json_free_and_complete(self):
        prompt = (
            ROOT / ".github" / "prompts" / "generate-hackathon-domain.prompt.md"
        ).read_text(encoding="utf-8")
        for expected in (
            "never ask them to create, open, or edit JSON",
            "guides/<domain-id>/USER_GUIDE.md",
            "guides/<domain-id>/FACILITATOR_GUIDE.md",
            "every expected answer calculated from the generated CSVs",
            "under one hour",
            'DOMAIN_PROFILE="<domain-id>"',
        ):
            self.assertIn(expected, prompt)
        self.assertNotIn("The user will provide a domain ID", prompt)
        self.assertNotIn("Read `config/domain-briefs/<domain-id>.json`", prompt)

    def test_network_rail_brief_is_valid_and_has_no_placeholders(self):
        validate_brief(NETWORK_RAIL_BRIEF)
        self.assertNotIn("REPLACE:", json.dumps(NETWORK_RAIL_BRIEF))
        self.assertEqual("network-rail", NETWORK_RAIL_BRIEF["domain"]["id"])

    def test_rendered_prompt_names_all_required_outputs_and_boundaries(self):
        prompt = render_prompt(NETWORK_RAIL_BRIEF)
        for expected in (
            "config/domains/network-rail.json",
            "sample-data/network-rail/base/generate_base_data.py",
            "sample-data/network-rail/derived-routing/generate_derived_routing_data.py",
            "ontology/network-rail/ontology-definition.json",
            "agent-configuration/routing/network-rail/data-agent-configuration.json",
            "evaluation/challenge/network-rail.json",
            "evaluation/routing/network-rail.json",
            "guides/network-rail/USER_GUIDE.md",
            "guides/network-rail/FACILITATOR_GUIDE.md",
            "synthetic data only",
            "Do not deploy to Fabric",
        ):
            self.assertIn(expected, prompt)

    def test_starter_brief_requires_csa_domain_decisions(self):
        brief = starter_brief("water-utilities", "Water Utilities Operations")
        self.assertEqual("water-utilities", brief["domain"]["id"])
        self.assertIn("REPLACE:", json.dumps(brief))
        with self.assertRaisesRegex(ValueError, "replace all REPLACE"):
            validate_brief(brief)


if __name__ == "__main__":
    unittest.main()