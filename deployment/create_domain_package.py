"""Create a reusable domain brief and Copilot generation prompt."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BRIEFS_DIR = ROOT / "config" / "domain-briefs"


def _domain_id(value: str) -> str:
    if not re.fullmatch(r"[a-z][a-z0-9-]+", value):
        raise argparse.ArgumentTypeError(
            "domain must start with a lowercase letter and contain only lowercase letters, numbers, and hyphens"
        )
    return value


def starter_brief(domain_id: str, display_name: str) -> dict[str, Any]:
    return {
        "domain": {
            "id": domain_id,
            "displayName": display_name,
            "description": "REPLACE: concise business scenario and intended decisions.",
            "culture": "en-GB",
            "currency": "GBP",
        },
        "audience": ["REPLACE: primary user persona"],
        "entities": [
            {
                "name": "REPLACE: business entity",
                "grain": "REPLACE: what one row represents",
                "key": "REPLACE: stable key",
            }
        ],
        "relationships": ["REPLACE: Entity A relates to Entity B through key"],
        "metrics": [
            {
                "name": "REPLACE: KPI name",
                "definition": "REPLACE: unambiguous business definition",
            }
        ],
        "terminology": {"REPLACE: user phrase": "REPLACE: governed meaning"},
        "dataRules": ["Use synthetic data only; do not include personal or operationally sensitive data."],
        "safetyRules": ["Answers are for demonstration and must not direct safety-critical operations."],
    }


def validate_brief(brief: dict[str, Any]) -> None:
    errors: list[str] = []
    domain = brief.get("domain", {})
    for field in ("id", "displayName", "description", "culture", "currency"):
        if not domain.get(field):
            errors.append(f"domain.{field} is required")
    for field in ("audience", "entities", "relationships", "metrics", "dataRules", "safetyRules"):
        if not brief.get(field):
            errors.append(f"{field} must contain at least one item")
    for index, entity in enumerate(brief.get("entities", [])):
        for field in ("name", "grain", "key"):
            if not entity.get(field):
                errors.append(f"entities[{index}].{field} is required")
    for index, metric in enumerate(brief.get("metrics", [])):
        for field in ("name", "definition"):
            if not metric.get(field):
                errors.append(f"metrics[{index}].{field} is required")
    if "REPLACE:" in json.dumps(brief):
        errors.append("replace all REPLACE: placeholders before generating a package")
    if errors:
        raise ValueError("Invalid domain brief:\n- " + "\n- ".join(errors))


def render_prompt(brief: dict[str, Any]) -> str:
    validate_brief(brief)
    domain_id = brief["domain"]["id"]
    display_name = brief["domain"]["displayName"]
    brief_json = json.dumps(brief, indent=2, ensure_ascii=True)
    return f"""# Generate the {display_name} Hackathon Domain

Use the workspace skill at `skills/fabric-data-agent-hackathon/SKILL.md` and adapt this repository for the domain brief below. Work from the existing UK legal implementation as a structural reference, but do not perform vocabulary-only replacement.

## Domain brief

```json
{brief_json}
```

## Required outputs

Create and validate all of the following:

1. `config/domains/{domain_id}.json`, conforming to `config/domain-profile.schema.json`.
2. `domains/{domain_id}/step1/generate_step1_data.py` and deterministic synthetic CSVs for all core entities.
3. `domains/{domain_id}/step5/ontology_definition.json` with domain entities and relationships.
4. `domains/{domain_id}/step6/generate_step6_data.py`, derived CSV marts, and `data_agent_configuration.json`.
5. `domains/{domain_id}/evaluation/evaluation_dataset.json` with expected answers calculated from the generated data.
6. `domains/{domain_id}/evaluation/TEST_QUERIES.md` with lookup, aggregation, ranking, relationship, routing, ambiguity, and out-of-scope questions.
7. `domains/{domain_id}/README.md` containing generation, validation, notebook deployment, and review instructions.
8. Focused tests that validate the profile, exact CSV headers, foreign keys, deterministic generation, and evaluation expected values.

## Implementation rules

- Preserve the repository's six-step learning journey and notebook-first deployment.
- Model the actual entity grains, keys, relationships, terminology, and KPI definitions in the brief.
- Use synthetic data only. Do not imply that generated records represent live operational data.
- Keep safety-critical, security-sensitive, personal, and infrastructure-vulnerability details out of generated data.
- Treat operational and safety conclusions as demonstration-only; include the brief's safety rules in agent instructions.
- Make basic-model ambiguity intentional and teaching-focused; make optimized measures explicit and governed.
- Keep all domain-owned files under `domains/{domain_id}/`, except the profile under `config/domains/`.
- Do not edit or overwrite the UK legal package.
- Do not deploy to Fabric. Generate locally, run focused tests, then run `python -m unittest discover -s tests -v`.
- Stop and list assumptions requiring a domain expert if a grain, key, KPI, relationship, or safety rule is underspecified.

## Completion report

Report the files created, tests run, assumptions made, and the exact `DOMAIN_PROFILE=\"{domain_id}\"` notebook setting for deployment.
"""


def _write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def _display_path(path: Path) -> Path:
    try:
        return path.relative_to(ROOT)
    except ValueError:
        return path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Initialize a domain brief or render its full-package Copilot prompt."
    )
    parser.add_argument("--domain", required=True, type=_domain_id, help="Domain ID, for example network-rail")
    parser.add_argument("--init", action="store_true", help="Create a starter brief instead of rendering a prompt")
    parser.add_argument("--display-name", help="Display name required with --init")
    parser.add_argument("--output", type=Path, help="Prompt output path; stdout is used when omitted")
    parser.add_argument("--force", action="store_true", help="Replace an existing initialized brief or prompt")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    brief_path = BRIEFS_DIR / f"{args.domain}.json"
    if args.init:
        if not args.display_name:
            raise SystemExit("--display-name is required with --init")
        if brief_path.exists() and not args.force:
            raise SystemExit(f"Brief already exists: {brief_path.relative_to(ROOT)} (use --force to replace it)")
        _write_json(brief_path, starter_brief(args.domain, args.display_name))
        print(f"Created {brief_path.relative_to(ROOT)}")
        return 0

    if not brief_path.is_file():
        raise SystemExit(
            f"Brief not found: {brief_path.relative_to(ROOT)}. "
            f"Run with --init --display-name \"Your Domain\" first."
        )
    brief = json.loads(brief_path.read_text(encoding="utf-8"))
    prompt = render_prompt(brief)
    if args.output:
        output_path = args.output if args.output.is_absolute() else ROOT / args.output
        if output_path.exists() and not args.force:
            raise SystemExit(f"Output already exists: {output_path} (use --force to replace it)")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(prompt, encoding="utf-8")
        print(f"Created {_display_path(output_path)}")
    else:
        print(prompt, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())