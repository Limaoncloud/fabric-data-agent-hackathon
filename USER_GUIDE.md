# Fabric Data Agent User Guide (Simple Step-by-Step)

This guide supports a three-hour, hands-on learning loop:

> Ask a question, observe the result, form a hypothesis, change one durable control, and retest.

The environment starts with Lakehouse data and a `LegalFirmOptimized` semantic model that has correct relationships, explicit measures, and descriptions, but intentionally has no synonyms, Prep for AI configuration, AI instructions, Verified Answers, or Data Agent. A deliberately weak `LegalFirmBasic` model is also deployed for optional side-by-side comparison; it is background only and not part of the core walkthrough.

Participants work through these stages:

1. Create an agent baseline from the predeployed Lakehouse
2. Configure the data agent with best practices and retest
3. Optimize the semantic model and retest
4. Bonus: Add ontology and retest
5. Bonus: Add multiple data sources with routing best practices and retest

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
| 0:20-1:00 | Configure the Lakehouse data agent with best practices and retest |
| 1:00-1:45 | Build the Optimized-model agent, then configure Prep for AI and Data Agent instructions |
| 1:45-2:30 | Add the Lakehouse as a second source and configure routing |
| 2:30-2:45 | Rerun baseline and unseen challenge questions |
| 2:45-3:00 | Team debrief: what helped, what did not, and why |

---

## Quick File Map

### Step 1 files (cleaned baseline)
- `step1/step1_cleaned_customers.csv`
- `step1/step1_cleaned_cases.csv`
- `step1/step1_cleaned_solicitors.csv`
- `step1/step1_cleaned_transactions.csv`
- `step1/step1_cleaned_interactions.csv`

### Semantic model and config files
- [Reusable deployment notebook](NB_Deploy_Data_Agent_Hackathon.ipynb)
- [UK Legal domain profile](config/domains/uk-legal.json)
- [Basic model reference](step3/README.md) (background only; not part of the participant walkthrough)
- [Optimized model facilitator reference](step4/README.md) (contains a complete solution path; do not distribute during the participant challenge)
- `step5/step5_ontology_definition.json`
- `step6/step6_data_agent_configuration.json`

### Lakehouse routing data files
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

## Step 1: Build A Lakehouse Baseline Agent, Test

### Goal
Create a baseline Data Agent using the `LegalFirmDemo` Lakehouse that the organizer notebook already deployed. Do not recreate the Lakehouse or upload files.

### Actions
1. Open the Fabric workspace containing the deployed hackathon items.
2. Select **+ New item**.
3. In **All items**, search for and select **Fabric data agent**.
4. Name it `LegalFirmLakehouseBaselineAgent`, then create it.
5. In the OneLake catalog, select the `LegalFirmDemo` Lakehouse and select **Add**.
6. In the left **Explorer**, expand `LegalFirmDemo` and make only these tables available to the AI:
   - `step1_cleaned_customers`
   - `step1_cleaned_cases`
   - `step1_cleaned_solicitors`
   - `step1_cleaned_transactions`
   - `step1_cleaned_interactions`
7. Leave the three tables beginning with `step6_` unselected in this baseline step.
8. Leave **Data agent instructions** and **Example queries** empty for the first test. This preserves an untuned baseline.
9. Start asking questions in the agent chat. Expand the generated steps or query when diagnosing an answer.

The agent can contain up to five data sources, but this baseline uses only one: `LegalFirmDemo`.

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

### Worked Example 1: Teach A Business Term With Instructions

1. Ask: **"How many open matters do we have?"**
2. Record the answer and inspect the generated SQL or agent steps.
3. If *matter* is not understood, open **Data agent instructions** and add one concise rule: `In legal terminology, matter and matters mean case and cases. Use step1_cleaned_cases.`
4. Ask the exact question again, then test: **"How many cases are currently open?"**
5. Record whether the generated SQL and answer improved.

Lakehouse tables do not have the semantic-model synonym editor. For Lakehouse sources, use Data Agent instructions, data-source descriptions, schema selection, and validated SQL example queries. You will add true model-object synonyms later in Step 4 with `LegalFirmOptimized`.

### Worked Example 2: Add A Lakehouse SQL Example Query

Participants are not expected to know the table schema or write their first SQL example from scratch. Add this non-challenge example together:

**Question:** How many payment transactions were recorded?

**Expected answer:** 199

```sql
SELECT COUNT(*) AS payment_transaction_count
FROM step1_cleaned_transactions
WHERE transaction_type = 'Payment';
```

