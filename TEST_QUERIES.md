# Test Queries for Fabric Data Agent Demo

This file contains test queries to validate each step of the demo and demonstrate improvements.

## Query Testing Framework

### Expected Behavior by Step

| Step | Query Accuracy | Notes |
|------|---------------|-------|
| Step 1-2 | N/A | Data preparation only |
| Step 3 | ~64% | Basic model, many issues |
| Step 4 | 100% | Optimized model |
| Step 5 | 95%+ | With ontology |
| Step 6 | 94%+ | With routing |

---

## Category 1: Customer/Client Queries
**Should Route To:** ClientCasePortfolio

### Q1: "How many active customers do we have?"
**Expected Source:** ClientCasePortfolio  
**Expected Query:** `SELECT COUNT(DISTINCT customer_id) FROM Customers WHERE customer_status = 'Active'`  
**Expected Answer:** ~15 active customers  
**Measure Used:** Number of Active Customers  
**Verified Answer:** VA004

---

### Q2: "Show me all corporate clients"
**Expected Source:** ClientCasePortfolio  
**Expected Query:** `SELECT customer_id, customer_name FROM Customers WHERE customer_type = 'Corporate'`  
**Expected Answer:** List of corporate customers (ACME Corporation, TechStart Ltd, BuildRight Construction, etc.)  
**Measure Used:** Number of Corporate Customers

---

### Q3: "Which clients are in London?"
**Expected Source:** ClientCasePortfolio  
**Expected Query:** `SELECT customer_name, customer_postcode FROM Customers WHERE customer_postcode LIKE 'SW%' OR customer_postcode LIKE 'EC%' OR customer_postcode LIKE 'W1%'`  
**Expected Answer:** Clients with London postcodes (SW, EC, W1, etc.)

---

## Category 2: Case Queries
**Should Route To:** ClientCasePortfolio

### Q4: "What case types do we handle?"
**Expected Source:** ClientCasePortfolio  
**Expected Query:** `SELECT DISTINCT case_type, COUNT(*) FROM Cases GROUP BY case_type ORDER BY COUNT(*) DESC`  
**Expected Answer:** List of case types (Conveyancing, Corporate Law, Family Law, etc.)  
**Example Query Match:** Example #3 in ClientCasePortfolio

---

### Q5: "Show me all cases assigned to Sarah Jones"
**Expected Source:** ClientCasePortfolio  
**Expected Query:** `SELECT case_id, case_type, case_value_gbp, payment_status FROM Cases WHERE assigned_solicitor_name = 'Sarah Jones'`  
**Expected Answer:** List of Sarah Jones' cases  
**Example Query Match:** Example #2 in ClientCasePortfolio

---

### Q6: "What's the total value of all cases?"
**Expected Source:** ClientCasePortfolio  
**Expected Query:** DAX: `Total Case Value`  
**Expected Answer:** ~£1,085,200  
**Measure Used:** Total Case Value  
**Verified Answer:** VA001 (Exact Match)

---

### Q7: "Which clients have high-value cases?"
**Expected Source:** ClientCasePortfolio  
**Expected Query:** `SELECT DISTINCT c.customer_name FROM Customers c JOIN Cases cs ON c.customer_id = cs.customer_id WHERE cs.high_value_case_flag = 'Yes'`  
**Expected Answer:** ACME Corporation, Heritage Properties Group, etc.  
**Example Query Match:** Example #4 in ClientCasePortfolio

---

### Q8: "How many cases were started in Q1 2023?"
**Expected Source:** ClientCasePortfolio  
**Expected Query:** `SELECT COUNT(*) FROM Cases WHERE case_start_date >= '2023-01-01' AND case_start_date < '2023-04-01'`  
**Expected Answer:** Count of cases in Q1 2023  
**Example Query Match:** Example #5 in ClientCasePortfolio

---

### Q9: "Show me case value by case type"
**Expected Source:** ClientCasePortfolio  
**Expected Query:** DAX: `Total Case Value` grouped by `case_type`  
**Expected Answer:** Bar chart or table with case types and values  
**Verified Answer:** VA002 (Exact Match)

