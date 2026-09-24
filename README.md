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
1. **AromaPure** (Direct-to-consumer and marketplace catalogue: diffusers, room sprays, candles, flakes)
2. **Odonil** (Established air care brand prominent in air freshening blocks, gels, and room sprays)
3. **Godrej aer** (Prominent air care brand in bathroom fresheners, aerosol sprays, and automatic diffusers)
4. **Air Wick** (Global FMCG brand specialized in automatic sprays, plug-in diffusers, and refills)
5. **Ambi Pur** (Global P&G brand in air sprays, bathroom fresheners, and plug-in devices)

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

## 7. Current Folder Structure
```
.
├── main.py                          # CLI orchestrator & single-command pipeline runner
├── requirements.txt                 # Python dependencies
├── README.md                        # Technical documentation & project specification
├── PIPELINE_RUN_REPORT.md           # Latest pipeline execution run report
├── .gitignore                       # Git ignore rules for caches, builds, and local envs
├── config/
│   └── config.yaml                  # Pipeline scraping parameters, rate limits, and brands
├── api/
│   ├── main.py                      # FastAPI application entry point & CORS configuration
│   ├── database.py                  # SQLite connection lifecycle & dependency injection
│   ├── schemas.py                   # Pydantic data models & response contracts
│   └── routes/
│       ├── overview.py              # Macro market KPIs & categorical distributions
│       ├── brands.py                # Symmetric brand comparison & brand deep-dive endpoints
│       ├── products.py              # Paginated, filterable product catalogue endpoint
│       └── analytics.py             # Price positioning, unit economics, clusters & matrix
├── dashboard/
│   ├── package.json                 # Dashboard npm dependencies
│   ├── vite.config.js               # Vite build configuration
│   ├── tailwind.config.js           # Tailwind CSS configuration
│   ├── index.html                   # HTML entry point
│   └── src/
│       ├── main.jsx                 # React root mount
│       ├── App.jsx                  # Main layout & client-side tab router
│       ├── api/client.js            # Frontend REST client with VITE_API_BASE_URL
│       ├── components/              # Reusable UI components (Header, Sidebar, KpiCard, FilterBar, DataTable, ChartCard)
│       ├── pages/
│       │   ├── Overview.jsx         # Market Overview page (120-product deterministic sample)
│       │   ├── BrandComparison.jsx  # Symmetric Brand Comparison benchmark (Full dataset)
│       │   ├── PricePositioning.jsx # Price vs. Rating scatter, unit pricing, clusters (Full dataset)
│       │   ├── ProductAnalysis.jsx  # Paginated product table with filtering (120-product sample)
│       │   └── BusinessInsights.jsx # 8-part diagnostic framework & whitespace matrix (Full dataset)
│       ├── styles/index.css         # Styling rules & design tokens
│       └── utils/dashboardSample.js  # Deterministic 120-product sample generator (24/brand)
├── data/
│   ├── market_intelligence.db       # Primary SQLite 3NF relational database
│   ├── pipeline_runs/               # Automated pipeline run manifests (JSON)
│   ├── processed/                   # Cleaned, rejected, and transformed CSV datasets
│   └── raw/                         # Immutable raw collection artifacts (JSON, HTML) & manifests
├── docs/                            # Comprehensive requirement coverage & audit documentation
├── extra/                           # Auxiliary development QA reports & exploratory scripts
├── sql/
│   ├── schema.sql                   # 3NF SQLite schema, indexes, and analytical views
│   └── analytics_queries.sql        # Reference SQL queries for aggregations & medians
├── src/
│   ├── scrapers/                    # Source-specific ingestion modules
│   ├── cleaning/                    # Deduplication, scope filtering & unit extraction
│   ├── transformation/              # Data type casting & analytical transformation
│   ├── database/                    # SQLite relational database loader & validator
│   ├── pipeline/                    # Orchestrator & automated data quality gatekeeper
│   └── utils/                       # Logging, manifests, and file helpers
└── tests/                           # Comprehensive test suite (47 automated pytest tests)
```

## 8. Actual Data Schema

