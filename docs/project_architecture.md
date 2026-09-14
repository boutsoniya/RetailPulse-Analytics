# RetailPulse Project Architecture

## Objective

RetailPulse is an end-to-end retail analytics portfolio project designed to demonstrate the internship competencies of data collection and cleaning, SQL analysis, visualization/dashboard creation, insight generation and SDLC-based project development.

## Architecture

```text
Raw Retail Transactions
          |
          v
   Data Quality Layer
   Excel + Python
          |
          v
 Clean Analytical Dataset
       /       \
      /         \
     v           v
   SQL        Python EDA
    |             |
    +------ + ----+
           |
           v
     Analytical Model
           |
           v
        Power BI
           |
     +-----+-----+----------------+
     |           |                |
 Executive     Sales          Customer / Profit
 Dashboard   Dashboard          Intelligence
     |           |                |
     +-----------+----------------+
                 |
                 v
       Management Insights
                 |
                 v
     Recommendations / Forecast
```

## Development lifecycle

1. **Requirement analysis** — define business questions and KPIs.
2. **Data collection** — generate a reproducible synthetic retail transaction dataset.
3. **Data preparation** — validate, clean and engineer analytical fields.
4. **Database design** — separate customer, product and sales entities.
5. **Analysis** — calculate KPIs, trends, profitability and customer segments.
6. **Visualization** — translate validated metrics into decision-oriented Power BI pages.
7. **Testing** — cross-check totals and KPI definitions across layers.
8. **Documentation** — preserve assumptions, data dictionary, queries and methodology.
9. **Delivery** — publish reproducible code and supporting artifacts through GitHub.

## Design principles

- **Reproducibility:** synthetic data is generated from a fixed seed.
- **Traceability:** dashboard KPIs can be traced back to source columns and SQL/Python calculations.
- **Explainability:** methods are selected so they can be defended in an academic viva.
- **Separation of concerns:** data, analysis, SQL, visualization and documentation are stored separately.
- **No confidential claims:** the dataset does not represent WSA or any real client.
