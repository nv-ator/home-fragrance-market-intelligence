# Home Fragrance Market Intelligence

## 1. Project Overview

This project provides an automated, end-to-end market intelligence pipeline and interactive analytics dashboard focused on the home fragrance sector in India. It systematically ingests publicly accessible product catalogue data across five selected competitor brands, executes a rigorous cleaning and unit-standardization pipeline, normalizes pricing metrics, and powers an exploratory React dashboard delivering brand positioning and portfolio insights.

## 2. Business Objective

The primary business objective is to empower brand managers, category planners, and market researchers to evaluate brand positioning across observed e-commerce catalogues without relying on speculative or fabricated sales estimates.

The platform addresses key questions:

- How do key competitors position their catalogues across price tiers and formats?
- Where are observed strengths, coverage concentrations, and portfolio gaps?
- What are the customer rating signals and engagement footprints across pack sizes and categories?

## 3. Selected Brands

The pipeline systematically analyzes five selected brands in the Indian home fragrance space:

1. **AromaPure** — D2C and marketplace catalogue covering diffusers, room sprays, candles, and fragrance products
2. **Odonil** — air freshening blocks, gels, and room sprays
3. **Godrej aer** — bathroom fresheners, aerosol sprays, and automatic diffusers
4. **Air Wick** — automatic sprays, plug-in diffusers, and refills
5. **Ambi Pur** — car fresheners, air sprays, and bathroom fresheners

**Note:** AromaPure receives no special bias or asymmetric treatment in the schema, metrics, or dashboard interface. All five brands are evaluated symmetrically.

## 4. Data Sources

Data is sourced strictly from public, accessible e-commerce and brand catalogue sources without bypassing access controls, authentication walls, or CAPTCHA:

- **AromaPure:** Official public product catalogue endpoint (`https://aromahpure.com/products.json`)
- **Odonil:** Public Amazon India catalogue search listings
- **Godrej aer:** Public Amazon India catalogue search listings
- **Air Wick:** Public Amazon India catalogue search listings
- **Ambi Pur:** Public Amazon India catalogue search listings

Source URLs and raw collection artifacts are preserved in the project for auditability.

## 5. Data Collection Method

- **Methodology:** Polite HTTP requests using standard headers to public endpoints and public search/catalogue listings using `requests` and `BeautifulSoup4`.
- **Access policy:** No browser automation, CAPTCHA bypass, login bypass, authentication bypass, or access-control circumvention was used.
- **Request behavior:** Configurable timeouts, retry handling with exponential backoff, and polite sequential delays between marketplace requests.
- **Compliance:** Access restrictions are respected and collection activities are logged with audit provenance.
- **Storage:** Raw responses are preserved in `data/raw/` before parsing or transformation. Collection manifests are generated for pipeline runs.

## 6. Pipeline Architecture

```text
Public E-commerce / Catalogue Sources
                ↓
     Data Collection / Scraper
          (src/scrapers/)
                ↓
       Raw Data & Manifests
       (data/raw/)
                ↓
      Cleaning & Validation
       (src/cleaning/)
                ↓
         Standardization
      (src/transformation/)
                ↓
       Analytics Dataset
    (data/processed/ + SQLite)
                ↓
         FastAPI Backend
             (api/)
                ↓
      React / Vite Dashboard
          (dashboard/)
                ↓
        Business Insights
```

## 7. Data Schema

The unified analytical dataset schema captures both raw observed attributes and standardized dimensions:

- `product_id`: Unique identifier (SKU, ASIN, or composite hash)
- `brand_name`: Standardized brand identifier
- `title`: Complete product title as listed
- `category`: Standardized home fragrance category
- `product_type`: Specific format/form factor
- `price`: Observed selling price in INR
- `mrp`: Maximum Retail Price / Compare-at price where available
- `discount_pct`: Observed discount percentage calculated from selling price and MRP
- `pack_size_raw`: Extracted text describing quantity/volume
- `standardized_unit`: Base unit of measurement (`ml`, `g`, `count`)
- `standardized_quantity`: Total normalized numerical quantity in base units
- `price_per_unit`: Standardized price per unit
- `rating`: Observed average consumer star rating
- `review_count`: Observed number of consumer reviews/ratings
- `platform`: Source channel
- `availability`: Stock availability status
- `scraped_at`: Timestamp of collection in UTC

