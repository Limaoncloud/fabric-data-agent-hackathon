# Fabric Data Agent Demo - Complete Deployment Guide

## Overview

This guide walks you through deploying all 6 steps of the UK Legal Firm Customer 360 demo to Microsoft Fabric.

**Time Required:** ~2-3 hours for complete deployment  
**Prerequisites:** Fabric workspace with Contributor/Admin access, Power BI Premium/Fabric capacity

---

## 📋 Pre-Deployment Checklist

Before you begin, ensure you have:

- ✅ **Fabric Workspace** with adequate capacity (F2 or higher recommended)
- ✅ **Power BI Desktop** (latest version) for semantic model creation
- ✅ **Azure CLI** installed (`az --version` to verify)
- ✅ **Fabric login** configured (`az login`)
- ✅ **Data files generated** (run `python step1/generate_step1_data.py` and `python step2/generate_step2_data.py`)
- ✅ **Workspace permissions** (Contributor or Admin role)

---

## 🎯 Deployment Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    FABRIC WORKSPACE                          │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  STEP 1 & 2: DATA LAYER                                     │
│  ┌────────────────────────────────────────────┐             │
│  │  Lakehouse: LegalFirmDemo                  │             │
│  │  ├─ Tables/                                │             │
│  │  │  ├─ step1_raw_customers (200)           │             │
│  │  │  ├─ step1_raw_cases (500)               │             │
│  │  │  ├─ step1_raw_solicitors (15)           │             │
│  │  │  ├─ step1_raw_transactions (1000)       │             │
│  │  │  ├─ step1_raw_interactions (800)        │             │
│  │  │  ├─ step2_cleaned_customers (166)       │             │
│  │  │  ├─ step2_cleaned_cases (500)           │             │
│  │  │  ├─ step2_cleaned_solicitors (15)       │             │
│  │  │  ├─ step2_cleaned_transactions (1000)   │             │
│  │  │  └─ step2_cleaned_interactions (800)    │             │
│  └────────────────────────────────────────────┘             │
│                                                              │
│  STEP 3 & 4: SEMANTIC MODEL LAYER                           │
│  ┌────────────────────────────────────────────┐             │
│  │  Semantic Model: LegalFirmBasic (Step 3)   │             │
│  │  └─ Single table, anti-patterns, flat      │             │
│  │                                             │             │
│  │  Semantic Model: LegalFirmOptimized (Step 4)│            │
│  │  ├─ Star schema (5 tables)                 │             │
│  │  ├─ Prep for AI configured                 │             │
│  │  │  ├─ AI Data Schema (20 cols, 15 measures)│           │
│  │  │  ├─ Verified Answers (6 answers)        │             │
│  │  │  └─ AI Instructions (business rules)    │             │
│  │  └─ Relationships & hierarchies            │             │
│  └────────────────────────────────────────────┘             │
│                                                              │
│  STEP 5: ONTOLOGY LAYER (Optional - Preview)               │
│  ┌────────────────────────────────────────────┐             │
│  │  Ontology: LegalFirmOntology               │             │
│  │  ├─ Entities: Client, Case, Solicitor,    │             │
│  │  │            Transaction, Interaction     │             │
│  │  ├─ Relationships: ClientHasCase, etc.    │             │
│  │  └─ Contextualizations                    │             │
│  └────────────────────────────────────────────┘             │
│                                                              │
│  STEP 6: DATA AGENT                                         │
│  ┌────────────────────────────────────────────┐             │
│  │  Data Agent: LegalFirmAgent                │             │
│  │  ├─ Source 1: ClientCasePortfolio          │             │
│  │  ├─ Source 2: FinancialTransactions        │             │
│  │  └─ Routing rules & examples               │             │
│  └────────────────────────────────────────────┘             │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 🚀 Step-by-Step Deployment

### **Step 0: Setup Environment Variables**

