# Dashboard QA & Numerical Consistency Audit Report

**Audit Date**: September 24, 2026  
**Auditor**: Automated Verification & Integrity Subsystem  
**Scope**: React Frontend (`dashboard/`), FastAPI Analytical Backend (`api/`), SQLite Database (`data/market_intelligence.db`), and Transformation Pipeline  
**Dataset Under Audit**: 767 Validated Unique Products across 5 Tracked Competitor Brands  

---

## 1. Executive Summary

This rigorous Quality Assurance (QA) audit verifies numerical consistency, data provenance, analytical objectivity, and architectural compliance across the entire analytical stack:

$$\text{SQLite (767 Rows)} \longleftrightarrow \text{FastAPI REST Endpoints} \longleftrightarrow \text{React BI Dashboard}$$

All 5 core dashboard views (**Market Overview**, **Brand Comparison**, **Price Positioning**, **Product Analysis**, and **Business Insights**) were audited against the raw database queries, schema definitions, and visual components.

---

## 2. Authoritative Dataset & Median Reconciliation (Task 3)

### Deterministic Database Median Verification
A total of **767 products** exist in `products` (odd count). When sorted by `selling_price` ascending:
- **Total records**: 767
- **Exact Median index**: $(767 + 1) / 2 = 384\text{th}$ item (0-indexed row 383)
- **Surrounding prices**: `[443.0, 443.0, 448.0, 449.0, 449.0]`
- **Authoritative Median**: **₹448.00**

```sql
WITH RankedPrices AS (
    SELECT selling_price,
           ROW_NUMBER() OVER (ORDER BY selling_price) as row_num,
           COUNT(*) OVER () as total_count
    FROM products
    WHERE selling_price IS NOT NULL
)
SELECT ROUND(AVG(selling_price), 2) as median_price
FROM RankedPrices
WHERE row_num IN ((total_count + 1) / 2, (total_count + 2) / 2);
-- Result: 448.00
```

### Tri-Layer Reconciliation:
| Layer | Metric | Value | Verification Status |
| :--- | :--- | :--- | :--- |
| **SQLite Analytical DB** | `ROUND(AVG(selling_price), 2)` | **₹667.81** | Verified |
| **SQLite Analytical DB** | Exact Median `selling_price` | **₹448.00** | Verified (Row 384 of 767) |
| **FastAPI Backend** | `/api/overview` $\to$ `average_price` | **₹667.81** | Verified (Exact match) |
| **FastAPI Backend** | `/api/overview` $\to$ `median_price` | **₹448.00** | Verified (Exact match) |
| **React Dashboard** | `<KpiCard title="Average Price" />` | **₹667.81** | Verified |
| **React Dashboard** | `<KpiCard title="Median Price" />` | **₹448.00** | Verified |

*Note on previous reports*: An early draft report mentioned ₹419.00 based on an unweighted subcategory median. The authoritative catalogue-wide median across all 767 unique analytical products is **₹448.00**, and all layers now report this exact figure.

---

## 3. Brand Metrics & Symmetric Evaluation (Task 4 & 5)

All 5 competitor brands were evaluated symmetrically without creating artificial rankings, tiers, or leader/loser designations. Missing ratings, reviews, and discounts are excluded from denominators rather than imputed as zero.

| Brand | Product Count | Share of Assortment | Avg Price (₹) | Median Price (₹) | Avg Rating (Stars) | Rated Count | Total Reviews | Avg Discount (%) | Discounted Count | Categories | Platforms |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **AromaPure** | 360 | 46.94% | ₹665.21 | ₹499.00 | *Not available* | 0 | *Not available* | 43.8% | 348 | 7 | 1 |
| **Odonil** | 145 | 18.90% | ₹306.22 | ₹239.00 | 4.11 ★ | 124 | 473 | 34.4% | 75 | 5 | 1 |
| **Godrej aer** | 129 | 16.82% | ₹368.11 | ₹299.00 | 4.13 ★ | 118 | 453 | 33.6% | 60 | 3 | 1 |
| **Air Wick** | 91 | 11.86% | ₹1,766.13 | ₹905.00 | 4.30 ★ | 87 | 336 | 25.0% | 44 | 2 | 1 |
| **Ambi Pur** | 42 | 5.48% | ₹479.19 | ₹518.50 | 3.97 ★ | 35 | 125 | 31.9% | 18 | 5 | 1 |
| **Total / Market** | **767** | **100.0%** | **₹667.81** | **₹448.00** | **4.15 ★** | **364** | **1,387** | **39.5%** | **545** | **7** | **2** |

### Review Share vs. Market Share Discipline (Task 5)
- Total observed marketplace reviews: **1,387** (Odonil: 34.10%, Godrej aer: 32.66%, Air Wick: 24.22%, Ambi Pur: 9.01%).
- AromaPure direct-to-consumer store listings do not expose public star ratings or customer review counts.
- **Strict Distinction**: The dashboard renders review counts strictly as *"Observed Marketplace Reviews"* and clearly notes that AromaPure reviews are *"Not available"*. It never refers to review volume or assortment count as "market share" or "sales volume".

---

## 4. Page-by-Page Audit Findings

