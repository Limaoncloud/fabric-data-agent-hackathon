# Fabric Data Agent Demo - Complete Deployment Guide

## Overview

This guide walks you through deploying all 6 steps of the UK Legal Firm Customer 360 demo to Microsoft Fabric.

**Time Required:** ~2-3 hours for complete deployment  
**Prerequisites:** Fabric workspace with Contributor/Admin access, Power BI Premium/Fabric capacity

---

## 📋 Pre-Deployment Checklist

Before you begin, ensure you have:

- ✅ **Fabric Workspace** with adequate capacity (F2 or higher recommended)
- ✅ **Contributor or Admin access** to create Fabric items
- ✅ **Data files generated** (run `python step1/generate_step1_data.py`)

## Recommended: Deploy from the Fabric Notebook

Use `NB_Deploy_Data_Agent_Hackathon.ipynb` for the reproducible deployment path:

1. Import the notebook into the target capacity-backed workspace.
2. Leave `WORKSPACE_ID=""` to deploy to the notebook's current workspace.
3. Leave `DOMAIN_PROFILE="uk-legal"` for the legal scenario.
4. Keep `ENABLE_PREP_FOR_AI=False`, `ENABLE_DATA_AGENT=False`, and the preview stages disabled for a participant-ready deployment.
5. Run all cells to create the Lakehouse, managed Delta tables, Basic model, and Optimized model.

The notebook generates semantic models as TMDL through Fabric APIs. It does not require Power BI Desktop, PBIP, PBIX, BIM, or template files. See [deployment/README.md](deployment/README.md) for custom-domain deployment.

The remaining sections document the equivalent manual workflow and troubleshooting details.

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
│  │  │  ├─ step1_cleaned_customers (171)       │             │
│  │  │  ├─ step1_cleaned_cases (500)           │             │
│  │  │  ├─ step1_cleaned_solicitors (15)       │             │
│  │  │  ├─ step1_cleaned_transactions (1000)   │             │
│  │  │  └─ step1_cleaned_interactions (800)    │             │
│  │  └─ 3 Step 6 routing marts                 │             │
│  └────────────────────────────────────────────┘             │
│                                                              │
│  STEP 3 & 4: SEMANTIC MODEL LAYER                           │
│  ┌────────────────────────────────────────────┐             │
│  │  Semantic Model: LegalFirmBasic (Step 3)   │             │
│  │  └─ 5 disconnected tables, anti-patterns   │             │
│  │                                             │             │
│  │  Semantic Model: LegalFirmOptimized (Step 4)│            │
│  │  ├─ Star schema (5 tables)                 │             │
│  │  ├─ Explicit measures and descriptions     │             │
│  │  ├─ Relationships configured               │             │
│  │  └─ AI configuration left to participants  │             │
│  └────────────────────────────────────────────┘             │
│                                                              │
│  STEP 5: ONTOLOGY LAYER (Optional - Preview)               │
│  ┌────────────────────────────────────────────┐             │
│  │  Ontology: LegalFirmOntology               │             │
│  │  ├─ Entities: Customer, LegalCase, Solicitor│            │
│  │  └─ 2 core relationships                  │             │
│  └────────────────────────────────────────────┘             │
│                                                              │
│  STEP 6: DATA AGENT                                         │
│  ┌────────────────────────────────────────────┐             │
│  │  Data Agent: LegalFirmCustomer360Agent     │             │
│  │  ├─ Source 1: LegalFirmOptimized           │             │
│  │  ├─ Source 2: LegalFirmDemo marts          │             │
│  │  └─ Source instructions & examples         │             │
│  └────────────────────────────────────────────┘             │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 🚀 Step-by-Step Deployment

### **Step 0: Setup Environment Variables**

Skip this section when running the Fabric notebook with `WORKSPACE_ID=""`; the notebook resolves its current workspace automatically. Use the following only for manual REST or CLI work.

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

### **Option A: Via Fabric Portal (Manual)**

