# Step 3: Initial Semantic Model (Not Following Best Practices)

## Overview
This semantic model represents common pitfalls and anti-patterns found in real-world Power BI models before optimization for AI. It's intentionally designed to show what NOT to do according to Microsoft Learn best practices.

## ❌ Problems with This Semantic Model

### 1. **Not Using Star Schema** ❌
**Issue:** The model uses a single flat table (`tbl_data`) instead of a proper star schema with fact and dimension tables.

**Current Structure:**
```
tbl_data (everything in one table)
```

**Recommended Structure:**
```
FactCases (transactions/events)
  ├─ case_id
  ├─ customer_id (FK)
  ├─ solicitor_id (FK)
  ├─ case_start_date
  └─ case_value_gbp

DimCustomers (customer attributes)
  ├─ customer_id (PK)
  ├─ customer_name
  ├─ customer_type
  └─ customer_status

DimSolicitors (solicitor attributes)
  ├─ solicitor_id (PK)
  └─ solicitor_name

DimCaseTypes (case type attributes)
  ├─ case_type_id (PK)
  └─ case_type_name

DimDate (date dimension)
  ├─ date_id (PK)
  ├─ year
  ├─ quarter
  └─ month
```

**Impact:** 
- Poor DAX performance
- Harder for AI to understand relationships
- Inefficient query patterns
- Best Practice: *"Semantic models that use flat, denormalized tables make DAX less efficient"*

### 2. **Non-Descriptive Table Name** ❌
**Issue:** `tbl_data` provides no context about what the table contains.

**Better Names:**
- `LegalClientCases`
- `ClientCasePortfolio`
- `CasesAndCustomers`

**Impact:** The DAX generation tool struggles to understand the purpose and content of the table.

### 3. **Relying on Hidden Fields** ❌
**Issue:** Multiple columns are hidden that might be useful:
- `customer_postcode` (hidden)
- `customer_phone` (hidden)
- `customer_email` (hidden)
- `MonthNum` (hidden)
- `YearNum` (hidden)
- `QtrNum` (hidden)

**Why This is Bad:**
- If someone creates a Verified Answer using these fields, it won't work
- Users can't query by these dimensions
- AI can't access this data for natural language queries

**Best Practice Violation:** *"Verified answers won't work if they reference hidden columns in the model"*

### 4. **Including Unnecessary Helper Measures** ❌
**Issue:** The model includes hidden helper measures:
- `_helper_sum`
- `_helper_count`

**Why This is Bad:**
- Adds noise for the DAX generation tool
- Increases parsing complexity
- These aren't business metrics

**Best Practice:** *"When configuring your AI data schema, include only the measures that calculate actual business metrics. Excluding helper measures reduces noise."*

### 5. **Duplicate and Overlapping Measures** ❌
**Issue:** Multiple measures calculate the exact same thing with different names:

**Total Value (5 duplicates!):**
- `TotalVal` = `SUM(tbl_data[case_value_gbp])`
- `TotalValue` = `SUM(tbl_data[case_value_gbp])`
- `Total_Value_GBP` = `SUM(tbl_data[case_value_gbp])`
- `GrossVal` = `SUM(tbl_data[case_value_gbp])`
- `Rev` = `SUM(tbl_data[case_value_gbp])`

**Average Value (2 duplicates):**
- `AvgVal` = `AVERAGE(tbl_data[case_value_gbp])`
- `Avg_Case_Val` = `AVERAGE(tbl_data[case_value_gbp])`

**Case Count (2 duplicates):**
- `CaseCount` = `COUNTROWS(tbl_data)`
- `NumCases` = `COUNTROWS(tbl_data)`

**Impact:**
- Creates ambiguity - which "total sales" should the AI use?
- Confuses users and the DAX generation tool
- Makes responses unpredictable

**Best Practice:** *"Multiple measures that calculate similar metrics create ambiguity. Consolidate or clearly differentiate measures."*

### 6. **Non-Descriptive Measure Names** ❌
**Issue:** Abbreviated or unclear measure names:
- `TotalVal` → Should be `Total Case Value`
- `Rev` → Should be `Revenue` or `Total Revenue`
- `AvgVal` → Should be `Average Case Value`
- `ActiveCnt` → Should be `Active Customer Count`
- `M_01`, `M_02` → Should be `January Cases`, `February Cases`
- `Q1_Val` → Should be `Q1 Case Value`

**Impact:**
- The DAX generation tool has to guess what these abbreviations mean
- Natural language queries become less accurate
- Users don't know which measures to ask about

**Best Practice:** *"Object names like TR_AMT, F_SLS, or DIM_GEO_01 provide no context. Use clear, business-friendly names."*

### 7. **Relying on Implicit Measures** ❌
**Issue:** The `case_value_gbp` column has `summarizeBy: sum` set, creating an implicit measure.

**Why This is Bad:**
- Implicit measures can lead to unpredictable results
- No control over formatting or calculation context
- Harder to track what's being calculated

**Best Practice:** *"Relying on implicit measures can lead to unpredictable results. Create explicit DAX measures for calculations."*