---

### Q10: "What cases have payment status overdue?"
**Expected Source:** ClientCasePortfolio  
**Expected Query:** `SELECT case_id, customer_id, case_value_gbp FROM Cases WHERE payment_status = 'Overdue'`  
**Expected Answer:** List of overdue cases  
**Measure Used:** Overdue Payment Value

---

## Category 3: Financial/Billing Queries
**Should Route To:** FinancialTransactions

### Q11: "How many hours did Sarah Jones bill in March 2023?"
**Expected Source:** FinancialTransactions  
**Expected Query:** `SELECT SUM(hours_worked) FROM FinancialTransactions WHERE solicitor_name = 'Sarah Jones' AND transaction_type = 'Timesheet' AND transaction_date >= '2023-03-01' AND transaction_date < '2023-04-01'`  
**Expected Answer:** Sum of hours (e.g., 14.5 hours)  
**Example Query Match:** Example #1 in FinancialTransactions

---

### Q12: "What's the total of all expenses for case CASE005?"
**Expected Source:** FinancialTransactions  
**Expected Query:** `SELECT SUM(expense_amount_gbp) FROM FinancialTransactions WHERE case_id = 'CASE005' AND transaction_type = 'Expense'`  
**Expected Answer:** £250.00  
**Example Query Match:** Example #2 in FinancialTransactions

---

### Q13: "Show me all unpaid invoices"
**Expected Source:** FinancialTransactions  
**Expected Query:** `SELECT DISTINCT invoice_number, payment_amount_gbp, customer_id FROM FinancialTransactions WHERE transaction_type = 'Invoice' AND invoice_number NOT IN (SELECT invoice_number FROM FinancialTransactions WHERE transaction_type = 'Payment')`  
**Expected Answer:** List of invoices without corresponding payment records  
**Example Query Match:** Example #3 in FinancialTransactions (Exact)

---

### Q14: "What's Robert Smith's hourly rate?"
**Expected Source:** FinancialTransactions  
**Expected Query:** `SELECT DISTINCT hourly_rate_gbp FROM FinancialTransactions WHERE solicitor_name = 'Robert Smith' AND transaction_type = 'Timesheet'`  
**Expected Answer:** £350  
**Example Query Match:** Example #4 in FinancialTransactions

---

### Q15: "How much total payment did we receive in Q2 2023?"
**Expected Source:** FinancialTransactions  
**Expected Query:** `SELECT SUM(payment_amount_gbp) FROM FinancialTransactions WHERE transaction_type = 'Payment' AND payment_date >= '2023-04-01' AND payment_date < '2023-07-01'`  
**Expected Answer:** Sum of Q2 payments  
**Example Query Match:** Example #5 in FinancialTransactions

---

### Q16: "What expenses were incurred on CASE011?"
**Expected Source:** FinancialTransactions  
**Expected Query:** `SELECT transaction_date, description, expense_amount_gbp FROM FinancialTransactions WHERE case_id = 'CASE011' AND transaction_type = 'Expense'`  
**Expected Answer:** £125.00 for document certification

---

### Q17: "Show me all timesheets for February 2023"
**Expected Source:** FinancialTransactions  
**Expected Query:** `SELECT solicitor_name, hours_worked, hourly_rate_gbp FROM FinancialTransactions WHERE transaction_type = 'Timesheet' AND transaction_date >= '2023-02-01' AND transaction_date < '2023-03-01'`  
**Expected Answer:** List of timesheet entries for February

---

## Category 4: Solicitor Performance Queries

### Q18: "Who are our top solicitors by case value?"
**Expected Source:** ClientCasePortfolio  
**Expected Query:** DAX with grouping by solicitor  
**Expected Answer:** Table with solicitors ranked by Total Case Value  
**Measure Used:** Total Case Value, Number of Cases, Average Case Value  
**Verified Answer:** VA003 (Exact Match)

---

