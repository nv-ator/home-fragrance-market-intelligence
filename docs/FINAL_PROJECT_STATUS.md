# Final Project Status

## 1. Authoritative Dataset Summary

The primary analytical dataset is completely synchronized across the SQLite database (`data/market_intelligence.db`), CSV exports (`data/processed/products_clean.csv`, `data/processed/products_transformed.csv`), the FastAPI analytical API, the React dashboard, and project documentation.

- **Total Validated Products**: **684** (after car-only product exclusion)
- **Raw Observations Collected**: **1,012** (immutable in `data/raw/`)
- **Duplicates Excluded**: **169**
- **Out-of-Scope Items Filtered**: **135** (all automotive-only items)
- **Invalid / Zero Price Filtered**: **20**
- **Invalid Brand Filtered**: **4**
- **Tracked Competitor Brands**: **5**
  - **AromaPure**: 298 products (43.57% of collected catalogue)
  - **Odonil**: 132 products (19.30%)
  - **Godrej aer**: 132 products (19.30%)
  - **Air Wick**: 91 products (13.30%)
  - **Ambi Pur**: 31 products (4.53%)
- **Platforms Observed**:
  - **Amazon India**: 386 products (56.43%)
  - **AromaPure Official Catalogue**: 298 products (43.57%)
- **Market Pricing Metrics**:
  - **Mean Selling Price**: ₹663.42
  - **Median Selling Price**: ₹434.00 (exact window function median)
  - **Rated Products**: 340 products (49.71% of catalogue)
  - **Mean Rating**: 4.16 ★ (median 4.20 ★)
  - **Observed Reviews**: 9,261 reviews across 491 listings
  - **Discounted Products (>0%)**: 431 products (mean discount 43.70%)
  - **Total Products with MRP Observed**: 479 products (mean discount 39.33%)
- **Price Distribution Brackets**:
  - Under ₹250: 160 products (23.39%)
  - ₹250–₹499: 264 products (38.60%)
  - *(Combined Sub-₹500: 424 products / 61.99%)*
  - ₹500–₹999: 170 products (24.85%)
  - ₹1,000–₹1,999: 55 products (8.04%)
  - ₹2,000+: 35 products (5.12%)
- **Unit Economics**:
  - `price_per_unit`: 684 products (mean: ₹614.93, median: ₹434.00)
  - `price_per_100ml` (liquids): 231 products (mean: ₹1,203.48, median: ₹665.00, range: ₹34.04 to ₹3,993.33)
  - `price_per_100g` (solids): 23 products (mean: ₹369.28, median: ₹330.00, range: ₹78.67 to ₹1,133.33)
- **Price vs. Rating Relationship**:
  - 340 rated products; Pearson correlation $r = +0.24$ (weak empirical correlation; no causation inferred)

---

## 2. Technical Stack

- **Data Engineering**: Python 3.10+, `requests`, `BeautifulSoup4`, `pandas`, `pydantic`
- **Database**: SQLite 3.25+ (`data/market_intelligence.db`, 3NF normalized schema, B-tree indexes, analytical views)
- **Backend API**: FastAPI, Uvicorn, Starlette TestClient, OpenAPI / Swagger
- **Frontend BI Dashboard**: React 18, Vite, Tailwind CSS, Lucide React, Recharts
- **Testing**: `pytest`, `pytest-cov`, automated quality gates

---

## 3. End-to-End Pipeline

The complete pipeline is automated and reproducible through a single command:
```bash
python main.py
```
Flow:
$$\text{COLLECT (1,012)} \longrightarrow \text{CLEAN (684)} \longrightarrow \text{TRANSFORM (684)} \longrightarrow \text{DATABASE (SQLite)} \longrightarrow \text{VALIDATE (8/8 Gates)}$$

---

## 4. Interactive Dashboard Pages

1. **Market Overview (`/overview`)**: 6 Macro KPI cards, Brand Assortment Bar Chart, Platform Donut Chart, Category Bar Chart, Price Distribution Brackets (uses 120-product balanced deterministic sample; 24/brand).
2. **Brand Comparison (`/brands`)**: Symmetrical Benchmark Matrix, Average vs. Median Price Chart, Customer Rating Signals, Assortment Depth, Category Coverage Count, and interactive Brand Drilldown (Full 684 dataset).
3. **Price Positioning (`/price-positioning`)**: Price vs. Customer Rating Scatter Plot (unrated items excluded), Promotional Discount Depth by Brand, Segregated Unit Pricing Cards, and Product Clusters (Full 684 dataset).
4. **Product Analysis (`/products`)**: Dynamic Multi-Attribute Filter Bar, Title Keyword Search, Pagination (20/50/100), and Product Detail Drawer with direct public listing links (120-product balanced sample).
5. **Business Insights (`/insights`)**: Factual Observed Category Presence Matrix and 8 diagnostic cards following the 4-part framework with interactive Brand Lens focus (Full 684 dataset).