```powershell
# Set your workspace details
$WORKSPACE_NAME = "YourFabricWorkspace"
$LAKEHOUSE_NAME = "LegalFirmDemo"

# Get workspace ID (requires az login and Fabric CLI extension)
az login
$WORKSPACE_ID = (az rest --method GET --url "https://api.fabric.microsoft.com/v1/workspaces" | ConvertFrom-Json).value | Where-Object {$_.displayName -eq $WORKSPACE_NAME} | Select-Object -ExpandProperty id

Write-Host "Workspace ID: $WORKSPACE_ID"
```

---

## 📊 STEP 1 & 2: Deploy Data Layer (Lakehouse)

### **Option A: Via Fabric Portal (Recommended for Demo)**

#### 1. Create Lakehouse
1. Open your Fabric workspace: https://app.fabric.microsoft.com/
2. Click **+ New** → **Lakehouse** → Name it `LegalFirmDemo`
3. Click **Create**

#### 2. Upload Raw Data (Step 1)
1. In the Lakehouse, go to **Tables**
2. Click **Get data** → **Upload files**
3. Upload all 5 Step 1 CSV files:
   - `step1/step1_raw_customers.csv`
   - `step1/step1_raw_cases.csv`
   - `step1/step1_raw_solicitors.csv`
   - `step1/step1_raw_transactions.csv`
   - `step1/step1_raw_interactions.csv`
4. For each file:
   - Click **Load to new table**
   - Keep suggested table name (e.g., `step1_raw_customers`)
   - Click **Load**

#### 3. Upload Cleaned Data (Step 2)
1. Repeat the same process for Step 2 files:
   - `step2/step2_cleaned_customers.csv`
   - `step2/step2_cleaned_cases.csv`
   - `step2/step2_cleaned_solicitors.csv`
   - `step2/step2_cleaned_transactions.csv`
   - `step2/step2_cleaned_interactions.csv`

**Result:** You now have 10 tables in your Lakehouse (5 raw + 5 cleaned)

### **Option B: Via Notebook (Automated)**

1. Create a new **Fabric Notebook** in your workspace
2. Run this code:

```python
# Load CSV files into Lakehouse tables
import notebookutils

# Step 1: Raw data
df_raw_customers = spark.read.csv("/lakehouse/default/Files/step1_raw_customers.csv", header=True, inferSchema=True)
df_raw_customers.write.mode("overwrite").saveAsTable("step1_raw_customers")

df_raw_cases = spark.read.csv("/lakehouse/default/Files/step1_raw_cases.csv", header=True, inferSchema=True)
df_raw_cases.write.mode("overwrite").saveAsTable("step1_raw_cases")

df_raw_solicitors = spark.read.csv("/lakehouse/default/Files/step1_raw_solicitors.csv", header=True, inferSchema=True)
df_raw_solicitors.write.mode("overwrite").saveAsTable("step1_raw_solicitors")

df_raw_transactions = spark.read.csv("/lakehouse/default/Files/step1_raw_transactions.csv", header=True, inferSchema=True)
df_raw_transactions.write.mode("overwrite").saveAsTable("step1_raw_transactions")

df_raw_interactions = spark.read.csv("/lakehouse/default/Files/step1_raw_interactions.csv", header=True, inferSchema=True)
df_raw_interactions.write.mode("overwrite").saveAsTable("step1_raw_interactions")

# Step 2: Cleaned data
df_cleaned_customers = spark.read.csv("/lakehouse/default/Files/step2_cleaned_customers.csv", header=True, inferSchema=True)
df_cleaned_customers.write.mode("overwrite").saveAsTable("step2_cleaned_customers")

df_cleaned_cases = spark.read.csv("/lakehouse/default/Files/step2_cleaned_cases.csv", header=True, inferSchema=True)
df_cleaned_cases.write.mode("overwrite").saveAsTable("step2_cleaned_cases")

df_cleaned_solicitors = spark.read.csv("/lakehouse/default/Files/step2_cleaned_solicitors.csv", header=True, inferSchema=True)
df_cleaned_solicitors.write.mode("overwrite").saveAsTable("step2_cleaned_solicitors")

df_cleaned_transactions = spark.read.csv("/lakehouse/default/Files/step2_cleaned_transactions.csv", header=True, inferSchema=True)
df_cleaned_transactions.write.mode("overwrite").saveAsTable("step2_cleaned_transactions")

df_cleaned_interactions = spark.read.csv("/lakehouse/default/Files/step2_cleaned_interactions.csv", header=True, inferSchema=True)
df_cleaned_interactions.write.mode("overwrite").saveAsTable("step2_cleaned_interactions")

print("✅ All 10 tables loaded successfully!")
print(f"📊 Total records: {df_raw_customers.count() + df_raw_cases.count() + df_raw_solicitors.count() + df_raw_transactions.count() + df_raw_interactions.count()}")
```