Source-specific provenance fields are retained where applicable, including review-source and seller information.

## 8. Cleaning & Validation

The data cleaning stage implements verification rules including:

- **Canonical Product Identity**
  - Amazon listings: Unique marketplace ASIN
  - AromaPure catalogue: Unique product and variant/SKU identity where available

- **Deduplication**
  - Duplicate search observations are identified and reduced to one canonical product record.

- **Home Fragrance Scoping**
  - Car-only products and unrelated non-fragrance products are excluded from the analytical dataset where they fall outside the defined home-fragrance scope.

- **Price Sanity & Outlier Handling**
  - Selling prices must be positive numeric INR values.
  - Zero-price promotional/freebie records are rejected.

- **Missing Value Preservation**
  - Missing fields remain `NULL`.
  - Missing discounts are never converted to 0%.
  - Missing ratings are never converted to 0.

## 9. Price Normalization

To enable meaningful comparisons across disparate product formats:

- grams (`g`) for solids/gels/candles
- milliliters (`ml`) for liquids/sprays/oils
- units (`count`) for multi-packs

### Normalized Price Metrics

- **Price per Unit**

  `Selling Price / Total Units`

  Available across the validated 767-product dataset.

- **Price per 100ml**

  `Selling Price / Total ml × 100`

  Available for 271 liquid products.

- **Price per 100g**

  `Selling Price / Total grams × 100`

  Available for 30 solid products.

### Integrity Rule

Mass and volume metrics are strictly separated. No arbitrary density conversions such as `1g = 1ml` are applied.

## 10. Analytics Dataset Statistics

- **Total Validated Products:** **767**

### Validated Products by Brand

- **AromaPure:** 360 products
- **Odonil:** 145 products
- **Godrej aer:** 129 products
- **Air Wick:** 91 products
- **Ambi Pur:** 42 products

- **Rejected Records:** 669 records across duplicate, out-of-scope, zero-price, and invalid-brand validation categories.

Rejected records are preserved in:

`data/processed/products_rejected.csv`

## 11. Database Architecture & Analytical Model

The local analytical storage uses **SQLite**, providing lightweight local deployment and transactional database functionality suitable for the analytical workload.

### Relational Schema

The database includes:

- **`brands`** — brand master table
- **`categories`** — standardized category definitions
- **`data_sources`** — source and platform metadata
- **`products`** — canonical analytical product records

The `products` table contains pricing, discount, rating, review, availability, pack-size, normalized quantity, unit economics, source, and collection metadata.

### Reusable Analytical Views & SQL

Reusable analytical views are defined in:

`sql/schema.sql`

including:

- `vw_products_analytical`
- `vw_market_overview`
- `vw_brand_comparison`
- `vw_category_coverage`

Parametric analytical queries are available in:

`sql/analytics_queries.sql`

### Database Loading & Rebuild

The database can be deterministically rebuilt from the processed dataset:

```bash
python main.py --stage database --rebuild
```

## 12. Dashboard Architecture

The web dashboard is built using:

- React
- Vite
- Tailwind CSS
- Recharts

### Dashboard Sections

- **Market Overview**
  - Key market KPIs
  - Platform breakdown
  - Category and format distribution

- **Brand Comparison**
  - Average and median price
  - Average rating
  - Assortment count
  - Category coverage
  - Review engagement signals

- **Price Positioning**
  - Price vs. Rating
  - Price-per-unit comparisons
  - Discount distribution
  - Product clustering

- **Product Analysis**
  - Searchable and filterable product catalogue
  - Multi-attribute filtering
  - Product-level detail view

- **Business Insights**
  - Data-driven diagnostic panels
  - Category coverage observations
  - Portfolio investigation areas

## 13. Portfolio Gap Methodology

The system identifies portfolio opportunities through an objective diagnostic framework:

1. **Category Void**
   - Identifies categories where a brand has no or limited observed assortment while other tracked brands have collected products.

2. **Price Tier Blank Spots**
   - Identifies price bands with limited or no observed products for a brand.

3. **Engagement Asymmetries**
   - Identifies categories where competitor review engagement is visibly higher while observed brand assortment is limited.

4. **Structured Decision Framing**

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

These findings are intended as analytical investigation areas rather than direct product-launch recommendations.

## 14. Limitations

