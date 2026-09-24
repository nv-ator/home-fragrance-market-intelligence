# Home Fragrance Market Intelligence & Brand Positioning

## 1. Project Overview
This project provides an automated, end-to-end market intelligence pipeline and interactive analytics dashboard focused on the home fragrance sector in India. It systematically ingests publicly accessible product catalogue data across five major competitor brands, executes a rigorous cleaning and unit-standardization pipeline, normalizes pricing metrics, and powers an exploratory React dashboard delivering actionable brand positioning insights.

## 2. Business Objective
The primary business objective is to empower brand managers, category planners, and market researchers to evaluate brand positioning across observed e-commerce catalogues without relying on speculative or fabricated sales estimates. The platform addresses key questions:
- How do key competitors position their catalogues across price tiers and formats?
- Where are observed strengths, coverage concentrations, and portfolio gaps?
- What are the customer rating signals and engagement footprints across pack sizes and categories?

## 3. Selected Brands
The pipeline systematically analyzes five prominent brands in the Indian home fragrance space:
1. **AromaPure** (D2C and marketplace catalogue: diffusers, room sprays, candles, flakes)
2. **Odonil** (Market leader in air freshening blocks, gels, and room sprays)
3. **Godrej aer** (Market leader in bathroom fresheners, aerosol sprays, and automatic diffusers)
4. **Air Wick** (Global FMCG brand specialized in automatic sprays, plug-in diffusers, and refills)
5. **Ambi Pur** (P&G brand prominent in car fresheners, air sprays, and bathroom fresheners)

*Note: AromaPure receives no special bias or asymmetric treatment in the schema, metrics, or dashboard interface. All five brands are evaluated symmetrically.*

## 4. Data Sources
Data is sourced strictly from public, accessible e-commerce and brand catalogue sources without bypassing access controls, authentication walls, or CAPTCHA:
- **AromaPure**: Official public product catalogue endpoint (`https://aromahpure.com/products.json`).
- **Odonil**: Public Amazon India catalogue search listings (`https://www.amazon.in/s?k=Odonil+air+freshener`, etc.).
- **Godrej aer**: Public Amazon India catalogue search listings (`https://www.amazon.in/s?k=Godrej+aer+air+freshener`, etc.).
- **Air Wick**: Public Amazon India catalogue search listings (`https://www.amazon.in/s?k=Air+Wick+air+freshener`, etc.).
- **Ambi Pur**: Public Amazon India catalogue search listings (`https://www.amazon.in/s?k=Ambi+Pur+air+freshener`, etc.).

## 5. Data Collection Method
- **Methodology**: Polite HTTP requests using standard headers to public endpoints and public search/catalogue listings using `requests` and `BeautifulSoup4`. No browser automation (Selenium/Playwright), CAPTCHA bypass, or login bypass.
- **Request Behavior**: Configurable timeouts (15s), exponential backoff retries (3 attempts), and polite sequential delays (2.5s–4.0s) between marketplace requests.
- **Compliance**: Respects access restrictions and logs all activities with audit provenance.
- **Storage**: Raw responses are preserved immutably in `data/raw/` (JSON for AromaPure, HTML files for Amazon searches) before any parsing or transformation occurs. A collection run manifest (`data/raw/manifests/collection_<run_id>.json`) is generated for every run.

## 6. Pipeline Architecture
```
Public E-commerce / Catalogue Sources
                ↓
    Data Collection / Scraper (src/scrapers/)
                ↓
            Raw Data (data/raw/) & Manifests (data/raw/manifests/)
                ↓
       Cleaning & Validation (src/cleaning/)
                ↓
          Standardization (src/transformation/)
                ↓
    Analytics Dataset (data/processed/ & SQLite)
                ↓
          FastAPI Backend (api/)
                ↓
        React / Vite Dashboard (dashboard/)
                ↓
          Business Insights
```

