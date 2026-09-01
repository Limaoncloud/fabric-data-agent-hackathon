# Optimized Direct Lake Semantic Model (Facilitator Reference)

## Purpose

Demonstrate semantic-model best practices and high / 100% Copilot accuracy using an optimized Direct Lake semantic model over the LegalFirmDemo Lakehouse.

The deployment notebook generates and deploys `LegalFirmSemanticModel` automatically from `config/domains/uk-legal.json`; you do not need to build it by hand. This document is a facilitator/background reference describing exactly what the notebook builds (sections 1-4) and the participant-authored steps that remain manual (sections 5-7: verified-answer report, Prep for AI, and pinning verified answers).

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

## Result

You now have an optimized Direct Lake semantic model with a clean star schema, business-friendly measures, AI schema configuration, AI instructions, and verified answers grounded in actual report visuals.