---

## 5. Structured Business Insights

All insights adhere strictly to the 4-part framework:
**Factual Observation $\longrightarrow$ Analytical Interpretation $\longrightarrow$ Commercial Business Question $\longrightarrow$ Internal Validation Required**

1. **Assortment Concentration & Catalogue Depth** (78.4% in Ambient Fragrance and Scented Candle formats)
2. **Retail Price Brackets & Dispersion** (62.0% under ₹500, volume anchor)
3. **Weak Empirical Relationship Between Price and Ratings** (r = +0.24 across 340 rated products)
4. **Promotional Discount Depth** (39.3% average discount across 479 items with MRP)
5. **Catalogue Whitespace & Coverage Voids** (3 to 6 categories spanned per brand)
6. **Unit Economics Spread by Physical Form** (₹1,203.48/100ml for liquids vs. ₹369.28/100g for solids)
7. **Customer Feedback & Review Transparency** (9,261 reviews across 491 listings)
8. **Pack-Size Patterns & Multipack Dynamics** (87.6% single units, 12.4% multipacks)

---

## 6. Verification & Testing

- **Python Test Suite**: **47 / 47 tests passed** (`python -m pytest tests/ -v`, 100% pass rate)
- **Frontend Production Build**: **PASS** (`npm run build` succeeds cleanly in ~25s, generating `dist/` with 0 errors)
- **Database & API Connectivity**: Verified (sub-10ms query execution, parameterized SQL, proper CORS)
- **Automated Data Quality Gate**: **8 / 8 quality checks passed** (`python main.py --stage validate`)

---

## 7. Completed Documentation Suite

- [`README.md`](file:///c:/Users/ndauj/OneDrive/Desktop/Assignment/README.md) — Comprehensive technical reference (24 sections)
- [`docs/FINAL_METRICS.md`](file:///c:/Users/ndauj/OneDrive/Desktop/Assignment/docs/FINAL_METRICS.md) — Authoritative metric source of truth
- [`docs/REQUIRED_FIELD_AUDIT.md`](file:///c:/Users/ndauj/OneDrive/Desktop/Assignment/docs/REQUIRED_FIELD_AUDIT.md) — Field mapping and completeness audit
- [`docs/FINAL_SUBMISSION_CHECKLIST.md`](file:///c:/Users/ndauj/OneDrive/Desktop/Assignment/docs/FINAL_SUBMISSION_CHECKLIST.md) — Full assignment requirement audit
- [`docs/PRESENTATION_PLAN.md`](file:///c:/Users/ndauj/OneDrive/Desktop/Assignment/docs/PRESENTATION_PLAN.md) — Executive presentation breakdown
- [`docs/DEMO_TALKING_POINTS.md`](file:///c:/Users/ndauj/OneDrive/Desktop/Assignment/docs/DEMO_TALKING_POINTS.md) — Spoken presentation script for video demo / live presentation
- [`PIPELINE_RUN_REPORT.md`](file:///c:/Users/ndauj/OneDrive/Desktop/Assignment/PIPELINE_RUN_REPORT.md) — Automated run report and quality gate log

---

## 8. Genuine Remaining Limitations

1. **E-Commerce Catalogue Snapshot**: Captures public online catalogue listings collected during September 2026; does not measure physical retail off-take, kirana distribution, or unit sales volume.
2. **Review Visibility Asymmetry**: Marketplace review counts on Amazon India and direct storefront review counts reflect channel-specific social proof signals rather than commercial market share or aggregate sales volume.
3. **Formulation Densities**: Liquid ($ml$) and solid ($g$) products are standardized strictly within their physical dimensions and are never converted across states due to formulation density variations.

---

## 9. Submission Readiness

**READY**

The Home Fragrance Market Intelligence and Brand Positioning platform is complete, verified, numerically consistent across all layers, and ready for demonstration and final submission.