## 7. Data Schema
The unified analytical dataset schema captures both raw observed attributes and standardized dimensions:
- `product_id`: Unique identifier (SKU, ASIN, or composite hash)
- `brand_name`: Standardized brand identifier (AromaPure, Odonil, Godrej aer, Air Wick, Ambi Pur)
- `title`: Complete product title as listed
- `category`: Standardized home fragrance category (e.g., Room Spray, Automatic Spray, Pocket/Gel, Reed Diffuser, Scented Candle)
- `product_type`: Specific format/form factor
- `price`: Observed selling price in INR (float)
- `mrp`: Maximum Retail Price / Compare-at price in INR (float, where available)
- `discount_pct`: Observed discount percentage calculated as `((mrp - price) / mrp) * 100`
- `pack_size_raw`: Extracted text describing quantity/volume (e.g., "10g", "250ml", "Pack of 3")
- `standardized_unit`: Base unit of measurement (`ml`, `g`, `count`)
- `standardized_quantity`: Total normalized numerical quantity in base units
- `price_per_unit`: Standardized price per unit (INR per ml / INR per g / INR per count)
- `rating`: Observed average consumer star rating (0.0 to 5.0)
- `review_count`: Total number of consumer reviews/ratings
- `platform`: Source channel (e.g., `AromaPure Official`, `Amazon India`)
- `availability`: Stock availability status (`In Stock`, `Out of Stock`)
- `scraped_at`: Timestamp of collection (UTC)

## 8. Cleaning & Validation
The data cleaning stage implements rigorous verification rules:
- **Canonical Product Identity**:
  - Amazon listings: Unique marketplace ASIN.
  - AromaPure catalogue: Unique composite key `Product_ID` + `Variant_ID` (or SKU).
- **Deduplication**: Automatically identified 556 duplicate search observations and preserved 1 canonical record per product.
- **Home Fragrance Scoping**: Explicitly excluded 66 car-only products (e.g. car dashboard perfume, car vent clips) and 2 unrelated cleaners, prioritizing ambient and home air care.
- **Price Sanity & Outlier Handling**: Required positive numeric selling prices in INR; eliminated 41 zero-price promotional freebie entries.
- **Missing Value Preservation**: Missing fields remain `NULL`. Never defaulted missing discount to 0% or missing ratings to 0.

## 9. Price Normalization
To enable meaningful comparisons across disparate product formats:
- Quantities are parsed into standardized metrics: grams ($g$) for solids/gels/candles, milliliters ($ml$) for liquids/sprays/oils, and units ($count$) for multi-packs.
- Normalized price metrics:
  - $\text{Price per Unit} = \frac{\text{Selling Price}}{\text{Total Units}}$ (100% coverage, 767 products)
  - $\text{Price per 100ml} = \frac{\text{Selling Price}}{\text{Total ml}} \times 100$ (35.3% coverage, 271 liquid products)
  - $\text{Price per 100g} = \frac{\text{Selling Price}}{\text{Total grams}} \times 100$ (3.9% coverage, 30 solid products)
- **Integrity Rule**: Mass and volume metrics are strictly separated. No arbitrary density conversions ($1g \neq 1ml$) are applied.

## 10. Analytics Dataset Statistics
- **Total Validated Products**: **767** (exceeds 100+ requirement by 7.6x)
- **Validated Products by Brand**:
  - **AromaPure**: 360 products
  - **Odonil**: 145 products
  - **Godrej aer**: 129 products
  - **Air Wick**: 91 products
  - **Ambi Pur**: 42 products
- **Total Rejections**: 669 records (556 duplicates, 68 out-of-scope, 41 zero price, 4 invalid brand). Fully audited in `data/processed/products_rejected.csv`.

## 11. Database Architecture & Analytical Model
The local analytical storage uses **SQLite 3.25+** (`data/market_intelligence.db`), providing zero-dependency local deployment, ACID transactions, foreign key enforcement, window functions, and sub-millisecond query performance for the dashboard layer.

