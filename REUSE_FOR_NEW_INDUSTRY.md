# Reuse This Hackathon For Another Industry

This repository separates the reusable six-step Fabric workflow from industry-specific data and business meaning. A CSA supplies one concise domain brief; Copilot uses the existing skill and profile schema to create the full local package.

## Network Rail Quick Start

1. Review `config/domain-briefs/network-rail.json` with an asset, operations, and safety domain expert.
2. In VS Code Chat, run `/Generate Hackathon Domain network-rail`.
3. Review Copilot's assumptions before accepting generated schemas or KPIs.
4. Run all local tests before setting `DOMAIN_PROFILE="network-rail"` in the deployment notebook.
5. Keep preview deployment flags disabled until the generated Ontology and Data Agent scope have been reviewed.

To inspect or save the exact generated instruction without invoking the workspace prompt:

```powershell
python deployment/create_domain_package.py --domain network-rail
python deployment/create_domain_package.py --domain network-rail --output generated/network-rail-prompt.md
```

## Create A Different Industry

Initialize a small brief:

```powershell
python deployment/create_domain_package.py --domain water-utilities --init --display-name "Water Utilities Operations"
```

Edit `config/domain-briefs/water-utilities.json`. Replace every `REPLACE:` value and define:

- business audience and scenario
- entity grains and stable keys
- relationships and cardinality intent
- governed metric definitions
- terminology and ambiguity rules
- synthetic-data, privacy, security, and safety boundaries

Then run:

```powershell
python deployment/create_domain_package.py --domain water-utilities
```

Paste that output into Copilot Chat, or invoke `/Generate Hackathon Domain water-utilities`.

## What Copilot Generates

- validated domain profile under `config/domains/`
- deterministic base-data generator and CSVs under `sample-data/<domain>/base/`
- derived-routing marts and generator under `sample-data/<domain>/derived-routing/`
- basic and optimized semantic-model references under `semantic-model/basic-reference/<domain>/` and `semantic-model/optimized/<domain>/`
- ontology definition under `ontology/<domain>/`
- Data Agent routing configuration under `agent-configuration/routing/<domain>/`
- evaluation questions with expected answers under `evaluation/challenge/<domain>.json` and `evaluation/routing/<domain>.json`
- focused tests

The deployment notebook and `deployment/hackathon_deployer.py` remain shared. A new domain should not require notebook code changes.

## Example Chat Prompt

```text
Use the Fabric Data Agent Hackathon skill to generate the complete package for the
network-rail domain brief. Preserve the six-step journey, use deterministic synthetic
data only, calculate evaluation answers from the generated CSVs, include the railway
safety boundaries in the agent instructions, add focused tests, and do not deploy to
Fabric. Stop and list any assumptions that require a railway domain expert.
```

## Review Gate

Generation is not domain approval. Before deployment, a qualified reviewer must confirm the table grains, keys, metric definitions, synthetic distributions, agent scope, and safety wording. Never substitute generated data or answers for live railway operational systems.