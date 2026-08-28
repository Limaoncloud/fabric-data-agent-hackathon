---
name: fabric-data-agent-hackathon
description: "Build and deploy a reusable Microsoft Fabric Data Agent hackathon from a domain profile. Use when asked to create a Customer 360 demo, provision the Lakehouse and Direct Lake semantic models from a Fabric notebook, adapt the six-step journey to Legal, Retail, Insurance, Healthcare, Banking, or Manufacturing, configure optional Ontology/Data Agent assets, or generate a new domain package without PBIP/PBIX files."
argument-hint: "Describe the target domain and whether Ontology or Data Agent preview deployment is required"
---

# Fabric Data Agent Hackathon Playbook Skill

Companion quickstart:
- See SKILL_QUICKSTART_30MIN.md for a fast event setup path.

## Purpose
Use this skill to reproduce a complete Microsoft Fabric Data Agent hackathon demo for a Customer 360 scenario, with measurable quality improvements from a cleaned baseline to multi-source routed answers.

Default scenario:
- UK legal firm Customer 360 (can be replaced with any industry profile)

This skill captures the exact workflow used in this project and is designed for repeatable event delivery.

## When To Use
Use this skill when the user asks to:
- Build a Customer 360 Fabric Data Agent hackathon demo
- Create a multi-step maturity journey (raw data to optimized agent)
- Demonstrate semantic model and ontology impact on answer quality
- Demonstrate multi-source routing best practices
- Package demo assets for deployment and reuse

Trigger phrases:
- "build a Fabric data agent hackathon"
- "create Customer 360 demo"
- "set up six-step data agent journey"
- "show semantic model improvement"
- "show data source routing improvements"

## How To Use This Skill

### Operator flow
1. Confirm target industry (or keep UK legal default).
2. Create or validate `config/domains/<domain>.json` against `config/domain-profile.schema.json`.
3. Run `NB_Deploy_Data_Agent_Hackathon.ipynb` in the target Fabric workspace.
4. Reuse the same evaluation prompts across all steps.
5. Publish final outputs and share deployment/user guides.

### Notebook-first deployment
- Default `WORKSPACE_ID=""` so the notebook deploys to its current workspace.
- Default `DOMAIN_PROFILE="uk-legal"`.
- Generate Direct Lake semantic models as TMDL in memory; do not create PBIP, PBIX, BIM, or report-template artifacts.
- Keep Ontology and Data Agent SDK stages feature-gated because they are preview-dependent.
- Treat Verified Answers as a manual live-authoring step because they require saved report visuals.
- Use a release tag or commit SHA for `REPOSITORY_REF` during an event.

### Direct invocation prompts
Use one of these prompts in Copilot Chat:
- "Use the Fabric Data Agent Hackathon Playbook skill and run the six-step setup for UK legal Customer 360."
- "Use the Fabric Data Agent Hackathon Playbook skill for Retail industry and generate the full artifact plan."
- "Use the hackathon playbook skill and adapt entity names to Insurance while keeping the same six-step evaluation flow."

### Required inputs to provide early
- Industry name and domain vocabulary
- Demo duration (15-minute showcase or longer workshop)
- Whether to use prepared repo assets or generate new data
- Whether the optional ontology phase is mandatory or optional

### New-domain procedure
1. Create or review `config/domain-briefs/<domain>.json`. Use `python deployment/create_domain_package.py --domain <domain> --init --display-name "<name>"` for a new brief.
2. Render the complete generation contract with `python deployment/create_domain_package.py --domain <domain>` or run `/Generate Hackathon Domain <domain>` in VS Code Chat.
3. Inspect source files or the proposed synthetic schema; do not invent unreviewed columns, keys, KPIs, privacy rules, or safety rules.
4. Create `config/domains/<domain>.json` from `config/domain-profile.schema.json`, using domain-specific grains, relationships, DAX, descriptions, AI scope, routing, and evaluation intent.
5. Add or map source data for every `tables[].sourcePath` and make profile columns exactly match source headers.
6. Calculate evaluation expected answers from the generated data and add focused domain tests.
7. Run `python -m unittest discover -s tests -v` when the new package is committed.
8. Set `DOMAIN_PROFILE` in `NB_Deploy_Data_Agent_Hackathon.ipynb` and keep `WORKSPACE_ID=""` unless deploying elsewhere.
9. Run the stable core first. Enable Ontology and Data Agent only after reviewing their generated scope.

Network Rail example:
- Brief: `config/domain-briefs/network-rail.json`
- Command: `python deployment/create_domain_package.py --domain network-rail`
- CSA runbook: `REUSE_FOR_NEW_INDUSTRY.md`

Do not implement a new domain as vocabulary-only search and replace. Different domains require their own table grains, relationships, metric definitions, sample distributions, and routing examples.

