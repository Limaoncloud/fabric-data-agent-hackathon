# Fabric Data Agent Hackathon Quickstart Skill (30 Minutes)

## Purpose
Use this skill to stand up a fast, demo-ready Fabric Data Agent hackathon in about 30 minutes, using the prepared multi-table assets in this repository.

Default scenario:
- UK legal firm Customer 360

Flexible scenario:
- Any industry Customer 360 by remapping business entities and prompts

## Outcome
By the end of this workflow, participants can:
- Query an industry-specific Customer 360 scenario (UK legal by default)
- See quality progression across maturity steps
- Observe multi-source routing behavior in Step 6

## Industry Profile (Set First)
Define a quick profile before running the demo:
- customer entity
- service/workflow entity
- staff/owner entity
- financial entity
- interaction entity
- currency
- top KPI names

Example mappings:
- UK legal: Client, Case, Solicitor, Transaction, Interaction, GBP
- Retail: Customer, Order, StoreAssociate, Payment, SupportContact, USD
- Insurance: Policyholder, Claim, Adjuster, Payment, ContactEvent, USD

## Best Use Cases
Use when:
- You have limited event time
- You need a reliable live demo path
- You want repeatable onboarding for new hackathon teams

Do not use when:
- You need deep custom model authoring from scratch
- You need tenant-specific production hardening

## How To Use This Skill

### Fast invocation prompts
Use one of these prompts in Copilot Chat:
- "Use the Fabric Data Agent Hackathon Quickstart skill and set up a 30-minute UK legal demo."
- "Use the 30-minute hackathon quickstart skill for Retail with the same six-step structure."
- "Use the quickstart skill and give me only the must-do tasks for a live event."

### What to provide in your first prompt
- Target industry (or say "use UK legal default")
- Available time window
- Whether Step 5 ontology is in scope
- Whether to use existing repo files as-is

### What you should get back from the skill
- A time-boxed checklist by minute range
- Table/model/agent setup sequence
- Prompt pack for live testing
- Routing tuning actions for Step 6

## Inputs Required
- A Fabric workspace with permission to create Lakehouse, semantic model, and Data Agent
- `NB_Deploy_Data_Agent_Hackathon.ipynb`
- Repository assets accessible from GitHub

## 30-Minute Runbook

### 0 to 5 minutes: Deploy participant-ready assets
1. Import and open `NB_Deploy_Data_Agent_Hackathon.ipynb` in the target workspace.
2. Keep `WORKSPACE_ID=""` and `DOMAIN_PROFILE="uk-legal"` for the default scenario.
3. Keep `ENABLE_PREP_FOR_AI=False` and `ENABLE_DATA_AGENT=False`.
4. Run all cells to deploy the Lakehouse tables and the Optimized semantic model.

Success check:
- Eight Lakehouse tables and the Optimized semantic model are available; Direct Lake partitions are refreshed.

### 5 to 10 minutes: Stand up a baseline agent
1. Create a Data Agent over the cleaned Lakehouse tables.
2. Select only the five `step1_cleaned_*` tables and leave instructions/examples empty for the baseline.
3. Run baseline prompts:
   - How many active customers do we have?
  - How many open service records do we have?
   - How many unpaid invoices?

Success check:
- Agent returns data-backed answers for all baseline prompts.

### 10 to 15 minutes: Attach semantic model fast path
1. Create a new Data Agent using the predeployed `LegalFirmOptimized` semantic model.
2. Re-run baseline prompts before adding AI metadata.
3. Add one semantic-model synonym or AI instruction in Prep for AI, then retest.

Success check:
- Answers become more consistent and business-aware.

### 15 to 22 minutes: Enable Step 6 multi-source demo
1. Confirm the notebook loaded the three Step 6 tables.
2. Set `ENABLE_DATA_AGENT=True` to stage the profile-defined semantic-model and Lakehouse sources.
3. Review staging, then set `PUBLISH_DATA_AGENT=True` when ready.

Success check:
- All Step 6 tables exist and are connected.

### 22 to 27 minutes: Apply routing best practices
Apply in this order:
1. Tight schema selection per source
2. Focused source descriptions
3. Validated example query pairs for Lakehouse/KQL sources only
4. Concise topic routing rules

Reference:
- https://learn.microsoft.com/en-us/fabric/data-science/data-agent-routing

Success check:
- Distinct prompt families route to intended sources.

### 27 to 30 minutes: Live test and storytelling
Run this final prompt set:
- How many active customers do we have?
- How many unpaid invoices do we have?
- How many interaction events happened in Q1?
- Which high-value open service records also have overdue invoices?
- Which staff members are in top performance tier?

Narrative pattern:
1. Baseline on cleaned tables
2. Model uplift
3. Multi-source routing uplift

## Copy-Paste Prompt Pack For Facilitators
Use these prompts exactly during the event:

1. "How many active customers do we have?"
2. "How many open service records do we have?"
3. "How many unpaid invoices do we have?"
4. "How many interaction events happened in Q1?"
5. "Which high-value open service records also have overdue invoices?"
6. "Which staff members are in top performance tier?"

UK legal default prompt substitutions:
1. "How many open cases do we have?"
2. "How many client meetings happened in Q1?"
3. "Which solicitors are in top performance tier?"

## Minimal Artifacts Checklist
- Deployment notebook completed
- Profile-defined Lakehouse tables loaded
- Optimized Direct Lake semantic model available
- Prep for AI metadata applied
- Data Agent staged or published when enabled
- Demo prompts ready

## Troubleshooting In Event Time
- Wrong routing source selected:
  - Narrow schema further and rewrite source description with explicit scope.
- Financial prompts answered from non-finance source:
  - Add 2 to 3 stronger finance examples and a direct routing rule.
- Cross-domain prompt fails:
  - Ensure case-finance derived table is loaded and included in source scope.
- Inconsistent counts:
  - Verify table refresh and that only cleaned tables are active in the demo path.

## Facilitator Notes
- Prefer speed and reliability over feature completeness.
- Keep ontology as optional if time is constrained.
- If extra time is available, show Step 5 ontology as bonus.
- Keep the six-step structure fixed, but change domain vocabulary and KPI definitions to fit the target industry.

## Optional Extension (If +15 Minutes)
1. Add Step 5 ontology layer.
2. Re-run relationship-heavy prompts.
3. Compare improvements in cross-entity reasoning.