### Relational Schema (SQLite 3NF Star/Snowflake Design):
1. **`brands`**: `brand_id` (PK), `brand_name` (UNIQUE)
2. **`categories`**: `category_id` (PK), `category_name` (UNIQUE), `product_format`
3. **`data_sources`**: `source_id` (PK), `source_name`, `platform`, `source_type` (UNIQUE `source_name, platform`)
4. **`products`**:
   - `product_id` (PK): Integer autoincrement primary key
   - `canonical_id` (UNIQUE): Canonical product identity (Amazon ASIN or AromaPure product/variant hash)
   - `brand_id` (FK): Reference to `brands.brand_id`
   - `category_id` (FK): Reference to `categories.category_id`
   - `source_id` (FK): Reference to `data_sources.source_id`
   - `title_clean`: Normalized, readable product title
   - `title_raw`: Original unedited listing title
   - `platform`: Source channel (`Amazon India` or `AromaPure Official`)
   - `product_url`: Public web link to product listing
   - `selling_price`: Observed retail price in INR (non-null positive float)
   - `mrp`: Maximum Retail Price / List Price in INR (float, where available)
   - `discount_pct`: Observed discount percentage `((mrp - selling_price) / mrp) * 100`
   - `discount_source`: Provenance tag (`computed_from_mrp`, `unavailable`)
   - `rating`: Customer star rating from 1.0 to 5.0 (NULL for unrated items)
   - `review_count`: Total consumer reviews (NULL when unstated)
   - `rating_source` / `review_source`: Extraction provenance
   - `seller`: Marketplace seller name (preserved as NULL when unobserved on search cards)
   - `availability`: Stock availability (`In Stock`, `Out of Stock`)
   - `pack_count`: Number of units in pack (default 1)
   - `unit_quantity`: Physical quantity per unit
   - `unit`: Measurement unit (`ml`, `g`, `count`)
   - `total_quantity`: Total normalized quantity (`pack_count * unit_quantity`)
   - `price_per_unit`: Standardized price per unit item (`selling_price / pack_count`)
   - `price_per_100g`: Price normalized per 100 grams for solid formats
   - `price_per_100ml`: Price normalized per 100 milliliters for liquid formats
   - `scraped_at`: ISO 8601 UTC timestamp of data collection
   - `raw_reference`: Path to raw immutable archive file

### Reusable Analytical Views:
- **`vw_products_analytical`**: Complete pre-joined analytical view combining products, brands, categories, and sources.
- **`vw_market_overview`**: Macro market aggregate metrics.
- **`vw_brand_comparison`**: Symmetrical brand-level benchmarking view.
- **`vw_category_coverage`**: Category-by-brand coverage cross-tabulation.

## 9. Required Product-Field Coverage Audit

Every field explicitly required by the assignment is tracked with full audit provenance:

| Assignment Field | Dataset Column | Populated Records | Completeness (%) | Implementation & Null-Policy Status |
| :--- | :--- | :---: | :---: | :--- |
| **Brand** | `brand` | 684 / 684 | 100.0% | **Populated**: Mandatory dimension across all 5 brands. |
| **Product Name** | `title_clean`, `title_raw` | 684 / 684 | 100.0% | **Populated**: Normalized clean title and immutable raw title. |
| **Category / Subcategory** | `category`, `product_format` | 684 / 684 | 100.0% | **Populated**: 7 standardized categories; specific format tracked. |
| **Platform** | `platform` | 684 / 684 | 100.0% | **Populated**: Amazon India (386) and AromaPure Official (298). |
| **URL / ID** | `product_url`, `canonical_id` | 684 / 684 | 100.0% | **Populated**: ASIN or product-variant hash; direct source URL. |
| **Selling Price** | `selling_price` | 684 / 684 | 100.0% | **Populated**: Non-zero positive INR numeric price required. |
| **MRP** | `mrp` | 672 / 684 | 98.2% | **Partially Populated**: Preserved as NULL when unlisted. |
| **Discount** | `discount_pct` | 479 / 684 | 70.0% | **Partially Populated**: Computed when MRP is available; NULL preserved (never 0%). |
| **Pack / Unit Size** | `pack_count`, `unit_quantity` | 684 / 684 | 100.0% | **Populated**: Pack count extracted (599 singles, 85 multipacks). |
| **Total Quantity** | `total_quantity`, `unit` | 274 / 684 | 40.1% | **Partially Populated**: Calculated when mass ($g$) or volume ($ml$) is stated. |
| **Rating** | `rating` | 340 / 684 | 49.7% | **Partially Populated**: Public marketplace ratings; NULL preserved on unrated. |
| **Review Count** | `review_count` | 491 / 684 | 71.8% | **Partially Populated**: Observed marketplace reviews and public storefront reviews. |
| **Availability** | `availability` | 684 / 684 | 100.0% | **Populated**: Stock availability status. |
| **Fragrance / Product Type** | `product_format` | 684 / 684 | 100.0% | **Populated**: Standardized form factor (Candle, Spray, Diffuser, etc.). |
| **Seller, if available** | `seller` | 0 / 684 | 0.0% | **Unavailable for some sources**: Public Amazon search cards omit merchant IDs; preserved as legitimate NULL rather than fabricating values. |
| **Scraped Date** | `scraped_at` | 684 / 684 | 100.0% | **Populated**: ISO 8601 UTC timestamp on all records. |