### Relational Schema (3NF Star/Snowflake Design):
- **`brands`**: `brand_id` (PK), `brand_name` (UNIQUE)
- **`categories`**: `category_id` (PK), `category_name` (UNIQUE), `product_format`
- **`data_sources`**: `source_id` (PK), `source_name`, `platform`, `source_type` (UNIQUE)
- **`products`**: `product_id` (PK), `canonical_id` (UNIQUE), `brand_id` (FK), `category_id` (FK), `source_id` (FK), `title_clean`, `title_raw`, `platform`, `product_url`, `selling_price`, `mrp`, `discount_pct`, `discount_source`, `rating`, `review_count`, `availability`, `pack_count`, `unit_quantity`, `unit`, `total_quantity`, `price_per_unit`, `price_per_100g`, `price_per_100ml`, `scraped_at`, `raw_reference`.

### Reusable Analytical Views & SQL:
- Views defined in `sql/schema.sql`: `vw_products_analytical`, `vw_market_overview`, `vw_brand_comparison`, `vw_category_coverage`.
- Parametric analytical queries in `sql/analytics_queries.sql` including exact median price calculation via window functions:
  ```sql
  WITH RankedPrices AS (
      SELECT selling_price,
             ROW_NUMBER() OVER (ORDER BY selling_price) AS row_num,
             COUNT(*) OVER () AS total_count
      FROM products WHERE selling_price IS NOT NULL
  )
  SELECT ROUND(AVG(selling_price), 2) AS market_median_price
  FROM RankedPrices
  WHERE row_num IN ((total_count + 1) / 2, (total_count + 2) / 2);
  ```

### Database Loading & Rebuild:
The database is deterministically generated from `data/processed/products_clean.csv`:
```bash
python main.py --stage database --rebuild
```

## 12. Dashboard Architecture
The web dashboard is built using modern **React**, **Vite**, and **Tailwind CSS**, featuring rich data visualizations:
- **Market Overview**: Key KPI metric cards, platform breakdown, and format distribution.
- **Brand Comparison**: Multi-metric benchmark cards, category coverage matrices, and review share.
- **Price Positioning**: Interactive scatter plots (Price vs. Rating), price-per-unit comparative distributions, and discount depth.
- **Product Explorer**: Searchable, filterable catalogue table with multi-attribute filtering (Brand, Category, Price Range, Rating, Availability).
- **Business Insights**: Dynamic, automated diagnostic panels assessing visible gaps and opportunities for any selected brand.

## 13. Portfolio Gap Methodology
The system identifies portfolio opportunities through an objective diagnostic matrix:
1. **Category Void**: Identifies fragrance categories where a brand has zero or negligible share of collected assortment despite active competitor presence.
2. **Price Tier Blank Spots**: Flags price bands unserved by the brand in the collected catalogue.
3. **Engagement Asymmetries**: Identifies categories with high competitor review engagement but low brand assortment coverage.
4. **Structured Decision Framing**: Every finding follows the strict sequence:
   $$\text{Observed Data} \longrightarrow \text{Interpretation} \longrightarrow \text{Business Question} \longrightarrow \text{Investigation Area} \longrightarrow \text{Validation Required}$$

## 14. Limitations
- **Catalogue Scope**: Metrics represent the collected catalogue sample at the time of scraping, not total historical or offline sales volume.
- **No Private Commercial Metrics**: Sales velocity, gross revenue, conversion rates, and profit margins are not publicly available and are strictly excluded from all models.
- **Platform Bias**: Marketplace visibility algorithms may impact the ranking and assortment surfacing order.
- **Catalogue Terminology**: Metric "Share of Collected Assortment" must not be conflated with commercial "Market Share".

## 15. Setup
### Prerequisites
- Python 3.10+
- Node.js 18+ & npm

### Python Environment
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### Dashboard Setup
```bash
cd dashboard
npm install
cd ..
```

## 16. Reproducible Automation (Single-Command Pipeline)

The complete end-to-end data pipeline is automated and reproducible through a single command:

```bash
python main.py
```

### Complete Pipeline Flow:
```
python main.py
      ↓
[COLLECT]    Public Ingestion: AromaPure Official JSON & Amazon Search HTML (1,436 raw observations)
      ↓
[CLEAN]      Deduplication, Scope Filtering (car-only excluded), Price Validation (767 valid products)
      ↓
[TRANSFORM]  Factual & Deterministic Transformation: Type Enforcement & Standardized Dimensions (data/processed/products_transformed.csv)
      ↓
[DATABASE]   SQLite Relational 3NF Load & Indexing (data/market_intelligence.db)
      ↓
[VALIDATE]   Automated Quality Gate (>=100 dynamic count, 5 brands, price integrity, canonical uniqueness)
      ↓
[REPORT]     Execution Manifest (data/pipeline_runs/run_<timestamp>.json) & PIPELINE_RUN_REPORT.md
```

