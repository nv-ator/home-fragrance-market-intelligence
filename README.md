# Home Fragrance Market Intelligence

> **Automated Data Pipeline · SQLite · FastAPI · React · Vite · Business Intelligence**

An end-to-end market intelligence platform for analyzing publicly available home-fragrance product catalogues across five brands in India.

The system collects catalogue data, preserves raw source artifacts, cleans and validates records, standardizes pack sizes and unit economics, stores the analytical dataset in SQLite, exposes metrics through FastAPI, and presents the results through an interactive React dashboard.

---

## 1. Project Overview

The project provides an automated market intelligence workflow for the Indian home-fragrance category.

It follows the complete engineering lifecycle:

```text
Collect
  ↓
Clean
  ↓
Validate
  ↓
Transform
  ↓
Store
  ↓
Analyze
  ↓
Visualize
  ↓
Communicate
```

The platform is designed to help analyze:

- Product assortment
- Brand and category coverage
- Observed pricing
- Unit economics
- Ratings and review signals
- Discounts
- Product formats
- Portfolio gaps
- Observed price positioning

The analysis is based on publicly accessible catalogue data and **does not claim commercial market share, revenue, sales volume, or profitability**.

---

# 2. Business Objective

The objective is to provide a structured view of competitor product catalogues that can support category and brand analysis.

The system addresses questions such as:

- How are tracked brands positioned across observed price ranges?
- Which categories and product formats are represented?
- Where are observed catalogue concentrations or gaps?
- How do pack sizes affect comparable pricing?
- What rating and review signals are visible in public sources?
- Which portfolio areas could warrant further investigation?

All findings distinguish between:

**Observed Data → Interpretation → Business Question → Validation Required**

---

# 3. Brands Covered

The final dataset contains five tracked brands:

| Brand | Final Validated Products |
|---|---:|
| AromaPure | 298 |
| Godrej aer | 132 |
| Odonil | 132 |
| Air Wick | 91 |
| Ambi Pur | 31 |
| **Total** | **684** |

Each brand is processed through the same analytical pipeline and schema.

> **Important:** Product counts represent the collected public catalogue and should not be interpreted as market share.

---

# 4. Data Sources

Data was collected from publicly accessible e-commerce and brand catalogue sources.

| Brand | Source |
|---|---|
| AromaPure | Official public product catalogue |
| Odonil | Public Amazon India catalogue listings |
| Godrej aer | Public Amazon India catalogue listings |
| Air Wick | Public Amazon India catalogue listings |
| Ambi Pur | Public Amazon India catalogue listings |

Source URLs and raw collection artifacts are retained for auditability.

## Collection Policy

The project does **not** use:

- CAPTCHA bypass
- Authentication bypass
- Login circumvention
- Access-control circumvention
- Credential-based scraping
- Anti-bot bypass techniques

Collection uses standard public HTTP requests with configurable timeouts, retry handling, and polite request delays.

Raw responses are preserved before transformation.

---

# 5. System Architecture

```text
┌──────────────────────────────────────────────┐
│        Public Catalogue / E-commerce         │
│                 Sources                      │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│              Data Collection                 │
│             src/scrapers/                    │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│            Raw Data + Manifests              │
│                 data/raw/                    │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│          Cleaning & Validation               │
│              src/cleaning/                   │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│        Transformation & Normalization        │
│           src/transformation/                │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│             SQLite Database                  │
│          data/market_intelligence.db         │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│              FastAPI Backend                 │
│                   api/                       │
└──────────────────────┬───────────────────────┘
                       │ REST API
                       ▼
┌──────────────────────────────────────────────┐
│          React / Vite Dashboard              │
│                dashboard/                    │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
              Business Insights
```

---

# 6. Technology Stack

### Data Engineering

- Python
- Requests
- BeautifulSoup4
- Pandas
- SQLite
- SQL

### Backend

- FastAPI
- Uvicorn
- Pydantic

### Frontend