### **Verify Data Load**

```sql
-- Run in Lakehouse SQL Endpoint
SELECT 'step1_raw_customers' as table_name, COUNT(*) as row_count FROM step1_raw_customers
UNION ALL
SELECT 'step1_raw_cases', COUNT(*) FROM step1_raw_cases
UNION ALL
SELECT 'step1_raw_solicitors', COUNT(*) FROM step1_raw_solicitors
UNION ALL
SELECT 'step1_raw_transactions', COUNT(*) FROM step1_raw_transactions
UNION ALL
SELECT 'step1_raw_interactions', COUNT(*) FROM step1_raw_interactions
UNION ALL
SELECT 'step2_cleaned_customers', COUNT(*) FROM step2_cleaned_customers
UNION ALL
SELECT 'step2_cleaned_cases', COUNT(*) FROM step2_cleaned_cases
UNION ALL
SELECT 'step2_cleaned_solicitors', COUNT(*) FROM step2_cleaned_solicitors
UNION ALL
SELECT 'step2_cleaned_transactions', COUNT(*) FROM step2_cleaned_transactions
UNION ALL
SELECT 'step2_cleaned_interactions', COUNT(*) FROM step2_cleaned_interactions;
```

**Expected Output:**
```
table_name                      row_count
step1_raw_customers             200
step1_raw_cases                 500
step1_raw_solicitors            15
step1_raw_transactions          1000
step1_raw_interactions          800
step2_cleaned_customers         166
step2_cleaned_cases             500
step2_cleaned_solicitors        15
step2_cleaned_transactions      1000
step2_cleaned_interactions      800
```

✅ **Checkpoint:** You now have all data in Fabric Lakehouse!

---

## 🎨 STEP 3: Create Basic Semantic Model (Anti-Patterns)

### **Purpose:** Demonstrate poor practices and low accuracy (~57%)

#### **Option A: Power BI Desktop (Manual)**

1. **Open Power BI Desktop**
2. **Get Data** → **Power Platform** → **Microsoft Fabric** → **Lakehouse**
3. **Connect** to your `LegalFirmDemo` lakehouse
4. **Select Step 1 raw tables only** (demonstrate poor data quality impact)
5. **Load** all 5 raw tables

6. **Create a flat model (anti-pattern):**
   - Do NOT create relationships between tables
   - Keep all tables independent

7. **Create duplicate measures (anti-pattern):**
   ```dax
   Total Cases = COUNTROWS(step1_raw_cases)
   TotalCases = COUNTROWS(step1_raw_cases)  
   total_cases = COUNTROWS(step1_raw_cases)
   Case Count = COUNTROWS(step1_raw_cases)
   ```

8. **Create ambiguous measures:**
   ```dax
   Total = SUM(step1_raw_cases[val])
   Count = COUNTROWS(step1_raw_customers)
   Value = SUM(step1_raw_transactions[amt])
   ```

9. **Do NOT configure Prep for AI** (leave blank)

10. **Save** as `LegalFirmBasic.pbix`

11. **Publish** to your Fabric workspace

**Result:** Low accuracy semantic model for Step 3 comparison

#### **Option B: Using JSON Definition (Advanced)**

The `step3/step3_basic_semantic_model.json` file contains the model definition. You can use Power BI Project (PBIP) format:

1. Create a new folder: `LegalFirmBasic`
2. Place JSON contents in `definition.pbidataset` (PBIP format)
3. Open with Power BI Desktop
4. Publish to workspace

---

## 🌟 STEP 4: Create Optimized Semantic Model (100% Accuracy!)