## 10. Cleaning and Validation Rules
The data cleaning stage implements rigorous, deterministic verification:
- **Canonical Product Identity**:
  - Amazon listings: Unique marketplace **ASIN**. Multiple query occurrences are deduplicated to 1 canonical record.
  - AromaPure catalogue: Composite key **Product ID + Variant ID** (or SKU), preserving legitimate fragrance/size variations.
- **Home Fragrance Boundary & Car-Product Exclusion**:
  - Strictly filters out automotive-only products ("car perfume", "car vent", "vent clip", "car hanging", "hanging card", "car spray", "car dashboard perfume", "auto fragrance").
  - In the latest cleaning run, **135 car-only records** were identified and rejected into `data/processed/products_rejected.csv`.
- **Price Sanity & Non-Zero Enforcement**:
  - Requires positive numeric selling prices in INR; eliminated 20 zero-price promotional or gift-card entries.
- **Brand Validation**:
  - Verified that listing belongs strictly to the 5 selected brands; rejected 4 non-target brand search bleed items.
- **Missing Value Preservation**:
  - Missing ratings, discounts, or reviews remain strictly `NULL`. Never imputed as 0 or 0.0.

## 11. Price and Unit Normalization
To enable meaningful comparisons across disparate product formats:
- Quantities are parsed into standardized metrics: grams ($g$) for solids/gels/candles, milliliters ($ml$) for liquids/sprays/oils, and units ($count$) for multi-packs.
- Normalized price metrics:
  - $\text{Price per Unit} = \frac{\text{Selling Price}}{\text{Pack Count}}$ (100% coverage, 684 products, Mean: ₹614.93, Median: ₹434.00)
  - $\text{Price per 100ml} = \frac{\text{Selling Price}}{\text{Total ml}} \times 100$ (33.8% coverage, 231 liquid products, Mean: ₹1,203.48, Median: ₹665.00)
  - $\text{Price per 100g} = \frac{\text{Selling Price}}{\text{Total grams}} \times 100$ (3.4% coverage, 23 solid products, Mean: ₹369.28, Median: ₹330.00)
- **Integrity Rule**: Mass and volume metrics are strictly separated. No arbitrary density conversions ($1g \neq 1ml$) are applied.

## 12. Current Dataset Statistics (After Car-Product Exclusion)

> [!IMPORTANT]
> The full dataset has been cleaned to exclude car-freshener / car-only products. The previous count of 767 products is superseded by the current authoritative count of **684 validated products**.

### Full Validated Dataset vs. Dashboard Analytical Sample

| Dimension | Full Validated Dataset | Dashboard Analytical Sample |
| :--- | :---: | :---: |
| **Total Products** | **684** | **120** |
| **Products per Brand** | Dynamic (31 to 298) | **Exactly 24 per brand** |
| **Car-Only Products Included** | **0** (strictly excluded) | **0** (strictly excluded) |
| **Primary Usage** | Relational DB, API Analytics, Benchmark Matrix, Clusters | Dashboard exploratory presentation & balanced sampling |

### Brand Assortment Breakdown (Full Dataset):

| Brand Name | Validated Products | Share of Assortment (%) | Minimum Target (>=20) Met? |
| :--- | :---: | :---: | :---: |
| **AromaPure** | 298 | 43.57% | **YES** |
| **Odonil** | 132 | 19.30% | **YES** |
| **Godrej aer** | 132 | 19.30% | **YES** |
| **Air Wick** | 91 | 13.30% | **YES** |
| **Ambi Pur** | 31 | 4.53% | **YES** |
| **Total** | **684** | **100.00%** | **YES (6.8x above 100-product floor)** |

### Platform Breakdown:
- **Amazon India**: 386 products (56.43%)
- **AromaPure Official**: 298 products (43.57%)