### Factual Transformation Methodology:
The transformation stage strictly enforces deterministic data typing and formats observable metrics:
- **Numerical Coercion**: Casts prices, discounts, ratings, reviews, and normalized quantities into valid numeric data types.
- **Null Safety**: Preserves unobserved or unavailable fields as `NULL` without imputation.
- **Zero Arbitrary Labels**: Refrains from fabricating speculative business classifications such as "Value", "Mass-Market", or "Premium" at the data layer. All positioning analysis on the dashboard is derived directly and transparently from continuous empirical distributions (mean, median, percentiles, price-per-unit, and price-vs-rating plots).

### Idempotency & Re-execution Guarantee:
Running `python main.py` repeatedly is completely safe. The database layer implements a deterministic rebuild pattern from the verified processed dataset, ensuring zero duplicated records and zero drift across runs.

### Modular CLI Sub-Commands for Debugging:
- **Run Full Pipeline**: `python main.py` or `python main.py --stage all`
- **Run Collection Only**: `python main.py --stage collect`
- **Run Cleaning Only**: `python main.py --stage clean`
- **Run Transformation Only**: `python main.py --stage transform`
- **Run Database Load / Rebuild**: `python main.py --stage database [--rebuild]`
- **Run Quality Gate Checks**: `python main.py --stage validate`
- **Help Documentation**: `python main.py --help`

## 17. Analytical API Layer (FastAPI Backend)

The FastAPI analytical service provides a high-performance REST delivery layer between the SQLite database (`data/market_intelligence.db`) and the upcoming React dashboard.

### Architecture:
```
SQLite (3NF Data Model) ──> FastAPI (Parametric SQL & Pydantic) ──> React / Vite Dashboard
```

### Running the API:
```bash
python -m uvicorn api.main:app --reload --port 8000
```
- Interactive OpenAPI / Swagger Documentation: `http://localhost:8000/docs`
- Raw OpenAPI JSON Schema: `http://localhost:8000/openapi.json`

### CORS Configuration:
Pre-configured for local frontend development:
- `http://localhost:5173` (Vite dev server)
- `http://localhost:3000` (Alternative React port)

### Endpoint Catalog:

| Endpoint | Method | Response Description |
| :--- | :---: | :--- |
| `/api/health` | `GET` | Health check verifying API & SQLite connection status (`{"status":"ok","database":"connected"}`). |
| `/api/overview` | `GET` | Macro market KPIs: total products (767), average price (₹667.81), exact median price (₹448.00), ratings, and distribution shares by brand, platform, and category. |
| `/api/brands` | `GET` | Master list of tracked brands with observed catalogue product counts. |
| `/api/brands/comparison` | `GET` | Side-by-side benchmark matrix across all 5 brands (average price, exact median, average rating, reviews, discount %, category coverage). |
| `/api/brands/{brand_name}` | `GET` | Deep-dive brand diagnostics: price statistics, category breakdown, platform share, discount depth, and quantity metrics. (Returns 404 for unknown brand). |
| `/api/products` | `GET` | Paginated product catalogue supporting multi-attribute filtering (`brand`, `platform`, `category`, `product_format`, `availability`, `min_price`, `max_price`, `min_rating`, `max_rating`, `min_quantity`, `max_quantity`, `page`, `page_size`). |
| `/api/products/{product_id}` | `GET` | Complete factual record for an individual product. (Returns 404 if not found). |
| `/api/analytics/price-positioning` | `GET` | Empirical data points for Price vs. Rating scatter analysis. Preserves factual ratings without imputation. |
| `/api/analytics/price-normalization` | `GET` | Segregated unit pricing benchmarks: `price_per_unit` (767 products), `price_per_100g` (30 products), `price_per_100ml` (271 products). Never combines mass and volume. |
| `/api/analytics/categories` | `GET` | Category-level breakdown: product count, brand participation, average selling price, average rating, and average discount. |
| `/api/analytics/platforms` | `GET` | Channel breakdown comparing Amazon India and AromaPure Official Catalogue. |
| `/api/analytics/discounts` | `GET` | Verified discount records where `discount_pct` is non-null. Missing discounts are excluded and never treated as 0%. |
| `/api/analytics/category-coverage` | `GET` | Brand $\times$ Category coverage matrix. Note: Zero indicates "No observed product in collected dataset", not absence of commercial offering. |
| `/api/filters` | `GET` | Dynamic distinct values for brands, categories, formats, platforms, availability, and min/max ranges to populate frontend filter components. |

