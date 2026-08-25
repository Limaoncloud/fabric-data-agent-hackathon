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
- Whether ontology (Step 5) is mandatory or optional

### New-domain procedure
1. Inspect the source files or existing Lakehouse schema; do not invent columns or keys.
2. Copy the structural contract from `config/domain-profile.schema.json`, not the legal values.
3. Create `config/domains/<domain>.json` with domain-specific grains, relationships, DAX, descriptions, AI scope, routing, and evaluation intent.
4. Add or map source data for every `tables[].sourcePath` and make profile columns exactly match source headers.
5. Run `python -m unittest discover -s tests -v` and add domain-specific profile tests when the new package is committed.
6. Set `DOMAIN_PROFILE` in `NB_Deploy_Data_Agent_Hackathon.ipynb` and keep `WORKSPACE_ID=""` unless deploying elsewhere.
7. Run the stable core first. Enable Ontology and Data Agent only after reviewing their generated scope.

Do not implement a new domain as vocabulary-only search and replace. Different domains require their own table grains, relationships, metric definitions, sample distributions, and routing examples.

### Minimum completion bar
- All step folders have corresponding artifacts
- Step 6 has physical derived tables plus routing configuration
- Evaluation results exist for each completed step

## When Not To Use
Do not use this skill for:
- Single-table quick demos
- Non-Fabric analytics platforms
- Report-only visualization tasks without a Data Agent

## Demo Objective
Deliver a progressive six-step demonstration that shows answer-quality uplift:
- Step 1: Raw multi-table data baseline
- Step 2: Cleaned multi-table data
- Step 3: Basic semantic model
- Step 4: Optimized semantic model with Prep for AI
- Step 5: Ontology layer
- Step 6: Multiple data sources with routing best practices

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
Use this folder structure:

```text
step1/
step3/
step4/
step5/
step6/
```

Key files used in this demo:
- NB_Deploy_Data_Agent_Hackathon.ipynb
- config/domain-profile.schema.json
- config/domains/uk-legal.json
- deployment/hackathon_deployer.py
- step1/step1_cleaned_customers.csv
- step1/step1_cleaned_cases.csv
- step1/step1_cleaned_solicitors.csv
- step1/step1_cleaned_transactions.csv
- step1/step1_cleaned_interactions.csv
- step3/README.md
- step4/README.md
- step5/step5_ontology_definition.json
- step6/step6_data_agent_configuration.json
- step6/generate_step6_data.py
- step6/step6_client_engagement_summary.csv
- step6/step6_case_finance_insights.csv
- step6/step6_solicitor_performance_mart.csv
- evaluation/evaluate_agent.py
- evaluation/evaluation_dataset.json
- evaluation/TEST_QUERIES.md
- USER_GUIDE.md

## Authoring Workflow

### Step 1 - Cleaned Multi-Table Baseline
Actions:
- Use the cleaned industry-specific Customer 360 baseline with hundreds or thousands of rows.
- Use multiple related tables, not a single denormalized table.
- Upload to Fabric Lakehouse and connect a Data Agent.
- Run baseline prompts and record initial quality.

Minimum data domains:
- Customer entity table
- Service/workflow entity table
- Staff/owner entity table
- Financial events table
- Engagement/interactions table

### Step 2 - Data Agent Configuration Best Practices
Actions:
- Keep Step 1 data unchanged.
- Tighten schema scope and table/column selection.
- Improve source descriptions, example queries, and agent instructions.
- Re-run the same prompts for like-for-like comparison.

### Step 3 - Basic Semantic Model
Actions:
- Generate the Basic Direct Lake semantic model from the selected domain profile.
- Keep relationships disabled and use intentionally ambiguous/duplicate measures for the teaching baseline.
- Publish and connect the Data Agent.
- Re-run test suite and log quality changes.

### Step 4 - Optimized Semantic Model
Actions:
- Generate the Optimized Direct Lake semantic model from the same profile.
- Apply a clear star schema, descriptions, formats, and unambiguous measures.
- Configure Prep for AI:
  - AI Data Schema
  - AI Instructions
- Configure Verified Answers manually from saved report visuals.
- Reconnect Data Agent and retest.

Guidance:
- Prefer users to attempt this themselves first.
- Use official Learn tooling guidance as needed.

References:
- https://learn.microsoft.com/en-us/fabric/data-science/semantic-model-best-practices#tools

### Step 5 - Ontology Layer
Actions:
- Introduce ontology entities and relationships for cross-domain reasoning.
- Map core business entities from `INDUSTRY_PROFILE`.
- Re-run relationship-heavy prompts.

### Step 6 - Multi-Source Routing
Actions:
- Add additional physical data sources (not config-only).
- Generate Step 6 derived datasets using step6/generate_step6_data.py.
- Upload Step 6 files and register multiple agent sources.
- Apply routing best practices and retest.

Required Step 6 routing sequence:
1. Tighten schema scope per source
2. Add concise source descriptions
3. Add source-specific example queries
4. Add short topic-based routing rules

References:
- https://learn.microsoft.com/en-us/fabric/data-science/data-agent-routing

## Routing Best Practices (Mandatory)
- Keep each source narrowly scoped to one topic area.
- Avoid overlapping descriptions that create source ambiguity.
- Include representative examples that are clearly source-specific.
- Encode explicit routing hints for finance, customer/service, engagement, and cross-domain questions.
- Validate orchestration outcomes and iteratively refine schema/description/examples/rules.

## Evaluation Pattern
Use the same test prompts across all six steps so quality movement is attributable.

Recommended assets:
- evaluation/evaluation_dataset.json
- evaluation/evaluate_agent.py
- step1/step1_results.json ... step6/step6_results.json

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
- Ensure all paths and instructions reflect folderized steps.
- Include reproducible commands where practical.

## Packaging Rules For Future Events
- Keep only multi-table artifacts for final event package.
- Remove legacy single-table assets.
- Group all outputs by step folders.
- Keep user-facing guide concise and practical.
- Keep reusable domain profiles under `config/domains/` and generated deployment logic under `deployment/`.
- Do not commit generated PBIP, PBIX, BIM, or report-template artifacts.

## Success Criteria
- A participant can run the walkthrough end-to-end without hidden dependencies.
- Step-by-step quality improvements are demonstrable.
- Step 6 clearly shows better multi-source routing behavior.
- Repo is ready to publish and share publicly.

## Reusable Deliverables Checklist
- Multi-table raw CSV package
- Multi-table cleaned CSV package
- Validated domain profile
- Notebook-generated Basic and Optimized Direct Lake semantic models
- Ontology definition
- Multi-source routing configuration
- Step 6 derived data generator and outputs
- User guide
- Deployment guide
- Evaluation script, dataset, and per-step results

Industry adaptation add-ons:
- One short `INDUSTRY_PROFILE` document in the repo root
- 10 to 20 industry-specific test prompts mapped to the same evaluation intent categories

## Suggested 15-Minute Demo Script
1. Show Step 1 baseline errors and ambiguity
2. Show Step 2 stabilization from cleaning
3. Show Step 3 structural gains from semantic model
4. Show Step 4 major uplift from optimization + Prep for AI
5. Show Step 5 relationship reasoning with ontology
6. Show Step 6 orchestrator routing improvements across sources

## Notes For Skill Operators
- If a user asks for scale-up, increase row counts but preserve table relationships.
- If a user asks for realism, expand finance and engagement behavior before tuning prompts.
- If a user asks for event readiness, prioritize deployment reproducibility and clear documentation over additional model complexity.
- If a user changes industry, keep table roles and evaluation structure constant, and only swap domain lexicon, KPIs, and example prompts.