1. In the Data Agent, select **Example queries**.
2. For the `LegalFirmDemo` Lakehouse source, select **Add or Edit Example Queries**.
3. Enter the question and SQL exactly as shown above.
4. Validate and save the example. Fabric only uses examples that pass validation.
5. Ask the question in chat and inspect the generated SQL and answer.
6. Test the paraphrase: **How many payments are in the transaction table?**
7. Confirm that both questions return `199`, then continue with the challenge questions without giving participants more SQL solutions.

This question is deliberately outside the six-question scored challenge. Data Agent example question/query pairs are supported for the Lakehouse source, but not for the `LegalFirmBasic` or `LegalFirmOptimized` Power BI semantic-model sources.

### Diagnostic Hints For The Remaining Questions

- Is the failure caused by model structure, naming, business terminology, source selection, or answer style?
- Did the generated SQL use the expected table, columns, filters, and aggregation?
- Is the term an alternative name that should be defined in Data Agent instructions?
- Would narrowing the selected Lakehouse tables or columns reduce ambiguity?
- Would a clearer Lakehouse source description help the agent choose this source?
- Would a validated SQL example demonstrate logic that instructions alone cannot express?
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

## Step 3: Optimize Semantic Model, Retest

### Goal
Compare a technically optimized model with and without participant-authored AI metadata.

