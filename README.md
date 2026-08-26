# Fabric Data Agent Hackathon Demo

## What This Repository Is

This repository provides a complete, reusable Microsoft Fabric Data Agent hackathon package.

It demonstrates how answer quality improves across a six-step maturity journey:
1. Cleaned multi-table data baseline
2. Data agent configuration best practices
3. Basic semantic model
4. Optimized semantic model followed by participant-authored Prep for AI
5. Ontology layer
6. Multi-source routing with best practices

Default example domain is UK legal Customer 360, and the package can be adapted to other industries.

## Who This Is For

- Hackathon organizers who need a repeatable Fabric Data Agent demo
- Solution architects demonstrating semantic model and routing impact
- Teams learning how to productionize agent quality step by step

## Repository Highlights

- Multi-table data assets across step folders
- Semantic model and ontology configuration templates
- Step 6 routing configuration and derived data generator
- Evaluation harness and sample prompt dataset
- End-user and deployment documentation
- Copilot skill documents for future event reuse

## Quick Start (30 Minutes)

1. Import `NB_Deploy_Data_Agent_Hackathon.ipynb` into a capacity-backed Fabric workspace.
2. Leave `WORKSPACE_ID=""` and `DOMAIN_PROFILE="uk-legal"` for the default deployment.
3. Keep `ENABLE_PREP_FOR_AI=False`, `ENABLE_DATA_AGENT=False`, and preview stages disabled.
4. Run all cells to create the Lakehouse, Delta tables, and both Direct Lake semantic models.
5. Participants create Data Agents, run baseline prompts, and add selected synonyms, Prep for AI, Verified Answers, and agent instructions.

The notebook generates semantic models as TMDL through Fabric APIs. It does not require PBIP or PBIX files.

Notebook deployment details:
- [deployment/README.md](deployment/README.md)

Use this guide:
- skills/fabric-data-agent-hackathon/SKILL_QUICKSTART_30MIN.md

## Full Build Path

Follow the complete end-to-end user flow:
- USER_GUIDE.md

Deployment details:
- DEPLOYMENT_GUIDE.md

## Step Assets

### Data generation and data files
- step1/generate_step1_data.py
- step1/step1_cleaned_customers.csv
- step1/step1_cleaned_cases.csv
- step1/step1_cleaned_solicitors.csv
- step1/step1_cleaned_transactions.csv
- step1/step1_cleaned_interactions.csv
- step6/generate_step6_data.py
- step6/step6_client_engagement_summary.csv
- step6/step6_case_finance_insights.csv
- step6/step6_solicitor_performance_mart.csv

### Model and agent configuration
- NB_Deploy_Data_Agent_Hackathon.ipynb
- config/domain-profile.schema.json
- config/domains/uk-legal.json
- deployment/hackathon_deployer.py
- step3/README.md
- step4/README.md
- step5/step5_ontology_definition.json
- step6/step6_data_agent_configuration.json

### Evaluation and testing
- evaluation/evaluate_agent.py
- evaluation/evaluation_dataset.json
- evaluation/TEST_QUERIES.md
- evaluation/EVALUATION_GUIDE.md
- EVALUATION_COMPARISON.md

## How To Run Local Scripts

Prerequisite: Python 3.10+

Generate or validate Step 1 cleaned baseline data:

```powershell
python step1/generate_step1_data.py
```

Generate Step 6 derived data sources:

```powershell
python step6/generate_step6_data.py
```

Run simulation evaluation for all steps:

```powershell
for ($i=1; $i -le 6; $i++) {
    python evaluation/evaluate_agent.py --dataset evaluation/evaluation_dataset.json --output step${i}/step${i}_results.json --simulation --step $i
}
```

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

## Suggested Demo Flow (15 Minutes)

1. Show baseline quality on raw or cleaned tables.
2. Show semantic model uplift.
3. Show ontology reasoning uplift.
4. Show Step 6 routing improvements across multiple sources.

## Notes

- This repo intentionally focuses on multi-table artifacts for realistic Customer 360 behavior.
- Keep prompt sets consistent across steps for fair quality comparison.
- For event delivery, prioritize reproducibility over custom complexity.


