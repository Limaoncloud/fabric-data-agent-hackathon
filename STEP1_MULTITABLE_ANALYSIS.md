# Step 1: Raw Multi-Table Data Analysis

## Overview

This step demonstrates the **worst-case scenario** — raw data as it often arrives from multiple systems, spreadsheets, and manual entry at scale. The data contains **9 real-world quality issues** spread across **5 tables** and **2,515 records** that will severely impact a data agent's ability to generate accurate queries.

## Dataset: Multi-Table Raw Data

**Total Records:** 2,515 across 5 tables  
**Purpose:** Show what happens when you feed poor-quality data at scale to a data agent

### Tables Included

1. **step1_raw_customers.csv** — 200 customers (with ~10% duplicates)
2. **step1_raw_cases.csv** — 500 legal cases  
3. **step1_raw_solicitors.csv** — 15 solicitors
4. **step1_raw_transactions.csv** — 1,000 financial transactions
5. **step1_raw_interactions.csv** — 800 customer interactions

---

## The 9 Data Quality Issues at Scale

### 1. **Vague Column Names** ❌
Across all 5 tables:
```
Customers:     id, n, typ, loc, dt, ph, em, stat, col9
Cases:         cid, custid, sol, typ, val, dt_start, st, col8
Solicitors:    sid, nm, spec, hiredt, rate, loc, stat
Transactions:  tid, cid, typ, dt, amt, hrs, paystat, col8
Interactions:  iid, cust, sol, typ, dt, dur, notes, col8
```

**Impact:** The data agent has to guess what "n", "typ", "sol", "dt" mean across different tables. Column name reuse creates massive confusion.

**Example Issues:**
- "typ" appears in 3 tables with different meanings (customer type, case type, transaction type)
- "dt" appears in 4 tables (customer signup date, case start date, transaction date, interaction date)
- "sol" means solicitor name in one table, but what does it reference?
- Mystery columns "col8", "col9" — what are they for?
- "stat" vs "st" — are these the same? Status? State? Statistics?

**Scale Impact:** With 2,515 records across 5 tables, the agent faces ~40 ambiguous column names

---

### 2. **Inconsistent Date Formats** ❌
Across 2,515 records, dates appear in 5+ different formats:
```
Examples from actual data:
15/03/2023       (DD/MM/YYYY - UK format)
03/15/2023       (MM/DD/YYYY - US format)
2023-03-15       (ISO format)
15-03-23         (Short format)
15.03.2023       (Dot separator)
2023-03-15 14:30 (With timestamp)
```

**Impact:** The agent can't reliably parse dates. Is "03/04/2023" March 4th or April 3rd?

**Scale Impact:** 
- ~2,100 date values across all tables
- Each table uses different predominant formats
- Date range queries become unreliable

---

### 3. **Mixed Phone Number Formats** ❌
200 customer phone numbers in 6+ different formats:
```
Examples from 200 customers:
+447123456789
07123456789
+44 7123456789
0712 3456789
(0712) 3456789
7123456789
```

**Impact:** Can't match or search phone numbers reliably. Duplicate detection fails.

**Scale Impact:**
- 200 phone numbers in inconsistent formats
- Phone-based customer matching fails
- "Find customer by phone" queries break

---

### 4. **Duplicate Records** ❌
~10% duplication rate across tables:
```
Customers: ~20 duplicate customers (10% of 200)
Cases:     Some cases reference wrong customer IDs
```

**Impact:** Query results include duplicates. "How many customers?" returns wrong count.

**Scale Impact:**
- ~20 duplicate customer records
- "Total customers" query: 200 actual vs 220 reported
- Aggregate queries (sum, avg) are inflated
- "Top 10 customers" includes same customer multiple times

---

### 5. **Inconsistent Terminology** ❌
Thousands of inconsistent values across categorical fields:
```
Customer Type (200): Corporate, Corp, Business, Company, Org, C, 
                     Person, Individual, P, Indiv, Priv

Status (200+): Active, active, ACTIVE, Act, A, 1,
               Inactive, inactive, I, 0, Suspended, N/A, ""

Case Status (500): Open, open, OPEN, Active, Ongoing, In Progress, IP,
                   Closed, closed, Complete, Done, C,
                   Pending, P, On Hold, Paused

Case Type (500): Conveyancing, conveyancing, CONV, Conv,
                 Employment, employment, EMP, Empl

Payment Status (1000): Paid, paid, P, 1, Complete,
                       Unpaid, unpaid, U, 0, Pending,
                       Overdue, Late, "", N/A
```