### Category Breakdown:
1. **Ambient Fragrance (General)**: 383 products (55.99%)
2. **Scented Candle & Wax**: 153 products (22.37%)
3. **Reed Diffuser & Fragrance Oil**: 80 products (11.70%)
4. **Room Spray & Aerosol**: 40 products (5.85%)
5. **Automatic Spray & Refill**: 15 products (2.19%)
6. **Bathroom Freshener & Block**: 10 products (1.46%)
7. **Freshener Gel & Pocket**: 3 products (0.44%)

### Market Pricing & Engagement Metrics:
- **Average Selling Price**: **₹663.42**
- **Median Selling Price**: **₹434.00** (Exact 50th percentile)
- **Price Range**: ₹51.00 to ₹6,345.00
- **Price Distribution**:
  - Under ₹250: 160 products (23.39%)
  - ₹250–₹499: 264 products (38.60%)
  - *Combined Sub-₹500*: **424 products (61.99%)**
  - ₹500–₹999: 170 products (24.85%)
  - ₹1,000+: 90 products (13.16%)
- **Rated Products Count**: 340 products (49.71%)
- **Average Customer Rating**: **4.16 ★** (Median: 4.20 ★, Range: 1.0 ★ – 5.0 ★)
- **Total Observed Reviews**: **9,261 reviews** across 491 products with review data
- **Observed Discounts**: 479 products with MRP (Average discount: 39.33%; 431 products with discount >0%, average 43.70%)
- **Total Rejections**: 328 records (169 duplicates, 135 car-only out-of-scope, 20 zero/invalid price, 4 invalid brand), fully audited in `data/processed/products_rejected.csv`.

### Symmetrical Brand Benchmark Matrix:

| Metric | AromaPure | Odonil | Godrej aer | Air Wick | Ambi Pur | Overall Market |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Product Count** | 298 | 132 | 132 | 91 | 31 | **684** |
| **Assortment Share** | 43.57% | 19.30% | 19.30% | 13.30% | 4.53% | **100.00%** |
| **Mean Price (₹)** | ₹633.21 | ₹292.49 | ₹397.72 | ₹1,730.95 | ₹530.97 | **₹663.42** |
| **Median Price (₹)** | ₹485.00 | ₹237.00 | ₹372.50 | ₹905.00 | ₹539.00 | **₹434.00** |
| **Min Price (₹)** | ₹99.00 | ₹51.00 | ₹51.00 | ₹156.00 | ₹229.00 | **₹51.00** |
| **Max Price (₹)** | ₹4,899.00 | ₹5,499.00 | ₹1,590.00 | ₹6,345.00 | ₹999.00 | **₹6,345.00** |
| **Rated Products** | 0 (0.0%) | 112 (84.8%) | 117 (88.6%) | 86 (94.5%) | 25 (80.6%) | **340 (49.7%)** |
| **Mean Rating (★)** | *N/A (NULL)* | 4.11 ★ | 4.13 ★ | 4.29 ★ | 4.08 ★ | **4.16 ★** |
| **Median Rating (★)**| *N/A (NULL)* | 4.20 ★ | 4.20 ★ | 4.30 ★ | 4.20 ★ | **4.20 ★** |
| **Total Reviews** | 7,958 | 427 | 449 | 332 | 95 | **9,261** |
| **Discount Count (>0%)**| 289 (97.0%) | 46 (34.8%) | 62 (47.0%) | 25 (27.5%) | 9 (29.0%) | **431 (63.0%)** |
| **Mean Discount (>0%)**| 45.21% | 52.56% | 35.51% | 41.56% | 12.61% | **43.70%** |
| **Total MRP Observed** | 289 | 131 | 131 | 90 | 31 | **479** |
| **Categories Spanned** | 6 | 3 | 3 | 3 | 5 | **7** |

### Category Coverage Matrix:

| Category | Air Wick | Ambi Pur | AromaPure | Godrej aer | Odonil | Total |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Ambient Fragrance (General)** | 82 | 11 | 42 | 121 | 127 | **383** |
| **Scented Candle & Wax** | 0 | 0 | 153 | 0 | 0 | **153** |
| **Reed Diffuser & Fragrance Oil** | 0 | 2 | 78 | 0 | 0 | **80** |
| **Room Spray & Aerosol** | 1 | 11 | 18 | 6 | 4 | **40** |
| **Automatic Spray & Refill** | 8 | 4 | 3 | 0 | 0 | **15** |
| **Bathroom Freshener & Block** | 0 | 0 | 4 | 5 | 1 | **10** |
| **Freshener Gel & Pocket** | 0 | 3 | 0 | 0 | 0 | **3** |
| **Total Products** | **91** | **31** | **298** | **132** | **132** | **684** |

