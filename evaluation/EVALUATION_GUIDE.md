# Evaluation Framework - Quick Start Guide

This guide explains how to use the evaluation framework to measure actual data agent accuracy.

## What's Included

1. **NB_Evaluate_Data_Agent_Hackathon.ipynb** - Participant notebook for entering observed results and generating a scored report
2. **evaluation/challenge/uk-legal.json** - Current six-question participant challenge with checked ground truths and paraphrases
3. **evaluation/routing/uk-legal.json** - Optional 3-question extension for Step 5 (Lakehouse routing); run separately from the six-question challenge
4. **evaluation/FACILITATOR_GUIDE.md** - Facilitator-only answers, escalating hints, and debrief guidance
5. **evaluation/legacy/uk-legal.json** - Extended legacy question bank; source names (`ClientCasePortfolio`, `FinancialTransactions`) predate the current `LegalFirmOptimized`/`LegalFirmDemo` architecture. Regenerate all ground truths and source names before formal use.
6. **evaluation/evaluate_agent.py** - Facilitator framework for SDK-backed or simulated evaluation
7. **evaluation/legacy/TEST_QUERIES.md** - Extended manual testing reference; also predates the current architecture and step numbering

For the three-hour hackathon, use `evaluation/challenge/uk-legal.json`. Its expected answers are tested directly against the checked-in CSV files. Add `evaluation/routing/uk-legal.json` once you reach Step 5.

## Why Evaluate?

The demo documentation shows **estimated** accuracy improvements based on Microsoft Learn best practices. To get **actual measured results** for your hackathon:

1. ✅ Proves the improvements are real
2. ✅ Provides concrete metrics (not estimates)
3. ✅ Identifies specific areas for improvement
4. ✅ Creates reproducible benchmarks

## Quick Start: Run Evaluation

### Option 1: Participant Results Notebook (Recommended During The Event)

1. Import `NB_Evaluate_Data_Agent_Hackathon.ipynb` into Fabric.
2. Enter observed baseline and final results in its single participant input cell.
3. Mark query/measure logic only after inspecting the Data Agent run steps.
4. Run all cells to receive baseline and final scores out of 24.
5. Submit the exported CSV and JSON with query evidence.

This path does not call the Data Agent API and requires no SDK setup.

### Option 2: Simulation Mode (Framework Test Only)

Test the evaluation framework without connecting to Fabric:

```bash
python evaluation/evaluate_agent.py --simulation --dataset evaluation/challenge/uk-legal.json --output results_simulation.json
```

This will:
- ✅ Test all 6 challenge queries
- ✅ Simulate routing logic
- ✅ Calculate accuracy metrics
- ✅ Generate a report

### Option 3: Official Fabric SDK Mode (Facilitator Automation)

To test against an actual Fabric Data Agent using the Microsoft-recommended workflow:

```bash
# Install dependencies
pip install -U fabric-data-agent-sdk pandas

# Run SDK-backed evaluation
python evaluation/evaluate_agent.py \
  --sdk-mode \
  --agent-id <your_data_agent_name> \
  --workspace-name <optional_workspace_name> \
  --table-name demo_evaluation_output \
  --stage production \
  --dataset evaluation/challenge/uk-legal.json \
  --output results.json \
  --save-official-details-csv
```

What this does:
- Calls `evaluate_data_agent` from the Fabric SDK
- Retrieves official summary via `get_evaluation_summary`
- Retrieves official details via `get_evaluation_details`
- Produces local JSON output plus optional CSV of official detail rows
- Prints a compatibility report (custom metrics vs official summary)

### Optional: Custom Critic Prompt in SDK Mode

Use a stricter or domain-specific evaluator prompt:

```bash
python evaluation/evaluate_agent.py \
  --sdk-mode \
  --agent-id <your_data_agent_name> \
  --table-name demo_evaluation_output \
  --dataset evaluation/challenge/uk-legal.json \
  --output results.json \
  --critic-prompt-file critic_prompt.txt
```

You can also pass inline text with `--critic-prompt`.

## Understanding the Dataset

### evaluation/challenge/uk-legal.json Structure

```json
{
  "metadata": {
    "name": "UK Legal Data Agent Hackathon Challenge",
    "total_queries": 6
  },
  "evaluation_queries": [
    {
      "id": "HC001",
      "question": "How many active clients do we have?",
      "paraphrase": "What is our current active customer count?",
      "category": "terminology",
      "expected_source": "LegalFirmOptimized",
      "ground_truth_answer": 101,
      "answer_type": "number",
      "difficulty": "easy",
      "tests_routing": true,
      "notes": "Should use Number of Active Customers measure"
    }
  ]
}
```