#### 1. Create Lakehouse
1. Open your Fabric workspace: https://app.fabric.microsoft.com/
2. Click **+ New** → **Lakehouse** → Name it `LegalFirmDemo`
3. Click **Create**

#### 2. Upload Baseline Data (Step 1)
1. In the Lakehouse, go to **Tables**
2. Click **Get data** → **Upload files**
3. Upload all 5 Step 1 CSV files:
   - `step1/step1_cleaned_customers.csv`
   - `step1/step1_cleaned_cases.csv`
   - `step1/step1_cleaned_solicitors.csv`
   - `step1/step1_cleaned_transactions.csv`
   - `step1/step1_cleaned_interactions.csv`
4. For each file:
   - Click **Load to new table**
   - Keep suggested table name (e.g., `step1_cleaned_customers`)
   - Click **Load**

#### 3. Apply Data Agent Best Practices (Step 2)
1. Keep the same Step 1 tables (no additional file uploads).
2. Configure tighter schema scope and source descriptions in the Data Agent.
3. Add representative example queries and concise routing guidance.

**Result:** Step 2 is configuration-only and uses the same 5 Step 1 tables.

### **Option B: Via Notebook (Recommended)**

Import and run `NB_Deploy_Data_Agent_Hackathon.ipynb`. It reads all tables declared in `config/domains/uk-legal.json` and writes them as managed Delta tables. The current profile loads the five Step 1 tables plus three Step 6 routing marts.

### **Verify Data Load**

```sql
-- Run in Lakehouse SQL Endpoint
SELECT 'step1_cleaned_customers' as table_name, COUNT(*) as row_count FROM step1_cleaned_customers
UNION ALL
SELECT 'step1_cleaned_cases', COUNT(*) FROM step1_cleaned_cases
UNION ALL
SELECT 'step1_cleaned_solicitors', COUNT(*) FROM step1_cleaned_solicitors
UNION ALL
SELECT 'step1_cleaned_transactions', COUNT(*) FROM step1_cleaned_transactions
UNION ALL
SELECT 'step1_cleaned_interactions', COUNT(*) FROM step1_cleaned_interactions
;
```

**Expected Output:**
```
table_name                      row_count
step1_cleaned_customers         171
step1_cleaned_cases             500
step1_cleaned_solicitors        15
step1_cleaned_transactions      1000
step1_cleaned_interactions      800
```

The three Step 6 marts contain 171 engagement rows, 500 case-finance rows, and 15 solicitor-performance rows, for 3,172 rows across all eight profile-managed tables.

✅ **Checkpoint:** You now have all profile-managed data in the Fabric Lakehouse.

---

## 🎨 STEP 3: Create Basic Semantic Model (Anti-Patterns)

### **Purpose:** Demonstrate poor practices and lower answer quality

#### **Recommended: Deploy from the Notebook**

Run the semantic-model section of `NB_Deploy_Data_Agent_Hackathon.ipynb`, or run the full notebook from the beginning. It generates the `LegalFirmBasic` Direct Lake model as TMDL from `config/domains/uk-legal.json` and deploys it directly through the Fabric API.

No Power BI Desktop or PBIX file is required. The generated Basic model deliberately contains five disconnected Step 1 tables, duplicate measures, ambiguous measures, and no Prep for AI configuration.

#### **Optional: Create Manually in Fabric**

To demonstrate the build manually, create a new Direct Lake semantic model from the `LegalFirmDemo` Lakehouse in the Fabric web UI, select the five Step 1 cleaned tables, and follow [step3/README.md](step3/README.md) for the anti-pattern measures and configuration.

**Result:** A deliberately low-quality semantic model for the Step 3 comparison.

---

## 🌟 STEP 4: Create Optimized Semantic Model

### **Purpose:** Provide a technically sound model for participant-led AI tuning

#### **Recommended: Deploy from the Notebook**

