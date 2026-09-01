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

Current table and two-source routing architecture:
- README_MULTITABLE.md

Deployment details:
- deployment/README.md

## Step Assets

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
- NB_Evaluate_Data_Agent_Hackathon.ipynb
- NB_Automated_Data_Agent_Evaluation.ipynb
- NB_Run_SDK_Evaluation.ipynb
- evaluation/evaluate_agent.py
- evaluation/challenge/uk-legal.json
- evaluation/routing/uk-legal.json
- evaluation/FACILITATOR_GUIDE.md
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

Run simulation evaluation for the scored challenge and the optional Step 5 routing extension (illustrative only, not measured accuracy):

```powershell
for ($i=1; $i -le 6; $i++) {
    python evaluation/evaluate_agent.py --dataset evaluation/challenge/uk-legal.json --output evaluation/results/step${i}-challenge.json --simulation --step $i
}
python evaluation/evaluate_agent.py --dataset evaluation/routing/uk-legal.json --output evaluation/results/step5-routing.json --simulation --step 5
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

For the parameter-driven CSA workflow, Network Rail example, and reusable VS Code prompt, see [REUSE_FOR_NEW_INDUSTRY.md](REUSE_FOR_NEW_INDUSTRY.md). Start with:

```powershell
python deployment/create_domain_package.py --domain network-rail
```

## Suggested Demo Flow (15 Minutes)

1. Show baseline quality on raw or cleaned tables.
2. Show semantic model uplift.
3. Show multi-source routing improvements across the Lakehouse and derived data.
4. Show optional ontology reasoning uplift.

## Notes

- This repo intentionally focuses on multi-table artifacts for realistic Customer 360 behavior.
- Keep prompt sets consistent across steps for fair quality comparison.
- For event delivery, prioritize reproducibility over custom complexity.


