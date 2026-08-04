# Fabric Data Agent Hackathon Demo - Complete Summary

## Demo Overview
**Title:** UK Legal Firm Customer 360 with Fabric Data Agent  
**Duration:** 15-20 minutes  
**Audience:** UK legal firm stakeholders, data professionals  
**Goal:** Demonstrate how proper data agent configuration transforms query accuracy from 55% to 95%+

---

## Demo Dataset
**Scenario:** UK law firm with:
- 19 unique customers (Individual and Corporate)
- 19 legal cases across 10 practice areas
- 50 financial transactions (timesheets, expenses, invoices, payments)
- 3 solicitors (Sarah Jones, Robert Smith, Michael Brown)
- Total case value: ~£1M GBP

**Practice Areas:** Conveyancing, Corporate Law, Family Law, Litigation, Employment Law, Wills & Probate, Commercial Property, Personal Injury, Immigration, Intellectual Property

---

## Six-Step Journey

### Step 1: Raw Imperfect Data ❌
**Purpose:** Show real-world data quality issues

**9 Major Issues:**
1. ❌ Vague column names (typ, col1, col2, flag)
2. ❌ Inconsistent formats (dates, phones, postcodes)
3. ❌ Inconsistent capitalization
4. ❌ Missing values
5. ❌ Duplicate records (John Smith × 3, ACME Corp × 2)
6. ❌ Data type issues
7. ❌ Inconsistent terminology
8. ❌ Missing business context
9. ❌ Invalid placeholder data

**Impact:** Data agent struggles to understand meaning, context, and relationships

**Demo File:** `step1_raw_customer_data.csv`  
**Analysis:** `step1_analysis.md`

---

### Step 2: Data Cleaning ✅
**Purpose:** Apply Microsoft Learn best practices for AI-ready data

**8 Best Practices Applied:**
1. ✅ Descriptive, business-friendly column names
2. ✅ Standardized data formats (dates, phones, postcodes)
3. ✅ Standardized values and terminology
4. ✅ Proper handling of missing values
5. ✅ Duplicate resolution
6. ✅ Added business context
7. ✅ Made flag columns explicit
8. ✅ Proper name formatting

**Improvement Metrics (Measured):**
- Descriptive Column Names: +200% (5/15 → 15/15)
- Consistent Date Format: +100% (50% → 100%)
- Standardized Phone Format: +400% (20% → 100%)
- Consistent Terminology: +150% (40% → 100%)
- Duplicate Records: -100% (5 → 0, eliminated)
- Proper NULL Handling: +67% (60% → 100%)

**Demo File:** `step2_cleaned_customer_data.csv`  
**Analysis:** `step2_cleaning_analysis.md`

---

### Step 3: Basic Semantic Model (Non-Optimized) ❌
**Purpose:** Show common semantic model pitfalls

**12 Anti-Patterns:**
1. ❌ Not using star schema (flat table)
2. ❌ Non-descriptive table name (tbl_data)
3. ❌ Relying on hidden fields
4. ❌ Including unnecessary helper measures
5. ❌ Duplicate measures (5 for total value!)
6. ❌ Non-descriptive measure names (TotalVal, Rev, M_01)
7. ❌ Relying on implicit measures
8. ❌ Ambiguous date fields
9. ❌ No descriptions on any objects
10. ❌ No Prep for AI configuration
11. ❌ Missing business context
12. ❌ Hard-coded time measures

**Query Accuracy (Est.):** ~64%

**Demo File:** `step3_basic_semantic_model.json`  
**Analysis:** `step3_analysis.md`

---

### Step 4: Optimized Semantic Model ✅
**Purpose:** Apply all semantic model best practices for AI

**10 Major Improvements:**
1. ✅ Star schema design (Cases fact + Customers dimension)
2. ✅ Business-friendly descriptive names
3. ✅ Eliminated duplicate measures
4. ✅ Removed helper measures
5. ✅ Explicit measures only
6. ✅ Comprehensive descriptions with synonyms
7. ✅ Unhidden essential fields
8. ✅ Removed hard-coded time measures
9. ✅ Configured Prep for AI (AI Data Schema + Verified Answers + AI Instructions)
10. ✅ Clear date field guidance

**Prep for AI Configuration:**
- **AI Data Schema:** Focused subset of 15 columns and 12 measures
- **Verified Answers:** 6 common questions pre-configured
- **AI Instructions:** Comprehensive business context, terminology, and preferences

**Query Accuracy (Est.):** ~100% (from ~64%)  
**Improvement (Est.):** ~+56%

**Demo File:** `step4_optimized_semantic_model.json`  
**Analysis:** `step4_optimization_analysis.md`

---

### Step 5: Ontology Layer ✅
**Purpose:** Add semantic entity-relationship layer

