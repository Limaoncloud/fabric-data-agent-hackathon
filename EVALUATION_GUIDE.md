# Evaluation Framework - Quick Start Guide

This guide explains how to use the evaluation framework to measure actual data agent accuracy.

## What's Included

1. **evaluation_dataset.json** - 30 ground truth questions with expected answers
2. **evaluate_agent.py** - Python framework to test and measure accuracy
3. **TEST_QUERIES.md** - Manual testing guide with expected results

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
python evaluate_agent.py --simulation --dataset evaluation_dataset.json --output results_simulation.json
```

This will:
- ✅ Test all 30 queries
- ✅ Simulate routing logic
- ✅ Calculate accuracy metrics
- ✅ Generate a report

### Option 2: Production Mode (Requires Fabric API)

To test against an actual Fabric Data Agent:

```bash
# Install dependencies
pip install azure-identity azure-ai-projects pandas numpy

# Run evaluation
python evaluate_agent.py \
  --workspace-id <your_workspace_id> \
  --agent-id <your_agent_id> \
  --dataset evaluation_dataset.json \
  --output results.json
```

**Note:** You'll need to update `evaluate_agent.py` with the actual Fabric Data Agent API calls. The current implementation has placeholder code.

## Understanding the Dataset

### evaluation_dataset.json Structure

```json
{
  "metadata": {
    "name": "UK Legal Firm Data Agent Evaluation",
    "total_queries": 30
  },
  "evaluation_queries": [
    {
      "id": "Q001",
      "question": "How many active customers do we have?",
      "category": "customer_count",
      "expected_source": "ClientCasePortfolio",
      "ground_truth_answer": 15,
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
python evaluate_agent.py \
  --agent-id step3_agent \
  --dataset evaluation_dataset.json \
  --output step3/step3_results.json
```

**Expected Metrics:**
- Exact Match Accuracy: ~60-70%
- Routing Accuracy: ~70% (no routing rules)
- Measure Selection: ~40% (duplicate measures confuse agent)

### Step 4 (Optimized Model) - Expected Results

```bash
# Test Step 4 agent
python evaluate_agent.py \
  --agent-id step4_agent \
  --dataset evaluation_dataset.json \
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
python evaluate_agent.py \
  --agent-id step6_agent \
  --dataset evaluation_dataset.json \
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
    "total_queries": 30,
    "exact_match_accuracy": 0.9333,
    "semantic_match_accuracy": 0.9667,
    "routing_accuracy": 0.9444,
    "by_category": { ... }
  },
  "detailed_metrics": [
    {
      "query_id": "Q001",
      "exact_match": true,
      "semantic_match": true,
      "routing_correct": true,
      "notes": "OK"
    }
  ]
}
```

## Manual Testing Alternative

If you prefer manual testing, use [TEST_QUERIES.md](TEST_QUERIES.md):

1. Open your Data Agent in Fabric
2. Run each query from TEST_QUERIES.md
3. Compare actual answer to ground truth
4. Record results in the log template

This is more time-consuming but doesn't require code.

## Integration with Actual Fabric API

To connect to a real Fabric Data Agent, update `evaluate_agent.py`:

### 1. Install Fabric SDK

```bash
pip install <fabric-data-agent-sdk>
```

### 2. Update execute_query Method

Replace the placeholder in `DataAgentEvaluator.execute_query()`:

```python
def execute_query(self, question: str) -> QueryResult:
    start_time = time.time()
    
    # Call actual Fabric Data Agent API
    response = self.client.query(
        workspace_id=self.workspace_id,
        agent_id=self.agent_id,
        question=question
    )
    
    result = QueryResult(
        query_id="",
        question=question,
        answer=response.answer,
        source_used=response.data_source_used,
        response_time_ms=(time.time() - start_time) * 1000,
        dax_query=response.dax_query,
        sql_query=response.sql_query,
        error=response.error,
        run_steps=response.run_steps
    )
    
    return result
```

### 3. Parse Run Steps

Update `evaluate_query()` to parse run steps for:
- Verified Answer usage
- Routing decisions
- Measure selection

## Best Practices

### 1. Test All Steps
Create separate agents for Steps 3, 4, and 6, then evaluate each:

```bash
python evaluate_agent.py --agent-id step3_agent --output step3/step3_results.json
python evaluate_agent.py --agent-id step4_agent --output step4/step4_results.json
python evaluate_agent.py --agent-id step6_agent --output step6/step6_results.json
```

### 2. Run Multiple Times
Run evaluation 3-5 times and average results (LLMs can be non-deterministic)

### 3. Add Custom Queries
Extend `evaluation_dataset.json` with your own domain-specific queries

### 4. Track Over Time
Save results with timestamps to track improvements:

```bash
python evaluate_agent.py --output results_$(date +%Y%m%d_%H%M%S).json
```

### 5. Focus on Categories
If certain categories score low, dig into those specific queries

## Troubleshooting

### "No module named 'azure'"
Install dependencies: `pip install azure-identity`

### "Actual API integration not implemented"
Update `execute_query()` with real Fabric API calls

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
2. **Run evaluation** on both
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

1. Show the evaluation_dataset.json file (ground truth queries)
2. Run the evaluation script live (if time permits)
3. Display the report with actual percentages
4. Highlight specific query improvements

## Summary

✅ **evaluation_dataset.json** - 30 ground truth queries  
✅ **evaluate_agent.py** - Automated testing framework  
✅ **TEST_QUERIES.md** - Manual testing guide  
✅ **Measured metrics** replace estimated percentages  
✅ **Before/after comparison** proves improvements  

This transforms your demo from "best practices say this works" to "here's proof it works!"

---

**Need help?** Check the example queries in TEST_QUERIES.md or review the simulation mode output.