- **Catalogue Scope:** Metrics represent the collected public catalogue sample at the time of scraping, not total historical or offline sales volume.
- **No Private Commercial Metrics:** Sales velocity, revenue, conversion rates, margins, and profitability are not publicly available and are excluded.
- **Platform Bias:** Marketplace visibility and ranking algorithms may influence which products are surfaced.
- **Review Comparability:** Review counts depend on the source and availability of public review information. Marketplace and official-brand review counts should not automatically be treated as directly comparable.
- **Catalogue Coverage:** Absence from the collected dataset does not prove that a brand does not commercially offer a product in that category.
- **Market Share:** Share of collected assortment must not be interpreted as commercial market share.

## 15. Setup

### Prerequisites

- Python 3.10+
- Node.js 18+
- npm

### Python Environment

```bash
python -m venv venv
```

#### Windows

```bash
venv\Scripts\activate
```

#### Linux/macOS

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## 16. Reproducible Automation

The complete end-to-end pipeline is automated and reproducible through a single command:

```bash
python main.py
```

### Complete Pipeline Flow

```text
python main.py
      ↓
[COLLECT]
Public ingestion from selected catalogue sources
      ↓
[CLEAN]
Deduplication, scope filtering, price validation
      ↓
[TRANSFORM]
Type enforcement and standardized dimensions
      ↓
[DATABASE]
SQLite analytical dataset loading
      ↓
[VALIDATE]
Automated quality gate
      ↓
[REPORT]
Pipeline execution manifest and validation report
```

### Transformation Methodology

The transformation stage performs deterministic processing:

- Numerical coercion for prices, discounts, ratings, reviews, and quantities
- Standardized quantity and unit handling
- Preservation of unavailable values as `NULL`
- No speculative business labels such as "Value", "Mass-Market", or "Premium"
- Analytical positioning based on observed empirical distributions

### Re-execution

Running:

```bash
python main.py
```

repeatedly uses the deterministic pipeline/database process and avoids duplicate analytical records.

### Modular CLI Commands

```bash
# Full pipeline
python main.py

# Collection only
python main.py --stage collect

# Cleaning only
python main.py --stage clean

# Transformation only
python main.py --stage transform

# Database rebuild
python main.py --stage database --rebuild

# Validation / quality gate
python main.py --stage validate

# Help
python main.py --help
```

## 17. Analytical API Layer — FastAPI Backend

The FastAPI analytical service provides a REST delivery layer between the SQLite analytical database and the React/Vite dashboard.

### Architecture

```text
SQLite
  ↓
FastAPI
  ↓
Parameterized SQL / Pydantic
  ↓
React / Vite Dashboard
```

### Running the API

```bash
python -m uvicorn api.main:app --reload --port 8000
```

API documentation:

`http://localhost:8000/docs`

OpenAPI schema:

`http://localhost:8000/openapi.json`

### Endpoint Catalog

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/health` | GET | API and database health check |
| `/api/overview` | GET | Market-level KPIs |
| `/api/brands` | GET | Tracked brand list |
| `/api/brands/comparison` | GET | Brand comparison metrics |
| `/api/brands/{brand_name}` | GET | Brand-level diagnostics |
| `/api/products` | GET | Filterable and paginated product catalogue |
| `/api/products/{product_id}` | GET | Individual product record |
| `/api/analytics/price-positioning` | GET | Price vs. rating analytical data |
| `/api/analytics/price-normalization` | GET | Unit pricing metrics |
| `/api/analytics/categories` | GET | Category-level analysis |
| `/api/analytics/platforms` | GET | Platform/channel analysis |
| `/api/analytics/discounts` | GET | Discount analysis |
| `/api/analytics/category-coverage` | GET | Brand × category coverage |
| `/api/filters` | GET | Dynamic dashboard filter values |

### Data Quality & Null Handling

- Missing ratings, reviews, and discounts are returned as JSON `null`.
- Missing values are never converted to artificial zero values.
- Database queries use parameterized SQL.
- Analytical queries use database indexes where applicable.

## 18. React Business Intelligence Dashboard

The frontend is a responsive Business Intelligence dashboard built with **React**, **Vite**, **Tailwind CSS**, and **Recharts**.

It communicates with the FastAPI analytical backend over REST endpoints.

### Dashboard Structure

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

### Installation & Execution

```bash
cd dashboard
npm install
npm run dev
```

The application runs at:

`http://localhost:5173`

Production build:

