# Fabric Data Agent Hackathon Demo

## What This Repository Is

This repository provides a complete, reusable Microsoft Fabric Data Agent hackathon package.

It demonstrates how answer quality improves across a six-phase maturity journey:
1. Data readiness
2. Semantic model readiness
3. Agent configuration
4. Lakehouse source tuning
5. Routing with derived data
6. Optional ontology

USER_GUIDE.md implements this journey as six numbered workshop steps for one continuously-extended Data Agent.

Default example domain is UK legal Customer 360, and the package can be adapted to other industries.

## Who This Is For

- Hackathon organizers who need a repeatable Fabric Data Agent demo
- Solution architects demonstrating semantic model and routing impact
- Teams learning how to productionize agent quality step by step

## Start Here

Choose one path:

| Role | Start with | Purpose |
| --- | --- | --- |
| Participant | [USER_GUIDE.md](USER_GUIDE.md) | Follow the six workshop steps and test one continuously improved Data Agent |
| Facilitator | [FACILITATOR_GUIDE.md](FACILITATOR_GUIDE.md) | Prepare the event, use solution checkpoints, give hints, and validate results |
| Automation or troubleshooting | [deployment/README.md](deployment/README.md) | Understand deployment parameters, generated artifacts, and rerun behavior |

Use `NB_Deploy_Data_Agent_Hackathon.ipynb` to create the environment. Use `NB_Run_SDK_Evaluation.ipynb` to capture live baseline/final evidence, then use `NB_Review_And_Score_Data_Agent.ipynb` to calculate the reviewed 24-point scorecard.

### Notebook Guide

| Notebook | Use it for |
| --- | --- |
| `NB_Deploy_Data_Agent_Hackathon.ipynb` | Create or reset the Lakehouse, tables, and semantic model |
| `NB_Run_SDK_Evaluation.ipynb` | Run measured baseline/final tests against the live Data Agent |
| `NB_Review_And_Score_Data_Agent.ipynb` | Enter reviewed evidence and calculate the deterministic 24-point score |

These two notebooks are the complete evaluation workflow. The first captures evidence; the second reviews and scores it.

## Repository Highlights

- Multi-table data assets across artifact-typed folders keyed by domain
- Semantic model and ontology configuration templates
- Routing configuration and derived-routing data generator
- Evaluation harness and sample prompt dataset
- End-user and deployment documentation
- Copilot skill documents for future event reuse

## Quick Start (30 Minutes)

