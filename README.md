# RetailPulse Analytics

## End-to-End Retail Business Intelligence & Analytics System

RetailPulse is a **45-day Data Analytics internship case study** designed to demonstrate the complete journey from transaction data to validated business recommendations using **Excel, SQL, Python and Power BI-style reporting**.

> **Academic integrity note:** the analytical dataset is synthetic and reproducible. It is not presented as confidential WSA or client data.

## Business problem

A retail management team receives transaction-level data but needs a concise way to answer:

- How much revenue and profit are being generated?
- Which regions and categories drive performance?
- Which customer segments have stronger basket economics?
- How do discounts affect profitability?
- Which products deserve attention?
- What operational impact comes from returns and cancellations?

## 45-day project architecture

```text
Business Requirements
        ↓
Synthetic / Source-like Transaction Data
        ↓
Excel-style Profiling + Python Data Cleaning
        ↓
Validated Analytical Dataset
        ↓
SQL Data Model + Business Queries
        ↓
Python EDA + RFM Segmentation
        ↓
Power BI Model / Dashboard Specification
        ↓
Interactive Executive Dashboard
        ↓
Validation + Insights + Recommendations
```

## What is actually demonstrated

| Internship skill | Project evidence |
|---|---|
| Data collection & cleaning | Source-like transaction data, quality issues, validation rules, cleaned dataset |
| Excel | Profiling, cleaning logic and KPI preparation workflow |
| SQL | Fact/dimension design, KPI, regional, category, segment and discount queries |
| Python | Reproducible cleaning, financial recalculation, EDA-ready aggregates and RFM |
| Power BI / Tableau | Executive dashboard layout, KPI definitions, filters and visual-selection rationale |
| Insight generation | Category, regional, customer and profitability recommendations |
| SDLC | Requirements → design → implementation → testing → deployment → maintenance |

## Dataset

The reference case-study structure uses a transaction-level retail dataset with **Order ID, Order Date, Region, Customer Segment, Category, Product, Quantity, Unit Price, Discount, Sales, Cost, Profit and Order Status**. The generator additionally carries city, state, channel and payment method to support richer analysis.

The generator intentionally includes a small number of controlled data-quality issues so the cleaning stage is demonstrable rather than cosmetic. The cleaned pipeline recalculates sales/profit and treats **Completed** orders as realized sales while retaining Returned and Cancelled records for operational analysis.

## Repository structure

```text
RetailPulse-Analytics/
├── data/
│   ├── raw/
│   └── processed/
├── excel/
├── notebooks/
├── python/
│   ├── generate_retail_data.py
│   ├── prepare_data.py
│   ├── customer_rfm.py
│   └── run_analysis.py
├── sql/
│   ├── schema.sql
│   └── analytics_queries.sql
├── powerbi/
├── dashboards/
├── docs/
├── reports/
├── screenshots/
├── app.py
├── requirements.txt
└── README.md
```

## Key analytical layers

### 1. Data quality
- Missing-value detection and repair
- Duplicate order detection
- Date and numeric validation
- Discount and quantity range checks
- Recalculation of Sales and Profit
- Before/after quality reporting

### 2. SQL analytics
- Executive KPIs
- Monthly performance
- Regional scorecard
- Category profitability
- Customer-segment economics
- Discount bands
- Product ranking
- Order-status analysis

### 3. Python analytics
- Reproducible transformations
- Descriptive EDA
- Revenue/profit trend analysis
- Category and regional diagnostics
- RFM customer segmentation
- Independent KPI validation

### 4. Dashboard
The live application is designed as a management-facing interface rather than a collection of decorative charts. It includes filters for **region, category, customer segment and channel**, plus:

- Executive KPI strip
- Monthly revenue and profit trend
- Category contribution
- Regional scorecard
- Channel contribution
- Customer-segment performance
- Product ranking
- Discount-vs-margin diagnostic
- Category margin matrix
- Order-status operations view
- Auto-generated management recommendations

## Running locally

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
# source .venv/bin/activate

pip install -r requirements.txt
python -m python.prepare_data
python -m python.customer_rfm
python app.py
```

Then open the local Flask address shown in the terminal.

## Validation philosophy

The project follows the report methodology: calculations are validated before publication, completed orders are used for realized-sales KPIs, and regional/category/segment totals should reconcile to the overall total. This keeps the dashboard analytically defensible rather than merely visually polished.

## Academic alignment

The project is structured around the internship competencies and report framework: company/internship context, literature-supported methodology, requirements, data preparation, SQL analysis, EDA, dashboard design, validation, professional learning, conclusion and future scope.

## Author

**Soniya Rajpurohit**  
B.Tech Practical Training / Data Analytics Internship Project
