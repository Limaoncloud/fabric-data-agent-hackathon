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

## Worked Example

**Question:** How many open matters do we have?

**Expected answer:** 180.

Demonstrate only this example. Ask whether *matter* is a new calculation or another name for *case*. Add `matter` and `matters` as synonyms for the Cases table, retest the original question, and then test: **How many matters are currently open?**

Do not demonstrate additional fixes.

## Answer Key

| ID | Question | Expected answer | Likely learning area |
| --- | --- | ---: | --- |
| HC001 | How many active clients do we have? | 101 | Legal terminology and measure selection |
| HC002 | What is the total value of all matters? | GBP 123,590,881 | Terminology and explicit measure selection |
| HC003 | How much revenue have we generated? | GBP 5,420,217 | Business definition of revenue |
| HC004 | How many invoices remain unpaid? | 54 | Existing measure discoverability |
| HC005 | How many legal cases are currently open? | 180 | Consistency across terminology |
| HC006 | How many customers do we have? | 171 | Basic grounding and schema scope |

Ground truths come from the checked-in Step 1 CSV files. The machine-readable set is `evaluation/hackathon_challenge_dataset.json`.

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

- Would one synonym address the terminology gap?
- Is the AI Data Schema too broad or missing a required object?
- Does the business rule belong in a measure description or AI instruction?
- Is the issue specific to one source and better placed in Data Agent source instructions?
- Is this question stable enough to justify a Verified Answer?

Never tell a team both the diagnosis and the exact control in the same hint.

## Suggested Interventions

These are not mandatory solutions. Accept alternatives when teams can explain and demonstrate the effect.

| ID | Candidate intervention | Evidence to request |
| --- | --- | --- |
| HC001 | Add `client` as a customer synonym or clarify terminology | Original and paraphrase both select Active Customers |
| HC002 | Add `matter` as a case synonym and expose Total Case Value | Agent uses the explicit measure for both phrasings |
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
    --dataset evaluation/hackathon_challenge_dataset.json `
    --output evaluation/hackathon_challenge_results.json
```
