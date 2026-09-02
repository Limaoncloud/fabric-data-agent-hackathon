# Reuse This Hackathon Without Editing JSON

A CSA supplies one plain-English prompt. Copilot creates the internal JSON contracts, synthetic data, model configuration, routing assets, participant/facilitator guides, evaluation questions, calculated answers, and tests.

The target is less than one hour of CSA time for a complete local package. Fabric deployment time is separate because workspace capacity and item provisioning times vary.

## Before You Start

1. Open this repository in VS Code on the `dev` branch or a release tag.
2. Confirm GitHub Copilot Chat is available in Agent mode.
3. Start from a clean working tree so generated files are easy to review.
4. Have a domain expert available only if KPI or safety definitions are genuinely unclear.

You do not need to open `config/`, understand the profile schema, write Python, or edit JSON.

## One-Hour Workflow

| Time | CSA action | Copilot action |
| --- | --- | --- |
| 0-5 min | Describe the industry, audience, scenario, KPIs, and boundaries | Build a plain-English domain contract |
| 5-10 min | Answer up to four blocking questions, if needed | Resolve grains, relationships, KPI definitions, and safety constraints |
| 10-40 min | Wait while the agent works | Generate data, model, routing, ontology, guides, questions, answers, and tests |
| 40-50 min | Review assumptions and question/answer summary | Fix generated-package test failures |
| 50-60 min | Check the acceptance list and commit the package | Report the deployment setting and next step |

### Step 1: Invoke The Workspace Prompt

In VS Code Chat, type `/` and select **Generate Hackathon Domain**. Put your complete plain-English request in the same message.

Do not create a domain brief first. The workspace prompt creates and validates it internally.

### Step 2: Answer Only Blocking Questions

Copilot may ask up to four concise questions when it cannot safely infer a grain, relationship, KPI definition, privacy rule, or safety boundary. Answer in business language.

Examples:

- "One incident can affect several assets, but each repair work order belongs to one incident."
- "On-time means completed on or before the promised completion date."
- "Use synthetic UK data and do not generate customer names, addresses, or real asset locations."

If the opening prompt is sufficiently specific, Copilot should proceed without another approval turn.

### Step 3: Let Copilot Generate The Complete Package

Copilot creates the internal brief and then generates:

- `config/domains/<domain>.json` and the internal brief used to produce it;
- deterministic base and derived-routing data generators plus CSVs;
- semantic-model measures, relationships, descriptions, and Prep for AI reference;
- ontology and Data Agent source/routing configuration;
- `guides/<domain>/USER_GUIDE.md` with the six-step participant journey;
- `guides/<domain>/FACILITATOR_GUIDE.md` with setup, checkpoints, hints, and the complete answer key;
- six scored challenge questions and three routing questions;
- expected answers calculated from the generated CSVs, with expected source or measure;
- focused package tests followed by the full repository test suite.

Copilot must not stop after creating a plan or empty scaffold and must not deploy to Fabric.

### Step 4: Review The Completion Report

The final response must show:

1. The plain-English domain contract and assumptions needing expert review.
2. Every generated file grouped by data, model, agent, evaluation, and guides.
3. All nine questions, calculated answers, and expected source or measure.
4. Focused and full test results.
5. The exact `DOMAIN_PROFILE="<domain>"` value.
6. The next step for deploying with `NB_Deploy_Data_Agent_Hackathon.ipynb`.

### Step 5: Apply The Acceptance Checklist

- [ ] No existing domain package was overwritten.
- [ ] Participant and facilitator guides use the new domain vocabulary throughout.
- [ ] Every table has a clear one-row grain and stable synthetic key.
- [ ] Every KPI has an unambiguous business definition.
- [ ] Evaluation answers were calculated from generated data, not manually invented.
- [ ] Standard questions route to the semantic model and specialist questions route to prepared Lakehouse tables.
- [ ] Safety, privacy, and regulatory boundaries appear in the agent guidance.
- [ ] Focused tests and the full repository suite pass.
- [ ] The completion report provides the exact deployment profile value.

## Copy-Paste Example: Water Utilities

Invoke **Generate Hackathon Domain** with this message:

```text
Create a complete reusable Fabric Data Agent hackathon for Water Utilities
Operations. I am a CSA and do not want to create or edit JSON.

Audience: regional operations managers and service-performance analysts in a UK
water company.

Scenario: help the audience understand customers, water assets, leakage incidents,
repair work orders, inspections, service interruptions, and operational performance.

Use five core entities where practical: Customers, Assets, Incidents, Work Orders,
and Inspections. Infer sensible one-row grains, synthetic keys, and relationships.
An incident can affect one primary asset. A work order belongs to one incident, and
an inspection belongs to one asset.

Governed KPIs:
- Open incidents: incidents whose status is Open or Investigating.
- Total estimated leakage: sum of estimated leakage volume for active incidents.
- Average repair duration: average hours from work started to work completed for
	completed work orders only.
- Repeat incidents: incidents on an asset that had another incident in the prior
	30 days.
- Work completed on time: percentage of completed work orders finished on or before
	the promised completion timestamp.
- Assets requiring attention: active assets with either an open high-severity
	incident or a failed latest inspection.

Terminology: customer and account holder are synonyms; incident, event, and issue
may be used interchangeably; repair and work order are related but not synonyms.
High severity means severity Critical or High.

Create deterministic synthetic UK data only. Do not use real customer identities,
addresses, precise infrastructure locations, credentials, or vulnerability details.
The agent may summarize demonstration data but must not direct safety-critical field
operations or claim regulatory compliance.

Generate everything: the deployable domain profile, base and derived data, semantic
model reference, ontology, routing configuration, domain-specific participant guide,
facilitator guide with hints and complete answer key, six scored questions, three
routing questions, calculated expected answers and expected sources/measures, and
focused tests. Run the full test suite, fix generated-package failures, do not deploy
to Fabric, and finish with the exact DOMAIN_PROFILE value and a grouped file list.
```

This prompt is deliberately detailed enough that Copilot should normally proceed without clarification. The resulting values depend on the generated deterministic data, so the completion report must show the calculated answers rather than copying example numbers.

## Expected Outcome

After the example completes, you should have a self-contained `water-utilities` package alongside `uk-legal`. Set:

```python
DOMAIN_PROFILE = "water-utilities"
```

in `NB_Deploy_Data_Agent_Hackathon.ipynb`, keep preview deployment flags disabled for the first run, and deploy the stable Lakehouse and semantic-model core.

## Review Gate

Generation is not domain approval. Before a real event, a qualified reviewer must confirm grains, keys, KPI definitions, synthetic distributions, agent scope, evaluation questions, answer keys, and safety wording. Generated records and recommendations must never be represented as live operational data or safety instructions.