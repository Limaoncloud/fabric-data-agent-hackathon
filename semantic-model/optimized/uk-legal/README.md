# LegalFirmSemanticModel Artifact Reference

This folder documents the semantic model created by `NB_Deploy_Data_Agent_Hackathon.ipynb`. It is an artifact reference, not a workshop runbook.

- Participant steps: [USER_GUIDE.md](../../../USER_GUIDE.md)
- Facilitator Prep for AI, Verified Answers, routing instructions, expected answers, and checks: [FACILITATOR_GUIDE.md](../../../FACILITATOR_GUIDE.md)
- Machine-readable source of truth: [config/domains/uk-legal.json](../../../config/domains/uk-legal.json)

## Deployed Model

- Semantic model: `LegalFirmSemanticModel`
- Storage mode: Direct Lake
- Lakehouse: `LegalFirmDemo`
- Measure table: `_Measures`

| Lakehouse table | Model table |
| --- | --- |
| `base_customers` | `Customers` |
| `base_cases` | `Cases` |
| `base_transactions` | `Transactions` |
| `base_solicitors` | `Solicitors` |
| `base_interactions` | `Interactions` |

## Relationships

| From | To | Cardinality | Cross filter |
| --- | --- | --- | --- |
| `Customers[customer_id]` | `Cases[customer_id]` | One to many | Both |
| `Cases[case_id]` | `Transactions[case_id]` | One to many | Single |
| `Customers[customer_id]` | `Interactions[customer_id]` | One to many | Single |
| `Solicitors[solicitor_name]` | `Cases[solicitor_name]` | One to many | Single |

The solicitor-name relationship is suitable for the demo. A production model should use an immutable solicitor identifier.

## Measures

The deployment creates these explicit measures:

- Customer: `Total Customers`, `Active Customers`, `Corporate Customers`
- Case: `Total Cases`, `Open Cases`, `Total Case Value`, `Average Case Value`
- Transaction: `Total Revenue`, `Total Expenses`, `Total Hours Billed`, `Outstanding Invoices`
- Solicitor: `Total Solicitors`, `Average Hourly Rate`, `Cases Per Solicitor`
- Interaction: `Total Interactions`, `Average Interaction Duration`

Do not edit this document as a second copy of the facilitator instructions. Update the domain profile for generated model changes and the facilitator guide for workshop solution guidance.