### Q19: "Show me each solicitor's caseload"
**Expected Source:** ClientCasePortfolio  
**Expected Query:** `SELECT assigned_solicitor_name, COUNT(*) as case_count FROM Cases GROUP BY assigned_solicitor_name`  
**Expected Answer:** Sarah Jones: X cases, Robert Smith: Y cases, Michael Brown: Z cases

---

### Q20: "How many hours did each solicitor bill last month?"
**Expected Source:** FinancialTransactions  
**Expected Query:** `SELECT solicitor_name, SUM(hours_worked) FROM FinancialTransactions WHERE transaction_type = 'Timesheet' AND transaction_date >= [last_month_start] GROUP BY solicitor_name`  
**Expected Answer:** Total hours by solicitor

---

## Category 5: Ontology/Entity-Based Queries

### Q21: "Show me all cases for ACME Corporation"
**Expected Source:** Ontology (if available) or ClientCasePortfolio  
**Expected Behavior:** 
- Query Client entity where name contains "ACME"
- Traverse ClientHasCase relationship
- Return related LegalCase entities
**Expected Answer:** List of ACME's cases (CASE002, CASE007, CASE013)

---

### Q22: "Which solicitors work with corporate clients?"
**Expected Source:** Ontology (if available) or ClientCasePortfolio  
**Expected Behavior:**
- Query Client entity where ClientType = 'Corporate'
- Traverse SolicitorServesClient derived relationship
- Return related Solicitor entities
**Expected Answer:** Solicitors who handle corporate cases

---

### Q23: "What's the client portfolio summary for each customer?"
**Expected Source:** Ontology (if available) or ClientCasePortfolio  
**Expected Behavior:**
- Use ClientPortfolioContext contextualization
- Return aggregated metrics per client
**Expected Answer:** Table with TotalCaseValue, NumberOfCases, AverageCaseValue per client

---

### Q24: "Show me case opening trends by month"
**Expected Source:** Ontology (if available) or ClientCasePortfolio  
**Expected Behavior:**
- Use CaseStartDate timeseries property
- Aggregate by month
**Expected Answer:** Timeseries showing case counts by month

---

## Category 6: Multi-Source Queries (Complex)

### Q25: "What's the total billing for ACME Corporation?"
**Expected Sources:** Both (ClientCasePortfolio + FinancialTransactions)  
**Expected Behavior:**
1. Query ClientCasePortfolio for ACME's case_ids
2. Query FinancialTransactions for invoices for those case_ids
3. Sum invoice amounts
**Expected Answer:** Total invoiced amount for ACME

---

### Q26: "Show me solicitor performance with hours and case count"
**Expected Sources:** Both (ClientCasePortfolio + FinancialTransactions)  
**Expected Behavior:**
1. Query ClientCasePortfolio for case counts per solicitor
2. Query FinancialTransactions for hours per solicitor
3. Combine results
**Expected Answer:** Table with solicitor name, case count, total hours

---

### Q27: "Which cases have expenses but no payment?"
**Expected Sources:** Both (ClientCasePortfolio + FinancialTransactions)  
**Expected Behavior:**
1. Query FinancialTransactions for case_ids with expenses
2. Query FinancialTransactions for case_ids with payments
3. Find difference (expenses but no payment)
4. Join with ClientCasePortfolio for case details
**Expected Answer:** List of cases with outstanding expenses

---

## Category 7: Time-Based Queries

### Q28: "What's our YTD revenue?"
**Expected Source:** ClientCasePortfolio or FinancialTransactions (depends on definition of "revenue")  
**Expected Query (Cases):** `SELECT SUM(case_value_gbp) FROM Cases WHERE case_start_date >= '2023-01-01'`  
**Expected Query (Invoices):** `SELECT SUM(payment_amount_gbp) FROM FinancialTransactions WHERE transaction_type = 'Invoice' AND transaction_date >= '2023-01-01'`  
**Expected Answer:** Total case value or invoiced amount YTD

---

### Q29: "How many cases were completed in July 2023?"
**Expected Source:** ClientCasePortfolio  
**Expected Query:** `SELECT COUNT(*) FROM Cases WHERE case_completion_date >= '2023-07-01' AND case_completion_date < '2023-08-01'`  
**Expected Answer:** Count of completed cases in July