Run `NB_Deploy_Data_Agent_Hackathon.ipynb` with `ENABLE_PREP_FOR_AI=False`. The notebook generates `LegalFirmOptimized` as TMDL and deploys it through the Fabric API with:

- Five business-named Direct Lake tables.
- Four one-direction relationships from the domain profile.
- Eighteen explicit business measures.
- Business-friendly names and descriptions.

The participant-ready model intentionally has no synonyms, AI Data Schema selection, AI instructions, Verified Answers, or Data Agent. No Power BI Desktop or PBIX file is required for deployment.

#### **Participant Challenge: Improve Agent Understanding**

Participants create a Data Agent using the Basic or Optimized model, run baseline questions, diagnose incorrect or inconsistent behavior, and decide which durable control to improve:

- Semantic-model synonyms in Prep for AI (not Lakehouse table synonyms).
- AI Data Schema scope.
- AI instructions and example prompts.
- Data Agent source descriptions and instructions.
- Verified Answers based on saved report visuals.

Provide one worked example, then use questions and diagnostic hints without mapping each question to an exact fix. Participants should retest after every change and record what improved or did not improve.

#### **Optional Organizer Automation**

Set `ENABLE_PREP_FOR_AI=True` only when an organizer needs a completed demonstration environment. This optional path attempts to deploy AI instructions, example prompts, and AI schema metadata. Verified Answers remain manual because Fabric requires saved report visuals.

✅ **Checkpoint:** Participants receive an optimized, described model whose AI-specific configuration is intentionally incomplete.

---

## 🧬 STEP 5: Create Ontology (Optional - Preview Feature)

**Note:** Fabric IQ Ontology is currently in preview. Check availability in your region.

The notebook deploys Ontology only when both `ENABLE_ONTOLOGY=True` and `CONFIRM_PREVIEW_DEPLOYMENTS=True`. Review the proposal printed by the notebook before confirming deployment.

The current domain profile creates these entities:

| Entity | Source table | Key |
| --- | --- | --- |
| Customer | `step1_cleaned_customers` | `customer_id` |
| LegalCase | `step1_cleaned_cases` | `case_id` |
| Solicitor | `step1_cleaned_solicitors` | `solicitor_name` |

It creates two relationships: `CustomerHasCase` and `SolicitorHandlesCase`.

`config/domains/uk-legal.json` is the deployment source of truth. `step5/step5_ontology_definition.json` is a legacy design reference and does not match the current profile schema closely enough to deploy unchanged.

---

## 🤖 STEP 6: Configure Data Agent (Multi-Source)

**Note:** Data Agent deployment uses a preview SDK and is disabled by default. Set `ENABLE_DATA_AGENT=True` after reviewing the staged source configuration. Set `PUBLISH_DATA_AGENT=True` only when you are ready to publish.

The notebook creates or updates `LegalFirmCustomer360Agent` with two Fabric item sources:

| Source | Objects | Use for |
| --- | --- | --- |
| `LegalFirmOptimized` semantic model | Customers, Cases, Solicitors, Transactions, Interactions | Model measures and general customer, case, solicitor, transaction, and interaction questions |
| `LegalFirmDemo` Lakehouse | `step6_client_engagement_summary`, `step6_case_finance_insights`, `step6_solicitor_performance_mart` | Engagement segments, combined case-finance outcomes, and solicitor performance |

The source instructions and examples come from `config/domains/uk-legal.json`. `step6/step6_data_agent_configuration.json` is a more detailed legacy design reference; it is not the configuration consumed by the notebook.

### **Test the Agent**

Try these queries in the Data Agent chat:

1. "How many active customers do we have?" → `LegalFirmOptimized`
2. "What is our total revenue?" → `LegalFirmOptimized`
3. "Which customers are in the low engagement segment?" → `LegalFirmDemo`
4. "Which high-value open cases have outstanding balances?" → `LegalFirmDemo`
5. "Which solicitors are in the top performance tier?" → `LegalFirmDemo`

---

## ✅ Verification & Testing

