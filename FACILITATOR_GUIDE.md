# Fabric Data Agent Facilitator Guide

Keep this guide separate from participant materials until teams have recorded their baseline answers and diagnoses.

## How To Use This Guide

1. Use [USER_GUIDE.md](USER_GUIDE.md) as the participant-facing workshop flow. Participants should test, diagnose, change one control, and retest.
2. Use this guide privately for expected answers, solution checkpoints, escalating hints, and debrief prompts.
3. Import both [NB_Deploy_Data_Agent_Hackathon.ipynb](NB_Deploy_Data_Agent_Hackathon.ipynb) and [NB_Run_SDK_Evaluation.ipynb](NB_Run_SDK_Evaluation.ipynb) into Fabric. Use the first to create or reset the environment and the second after every required workshop stage.
4. Keep [NB_Review_And_Score_Data_Agent.ipynb](NB_Review_And_Score_Data_Agent.ipynb) only as an optional facilitator tool when manual evidence scoring is needed; it is not part of the participant workflow.

The deployment notebook creates `LegalFirmDemo` and `LegalFirmSemanticModel`. Participants create and improve one `LegalFirmAgent`; they do not create a new agent at each step.

## Suggested Demo Flow (15 Minutes)

1. Show baseline quality on raw or cleaned tables.
2. Show semantic model uplift.
3. Show multi-source routing improvements across the Lakehouse and derived data.
4. Show optional ontology reasoning uplift.

## Facilitator Solution Checkpoints

These are reference outcomes, not a script to reveal to participants. Accept a different configuration when the team can demonstrate correct answers, durable behavior across paraphrases, and the expected source or measure.

### Step 1: Untuned Baseline

- Source: `LegalFirmSemanticModel` only.
- Leave Prep for AI instructions, synonyms, Verified Answers, and Data Agent instructions empty.
- Let participants complete the four exploratory Step 1 prompts.
- Before changing any Step 2 controls, run `NB_Run_SDK_Evaluation.ipynb` with `SNAPSHOT_NAME = "step1_baseline"` to capture all 16 challenge prompts.

### Step 2: Prep For AI And Agent Instructions

In `LegalFirmSemanticModel > Model settings > Prep data for AI`:

- Include business-facing identifiers, names, statuses, dates, values, transaction types, payment status, hours, and every measure from `_Measures`.
- Add `client`/`clients` as alternatives for customer/customers and `matter`/`matters` as alternatives for case/cases.
- Keep calculations in explicit measures when a suitable measure already exists.

Use these semantic-model AI instructions as the reference solution:

```text
This is a UK legal firm. Customers may be Individual or Corporate, and legal matters are stored as cases.

Revenue means Invoice transactions only, not Payments. Billed hours means hours_worked from Timesheet transactions. Outstanding means Invoices where payment_status is Unpaid. Active customers have status Active.

Always filter Transactions by transaction_type when calculating revenue, expenses, invoices, payments, or timesheets. Case values are in GBP. Dates use UK format. When asked for top, highest, most, or best, sort descending. Use the current calendar year unless the user explicitly requests the April-to-March fiscal year.

A high-value case is greater than GBP 100,000. A large customer has more than five cases. A senior solicitor has an hourly rate greater than GBP 300.
```

Use these initial Data Agent instructions while the semantic model is the only source:

```text
Use LegalFirmSemanticModel for business questions about customers, cases, solicitors, transactions, interactions, revenue, case value, billed hours, and outstanding invoices. Use an explicit semantic-model measure whenever one exists; do not recreate it from a raw column.

Treat matter and matters as alternatives for case and cases. Ask one concise clarifying question only when different interpretations would materially change the answer.

Present monetary values in GBP and dates in UK format. State important filters or time periods. Do not invent values, definitions, or legal conclusions, and do not present an answer as legal advice.
```

Checkpoint: **How many matters are currently open?** should return `180` using `[Open Cases]`. **How much revenue have we generated?** should return `GBP 5,420,217` using `[Total Revenue]`.

### Optional Verified Answers

Verified Answers are grounded in saved report visuals; do not paste raw DAX as an answer. Create a small report from `LegalFirmSemanticModel`, add Card visuals for stable measures, save it, and use each visual's **Add to Q&A** action with **Verified answer** enabled.

Recommended cards: `[Total Customers]`, `[Total Case Value]`, `[Open Cases]`, `[Total Revenue]`, and `[Outstanding Invoices]`.

### Steps 3-4: Add And Tune The Lakehouse Source

Add `LegalFirmDemo` to the same `LegalFirmAgent`. Initially select only the five `base_*` tables. Lakehouse sources use selected objects, descriptions, Data Agent instructions, and validated SQL examples; they do not use semantic-model synonyms.

Use this routing principle:

