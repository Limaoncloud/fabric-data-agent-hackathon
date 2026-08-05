# Fabric Data Agent Hackathon Demo

## What This Repository Is

This repository provides a complete, reusable Microsoft Fabric Data Agent hackathon package.

It demonstrates how answer quality improves across a six-step maturity journey:
1. Raw multi-table data baseline
2. Cleaned multi-table data
3. Basic semantic model
4. Optimized semantic model with Prep for AI
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

1. Upload cleaned files from step2 to a Fabric Lakehouse.
2. Create a Data Agent over cleaned tables.
3. Connect to an optimized semantic model (step4 reference).
4. Generate and upload Step 6 derived files.
5. Apply Step 6 routing template and run test prompts.

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
- step1/step1_raw_customers.csv
- step1/step1_raw_cases.csv
- step1/step1_raw_solicitors.csv
- step1/step1_raw_transactions.csv
- step1/step1_raw_interactions.csv
- step2/generate_step2_data.py
- step2/step2_cleaned_customers.csv
- step2/step2_cleaned_cases.csv
- step2/step2_cleaned_solicitors.csv
- step2/step2_cleaned_transactions.csv
- step2/step2_cleaned_interactions.csv
- step6/generate_step6_data.py
- step6/step6_client_engagement_summary.csv
- step6/step6_case_finance_insights.csv
- step6/step6_solicitor_performance_mart.csv

### Model and agent configuration
- step3/step3_basic_semantic_model.json
- step4/step4_optimized_semantic_model.json
- step5/step5_ontology_definition.json
- step6/step6_data_agent_configuration.json

### Evaluation and testing
- evaluate_agent.py
- evaluation_dataset.json
- TEST_QUERIES.md
- EVALUATION_GUIDE.md
- EVALUATION_COMPARISON.md

## How To Run Local Scripts

Prerequisite: Python 3.10+

Generate Step 1 raw data:

```powershell
python step1/generate_step1_data.py
```

Generate Step 2 cleaned data:

```powershell
python step2/generate_step2_data.py
```

Generate Step 6 derived data sources:

```powershell
python step6/generate_step6_data.py
```

Run simulation evaluation for all steps:

```powershell
for ($i=1; $i -le 6; $i++) {
    python evaluate_agent.py --dataset evaluation_dataset.json --output step${i}/step${i}_results.json --simulation --step $i
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

Keep the same six-step method and replace only domain profile elements:
- Customer entity name
- Service/workflow entity name
- Staff/owner entity name
- Financial entity name
- Interaction entity name
- Currency and KPI names

This allows reuse across Retail, Insurance, Banking, Healthcare, Manufacturing, and more.

## Suggested Demo Flow (15 Minutes)

1. Show baseline quality on raw or cleaned tables.
2. Show semantic model uplift.
3. Show ontology reasoning uplift.
4. Show Step 6 routing improvements across multiple sources.

## Notes

- This repo intentionally focuses on multi-table artifacts for realistic Customer 360 behavior.
- Keep prompt sets consistent across steps for fair quality comparison.
- For event delivery, prioritize reproducibility over custom complexity.