### Data Quality & Null Handling:
- **No Zero Imputation**: Missing ratings, reviews, or discounts are strictly emitted as JSON `null` (never converted to 0 or 0.0).
- **Parameterized SQL**: All database queries use parameterized SQL bindings to guarantee security and zero query injection.
- **Index-Accelerated**: Leverages existing B-tree indexes on `brand_id`, `category_id`, `selling_price`, and `platform`.

## 18. React Business Intelligence Dashboard

The frontend is a modern, responsive Business Intelligence dashboard built with **React**, **Vite**, **Tailwind CSS**, and **Recharts**. It communicates exclusively with the FastAPI analytical backend over REST endpoints and presents zero speculative rankings or arbitrary business tier labels.

### Dashboard Architecture & Location
```
dashboard/
├── package.json
├── vite.config.js
├── tailwind.config.js
├── index.html
└── src/
    ├── main.jsx
    ├── App.jsx
    ├── api/
    │   └── client.js             # Centralized API client with VITE_API_BASE_URL
    ├── components/
    │   ├── Header.jsx            # System health indicator & collection metadata
    │   ├── Sidebar.jsx           # Responsive desktop/tablet/mobile navigation
    │   ├── KpiCard.jsx           # KPI presentation with methodology definitions
    │   ├── ChartCard.jsx         # Uniform chart container with explanations
    │   ├── FilterBar.jsx         # Multi-field dynamic filter bar
    │   ├── DataTable.jsx         # Paginated catalogue table with detail drawer
    │   └── EmptyState.jsx        # Loading, error, and empty-state handlers
    ├── pages/
    │   ├── Overview.jsx          # Macro market KPIs, brand/category/platform charts
    │   ├── BrandComparison.jsx   # Symmetric side-by-side brand benchmark matrices
    │   ├── PricePositioning.jsx  # Price vs. Rating scatter & segregated unit economics
    │   ├── ProductAnalysis.jsx   # 767-product interactive filtering & pagination
    │   └── BusinessInsights.jsx  # 4-part diagnostic framework & coverage matrix
    └── styles/
        └── index.css             # Tailwind design tokens & typography
```

### Installation & Execution
```bash
# 1. Navigate to the dashboard directory
cd dashboard

# 2. Install dependencies
npm install

# 3. Start local development server
npm run dev
# The application opens at http://localhost:5173

# 4. Production build & verification
npm run build
```

### Environment Configuration
Configure backend endpoint connectivity via `.env` in `dashboard/`:
```env
VITE_API_BASE_URL=http://localhost:8000
```
If omitted, defaults automatically to `http://localhost:8000`.

### Dashboard Pages & Visualizations
1. **Market Overview (`/overview`)**:
   - 6 KPI cards: Total Observed Products (767), Tracked Brands (5), Catalogue Average Price (₹667.81), Exact Median Price (₹448.00), Catalogue Average Rating (4.15★), and Average Observed Discount (39.5%).
   - Charts: Assortment by Brand (Bar), Assortment by Category (Horizontal Bar), Assortment by Platform (Donut), and Observed Price Distribution (Bar).
2. **Brand Comparison (`/brands`)**:
   - Symmetric comparison table with brand focus selector (AromaPure, Odonil, Godrej aer, Air Wick, Ambi Pur).
   - Side-by-side charts: Average vs. Median Price, Observed Rating Benchmark, Assortment Count, and Category Coverage count.