### 8. **Ambiguous Date Fields** ❌
**Issue:** Multiple date columns without clear guidance:
- `case_start_date`
- `case_completion_date`

Plus hidden calculated columns:
- `MonthNum`
- `YearNum`
- `QtrNum`

**Questions:**
- Which date should be used for time-based analysis?
- What date for "cases this quarter"?
- What date for "YTD calculations"?

**Impact:**
- AI doesn't know which date field to use by default
- Inconsistent results across queries
- Confusion about fiscal vs calendar year

**Best Practice:** *"Multiple date columns without clear guidance confuse the AI. Use Verified Answers and AI instructions to specify which date field to use."*

### 9. **No Descriptions on Any Objects** ❌
**Issue:** All measures and columns have empty descriptions:
```json
"description": ""
```

**Impact:**
- DAX generation tool has no additional context
- No synonyms or alternate terms
- No business logic explanations

**Best Practice:** *"Add descriptions to tables, columns, and measures to help the LLM understand the purpose of each object."*

### 10. **No Prep for AI Configuration** ❌
**Issue:** The model has NO Prep for AI setup:
```json
"prepForAI": {
  "configured": false,
  "aiDataSchema": null,
  "verifiedAnswers": [],
  "aiInstructions": null
}
```

**Missing Components:**

#### a) No AI Data Schema
- Haven't selected which tables/columns/measures should be prioritized for AI
- All objects are available, creating noise
- No focused subset for the data agent

#### b) No Verified Answers
- No pre-configured question-answer pairs
- Common questions will require full DAX generation each time
- No consistency for frequently asked questions

#### c) No AI Instructions
- No business terminology definitions
- No guidance on fiscal year vs calendar year
- No explanation of what "high value" means
- No default analysis preferences

**Best Practice:** *"When querying semantic models, the DAX generation tool relies solely on metadata and Prep for AI configurations. Proper Prep for AI configuration is essential."*

### 11. **Missing Business Context** ❌
**Issue:** Measures like `PendingVal`, `ActiveCnt` don't explain:
- What makes a case "Active"?
- What does "Pending" mean?
- Should we filter by `customer_status` or `payment_status`?

### 12. **Hard-Coded Month and Quarter Measures** ❌
**Issue:** Individual measures for each month and quarter:
- `M_01`, `M_02`, etc.
- `Q1_Val`, etc.

**Why This is Bad:**
- Not scalable (would need 12 month measures)
- Hard-coded values in DAX
- Better to use proper date dimension
- AI can't generalize to other time periods

## Example Query Problems

Let's see how these issues impact actual queries:

### Query 1: "What's our total revenue?"

**Problem:** Which measure should be used?
- `TotalVal`?
- `TotalValue`?
- `Total_Value_GBP`?
- `GrossVal`?
- `Rev`?

**Result:** Unpredictable - AI picks randomly

---

### Query 2: "Show me case value by month"

**Problem:** 
- Should use `case_start_date` or `case_completion_date`?
- Hidden `MonthNum` column not accessible
- Hard-coded `M_01`, `M_02` measures don't scale

**Result:** Likely generates inefficient DAX or returns error

---

### Query 3: "Who are our top solicitors?"

**Problem:**
- No star schema, so solicitor data is denormalized
- Unclear what "top" means (by case count? by case value?)
- Which measure to use for value?

**Result:** Ambiguous results

---

### Query 4: "What's the average value of corporate clients' cases?"

**Problem:**
- Which average measure: `AvgVal` or `Avg_Case_Val`?
- No clear dimension structure
- Flat table makes complex filtering harder

**Result:** May get incorrect result or inefficient query

## Impact on Data Agent Performance

| Aspect | Impact | Severity |
|--------|--------|----------|
| **Query Accuracy** | Multiple similar measures confuse AI | 🔴 High |
| **Query Performance** | Flat table structure inefficient | 🔴 High |
| **Response Time** | No verified answers means full generation each time | 🟡 Medium |
| **Consistency** | Ambiguous measures lead to variable results | 🔴 High |
| **Usability** | Abbreviated names hard to understand | 🟡 Medium |
| **Completeness** | Hidden fields limit query capabilities | 🟡 Medium |

## What's Missing for AI Readiness

1. ❌ Star schema design
2. ❌ Descriptive table and measure names
3. ❌ AI Data Schema configuration
4. ❌ Verified Answers for common questions
5. ❌ AI Instructions for business context
6. ❌ Object descriptions and synonyms
7. ❌ Consolidated measures (remove duplicates)
8. ❌ Proper date dimension
9. ❌ Clear business metric definitions
10. ❌ Explicit DAX measures (no implicit)

## Next Steps

In **Step 4**, we'll optimize this semantic model by:
1. Restructuring to star schema (if possible) or clarifying relationships
2. Renaming all objects with business-friendly names
3. Removing duplicate measures
4. Configuring AI Data Schema
5. Creating Verified Answers
6. Adding AI Instructions
7. Adding descriptions to all objects
8. Unhiding useful fields or removing unnecessary hidden fields

This will dramatically improve the data agent's accuracy and reliability!