### **Purpose:** Demonstrate best practices and achieve 100% accuracy

#### **Create Star Schema Model**

1. **Open Power BI Desktop**
2. **Get Data** → **Microsoft Fabric** → **Lakehouse**
3. **Connect** to `LegalFirmDemo`
4. **Select Step 2 cleaned tables** (all 5 tables)
5. **Load** tables

#### **Create Relationships (Star Schema)**

Go to **Model View** and create these relationships:

```
Customers (1) → (*) Cases
  - From: Customers[customer_id]
  - To: Cases[customer_id]
  - Cardinality: One to Many
  - Cross filter: Both directions

Cases (1) → (*) Transactions
  - From: Cases[case_id]
  - To: Transactions[case_id]
  - Cardinality: One to Many
  - Cross filter: Single

Customers (1) → (*) Interactions
  - From: Customers[customer_id]
  - To: Interactions[customer_id]
  - Cardinality: One to Many
  - Cross filter: Single

Solicitors (1) → (*) Cases
  - From: Solicitors[solicitor_name]
  - To: Cases[solicitor_name]
  - Cardinality: One to Many (Note: Not ideal, should use ID)
  - Cross filter: Single
```

#### **Create Measures Table**

1. Create a new **blank table** named `_Measures`
2. Add these measures:

```dax
-- Customer Metrics
Total Customers = COUNTROWS(Customers)
Active Customers = CALCULATE(COUNTROWS(Customers), Customers[status] = "Active")
Corporate Customers = CALCULATE(COUNTROWS(Customers), Customers[customer_type] = "Corporate")

-- Case Metrics
Total Cases = COUNTROWS(Cases)
Open Cases = CALCULATE(COUNTROWS(Cases), Cases[case_status] = "Open")
Total Case Value = SUM(Cases[case_value_gbp])
Average Case Value = AVERAGE(Cases[case_value_gbp])

-- Transaction Metrics
Total Revenue = SUMX(FILTER(Transactions, Transactions[transaction_type] = "Invoice"), Transactions[amount_gbp])
Total Expenses = SUMX(FILTER(Transactions, Transactions[transaction_type] = "Expense"), Transactions[amount_gbp])
Total Hours Billed = SUM(Transactions[hours_worked])
Outstanding Invoices = CALCULATE(
    COUNTROWS(Transactions),
    Transactions[transaction_type] = "Invoice",
    Transactions[payment_status] = "Unpaid"
)

-- Solicitor Metrics
Total Solicitors = COUNTROWS(Solicitors)
Average Hourly Rate = AVERAGE(Solicitors[hourly_rate_gbp])
Cases Per Solicitor = DIVIDE([Total Cases], [Total Solicitors], 0)

-- Interaction Metrics
Total Interactions = COUNTROWS(Interactions)
Average Interaction Duration = AVERAGE(Interactions[duration_minutes])
```

#### **Configure Prep for AI** ⭐ **CRITICAL STEP**

1. **Go to Model View** → Select any table
2. Open **Model Settings** (may need to enable in Preview Features)
3. Navigate to **Prep for AI** section

**A. Configure AI Data Schema:**

Select these columns (20 columns total):
- Customers: customer_id, customer_name, customer_type, city, status
- Cases: case_id, case_type, case_value_gbp, case_status, start_date
- Solicitors: solicitor_name, specialization, hourly_rate_gbp
- Transactions: transaction_type, amount_gbp, payment_status
- Interactions: interaction_type, interaction_date

Select these measures (15 measures):
- All measures from _Measures table (Total Customers, Active Customers, Total Cases, etc.)

**B. Create Verified Answers:**

Click **+ New Verified Answer** for each:

1. **How many customers do we have?**
   - Answer: Use measure `[Total Customers]`
   - Description: "Total count of unique customers in the system"

2. **What's the total case value?**
   - Answer: Use measure `[Total Case Value]`
   - Description: "Sum of case_value_gbp for all cases in GBP"

3. **How many open cases?**
   - Answer: Use measure `[Open Cases]`
   - Description: "Count of cases with status='Open'"