1. Download [NB_Deploy_Data_Agent_Hackathon.ipynb](https://github.com/Limaoncloud/fabric-data-agent-hackathon/blob/dev/NB_Deploy_Data_Agent_Hackathon.ipynb) and use **Import → Notebook** to upload it into a capacity-backed Fabric workspace. First time importing a notebook into Fabric? See [USER_GUIDE.md](USER_GUIDE.md#import-the-deployment-notebook-into-fabric) for exact steps.
2. Leave `WORKSPACE_ID=""` and `DOMAIN_PROFILE="uk-legal"` for the default deployment.
3. Keep `ENABLE_PREP_FOR_AI=False`, `ENABLE_DATA_AGENT=False`, and preview stages disabled.
4. Run all cells to create the Lakehouse, Delta tables, and the Optimized Direct Lake semantic model.
5. Participants create and tune one Data Agent, starting with the semantic model, then adding Lakehouse routing.

The notebook generates semantic models as TMDL through Fabric APIs. It does not require PBIP or PBIX files.

Notebook deployment details:
- [deployment/README.md](deployment/README.md)

Use this guide:
- skills/fabric-data-agent-hackathon/SKILL_QUICKSTART_30MIN.md

## Full Build Path

Follow the complete end-to-end user flow:
- USER_GUIDE.md

The table and two-source routing architecture is documented below.

Deployment details:
- deployment/README.md

## Multi-Table Architecture

The deployment notebook creates `LegalFirmDemo`, a Lakehouse with eight managed Delta tables, and `LegalFirmSemanticModel`, an optimized Direct Lake semantic model.

### Baseline Lakehouse Tables

| Table | Grain | Current rows |
| --- | --- | ---: |
| `base_customers` | One row per customer | 171 |
| `base_cases` | One row per legal case | 500 |
| `base_solicitors` | One row per solicitor | 15 |
| `base_transactions` | One row per transaction | 1,000 |
| `base_interactions` | One row per interaction | 800 |

### Derived Routing Tables

| Table | Grain | Routing purpose |
| --- | --- | --- |
| `routing_client_engagement_summary` | One row per customer | Engagement segments and interaction recency |
| `routing_case_finance_insights` | One row per case | Combined case-finance outcomes and payment risk |
| `routing_solicitor_performance_mart` | One row per solicitor | Performance tiers and solicitor rankings |

### Final Routing Architecture

Create one Fabric Data Agent with exactly two sources:

| Source | Selected objects | Use when |
| --- | --- | --- |
| `LegalFirmSemanticModel` | All five model tables | Standard customer, case, solicitor, transaction, interaction, and explicit-measure questions |
| `LegalFirmDemo` | Only the three `routing_*` tables | Engagement segments, combined case-finance outcomes, payment risk, and solicitor performance tiers |

This is the final Step 5 configuration. Steps 3-4 temporarily select the five `base_*` Lakehouse tables to teach detailed lookup and source tuning. Step 5 deselects them and selects only the three `routing_*` tables because the semantic model already covers standard business topics.

Lakehouse sources support validated SQL example question/query pairs. Power BI semantic-model sources do not. Configure semantic-model synonyms through Prep for AI, not on Lakehouse tables.

The deployable source of truth is [config/domains/uk-legal.json](config/domains/uk-legal.json). The human-readable routing configuration is [agent-configuration/routing/uk-legal/data-agent-configuration.json](agent-configuration/routing/uk-legal/data-agent-configuration.json).

## Step Assets

The three routing folders are intentionally separate:

| Folder | Contains |
| --- | --- |
| `sample-data/uk-legal/derived-routing/` | CSV data used to create the three prepared routing tables |
| `agent-configuration/routing/uk-legal/` | Reference Data Agent source selection and routing configuration |
| `evaluation/routing/uk-legal/` | Optional Step 5 routing test questions and expected answers |

### Data generation and data files
- sample-data/uk-legal/base/generate_base_data.py
- sample-data/uk-legal/base/customers.csv
- sample-data/uk-legal/base/cases.csv
- sample-data/uk-legal/base/solicitors.csv
- sample-data/uk-legal/base/transactions.csv
- sample-data/uk-legal/base/interactions.csv
- sample-data/uk-legal/derived-routing/generate_derived_routing_data.py
- sample-data/uk-legal/derived-routing/client_engagement_summary.csv
- sample-data/uk-legal/derived-routing/case_finance_insights.csv
- sample-data/uk-legal/derived-routing/solicitor_performance_mart.csv

### Model and agent configuration
- NB_Deploy_Data_Agent_Hackathon.ipynb
- config/domain-profile.schema.json
- config/domains/uk-legal.json
- deployment/hackathon_deployer.py
- semantic-model/optimized/uk-legal/README.md
- ontology/uk-legal/ontology-definition.json
- agent-configuration/routing/uk-legal/data-agent-configuration.json

### Evaluation and testing
- NB_Run_SDK_Evaluation.ipynb
- NB_Review_And_Score_Data_Agent.ipynb
- evaluation/challenge/uk-legal.json
- evaluation/routing/uk-legal.json
- FACILITATOR_GUIDE.md
- evaluation/EVALUATION_GUIDE.md

## How To Run Local Scripts

Prerequisite: Python 3.10+

Generate or validate the UK legal base dataset:

```powershell
python sample-data/uk-legal/base/generate_base_data.py
```

Generate the derived routing data sources:

```powershell
python sample-data/uk-legal/derived-routing/generate_derived_routing_data.py
```

Run the repository tests with `python -m unittest discover -s tests -v`.

## How To Use The Copilot Skills

Full playbook skill:
- skills/fabric-data-agent-hackathon/SKILL.md

Quickstart skill:
- skills/fabric-data-agent-hackathon/SKILL_QUICKSTART_30MIN.md

Example prompts to invoke:
- Use the Fabric Data Agent Hackathon Playbook skill and run the six-step setup for UK legal Customer 360.
- Use the 30-minute hackathon quickstart skill for Retail with the same six-step structure.

## Adapting To Other Industries

Keep the same six-step method and create a validated domain profile containing:
- Customer entity name
- Service/workflow entity name
- Staff/owner entity name
- Financial entity name
- Interaction entity name
- Source schemas, relationships, measures, currency, AI instructions, and routing

Set `DOMAIN_PROFILE` to a committed profile name, or provide `CUSTOM_PROFILE_URL` and `ASSET_BASE_URL`. This allows reuse across Retail, Insurance, Banking, Healthcare, Manufacturing, and more without changing notebook code.

For the JSON-free CSA workflow, one-hour runbook, and a complete copy-paste Water Utilities example, see [REUSE_FOR_NEW_INDUSTRY.md](REUSE_FOR_NEW_INDUSTRY.md). In VS Code Chat, type `/`, select **Generate Hackathon Domain**, and describe the industry in plain English.

## Suggested Demo Flow (15 Minutes)

1. Show baseline quality on raw or cleaned tables.
2. Show semantic model uplift.
3. Show multi-source routing improvements across the Lakehouse and derived data.
4. Show optional ontology reasoning uplift.

## Notes

- This repo intentionally focuses on multi-table artifacts for realistic Customer 360 behavior.
- Keep prompt sets consistent across steps for fair quality comparison.
- For event delivery, prioritize reproducibility over custom complexity.