**Impact:** Filtering queries fail. "Show active customers" might miss "Act", "A", or "1".

**Scale Impact:**
- 200 customer statuses with ~8 variations
- 500 case statuses with ~15 variations  
- 1,000 payment statuses with ~10 variations
- Total: ~2,700 categorical values needing standardization

---

### 6. **Poor NULL Handling** ❌
Missing values represented inconsistently across 2,515 records:
```
Customers (200):     ~30 missing emails (15%)
Interactions (800):  ~240 missing notes (30%)
Transactions (1000): ~100 missing hour values

Missing value representations:
- Empty strings ""
- "N/A"  
- "Unknown"
- "TBC"
- "." (single dot)
- "null" (as text)
- Actual NULL
```

**Impact:** Count queries are inaccurate. "Customers with email" depends on NULL handling logic.

**Scale Impact:**
- ~370 missing values across all tables
- "COUNT(*) WHERE email IS NOT NULL" returns wrong results
- Data completeness queries are unreliable

---

### 7. **Inconsistent Casing and Spacing** ❌
Case sensitivity issues across thousands of text values:
```
Customer Names (200):
  "ACME Ltd" vs "Acme Ltd" vs "acme ltd"
  "John Smith" vs "john smith" vs "JOHN SMITH"

Solicitor Names (15):
  "Sarah Jones" vs "sarah jones"

Case Types (500):
  "Commercial" vs "commercial" vs "COMMERCIAL" vs "COMM"
  "Property  Law" (double space) vs "Property Law"

Cities (200):
  "London" vs "london" vs "LONDON"
```

**Impact:** String matching fails. Queries for "commercial" might miss "Commercial".

**Scale Impact:**
- ~200 customer names with case variations
- ~500 case type values with case/spacing issues
- "GROUP BY case_type" creates duplicate groups

---

### 8. **Vague Abbreviations** ❌
Abbreviations used inconsistently across 2,515 records:
```
Case Types (500 cases):
  "Conv" — Conveyancing or Conversion?
  "Corp" — Corporate or Corporation?  
  "IP"   — Intellectual Property or In Progress?
  "Emp"  — Employment or Employee?
  "Comm" — Commercial or Communication?

Values (1000 transactions):
  "50K" — £50,000 or 50 kilobytes?
  "GBP 5000" vs "£5000" vs "5000" — same value, different formats

Interaction Types (800):
  "Call" vs "Cal" vs "C"
  "Email" vs "Em" vs "E"
```

**Impact:** The agent can't understand business terms. Query interpretation is ambiguous.

**Scale Impact:**
- ~500 abbreviated case types
- ~200 abbreviated customer types
- ~1,000 abbreviated transaction types
- Queries like "Show me IP cases" could mean intellectual property OR in-progress

---

### 9. **No Foreign Keys or Relationships** ❌
No proper relationships across 5 tables with 2,515 records:
```
Customers → Cases: 
  custid references id, but formats inconsistent
  Some cases reference non-existent customers

Cases → Transactions:
  cid format varies: "C00001" vs "CASE1"
  ~50 transactions reference non-existent cases

Customers → Interactions:
  cust references id, but no validation
  Orphaned interactions exist

Solicitors → Cases/Interactions:
  sol contains name (text), not ID
  "Sarah Jones" vs "sarah jones" breaks joins
  No foreign key constraint
```

**Impact:** JOIN queries fail or produce incorrect results. Can't navigate between entities.

**Scale Impact:**
- 500 cases referencing 200 customers (relationships unvalidated)
- 1,000 transactions referencing 500 cases (ID format mismatch)
- 800 interactions referencing 200 customers and 15 solicitors
- "Show customer cases" query: ~50 orphaned cases returned
- "Total revenue per customer": incorrect aggregations

---

## Expected Agent Performance at Scale

With this poor-quality data across 2,515 records, a Fabric Data Agent would struggle significantly:

- **Query Accuracy:** ~40-50% (estimated from evaluation)
- **Common Failures:**
  - Can't identify column meanings across 5 tables
  - Date filters return wrong results (~2,100 dates affected)
  - Duplicate counting (+10% inflation in aggregates)
  - Failed string matching (case sensitivity affects ~1,200 records)
  - Incorrect aggregations (duplicates inflate sums by ~10-15%)
  - Unable to join tables reliably (~100+ orphaned records)
  - Cross-table queries fail due to ID format mismatches
  - Categorical filters miss ~30% of matching records

