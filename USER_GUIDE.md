# Fabric Data Agent User Guide (Simple Step-by-Step)

This guide walks you through **Steps 1 to 6** in a simple flow:

1. Load cleaned data and create an agent baseline
2. Configure the data agent with best practices and retest
3. Build a semantic model and retest
4. Optimize the semantic model and retest
5. Bonus: Add ontology and retest
6. Bonus: Add multiple data sources with routing best practices and retest

---

## Prerequisites

- Microsoft Fabric workspace with enough capacity
- Access to create Lakehouse, Semantic Model, and Data Agent
- Power BI Desktop (for semantic model steps)
- Files already in this repo

---

## Quick File Map

### Step 1 files (cleaned baseline)
- `step1/step1_cleaned_customers.csv`
- `step1/step1_cleaned_cases.csv`
- `step1/step1_cleaned_solicitors.csv`
- `step1/step1_cleaned_transactions.csv`
- `step1/step1_cleaned_interactions.csv`

### Step 3 to 6 model/config files
- `step3/LegalFirmBasic Direct Lake Instructions.docx` (manual Power BI Service build guide)
- `step4/LegalFirmOptimized Direct Lake Instructions.docx` (manual Power BI Service optimization guide)
- `step5/step5_ontology_definition.json`
- `step6/step6_data_agent_configuration.json`

### Step 6 additional data files
- `step6/step6_client_engagement_summary.csv`
- `step6/step6_case_finance_insights.csv`
- `step6/step6_solicitor_performance_mart.csv`
- `step6/generate_step6_data.py`

### Test prompts
- `evaluation/TEST_QUERIES.md`

### Verification reference
- `Verification.xlsx` (use this workbook to validate expected answers and compare results for each step)

Validation workflow:
1. Run the test prompts for the current step.
2. Record the agent output.
3. Compare with the expected result for that step in `Verification.xlsx`.
4. Mark pass/fail and note any mismatch before moving to the next step.

---

## Step 1: Upload Cleaned Data, Build Agent, Test

### Goal
Create a baseline agent on cleaned multi-table data before semantic-model and ontology tuning.

### Actions
1. In Fabric, create a new Lakehouse (example name: `LegalFirmDemo`).
2. Upload all 5 cleaned CSV files from `step1/`:
   - `step1_cleaned_customers.csv`
   - `step1_cleaned_cases.csv`
   - `step1_cleaned_solicitors.csv`
   - `step1_cleaned_transactions.csv`
   - `step1_cleaned_interactions.csv`
3. Load each file to a new table.
4. Create a Data Agent connected to this Lakehouse/tables.
5. Add simple instructions and sample questions.

### Test (in agent chat)
Try 5 prompts:
- "How many active customers do we have?"
- "How many open cases?"
- "What is total case value?"
- "How many unpaid invoices?"
- "Which solicitor handles most cases?"

Also test these advanced prompts:
- "Find count of customers with no interactions in the last 60 days but with unpaid"
- "Calculate unpaid invoice ratio by case type: unpaid invoice count divided by total invoices."

### Expected
- Better than raw-data quality, but still room to improve
- Some ambiguity on source usage and answer style
- This is your cleaned-data baseline

---

## Step 2: Configure Data Agent Best Practices, Retest

### Goal
Improve response consistency and quality by configuring the data agent using Microsoft best practices.

