# Step 5: Adding Ontology Layer

## Overview
An ontology layer provides a semantic abstraction over your data sources, defining business entities, their properties, and relationships in a way that's natural for users to query. It enhances the Fabric Data Agent's ability to understand entity-based questions and traverse complex relationships.

## What is an Ontology?

An ontology in Fabric defines:
1. **Entity Types** - Business objects (Client, Case, Solicitor)
2. **Properties** - Attributes of entities with synonyms
3. **Relationships** - How entities connect to each other
4. **Contextualizations** - Pre-computed aggregations and joined views
5. **Bindings** - Mappings to underlying data sources (Lakehouse, Eventhouse)

## Entities Defined in This Ontology

### 1. **Client Entity** 🧑‍💼

**Purpose:** Represents a customer of the law firm

**Properties:**
- `ClientID` (Key) - Unique identifier
- `ClientName` - Full name
- `ClientType` - Individual or Corporate
- `ClientStatus` - Active, Inactive, Closed
- `Address`, `Postcode`, `Phone`, `Email` - Contact information

**Synonyms:** Customer, Client, Customer Entity, Legal Client

**Binding:** Mapped to `Customers` table in Lakehouse

**Use Cases:**
- "Show me all active clients"
- "What clients are located in London?" (using postcode)
- "List corporate clients"

---

### 2. **LegalCase Entity** ⚖️

**Purpose:** Represents a legal matter or case

**Properties:**
- `CaseID` (Key) - Unique identifier
- `CaseType` - Type of legal work
- `CaseValue` - Financial value in GBP
- `CaseStartDate` (Timeseries) - When case opened
- `CaseCompletionDate` - When case closed
- `PaymentStatus` - Paid, Pending, Overdue, Closed
- `HighValueFlag` - Boolean for cases >= £50k

**Synonyms:** Case, Matter, Legal Matter, File, Case File

**Binding:** Mapped to `Cases` table in Lakehouse

**Timeseries Support:** `CaseStartDate` enables time-based analysis
- "How many cases opened each month?"
- "Show me case trends over time"

**Use Cases:**
- "Show me all conveyancing cases"
- "What cases are overdue on payment?"
- "List high-value cases"

---

### 3. **Solicitor Entity** 👨‍⚖️

**Purpose:** Represents a legal professional at the firm

**Properties:**
- `SolicitorName` (Key) - Solicitor's name

**Synonyms:** Lawyer, Attorney, Legal Professional

**Binding:** Derived distinctly from `Cases` table's `assigned_solicitor_name`

**Use Cases:**
- "Who are our solicitors?"
- "Show me Sarah Jones' workload"

---

## Relationships Defined

### 1. **ClientHasCase** (One-to-Many)

**From:** Client → **To:** LegalCase

**Description:** Links clients to their legal cases

**Cardinality:** One client can have many cases

**Query Examples:**
- "Show me all cases for client ACME Corporation"
- "What matters does John Smith have?"
- "List cases for corporate clients"

**Traversal:** `Client.ClientID` → `LegalCase.ClientID`

---

### 2. **SolicitorAssignedToCase** (One-to-Many)

**From:** Solicitor → **To:** LegalCase

**Description:** Links solicitors to cases they handle

**Cardinality:** One solicitor can handle many cases

**Query Examples:**
- "Show me all cases assigned to Sarah Jones"
- "What's Robert Smith's caseload?"
- "Which solicitor handles the most cases?"

**Traversal:** `Solicitor.SolicitorName` → `LegalCase.SolicitorName`

---

### 3. **SolicitorServesClient** (Many-to-Many) *Derived*

**From:** Solicitor ↔ **To:** Client

**Description:** Shows which solicitors work with which clients (via cases)

**Type:** Derived relationship (computed through cases)

**Derivation Path:** 
```
Solicitor → SolicitorAssignedToCase → LegalCase → ClientHasCase → Client
```

**Query Examples:**
- "What clients does Sarah Jones work with?"
- "Show me which solicitors work with corporate clients"
- "Who are ACME Corporation's solicitors?"

**Benefits:** 
- ✅ Automatically computed
- ✅ No need to maintain separate relationship table
- ✅ Always up-to-date

---

## Contextualizations (Aggregated Views)

Contextualizations provide pre-defined aggregations and joined views for common analysis patterns.

### 1. **ClientPortfolioContext** 📊

**Entity:** Client

**Purpose:** Holistic view of client relationship