*Note: Zero indicates absence of observed product in the collected public dataset, not proof of non-existence in offline commercial channels.*

## 13. Scrape & Run Provenance (No `scrape_runs` Table)
- The database does **NOT** contain a separate `scrape_runs` table.
- Instead, run tracking, source provenance, and collection integrity are handled systematically through:
  1. The **`data_sources`** dimension table in SQLite (tracking `source_name`, `platform`, `source_type`).
  2. The **`scraped_at`** and **`raw_reference`** columns on every product record.
  3. **Collection Manifests** saved immutably in `data/raw/manifests/collection_<run_id>.json`.
  4. **Pipeline Run Manifests** saved in `data/pipeline_runs/run_<run_id>.json`.
  5. The executive **`PIPELINE_RUN_REPORT.md`** generated upon each pipeline execution.

## 14. Configuration Management
- **`config/config.yaml`**: The primary active configuration file specifying:
  - Selected competitor brands and source URLs/search queries.
  - Request settings: timeout (15s), polite sequential delay range (2.5s–4.0s), retry count (3), backoff factor (2.0), user agent string, and page limits per query (2 pages).
  - Storage paths for raw data archives.
- **Dashboard Configuration**: The React dashboard uses `VITE_API_BASE_URL` (configurable via `dashboard/.env`), defaulting to `http://localhost:8000` if omitted.

## 15. Automation & Scheduling
- **Current Status**: No automated cron jobs, GitHub Actions workflows, Airflow, or Prefect schedulers are currently configured in the repository.
- Pipeline execution is currently triggered deterministically on demand via the CLI (`python main.py`).
- Scheduled recurring ingestion is documented as an architectural extension under **Future Improvements**.

## 16. Analytical API Layer (FastAPI Backend)
The FastAPI analytical service provides a high-performance REST delivery layer between SQLite and the dashboard:

```bash
python -m uvicorn api.main:app --reload --port 8000
```
- Interactive OpenAPI / Swagger UI: `http://localhost:8000/docs`

### Actual Endpoints:

| Endpoint | Method | Response Description |
| :--- | :---: | :--- |
| `/api/health` | `GET` | Health check verifying API & SQLite connection status (`{"status":"ok","database":"connected"}`). |
| `/api/overview` | `GET` | Macro market KPIs (total 684 products, average price ₹663.42, exact median price ₹434.00, ratings, discounts, distributions). |
| `/api/brands` | `GET` | Master list of 5 tracked brands with product counts. |
| `/api/brands/comparison` | `GET` | Symmetrical benchmark matrix across all 5 brands (prices, ratings, reviews, discounts, category coverage). |
| `/api/brands/{brand_name}` | `GET` | Deep-dive brand diagnostics (returns 404 for unknown brand). |
| `/api/products` | `GET` | Paginated product catalogue with multi-attribute filtering (`brand`, `platform`, `category`, `product_format`, `availability`, `min_price`, `max_price`, `min_rating`, `max_rating`, `min_quantity`, `max_quantity`, `pack_count`, `search`, `page`, `page_size`). |
| `/api/products/{product_id}` | `GET` | Complete factual record for an individual product (returns 404 if not found). |
| `/api/analytics/price-positioning` | `GET` | Scatter data points (Price vs. Rating) across all 684 products. |
| `/api/analytics/price-normalization` | `GET` | Unit pricing benchmarks: `price_per_unit` (684 products), `price_per_100g` (23 products), `price_per_100ml` (231 products). Strictly segregated. |
| `/api/analytics/categories` | `GET` | Category breakdown: count, brand participation, average price, rating, discount. |
| `/api/analytics/platforms` | `GET` | Channel breakdown (Amazon India vs. AromaPure Official). |
| `/api/analytics/discounts` | `GET` | Verified discount records (479 products). Excludes missing discounts. |
| `/api/analytics/category-coverage` | `GET` | Brand $\times$ Category coverage matrix. |
| `/api/analytics/product-clusters` | `GET` | K-Means clustering ($K=2..5$, optimal $K=4$, silhouette score 0.47) across complete records. |
| `/api/filters` | `GET` | Dynamic distinct filter values and min/max ranges for frontend components. |

## 17. React BI Dashboard Architecture & Actual Pages

The dashboard is built with **React 18**, **Vite**, **Tailwind CSS**, and **Recharts**.

