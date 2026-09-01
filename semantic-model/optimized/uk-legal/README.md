# Optimized Direct Lake Semantic Model (Facilitator Reference)

## Purpose

Demonstrate semantic-model best practices and high / 100% Copilot accuracy using an optimized Direct Lake semantic model over the LegalFirmDemo Lakehouse.

The deployment notebook generates and deploys `LegalFirmSemanticModel` automatically from `config/domains/uk-legal.json`; you do not need to build it by hand. This document is a facilitator/background reference describing exactly what the notebook builds (sections 1-4) and the participant-authored steps that remain manual (sections 5-8: verified-answer report, Prep for AI, pinning verified answers, and Lakehouse routing configuration).

## 1. What the notebook creates

The notebook creates a Direct Lake semantic model named LegalFirmSemanticModel over the LegalFirmDemo Lakehouse, using the five base cleaned tables (`base_customers`, `base_cases`, `base_transactions`, `base_solicitors`, `base_interactions`).

## 2. Tables renamed for business-friendly usage

| Original table | Rename to |
| --- | --- |
| base_customers | Customers |
| base_cases | Cases |
| base_transactions | Transactions |
| base_solicitors | Solicitors |
| base_interactions | Interactions |

## 3. Star schema relationships already configured

The notebook creates these relationships:

| Relationship | From | To | Cardinality | Cross filter |
| --- | --- | --- | --- | --- |
| Customers (1) to Cases (*) | Customers[customer_id] | Cases[customer_id] | One to many | Both |
| Cases (1) to Transactions (*) | Cases[case_id] | Transactions[case_id] | One to many | Single |
| Customers (1) to Interactions (*) | Customers[customer_id] | Interactions[customer_id] | One to many | Single |
| Solicitors (1) to Cases (*) | Solicitors[solicitor_name] | Cases[solicitor_name] | One to many | Single |

*Note: The solicitor relationship works for demo purposes, but using a `solicitor_id` would be better practice in a production model.*

## 4. Measures already created

The notebook creates a blank table named `_Measures` with these measures:

| Group | DAX measure |
| --- | --- |
| Customer Metrics | Total Customers = COUNTROWS(Customers) |
| Customer Metrics | Active Customers = CALCULATE(COUNTROWS(Customers), Customers[status] = "Active") |
| Customer Metrics | Corporate Customers = CALCULATE(COUNTROWS(Customers), Customers[customer_type] = "Corporate") |
| Case Metrics | Total Cases = COUNTROWS('Cases') |
| Case Metrics | Open Cases = CALCULATE(COUNTROWS('Cases'), 'Cases'[case_status] = "Open") |
| Case Metrics | Total Case Value = SUM(Cases[case_value_gbp]) |
| Case Metrics | Average Case Value = AVERAGE(Cases[case_value_gbp]) |
| Transaction Metrics | Total Revenue = SUMX(FILTER(Transactions, Transactions[transaction_type] = "Invoice"), Transactions[amount_gbp]) |
| Transaction Metrics | Total Expenses = SUMX(FILTER(Transactions, Transactions[transaction_type] = "Expense"), Transactions[amount_gbp]) |
| Transaction Metrics | Total Hours Billed = SUM(Transactions[hours_worked]) |
| Transaction Metrics | Outstanding Invoices = CALCULATE(COUNTROWS(Transactions), Transactions[transaction_type] = "Invoice", Transactions[payment_status] = "Unpaid") |
| Solicitor Metrics | Total Solicitors = COUNTROWS(Solicitors) |
| Solicitor Metrics | Average Hourly Rate = AVERAGE(Solicitors[hourly_rate_gbp]) |
| Solicitor Metrics | Cases Per Solicitor = DIVIDE([Total Cases], [Total Solicitors], 0) |
| Interaction Metrics | Total Interactions = COUNTROWS(Interactions) |
| Interaction Metrics | Average Interaction Duration = AVERAGE(Interactions[duration_minutes]) |

## 5. Create a report for verified answers

Verified answers should be based on saved report visuals, not raw DAX pasted into the answer box.

1. From the LegalFirmSemanticModel semantic model, select Create report.
1. Create a report named LegalFirmSemanticModel QA Report.
1. Add a page called Verified Answers.
1. Add the visuals below using the measures from `_Measures`.
1. Save the report.

| Question | Visual type | Configuration |
| --- | --- | --- |
| How many customers do we have? | Card | Measure: [Total Customers] |
| What is the total case value? | Card | Measure: [Total Case Value] |
| How many open cases do we have? | Card | Measure: [Open Cases] |
| What is the total revenue? | Card | Measure: [Total Revenue] |
| How many unpaid invoices do we have? | Card | Measure: [Outstanding Invoices] |

## 6. Configure Prep data for AI

Go back to the LegalFirmSemanticModel semantic model and open Model settings > Prep data for AI.

### A. Select AI data schema fields

