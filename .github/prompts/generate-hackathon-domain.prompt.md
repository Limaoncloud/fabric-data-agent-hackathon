---
name: "Generate Hackathon Domain"
description: "Create a complete, validated Fabric Data Agent hackathon for a new industry through a JSON-free guided interview. Use when a CSA wants reusable data, models, routing, guides, questions, and answers in under one hour."
argument-hint: "Describe the industry, audience, scenario, and important KPIs in plain English"
agent: "agent"
---

Follow [the JSON-free reuse workflow](../../REUSE_FOR_NEW_INDUSTRY.md) and adapt the existing UK legal implementation as a structural reference. Do not perform vocabulary-only replacement; model the new industry's actual grains, relationships, terminology, KPIs, routing needs, and safety boundaries.

The user is a CSA. Give them a JSON-free experience: never ask them to create, open, or edit JSON. Accept an initial plain-English description such as:

```text
Create this hackathon for water utilities. The audience is operations managers.
Focus on customers, water assets, leakage incidents, repair work, inspections,
service interruptions, and operational performance. Important measures include
open incidents, leakage volume, repair duration, repeat incidents, and work
completed on time. Use synthetic UK data and do not give safety-critical advice.
```

## Intake

Infer conventional, low-risk implementation details from the user's description and the existing UK legal package. Ask questions only when an answer is required to define a business grain, relationship, governed KPI, privacy rule, or safety boundary. Ask at most four concise questions in one turn.

If the description is sufficient, do not ask questions merely to seek confirmation. Create a short plain-English domain contract containing:

- domain name, ID, audience, scenario, culture, and currency;
- core entities, one-row grains, and stable synthetic keys;
- relationships and intended cardinalities;
- 5-10 governed KPIs with unambiguous definitions;
- synonyms and ambiguous terminology;
- standard semantic-model questions and derived-routing scenarios;
- synthetic-data, privacy, security, regulatory, and safety boundaries;
- assumptions that require later domain-expert review.

Proceed immediately using that contract. Do not require a separate approval turn unless an unresolved assumption would make generated data, KPI answers, or safety wording materially wrong.

## Internal Generation

Create `config/domain-briefs/<domain-id>.json` internally from the approved or sufficiently specified plain-English contract. Validate it, then use `deployment/create_domain_package.py` as an internal generation contract. JSON is an implementation artifact, not a CSA input.

Generate and validate all of these outputs:

1. The complete validated domain profile under `config/domains/`.
2. Deterministic synthetic base and derived-routing generators plus CSV files.
3. The optimized semantic-model reference, ontology definition, and Data Agent routing configuration.
4. `guides/<domain-id>/USER_GUIDE.md`, adapted to the domain while preserving the six-step participant journey.
5. `guides/<domain-id>/FACILITATOR_GUIDE.md`, including setup, checkpoints, escalating hints, expected source/measure, complete answer key, and debrief prompts. Make it facilitator-ready: provide exact Prep for AI settings, semantic-model AI instructions, Data Agent instructions, per-source descriptions and instructions, validated Lakehouse example queries, Verified Answers setup, test prompts, expected results, and checkpoints for every tuning step.
6. Core challenge and routing evaluation JSON, with every expected answer calculated from the generated CSVs rather than invented.
7. Focused tests for schemas, CSV headers, foreign keys, deterministic generation, expected answers, guide links, and package completeness.

Keep shared deployment notebooks and Python deployment code unchanged unless the generated package exposes a real compatibility defect. Do not overwrite another domain package. Do not deploy to Fabric.

Preserve the learning controls in the generated guides and configuration:

- Leave Data Agent instructions and example queries empty for the first baseline run.
- For Lakehouse sources, use source descriptions, Data Agent instructions, and validated SQL examples; do not describe this as adding table synonyms.
- Prefer the semantic model for governed business measures and prepared Lakehouse tables for specialist routing questions.
- Keep expected answers deterministic and calculate them from the generated data rather than inventing them.
- Use one fixed challenge question set for the initial agent, Prep for AI, Lakehouse attached, Lakehouse tuned, and final standard snapshots. Keep routing questions in a separate routing snapshot and ontology qualitative unless a dedicated ontology dataset is generated.
- Require the SDK evaluation workflow to calculate accuracy percentage per snapshot and produce a question-by-step comparison. Explain improvements and regressions from the measured results; never fabricate a monotonic accuracy increase.

## One-Hour Constraint

Optimize for a complete usable package in under one hour of CSA time:

- use the existing architecture and templates;
- generate 5 core entities unless the scenario requires more;
- generate 6 scored questions and 3 routing questions;
- prefer deterministic, modest-size synthetic datasets;
- do not stop after a plan or partial scaffold;
- run focused tests, then `python -m unittest discover -s tests -v`;
- fix failures in generated files before reporting completion.

## Completion Report

Report:

- the plain-English domain contract and review assumptions;
- every generated file grouped by data, model, agent, evaluation, and guides;
- all questions with their calculated answers and expected source or measure;
- the staged evaluation plan and expected accuracy-percentage comparison output;
- tests run and results;
- the exact `DOMAIN_PROFILE="<domain-id>"` notebook setting;
- the next manual step: run `NB_Deploy_Data_Agent_Hackathon.ipynb` in Fabric.

Do not claim completion if a required guide, question, calculated answer, or test is missing.