4. **What's the total revenue?**
   - Answer: Use measure `[Total Revenue]`
   - Description: "Sum of Invoice transaction amounts in GBP"

5. **Which solicitor has the most cases?**
   - Answer: Use DAX: `TOPN(1, SUMMARIZE(Cases, Cases[solicitor_name], "CaseCount", [Total Cases]), [CaseCount], DESC)`
   - Description: "Solicitor with highest case count"

6. **How many active corporate customers?**
   - Answer: Use DAX: `CALCULATE([Total Customers], Customers[customer_type]="Corporate", Customers[status]="Active")`
   - Description: "Count of customers where type=Corporate and status=Active"

**C. Add AI Instructions:**

```
Business Context:
- This is a UK legal firm specializing in conveyancing, employment law, family law, and commercial law
- Customers can be Individual or Corporate
- Cases are assigned to solicitors with different specializations
- Financial transactions include Invoices, Payments, Timesheets, and Expenses
- Fiscal year runs April-March (UK standard)

Terminology:
- "Revenue" means Invoice transactions only, not Payments
- "Billed hours" means hours_worked from Timesheet transactions
- "Outstanding" means Invoices with payment_status = 'Unpaid'
- "Active" customers have status = 'Active' (not 'Inactive' or 'Suspended')

Calculation Rules:
- Always filter transactions by transaction_type when calculating revenue/expenses
- Case values are in GBP (£)
- Dates use DD/MM/YYYY format (UK standard)
- When calculating "top" or "best", use descending order
- When asked about "this year", use current year only

Thresholds:
- High-value case: > £100,000
- Large customer: > 5 cases
- Senior solicitor: hourly_rate_gbp > £300
```

4. **Save** as `LegalFirmOptimized.pbix`
5. **Publish** to your Fabric workspace

✅ **Checkpoint:** You now have an optimized semantic model with Prep for AI!

---

## 🧬 STEP 5: Create Ontology (Optional - Preview Feature)

**Note:** Fabric IQ Ontology is currently in preview. Check availability in your region.

### **Using Fabric Portal**

1. In your workspace, click **+ New** → **Ontology** (if available)
2. Name it `LegalFirmOntology`

### **Define Entities**

Using the `step5/step5_ontology_definition.json` as reference:

**Entity 1: Client**
- Source: `step2_cleaned_customers` table
- Key: `customer_id`
- Properties: customer_name, customer_type, city, phone, email, status, signup_date

**Entity 2: LegalCase**
- Source: `step2_cleaned_cases` table
- Key: `case_id`
- Properties: case_type, case_value_gbp, case_status, start_date

**Entity 3: Solicitor**
- Source: `step2_cleaned_solicitors` table
- Key: `solicitor_id`
- Properties: solicitor_name, specialization, hire_date, hourly_rate_gbp, office_location

**Entity 4: FinancialTransaction**
- Source: `step2_cleaned_transactions` table
- Key: `transaction_id`
- Properties: transaction_type, transaction_date, amount_gbp, hours_worked, payment_status

**Entity 5: CustomerInteraction**
- Source: `step2_cleaned_interactions` table
- Key: `interaction_id`
- Properties: interaction_type, interaction_date, duration_minutes, notes

### **Define Relationships**

1. **ClientHasCase**: Client → LegalCase (customer_id)
2. **SolicitorAssignedToCase**: Solicitor → LegalCase (solicitor_name)
3. **CaseHasTransaction**: LegalCase → FinancialTransaction (case_id)
4. **ClientHasInteraction**: Client → CustomerInteraction (customer_id)
5. **SolicitorHandlesInteraction**: Solicitor → CustomerInteraction (solicitor_name)

### **Add Contextualizations**

**ClientPortfolioContext:**
- Aggregates: Total cases, total case value, open cases count
- Description: "Client's complete portfolio of legal cases and their values"

**SolicitorWorkloadContext:**
- Aggregates: Cases handled, total hours billed, revenue generated
- Description: "Solicitor's workload and performance metrics"

**CaseFinancialContext:**
- Aggregates: Total invoiced, total paid, outstanding amount
- Description: "Financial summary for a legal case"

---

## 🤖 STEP 6: Configure Data Agent (Multi-Source)