### Minimum completion bar
- Every artifact-typed folder (`sample-data/`, `semantic-model/`, `ontology/`, `agent-configuration/`, `evaluation/`) has corresponding content for the domain
- The routing phase has physical derived tables plus routing configuration
- Evaluation results exist for each completed phase

## When Not To Use
Do not use this skill for:
- Single-table quick demos
- Non-Fabric analytics platforms
- Report-only visualization tasks without a Data Agent

## Demo Objective
Deliver a progressive demonstration that shows answer-quality uplift across six phases:
- Data readiness: load the domain's base tables into the Lakehouse
- Semantic model readiness: build the Data Agent on the Optimized semantic model and tune it with Prep for AI
- Agent configuration: attach the Lakehouse to the same agent as a second source
- Lakehouse source tuning: apply Data Agent best practices to the Lakehouse source
- Routing with derived data: add derived Lakehouse marts and configure multi-source routing
- Optional ontology: add an ontology layer for cross-entity reasoning

USER_GUIDE.md implements this journey as six numbered workshop steps for one continuously-extended Data Agent; this skill describes it as reusable phases so it applies to any domain.

## Industry Flexibility (Required)
Treat industry as a configurable input.

Define a complete domain profile before execution. It must include:
- Domain identity, culture, and currency
- Source files, exact columns, data types, and physical Lakehouse table names
- Business-facing semantic-model table and column names
- Relationships, measures, formats, and descriptions
- AI schema, AI instructions, and Verified Answer candidates
- Optional Ontology entities and relationships
- Data Agent sources, object scope, descriptions, instructions, and examples

Design rule:
- Keep the six-step methodology unchanged.
- Swap domain language, sample data labels, prompt phrasing, and KPI definitions via `INDUSTRY_PROFILE`.

## Expected Repository Structure
Use artifact-typed folders keyed by domain ID, not numbered step folders. Numbering belongs only in USER_GUIDE.md-style prose:

```text
sample-data/uk-legal/base/
sample-data/uk-legal/derived-routing/
semantic-model/basic-reference/uk-legal/
semantic-model/optimized/uk-legal/
ontology/uk-legal/
agent-configuration/routing/uk-legal/
evaluation/challenge/
evaluation/routing/
evaluation/legacy/
```

Key files used in this demo:
- NB_Deploy_Data_Agent_Hackathon.ipynb
- config/domain-profile.schema.json
- config/domains/uk-legal.json
- deployment/hackathon_deployer.py
- sample-data/uk-legal/base/customers.csv
- sample-data/uk-legal/base/cases.csv
- sample-data/uk-legal/base/solicitors.csv
- sample-data/uk-legal/base/transactions.csv
- sample-data/uk-legal/base/interactions.csv
- semantic-model/basic-reference/uk-legal/README.md
- semantic-model/optimized/uk-legal/README.md
- ontology/uk-legal/ontology-definition.json
- agent-configuration/routing/uk-legal/data-agent-configuration.json
- sample-data/uk-legal/derived-routing/generate_derived_routing_data.py
- sample-data/uk-legal/derived-routing/client_engagement_summary.csv
- sample-data/uk-legal/derived-routing/case_finance_insights.csv
- sample-data/uk-legal/derived-routing/solicitor_performance_mart.csv
- evaluation/evaluate_agent.py
- evaluation/challenge/uk-legal.json
- evaluation/routing/uk-legal.json
- evaluation/legacy/uk-legal.json
- evaluation/legacy/TEST_QUERIES.md
- USER_GUIDE.md

## Authoring Workflow

### Phase 1 - Data Readiness
Actions:
- Load the domain's base CSVs into the Lakehouse as managed Delta tables, either via the deployment notebook or manual upload in the Fabric web UI.
- Confirm every profile-declared table and row count before any agent work begins.

Minimum data domains:
- Customer entity table
- Service/workflow entity table
- Staff/owner entity table
- Financial events table
- Engagement/interactions table

### Phase 2 - Semantic Model Readiness
Actions:
- Build one Data Agent on the domain's Optimized Direct Lake semantic model. Keep extending this same agent in later phases; do not create a second agent.
- Leave Data Agent instructions and example queries empty for the first baseline run.
- Run baseline prompts, including at least one deliberately ambiguous and one deliberately undefined question.
- Configure Prep for AI (AI Data Schema selection, synonyms, AI instructions), add a Data Agent instruction, and create one Verified Answer from a saved report visual.
- Retest and record which change affected which question.

Optional manual comparison: build the anti-pattern model from `semantic-model/basic-reference/<domain>/README.md`. The deployment notebook does not create this model.

### Phase 3 - Agent Configuration
Actions:
- Attach the Lakehouse to the same agent as a second source and select only the base tables.
- Leave the new source's description and examples empty for now; run the same baseline prompts to observe two-source ambiguity before tuning.