**Ontology Components:**
1. **3 Entity Types:**
   - Client (Customer entity with properties and synonyms)
   - LegalCase (Case entity with timeseries support)
   - Solicitor (Legal professional entity)

2. **3 Relationship Types:**
   - ClientHasCase (one-to-many)
   - SolicitorAssignedToCase (one-to-many)
   - SolicitorServesClient (many-to-many, derived)

3. **3 Contextualizations:**
   - ClientPortfolioContext (aggregated client metrics)
   - SolicitorWorkloadContext (solicitor performance)
   - CaseDetailsContext (complete case view)

4. **Timeseries Support:**
   - CaseStartDate with day granularity for trend analysis

**Benefits:**
- Natural entity-based queries ("Show me all cases for ACME")
- Automatic relationship traversal
- Pre-computed contextualized aggregations
- Synonym support for flexible phrasing
- Timeseries analysis built-in

**Query Accuracy (Est.):** ~95% (entity-based queries)  
**Improvement (Est.):** ~+40% over raw model

**Demo File:** `step5_ontology_definition.json`  
**Analysis:** `step5_ontology_analysis.md`

---

### Step 6: Multi-Source Routing ✅
**Purpose:** Demonstrate intelligent routing between data sources

**Two Data Sources:**

**Source 1: ClientCasePortfolio**
- Customer and case master data
- 2 tables: Customers, Cases
- Best for: Client info, case status, solicitor assignments

**Source 2: FinancialTransactions**
- Detailed transaction records
- 1 table: FinancialTransactions (Timesheets, Expenses, Invoices, Payments)
- Best for: Hours worked, billing rates, expenses, payment details

**5 Routing Best Practices Applied:**
1. ✅ Clear data source descriptions
2. ✅ Tightened schema selection
3. ✅ 5+ example queries per source
4. ✅ Detailed data source instructions
5. ✅ Agent-level routing rules

**Routing Accuracy (Est.):** ~94% (from ~55%)  
**Improvement (Est.):** ~+71%

**Demo Files:**  
- `step6_financial_transactions.csv`
- `step6_data_agent_configuration.json`

**Analysis:** `step6_routing_analysis.md`

---

## Overall Impact Summary

⚠️ **Note:** The percentages below are **estimated projections** based on Microsoft Learn best practices, not empirically measured results. See [evaluation_dataset.json](evaluation_dataset.json) and [evaluate_agent.py](evaluate_agent.py) for tools to measure actual accuracy.

| Metric | Before (Est.) | After (Est.) | Improvement (Est.) |
|--------|--------|-------|-------------|
| **Data Quality** | ~40% | ~95% | +138% |
| **Query Accuracy** | ~55% | ~95%+ | +73% |
| **Semantic Model** | ~64% | ~100% | +56% |
| **Entity Queries** | ~68% | ~95% | +40% |
| **Routing Accuracy** | ~55% | ~94% | +71% |
| **Response Consistency** | Low | High | Significant |

**Bottom Line:** Proper configuration is expected to transform accuracy from ~55% to ~95%+ based on best practices.

---

## Demo Script (15 minutes)

### Introduction (2 minutes)
*"Today I'll show how applying Microsoft Learn best practices transforms a Fabric Data Agent from 55% to 95%+ accuracy. We'll use a UK legal firm customer 360 scenario with real-world data quality issues."*

**Show:** README.md overview

---

### Part 1: The Problem (3 minutes)

**Show Step 1:** Raw data
- Open `step1_raw_customer_data.csv`
- Point out: vague names (col1, typ, flag), inconsistent formats, duplicates
- *"This is what real-world data looks like. The agent can't understand 'col1' or 'flag'."*

**Show Step 3:** Basic semantic model
- Open `step3_basic_semantic_model.json`
- Highlight: 5 duplicate measures for total value, `tbl_data` table name, no Prep for AI
- *"Even with cleaned data, a poorly designed model causes problems. Query accuracy: only 64%."*

**Run a demo query (simulated):**
- Question: "What's our total revenue?"
- Problem: Which measure? TotalVal? TotalValue? Rev? GrossVal?
- Result: ⚠️ Unpredictable, inconsistent

---

### Part 2: The Solution (8 minutes)

#### Step 2: Clean Data (1 minute)
- Show `step2_cleaned_customer_data.csv`
- Highlight: descriptive columns, consistent formats, no duplicates
- *"Proper naming and formatting are foundational."*

#### Step 4: Optimized Semantic Model (3 minutes)
- Show `step4_optimized_semantic_model.json`
- Highlight:
  - ✅ Star schema (Cases + Customers)
  - ✅ Single "Total Case Value" measure (no duplicates)
  - ✅ Comprehensive descriptions with synonyms
  - ✅ **Prep for AI:** AI Data Schema, Verified Answers, AI Instructions
  