### 120-Product Deterministic Analytical Sample
To ensure fair visual comparisons and balanced representation without distortion by catalogue asymmetries:
- The dashboard utilizes a balanced, deterministic sample of **120 products** (**exactly 24 products per brand across 5 brands**).
- The full dataset of **684 validated products** remains active in the database and powers all macro-benchmark endpoints, scatter plots, clustering models, and API queries.
- Zero car-only products appear in the sample or full dataset.

### Dashboard Pages:
1. **Market Overview (`/overview`)**:
   - 6 KPI cards: Total Observed Products (120 sample / 684 full dataset indicator), Tracked Brands (5), Average Price, Median Price, Rating, and Average Discount.
   - Breakdown charts: Assortment by Brand, Assortment by Category, Assortment by Platform, and Observed Price Distribution.
2. **Brand Comparison (`/brands`)**:
   - Side-by-side benchmark matrix and focus brand selector across all 5 competitor brands.
   - Comparative charts: Average vs. Median Price, Observed Rating Benchmark, Assortment Count, and Category Coverage count.
3. **Price Positioning (`/price-positioning`)**:
   - Price vs. Rating Scatter Plot (unrated items excluded from scatter to prevent 0-star distortions).
   - Segregated Unit Economics cards (₹/100ml for liquids and ₹/100g for solids).
   - Promotional discount distribution across brands.
   - Unsupervised K-Means Product Clustering ($K=4$, neutrally labeled Cluster 1–4).
4. **Product Analysis (`/products`)**:
   - Dynamic multi-attribute filtering (Brand, Category, Platform, Product Type / Format, Pack Size / Count, Availability, Price range, Rating threshold, Keyword search).
   - Paginated table (20 / 50 / 100 rows per page) with detail modal/drawer displaying verified attributes and public source link.
5. **Business Insights (`/insights`)**:
   - 8-part diagnostic framework: **Observation** (dataset fact) → **Interpretation** (analytical hypothesis) → **Commercial Question** (strategic query) → **Validation Required** (internal data needed).
   - Observed Category Presence Matrix identifying portfolio coverage and voids.

## 18. Business-Insight Methodology
The platform translates catalogue observations into commercial decision-support using a strict diagnostic structure:
- **Observation vs. Interpretation Discipline**: Measurable dataset facts are strictly distinguished from analytical hypotheses.
- **Assortment Share vs. Market Share**: Percentage counts indicate *Share of Collected Assortment*, NEVER commercial market share or revenue.
- **Review Count Interpretation**: Review volume reflects customer feedback visibility on public e-commerce channels, not sales velocity.
- **Category Whitespace**: A zero count in category coverage denotes absence of observation in the collected public dataset, not absence of commercial manufacturing in offline channels.
- **Continuous Distributions**: Positioning is analyzed via continuous statistical metrics (mean, median, IQR, percentiles), strictly avoiding subjective labels ("Value", "Premium", "Mass-Market").

## 19. Limitations
- **Catalogue Scope**: Metrics represent the collected catalogue sample at the time of scraping, not total historical or offline sales volume.
- **No Private Commercial Metrics**: Sales velocity, gross revenue, conversion rates, and profit margins are not publicly available and are strictly excluded from all models.
- **Platform Visibility**: Marketplace search order reflects platform algorithms at ingestion time.
- **Seller Visibility**: Third-party merchant names are omitted from search result cards and preserved as legitimate NULLs.

## 20. Setup Instructions
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

## 21. Exact Pipeline Execution Commands
The complete end-to-end data pipeline is automated and reproducible through a single command:

```bash
# Execute complete pipeline (Collect -> Clean -> Transform -> Database -> Validate)
python main.py

# Or execute individual stages:
python main.py --stage collect      # Run collection only
python main.py --stage clean        # Run cleaning and scope validation
python main.py --stage transform    # Run transformation
python main.py --stage database     # Load SQLite database (--rebuild to recreate from scratch)
python main.py --stage validate     # Run automated data-quality gate
```

## 22. Testing Instructions
Run the automated test suite covering scrapers, cleaning rules, unit normalizers, database integrity, and API endpoints:
```bash
python -m pytest tests/ -v
```

## 23. AI Usage Disclosure
AI-assisted tools were used during development primarily for debugging, documentation assistance, and code structuring. All generated suggestions and code changes were reviewed, tested, and validated against the project requirements and automated test suite.

## 24. Future Improvements
- Scheduled recurring ingestion via cron/workflow schedulers to track historical price elasticity and promotional discount cycles.
- Natural Language Processing (NLP) sentiment and fragrance profile extraction from customer review texts.
- Integration of regional quick-commerce stock availability feeds.