| Table | Columns to include |
| --- | --- |
| Customers | Customer ID, Customer Name, Customer Type, City, Customer Status |
| Cases | Case ID, Case Type, Case Value, Case Status, Start Date |
| Solicitors | Solicitor Name, Specialization, Hourly Rate |
| Transactions | Transaction Type, Transaction Date, Transaction Amount, Payment Status, Hours Worked |
| Interactions | Interaction Type, Interaction Date, Duration Minutes |

Include all measures from `_Measures`.

### B. Add AI instructions

#### Business context

- This is a UK legal firm specializing in conveyancing, employment law, family law, and commercial law.
- Customers can be Individual or Corporate.
- Cases are assigned to solicitors with different specializations.
- Financial transactions include Invoices, Payments, Timesheets, and Expenses.
- Fiscal year runs April to March.

#### Terminology

- Revenue means Invoice transactions only, not Payments.
- Billed hours means `hours_worked` from Timesheet transactions.
- Outstanding means Invoices with `payment_status = Unpaid`.
- Active customers have `status = Active`.

#### Calculation rules

- Always filter Transactions by `transaction_type` when calculating revenue, expenses, invoices, payments, or timesheets.
- Case values are in GBP.
- Dates use UK date format.
- When calculating top, highest, most, or best, sort descending.
- When asked about this year, use the current calendar year unless the user specifically asks for fiscal year.

#### Thresholds

- High-value case: `case_value_gbp` greater than 100000.
- Large customer: more than 5 cases.
- Senior solicitor: `hourly_rate_gbp` greater than 300.

### C. Add Data Agent instructions

Open the `LegalFirmAgent` Data Agent item and paste the following into **Data Agent instructions**. These instructions control source selection and answer behaviour. Keep business definitions and calculation rules in the semantic model's **Prep data for AI > AI instructions** section above.

```text
Use LegalFirmSemanticModel as the preferred source for business questions about customers, cases, solicitors, transactions, interactions, revenue, case value, billed hours, and outstanding invoices.

Use explicit semantic-model measures whenever an appropriate measure exists. Do not recreate a measure by aggregating a raw column. Apply the business definitions and calculation rules configured in the semantic model's Prep data for AI instructions.

Treat "matter" and "matters" as alternative terms for "case" and "cases". If a request is ambiguous and different interpretations would materially change the answer, ask one concise clarifying question before querying.

Present monetary values in GBP with two decimal places. Present dates in UK format. State any filters or time period used, and keep the response concise.

Do not invent values, definitions, or legal conclusions. If the available data cannot answer a question, say what information is missing. Answers are for demonstration and operational analysis only and must not be presented as legal advice.
```

Facilitator check: ask **What is our average case value?** and confirm that the answer uses `LegalFirmSemanticModel`, formats the result in GBP, and states the relevant scope or filters. Then ask **How many matters are currently open?** to confirm the terminology is handled consistently.

## 7. Create verified answers correctly

Verified answers are pinned directly on a report visual, not configured from Prep data for AI. Create them from the saved visuals in LegalFirmSemanticModel QA Report. Do not paste raw DAX as the answer.

| User question | Verified answer source |
| --- | --- |
| How many customers do we have? | Card visual using [Total Customers] |
| What is the total case value? | Card visual using [Total Case Value] |
| How many open cases do we have? | Card visual using [Open Cases] |
| What is the total revenue? | Card visual using [Total Revenue] |
| How many unpaid invoices do we have? | Card visual using [Outstanding Invoices] |

1. Open LegalFirmSemanticModel QA Report and go to the Verified Answers page.
1. Select the Card visual that answers the question.
1. Open the visual's **...** menu and select **Add to Q&A**.
1. Enter the natural-language question and turn on **Verified answer**.
1. Add a short description explaining the business meaning.
1. Save the report.
1. Repeat for each remaining question and visual.

## 8. Configure the Lakehouse source and final agent routing

Add `LegalFirmDemo` to the existing `LegalFirmAgent` as a second data source. Do not create a separate agent. Lakehouse sources do not have the semantic-model synonym editor; configure them with selected tables and columns, a data source description, Data Agent instructions, and validated SQL example queries.

### A. Initial Lakehouse configuration with base tables

Select only these tables for the initial Lakehouse test:

- `base_customers`
- `base_cases`
- `base_solicitors`
- `base_transactions`
- `base_interactions`

Paste this into the **Description** for the `LegalFirmDemo` data source:

```text
Detailed UK legal-firm Lakehouse data at customer, case, solicitor, transaction, and interaction grain. Use the base_* tables only for detailed row-level questions, combinations, or filters that LegalFirmSemanticModel does not expose. For standard counts, totals, revenue, case value, billed hours, and unpaid-invoice questions, prefer LegalFirmSemanticModel and its explicit measures.
```

Replace the earlier Data Agent instructions with this combined version:

