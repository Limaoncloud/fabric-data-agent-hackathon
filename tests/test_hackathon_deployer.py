import json
import re
import unittest
from pathlib import Path

from deployment.hackathon_deployer import (
    decode_definition_parts,
    definition_payload,
    load_json,
    render_copilot_parts,
    render_copilot_schema,
    render_ontology_parts,
    render_semantic_model_parts,
    validate_profile,
)

ROOT = Path(__file__).resolve().parents[1]
PROFILE = load_json(ROOT / "config" / "domains" / "uk-legal.json")
WORKSPACE_ID = "11111111-1111-1111-1111-111111111111"
LAKEHOUSE_ID = "22222222-2222-2222-2222-222222222222"


class ProfileTests(unittest.TestCase):
    def test_profile_cross_references_and_csv_headers(self):
        validate_profile(PROFILE, ROOT)


class SemanticModelTests(unittest.TestCase):
    def test_model_parts_and_base64_round_trip(self):
        basic = render_semantic_model_parts(PROFILE, "basic", WORKSPACE_ID, LAKEHOUSE_ID)
        optimized = render_semantic_model_parts(PROFILE, "optimized", WORKSPACE_ID, LAKEHOUSE_ID)

        self.assertEqual(5, sum(path.startswith("definition/tables/") for path in basic))
        self.assertEqual(5, sum(path.startswith("definition/tables/") for path in optimized))
        self.assertNotIn("definition/relationships.tmdl", basic)
        self.assertIn("definition/relationships.tmdl", optimized)
        self.assertEqual(basic, decode_definition_parts(definition_payload(basic, "TMDL")))
        self.assertEqual(optimized, decode_definition_parts(definition_payload(optimized, "TMDL")))

        for model_key, parts in (("basic", basic), ("optimized", optimized)):
            declarations = "\n".join(parts.values())
            for measure in PROFILE["semanticModels"][model_key]["measures"]:
                escaped_name = re.escape(measure["name"])
                pattern = rf"^\s*measure\s+(?:'{escaped_name}'|{escaped_name})\s*="
                self.assertEqual(1, len(re.findall(pattern, declarations, re.MULTILINE)), measure["name"])

    def test_copilot_parts_and_lineage_schema(self):
        parts = render_copilot_parts(PROFILE)
        self.assertIn("Copilot/Instructions/instructions.md", parts)
        self.assertIn("Copilot/settings.json", parts)
        self.assertIn("Copilot/examplePrompts.json", parts)
        json.loads(parts["Copilot/settings.json"])
        json.loads(parts["Copilot/examplePrompts.json"])

        optimized = render_semantic_model_parts(PROFILE, "optimized", WORKSPACE_ID, LAKEHOUSE_ID)
        tagged = {}
        tag_number = 1
        for path, content in optimized.items():
            if not path.startswith("definition/tables/"):
                tagged[path] = content
                continue
            output = []
            for line in content.splitlines():
                output.append(line)
                if re.match(r"^\s*(table|column|measure)\s+", line):
                    output.append(f"\tlineageTag: 00000000-0000-0000-0000-{tag_number:012d}")
                    tag_number += 1
            tagged[path] = "\n".join(output) + "\n"
        schema = json.loads(render_copilot_schema(PROFILE, tagged))
        self.assertEqual(5, len(schema["tables"]))
        self.assertTrue(all(table["id"] for table in schema["tables"]))


class OntologyTests(unittest.TestCase):
    def test_ontology_parts_are_deterministic_and_valid(self):
        first = render_ontology_parts(PROFILE, WORKSPACE_ID, LAKEHOUSE_ID)
        second = render_ontology_parts(PROFILE, WORKSPACE_ID, LAKEHOUSE_ID)
        self.assertEqual(first, second)
        self.assertEqual(3, sum(bool(re.fullmatch(r"EntityTypes/[^/]+/definition.json", path)) for path in first))
        self.assertEqual(3, sum("/DataBindings/" in path for path in first))
        self.assertEqual(2, sum(bool(re.fullmatch(r"RelationshipTypes/[^/]+/definition.json", path)) for path in first))
        self.assertEqual(2, sum("/Contextualizations/" in path for path in first))
        self.assertFalse(any("\\" in path for path in first))
        for path, content in first.items():
            if path == ".platform" or path.endswith(".json"):
                json.loads(content)


if __name__ == "__main__":
    unittest.main()