### Page 1 — Market Overview
- **KPIs**: All 6 cards verified against database queries. Total Products (767), Tracked Brands (5), Average Price (₹667.81), Median Price (₹448.00), Average Rating (4.15 ★ across 364 rated items), Average Discount (39.5% across 545 discounted items).
- **Charts**:
  1. *Assortment by Brand* (BarChart): 5 bars matching product counts exactly.
  2. *Assortment by Platform* (Donut): Amazon India (407 items, 53.06%) vs. AromaPure Official (360 items, 46.94%).
  3. *Products by Category* (Horizontal BarChart): 7 categories sorted by SKU count.
  4. *Observed Price Distribution* (BarChart): 5 brackets (Under ₹250: 181, ₹250–₹499: 288, ₹500–₹999: 199, ₹1,000–₹1,999: 59, ₹2,000+: 40; Sum: 767).
- **Methodology Callout**: Prominently highlights that data represents observed catalogue listings collected during the collection period.

### Page 2 — Brand Comparison
- **Benchmark Table**: All 5 brands rendered symmetrically. Rating and review count for AromaPure correctly display as *"No ratings"* and *"Not available"* rather than zero.
- **Brand Focus Selector**: Filtering by brand highlights the selected row and reveals a drilldown card without altering comparative charts.
- **Charts**:
  1. *Average vs. Median Price* (Grouped BarChart).
  2. *Customer Rating Benchmark* (BarChart with tooltips explaining unrated D2C presence).
  3. *Assortment Count by Brand* (BarChart).
  4. *Category Coverage by Brand* (BarChart showing represented categories out of 7).

### Page 3 — Price Positioning
- **Price vs. Rating Scatter Plot**:
  - X-Axis: Selling Price (₹).
  - Y-Axis: Customer Rating (3.0 – 5.0 ★).
  - 364 data points plotted across 4 rated brands.
  - **Zero Imputation Check**: Products without ratings (360 AromaPure products and 43 unrated marketplace items) are strictly excluded from the scatter plot and never plotted at $(x, 0.0)$.
- **Discount Distribution Chart**:
  - Displays average promotional discount depth across brands based on 545 products with non-null MRP.
- **Segregated Unit Pricing**:
  - `price_per_unit`: 767 products (Avg: ₹616.92, Min: ₹13.96, Max: ₹6,345.00).
  - `price_per_100ml`: 271 liquid products (Avg: ₹1,575.96, Median: ₹790.00, Min: ₹34.04, Max: ₹8,090.00).
  - `price_per_100g`: 30 solid products (Avg: ₹411.30, Median: ₹366.00, Min: ₹78.67, Max: ₹1,133.33).
  - Liquids and solids remain strictly segregated on separate visual cards with distinct units.

### Page 4 — Product Analysis
- **Dynamic Multi-Attribute Filtering**:
  - Brand (5 options), Category (7 options), Format (6 options), Platform (2 options), Availability (2 options).
  - Numeric ranges: Price (Min/Max), Rating threshold ($\ge 4.0\text{★}, \ge 4.2\text{★}, \ge 4.4\text{★}, \ge 4.6\text{★}$).
  - Keyword search in title (`title_clean` and `title_raw`).
- **Pagination**:
  - Server-side paginated queries (`LIMIT ? OFFSET ?`).
  - Rows per page: 20, 50, 100.
  - Tested page transitions; zero skipped or duplicated records.
- **Product Detail Drawer/Modal**:
  - Displays clean title, category, format, unit metrics, observed reviews, stock status, and direct clickable public listing URL.

### Page 5 — Business Insights
- **Observed Category Presence Matrix**:
  - Factual $7 \times 5$ cross-tabulation.
  - **Crucial Clarification**: A value of 0 is explicitly defined on screen as *"No observed product in the collected dataset"*, with a prominent disclaimer stating it does not imply the brand does not commercially produce that category.
- **5 Structured Diagnostic Insights**:
  - Every insight adheres strictly to the 4-part framework:
    1. **Factual Observation**: Verifiable dataset fact with exact counts.
    2. **Analytical Interpretation**: Objective deduction regarding catalogue concentration.
    3. **Commercial Business Question**: Strategic trade-off or investigative inquiry.
    4. **Internal Validation Required**: Specific internal proprietary metrics (POS sell-through, margin curves, defect logs) needed before making decisions.
  - Zero unsupported market share claims, zero speculative tiering, and zero subjective brand rankings.

---

## 5. Responsive Design & Usability Audit (Task 10)

| Viewport | Target Device | Layout Behavior | Usability Status |
| :--- | :--- | :--- | :--- |
| **1440px** | Large Desktop | Persistent left sidebar (w-64), 6-column KPI grid, 2-column chart cards. | **PASS** (Zero clipping or overlap) |
| **1280px** | Standard Laptop | Persistent left sidebar (w-64), 3-column KPI grid, 2-column chart cards. | **PASS** (Balanced density) |
| **768px** | Tablet Portrait | Collapsible hamburger drawer, 2-column KPI grid, stacked chart containers. | **PASS** (Fluid transitions) |
| **390px** | Mobile Screen | Slide-out overlay drawer, 1-column KPI cards, horizontally scrollable data table. | **PASS** (Zero horizontal overflow on body) |