### Hint
- Follow Microsoft Learn guidance:
  [Best practices for configuring your data agent - Microsoft Fabric | Microsoft Learn](https://learn.microsoft.com/en-us/fabric/data-science/data-agent-configuration-best-practices)

### Actions
1. Keep the same cleaned Step 1 tables and agent data source.
2. Improve data source scope and schema selection (include only relevant tables/columns).
3. Write clear and concise data source descriptions.
4. Add focused example prompts that represent real user intent.
5. Strengthen agent instructions:
   - domain terminology
   - expected answer style
   - assumptions and constraints
6. Keep data unchanged and rerun the same prompt set.

### Step 2 Examples You Can Reuse

#### A) Business Terms To Define Explicitly
Use this compact glossary in agent instructions (keep as one block): Active customer = `status='Active'`; Open case = `case_status='Open'`; High-value case = `case_value_gbp>=100000`; Unpaid invoice = `transaction_type='Invoice' AND payment_status='Unpaid'`; Overdue invoice = unpaid invoice older than 30 days; Revenue = sum(`amount_gbp`) for invoices; Payment collected = sum(`amount_gbp`) for payments; Billed hours = sum(`hours_worked`) for timesheets; Outstanding = Revenue - Payment collected.

#### B) Abbreviations And Synonyms
Use these canonical mappings: client->customer; matter->case; fee earner->solicitor; WIP->open case effort; AR->unpaid invoices; billed->invoice amount; collected->payment amount; top lawyer->solicitor with highest selected KPI; open matters->open cases; meetings/calls/touchpoints->interactions.

#### C) Clear Focused Instruction For The Data Agent
Copy-paste and adapt this block:

```text
You are a Fabric Data Agent for UK legal Customer 360.

Scope:
- Use only the Step 1 cleaned tables in this source.
- Do not invent fields, entities, or metrics outside the schema.

Terminology rules:
- Treat client = customer, matter = case, fee earner = solicitor.
- Revenue means Invoice amounts only.
- Outstanding means Invoice - Payment.
- Unpaid invoice means transaction_type=Invoice and payment_status=Unpaid.

Reasoning rules:
- For counts, return integer values.
- For money, return GBP with 2 decimals.
- When a request is ambiguous, state the assumption in one short line.
- If a required field is missing, say exactly what is missing.

Response style:
- Start with a direct answer in one sentence.
- Then provide a short calculation summary (max 3 bullets).
- Keep responses concise and evidence-based.
```

#### D) SQL Query Examples To Answer Questions
Use these SQL examples as the expected logic behind common business questions.

1. How many active customers do we have?

```sql
SELECT COUNT(*) AS active_customers
FROM step1_cleaned_customers
WHERE status = 'Active';
```

2. How many open cases do we have?

```sql
SELECT COUNT(*) AS open_cases
FROM step1_cleaned_cases
WHERE case_status = 'Open';
```

3. How many unpaid invoices do we have?

```sql
SELECT COUNT(*) AS unpaid_invoices
FROM step1_cleaned_transactions
WHERE transaction_type = 'Invoice'
   AND payment_status = 'Unpaid';
```

4. What is total outstanding amount?

```sql
WITH inv AS (
      SELECT COALESCE(SUM(amount_gbp), 0) AS total_invoiced
      FROM step1_cleaned_transactions
      WHERE transaction_type = 'Invoice'
),
pay AS (
      SELECT COALESCE(SUM(amount_gbp), 0) AS total_paid
      FROM step1_cleaned_transactions
      WHERE transaction_type = 'Payment'
)
SELECT CAST(inv.total_invoiced - pay.total_paid AS DECIMAL(18,2)) AS outstanding_amount_gbp
FROM inv
CROSS JOIN pay;
```

5. Which solicitors handle the most open cases?

```sql
SELECT
      solicitor_name,
      COUNT(*) AS open_case_count
FROM step1_cleaned_cases
WHERE case_status = 'Open'
GROUP BY solicitor_name
ORDER BY open_case_count DESC;
```

6. Corporate customers with more than 3 open cases and at least 1 unpaid invoice

```sql
WITH open_case_counts AS (
      SELECT
            c.customer_id,
            COUNT(*) AS open_cases
      FROM step1_cleaned_cases c
      WHERE c.case_status = 'Open'
      GROUP BY c.customer_id
),
unpaid_invoice_customers AS (
      SELECT DISTINCT
            c.customer_id
      FROM step1_cleaned_cases c
      JOIN step1_cleaned_transactions t
         ON t.case_id = c.case_id
      WHERE t.transaction_type = 'Invoice'
         AND t.payment_status = 'Unpaid'
)
SELECT
      cu.customer_id,
      cu.customer_name,
      occ.open_cases
FROM step1_cleaned_customers cu
JOIN open_case_counts occ
   ON occ.customer_id = cu.customer_id
JOIN unpaid_invoice_customers uic
   ON uic.customer_id = cu.customer_id
WHERE cu.customer_type = 'Corporate'
   AND occ.open_cases > 3
ORDER BY occ.open_cases DESC, cu.customer_name;
```

7. Cases opened this quarter with zero payments and more than 20 billed hours

```sql
WITH tx_rollup AS (
      SELECT
            case_id,
            SUM(CASE WHEN transaction_type = 'Payment' THEN amount_gbp ELSE 0 END) AS total_payments,
            SUM(CASE WHEN transaction_type = 'Timesheet' THEN hours_worked ELSE 0 END) AS total_hours
      FROM step1_cleaned_transactions
      GROUP BY case_id
)
SELECT
      c.case_id,
      c.customer_id,
      c.solicitor_name,
      c.case_type,
      c.case_status,
      c.start_date,
      COALESCE(t.total_payments, 0) AS total_payments,
      COALESCE(t.total_hours, 0) AS total_hours
FROM step1_cleaned_cases c
LEFT JOIN tx_rollup t
   ON t.case_id = c.case_id
WHERE YEAR(TRY_CONVERT(date, c.start_date, 103)) = YEAR(GETDATE())
   AND DATEPART(QUARTER, TRY_CONVERT(date, c.start_date, 103)) = DATEPART(QUARTER, GETDATE())
   AND COALESCE(t.total_payments, 0) = 0
   AND COALESCE(t.total_hours, 0) > 20
ORDER BY c.start_date;
```

8. High-value open cases that also have overdue unpaid invoices (30+ days)

```sql
SELECT DISTINCT
      c.case_id,
      c.customer_id,
      c.solicitor_name,
      c.case_value_gbp,
      c.case_status
FROM step1_cleaned_cases c
JOIN step1_cleaned_transactions t
   ON t.case_id = c.case_id
WHERE c.case_status = 'Open'
   AND c.case_value_gbp >= 100000
   AND t.transaction_type = 'Invoice'
   AND t.payment_status = 'Unpaid'
   AND TRY_CONVERT(date, t.transaction_date, 103) < DATEADD(day, -30, CAST(GETDATE() AS date))
ORDER BY c.case_value_gbp DESC;
```

### Test
Run the same 7 prompts from Step 1 and compare quality.

Add 3 to 5 complex prompts from section D above and compare:
- consistency of terminology mapping
- correctness of filter logic
- clarity of assumptions in responses

Optional validation:
- Run matching SQL from section E and compare agent answers against SQL outputs.

### Expected
- Better consistency
- Improved grounding and answer relevance
- Clearer and more repeatable answers

---

## Step 3: Build Basic Semantic Model, Retest

### Goal
Create a new Data Agent that uses a basic semantic model (non-optimized) as its data source, then observe behavior.

### Actions
1. For manual creation in **Power BI Service**, follow the Word guide: `step3/LegalFirmBasic Direct Lake Instructions.docx`.
2. In Power BI Service, connect to cleaned Lakehouse tables and build a basic model (minimal relationships, basic measures).
3. Publish the semantic model to your Fabric workspace.
4. Create a **new Data Agent** for Step 3 (do not reuse Step 1/Step 2 agent).
5. In the new agent, add the **published basic semantic model** as the data source.
6. Keep test prompts unchanged from Steps 1 and 2.

### Test
Run the same prompts 

### Expected
- Some improvement in structure-based queries
- Still confusion on certain measure selections

---

## Step 4: Optimize Semantic Model, Retest

### Goal
Apply best practices and validate major accuracy improvement.

### Hint
- You can use tools like a **Power BI Modeling MCP server** to help design a clean semantic model.
- You can also use any tools listed in Microsoft Learn here:
   [Semantic model best practices for data agent - Microsoft Fabric | Microsoft Learn](https://learn.microsoft.com/en-us/fabric/data-science/semantic-model-best-practices#tools)
- For manual optimization in **Power BI Service**, follow: `step4/LegalFirmOptimized Direct Lake Instructions.docx`.

### Actions
1. Improve model design to a clean star schema.
2. Create clear, unique measures (no duplicates/ambiguous names).
3. Configure Prep for AI:
   - AI Data Schema
   - Verified Answers
   - AI Instructions
4. Publish updated model.
5. Reconnect the agent to this optimized model.

### Test
Run the same prompt set and compare with previous steps.

### Expected
- Significant quality jump
- Better business logic understanding
- More accurate and repeatable answers

---

## Step 5 (Bonus): Add Ontology Data, Retest

### Goal
Add ontology layer for richer entity and relationship understanding.

### Actions
1. Create ontology from `step5/step5_ontology_definition.json` as reference.
2. Map entities and relationships:
   - Client
   - LegalCase
   - Solicitor
   - FinancialTransaction
   - CustomerInteraction
3. Attach ontology-aware source/context to the agent.

### Test
Run relationship-heavy prompts:
- "Which clients have open high-value cases and overdue invoices?"
- "Show solicitor workload with related customer interactions"
- "Which customer segments generate highest billed hours?"

### Expected
- Better cross-entity reasoning
- Better multi-table relationship answers
- Strongest quality before adding advanced routing patterns

---

## Step 6 (Bonus): Add Multiple Data Sources, Apply Routing Best Practices, Retest

### Goal
Demonstrate that Fabric Data Agent can route questions across multiple sources reliably and improve performance.

### Hint
- Use Microsoft Learn routing guidance:
   [Improve data source routing - Microsoft Fabric | Microsoft Learn](https://learn.microsoft.com/en-us/fabric/data-science/data-agent-routing)
- Key sequence to follow:
   1. Tighten schema selection
   2. Add focused data source descriptions
   3. Add example queries (few-shot)
   4. Add concise routing rules in agent instructions
- Use `step6/step6_data_agent_configuration.json` as your starting template.

### Actions
1. Create the Step 6 additional data files (if not already generated):
   - Run: `python step6/generate_step6_data.py`
2. Upload these Step 6 files into Lakehouse tables:
   - `step6/step6_client_engagement_summary.csv`
   - `step6/step6_case_finance_insights.csv`
   - `step6/step6_solicitor_performance_mart.csv`
3. Add at least 4-5 data sources (for example):
    - Client/case portfolio source
    - Financial transactions source
    - Client engagement/interactions source
    - Cross-domain case-finance source for combined analysis
   - Solicitor performance source
4. For each source, select only required tables/columns (avoid noisy schema).
5. Write a short source description that explains exactly when to use it.
6. Add source-specific example questions that are clearly distinct.
7. Add concise routing rules in agent instructions grouped by topic.
8. Use `step6/step6_data_agent_configuration.json` as the routing template and adapt IDs/table names for your workspace.
9. In Fabric run steps, inspect which source the orchestrator selected and adjust schema/description/examples/rules if routing is wrong.

### Test
Run prompts that should route to different sources:
- "How many active customers do we have?" (client/case source)
- "How many unpaid invoices do we have?" (financial source)
- "How many client meetings happened in Q1?" (engagement source)
- "Which high-value open cases also have overdue invoices?" (cross-domain)
- "Which solicitors are in top performance tier?" (solicitor performance source)

### Expected
- More consistent source selection
- Better answers for ambiguous questions
- Improved multi-source query quality and stability

---

## Suggested Demo Flow (15 minutes)

1. Step 1 cleaned baseline: show initial quality
2. Step 2 config best practices: show improved consistency
3. Step 3 basic model: show structured but imperfect answers
4. Step 4 optimized model: show major jump
5. Bonus Step 5 ontology: show advanced reasoning
6. Bonus Step 6 multi-source routing: show reliable source selection and better cross-domain answers

---

## Quick Validation Checklist

- [ ] Step 1 cleaned tables loaded and agent baseline answers captured
- [ ] Step 2 data agent best-practice configuration applied and prompts rerun
- [ ] Step 3 basic semantic model published and connected
- [ ] Step 4 optimized model + Prep for AI configured
- [ ] Bonus Step 5 ontology mapped and agent retested
- [ ] Bonus Step 6 multiple data sources configured with routing best practices and retested
- [ ] Side-by-side comparison recorded for your demo

---

## Optional: Regenerate Data Locally

From repo root:

```powershell
python step1/generate_step1_data.py
python step6/generate_step6_data.py

```



