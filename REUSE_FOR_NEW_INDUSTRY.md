# Reuse This Hackathon Without Editing JSON

A CSA supplies one plain-English prompt. Copilot creates the internal JSON contracts, synthetic data, model configuration, routing assets, participant/facilitator guides, evaluation questions, calculated answers, and tests.

The target is less than one hour of CSA time for a complete local package. Fabric deployment time is separate because workspace capacity and item provisioning times vary.

## Step 1: Ask Copilot To Recreate It For Your Industry

In VS Code Chat, type `/`, select **Generate Hackathon Domain**, and ask Copilot to create the same level of detail for a different industry.

### Copy-Paste Example: Water Utilities

```text
Create the same complete reusable Fabric Data Agent hackathon for Water Utilities
Operations. I am a CSA and do not want to create or edit JSON.

Audience: UK water-company regional operations managers and service-performance
analysts. Cover customers, assets, leakage incidents, repair work orders,
inspections, service interruptions, and operational performance.

Use five core entities where practical: Customers, Assets, Incidents, Work Orders,
and Inspections. Infer sensible grains, synthetic keys, and relationships. Use
deterministic synthetic UK data only, with no real identities, addresses, precise
infrastructure locations, credentials, or vulnerability details. Do not direct
safety-critical operations or claim regulatory compliance.

Define governed KPIs for open incidents, active-incident leakage, completed-work
repair duration, repeat incidents within 30 days, work completed by its promised
timestamp, and active assets needing attention because of a high-severity incident
or failed latest inspection. Treat customer/account holder and incident/event/issue
as alternate terminology. Repair and work order are related but are not synonyms.

Generate the same complete package and six-step learning journey as the UK legal
example: deployable profile, base and derived data, semantic model, ontology,
routing configuration, participant guide, facilitator guide, evaluation datasets,
calculated answers, and focused tests.

Keep the facilitator guide very detailed and ready to run. Include the exact Prep for AI settings,
semantic-model AI instructions, Data Agent instructions, each data
source description and instruction, validated Lakehouse example queries,
Verified Answers setup, expected source or measure, test prompts, complete answers, hints,
and checkpoints for every tuning step.

Use the same challenge questions at every standard evaluation snapshot. Report
accuracy percentage for the initial agent, Prep for AI, Lakehouse attached,
Lakehouse tuned, and final standard evaluation, plus a separate routing result.
Show the question-by-step comparison so facilitators can see where accuracy improves
or regresses as tuning progresses; never invent an improvement the results do not
show. Keep ontology evaluation optional unless a separate ontology dataset exists.

Run focused tests and the full test suite, fix generated-package failures, do not
deploy to Fabric, and finish with the exact DOMAIN_PROFILE value, calculated answer
summary, staged evaluation plan, and grouped file list.
```

Copilot should normally proceed from this prompt without clarification. Calculated answers must come from the generated deterministic data, not from example values.

## Step 2: Or Start With A Short Brief

You can also work conversationally. Select **Generate Hackathon Domain** and provide only the industry, audience, scenario, important KPIs, and safety or privacy boundaries. For example:

```text
Create this hackathon for water utilities. The audience is operations managers.
Focus on assets, leakage incidents, repairs, inspections, service interruptions,
and operational performance. Use synthetic UK data and do not provide
safety-critical advice. Ask me concise questions where a business definition is
needed, then generate the complete package.
```

Copilot may ask up to four concise clarifying questions about grains, relationships, KPI definitions, privacy, or safety. Answer in business language; Copilot creates and validates the implementation files.

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

## What Copilot Generates

Copilot creates and validates:

- `config/domains/<domain>.json` and the internal brief used to produce it;
- deterministic base and derived-routing data generators plus CSVs;
- semantic-model measures, relationships, descriptions, and Prep for AI reference;
- ontology and Data Agent source/routing configuration;
- `guides/<domain>/USER_GUIDE.md` with the six-step participant journey;
- `guides/<domain>/FACILITATOR_GUIDE.md` with exact tuning settings, checkpoints, test prompts, hints, and the complete answer key;
- six scored challenge questions and three routing questions;
- expected answers calculated from the generated CSVs, with expected source or measure;
- staged SDK snapshots with accuracy percentage and a question-by-step comparison;
- focused package tests followed by the full repository test suite.

Copilot must not stop after creating a plan or empty scaffold and must not deploy to Fabric.

## Review The Result

The completion report must show:

1. The plain-English domain contract and assumptions needing expert review.
2. Every generated file grouped by data, model, agent, evaluation, and guides.
3. All nine questions, calculated answers, and expected source or measure.
4. Focused and full test results.
5. The exact `DOMAIN_PROFILE="<domain>"` value.
6. The next step for deploying with `NB_Deploy_Data_Agent_Hackathon.ipynb`.

- [ ] No existing domain package was overwritten.
- [ ] Participant and facilitator guides use the new domain vocabulary throughout.
- [ ] Every table has a clear one-row grain and stable synthetic key.
- [ ] Every KPI has an unambiguous business definition.
- [ ] Evaluation answers were calculated from generated data, not manually invented.
- [ ] The facilitator guide includes exact Prep for AI, agent, source, example-query, and Verified Answers guidance.
- [ ] Evaluation uses fixed challenge questions and reports measured accuracy percentage at every stage.
- [ ] Standard questions route to the semantic model and specialist questions route to prepared Lakehouse tables.
- [ ] Safety, privacy, and regulatory boundaries appear in the agent guidance.
- [ ] Focused tests and the full repository suite pass.
- [ ] The completion report provides the exact deployment profile value.

## Expected Outcome

After the example completes, you should have a self-contained `water-utilities` package alongside `uk-legal`. Set:

```python
DOMAIN_PROFILE = "water-utilities"
```

in `NB_Deploy_Data_Agent_Hackathon.ipynb`, keep preview deployment flags disabled for the first run, and deploy the stable Lakehouse and semantic-model core.

## Review Gate

Generation is not domain approval. Before a real event, a qualified reviewer must confirm grains, keys, KPI definitions, synthetic distributions, agent scope, evaluation questions, answer keys, and safety wording. Generated records and recommendations must never be represented as live operational data or safety instructions.