# Evaluation Framework - Quick Start Guide

This guide explains how to use the evaluation framework to measure actual data agent accuracy.

## What's Included

1. **evaluation/hackathon_challenge_dataset.json** - Current six-question participant challenge with checked ground truths and paraphrases
2. **evaluation/FACILITATOR_GUIDE.md** - Facilitator-only answers, escalating hints, and debrief guidance
3. **evaluation/evaluation_dataset.json** - Extended legacy question bank; regenerate all ground truths before formal use with changed source data
4. **evaluation/evaluate_agent.py** - Python framework to test and measure accuracy
5. **evaluation/TEST_QUERIES.md** - Extended manual testing reference

For the three-hour hackathon, use `hackathon_challenge_dataset.json`. Its expected answers are tested directly against the checked-in CSV files.

## Why Evaluate?

The demo documentation shows **estimated** accuracy improvements based on Microsoft Learn best practices. To get **actual measured results** for your hackathon:

1. ✅ Proves the improvements are real
2. ✅ Provides concrete metrics (not estimates)
3. ✅ Identifies specific areas for improvement
4. ✅ Creates reproducible benchmarks

## Quick Start: Run Evaluation

### Option 1: Simulation Mode (No Fabric API)

Test the evaluation framework without connecting to Fabric:

```bash
python evaluation/evaluate_agent.py --simulation --dataset evaluation/hackathon_challenge_dataset.json --output results_simulation.json
```

This will:
- ✅ Test all 30 queries
- ✅ Simulate routing logic
- ✅ Calculate accuracy metrics
- ✅ Generate a report

### Option 2: Official Fabric SDK Mode (Recommended)

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
  --dataset evaluation/hackathon_challenge_dataset.json \
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
  --dataset evaluation/hackathon_challenge_dataset.json \
  --output results.json \
  --critic-prompt-file critic_prompt.txt
```

You can also pass inline text with `--critic-prompt`.

## Understanding the Dataset

### evaluation/hackathon_challenge_dataset.json Structure

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
Correct data source selected (ClientCasePortfolio vs FinancialTransactions)

### 4. Measure Selection Accuracy
Correct DAX measure used (important for Step 3 vs Step 4 comparison)

### 5. Response Time
Average query response time in milliseconds

### 6. Verified Answer Hit Rate
Percentage of queries that matched a Verified Answer

### 7. Error Rate
Percentage of queries that resulted in errors

## Comparing Across Steps

### Step 3 (Basic Model) - Expected Results

```bash
# Test Step 3 agent
python evaluation/evaluate_agent.py \
  --agent-id step3_agent \
  --dataset evaluation/evaluation_dataset.json \
  --output step3/step3_results.json
```

**Expected Metrics:**
- Exact Match Accuracy: ~60-70%
- Routing Accuracy: ~70% (no routing rules)
- Measure Selection: ~40% (duplicate measures confuse agent)

### Step 4 (Optimized Model) - Expected Results

```bash
# Test Step 4 agent
python evaluation/evaluate_agent.py \
  --agent-id step4_agent \
  --dataset evaluation/evaluation_dataset.json \
  --output step4/step4_results.json
```

**Expected Metrics:**
- Exact Match Accuracy: ~95-100%
- Routing Accuracy: N/A (single source)
- Measure Selection: ~95%+ (no duplicates)
- Verified Answer Hit Rate: ~20% (6/30 queries)

### Step 6 (With Routing) - Expected Results

```bash
# Test Step 6 agent
python evaluation/evaluate_agent.py \
  --agent-id step6_agent \
  --dataset evaluation/evaluation_dataset.json \
  --output step6/step6_results.json
```

**Expected Metrics:**
- Exact Match Accuracy: ~90-95%
- Routing Accuracy: ~90-95%
- Measure Selection: ~95%+
- Verified Answer Hit Rate: ~20%

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

If you prefer manual testing, use the challenge table in [FACILITATOR_GUIDE.md](FACILITATOR_GUIDE.md). Use [TEST_QUERIES.md](TEST_QUERIES.md) only for an extended follow-up:

1. Open your Data Agent in Fabric
2. Run each question and paraphrase from the six-question challenge
3. Compare actual answer to ground truth
4. Record results in the log template

This is more time-consuming but doesn't require code.

## Evaluation Modes in This Repo

### 1) Simulation mode
- Fast dry-run for framework validation
- Command: `python evaluation/evaluate_agent.py --simulation --step 4 --dataset evaluation/hackathon_challenge_dataset.json --output results.json`

### 2) SDK mode
- Official Microsoft workflow using Fabric Data Agent SDK
- Persists official evaluation tables in Fabric and saves local output
- Supports custom critic prompts and compatibility reporting

### 3) Custom production mode (legacy placeholder)
- Keeps backward compatibility but does not implement direct live query API calls
- Prefer SDK mode for production evaluations

## Best Practices

### 1. Test All Steps
Create separate agents for Steps 3, 4, and 6, then evaluate each:

```bash
python evaluation/evaluate_agent.py --agent-id step3_agent --output step3/step3_results.json
python evaluation/evaluate_agent.py --agent-id step4_agent --output step4/step4_results.json
python evaluation/evaluate_agent.py --agent-id step6_agent --output step6/step6_results.json
```

### 2. Run Multiple Times
Run evaluation 3-5 times and average results (LLMs can be non-deterministic)

### 3. Add Custom Queries
Extend `evaluation/evaluation_dataset.json` with your own domain-specific queries

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

1. **Deploy Step 3 and Step 4 agents** to Fabric workspace
2. **Run SDK evaluation** on both
3. **Show before/after metrics** in your presentation
4. **Use real numbers** instead of estimates

### Demo Script Addition

Add this to your demo:

> "To validate these improvements, I ran 30 test queries against both models. 
> Here are the actual measured results:
> - Step 3: 64% accurate
> - Step 4: 96% accurate
> - That's a measured 50% improvement!"

### Presentation Tips

1. Show the evaluation/evaluation_dataset.json file (ground truth queries)
2. Run the evaluation script live (if time permits)
3. Display the report with actual percentages
4. Highlight specific query improvements

## Summary

✅ **evaluation/evaluation_dataset.json** - 30 ground truth queries  
✅ **evaluation/evaluate_agent.py** - Automated testing framework  
✅ **evaluation/TEST_QUERIES.md** - Manual testing guide  
✅ **Measured metrics** replace estimated percentages  
✅ **Before/after comparison** proves improvements  

This transforms your demo from "best practices say this works" to "here's proof it works!"

---

**Need help?** Check the example queries in evaluation/TEST_QUERIES.md or review the simulation mode output.


