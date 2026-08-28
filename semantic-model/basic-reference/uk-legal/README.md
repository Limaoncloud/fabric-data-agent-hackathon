# LegalFirmBasic Direct Lake Semantic Model Instructions

## Purpose

Demonstrate poor semantic-model practices and low Q&A / Copilot accuracy, targeting approximately 57% accuracy, using a Direct Lake semantic model over the LegalFirmDemo Lakehouse.

## Fabric Web UI - Direct Lake Semantic Model

1. Open Microsoft Fabric in the browser.
1. Go to the workspace containing the LegalFirmDemo Lakehouse.
1. Open the LegalFirmDemo Lakehouse.
1. Select New semantic model.
1. Choose only the Step 1 cleaned tables to demonstrate baseline behavior before semantic model optimization.
1. Select all 5 Step 1 cleaned tables: step1_cleaned_cases, step1_cleaned_customers, step1_cleaned_transactions, step1_cleaned_solicitors, and step1_cleaned_interactions.
1. Create the semantic model in Direct Lake mode.
1. Name it LegalFirmBasic.
1. Open the semantic model.
1. Create a flat model anti-pattern: do not create relationships between tables, keep all tables independent, and do not define star-schema relationships.
1. Create the duplicate and ambiguous measures listed below.
1. Do not configure Prep data for AI, Q&A synonyms, or descriptions.
1. Save the semantic model.

## Measures to Create

### Duplicate measures

```dax
Total Cases = COUNTROWS(step1_cleaned_cases)
TotalCases = COUNTROWS(step1_cleaned_cases)
total_cases = COUNTROWS(step1_cleaned_cases)
Case Count = COUNTROWS(step1_cleaned_cases)
```

### Ambiguous measures

```dax
Total = SUM(step1_cleaned_cases[case_value_gbp])
Count = COUNTROWS(step1_cleaned_customers)
Value = SUM(step1_cleaned_transactions[amount_gbp])
```

## Result

You now have a deliberately low-quality Direct Lake semantic model over the Lakehouse for Step 3 comparison.