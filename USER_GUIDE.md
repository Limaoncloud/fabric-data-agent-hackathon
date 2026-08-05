# Fabric Data Agent User Guide (Simple Step-by-Step)

This guide walks you through **Steps 1 to 6** in a simple flow:

1. Load raw data and create an agent
2. Clean data and retest
3. Build a semantic model and retest
4. Optimize the semantic model and retest
5. Add ontology and retest
6. Add multiple data sources with routing best practices and retest

---

## Prerequisites

- Microsoft Fabric workspace with enough capacity
- Access to create Lakehouse, Semantic Model, and Data Agent
- Power BI Desktop (for semantic model steps)
- Files already in this repo

---

## Quick File Map

### Step 1 files
- `step1/step1_raw_customers.csv`
- `step1/step1_raw_cases.csv`
- `step1/step1_raw_solicitors.csv`
- `step1/step1_raw_transactions.csv`
- `step1/step1_raw_interactions.csv`

### Step 2 files
- `step2/step2_cleaned_customers.csv`
- `step2/step2_cleaned_cases.csv`
- `step2/step2_cleaned_solicitors.csv`
- `step2/step2_cleaned_transactions.csv`
- `step2/step2_cleaned_interactions.csv`

### Step 3 to 6 model/config files
- `step3/step3_basic_semantic_model.json`
- `step4/step4_optimized_semantic_model.json`
- `step5/step5_ontology_definition.json`
- `step6/step6_data_agent_configuration.json`

### Step 6 additional data files
- `step6/step6_client_engagement_summary.csv`
- `step6/step6_case_finance_insights.csv`
- `step6/step6_solicitor_performance_mart.csv`
- `step6/generate_step6_data.py`

### Test prompts
- `TEST_QUERIES.md`

---

## Step 1: Upload Raw Data, Build Agent, Test

### Goal
Create a baseline agent on raw data and observe weak results.

### Actions
1. In Fabric, create a new Lakehouse (example name: `LegalFirmDemo`).
2. Upload all 5 raw CSV files from `step1/`.
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

### Expected
- Inconsistent answers
- Wrong filters/aggregation in some queries
- This is your baseline quality

---

## Step 2: Clean Data, Repoint Agent, Retest

### Goal
Use cleaned data to improve consistency.

### Actions
1. Choose one cleaning approach:
   - Use a Fabric Notebook to clean Step 1 raw tables.
   - Ask GitHub Copilot to generate or refine cleaning logic.
   - Manually clean the raw CSV files.
   - Use the already cleaned files in `step2/`.
2. If you choose Notebook/Copilot/manual cleaning, make sure output schema matches Step 2 files:
   - `step2_cleaned_customers.csv`
   - `step2_cleaned_cases.csv`
   - `step2_cleaned_solicitors.csv`
   - `step2_cleaned_transactions.csv`
   - `step2_cleaned_interactions.csv`
3. Upload the cleaned files to the same or a new Lakehouse and load each file to a table.
4. Update your Data Agent to use cleaned tables instead of raw tables.
5. Keep the same test prompts.

### Test
Run the same 5 prompts from Step 1.

### Expected
- Better consistency
- Fewer obvious errors
- Still not perfect for business logic

---

## Step 3: Build Basic Semantic Model, Retest

### Goal
Add a semantic model (basic, non-optimized) and see behavior.

### Actions
1. Choose one option:
   - Manually create a basic semantic model in Power BI Desktop.
   - Use the already built raw semantic model file: `step3/step3_basic_semantic_model.json`.
2. If creating manually, connect to cleaned Lakehouse tables and build a basic model (minimal relationships, basic measures).
3. Publish the semantic model to your Fabric workspace.
4. Configure the agent to use this semantic model.
5. Keep test prompts unchanged.

### Test
Run the same prompts plus:
- "Show case value by case type"
- "Show top 5 customers by total case value"

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
- A ready optimized model exists in the repo at `step4/step4_optimized_semantic_model.json`, but it is recommended to try building/optimizing your own model first.

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

## Step 5: Add Ontology Data, Retest

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

## Step 6: Add Multiple Data Sources, Apply Routing Best Practices, Retest

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

1. Step 1 baseline (raw): show weak answers
2. Step 2 cleaned: show moderate improvement
3. Step 3 basic model: show structured but imperfect answers
4. Step 4 optimized model: show major jump
5. Step 5 ontology: show advanced reasoning
6. Step 6 multi-source routing: show reliable source selection and better cross-domain answers

---

## Quick Validation Checklist

- [ ] Step 1 raw tables loaded and agent answers captured
- [ ] Step 2 cleaned tables loaded and same prompts rerun
- [ ] Step 3 basic semantic model published and connected
- [ ] Step 4 optimized model + Prep for AI configured
- [ ] Step 5 ontology mapped and agent retested
- [ ] Step 6 multiple data sources configured with routing best practices and retested
- [ ] Side-by-side comparison recorded for your demo

---

## Optional: Regenerate Data Locally

From repo root:

```powershell
python step1/generate_step1_data.py
python step2/generate_step2_data.py
python step6/generate_step6_data.py
```
