# Multi-Table Architecture Reference

This file is a concise architecture reference for the UK Legal Data Agent hackathon. Participant instructions are in [USER_GUIDE.md](USER_GUIDE.md); deployment instructions are in [deployment/README.md](deployment/README.md).

## Deployed Assets

The organizer notebook creates these items before participants begin:

- `LegalFirmDemo` Lakehouse with eight managed Delta tables.
- `LegalFirmOptimized` Direct Lake semantic model.

### Baseline Lakehouse Tables

| Table | Grain | Current rows |
| --- | --- | ---: |
| `base_customers` | One row per customer | 171 |
| `base_cases` | One row per legal case | 500 |
| `base_solicitors` | One row per solicitor | 15 |
| `base_transactions` | One row per transaction | 1,000 |
| `base_interactions` | One row per interaction | 800 |

### Derived-Routing Analysis Tables

| Table | Grain | Routing purpose |
| --- | --- | --- |
| `routing_client_engagement_summary` | One row per customer | Engagement segments and interaction recency |
| `routing_case_finance_insights` | One row per case | Combined case and financial outcomes or payment risk |
| `routing_solicitor_performance_mart` | One row per solicitor | Performance tiers and solicitor rankings |

## Semantic Model

`LegalFirmOptimized` contains:

- `Customers`
- `Cases`
- `Solicitors`
- `Transactions`
- `Interactions`
- Four active one-direction relationships
- Explicit business measures
- Business-friendly names and descriptions

The participant-ready optimized model intentionally starts without synonyms, Prep for AI configuration, AI instructions, Verified Answers, or a Data Agent.

## Routing Architecture

Create one Fabric Data Agent with exactly two sources:

| Source | Selected objects | Use when |
| --- | --- | --- |
| `LegalFirmOptimized` semantic model | All five model tables | Standard customer, case, solicitor, transaction, and interaction questions answered by model fields or measures |
| `LegalFirmDemo` Lakehouse | Only the three `step6_*` analysis tables | Engagement segments, combined case-finance outcomes, payment risk, and solicitor performance tiers |

Do not select the five `step1_cleaned_*` Lakehouse tables in the routing configuration. Their standard business topics are already covered by `LegalFirmOptimized`; selecting both copies creates avoidable routing ambiguity.

SQL example question/query pairs can be configured for the Lakehouse source. They are not supported for the Power BI semantic-model source. Semantic-model synonyms are configured through Prep for AI, not on Lakehouse tables.

The deployable source-of-truth configuration is [config/domains/uk-legal.json](config/domains/uk-legal.json). The human-readable routing reference is [agent-configuration/routing/uk-legal/data-agent-configuration.json](agent-configuration/routing/uk-legal/data-agent-configuration.json).
