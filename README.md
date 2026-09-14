# RetailPulse Analytics

## End-to-End Retail Business Intelligence & Analytics System

RetailPulse transforms retail transaction data into decision-ready business insights using **Python, SQL, Excel and Power BI**.

> **Academic / portfolio note:** the project uses synthetic retail data designed for reproducible analytics. It does not represent confidential data from WSA or any real client.

### Business questions

- How is revenue and profit trending over time?
- Which products and categories drive revenue?
- Which regions and channels perform best?
- Which customers contribute the most value?
- Where do discounts reduce profitability?
- What sales trend can management expect next?

## Analytics workflow

```text
Synthetic / Raw Data
        |
        v
Excel + Python Data Quality Checks
        |
        v
Cleaned Analytical Dataset
        |
        +------------------+
        |                  |
        v                  v
      SQL             Python EDA
        |                  |
        +--------+---------+
                 |
                 v
          Power BI Model
                 |
                 v
     Executive Decision Dashboard
                 |
                 v
     Insights + Recommendations
```

## Planned deliverables

| Area | Deliverable |
|---|---|
| Data | Reproducible synthetic retail dataset generator |
| Excel | Cleaning workbook and KPI preparation |
| Python | Cleaning, EDA, customer segmentation and forecasting |
| SQL | Schema, loading scripts and analytical queries |
| Power BI | Executive, Sales, Customer and Profitability pages |
| Documentation | Data dictionary, methodology, architecture and testing |
| Academic report | Evidence for the B.Tech practical training seminar report |

## Repository structure

```text
RetailPulse-Analytics/
├── data/
│   ├── raw/
│   └── processed/
├── excel/
├── notebooks/
├── python/
├── sql/
├── powerbi/
├── dashboards/
├── docs/
├── reports/
├── screenshots/
├── requirements.txt
└── README.md
```

## Technology stack

- Python: pandas, NumPy, matplotlib, scikit-learn
- SQL: relational modeling, joins, aggregations, CTEs and window functions
- Excel: data quality checks, cleaning and KPI preparation
- Power BI: Power Query, data modeling, DAX and interactive reporting
- Git/GitHub: version control and project documentation

## Project status

### Phase 1 — Foundation: in progress

- [x] Repository created
- [x] Project architecture documented
- [x] Synthetic data generation design
- [x] SQL schema and KPI query plan
- [x] Python analysis scaffolding
- [ ] Generate final dataset
- [ ] Complete EDA outputs
- [ ] Build Excel workbook
- [ ] Build Power BI dashboard
- [ ] Add final screenshots
- [ ] Complete academic report

## Reproducibility

After cloning the repository:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
# source .venv/bin/activate

pip install -r requirements.txt
python python/generate_retail_data.py
python python/run_analysis.py
```

The generator uses a fixed random seed so the analytical dataset can be reproduced consistently.

## Academic alignment

The project is intentionally structured to demonstrate the internship competencies stated on the internship certificate: data collection and cleaning, SQL, Power BI/Tableau-style visualization, insight generation, dashboard creation and SDLC-based project development.

## Author

**Soniya Rajpurohit**

B.Tech Practical Training / Data Analytics Internship Project