### Hint
- You can use tools like a **Power BI Modeling MCP server** to help design a clean semantic model.
- You can also use any tools listed in Microsoft Learn here:
   [Semantic model best practices for data agent - Microsoft Fabric | Microsoft Learn](https://learn.microsoft.com/en-us/fabric/data-science/semantic-model-best-practices#tools)
- Facilitators may use the [Optimized model reference](step4/README.md) after the exercise; participants should diagnose and choose improvements without following the completed solution path.

### Actions
1. Create a new Data Agent using the predeployed `LegalFirmOptimized` model.
2. Run the unchanged baseline questions before adding AI-specific configuration.
3. Inspect the existing relationships, measures, names, and descriptions.

### Example Prompts, Including Two That Should Stumble
Ask these before making any AI configuration changes and record each answer plus the model object used:
- "How many active customers do we have?"
- "What is the total case value?"
- "How much money have we made?" — deliberately ambiguous; watch whether the agent uses Invoices only or every transaction type.
- "How many senior solicitors do we have?" — deliberately undefined; "senior" is not a model field or measure.

### Test
Run the same prompt set and compare with previous steps.

### Expected
- Significant quality jump
- Better business logic understanding
- More accurate and repeatable answers
- Evidence showing which specific changes affected behavior

### Configure Prep Data For AI
Open **LegalFirmOptimized → Model settings → Prep data for AI**. It has three controls; two get a full worked example below, one you diagnose yourself:
- **Table/column selection (AI Data Schema)** — scope which tables and columns the agent can see.
- **Synonyms** — teach alternate business words for existing model objects.
- **AI instructions** — teach business rules that no single field or measure already expresses.

A fourth control lives on the **Data Agent** item itself, separate from the semantic model: **Data Agent instructions**, which shapes source selection and answer style rather than model semantics.

#### Worked example 1: Verified answer from a report visual
1. Ask **"What is the total case value?"** and note the current answer and source.
2. From `LegalFirmOptimized`, select **Create report**, add a page named **Verified Answers**, and add a Card visual bound to the `[Total Case Value]` measure. Save the report.
3. In **Prep data for AI → Verified answers**, select **New verified answer**, enter the question, then select the saved report, page, and Card visual. Add a short description and save.
4. Ask the same question again in the agent chat and confirm it now answers from the verified visual instead of generating a new query.

#### Worked example 2: Tweak an AI instruction
1. Ask **"How many senior solicitors do we have?"** and record the result. The model has no field or measure for seniority, so the agent must guess or refuse.
2. In **Prep data for AI → AI instructions**, add one concise rule: `Senior solicitor means hourly_rate_gbp greater than 300.`
3. Ask the same question again, then test the paraphrase **"How many solicitors charge a high hourly rate?"**
4. Record whether the answer and generated filter now match the rule, and note this was a business-rule gap, not a naming gap.

#### Two more examples of the same method: synonyms and Data Agent instructions

We won't spoon-feed every control. These two examples show how to analyse a failure and pick the right place to fix it, so you can apply the same method to table/column selection.

**Example A — synonym.** Ask: **How many open matters do we have?**
1. Record the answer and which model object the agent appears to use.
2. Decide whether *matter* describes a new business rule or another name for an existing concept.
3. In **Prep data for AI**, add `matter` and `matters` as synonyms for the `Cases` table. This synonym control is available because Step 3 uses a Power BI semantic model, not a Lakehouse source.
4. Ask the same question again, then test: **How many matters are currently open?**
5. Record what changed and what evidence supports your conclusion.

**Example B — Data Agent instruction.** Ask: **What is our average case value?**
1. Check the number formatting in the answer.
2. Open the Data Agent item (not the semantic model) and add one **Data Agent instruction**: `Present all monetary answers in GBP with two decimal places.`
3. Retest the same question and confirm the answer style changed without changing the underlying measure.
4. Decide yourself whether a similar answer-style or source-preference rule belongs here rather than in the semantic model's AI instructions.

Now apply the same analyse → pick the control → change one thing → retest method to **table/column selection**: find a question where the agent uses an irrelevant or hidden column, narrow the AI Data Schema to the business-facing fields and measures only, and retest.

#### Your questions

Do not change several controls at once. For each question, capture the baseline, form a hypothesis, make one change, and retest the question plus its paraphrase. Keep going until you consider the agent AI-ready.

| Question | Paraphrase | Hint |
| --- | --- | --- |
| How many active clients do we have? | What is our current active customer count? | Is every business term represented in the model language? |
| What is the total value of all matters? | What is our complete case portfolio worth? | Did the agent select an explicit measure or aggregate a field itself? |
| How much revenue have we generated? | What is the total amount invoiced? | Could revenue mean invoices, payments, or all transactions? |
| How many invoices remain unpaid? | What is our unpaid invoice count? | Does an existing measure already match the intent? |
| How many legal cases are currently open? | How many open matters are on our books? | Does behavior remain consistent when terminology changes? |
| How many customers do we have? | What is our total client count? | If this fails, inspect scope and grounding before adding instructions. |

#### Results worksheet

| Question | Baseline answer | Hypothesis | One change made | Retest answer | Paraphrase result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| 1 |  |  |  |  |  |  |
| 2 |  |  |  |  |  |  |
| 3 |  |  |  |  |  |  |
| 4 |  |  |  |  |  |  |
| 5 |  |  |  |  |  |  |
| 6 |  |  |  |  |  |  |

Facilitators should use [evaluation/FACILITATOR_GUIDE.md](evaluation/FACILITATOR_GUIDE.md) only after teams record their own diagnoses.

### Two Questions That Will Still Stumble
Ask these once your AI configuration is otherwise stable:
- "Which customers are in the low engagement segment?"
- "Which solicitors are in the top performance tier?"

Both should stumble or be refused. `LegalFirmOptimized` has no engagement-segment or performance-tier classification at any grain; that derived, row-level context only exists in the Lakehouse tables added in Step 5. This is the motivation for Step 5.

---

## Step 4 (Bonus): Add Ontology Data, Retest

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

## Step 5 (Bonus): Route Between The Optimized Model And Lakehouse Tables

### Goal
Create one Data Agent with two complementary sources and teach it when to use each:

1. `LegalFirmOptimized` for standard customer, case, solicitor, transaction, and interaction questions backed by model relationships and measures.
2. `LegalFirmDemo` for questions that require the three prepared Lakehouse analysis tables.

### Actions: Add The Sources First
1. Select **+ New item → Fabric data agent**.
2. Name it `LegalFirmRoutingAgent`.
3. Add the `LegalFirmOptimized` Power BI semantic model as the first source and make all five model tables available: `Customers`, `Cases`, `Solicitors`, `Transactions`, and `Interactions`.
4. Add the `LegalFirmDemo` Lakehouse as the second source and make only these three tables available:
   - `step6_client_engagement_summary`
   - `step6_case_finance_insights`
   - `step6_solicitor_performance_mart`
5. Leave the five `step1_cleaned_*` Lakehouse tables unselected. Their standard business questions are already covered by `LegalFirmOptimized`.
6. Leave descriptions, instructions, and example queries empty for now.

### Ask A Few Questions Before Configuring Anything
- "Which customers are in the low engagement segment?"
- "Which high-value open cases have outstanding balances?"
- "Which solicitors are in the top performance tier?"

Record the answer, the source selected, and whether routing was correct or ambiguous. With two unscoped sources available, expect inconsistent or unexplained source selection.

### Read The Routing Best Practices
[Improve data source routing - Microsoft Fabric | Microsoft Learn](https://learn.microsoft.com/en-us/fabric/data-science/data-agent-routing)

Remember that SQL example question/query pairs can be added to the Lakehouse source, but not to the Power BI semantic-model source.

### Worked Example 1: Source Description And SQL Example

**`LegalFirmOptimized` description:**
> Use for standard customer, case, solicitor, transaction, and interaction questions. Prefer its explicit measures for customer counts, case counts and values, revenue, payments, expenses, billed hours, and unpaid invoices.

**`step6_client_engagement_summary` description (on `LegalFirmDemo`):**
> Use only for engagement segment questions. This table is already prepared at customer grain with `engagement_segment`, `total_interactions`, and `last_interaction_date`.

Add and validate this SQL example for `step6_client_engagement_summary`:

```sql
SELECT customer_id, customer_name, total_interactions, last_interaction_date
FROM step6_client_engagement_summary
WHERE engagement_segment = 'Low Engagement'
ORDER BY customer_name;
```

Ask **"Which customers are in the low engagement segment?"** again and confirm it now routes to `LegalFirmDemo` and uses this table.

### Worked Example 2: Data Agent Instruction

Add this concise **Data agent instruction** at the Data Agent level:

```text
Use LegalFirmOptimized for ordinary customer, case, solicitor, transaction,
and interaction questions that can be answered by model fields or measures.

Use LegalFirmDemo only when the question asks about engagement segments,
combined case-finance outcomes, payment risk, outstanding balances by case,
or solicitor performance tiers.

Prefer one source when the question is clear. Do not combine sources unless
the requested result cannot be answered by one selected source.
```

Retest the same question plus a paraphrase and record whether the instruction, not just the example, influenced the routing decision.

### Now Do The Rest Yourself

Using the same method, write your own description and one validated SQL example for:
- `step6_case_finance_insights` (case-level financial outcome and payment-risk questions)
- `step6_solicitor_performance_mart` (solicitor ranking and performance-tier questions)

Retest the two remaining questions from the baseline set above after each change.

### Diagnose Incorrect Routing

If a question routes incorrectly, change one control and retest:

1. Confirm only the intended objects are selected for each source.
2. Make the two source descriptions more distinct rather than longer.
3. Check that the Data Agent instruction names the correct source and topic.
4. For a Lakehouse question, add or correct one validated SQL example pair.
5. Clear the chat and test both the original question and a paraphrase.

### Evaluate Your Routing

Use this table to check whether your configuration routes each question to the intended source and object.

| Question | Expected source | Expected object | Why |
| --- | --- | --- | --- |
| How many active customers do we have? | `LegalFirmOptimized` | `[Active Customers]` | Standard model measure |
| What is our total revenue? | `LegalFirmOptimized` | `[Total Revenue]` | Standard financial measure |
| Which customers are in the low engagement segment? | `LegalFirmDemo` | `step6_client_engagement_summary` | Prepared engagement classification |
| Which high-value open cases have outstanding balances? | `LegalFirmDemo` | `step6_case_finance_insights` | Combined case and financial outcome |
| Which solicitors are in the top performance tier? | `LegalFirmDemo` | `step6_solicitor_performance_mart` | Prepared solicitor tier |

### Expected
- Standard metrics route to `LegalFirmOptimized`.
- Engagement, case-finance, risk, and performance-tier questions route to the selected `step6_*` Lakehouse tables.
- Participants can explain which source was selected and which configuration influenced the routing decision.

---

## Suggested Demo Flow (15 minutes)

1. Step 1 cleaned baseline: show initial quality
2. Step 2 config best practices: show improved consistency
3. Step 3 optimized model: show the before/after effect of participant AI tuning
4. Bonus Step 4 ontology: show advanced reasoning
5. Bonus Step 5 multi-source routing: show reliable source selection and better cross-domain answers

---

## Quick Validation Checklist

- [ ] Step 1 cleaned tables loaded and agent baseline answers captured
- [ ] Step 2 data agent best-practice configuration applied and prompts rerun
- [ ] Step 3 optimized model tested before and after selected participant-authored AI improvements
- [ ] Bonus Step 4 ontology mapped and agent retested
- [ ] Bonus Step 5 agent configured with `LegalFirmOptimized` plus the three selected `step6_*` Lakehouse tables and routing retested
- [ ] Side-by-side comparison recorded for your demo

---

## Evaluate Your Agent

Use [NB_Evaluate_Data_Agent_Hackathon.ipynb](NB_Evaluate_Data_Agent_Hackathon.ipynb) after completing the six-question Agent Testing Challenge.

1. Import the evaluation notebook into the Fabric workspace.
2. In the Data Agent chat, ask each original question and its paraphrase.
3. Record the baseline and final answers and the Fabric item selected as the source.
4. Expand the run steps and inspect the generated SQL or DAX. Mark the logic `True` only when the table or measure, filters, and aggregation are correct.
5. Enter those observations in the notebook's **Enter Test Results** cell.
6. Run all cells. Fix any actionable validation errors.
7. Review the per-question scorecard and the baseline and final totals out of 24.
8. Submit the exported CSV and JSON together with screenshots or copied query evidence.

The notebook performs deterministic scoring from participant-entered observations; it does not call the live Data Agent API. Facilitators can use the SDK workflow in [evaluation/EVALUATION_GUIDE.md](evaluation/EVALUATION_GUIDE.md) for independent automated runs after the event.

---

## Optional: Regenerate Data Locally

From repo root:

```powershell
python step1/generate_step1_data.py
python step6/generate_step6_data.py

```



