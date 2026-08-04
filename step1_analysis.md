# Step 1: Raw Imperfect Customer Data

## Overview
This dataset represents typical real-world data quality issues found in a UK legal firm's customer database. It contains customer information, case details, and financial data with intentional imperfections to demonstrate data cleaning best practices.

## Data Quality Issues Present

### 1. **Poor Column Naming** ❌
- **Issue**: Vague, non-descriptive column names like `typ`, `col1`, `col2`, `flag`, `date1`, `date2`
- **Impact**: Makes it difficult for the data agent to understand the meaning and context
- **Examples**: 
  - `typ` instead of `customer_type`
  - `col1` instead of `case_type`
  - `col2` instead of `payment_status`
  - `flag` instead of `high_value_flag`

### 2. **Inconsistent Data Formats** ❌
- **Dates**: Multiple formats (YYYY-MM-DD, DD/MM/YYYY)
  - Row 1: `2023-01-15`
  - Row 2: `15/02/2023`
- **Phone Numbers**: Inconsistent formatting
  - `020-7123-4567`
  - `+44 20 7123 4568`
  - `07700900123`
  - `+44-7700-900456`
  - `null`
- **Postcodes**: Inconsistent formatting and missing spaces
  - `SW1A 1AA` (correct)
  - `SW1A1AA` (missing space)
  - `invalid postcode`

### 3. **Inconsistent Capitalization** ❌
- **Customer Types**: `IND`, `ind`, `Individual`, `CORP`, `Corp`, `Company`
- **Status**: `active`, `Active`, `ACTIVE`, `INACTIVE`, `inactive`
- **Payment Status**: `paid`, `Paid`, `pending`, `overdue`
- **Names**: `john smith` vs `ACME Corporation Ltd`

### 4. **Missing Values** ❌
- Row 2: Missing postcode
- Row 5: Phone listed as `null`
- Row 6: Missing `date1`
- Row 9: Missing customer name
- Row 10: Phone is `null`
- Row 11: Missing postcode
- Row 14: Missing address
- Row 18: Missing phone and postcode

### 5. **Duplicate Records** ❌
- **Rows 1, 4, and 19**: Same customer (John Smith) with slight variations
  - Different capitalization
  - Different phone formats
  - Different case types (`convey` vs `property` vs `conveyancing`)

- **Rows 2 and 13**: Same company (ACME Corporation Ltd)
  - Different postcode (typo or moved?)
  - Different case values

### 6. **Data Type Issues** ❌
- Phone numbers stored as text with "null" string instead of actual NULL
- Mixed date formats in same column
- Numeric `flag` column (0/1) without context
- `value` stored as number without currency context (GBP assumed)

### 7. **Inconsistent Terminology** ❌
- Case types use abbreviations without standardization:
  - `convey`, `property`, `conveyancing` (should be standardized)
  - `corp`, `merger` (unclear)
  - `comm_prop`, `property_dev` (inconsistent abbreviation style)
  - `wills`, `probate` (related but different naming)

### 8. **Missing Business Context** ❌
- No clear indication of what `flag` column represents
- `sol` column abbreviated (should be `solicitor_name`)
- No currency symbol for `value`
- Unclear what `date1` and `date2` represent (case open date? billing date?)

### 9. **Invalid/Placeholder Data** ❌
- Row 8: `invalid postcode`
- Row 5: String "null" instead of proper NULL
- Empty strings in various fields

## Dataset Context

### UK Legal Firm Structure
- **Customer Types**:
  - Individual clients (IND, ind, Individual)
  - Corporate clients (CORP, Corp, Company)

- **Case Types**:
  - Conveyancing (property transactions)
  - Litigation
  - Family law (divorce)
  - Corporate law (mergers, franchises)
  - Employment law
  - Wills and probate
  - Personal injury
  - Immigration
  - Intellectual property

- **Solicitors**:
  - Sarah Jones
  - Robert Smith
  - Michael Brown

- **Financial Values**:
  - Range from £3,500 to £250,000
  - Represents estimated case value or total billing

## Impact on Data Agent
Without cleaning and proper configuration, a data agent would struggle with:
1. Understanding what each column represents
2. Joining or aggregating data correctly
3. Interpreting customer types and case types
4. Handling date calculations
5. Identifying unique customers (duplicates)
6. Providing accurate answers to natural language questions

## Next Steps
In Step 2, we will apply Microsoft Learn best practices to clean this data and make it AI-ready.