**Note:** Data Agent configuration depends on Fabric's agent builder (preview).

### **Manual Configuration via Fabric Portal**

1. In workspace, click **+ New** → **Data Agent** (if available)
2. Name it `LegalFirmAgent`

### **Configure Data Source 1: ClientCasePortfolio**

- **Type:** Semantic Model
- **Model:** `LegalFirmOptimized`
- **Description:** "Contains customer information, legal cases, solicitors, and customer interactions. Use this for questions about clients, cases, solicitor performance, or customer engagement."
- **Example Queries:**
  - "How many active customers do we have?"
  - "Show me all conveyancing cases"
  - "Which solicitor handles the most cases?"
  - "List all interactions with customer CUST0023"

### **Configure Data Source 2: FinancialTransactions**

- **Type:** Lakehouse Table
- **Table:** `step2_cleaned_transactions`
- **Description:** "Contains financial transaction details including invoices, payments, timesheets, and expenses. Use this for billing, revenue, payment status, and financial analysis questions."
- **Example Queries:**
  - "What's the total revenue in Q1 2023?"
  - "How many unpaid invoices?"
  - "Total hours billed by solicitor Sarah Jones"
  - "Show me all expenses for case CASE0042"

### **Add Routing Rules**

The `step6/step6_data_agent_configuration.json` contains routing logic:

```json
{
  "routing_rules": [
    {
      "keywords": ["customer", "client", "case", "solicitor", "interaction"],
      "target_source": "ClientCasePortfolio"
    },
    {
      "keywords": ["financial", "transaction", "invoice", "payment", "billing", "revenue", "expense"],
      "target_source": "FinancialTransactions"
    }
  ]
}
```

### **Test the Agent**

Try these queries in the Data Agent chat:

1. "How many customers do we have?" → ClientCasePortfolio
2. "What's our total revenue?" → FinancialTransactions
3. "Show me high-value cases over £100k" → ClientCasePortfolio
4. "How many unpaid invoices?" → FinancialTransactions
5. "Which solicitor has the best performance?" → Both sources (JOIN)

---

## ✅ Verification & Testing

### **Test Each Step**

Use queries from `TEST_QUERIES.md`:

```powershell
# Load test queries
$queries = Get-Content TEST_QUERIES.md

# Test each step manually in Fabric
# Step 1: Query raw data (expect ~47% accuracy)
# Step 2: Query cleaned data (expect ~60% accuracy)
# Step 3: Query basic model (expect ~57% accuracy)
# Step 4: Query optimized model (expect ~100% accuracy!)
# Step 5: Query with ontology (expect ~100% accuracy)
# Step 6: Query with agent routing (expect ~93% accuracy)
```

### **Run Automated Evaluation**

Once deployed, update `evaluate_agent.py` with actual IDs:

```powershell
# Update with your actual workspace and agent IDs
python evaluate_agent.py `
    --workspace-id "your-workspace-id" `
    --agent-id "your-agent-id" `
    --dataset evaluation_dataset.json `
    --output production_results.json

# Compare to simulation
Get-Content production_results.json | ConvertFrom-Json | Select-Object -ExpandProperty aggregate_metrics
```

---

## 📊 Post-Deployment Validation

### **1. Data Layer Validation**

```sql
-- Verify all tables exist and have correct row counts
SELECT 
    t.name as TableName,
    SUM(p.rows) as RowCount
FROM sys.tables t
INNER JOIN sys.partitions p ON t.object_id = p.object_id
WHERE p.index_id IN (0,1)
    AND t.name LIKE 'step%'
GROUP BY t.name
ORDER BY t.name;
```

### **2. Semantic Model Validation**

In Power BI Desktop connected to published model:

```dax
// Test measures
EVALUATE ROW(
    "Total Customers", [Total Customers],
    "Total Cases", [Total Cases],
    "Total Revenue", [Total Revenue],
    "Active Customers", [Active Customers]
)
```

Expected results:
- Total Customers: 166
- Total Cases: 500
- Total Revenue: ~£2.5M - £3M
- Active Customers: ~120

