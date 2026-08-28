# Multi-Table Architecture Reference

This file is a concise architecture reference for the UK Legal Data Agent hackathon. Participant instructions are in [USER_GUIDE.md](USER_GUIDE.md); deployment instructions are in [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md).

## Deployed Assets

The organizer notebook creates these items before participants begin:

- `LegalFirmDemo` Lakehouse with eight managed Delta tables.
- `LegalFirmOptimized` Direct Lake semantic model.

`LegalFirmBasic` is not deployed by the notebook. Build it manually from [semantic-model/basic-reference/uk-legal/README.md](semantic-model/basic-reference/uk-legal/README.md) only if you want the anti-pattern comparison.

### Baseline Lakehouse Tables

| Table | Grain | Current rows |
| --- | --- | ---: |
| `step1_cleaned_customers` | One row per customer | 171 |
| `step1_cleaned_cases` | One row per legal case | 500 |
| `step1_cleaned_solicitors` | One row per solicitor | 15 |
| `step1_cleaned_transactions` | One row per transaction | 1,000 |
| `step1_cleaned_interactions` | One row per interaction | 800 |

### Derived-Routing Analysis Tables

| Table | Grain | Routing purpose |
| --- | --- | --- |
| `step6_client_engagement_summary` | One row per customer | Engagement segments and interaction recency |
| `step6_case_finance_insights` | One row per case | Combined case and financial outcomes or payment risk |
| `step6_solicitor_performance_mart` | One row per solicitor | Performance tiers and solicitor rankings |

## Semantic Models

`LegalFirmBasic` contains the five business tables without relationships and includes intentionally ambiguous or duplicate measures.

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
