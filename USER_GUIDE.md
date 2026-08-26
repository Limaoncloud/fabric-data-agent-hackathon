# Fabric Data Agent User Guide (Simple Step-by-Step)

This guide supports a three-hour, hands-on learning loop:

> Ask a question, observe the result, form a hypothesis, change one durable control, and retest.

The environment starts with Lakehouse data and two semantic models. `LegalFirmBasic` is deliberately weak. `LegalFirmOptimized` has correct relationships, explicit measures, and descriptions, but intentionally has no synonyms, Prep for AI configuration, AI instructions, Verified Answers, or Data Agent.

Participants work through these stages:

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
- Power BI Desktop or Fabric report authoring only if configuring Verified Answers
- Files already in this repo

## Automated Deployment (Recommended)

1. Import `NB_Deploy_Data_Agent_Hackathon.ipynb` into the target Fabric workspace.
2. Leave `WORKSPACE_ID=""` to use the notebook's current workspace.
3. Leave `DOMAIN_PROFILE="uk-legal"` for the default scenario.
4. Keep `ENABLE_PREP_FOR_AI=False`, `ENABLE_DATA_AGENT=False`, and the preview stages disabled.
5. Run all cells to create the participant-ready Lakehouse and both Direct Lake semantic models.
6. Review the deployment summary, then begin the participant exercises in Fabric.

See [deployment/README.md](deployment/README.md) for parameters and custom-domain packaging.

## Suggested Three-Hour Schedule

| Time | Activity |
| --- | --- |
| 0:00-0:20 | Scenario, Data Agent creation, and baseline questions |
| 0:20-1:00 | Diagnose the Basic model and record failure types |
| 1:00-1:30 | Compare the same questions against the Optimized model |
| 1:30-2:20 | Add selected synonyms, Prep for AI, and agent instructions one change at a time |
| 2:20-2:45 | Rerun baseline and unseen challenge questions |
| 2:45-3:00 | Team debrief: what helped, what did not, and why |

---

## Quick File Map

### Step 1 files (cleaned baseline)
- `step1/step1_cleaned_customers.csv`
- `step1/step1_cleaned_cases.csv`
- `step1/step1_cleaned_solicitors.csv`
- `step1/step1_cleaned_transactions.csv`
- `step1/step1_cleaned_interactions.csv`

### Step 3 to 6 model/config files
- [Reusable deployment notebook](NB_Deploy_Data_Agent_Hackathon.ipynb)
- [UK Legal domain profile](config/domains/uk-legal.json)
- [Step 3: LegalFirmBasic Direct Lake instructions](step3/README.md) (manual Power BI Service build guide)
- [Step 4 facilitator reference](step4/README.md) (contains a complete solution path; do not distribute during the participant challenge)
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
- "Find count of customers with no interactions in the last 60 days but with unpaid invoices over 10000."
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

### One Worked Example

1. Ask: **"How many open matters do we have?"**
2. Record the answer and which model object the agent appears to use.
3. If the legal term *matter* is not understood, add one relevant synonym rather than changing several controls at once.
4. Ask the exact question again, then test a paraphrase.
5. Record whether the change helped and what evidence supports that conclusion.

### Diagnostic Hints For The Remaining Questions

- Is the failure caused by model structure, naming, business terminology, source selection, or answer style?
- Does the requested metric already exist as an explicit measure?
- Is the term an alternative name, or does it encode a business rule?
- Would narrowing the AI Data Schema reduce ambiguity?
- Should the guidance live in the semantic model, Prep for AI, or Data Agent instructions?
- Is the question stable and important enough to justify a Verified Answer?
- Can you test the hypothesis by changing only one control?

### Test
Run the same 7 prompts from Step 1 and compare quality.

Add 3 to 5 complex prompts from the challenge set and compare:
- consistency of terminology mapping
- correctness of filter logic
- clarity of assumptions in responses

Use the facilitator-provided evaluation results only after recording your own answer and diagnosis.

### Expected
- Better consistency
- Improved grounding and answer relevance
- Clearer and more repeatable answers

---

## Step 3: Build Basic Semantic Model, Retest

### Goal
Create a new Data Agent that uses a basic semantic model (non-optimized) as its data source, then observe behavior.

### Actions
1. For manual creation in **Power BI Service**, follow the [Step 3 Direct Lake instructions](step3/README.md).
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
Compare a technically optimized model with and without participant-authored AI metadata.

### Hint
- You can use tools like a **Power BI Modeling MCP server** to help design a clean semantic model.
- You can also use any tools listed in Microsoft Learn here:
   [Semantic model best practices for data agent - Microsoft Fabric | Microsoft Learn](https://learn.microsoft.com/en-us/fabric/data-science/semantic-model-best-practices#tools)
- Facilitators may use the [Step 4 reference](step4/README.md) after the exercise; participants should diagnose and choose improvements without following the completed solution path.

### Actions
1. Create a new Data Agent using the predeployed `LegalFirmOptimized` model.
2. Run the unchanged baseline questions before adding AI-specific configuration.
3. Inspect the existing relationships, measures, names, and descriptions.
4. Choose one observed failure and improve one control: synonym, AI Data Schema scope, AI instruction, example prompt, source description, or agent instruction.
5. Retest the same question and a paraphrase before making another change.
6. Add a Verified Answer only when a stable, high-value question warrants a saved visual response.

### Test
Run the same prompt set and compare with previous steps.

### Expected
- Significant quality jump
- Better business logic understanding
- More accurate and repeatable answers
- Evidence showing which specific changes affected behavior

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
4. Step 4 optimized model: show the before/after effect of participant AI tuning
5. Bonus Step 5 ontology: show advanced reasoning
6. Bonus Step 6 multi-source routing: show reliable source selection and better cross-domain answers

---

## Quick Validation Checklist

- [ ] Step 1 cleaned tables loaded and agent baseline answers captured
- [ ] Step 2 data agent best-practice configuration applied and prompts rerun
- [ ] Step 3 basic semantic model published and connected
- [ ] Step 4 optimized model tested before and after selected participant-authored AI improvements
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