### **3. Data Agent Validation**

Test these queries and verify routing:

| Query | Expected Source | Expected Answer |
|-------|----------------|-----------------|
| "How many customers?" | ClientCasePortfolio | 166 |
| "Total revenue?" | FinancialTransactions | £2.8M (approx) |
| "Open cases?" | ClientCasePortfolio | 285 |
| "Unpaid invoices?" | FinancialTransactions | ~45 |

---

## 🎤 Demo Presentation Tips

### **Opening (2 min)**
- "We have 2,500+ records across 5 normalized tables"
- "Real-world UK legal firm scenario with Customer 360"
- "Progressive improvement from 47% to 100% accuracy"

### **Step 1 Demo (3 min)**
- Show raw data with vague columns (`id`, `typ`, `col9`)
- Run query: "How many customers?" → Get wrong answer
- Explain: "Data quality issues compound at scale"

### **Step 2 Demo (2 min)**
- Show cleaned data with descriptive columns
- Run same query → Still not great (~60% accuracy)
- Key message: "Cleaning helps but isn't enough"

### **Step 3 Demo (2 min)**
- Show basic semantic model with duplicate measures
- Run query → Confusion, wrong measure selected
- Key message: "Poor model design hurts AI"

### **Step 4 Demo (5 min)** ⭐ **THE BREAKTHROUGH**
- Show star schema with relationships
- Show Prep for AI configuration (AI Data Schema, Verified Answers)
- Run queries → 100% accuracy!
- Key message: "Best practices deliver perfect results"

### **Step 5 Demo (2 min)**
- Show ontology layer with entities
- Run entity-based query: "Show me clients with high-value cases"
- Key message: "Entity intelligence maintained 100% accuracy"

### **Step 6 Demo (2 min)**
- Run multi-source query: "Compare customer revenue by type"
- Show routing to both sources
- Key message: "93% accuracy with cross-source complexity"

### **Closing (2 min)**
- Show evaluation results chart (47% → 100%)
- "77% improvement at Step 4 proves Prep for AI works"
- "Ready for production at enterprise scale"

---

## 🐛 Troubleshooting

### **Issue: Tables not loading**
- Verify CSV files are in Lakehouse Files section
- Check file paths in notebook (case-sensitive)
- Ensure Lakehouse is attached to notebook

### **Issue: Relationships not creating**
- Verify column data types match (e.g., both STRING)
- Check for NULL values in key columns
- Ensure cardinality is correct (1:many)

### **Issue: Prep for AI not available**
- Update Power BI Desktop to latest version
- Enable "Preview Features" in Options
- Verify workspace has Fabric capacity (not Pro)

### **Issue: Ontology not available**
- Check if preview feature is enabled in your region
- Verify Admin has enabled Fabric IQ features
- May need to request preview access from Microsoft

### **Issue: Data Agent not available**
- Data Agent is in limited preview
- May require signing up for preview program
- Alternative: Use Power BI Q&A or Copilot for similar functionality

---

## 📚 Additional Resources

- **Microsoft Learn:** Search for "Prep for AI Power BI"
- **Fabric Documentation:** https://learn.microsoft.com/fabric/
- **Community:** https://community.fabric.microsoft.com/
- **Support:** Open ticket via Fabric portal

---

## ✅ Deployment Complete!

Once all steps are deployed, you have:

- ✅ 10 tables in Lakehouse (2,515 raw + 2,481 cleaned records)
- ✅ 2 semantic models (basic vs optimized)
- ✅ Prep for AI configured with 6 verified answers
- ✅ Ontology with 5 entities (optional)
- ✅ Data Agent with multi-source routing
- ✅ 30 test queries to demonstrate improvement
- ✅ Evaluation framework showing 47% → 100% accuracy

**Time to impress at the hackathon!** 🚀🏆

---

## 📞 Need Help?

If you encounter issues during deployment:

1. Check `TROUBLESHOOTING.md` (if exists)
2. Review error messages in Fabric portal
3. Verify permissions (Contributor/Admin role required)
4. Check capacity status (not throttled)
5. Review Fabric service health status

**Good luck with your demo!** 🎉