### Phase 4 - Lakehouse Source Tuning
Actions:
- Add a clear source description, a Data Agent instruction distinguishing the Lakehouse from the semantic model, and a validated SQL example query pair.
- For Lakehouse sources, teach terminology through source descriptions and Data Agent instructions; do not describe this as adding table synonyms.
- Re-run the same prompts and confirm the agent reliably prefers the semantic model for standard questions.

### Phase 5 - Routing With Derived Data
Actions:
- Generate derived routing datasets using `sample-data/<domain>/derived-routing/generate_derived_routing_data.py`.
- Add the derived tables to the same Lakehouse source, write descriptions and SQL examples, and extend the Data Agent instruction to cover all three areas (semantic model, base tables, derived tables).
- Apply routing best practices and retest.

Required routing sequence:
1. Tighten schema scope per source
2. Add concise source descriptions
3. Add validated example query pairs for Lakehouse, Warehouse, or KQL sources; do not add them to Power BI semantic-model sources
4. Add short topic-based routing rules

References:
- https://learn.microsoft.com/en-us/fabric/data-science/data-agent-routing

### Phase 6 - Optional Ontology
Actions:
- Introduce ontology entities and relationships for cross-domain reasoning.
- Map core business entities from `INDUSTRY_PROFILE`.
- Re-run relationship-heavy prompts.

## Routing Best Practices (Mandatory)
- Keep each source narrowly scoped to one topic area.
- Avoid overlapping descriptions that create source ambiguity.
- Include representative examples that are clearly source-specific.
- Encode explicit routing hints for finance, customer/service, engagement, and cross-domain questions.
- Validate orchestration outcomes and iteratively refine schema/description/examples/rules.

## Evaluation Pattern
Use the same test prompts across all six phases so quality movement is attributable.

Recommended assets:
- evaluation/challenge/uk-legal.json
- evaluation/routing/uk-legal.json
- evaluation/evaluate_agent.py
- evaluation/results/step1-results.json ... evaluation/results/step6-results.json

Evaluation dimensions:
- Exact Match
- Semantic Match
- Routing Accuracy
- Error Rate

## Standard Prompt Set
Use these representative prompts and adapt entity names from `INDUSTRY_PROFILE`:
- "How many active customers do we have?"
- "How many open [service entities] do we have?"
- "What is total [service value metric]?"
- "How many unpaid invoices?"
- "Which [staff entity] handles most [service entities]?"
- "How many [interaction events] happened in Q1?"
- "Which high-value open [service entities] also have overdue invoices?"
- "Which [staff entity plural] are in top performance tier?"

UK legal default prompt examples:
- "How many open cases do we have?"
- "Which solicitor handles most cases?"
- "How many client meetings happened in Q1?"

## Deployment Expectations
- Use the root deployment notebook for Lakehouse load, model publish, optional agent wiring, and verification.
- Validate the profile against source headers before any Fabric write.
- Ensure all paths and instructions reflect the artifact-typed folder structure.
- Include reproducible commands where practical.

## Packaging Rules For Future Events
- Keep only multi-table artifacts for final event package.
- Remove legacy single-table assets.
- Group outputs by artifact type (`sample-data/`, `semantic-model/`, `ontology/`, `agent-configuration/`, `evaluation/`), not step folders.
- Keep user-facing guide concise and practical.
- Keep reusable domain profiles under `config/domains/` and generated deployment logic under `deployment/`.
- Do not commit generated PBIP, PBIX, BIM, or report-template artifacts.

## Success Criteria
- A participant can run the walkthrough end-to-end without hidden dependencies.
- Phase-by-phase quality improvements are demonstrable.
- The routing phase clearly shows better multi-source routing behavior.
- Repo is ready to publish and share publicly.

## Reusable Deliverables Checklist
- Multi-table raw CSV package
- Multi-table cleaned CSV package
- Validated domain profile
- Notebook-generated Optimized Direct Lake semantic model
- Ontology definition
- Multi-source routing configuration
- Derived-routing data generator and outputs
- User guide
- Deployment guide
- Evaluation script, dataset, and per-step results

Industry adaptation add-ons:
- One short `INDUSTRY_PROFILE` document in the repo root
- 10 to 20 industry-specific test prompts mapped to the same evaluation intent categories

## Suggested 15-Minute Demo Script
1. Show data-readiness baseline errors and ambiguity
2. Show semantic-model-readiness stabilization from Prep for AI
3. Show agent-configuration structural gains from attaching the Lakehouse
4. Show Lakehouse-source-tuning before/after results
5. Show routing-with-derived-data orchestrator improvements across sources
6. Show optional-ontology relationship reasoning

## Notes For Skill Operators
- If a user asks for scale-up, increase row counts but preserve table relationships.
- If a user asks for realism, expand finance and engagement behavior before tuning prompts.
- If a user asks for event readiness, prioritize deployment reproducibility and clear documentation over additional model complexity.
- If a user changes industry, keep table roles and evaluation structure constant, and only swap domain lexicon, KPIs, and example prompts.

