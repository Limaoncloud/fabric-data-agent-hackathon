# Step 4: Create Optimized Direct Lake Semantic Model

## Purpose

Demonstrate semantic-model best practices and high / 100% Copilot accuracy using an optimized Direct Lake semantic model over the LegalFirmDemo Lakehouse.

## 1. Create the Direct Lake semantic model

1. Open Microsoft Fabric in the browser.
1. Go to the workspace containing the LegalFirmDemo Lakehouse.
1. Open the LegalFirmDemo Lakehouse.
1. Select New semantic model.
1. Choose the Step 2 cleaned tables only.
1. Select all 5 optimized tables: step1_cleaned_customers, step1_cleaned_cases, step1_cleaned_transactions, step1_cleaned_solicitors, and step1_cleaned_interactions.
1. Create the semantic model in Direct Lake mode.
1. Name it LegalFirmOptimized.
1. Open the semantic model.

## 2. Rename tables for business-friendly usage

| Original table | Rename to |
| --- | --- |
| step1_cleaned_customers | Customers |
| step1_cleaned_cases | Cases |
| step1_cleaned_transactions | Transactions |
| step1_cleaned_solicitors | Solicitors |
| step1_cleaned_interactions | Interactions |

## 3. Create the star schema relationships

In Model view, create these relationships:

| Relationship | From | To | Cardinality | Cross filter |
| --- | --- | --- | --- | --- |
| Customers (1) to Cases (*) | Customers[customer_id] | Cases[customer_id] | One to many | Both |
| Cases (1) to Transactions (*) | Cases[case_id] | Transactions[case_id] | One to many | Single |
| Customers (1) to Interactions (*) | Customers[customer_id] | Interactions[customer_id] | One to many | Single |
| Solicitors (1) to Cases (*) | Solicitors[solicitor_name] | Cases[solicitor_name] | One to many | Single |

*Note: The solicitor relationship works for demo purposes, but using a `solicitor_id` would be better practice in a production model.*

## 4. Create a measures table

Create a blank table named `_Measures`, then add these measures:

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

1. From the LegalFirmOptimized semantic model, select Create report.
1. Create a report named LegalFirmOptimized QA Report.
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

Go back to the LegalFirmOptimized semantic model and open Model settings > Prep data for AI.

### A. Select AI data schema fields

| Table | Columns to include |
| --- | --- |
| Customers | customer_id, customer_name, customer_type, city, status |
| Cases | case_id, case_type, case_value_gbp, case_status, start_date, solicitor_name, customer_id |
| Solicitors | solicitor_name, specialization, hourly_rate_gbp |
| Transactions | transaction_type, amount_gbp, payment_status, case_id, hours_worked |
| Interactions | interaction_type, interaction_date, customer_id, duration_minutes |

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

## 7. Create verified answers correctly

In Prep data for AI > Verified answers, create verified answers from the saved report visuals in LegalFirmOptimized QA Report. Do not paste raw DAX as the answer.

| User question | Verified answer source |
| --- | --- |
| How many customers do we have? | Card visual using [Total Customers] |
| What is the total case value? | Card visual using [Total Case Value] |
| How many open cases do we have? | Card visual using [Open Cases] |
| What is the total revenue? | Card visual using [Total Revenue] |
| How many unpaid invoices do we have? | Card visual using [Outstanding Invoices] |

1. Click New verified answer.
1. Enter the natural-language question.
1. Select the LegalFirmOptimized QA Report.
1. Select the Verified Answers page.
1. Select the visual that answers the question.
1. Add a short description explaining the business meaning.
1. Save the verified answer.

## Result

You now have an optimized Direct Lake semantic model with a clean star schema, business-friendly measures, AI schema configuration, AI instructions, and verified answers grounded in actual report visuals.