3. **Price Positioning (`/price-positioning`)**:
   - Interactive Price vs. Rating Scatter Plot (unrated products excluded to prevent 0-star distortions).
   - Segregated Unit Economics comparison (strictly separating ₹/100ml and ₹/100g).
   - Promotional discount distribution across brands.
   - **Product Clusters (K-Means)**: Transparent mathematical grouping of products with complete numerical features (`selling_price`, `rating`, `discount_pct`, $\log(1 + \text{reviews})$). Evaluates $K=2..5$ and selects optimal $K$ via silhouette score. Labeled neutrally as *Cluster 1*, *Cluster 2*, etc., without subjective tiering labels.

4. **Product Analysis (`/products`)**:
   - Dynamic multi-attribute filtering (Brand, Category, Platform, Product Type / Format, Pack Size / Count, Availability, Price range, Rating threshold, Keyword search).
   - Paginated product table (20 / 50 / 100 rows per page) with detail modal/drawer displaying verified attributes and public source link.
5. **Business Insights (`/insights`)**:
   - 4-part diagnostic framework for each finding: **Observation** (dataset fact) → **Interpretation** (analytical hypothesis) → **Commercial Question** (strategic decision) → **Validation Required** (internal data needed).
   - Observed Category Presence Matrix identifying portfolio coverage and voids.


## 19. Business Insights Approach

The dashboard translates factual catalogue observations into commercial decision-support using a strict, reproducible diagnostic structure.

### 1. Observation vs. Interpretation Discipline
- **Factual Observation**: Strictly measurable empirical data points extracted directly from the verified database (e.g. *"430 of 767 products belong to Ambient Fragrance"*).
- **Analytical Interpretation**: Explicitly separated hypotheses explaining the observation without claiming causality (e.g. *"The collected catalogue exhibits concentration in general room ambience"*).
- **Commercial Business Question**: Formulated as strategic queries for brand leaders (e.g. *"Would assortment expansion into automated sprays be commercially viable?"*).
- **Internal Validation Required**: Identifies mandatory proprietary internal datasets (POS sell-through, gross margin curves, COGS, customer churn) required before committing capital.

### 2. Analytical Boundaries & Symmetrical Rules
- **Catalogue Assortment vs. Market Share**: Percentage counts indicate *Share of Collected Assortment*, NEVER commercial market share or dollar sales.
- **Review Share vs. Market Share**: Review volume (1,387 total observed reviews across marketplace listings) reflects customer feedback visibility on e-commerce, not market share or sales velocity. AromaPure official catalogue listings do not expose public review counts and are preserved as `NULL` (*"Not available"*).
- **Category Coverage & Portfolio Voids**: A value of 0 in the category coverage matrix denotes *"No observed product in the collected public dataset"*. It does NOT imply that a brand does not commercially produce or distribute products in that category in uncollected offline channels.
- **Price Positioning Methodology**: Analyzed through continuous empirical distributions (mean, median, IQR, unit pricing). Arbitrary and subjective marketing labels (*"Value"*, *"Mass-Market"*, *"Premium"*, *"Budget"*) are strictly excluded.
- **Unit Economics Separation**: Standardized liquid formulations (₹/100ml across 271 products) and solid formulations (₹/100g across 30 products) are presented on strictly separate visual cards to prevent artificial density distortion.
- **Portfolio-Opportunity Framing**: The dashboard avoids prescriptive commands (*"Brand X should launch Y"*). Instead, observed coverage voids frame investigative hypotheses to be evaluated against internal capability and demand.

## 20. Testing
Run the automated test suite covering scrapers, cleaning rules, unit normalizers, and API endpoints:
```bash
pytest tests/ -v
```

## 21. AI Usage Disclosure
AI-assisted tools were used during development primarily for debugging, documentation assistance, and development support. All generated suggestions and code changes were reviewed, tested, and validated against the project requirements and automated test suite.

## 22. Future Improvements
- Scheduled recurring ingestion to track historical price elasticity and promotional discount cycles.
- Natural Language Processing (NLP) sentiment and fragrance profile extraction from customer review texts.
- Integration of regional quick-commerce stock availability feeds.