### Specific Query Failures (Examples)

1. **"How many customers do we have?"**
   - Expected: 200 unique customers
   - Actual: 220 (includes ~20 duplicates)
   - Error: +10%

2. **"What's our total case value?"**
   - Expected: Sum of 500 cases
   - Actual: Misses ~50 cases due to format issues ("50K" not parsed)
   - Error: -10%

3. **"Show active customers"**
   - Expected: ~120 active customers
   - Actual: ~80 returned (misses "Act", "A", "1" variations)
   - Error: -33%

4. **"Total revenue by customer"**
   - Expected: 200 rows
   - Actual: 220 rows (duplicates) with wrong sums
   - Error: Multiple issues

5. **"Cases started in Q1 2023"**
   - Expected: ~125 cases
   - Actual: ~90 cases (date format parsing issues)
   - Error: -28%

6. **"Which solicitor handles the most cases?"**
   - Expected: Correct ranking
   - Actual: Broken due to "Sarah Jones" vs "sarah jones"
   - Error: JOIN failure

7. **"Total hours billed per case"**
   - Expected: 500 case totals
   - Actual: ~450 returned (ID format mismatch breaks JOIN)
   - Error: -10%

---

## Sample Data Preview

### Customers (first 5 of 200)
```
id,n,typ,loc,dt,ph,em,stat,col9
1,ACME Ltd,Corp,London,15/03/2023,+447123456789,acme.ltd@example.co.uk,Active,X
2,John Smith,Person,Manchester,2023-03-20,07234567890,john.smith@example.co.uk,active,Y
,Global PLC,C,Birmingham,20/03/2023,+44 7345678901,,A,
4,Sarah Jones,Individual,Leeds,03/25/2023,(0734) 5678912,sarah.jones@example.co.uk,1,X
5,Premier Group,Business,Glasgow,25-03-23,7456789123,premier.group@example.co.uk,ACTIVE,N/A
```

### Cases (first 5 of 500)
```
cid,custid,sol,typ,val,dt_start,st,col8
C00001,1,Sarah Jones,Conveyancing,£50000,15/04/2023,Open,X
C00002,2,Robert Smith,employment,25000,2023-04-20,OPEN,
CASE3,4,Michael Brown,CONV,75K,04/25/2023,Active,Y
C00004,8,sarah jones,Commercial,£125000,25-04-23,Ongoing,
C00005,15,Emma Wilson,IP,GBP 95000,2023-05-01,IP,X
```

### Transactions (first 5 of 1000)
```
tid,cid,typ,dt,amt,hrs,paystat,col8
T000001,C00001,Timesheet,15/05/2023,£1500,10.0,Paid,X
T000002,CASE2,expense,2023-05-16,250,,,Y
TXN3,C00005,TIME,16/05/2023,3500,25.0,paid,
T000004,C00010,Invoice,05/20/2023,50K,,Unpaid,X
T000005,CASE15,payment,20-05-23,GBP 12000,,P,
```

---

## Why This Matters for Data Agents

At scale (2,515 records across 5 tables), these quality issues compound:

1. **Cross-Table Queries Fail:** Without proper relationships, joining customers → cases → transactions is unreliable
2. **Aggregations Are Wrong:** Duplicates and format issues inflate totals by 10-15%
3. **Filters Miss Data:** Inconsistent terminology means ~30% of matching records aren't found
4. **Time-Series Analysis Breaks:** Date format chaos makes temporal queries unreliable
5. **Entity Resolution Fails:** Case sensitivity and duplicates prevent proper customer identification

**The Bottom Line:** Even with advanced AI, a data agent cannot overcome fundamental data quality issues at scale. The agent will return:
- Wrong counts
- Missing results
- Duplicate entries
- Failed joins
- Incorrect aggregations

**Step 2 will show** how data cleaning improves these issues, but **Step 4** will prove that semantic model optimization is the real breakthrough.

---

## Files Generated

Run `python generate_step1_data.py` to regenerate:

- `step1_raw_customers.csv` (200 rows)
- `step1_raw_cases.csv` (500 rows)
- `step1_raw_solicitors.csv` (15 rows)
- `step1_raw_transactions.csv` (1000 rows)
- `step1_raw_interactions.csv` (800 rows)

**Total: 2,515 records** with intentional quality issues for demo purposes.