### Query Categories

1. **customer_count** (5 queries) - Customer counting and filtering
2. **case_summary** (11 queries) - Case-level analysis
3. **financial_transactions** (8 queries) - Billing, hours, expenses
4. **solicitor_performance** (4 queries) - Solicitor metrics
5. **routing_test** (2 queries) - Multi-source queries

### Query Difficulty Levels

- **Easy** (13 queries) - Simple filtering and counting
- **Medium** (14 queries) - Aggregation, grouping, date ranges
- **Hard** (3 queries) - Complex joins, subqueries

## Metrics Measured

### 1. Exact Match Accuracy
Answer exactly matches ground truth (e.g., 15 = 15)

### 2. Semantic Match Accuracy
Answer is semantically correct within tolerance:
- Numbers: within 5% of ground truth
- Lists: 80%+ overlap
- Tables: all keys present, values within 5%

### 3. Routing Accuracy
Correct data source selected (`LegalFirmOptimized` vs `LegalFirmDemo`)

### 4. Measure Selection Accuracy
Correct DAX measure used (important for Step 3 vs Step 4 comparison)

### 5. Response Time
Average query response time in milliseconds

### 6. Verified Answer Hit Rate
Percentage of queries that matched a Verified Answer

### 7. Error Rate
Percentage of queries that resulted in errors

## Comparing Across Steps

USER_GUIDE.md builds one continuously-extended Data Agent (`LegalFirmAgent`), not separate agents per step. Snapshot the same agent's behavior at each step by giving each run its own output file:

```bash
# Step 1: semantic-model baseline
python evaluation/evaluate_agent.py --sdk-mode --agent-id LegalFirmAgent \
  --dataset evaluation/challenge/uk-legal.json --output evaluation/results/step1-semantic-baseline.json

# Step 2: after Prep for AI
python evaluation/evaluate_agent.py --sdk-mode --agent-id LegalFirmAgent \
  --dataset evaluation/challenge/uk-legal.json --output evaluation/results/step2-after-prep-for-ai.json

# Step 5: after attaching the Lakehouse, tuning it, and adding derived tables/routing
python evaluation/evaluate_agent.py --sdk-mode --agent-id LegalFirmAgent \
  --dataset evaluation/challenge/uk-legal.json --output evaluation/results/step5-challenge.json
python evaluation/evaluate_agent.py --sdk-mode --agent-id LegalFirmAgent \
  --dataset evaluation/routing/uk-legal.json --output evaluation/results/step5-routing.json
```

Use `--simulation` instead of `--sdk-mode` only to smoke-test the framework; simulation results are seeded and illustrative, never measured accuracy.

## Viewing Results

### Console Output

The script prints a detailed report:

```
================================================================================
EVALUATION REPORT
================================================================================

Total Queries: 30

Overall Accuracy:
  Exact Match:       93.33%
  Semantic Match:    96.67%
  Routing:           94.44%
  Measure Selection: 95.00%

Performance:
  Avg Response Time:  2,450 ms
  Verified Answer Hit Rate: 20.00%
  Error Rate:          3.33%

By Category:
  customer_count            (n= 5): Exact=100.0%, Semantic=100.0%, Routing=100.0%
  case_summary              (n=11): Exact= 90.9%, Semantic= 95.5%, Routing= 90.9%
  financial_transactions    (n= 8): Exact= 87.5%, Semantic= 93.8%, Routing= 93.8%
  ...
```

### JSON Output

Results are saved to JSON for further analysis:

```json
{
  "evaluation_date": "2026-08-04T10:30:00",
  "agent_id": "step4_agent",
  "aggregate_metrics": {
    "total_queries": 6,
    "exact_match_accuracy": 0.8333,
    "semantic_match_accuracy": 0.8333,
    "routing_accuracy": 1.0,
    "by_category": { ... }
  },
  "detailed_metrics": [
    {
      "query_id": "HC001",
      "exact_match": true,
      "semantic_match": true,
      "routing_correct": true,
      "notes": "OK"
    }
  ]
}
```

## Manual Testing Alternative

If you prefer manual testing, use the challenge table in [FACILITATOR_GUIDE.md](FACILITATOR_GUIDE.md). Use [TEST_QUERIES.md](legacy/TEST_QUERIES.md) only for an extended follow-up:

1. Open your Data Agent in Fabric
2. Run each question and paraphrase from the six-question challenge
3. Compare actual answer to ground truth
4. Record results in the log template

This is more time-consuming but doesn't require code.

## Evaluation Modes in This Repo

There are exactly two modes; `evaluate_agent.py` requires picking one.

### 1) Simulation mode (illustrative only)
- Seeded, reproducible dry-run for framework validation. Does not call a real agent.
- Never report these numbers as measured accuracy.
- Command: `python evaluation/evaluate_agent.py --simulation --seed 42 --step 2 --dataset evaluation/challenge/uk-legal.json --output results.json`

### 2) SDK mode (real, measured accuracy)
- Official Microsoft workflow using the Fabric Data Agent SDK against a real deployed agent.
- Persists official evaluation tables in Fabric and saves local output.
- Supports custom critic prompts and compatibility reporting.

## Best Practices

### 1. Test All Steps
Evaluate the same `LegalFirmAgent` at each step boundary, using a distinct output file per step:

```bash
python evaluation/evaluate_agent.py --sdk-mode --agent-id LegalFirmAgent --output evaluation/results/step1-semantic-baseline.json
python evaluation/evaluate_agent.py --sdk-mode --agent-id LegalFirmAgent --output evaluation/results/step2-after-prep-for-ai.json
python evaluation/evaluate_agent.py --sdk-mode --agent-id LegalFirmAgent --output evaluation/results/step5-challenge.json
```

### 2. Run Multiple Times
Run evaluation 3-5 times and average results (LLMs can be non-deterministic)

### 3. Add Custom Queries
Extend `evaluation/challenge/uk-legal.json` (core) or `evaluation/routing/uk-legal.json` (routing) with your own domain-specific queries. Only extend `evaluation/legacy/uk-legal.json` after regenerating its stale source names and ground truths.

### 4. Track Over Time
Save results with timestamps to track improvements:

```bash
python evaluation/evaluate_agent.py --output results_$(date +%Y%m%d_%H%M%S).json
```

### 5. Focus on Categories
If certain categories score low, dig into those specific queries

## Troubleshooting

### "No module named 'fabric'" or SDK import errors
Install dependencies: `pip install -U fabric-data-agent-sdk pandas`

### "fabric-data-agent-sdk is required for --sdk-mode"
Install the package and rerun with the same command.

### "No SDK detail row returned for this query"
The script flags unmatched rows as explicit failures. Check:
1. Agent accessibility and workspace scope
2. Whether the evaluation finished and wrote all rows
3. Table name/stage values used in the command

### Low Accuracy
1. Check data source descriptions
2. Review example queries
3. Verify AI Instructions
4. Test individual failing queries manually

### Slow Response Times
1. Optimize semantic model
2. Add more Verified Answers
3. Reduce schema selection
4. Check DAX measure efficiency

## For Your Hackathon

### Recommended Approach

1. **Deploy the semantic-model agent (Step 1) and tune it (Step 2)**
2. **Run SDK evaluation** before and after Step 2's Prep for AI changes
3. **Show before/after metrics** in your presentation
4. **Use real numbers** instead of estimates

### Demo Script Addition

Add this to your demo:

> "To validate these improvements, I ran the six-question challenge against the same
> agent before and after Prep for AI. Here are the actual measured results:
> - Before Prep for AI: 64% accurate
> - After Prep for AI: 96% accurate
> - That's a measured improvement from one real SDK evaluation, not an estimate."

### Presentation Tips

1. Show the evaluation/challenge/uk-legal.json file (ground truth queries)
2. Run the evaluation script live (if time permits)
3. Display the report with actual percentages
4. Highlight specific query improvements

## Summary

✅ **evaluation/challenge/uk-legal.json** - 6 ground truth queries  
✅ **evaluation/routing/uk-legal.json** - 3 optional routing queries  
✅ **evaluation/evaluate_agent.py** - Automated testing framework  
✅ **evaluation/legacy/TEST_QUERIES.md** - Manual testing guide (legacy reference)  
✅ **Measured metrics** replace estimated percentages  
✅ **Before/after comparison** proves improvements  

This transforms your demo from "best practices say this works" to "here's proof it works!"

---

**Need help?** Check the example queries in evaluation/legacy/TEST_QUERIES.md or review the simulation mode output.