```text
Prefer LegalFirmSemanticModel for standard customer, case, solicitor, transaction, and interaction questions that can be answered by model fields or explicit measures. Do not recreate an existing semantic-model measure by aggregating a raw Lakehouse column.

Use the LegalFirmDemo base_* tables only when a question needs row-level detail, a specific column or filter that the semantic model does not expose, or a multi-table calculation that cannot be answered by one semantic-model measure.

In legal terminology, "matter" and "matters" mean "case" and "cases". For a Lakehouse query, use base_cases for that concept.

Do not combine sources unless the requested result cannot be answered by one selected source. If different interpretations would materially change the result, ask one concise clarifying question before querying.

Present monetary values in GBP with two decimal places and dates in UK format. State the filters and time period used. Do not invent missing values, definitions, or legal conclusions. Answers are for demonstration and operational analysis only and must not be presented as legal advice.
```

Add and validate this non-challenge example under **Example queries** for `LegalFirmDemo`:

**Question:** How many payment transactions were recorded?

```sql
SELECT COUNT(*) AS payment_transaction_count
FROM base_transactions
WHERE transaction_type = 'Payment';
```

The expected result is **199**. Also test **How many payments are in the transaction table?** and confirm the same result and source.

### B. Final Lakehouse configuration with routing tables

Add these prepared tables to the same `LegalFirmDemo` source:

- `routing_client_engagement_summary`
- `routing_case_finance_insights`
- `routing_solicitor_performance_mart`

Replace the Lakehouse data source description with this final version:

```text
Detailed and prepared UK legal-firm analysis data. Use routing_client_engagement_summary only for customer engagement segments and interaction recency. Use routing_case_finance_insights only for combined case-finance outcomes, payment risk, and outstanding balances by case. Use routing_solicitor_performance_mart only for solicitor rankings and performance tiers. Use base_* tables only for row-level detail or filters not exposed by LegalFirmSemanticModel. Prefer LegalFirmSemanticModel for standard business metrics supported by model fields or explicit measures.
```

Replace the Data Agent instructions with this final combined version:

```text
Prefer LegalFirmSemanticModel for standard customer, case, solicitor, transaction, and interaction questions that can be answered by model fields or explicit measures. Do not recreate an existing semantic-model measure from raw Lakehouse columns.

Use LegalFirmDemo base_* tables only when a question needs row-level detail, a specific column or filter that the semantic model does not expose, or a multi-table calculation that cannot be answered by one semantic-model measure.

Use routing_client_engagement_summary only for engagement segments and interaction recency. Use routing_case_finance_insights only for combined case-finance outcomes, payment risk, and outstanding balances by case. Use routing_solicitor_performance_mart only for solicitor rankings and performance tiers.

In legal terminology, "matter" and "matters" mean "case" and "cases". Use the table appropriate to the requested analysis rather than treating matter as a separate entity.

Prefer one source when the question is clear. Do not combine sources unless the requested result cannot be answered by one selected source. If different interpretations would materially change the result, ask one concise clarifying question before querying.

Present monetary values in GBP with two decimal places and dates in UK format. State the filters and time period used. Do not invent missing values, definitions, or legal conclusions. Answers are for demonstration and operational analysis only and must not be presented as legal advice.
```

Add and validate these examples under **Example queries** for `LegalFirmDemo`:

**Question:** Which customers are in the low engagement segment?

```sql
SELECT customer_id, customer_name, total_interactions, last_interaction_date
FROM routing_client_engagement_summary
WHERE engagement_segment = 'Low Engagement'
ORDER BY customer_name;
```

**Question:** Which high-value open cases have outstanding balances?

```sql
SELECT case_id, solicitor_name, case_value_gbp, outstanding_amount_gbp
FROM routing_case_finance_insights
WHERE case_status = 'Open'
	AND case_value_gbp >= 100000
	AND outstanding_amount_gbp > 0
ORDER BY outstanding_amount_gbp DESC;
```

**Question:** Which solicitors are in the top performance tier?

```sql
SELECT solicitor_name, cases_handled, total_case_value_gbp
FROM routing_solicitor_performance_mart
WHERE performance_tier = 'Top'
ORDER BY total_case_value_gbp DESC;
```

### C. Facilitator routing checks

Clear the agent chat before the test, then inspect the selected source and generated DAX or SQL for each question.

| Test question | Expected source | Expected object |
| --- | --- | --- |
| How many active customers do we have? | `LegalFirmSemanticModel` | `[Active Customers]` |
| What is our total revenue? | `LegalFirmSemanticModel` | `[Total Revenue]` |
| How many payment transactions were recorded? | `LegalFirmDemo` | `base_transactions` |
| Which customers are in the low engagement segment? | `LegalFirmDemo` | `routing_client_engagement_summary` |
| Which high-value open cases have outstanding balances? | `LegalFirmDemo` | `routing_case_finance_insights` |
| Which solicitors are in the top performance tier? | `LegalFirmDemo` | `routing_solicitor_performance_mart` |

For each test, also ask one paraphrase. A successful configuration returns the correct result, chooses the expected source, uses the expected measure or table, and states important filters without blending sources unnecessarily.

## Result

You now have an optimized Direct Lake semantic model with a clean star schema, business-friendly measures, AI schema configuration, AI instructions, verified answers grounded in actual report visuals, and a Data Agent configured to route appropriately between the semantic model and Lakehouse.