---

## 6. Error & Empty State Audit (Task 11)

- **Backend Offline / Network Failure**: `<Header />` displays a red `"API Disconnected"` badge with a red pulse indicator. Pages render `<EmptyState isError={true} title="Unable to Load..." onRetry={...} />` with an actionable retry button rather than crashing or showing a blank page.
- **Zero Query Matches**: When filter combinations yield 0 products, the product table displays: *"No observed products match the selected filter criteria."* with a reset button.
- **Null Safety**: Star ratings on unrated products render as `"Not available"`, discounts without MRP render as `"—"`, and review counts render as `"Not available"`.

---

## 7. Automated Test Suite & Build Verification (Task 13)

### Python Automated Test Suite:
```bash
python -m pytest tests/ -v
# ======================== 44 passed, 2 warnings in 4.54s ========================
```
- Total tests: **44/44 passing** (100% pass rate).
- Added tests verifying `price_distribution` bracket sum, keyword search filter execution, and category coverage matrix total consistency.

### React Production Build:
```bash
cd dashboard && npm run build
# ✓ 2281 modules transformed.
# dist/index.html                   0.89 kB │ gzip:   0.50 kB
# dist/assets/index-DgUTYrmc.css   24.08 kB │ gzip:   5.10 kB
# dist/assets/index-B4i5VUTL.js   628.83 kB │ gzip: 173.86 kB
# ✓ built in 9.29s
```
- Production build succeeds with 0 errors.

---

## 8. Final QA Status

| Audit Dimension | Result | Notes |
| :--- | :---: | :--- |
| **Assignment Compliance** | **PASS** | Meets all analytical, technical, and structural requirements. |
| **Database / API Consistency** | **PASS** | Exact match across all KPIs, medians, and distribution sums. |
| **Dashboard Calculations** | **PASS** | Exact median (₹448.00) and accurate averages across all views. |
| **Business Insight Validity** | **PASS** | All 5 insights strictly structured into 4 diagnostic components. |
| **Filter Functionality** | **PASS** | Multi-field filtering, keyword search, pagination, and reset operational. |
| **Responsive UI** | **PASS** | Tested across 1440px, 1280px, 768px, and 390px viewports. |
| **API Error Handling** | **PASS** | Robust fallback states, offline badges, and retry triggers. |
| **Python Tests** | **44 / 44 PASSED** | Zero failures or regressions. |
| **React Production Build** | **PASS** | Clean production bundle generated in 9.29s. |

### Issues Found During Audit
1. **Low**: The Market Overview route lacked a dedicated price distribution bracket chart requested in the assignment brief.
2. **Medium**: In `BrandComparison.jsx`, only 2 charts were rendered instead of the 4 requested (added Assortment Count and Category Coverage charts).
3. **Medium**: In `PricePositioning.jsx`, promotional discount depth by brand was missing from the visual layout (added discount distribution chart).
4. **Low**: In `products.py`, the backend did not support a `search` keyword parameter and `limit` query alias used by the frontend filter bar.
5. **Low**: In `EmptyState.jsx`, polymorphic prop names (`onRetry` vs `onAction`, `isError` vs `type`) could cause silent event drop if mismatched.
6. **Low**: The Category Coverage matrix row items omitted precomputed `total` keys, causing potential display issues if frontend sum logic varied.

### Issues Fixed
1. Implemented `price_distribution` bracket calculation in `/api/overview` and added a visual `BarChart` in `Overview.jsx`.
2. Expanded `BrandComparison.jsx` to render all 4 required charts: Price Benchmark, Rating Signals, Assortment Count, and Category Coverage.
3. Added a dedicated *Promotional Discount Depth by Brand* chart in `PricePositioning.jsx` strictly filtering for valid non-null MRP items.
4. Added `search` and `limit` query parameters with parameterized SQL pattern matching in `/api/products`.
5. Enhanced `EmptyState.jsx` to support all prop conventions (`isError`/`type`, `onRetry`/`onAction`).
6. Updated `/api/analytics/category-coverage` to calculate row totals and export both `matrix` and `coverage_matrix`.
7. Updated `BusinessInsights.jsx` with verified database metrics and clarified category presence disclaimers.

### Remaining Project Limitations
- **Catalogue Snapshot**: The dataset reflects online public catalogue listings collected during September 2026 and does not represent total offline brick-and-mortar sales volume.
- **Platform Rating Asymmetry**: AromaPure official catalogue listings do not expose public customer review counts or star ratings, which are kept strictly as `NULL`.
- **Packaging Densities**: Liquid ($ml$) and solid ($g$) products are standardized strictly within their physical dimensions and are not converted across states due to formulation density variations.

### Recommended Next Step
Proceed to presentation rehearsal following [`docs/PRESENTATION_PLAN.md`](file:///c:/Users/ndauj/OneDrive/Desktop/Assignment/docs/PRESENTATION_PLAN.md), showcasing the live React dashboard, reproducible pipeline (`python main.py`), and FastAPI documentation (`/docs`).
