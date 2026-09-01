# Facilitator Guide: Agent Testing Challenge

Keep this guide separate from participant materials until teams have recorded their baseline answers and diagnoses.

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

Confirm that each prompt routes to the appropriate `base_*` table, filters on the exact identifier, and returns every available column for the matching record. Stop after these examples; do not provide SQL for the six scored questions.

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

## Debrief Questions

Ask each team to present:

- One failure they initially diagnosed incorrectly.
- One change that materially improved behavior.
- One change that did not help.
- Evidence that the improvement survives a paraphrase.
- Why the chosen configuration layer was more durable than an agent-only workaround.

## Final Unseen Questions

Use these after the six-question exercise. Do not provide expected values until teams submit answers.

- What is our active client population?
- What is the firm’s entire matter portfolio worth?
- How much have we invoiced in total?
- How many invoices are still outstanding and unpaid?
- How many matters remain open?
- What is the total number of clients in the system?

## Evaluation

Score each response on:

- Correct answer.
- Correct measure or field selection.
- Correct interpretation of business terminology.
- Robustness to paraphrasing.
- Evidence-based explanation of the change.

Use the focused dataset for this exercise:

```powershell
python evaluation/evaluate_agent.py `
    --simulation `
    --dataset evaluation/challenge/uk-legal.json `
    --output evaluation/results/hackathon-challenge.json
```
