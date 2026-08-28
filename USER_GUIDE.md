# Fabric Data Agent User Guide (Simple Step-by-Step)

This guide supports a three-hour, hands-on learning loop:

> Ask a question, observe the result, form a hypothesis, change one durable control, and retest.

The environment starts with Lakehouse data and a `LegalFirmSemanticModel` semantic model that has correct relationships, explicit measures, and descriptions, but intentionally has no synonyms, Prep for AI configuration, AI instructions, Verified Answers, or Data Agent.

You build one Data Agent and grow it step by step: first the semantic model, then the Lakehouse attached to that same agent as a second source. Each step is a continuation of the same agent, not a new one.

Participants work through these stages:

1. Build a Data Agent on the Optimized semantic model and retest
2. Configure the semantic-model agent with Prep for AI and retest
3. Attach the Lakehouse to the same agent and retest
4. Configure the Lakehouse source with best practices and retest
5. Add the derived Lakehouse tables and configure routing, retest
6. Bonus: Add ontology and retest

---

## Prerequisites

- Microsoft Fabric workspace with enough capacity
- Access to create Lakehouse, Semantic Model, and Data Agent
- Power BI Desktop or Fabric report authoring only if configuring Verified Answers
- Files already in this repo

## Automated Deployment (Recommended)

### Import The Deployment Notebook Into Fabric

New to Fabric? Follow these steps exactly:

1. Download the deployment notebook from this repo: [NB_Deploy_Data_Agent_Hackathon.ipynb](https://github.com/Limaoncloud/fabric-data-agent-hackathon/blob/dev/NB_Deploy_Data_Agent_Hackathon.ipynb). On the GitHub page, use **Download raw file** to save the `.ipynb` file to your computer.
2. Open Microsoft Fabric at [https://app.fabric.microsoft.com](https://app.fabric.microsoft.com).
3. Open the target workspace.
4. Select **Import → Notebook**, then upload the `.ipynb` file you downloaded.
5. Open the imported notebook once it appears in the workspace.
6. Leave `WORKSPACE_ID=""` and `DOMAIN_PROFILE="uk-legal"` for the default run.
7. Run all cells.

### Before You Run

- Keep `ENABLE_PREP_FOR_AI=False`, `ENABLE_DATA_AGENT=False`, and the preview stages disabled for a participant-ready deployment.
- Running all cells creates the participant-ready Lakehouse and the Optimized Direct Lake semantic model.
- Review the deployment summary printed at the end, then begin the participant exercises in Fabric.

See [deployment/README.md](deployment/README.md) for parameters and custom-domain packaging.

## Suggested Three-Hour Schedule

| Time | Activity |
| --- | --- |
| 0:00-0:20 | Scenario and Data Agent creation on the Optimized semantic model |
| 0:20-1:00 | Configure Prep for AI and Data Agent instructions, then retest |
| 1:00-1:30 | Attach the Lakehouse to the same agent and capture the two-source baseline |
| 1:30-2:00 | Configure the Lakehouse source with best practices and retest |
| 2:00-2:30 | Add the derived Lakehouse tables and configure routing |
| 2:30-2:45 | Bonus ontology or rerun unseen challenge questions |
| 2:45-3:00 | Team debrief: what helped, what did not, and why |

---

## Quick File Map

### Cleaned baseline data files
- `sample-data/uk-legal/base/customers.csv`
- `sample-data/uk-legal/base/cases.csv`
- `sample-data/uk-legal/base/solicitors.csv`
- `sample-data/uk-legal/base/transactions.csv`
- `sample-data/uk-legal/base/interactions.csv`

### Semantic model and config files
- [Reusable deployment notebook](NB_Deploy_Data_Agent_Hackathon.ipynb)
- [UK Legal domain profile](config/domains/uk-legal.json)
- [Optimized model facilitator reference](semantic-model/optimized/uk-legal/README.md) (contains a complete solution path; do not distribute during the participant challenge)
- `ontology/uk-legal/ontology-definition.json`
- `agent-configuration/routing/uk-legal/data-agent-configuration.json`

### Lakehouse routing data files
- `sample-data/uk-legal/derived-routing/client_engagement_summary.csv`
- `sample-data/uk-legal/derived-routing/case_finance_insights.csv`
- `sample-data/uk-legal/derived-routing/solicitor_performance_mart.csv`
- `sample-data/uk-legal/derived-routing/generate_derived_routing_data.py`

### Test prompts
- `evaluation/FACILITATOR_GUIDE.md`
- `evaluation/challenge/uk-legal.json`
- `evaluation/routing/uk-legal.json`

### Verification reference
- `Verification.xlsx` (use this workbook to validate expected answers and compare results for each step)

Validation workflow:
1. Run the test prompts for the current step.
2. Record the agent output.
3. Compare with the expected result for that step in `Verification.xlsx`.
4. Mark pass/fail and note any mismatch before moving to the next step.

---

## Step 1: Build A Data Agent With The Optimized Semantic Model, Test

### Goal
Create the one Data Agent you will keep extending through every later step, starting with the predeployed `LegalFirmSemanticModel` semantic model as its first source.

### Actions
1. Open the Fabric workspace containing the deployed hackathon items.
2. Select **+ New item → Fabric data agent**.
3. Name it `LegalFirmAgent`. You will attach the Lakehouse to this same agent later; do not create a second agent.
4. In the OneLake catalog, select the `LegalFirmSemanticModel` semantic model and select **Add**.
5. In the Explorer, make all five model tables available: `Customers`, `Cases`, `Solicitors`, `Transactions`, and `Interactions`.
6. Leave **Data agent instructions** and `LegalFirmSemanticModel`'s **Prep data for AI** settings unconfigured for the first test.

### Example Prompts, Including Two That Should Stumble
Ask these before making any AI configuration changes and record each answer plus the model object used:
- "How many active customers do we have?"
- "What is the total case value?"
- "How much money have we made?" — deliberately ambiguous; watch whether the agent uses Invoices only or every transaction type.
- "How many senior solicitors do we have?" — deliberately undefined; "senior" is not a model field or measure.

### Test
Run the prompts above in the agent chat.

### Expected
- Reasonable answers from the model's relationships and explicit measures
- No AI-specific tuning yet, so business terms and undefined thresholds can still fail
- This is your semantic-model baseline before Step 2

---

## Step 2: Configure The Semantic-Model Agent With Prep For AI, Retest

### Goal
Improve the same `LegalFirmAgent` by configuring `LegalFirmSemanticModel`'s Prep for AI settings and the agent's own instructions, then measure the effect.

### Hint
- You can use tools like a **Power BI Modeling MCP server** to help design a clean semantic model.
- You can also use any tools listed in Microsoft Learn here:
   [Semantic model best practices for data agent - Microsoft Fabric | Microsoft Learn](https://learn.microsoft.com/en-us/fabric/data-science/semantic-model-best-practices#tools)
- Facilitators may use the [Optimized model reference](semantic-model/optimized/uk-legal/README.md) after the exercise; participants should diagnose and choose improvements without following the completed solution path.

### Configure Prep Data For AI
Open **LegalFirmSemanticModel → Model settings → Prep data for AI**. It has three controls; two get a full worked example below, one you diagnose yourself:
- **Table/column selection (AI Data Schema)** — scope which tables and columns the agent can see.
- **Synonyms** — teach alternate business words for existing model objects.
- **AI instructions** — teach business rules that no single field or measure already expresses.

A fourth control lives on the **Data Agent** item itself, separate from the semantic model: **Data Agent instructions**, which shapes source selection and answer style rather than model semantics.

#### Worked example 1: Verified answer from a report visual
1. Ask **"What is the total case value?"** and note the current answer and source.
2. From `LegalFirmSemanticModel`, select **Create report**, add a page named **Verified Answers**, and add a Card visual bound to the `[Total Case Value]` measure. Save the report.
3. Select the Card visual, open its **...** menu, choose **Add to Q&A**, enter the question, and turn on **Verified answer**. The verified answer is pinned on the visual in the report, not in Prep data for AI.
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
3. In **Prep data for AI**, add `matter` and `matters` as synonyms for the `Cases` table. This synonym control is available on the `LegalFirmSemanticModel` Power BI semantic-model source.
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

### Test
Run the same prompt set from Step 1 and compare.

### Expected
- Significant quality jump over the Step 1 baseline
- Better business logic understanding
- More accurate and repeatable answers
- Evidence showing which specific changes affected behavior

### Two Questions That Will Still Stumble
Ask these once your AI configuration is otherwise stable:
- "Which customers are in the low engagement segment?"
- "Which solicitors are in the top performance tier?"

Both should stumble or be refused. `LegalFirmSemanticModel` has no engagement-segment or performance-tier classification at any grain; that derived, row-level context does not exist anywhere yet. This is the motivation for attaching the Lakehouse in Step 3.

---

## Step 3: Attach The Lakehouse To The Same Agent, Retest

### Goal
Continue building the same `LegalFirmAgent`: give it one Data Agent with two complementary sources by adding the `LegalFirmDemo` Lakehouse alongside `LegalFirmSemanticModel`, then observe how it behaves before any Lakehouse-specific tuning.

### Actions
1. Open the existing `LegalFirmAgent` Data Agent. Do not create a new agent.
2. Add the `LegalFirmDemo` Lakehouse as a second source and select **Add**.
3. In the left **Explorer**, expand `LegalFirmDemo` and make only these tables available to the AI:
   - `base_customers`
   - `base_cases`
   - `base_solicitors`
   - `base_transactions`
   - `base_interactions`
4. Leave the three tables beginning with `step6_` unselected; you will add them in Step 5.
5. Leave the Lakehouse source's description and example queries empty for now. Keep the Step 2 instructions on `LegalFirmSemanticModel` unchanged.

The agent can contain up to five data sources; it now has two.

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
- The agent now has two sources covering similar ground
- Without a Lakehouse description or examples, expect it to sometimes pick the wrong source, hesitate, or duplicate logic the semantic model already answers correctly
- This is your two-source baseline before you apply Lakehouse best practices in Step 4

---

## Step 4: Configure The Lakehouse Source With Best Practices, Retest

### Goal
Improve response consistency by configuring the `LegalFirmDemo` Lakehouse source on the same agent using Microsoft best practices, without changing `LegalFirmSemanticModel`.

### Hint
- Follow Microsoft Learn guidance:
  [Best practices for configuring your data agent - Microsoft Fabric | Microsoft Learn](https://learn.microsoft.com/en-us/fabric/data-science/data-agent-configuration-best-practices)

### Actions
1. Keep the same five `base_*` tables selected on `LegalFirmDemo`.
2. Improve data source scope and schema selection (include only relevant tables/columns).
3. Write a clear and concise description for the `LegalFirmDemo` source.
4. Add focused example queries that represent real user intent.
5. Extend the Data Agent instructions to say when the Lakehouse should be preferred over the semantic model.
6. Keep data unchanged and rerun the same prompt set.

### Worked Example 1: Teach A Business Term With Instructions

1. Ask: **"How many open matters do we have?"**
2. Record the answer and inspect the generated SQL or agent steps.
3. If *matter* is not understood for the Lakehouse path, open **Data agent instructions** and add one concise rule: `In legal terminology, matter and matters mean case and cases. Use base_cases.`
4. Ask the exact question again, then test: **"How many cases are currently open?"**
5. Record whether the generated SQL and answer improved, and which source it used.

Lakehouse tables do not have the semantic-model synonym editor. For Lakehouse sources, use Data Agent instructions, data-source descriptions, schema selection, and validated SQL example queries. You already added true model-object synonyms in Step 2 for `LegalFirmSemanticModel`.

### Worked Example 2: Add A Lakehouse SQL Example Query

Participants are not expected to know the table schema or write their first SQL example from scratch. Add this non-challenge example together:

**Question:** How many payment transactions were recorded?

**Expected answer:** 199

```sql
SELECT COUNT(*) AS payment_transaction_count
FROM base_transactions
WHERE transaction_type = 'Payment';
```

1. In the Data Agent, select **Example queries**.
2. For the `LegalFirmDemo` Lakehouse source, select **Add or Edit Example Queries**.
3. Enter the question and SQL exactly as shown above.
4. Validate and save the example. Fabric only uses examples that pass validation.
5. Ask the question in chat and inspect the generated SQL and answer.
6. Test the paraphrase: **How many payments are in the transaction table?**
7. Confirm that both questions return `199`, then continue with the challenge questions without giving participants more SQL solutions.

This question is deliberately outside the six-question scored challenge. Data Agent example question/query pairs are supported for the Lakehouse source, but not for the `LegalFirmSemanticModel` Power BI semantic-model source.

### Diagnostic Hints For The Remaining Questions

- Is the failure caused by model structure, naming, business terminology, source selection, or answer style?
- Did the generated SQL or DAX use the expected table or model object, columns, filters, and aggregation?
- Is the term an alternative name that should be defined in Data Agent instructions?
- Would narrowing the selected Lakehouse tables or columns reduce ambiguity?
- Would a clearer Lakehouse source description help the agent choose the right source?
- Would a validated SQL example demonstrate logic that instructions alone cannot express?
- Can you test the hypothesis by changing only one control?

### Test
Run the same 7 prompts from Step 3 and compare quality.

Add 3 to 5 complex prompts from the challenge set and compare:
- consistency of terminology mapping
- correctness of filter logic
- clarity of assumptions in responses
- which source the agent selected

Use the facilitator-provided evaluation results only after recording your own answer and diagnosis.

### Expected
- Better consistency between the two sources
- The agent reliably prefers `LegalFirmSemanticModel` for standard questions
- Clearer and more repeatable answers

---

## Step 5: Add The Derived Lakehouse Tables And Configure Routing, Retest

### Goal
Continue extending the same `LegalFirmAgent` with the three prepared Step 6 analysis tables on `LegalFirmDemo`, so it can also answer engagement, case-finance, and solicitor-performance questions that neither `LegalFirmSemanticModel` nor the raw `base_*` tables can.

### Actions: Add The Derived Tables
1. Open the existing `LegalFirmAgent` Data Agent and its `LegalFirmDemo` source.
2. In addition to the five `base_*` tables, make these three tables available:
   - `routing_client_engagement_summary`
   - `routing_case_finance_insights`
   - `routing_solicitor_performance_mart`
3. Leave their descriptions and example queries empty for now.

### Ask A Few Questions Before Configuring Anything
- "Which customers are in the low engagement segment?"
- "Which high-value open cases have outstanding balances?"
- "Which solicitors are in the top performance tier?"

Record the answer, the source selected, and whether routing was correct or ambiguous. With three Lakehouse table groups now unscoped, expect inconsistent or unexplained source selection.

### Read The Routing Best Practices
[Improve data source routing - Microsoft Fabric | Microsoft Learn](https://learn.microsoft.com/en-us/fabric/data-science/data-agent-routing)

Remember that SQL example question/query pairs can be added to the Lakehouse source, but not to the Power BI semantic-model source.

### Worked Example 1: Source Description And SQL Example

**`LegalFirmSemanticModel` description:**
> Use for standard customer, case, solicitor, transaction, and interaction questions. Prefer its explicit measures for customer counts, case counts and values, revenue, payments, expenses, billed hours, and unpaid invoices.

**`routing_client_engagement_summary` description (on `LegalFirmDemo`):**
> Use only for engagement segment questions. This table is already prepared at customer grain with `engagement_segment`, `total_interactions`, and `last_interaction_date`.

Add and validate this SQL example for `routing_client_engagement_summary`:

```sql
SELECT customer_id, customer_name, total_interactions, last_interaction_date
FROM routing_client_engagement_summary
WHERE engagement_segment = 'Low Engagement'
ORDER BY customer_name;
```

Ask **"Which customers are in the low engagement segment?"** again and confirm it now routes to `LegalFirmDemo` and uses this table.

### Worked Example 2: Data Agent Instruction

Update the **Data agent instruction** at the Data Agent level to cover all three areas of the now-continued agent:

```text
Prefer LegalFirmSemanticModel for standard customer, case, solicitor, transaction,
and interaction questions that can be answered by model fields or measures.

Only use the raw base_* Lakehouse tables if a question needs a specific
column or filter that the semantic model does not expose.

Use the routing_* Lakehouse tables only for engagement segments, combined
case-finance outcomes, payment risk, outstanding balances by case, or solicitor
performance tiers.

Do not combine sources unless the requested result cannot be answered by one
selected source.
```

Retest the same question plus a paraphrase and record whether the instruction, not just the example, influenced the routing decision.

### Now Do The Rest Yourself

Using the same method, write your own description and one validated SQL example for:
- `routing_case_finance_insights` (case-level financial outcome and payment-risk questions)
- `routing_solicitor_performance_mart` (solicitor ranking and performance-tier questions)

Retest the two remaining questions from the baseline set above after each change.

### Diagnose Incorrect Routing

If a question routes incorrectly, change one control and retest:

1. Confirm only the intended objects are selected for each source.
2. Make the source descriptions more distinct rather than longer.
3. Check that the Data Agent instruction names the correct source and topic for each question type.
4. For a Lakehouse question, add or correct one validated SQL example pair.
5. Clear the chat and test both the original question and a paraphrase.

### Evaluate Your Routing

Use this table to check whether your configuration routes each question to the intended source and object.

| Question | Expected source | Expected object | Why |
| --- | --- | --- | --- |
| How many active customers do we have? | `LegalFirmSemanticModel` | `[Active Customers]` | Standard model measure |
| What is our total revenue? | `LegalFirmSemanticModel` | `[Total Revenue]` | Standard financial measure |
| Which customers are in the low engagement segment? | `LegalFirmDemo` | `routing_client_engagement_summary` | Prepared engagement classification |
| Which high-value open cases have outstanding balances? | `LegalFirmDemo` | `routing_case_finance_insights` | Combined case and financial outcome |
| Which solicitors are in the top performance tier? | `LegalFirmDemo` | `routing_solicitor_performance_mart` | Prepared solicitor tier |

### Expected
- Standard metrics route to `LegalFirmSemanticModel`.
- Engagement, case-finance, risk, and performance-tier questions route to the selected `routing_*` Lakehouse tables.
- Participants can explain which source was selected and which configuration influenced the routing decision.

---

## Step 6 (Bonus): Add Ontology Data, Retest

### Goal
Add ontology layer for richer entity and relationship understanding.

### Actions
1. Create ontology from `ontology/uk-legal/ontology-definition.json` as reference.
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
- Strongest quality across the whole exercise

---

## Suggested Demo Flow (15 minutes)

1. Step 1 optimized-model baseline: show initial quality
2. Step 2 Prep for AI: show the before/after effect of participant AI tuning
3. Step 3 attach Lakehouse: show the two-source baseline and initial routing confusion
4. Step 4 Lakehouse best practices: show improved consistency
5. Step 5 derived tables and routing: show reliable source selection across all sources
6. Bonus Step 6 ontology: show advanced reasoning

---

## Quick Validation Checklist

- [ ] Step 1 semantic-model agent created and baseline answers captured
- [ ] Step 2 Prep for AI and Data Agent instructions applied and prompts rerun
- [ ] Step 3 Lakehouse attached to the same agent and two-source baseline captured
- [ ] Step 4 Lakehouse best-practice configuration applied and prompts rerun
- [ ] Step 5 derived `routing_*` tables added and routing retested
- [ ] Bonus Step 6 ontology mapped and agent retested
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
python sample-data/uk-legal/base/generate_base_data.py
python sample-data/uk-legal/derived-routing/generate_derived_routing_data.py

```