```bash
npm run build
```

### Environment Configuration

Optional `.env` configuration:

```env
VITE_API_BASE_URL=http://localhost:8000
```

If omitted, the frontend defaults to:

`http://localhost:8000`

## 19. Dashboard Pages & Visualizations

### 1. Market Overview

Displays:

- Total observed products
- Tracked brands
- Average price
- Median price
- Average rating
- Average observed discount
- Assortment by brand
- Assortment by category
- Assortment by platform
- Observed price distribution

### 2. Brand Comparison

Provides symmetric comparison across:

- AromaPure
- Odonil
- Godrej aer
- Air Wick
- Ambi Pur

Metrics include:

- Average price
- Median price
- Average rating
- Assortment count
- Category coverage
- Observed review engagement

### 3. Price Positioning

Includes:

- Interactive Price vs. Rating scatter plot
- Segregated ₹/100ml and ₹/100g unit economics
- Promotional discount distribution
- Product clustering

#### Product Clustering

K-Means clustering is applied to products with complete numerical features including:

- Selling price
- Rating
- Discount percentage
- `log(1 + reviews)`

Candidate values of `K=2..5` are evaluated using silhouette score.

Clusters are labelled neutrally as:

- Cluster 1
- Cluster 2
- Cluster 3
- Cluster 4

No subjective commercial labels such as "Premium" or "Budget" are assigned.

### 4. Product Analysis

Provides dynamic filtering by:

- Brand
- Category
- Platform
- Product type / format
- Pack size / count
- Availability
- Price range
- Rating
- Keyword search

The catalogue is paginated and provides product-level details and public source links.

### 5. Business Insights

Uses a four-part diagnostic framework:

**Observation → Interpretation → Commercial Question → Validation Required**

The dashboard also provides a Brand × Category observed coverage matrix.

## 20. Business Insights Approach

The dashboard translates factual catalogue observations into commercial decision-support using a reproducible analytical structure.

### Observation vs. Interpretation

- **Factual Observation:** Directly measurable data from the verified dataset.
- **Analytical Interpretation:** A hypothesis explaining an observed pattern without claiming causality.
- **Commercial Business Question:** A strategic question that a brand manager could investigate.
- **Internal Validation Required:** Proprietary information needed before making a commercial decision.

### Analytical Boundaries

#### Catalogue Assortment vs. Market Share

Percentages represent **Share of Collected Assortment**, not commercial market share or sales share.

#### Review Engagement vs. Market Share

Observed review counts represent customer-feedback visibility on the collected public sources. They should not be interpreted as market share, sales volume, or sales velocity.

AromaPure official review information was available for a subset of products. These source-specific observations are retained with their provenance, while unavailable values remain `NULL`.

#### Category Coverage

A zero in the category coverage matrix means:

> No observed product in the collected public dataset.

It does not prove that the brand has no commercial offering in that category.

#### Price Positioning

Price positioning is analyzed using:

- Mean
- Median
- Percentiles
- Distribution
- Unit pricing
- Price vs. rating relationships

Subjective labels such as:

- Value
- Mass-Market
- Premium
- Budget

are intentionally excluded.

#### Unit Economics

Liquid products are evaluated separately using ₹/100ml and solid products using ₹/100g.

Mass and volume are never combined through arbitrary density assumptions.

#### Portfolio Opportunity Framing

Observed catalogue gaps are presented as investigation areas rather than direct product-launch recommendations.

Commercial decisions should be validated using internal information such as:

- Sales data
- POS sell-through
- Gross margins
- COGS
- Customer research
- Distribution capability
- Demand signals

## 21. Testing

Run the automated test suite covering collection parsers, cleaning rules, unit normalization, database operations, pipeline orchestration, and API endpoints:

```bash
pytest tests/ -v
```

## 22. AI Usage Disclosure

AI-assisted tools were used during development primarily for debugging, documentation assistance, and development support.

All generated suggestions and code changes were reviewed, tested, and validated against the project requirements and automated test suite.

## 23. Future Improvements

Potential future improvements include:

- Scheduled recurring ingestion to track historical price and promotional changes
- Historical price tracking and change detection
- Natural Language Processing for customer-review sentiment and fragrance-profile extraction
- Integration of regional quick-commerce availability feeds
- Additional public catalogue sources for broader market coverage
- Historical dashboard snapshots for trend analysis