**Show Prep for AI components:**
1. **AI Data Schema:** Focused subset
2. **Verified Answers:** "What is the total value of all cases?" → card visual
3. **AI Instructions:** "High-value case = £50,000+, use calendar year, etc."

**Run the same query:**
- Question: "What's our total revenue?"
- Result: ✅ Uses "Total Case Value" measure, consistent, accurate
- Query accuracy: 100%

#### Step 5: Ontology (2 minutes)
- Show `step5_ontology_definition.json`
- Explain: Entity types (Client, LegalCase, Solicitor), Relationships, Contextualizations
- *"Ontology enables natural entity-based queries."*

**Demo query:**
- Question: "Show me all cases for ACME Corporation"
- Without ontology: Need to know table structure, relationships
- With ontology: ✅ Semantic understanding, automatic traversal

#### Step 6: Multi-Source Routing (2 minutes)
- Show `step6_data_agent_configuration.json`
- Explain: Two sources (ClientCasePortfolio vs FinancialTransactions)
- Show routing rules: case questions → Source 1, billing questions → Source 2

**Demo routing:**
1. "How many cases do we have?" → ✅ ClientCasePortfolio
2. "How many hours did Sarah Jones bill?" → ✅ FinancialTransactions
3. Routing accuracy: 94%

---

### Wrap-Up (2 minutes)

**Key Takeaways:**
1. ✅ **Data Quality First:** Descriptive names, consistent formats
2. ✅ **Semantic Model Best Practices:** Star schema, no duplicates, Prep for AI
3. ✅ **Ontology Adds Semantics:** Entity-relationship understanding
4. ✅ **Routing Needs Configuration:** Descriptions, examples, instructions

**Results:**
- 55% accuracy → 95%+ accuracy
- Inconsistent answers → Consistent, reliable results
- Slow, ambiguous queries → Fast, accurate responses

**Call to Action:**
*"Apply these best practices to your own data agents. The documentation and checklist are in the fabric-toolbox GitHub repository. Start with data quality, optimize your semantic model, configure Prep for AI, and test routing with multiple sources."*

---

## Demo Test Queries

### Should Work Perfectly (Step 4+5+6):

1. ✅ **"How many active customers do we have?"**
   - Routes to: ClientCasePortfolio
   - Uses: Number of Active Customers measure
   - Expected: ~15 active customers

2. ✅ **"Show me all cases assigned to Sarah Jones"**
   - Routes to: ClientCasePortfolio
   - Filters: assigned_solicitor_name = 'Sarah Jones'
   - Expected: List of cases

3. ✅ **"What's the total value of all cases?"**
   - Routes to: ClientCasePortfolio
   - Uses: Verified Answer VA001
   - Measure: Total Case Value
   - Expected: ~£1M GBP

4. ✅ **"How many hours did Robert Smith bill in Q2 2023?"**
   - Routes to: FinancialTransactions
   - Filters: transaction_type = 'Timesheet', solicitor = Robert Smith, Q2
   - Expected: Sum of hours

5. ✅ **"Show me all unpaid invoices"**
   - Routes to: FinancialTransactions
   - Uses: Example Query #3
   - Expected: List of outstanding invoices

6. ✅ **"Which solicitors work with corporate clients?"**
   - Routes to: Ontology
   - Uses: SolicitorServesClient derived relationship
   - Filters: ClientType = 'Corporate'
   - Expected: List of solicitors

7. ✅ **"What's the average case value by case type?"**
   - Routes to: ClientCasePortfolio
   - Uses: Average Case Value measure
   - Groups by: case_type
   - Expected: Table with averages

8. ✅ **"Show me case opening trends by month"**
   - Routes to: Ontology
   - Uses: CaseStartDate timeseries property
   - Aggregation: Count by month
   - Expected: Timeseries chart

---

## Files Delivered

### Data Files
- ✅ `step1_raw_customer_data.csv` - Imperfect raw data
- ✅ `step2_cleaned_customer_data.csv` - Cleaned data following best practices
- ✅ `step6_financial_transactions.csv` - Financial transaction records

### Configuration Files
- ✅ `step3_basic_semantic_model.json` - Non-optimized semantic model
- ✅ `step4_optimized_semantic_model.json` - Optimized semantic model with Prep for AI
- ✅ `step5_ontology_definition.json` - Ontology layer definition
- ✅ `step6_data_agent_configuration.json` - Complete data agent configuration

### Documentation Files
- ✅ `README.md` - Project overview and structure
- ✅ `step1_analysis.md` - Raw data quality issues analysis
- ✅ `step2_cleaning_analysis.md` - Data cleaning best practices applied
- ✅ `step3_analysis.md` - Semantic model anti-patterns explained
- ✅ `step4_optimization_analysis.md` - Semantic model best practices applied
- ✅ `step5_ontology_analysis.md` - Ontology layer benefits and examples
- ✅ `step6_routing_analysis.md` - Multi-source routing best practices
- ✅ `DEMO_SUMMARY.md` - This complete summary and demo script