- React
- Vite
- Tailwind CSS
- Recharts

### Development & Testing

- Pytest
- Git
- GitHub

---

# 7. Data Schema

The analytical dataset captures observed product information and standardized dimensions.

| Field | Description |
|---|---|
| `product_id` | Unique SKU, ASIN, or composite identifier |
| `brand_name` | Standardized brand |
| `title` | Product title |
| `category` | Standardized category |
| `product_type` | Product format/type |
| `price` | Observed selling price in INR |
| `mrp` | MRP / compare-at price where available |
| `discount_pct` | Calculated discount where MRP is available |
| `pack_size_raw` | Original pack/size text |
| `standardized_unit` | `ml`, `g`, or `count` |
| `standardized_quantity` | Normalized quantity |
| `price_per_unit` | Price normalized to the applicable unit |
| `rating` | Observed rating |
| `review_count` | Observed review count |
| `platform` | Source platform |
| `availability` | Observed availability |
| `scraped_at` | Collection timestamp |

Source-specific provenance fields are retained where available.

Missing information remains `NULL` rather than being converted into artificial values.

---

# 8. Data Cleaning & Validation

The cleaning pipeline applies deterministic validation rules.

## Product Identity

- Amazon products use unique marketplace ASINs.
- AromaPure products use available product/variant/SKU identities.

## Deduplication

Duplicate observations are reduced to canonical product records.

## Home-Fragrance Scope

Products outside the defined home-fragrance scope are excluded from the analytical dataset.

This includes **car-only products** where they fall outside the defined home-fragrance scope.

## Price Validation

- Selling prices must be positive numeric INR values.
- Zero-price promotional/freebie records are rejected.
- Invalid price records are excluded.

## Missing Values

Missing values are preserved:

- Missing rating → `NULL`
- Missing review count → `NULL`
- Missing discount → `NULL`
- Missing seller → `NULL` where unavailable

Missing information is never interpreted as zero.

---

# 9. Final Dataset

The final validated dataset contains:

## Full Validated Dataset

**684 products**

| Brand | Products |
|---|---:|
| AromaPure | 298 |
| Godrej aer | 132 |
| Odonil | 132 |
| Air Wick | 91 |
| Ambi Pur | 31 |
| **Total** | **684** |

The final cleaning process excluded **135 car-only records** that were outside the defined home-fragrance analytical scope.

## Dashboard Analytical Sample

For consistent cross-brand dashboard comparisons, the dashboard uses a deterministic analytical sample of:

**120 products**

| Brand | Dashboard Products |
|---|---:|
| AromaPure | 24 |
| Godrej aer | 24 |
| Odonil | 24 |
| Air Wick | 24 |
| Ambi Pur | 24 |
| **Total** | **120** |

The 120-product sample is an analytical presentation sample and should not be confused with the complete 684-product validated dataset.

---

# 10. Price Normalization

Products are normalized according to their physical measurement type.

### Solids / Gels / Candles

Measured using:

```text
₹ / 100g
```

Formula:

```text
Selling Price / Total Grams × 100
```

### Liquids / Sprays / Oils

Measured using:

```text
₹ / 100ml
```

Formula:

```text
Selling Price / Total ml × 100
```

### Multi-packs

Where applicable:

```text
₹ / Unit
```

Formula:

```text
Selling Price / Total Units
```

## Integrity Rule

Mass and volume are kept strictly separate.

The pipeline does **not** make arbitrary assumptions such as:

```text
1g = 1ml
```

---

# 11. Database Architecture

The analytical database uses **SQLite**.

Database:

```text
data/market_intelligence.db
```

## Main Tables

### `brands`

Stores the tracked brand master data.

### `categories`

Stores standardized category definitions.

### `data_sources`

Stores source and platform metadata.

### `products`

Stores canonical analytical product records.

The product records contain pricing, ratings, reviews, availability, pack-size information, normalized quantities, source metadata, and collection timestamps.

---

# 12. Analytical SQL

Reusable analytical views are defined in:

```text
sql/schema.sql
```

Important views include:

```text
vw_products_analytical
vw_market_overview
vw_brand_comparison
vw_category_coverage
```

Reusable analytical queries are available in:

```text
sql/analytics_queries.sql
```

The database can be deterministically rebuilt from the processed dataset using:

```bash
python main.py --stage database --rebuild
```

---

# 13. Automated Pipeline

The entire workflow can be executed through:

```bash
python main.py
```

Pipeline flow:

```text
python main.py
      │
      ▼
   COLLECT
      │
      ▼
    CLEAN
      │
      ▼
  TRANSFORM
      │
      ▼
  DATABASE
      │
      ▼
  VALIDATE
      │
      ▼
   REPORT
```

## Pipeline Stages

### Collection

Collect public catalogue data and preserve raw responses.

### Cleaning

Perform:

- Deduplication
- Brand validation
- Scope filtering
- Price validation
- Missing-value handling

### Transformation

Perform:

- Numerical coercion
- Unit normalization
- Quantity standardization
- Feature preparation

### Database

Load canonical records into SQLite.

### Validation

Run automated quality checks.

### Reporting

Generate pipeline execution and validation information.

---

# 14. CLI Commands

### Run the complete pipeline

```bash
python main.py
```

### Collection only

```bash
python main.py --stage collect
```

### Cleaning only

```bash
python main.py --stage clean
```

### Transformation only

```bash
python main.py --stage transform
```

### Database rebuild

```bash
python main.py --stage database --rebuild
```

### Validation

```bash
python main.py --stage validate
```

### Help

```bash
python main.py --help
```

---

# 15. FastAPI Backend

The FastAPI service provides the REST layer between SQLite and the React dashboard.

```text
SQLite
   ↓
FastAPI
   ↓
Parameterized SQL / Pydantic
   ↓
React Dashboard
```

## Run the API

```bash
python -m uvicorn api.main:app --reload --port 8000
```

API documentation:

```text
http://localhost:8000/docs
```

OpenAPI schema:

```text
http://localhost:8000/openapi.json
```

## API Endpoints

| Endpoint | Purpose |
|---|---|
| `/api/health` | API/database health check |
| `/api/overview` | Market-level KPIs |
| `/api/brands` | Tracked brands |
| `/api/brands/comparison` | Brand comparison |
| `/api/brands/{brand_name}` | Brand-level diagnostics |
| `/api/products` | Filterable product catalogue |
| `/api/products/{product_id}` | Product details |
| `/api/analytics/price-positioning` | Price/rating analysis |
| `/api/analytics/price-normalization` | Unit economics |
| `/api/analytics/categories` | Category analysis |
| `/api/analytics/platforms` | Platform analysis |
| `/api/analytics/discounts` | Discount analysis |
| `/api/analytics/category-coverage` | Brand × category coverage |
| `/api/filters` | Dashboard filter values |

---

# 16. React Business Intelligence Dashboard

The frontend is built with:

- React
- Vite
- Tailwind CSS
- Recharts

The frontend communicates with the FastAPI backend through REST APIs.

## Dashboard Structure

```text
dashboard/
├── package.json
├── vite.config.js
├── tailwind.config.js
├── index.html
└── src/
    ├── main.jsx
    ├── App.jsx
    ├── api/
    │   └── client.js
    ├── components/
    │   ├── Header.jsx
    │   ├── Sidebar.jsx
    │   ├── KpiCard.jsx
    │   ├── ChartCard.jsx
    │   ├── FilterBar.jsx
    │   ├── DataTable.jsx
    │   └── EmptyState.jsx
    ├── pages/
    │   ├── Overview.jsx
    │   ├── BrandComparison.jsx
    │   ├── PricePositioning.jsx
    │   ├── ProductAnalysis.jsx
    │   └── BusinessInsights.jsx
    └── styles/
        └── index.css
```

---

# 17. Dashboard Pages

## Market Overview

Provides:

- Total observed products
- Tracked brands
- Average price
- Median price
- Average rating
- Average observed discount
- Brand assortment
- Category distribution
- Platform distribution
- Price distribution

---

## Brand Comparison

Provides symmetric comparison across all five brands.

Metrics include:

- Average price
- Median price
- Average rating
- Assortment count
- Category coverage
- Observed review engagement

---

## Price Positioning

Provides:

- Price vs. rating analysis
- ₹/100ml comparisons
- ₹/100g comparisons
- Discount distribution
- Product clustering

---

## Product Analysis

Provides searchable and filterable product-level analysis.

Available filters include:

- Brand
- Category
- Platform
- Product type
- Pack size
- Availability
- Price range
- Rating
- Keyword search

---

## Business Insights

Provides diagnostic business-analysis panels based on observed catalogue data.

The framework is:

```text
Observation
     ↓
Interpretation
     ↓
Commercial Question
     ↓
Validation Required
```

---

# 18. Product Clustering

K-Means clustering is applied to products with complete numerical features.

Features include:

- Selling price
- Rating
- Discount percentage
- `log(1 + reviews)`

Candidate values of:

```text
K = 2 ... 5
```

are evaluated using silhouette score.

Clusters are labelled neutrally:

```text
Cluster 1
Cluster 2
Cluster 3
Cluster 4
```

The system intentionally avoids subjective commercial labels such as:

- Premium
- Budget
- Value
- Mass-Market

---

# 19. Portfolio Gap Methodology

The dashboard uses a diagnostic framework to identify areas for further investigation.

### 1. Category Voids

Categories where a brand has limited or no observed assortment while other tracked brands have collected products.

### 2. Price-Tier Gaps

Price ranges where the observed assortment is limited or absent.

### 3. Engagement Asymmetries

Categories where competitor review engagement is visibly higher while observed assortment is limited.

### 4. Decision Framework

Every finding follows:

```text
Observed Data
      ↓
Interpretation
      ↓
Business Question
      ↓
Investigation Area
      ↓
Validation Required
```

These findings are **investigation areas**, not direct product-launch recommendations.

---

# 20. Analytical Boundaries

The dashboard deliberately distinguishes catalogue observations from commercial conclusions.

## Catalogue Assortment ≠ Market Share

Percentages represent:

```text
Share of Collected Assortment
```

They do not represent:

- Market share
- Sales share
- Revenue share

## Reviews ≠ Sales

Review counts represent public customer-feedback visibility and should not be interpreted as:

- Sales volume
- Sales velocity
- Revenue
- Market share

## Category Absence

A category with zero observed products means:

> No product was observed in the collected public dataset.

It does **not** prove that the brand commercially offers no such product.

## Price Positioning

Positioning is analyzed using:

- Mean
- Median
- Percentiles
- Distribution
- Unit pricing
- Price vs. rating relationships

No subjective price-tier labels are assigned.

---

# 21. Business Insights Framework

The project separates factual observations from interpretations.

### Factual Observation

Directly measurable information from the validated dataset.

### Analytical Interpretation

A hypothesis that explains an observed pattern without claiming causality.

### Commercial Business Question

A question that can be investigated by a brand or category manager.

### Internal Validation Required

Additional proprietary information required before making a commercial decision.

Examples of required internal validation include:

- Sales data
- POS sell-through
- Gross margins
- COGS
- Customer research
- Distribution capability
- Demand signals

---

# 22. Limitations

### Catalogue Scope

The dataset represents publicly collected catalogue information at the time of collection, not total historical or offline sales.

### Commercial Metrics

The project does not contain reliable public information for:

- Revenue
- Sales velocity
- Conversion rates
- Margins
- Profitability

### Platform Bias

Marketplace ranking and visibility mechanisms may influence which products are surfaced.

### Review Comparability

Review counts depend on the source and availability of public information.

Marketplace and official-brand review counts should not automatically be treated as directly comparable.

### Catalogue Coverage