### **Test Each Step**

Use queries from `evaluation/TEST_QUERIES.md`:

```powershell
# Load test queries
$queries = Get-Content evaluation/TEST_QUERIES.md

# Test each step manually in Fabric
# Step 1-2: Validate data preparation and source descriptions
# Step 3: Establish the Basic model baseline
# Step 4: Tune the Optimized model with participant-authored Prep for AI
# Step 5: Evaluate entity traversal when Ontology is enabled
# Step 6: Evaluate source selection when Data Agent is enabled
```

Accuracy percentages in the evaluation documents are demo benchmarks, not deployment guarantees. Re-run the evaluation against your deployed artifacts and tenant features.

### **Run Automated Evaluation**

Once deployed, update `evaluation/evaluate_agent.py` with actual IDs:

```powershell
# Update with your actual workspace and agent IDs
python evaluation/evaluate_agent.py `
    --workspace-id "your-workspace-id" `
    --agent-id "your-agent-id" `
    --dataset evaluation/evaluation_dataset.json `
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

Run a DAX query against the published `LegalFirmOptimized` model using the Fabric or Power BI semantic-model query experience:

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
- Total Customers: 171
- Total Cases: 500
- Total Revenue: £5,420,217
- Active Customers: 101

### **3. Data Agent Validation**

Test these queries and verify routing:

| Query | Expected Source | Expected Answer |
|-------|----------------|-----------------|
| "How many customers?" | LegalFirmOptimized | 171 |
| "Total revenue?" | LegalFirmOptimized | £5,420,217 |
| "Open cases?" | LegalFirmOptimized | 180 |
| "Unpaid invoices?" | LegalFirmOptimized | 54 |

---

## 🎤 Demo Presentation Tips

### **Opening (2 min)**
- "We have 3,172 rows across 8 managed Delta tables"
- "Real-world UK legal firm scenario with Customer 360"
- "We compare a deliberately weak model with an optimized, AI-ready model"

### **Step 1 Demo (3 min)**
- Show raw data with vague columns (`id`, `typ`, `col9`)
- Run query: "How many customers?" → Get wrong answer
- Explain: "Data quality issues compound at scale"

### **Step 2 Demo (2 min)**
- Show cleaned data with descriptive columns
- Explain how source descriptions and scope improve interpretation
- Key message: "Cleaning helps but isn't enough"

### **Step 3 Demo (2 min)**
- Show basic semantic model with duplicate measures
- Run query → Confusion, wrong measure selected
- Key message: "Poor model design hurts AI"

### **Step 4 Demo (5 min)** ⭐ **THE BREAKTHROUGH**
- Show star schema with relationships
- Show the Optimized model before AI-specific tuning
- Let participants add selected Prep for AI controls and rerun the evaluated query set
- Key message: "Explicit relationships, measures, and AI metadata improve reliability"

### **Step 5 Demo (2 min)**
- Show ontology layer with entities
- Run entity-based query: "Show me clients with high-value cases"
- Key message: "Entity relationships support traversal-style questions"

### **Step 6 Demo (2 min)**
- Run multi-source query: "Compare customer revenue by type"
- Show routing to both sources
- Key message: "Source instructions make multi-source routing testable"

### **Closing (2 min)**
- Show results from the current evaluation run
- Compare measured Basic and Optimized model outcomes
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
- Confirm Prep for AI is available for the semantic model in the Fabric service
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

- ✅ 8 managed Delta tables with 3,172 current rows
- ✅ 2 semantic models (basic vs optimized)
- ✅ Optimized model with relationships, measures, and descriptions
- ✅ Synonyms, Prep for AI, Verified Answers, and agent instructions left as participant exercises
- ✅ Ontology with 3 entities and 2 relationships (optional)
- ✅ Data Agent with semantic-model and Lakehouse sources (optional)
- ✅ 30 test queries to demonstrate improvement
- ✅ Evaluation framework for measuring model quality and routing

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