```text
Prefer LegalFirmSemanticModel for standard business metrics supported by model fields or explicit measures. Use LegalFirmDemo base_* tables for detailed row-level lookups, a field or filter not exposed by the model, or a calculation the model cannot answer. Prefer LegalFirmDemo for exact transaction_id, case_id, or interaction_id record lookups. Do not combine sources unless one source cannot answer the request.
```

Use the three non-scored identifier examples in [USER_GUIDE.md](USER_GUIDE.md#worked-example-2-add-lakehouse-sql-example-queries) to teach SQL example queries. Do not provide SQL for the eight scored challenge questions.

### Step 5: Prepared Tables And Multi-Source Routing

Deselect the five `base_*` tables used in Steps 3-4, then select only these tables on the existing `LegalFirmDemo` source:

- `routing_client_engagement_summary` for engagement segments and interaction recency.
- `routing_case_finance_insights` for combined case-finance outcomes, payment risk, and outstanding balances.
- `routing_solicitor_performance_mart` for solicitor rankings and performance tiers.

Extend the instructions with:

```text
Use routing_client_engagement_summary only for engagement segments and interaction recency. Use routing_case_finance_insights only for combined case-finance outcomes, payment risk, and outstanding balances by case. Use routing_solicitor_performance_mart only for solicitor rankings and performance tiers. Continue to prefer LegalFirmSemanticModel for standard measures. Prefer one source when the question is clear.
```

Expected routing checks:

| Test | Expected source | Expected object |
| --- | --- | --- |
| How many active customers do we have? | `LegalFirmSemanticModel` | `[Active Customers]` |
| What is our total revenue? | `LegalFirmSemanticModel` | `[Total Revenue]` |
| Which customers are in the low engagement segment? | `LegalFirmDemo` | `routing_client_engagement_summary` |
| Which high-value open cases have outstanding balances? | `LegalFirmDemo` | `routing_case_finance_insights` |
| Which solicitors are in the top performance tier? | `LegalFirmDemo` | `routing_solicitor_performance_mart` |

Clear the chat before routing checks and inspect the selected source plus generated DAX or SQL. A correct answer alone does not prove correct routing.

The detailed `base_*` identifier lookups are Steps 3-4 checks. They are not part of the final Step 5 routing state after those tables are deselected.

## Learning Objective

Participants should learn to choose the lowest durable layer for a fix:

1. Model structure and explicit measures.
2. Names, descriptions, and synonyms.
3. Prep for AI schema and instructions.
4. Data Agent source descriptions and instructions.
5. Verified Answers for stable, high-value questions.

The expected loop is: test, observe, form a hypothesis, change one control, retest, and test a paraphrase.

## Controls By Source Type

| Source | Available tuning controls for this exercise |
| --- | --- |
| Lakehouse | Selected tables/columns, source description, Data Agent instructions, validated SQL example queries |
| Power BI semantic model | Model names/descriptions, Prep for AI synonyms, AI Data Schema, AI instructions, Verified Answers, Data Agent instructions |

Do not tell participants to add synonyms to Lakehouse tables. Fabric exposes model-object synonyms through Prep for AI on Power BI semantic models. Data Agent example question/query pairs support Lakehouse SQL sources, but not Power BI semantic-model sources.

## Worked Example

In Step 4, demonstrate why detailed identifier lookups should route to the Lakehouse. Ask these three questions before and after tuning:

- **Find transaction TXN000001 and show all its available details.**
- **Show the detailed case record for CASE0001.**
- **Find interaction INT000001 and show all its available details.**

Add a concise Data Agent instruction that prefers `LegalFirmDemo` for detailed lookups by `transaction_id`, `case_id`, or `interaction_id`. Then add, validate, and save the three SQL example pairs from the participant guide under **Example queries** for `LegalFirmDemo`.

Confirm that each prompt routes to the appropriate `base_*` table, filters on the exact identifier, and returns every available column for the matching record. Stop after these examples; do not provide SQL for the eight scored questions.

Do not demonstrate additional fixes or query solutions.

## Answer Key

| ID | Question | Expected answer | Likely learning area |
| --- | --- | ---: | --- |
| HC001 | How many active clients do we have? | 101 | Legal terminology and measure selection |
| HC002 | What is the total value of all matters? | GBP 123,590,881 | Terminology and explicit measure selection |
| HC003 | How much revenue have we generated? | GBP 5,420,217 | Business definition of revenue |
| HC004 | How many invoices remain unpaid? | 54 | Existing measure discoverability |
| HC005 | How many legal cases are currently open? | 180 | Consistency across terminology |
| HC006 | How many customers do we have? | 171 | Basic grounding and schema scope |
| HC007 | Find count of customers with no interactions in the last 60 days but with unpaid invoices over 10000. | 35 | Cross-table and time-relative reasoning |
| HC008 | What was the firm's client satisfaction score for 2025? | Cannot answer from available data | Safe abstention for an unsupported metric |

Ground truths come from the checked-in Step 1 CSV files. The machine-readable set is `evaluation/challenge/uk-legal.json`.

## Escalating Hints

Give only one hint at a time.

### Level 1: Observe

- Which source, table, field, or measure did the agent use?
- Is the answer wrong, incomplete, or merely phrased poorly?
- Does the same failure occur for the paraphrase?

### Level 2: Classify

- Is this model structure, terminology, business logic, schema scope, source routing, or response style?
- Does an explicit measure already represent the requested metric?
- Is the unfamiliar phrase an alternative name or a new calculation rule?

### Level 3: Choose A Control

- Is this a semantic-model source where a synonym is available, or a Lakehouse source where instructions/descriptions are the relevant controls?
- Is the AI Data Schema too broad or missing a required object?
- Does the business rule belong in a measure description or AI instruction?
- Is the issue specific to one source and better placed in Data Agent source instructions?
- Is this question stable enough to justify a Verified Answer?

Never tell a team both the diagnosis and the exact control in the same hint.

## Suggested Interventions

These are not mandatory solutions. Accept alternatives when teams can explain and demonstrate the effect.

| ID | Candidate intervention | Evidence to request |
| --- | --- | --- |
| HC001 | On the semantic model, add `client` as a customer synonym or clarify terminology in AI instructions | Original and paraphrase both select Active Customers |
| HC002 | On the semantic model, add `matter` as a case synonym and expose Total Case Value | Agent uses the explicit measure for both phrasings |
| HC003 | State that revenue means Invoice amounts and use Total Revenue | Agent does not substitute payments or all transactions |
| HC004 | Improve visibility or description of Outstanding Invoices | Agent selects the existing measure consistently |
| HC005 | Compare case and matter terminology behavior | Both phrasings return 180 without contradictory assumptions |
| HC006 | Reduce schema ambiguity before adding instructions | Agent returns 171 from Total Customers |
| HC007 | Route to the prepared Lakehouse data and verify the grouped threshold and recency exclusion | Agent returns 35 with correct cross-table logic |
| HC008 | Reinforce that unsupported metrics must not be inferred or fabricated | Both phrasings state that satisfaction data is unavailable and run no source query |

## Debrief Questions

Ask each team to present:

- One failure they initially diagnosed incorrectly.
- One change that materially improved behavior.
- One change that did not help.
- Evidence that the improvement survives a paraphrase.
- Why the chosen configuration layer was more durable than an agent-only workaround.

## Final Unseen Questions

Use these after the eight-question exercise. Do not provide expected values until teams submit answers.

- What is our active client population?
- What is the firm’s entire matter portfolio worth?
- How much have we invoiced in total?
- How many invoices are still outstanding and unpaid?
- How many matters remain open?
- What is the total number of clients in the system?

For the seventh scored question, the expected answer is **35** as of the workshop dataset: count customers whose summed Invoice transactions with `payment_status = 'Unpaid'` exceed GBP 10,000 and who have no interaction in the 60 days before evaluation. Inspect the generated logic to confirm the threshold is applied after summing per customer and the recent-interaction test uses the evaluation date.

For the eighth scored question, the correct response is an explicit abstention: the configured data contains no client satisfaction metric or survey results. The agent must not infer a score from interaction counts, notes, or any other proxy. Record the selected source as `none` and retain run-step evidence that no source query was executed.

## Evaluation

Score each response on:

- Correct answer.
- Correct measure or field selection.
- Correct interpretation of business terminology.
- Robustness to paraphrasing.
- Evidence-based explanation of the change.

Use the live SDK notebook for measured accuracy:

1. Import the deployment and SDK evaluation notebooks, then attach `LegalFirmDemo` to the evaluation notebook as its default Lakehouse.
2. Run with `SNAPSHOT_NAME = "step1_baseline"` for the initial agent.
3. Run with `SNAPSHOT_NAME = "step2_prep_ai"` after Prep for AI and agent instructions are configured.
4. Run with `SNAPSHOT_NAME = "step3_lakehouse_added"` immediately after attaching the Lakehouse and before tuning it.
5. Run with `SNAPSHOT_NAME = "step4_lakehouse_tuned"` after Lakehouse source tuning.
6. Run with `SNAPSHOT_NAME = "step5_final"` for the final standard challenge, then `SNAPSHOT_NAME = "step5_routing"` for the separate routing marts dataset.

The notebook maps each snapshot to the correct dataset. Keep the agent, stage, and challenge questions unchanged across challenge snapshots. Review its question-by-step comparison and missing-evidence warnings. Step 6 ontology is qualitative unless a separate ontology dataset is introduced. The manual review notebook remains optional for facilitator scoring.