Absence from the collected dataset does not prove that a brand has no commercial offering in that category.

### Market Share

Observed assortment must not be interpreted as commercial market share.

---

# 23. Setup

## Prerequisites

- Python 3.10+
- Node.js 18+
- npm

## Create Python Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

## Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

# 24. Run the Dashboard

Start the FastAPI backend first:

```bash
python -m uvicorn api.main:app --reload --port 8000
```

Then start the React dashboard:

```bash
cd dashboard
npm install
npm run dev
```

The frontend runs at:

```text
http://localhost:5173
```

The API runs at:

```text
http://localhost:8000
```

---

# 25. Environment Configuration

The frontend can optionally use:

```env
VITE_API_BASE_URL=http://localhost:8000
```

If this variable is omitted, the frontend defaults to:

```text
http://localhost:8000
```

For production deployment, `VITE_API_BASE_URL` should point to the publicly accessible FastAPI backend URL.

---

# 26. Production Build

Build the React application with:

```bash
cd dashboard
npm run build
```

The production output is generated in:

```text
dashboard/dist/
```

---

# 27. Testing

Run the automated test suite:

```bash
pytest tests/ -v
```

The tests cover areas including:

- Data collection
- Cleaning rules
- Unit normalization
- Database operations
- Pipeline orchestration
- API endpoints

The final project was validated through automated tests and production frontend build verification.

---

# 28. Project Structure

```text
home-fragrance-market-intelligence/
│
├── api/
│   ├── main.py
│   └── routes/
│
├── config/
│   └── config.yaml
│
├── dashboard/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── market_intelligence.db
│
├── docs/
│   ├── BUSINESS_REQUIREMENT_COVERAGE.md
│   ├── FINAL_METRICS.md
│   ├── FINAL_PROJECT_STATUS.md
│   ├── FINAL_REQUIREMENT_GAP_RESULT.md
│   └── FINAL_SUBMISSION_CHECKLIST.md
│
├── sql/
│   ├── schema.sql
│   └── analytics_queries.sql
│
├── src/
│   ├── cleaning/
│   ├── database/
│   ├── pipeline/
│   ├── scrapers/
│   ├── transformation/
│   └── utils/
│
├── tests/
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

# 29. Reproducibility & Provenance

The project preserves collection provenance through:

- Raw source artifacts
- Source metadata
- Collection timestamps
- Collection manifests
- Pipeline execution manifests
- Processed datasets
- Validation reports

A separate `scrape_runs` database table is not required because run-level provenance is maintained through these collection and pipeline artifacts.

---

# 30. AI Usage Disclosure

AI-assisted tools were used during development primarily for:

- Debugging
- Documentation assistance
- Development support

All generated suggestions and code changes were reviewed, tested, and validated against the project requirements and automated test suite.

---

# 31. Future Improvements

Potential production improvements include:

- Scheduled recurring ingestion
- Historical price tracking
- Price-change detection
- Review sentiment analysis
- Fragrance-profile extraction using NLP
- Regional quick-commerce availability feeds
- Additional public catalogue sources
- Historical dashboard snapshots
- Automated monitoring of catalogue changes

---

# 32. Key Project Takeaways

The project demonstrates an end-to-end data engineering and business intelligence workflow:

```text
Public Data
    ↓
Automated Collection
    ↓
Raw Data Preservation
    ↓
Cleaning & Validation
    ↓
Unit Normalization
    ↓
SQLite Storage
    ↓
FastAPI Analytics Layer
    ↓
React BI Dashboard
    ↓
Evidence-Based Insights
```

The final validated catalogue contains **684 products across five brands**, while a deterministic **120-product balanced sample** is used for consistent dashboard-level comparison.

The system is designed to support **evidence-based market intelligence without fabricating market share, sales, revenue, or unavailable commercial metrics**.

---

## License / Assignment Use

This project was developed as part of a technical assignment demonstrating data collection, automation, data engineering, analytics, visualization, and business insight generation.
