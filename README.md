# Fabric Data Agent Demo - UK Legal Firm Customer 360

This demo demonstrates Fabric Data Agent capabilities for a UK legal firm's customer 360 scenario with financial data.

## Demo Structure

### Step 1: Raw Imperfect Customer Data
- Contains data quality issues typical of real-world datasets
- Includes inconsistent naming, missing values, duplicate records

### Step 2: Data Cleaning with Best Practices
- Applies Microsoft Learn best practices for data agent configuration
- Demonstrates data transformation and cleaning

### Step 3: Initial Semantic Model (Non-Optimized)
- Creates a basic semantic model without following best practices
- Shows common pitfalls and issues

### Step 4: Optimized Semantic Model
- Applies semantic model best practices for AI
- Configures Prep for AI features
- Shows improvements in query accuracy

### Step 5: Ontology Integration
- Adds ontology layer for enhanced semantic understanding
- Demonstrates entity relationships and contextual queries

### Step 6: Multi-Source Routing
- Adds second data source (financial transactions)
- Demonstrates routing between data sources

## Files

- `step1_raw_customer_data.csv` - Raw imperfect customer data
- `step2_cleaned_customer_data.csv` - Cleaned data following best practices
- `step3_basic_semantic_model.json` - Initial semantic model configuration
- `step4_optimized_semantic_model.json` - Optimized semantic model with AI best practices
- `step5_ontology_definition.json` - Ontology layer definition
- `step6_financial_transactions.csv` - Second data source for routing demo
- `data_agent_configuration.json` - Complete data agent configuration
- `demo_queries.md` - Sample queries to test each step