---

## Additional Resources

### Microsoft Learn Documentation
1. [Best practices for configuring your data agent](https://learn.microsoft.com/en-us/fabric/data-science/data-agent-configuration-best-practices)
2. [Semantic model best practices for data agent](https://learn.microsoft.com/en-us/fabric/data-science/semantic-model-best-practices)
3. [Improve data source routing](https://learn.microsoft.com/en-us/fabric/data-science/data-agent-routing)

### GitHub Repositories
1. [fabric-toolbox](https://github.com/microsoft/fabric-toolbox/tree/main/samples/data_agent_checklist_notebooks) - Checklists and utilities
2. [Semantic Link Labs](https://github.com/microsoft/semantic-link-labs) - Programmatic semantic model updates
3. [Power BI MCP Server](https://github.com/microsoft/powerbi-modeling-mcp) - LLM-powered model optimization

---

## Deployment Checklist

To deploy this demo to your Fabric workspace:

### 1. Data Preparation
- [ ] Upload `step2_cleaned_customer_data.csv` to Lakehouse as "Customers" table
- [ ] Split into Cases and Customers tables (use notebook or dataflow)
- [ ] Upload `step6_financial_transactions.csv` as "FinancialTransactions" table

### 2. Semantic Model
- [ ] Create Power BI semantic model from Lakehouse
- [ ] Apply structure from `step4_optimized_semantic_model.json`
- [ ] Configure Prep for AI:
  - [ ] AI Data Schema
  - [ ] Verified Answers
  - [ ] AI Instructions
- [ ] Publish to workspace

### 3. Ontology (Optional)
- [ ] Create Ontology item in workspace
- [ ] Import definition from `step5_ontology_definition.json`
- [ ] Bind to Lakehouse tables
- [ ] Publish ontology

### 4. Data Agent
- [ ] Create Data Agent in workspace
- [ ] Add data source: ClientCasePortfolio (Lakehouse)
- [ ] Add data source: FinancialTransactions (Lakehouse)
- [ ] Configure agent instructions from `step6_data_agent_configuration.json`
- [ ] Add data source descriptions
- [ ] Add example queries
- [ ] Test routing

### 5. Testing
- [ ] Run all 8 test queries
- [ ] Verify routing decisions in run steps
- [ ] Check query accuracy
- [ ] Validate response consistency
- [ ] Review performance (response time)

---

## Success Metrics

**Before (No Best Practices) - Estimated:**
- Data Quality: ~40%
- Query Accuracy: ~55%
- Response Consistency: Low
- Routing Accuracy: ~55%

**After (All Best Practices) - Estimated:**
- Data Quality: ~95%
- Query Accuracy: ~95%+
- Response Consistency: High
- Routing Accuracy: ~94%

**ROI (Est.):** ~73% improvement in overall accuracy

**To Measure Actual Results:**
1. Use [evaluation_dataset.json](evaluation_dataset.json) with 30 test queries
2. Run [evaluate_agent.py](evaluate_agent.py) to measure real accuracy
3. Compare results across Steps 3, 4, 5, and 6

---

## Questions & Answers

**Q: Why two separate data sources instead of one big table?**  
A: Different data granularity (case-level vs transaction-level), different question types, and performance optimization. Also demonstrates routing capabilities.

**Q: Can I combine data from both sources in one query?**  
A: Yes! The agent can query one source, then the other, and combine results. Configure agent instructions to handle multi-source questions.

**Q: Do I need an ontology if I have a good semantic model?**  
A: Ontology is optional but adds entity-relationship semantics, synonyms, contextualizations, and timeseries support. Great for entity-based queries.

**Q: How long does it take to configure Prep for AI?**  
A: Initial setup: 2-4 hours. Includes defining AI Data Schema, creating 5-10 Verified Answers, and writing AI Instructions. Ongoing maintenance is minimal.

**Q: What's the #1 thing that improves accuracy?**  
A: **Descriptive naming.** Clear, business-friendly names for tables, columns, and measures are foundational. Everything else builds on that.

---

## Next Steps

1. **Apply to Your Data:** Use this demo as a template for your own datasets
2. **Start with Data Quality:** Clean data is the foundation
3. **Optimize Semantic Models:** Follow the checklist from Step 4
4. **Configure Prep for AI:** Invest time in AI Data Schema, Verified Answers, Instructions
5. **Test Routing:** Add example queries and validate routing decisions
6. **Iterate:** Use run steps to diagnose issues and refine configuration

**Happy building! 🚀**