---

### Q30: "What's our case completion rate?"
**Expected Source:** ClientCasePortfolio  
**Expected Query:** DAX: `Case Completion Rate`  
**Expected Answer:** Percentage of cases with completion dates  
**Measure Used:** Case Completion Rate

---

## Testing Checklist

### Step 3 Testing (Basic Model)
Run queries Q6, Q9, Q18 and observe:
- [ ] Ambiguity in measure selection (multiple revenue measures)
- [ ] Inconsistent results
- [ ] No verified answers hit
- [ ] Lower accuracy (~64%)

### Step 4 Testing (Optimized Model)
Run same queries Q6, Q9, Q18 and observe:
- [ ] ✅ Verified answers hit (VA001, VA002, VA003)
- [ ] ✅ Consistent measure selection
- [ ] ✅ Accurate results (100%)
- [ ] ✅ Descriptions used for context

### Step 5 Testing (With Ontology)
Run queries Q21, Q22, Q23, Q24 and observe:
- [ ] ✅ Entity-based query understanding
- [ ] ✅ Automatic relationship traversal
- [ ] ✅ Contextualized aggregations
- [ ] ✅ Timeseries support

### Step 6 Testing (With Routing)
Run queries across categories and observe:
- [ ] ✅ Q1-Q10 route to ClientCasePortfolio
- [ ] ✅ Q11-Q17 route to FinancialTransactions
- [ ] ✅ Q18-Q20 route correctly based on question
- [ ] ✅ Q25-Q27 use both sources
- [ ] ✅ Routing accuracy ~94%

---

## Troubleshooting

### If Routing is Wrong:
1. Check data source descriptions - Are they clear and distinct?
2. Review example queries - Do they match the question pattern?
3. Inspect run steps - Did routing tool get invoked? (signal of ambiguity)
4. Add routing rules to agent instructions as last resort

### If Query Results are Incorrect:
1. Check measure/column names - Are they descriptive?
2. Review AI Instructions - Is business terminology defined?
3. Verify AI Data Schema - Are relevant objects included?
4. Check Verified Answers - Do they match the question pattern?

### If Response is Slow:
1. Simplify semantic model - Remove unnecessary measures
2. Optimize DAX - Use efficient aggregations
3. Reduce schema selection - Include only necessary tables/columns
4. Add more Verified Answers - Pre-compute common queries

---

## Success Criteria

**Green Light (Passing):**
- ✅ 90%+ routing accuracy
- ✅ 95%+ query accuracy
- ✅ Consistent results across similar questions
- ✅ Response time < 5 seconds for simple queries
- ✅ Verified answers hit for common questions

**Yellow Light (Needs Improvement):**
- ⚠️ 70-90% routing accuracy → Add more example queries
- ⚠️ 85-95% query accuracy → Refine descriptions and instructions
- ⚠️ Occasional inconsistencies → Check for duplicate measures
- ⚠️ Response time 5-10 seconds → Optimize model or add verified answers

**Red Light (Requires Attention):**
- ❌ <70% routing accuracy → Redesign data source descriptions
- ❌ <85% query accuracy → Review semantic model and Prep for AI config
- ❌ Frequent inconsistencies → Consolidate duplicate measures
- ❌ Response time >10 seconds → Optimize model and reduce schema

---

## Query Log Template

Use this template to track query testing results:

| Query # | Question | Expected Source | Actual Source | Expected Answer | Actual Answer | Accuracy | Notes |
|---------|----------|----------------|---------------|-----------------|---------------|----------|-------|
| Q1 | How many active customers? | ClientCase | ClientCase | ~15 | 15 | ✅ | VA004 hit |
| Q6 | Total case value? | ClientCase | ClientCase | £1.08M | £1,085,200 | ✅ | VA001 hit |
| Q11 | Sarah's hours March? | FinTrans | FinTrans | 14.5 hrs | 14.5 | ✅ | Example #1 |

---

**Test thoroughly and iterate based on results!**