**Aggregations:**
- `TotalCaseValue` - Sum of all case values for this client
- `NumberOfCases` - Total count of cases
- `AverageCaseValue` - Average case value
- `ActiveCasesCount` - Count of non-closed cases

**Query Examples:**
- "Show me the portfolio summary for ACME Corporation"
- "What's the total value of all John Smith's cases?"
- "Which client has the most active cases?"

**Benefits:**
- ✅ Pre-computed metrics for performance
- ✅ Consistent calculation logic
- ✅ Natural language friendly

---

### 2. **SolicitorWorkloadContext** 📈

**Entity:** Solicitor

**Purpose:** Solicitor performance and workload metrics

**Aggregations:**
- `TotalCaseload` - Total number of cases
- `TotalCaseValue` - Sum of all case values
- `AverageCaseValue` - Average case value
- `NumberOfClients` - Distinct client count
- `HighValueCasesCount` - Count of high-value cases

**Query Examples:**
- "Show me solicitor workload comparison"
- "Who's our top-performing solicitor by revenue?"
- "How many clients does each solicitor serve?"

**Benefits:**
- ✅ Performance metrics readily available
- ✅ Enables solicitor comparison queries
- ✅ Workload balancing insights

---

### 3. **CaseDetailsContext** 🔍

**Entity:** LegalCase

**Purpose:** Complete case view with related entities

**Includes:**
- Case properties
- Client name and type
- Assigned solicitor name

**Query Examples:**
- "Show me complete details for case CASE001"
- "List all conveyancing cases with client and solicitor info"

**Benefits:**
- ✅ Avoids manual joins
- ✅ Consistent data shape
- ✅ Simplified queries

---

## Ontology vs. Semantic Model vs. Raw Tables

| Aspect | Raw Tables | Semantic Model (Step 4) | Ontology (Step 5) |
|--------|-----------|------------------------|-------------------|
| **Data Structure** | Relational tables | Star schema with measures | Entity-relationship model |
| **Query Language** | SQL | DAX | Natural language entities |
| **Relationships** | Foreign keys | Model relationships | Semantic relationships with synonyms |
| **Aggregations** | Manual GROUP BY | DAX measures | Contextualizations |
| **Synonyms** | None | Descriptions | Built-in property synonyms |
| **Derived Relationships** | Manual joins | Relationship paths | Auto-computed (e.g., SolicitorServesClient) |
| **Timeseries** | Date columns | Time intelligence | Timeseries properties with granularity |
| **Business Context** | None | AI Instructions | Entity descriptions + contextualizations |

---

## Query Examples: Impact of Ontology

### Query 1: "Show me all cases for ACME Corporation"

**Without Ontology (Semantic Model):**
```dax
Cases WHERE Related(Customers[customer_name]) = "ACME Corporation Ltd"
```
- Requires knowing table structure
- Must understand relationship
- Exact name matching required

**With Ontology:**
```
Query: "Show me all cases for ACME Corporation"
→ Entity: Client (name contains "ACME")
→ Relationship: ClientHasCase
→ Return: All related LegalCase entities
```
- Natural entity-based query
- Handles name variations via synonyms
- Automatic relationship traversal

---

### Query 2: "Which solicitors work with corporate clients?"

**Without Ontology:**
```dax
CALCULATE(
    VALUES(Cases[assigned_solicitor_name]),
    FILTER(
        Cases,
        RELATED(Customers[customer_type]) = "Corporate"
    )
)
```
- Complex DAX required
- Must know relationship structure
- Multiple table joins

**With Ontology:**
```
Query: "Which solicitors work with corporate clients?"
→ Entity: Client (where ClientType = "Corporate")
→ Relationship: SolicitorServesClient (derived)
→ Return: Related Solicitor entities
```
- Single natural language query
- Derived relationship handles complexity
- Semantic understanding of "corporate"

---

### Query 3: "What's the total value of Sarah Jones' cases?"

**Without Ontology:**
```dax
Total Case Value for Cases[assigned_solicitor_name] = "Sarah Jones"
```
- Requires knowing measure name
- Must filter correctly
- Single-purpose calculation

**With Ontology:**
```
Query: "What's the total value of Sarah Jones' cases?"
→ Entity: Solicitor (SolicitorName = "Sarah Jones")
→ Contextualization: SolicitorWorkloadContext.TotalCaseValue
→ Return: Aggregated value
```
- Uses pre-computed contextualization
- Consistent calculation logic
- Faster performance

---

### Query 4: "Show me case trends over time"

**Without Ontology:**
```dax
Cases grouped by MONTH(case_start_date), COUNT(case_id)
```
- Manual time grouping
- Need to specify granularity
- Basic date handling

**With Ontology:**
```
Query: "Show me case trends over time"
→ Entity: LegalCase
→ Timeseries Property: CaseStartDate (granularity: day)
→ Aggregation: COUNT by month
→ Return: Timeseries data
```
- Built-in timeseries support
- Automatic granularity handling
- Optimized for time-based queries

---

## Benefits of Ontology Layer

### 1. **Natural Entity-Based Queries** 🗣️
- Users think in terms of business entities (clients, cases, solicitors)
- No need to understand underlying table structure
- Synonyms allow flexible query phrasing

### 2. **Semantic Relationships** 🔗
- Relationships have business meaning (ClientHasCase, SolicitorServesClient)
- Automatic traversal of complex relationships
- Derived relationships compute automatically

### 3. **Contextualized Analysis** 📊
- Pre-defined aggregations (ClientPortfolio, SolicitorWorkload)
- Consistent calculation logic
- Performance optimized

### 4. **Timeseries Support** 📅
- Built-in time-based analysis
- Granularity specification (day, month, quarter)
- Trend and pattern queries

### 5. **Data Source Abstraction** 🗂️
- Ontology binds to underlying sources (Lakehouse, Eventhouse)
- Users don't need to know where data lives
- Can combine data from multiple sources

### 6. **Synonym Support** 🔤
- Multiple ways to refer to same concept
- "Client" = "Customer" = "Legal Client"
- "Case" = "Matter" = "File"
- Improves query matching

---

## Data Agent Configuration with Ontology

When the ontology is added to a data agent, it provides:

### Agent Instructions Enhancement:
```
## Ontology-Based Query Guidance

**Entity-Based Queries:**
- "Show me all cases for client ACME" → Query Client entity, traverse ClientHasCase
- "What solicitors work with corporate clients?" → Use SolicitorServesClient relationship

**Contextualized Queries:**
- "Client portfolio summary" → Use ClientPortfolioContext
- "Solicitor performance" → Use SolicitorWorkloadContext

**Timeseries Queries:**
- "Case opening trends" → Use CaseStartDate timeseries property
```

---

## Query Accuracy Improvement (Estimated)

⚠️ **Note:** Projected improvement based on ontology capabilities. Measure actual results using evaluation framework.

| Query Type | Without Ontology (Est.) | With Ontology (Est.) | Improvement (Est.) |
|-----------|------------------|---------------|-------------|
| **Entity-based** | ~70% | ~95% | +36% |
| **Relationship traversal** | ~60% | ~90% | +50% |
| **Contextualized aggregations** | ~75% | ~98% | +31% |
| **Synonym handling** | ~65% | ~95% | +46% |
| **Timeseries analysis** | ~70% | ~95% | +36% |
| **Overall** | ~68% | ~95% | +40% |

---

## Implementation Checklist ✅

- [x] **Define Entity Types** - Client, LegalCase, Solicitor
- [x] **Add Properties** - All key attributes with descriptions
- [x] **Include Synonyms** - Multiple ways to reference entities and properties
- [x] **Define Relationships** - ClientHasCase, SolicitorAssignedToCase, SolicitorServesClient
- [x] **Create Contextualizations** - ClientPortfolio, SolicitorWorkload, CaseDetails
- [x] **Configure Timeseries** - CaseStartDate with aggregations
- [x] **Bind to Data Sources** - Map to Lakehouse tables
- [x] **Add Agent Instructions** - Guidance for ontology-based queries

---

## Example Queries to Test

Test these queries against the ontology to see its power:

1. ✅ "Show me all cases for ACME Corporation"
2. ✅ "What clients does Sarah Jones work with?"
3. ✅ "List all high-value cases for corporate clients"
4. ✅ "Show me solicitor performance comparison"
5. ✅ "What's the client portfolio summary for each client?"
6. ✅ "Which solicitors work with individual clients?"
7. ✅ "Show me case opening trends by month"
8. ✅ "What's the total value of all conveyancing matters?"
9. ✅ "How many active cases does each solicitor have?"
10. ✅ "Show me complete details for high-value cases"

---

## Next Steps

In **Step 6**, we'll add a **second data source** (Financial Transactions) to demonstrate **data source routing** capabilities. The data agent will learn to:
- Route case-related questions to the Case/Customer ontology
- Route financial transaction questions to the new data source
- Combine data from both sources when needed

This will showcase how the agent intelligently selects the right data source for each query.
