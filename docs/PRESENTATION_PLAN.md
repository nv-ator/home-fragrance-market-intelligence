# Home Fragrance Market Intelligence — Presentation & Demonstration Plan

## Demonstration Overview
- **Total Duration**: 8 to 9 minutes (Strict ceiling: 10 minutes)
- **Format**: Live walkthrough of interactive React dashboard, pipeline architecture, and analytical findings
- **Audience**: Stakeholders, Category Leads, Brand Strategy Teams

---

## Presentation Breakdown

## Demonstration Timing Breakdown (8 to 9 Minutes)

| # | Section | Target Duration | Key Metric / Visual | Primary Message |
| :-: | :--- | :---: | :--- | :--- |
| **1** | Introduction & Context | 30 sec | Project Architecture | Objective market intelligence for Indian home fragrance |
| **2** | Business Problem | 40 sec | Problem Matrix | Bridging fragmented e-commerce signals with automated analytics |
| **3** | Data Collection & Sources | 50 sec | 1,436 Raw Obs / Manifests | Public endpoint collection with ethical compliance |
| **4** | Automated Pipeline | 50 sec | `python main.py` | Single-command end-to-end automation with quality gates |
| **5** | Data Quality & Normalization | 40 sec | 767 Clean Products | ASIN/variant deduplication, physical unit standardization |
| **6** | Page 1: Market Overview | 60 sec | 6 KPI Cards + 4 Charts | ₹667.81 Mean, ₹448.00 Median, 767 Products |
| **7** | Page 2: Brand Comparison | 60 sec | Symmetrical Matrix | Neutral benchmarking across 5 brands without bias |
| **8** | Page 3: Price Positioning | 60 sec | Scatter Plot + Unit Rates | ₹1,575.96/100ml vs. ₹411.30/100g segregated unit economics |
| **9** | Page 4: Product Analysis | 45 sec | Filter Bar + Data Table | Multi-attribute search and pagination across all 767 SKUs |
| **10** | Page 5: Business Insights | 90 sec | 7 Diagnostic Cards | 4-part framework: Observation → Interpretation → Question → Validation |
| **11** | Limitations & Validation | 40 sec | Guardrails Card | Online catalogue snapshot; validation required before capital allocation |
| **12** | Closing & Strategic Summary | 20 sec | System Status Badge | End-to-end reproducible market intelligence engine |
| **Total** | | **8 min 25 sec** | **Complete System** | **Within 8–9 minute target** |

---

## Detailed Section Guides

### 1. Introduction & Context (30 sec)
- **What to Show**: Dashboard Header & Title (`Home Fragrance Market Intelligence`).
- **What to Say**: "Welcome. Today we present an end-to-end Business Intelligence platform evaluating the competitive landscape of the Indian Home Fragrance and Air Care market across five major brands: AromaPure, Odonil, Godrej aer, Air Wick, and Ambi Pur."
- **Key Metric**: 5 competitor brands evaluated symmetrically.
- **Business Interpretation**: Provides a systematic, objective analytical lens across publicly listed catalogues.

### 2. Business Problem (40 sec)
- **What to Show**: Executive architectural summary in README or System Architecture Diagram.
- **What to Say**: "Category managers in home air care face fragmented e-commerce signals, inconsistent pack sizes, and promotional noise. Traditional syndicated market research reports are expensive and published with multi-month lags. Our objective was to build an automated, fully reproducible intelligence engine that converts live, public catalogue data into structured strategic decision support."
- **Key Number**: 5 brands, 7 categories, multiple digital retail channels.
- **Business Interpretation**: Replaces anecdotal pricing assumptions with continuous, verifiable empirical data.

### 3. Data Sources & Ethical Collection (50 sec)
- **What to Show**: `data/raw/` directory structure and collection run manifest (`collection_*.json`).
- **What to Say**: "We collected 1,436 raw observations from public e-commerce listings—specifically the AromaPure official direct catalogue and public Amazon India listings. The collection process adheres strictly to ethical data standards: standard HTTP requests, public endpoints, zero CAPTCHA or authentication bypass, with every raw response preserved immutably alongside SHA-256 cryptographic manifests."
- **Key Number**: 1,436 raw candidate observations; 0 bypass mechanisms.
- **Business Interpretation**: Transparent data provenance ensures executive trust and regulatory compliance.

### 4. Automated Pipeline & Quality Gates (50 sec)
- **What to Show**: Terminal showing single command execution: `python main.py`.
- **What to Say**: "The entire data engineering pipeline is 100% reproducible through a single command: `python main.py`. It orchestrates raw extraction, cleaning, deduplication, format normalization, SQLite loading, and automated quality gates checking 8 critical health invariants. The 3NF SQLite database is indexed for sub-10ms query execution."
- **Key Number**: 8/8 automated quality checks passed; 44 automated pytest tests passing.
- **Business Interpretation**: Engineering repeatability eliminates human error and enables automated refreshes.

### 5. Data Quality, Scoping & Normalization (40 sec)
- **What to Show**: `data/processed/products_clean.csv` audit summaries.
- **What to Say**: "Raw candidate data underwent strict scope filtering: we eliminated 66 car-only products and 2 unrelated cleaners to focus strictly on ambient home air care. 556 duplicate search observations were deduplicated via ASIN and variant keys, yielding exactly 767 unique validated products. Crucially, missing values are preserved as NULL rather than converted to zero."
- **Key Number**: 767 validated products; 556 duplicates resolved; 68 out-of-scope items rejected.
- **Business Interpretation**: Preserving missing ratings prevents artificial distortion of customer perception scores.

### 6. Dashboard Walkthrough — Page 1: Market Overview (60 sec)
- **What to Show**: Route `/overview` displaying 6 KPI cards, brand bar chart, platform donut chart, category horizontal bar chart, and price distribution brackets.
- **What to Say**: "Page 1 displays macro market health. Across 767 products, the catalogue average price is ₹667.81, while the exact median price is ₹448.00. Notice the 61.1% clustering of products under ₹500. We explicitly distinguish catalogue share from market share: AromaPure represents 46.9% of observed listings, not 46.9% of market sales."
- **Key Number**: Mean ₹667.81; Median ₹448.00; Rating 4.15★; Discount 39.5%.
- **Business Interpretation**: The catalogue exhibits significant SKU depth in entry-level accessible price points.

### 7. Dashboard Walkthrough — Page 2: Brand Comparison (60 sec)
- **What to Show**: Route `/brands` showing benchmark table and 4 comparative charts.
- **What to Say**: "Page 2 compares the five brands symmetrically without subjective 'winner' or 'loser' labels. Air Wick exhibits the highest average price at ₹1,766.13 driven by automatic dispensers, while Odonil and Godrej aer maintain accessible FMCG anchors (medians ₹239.00 and ₹299.00). Selecting any brand opens an instant focus drilldown."
- **Key Number**: Air Wick mean ₹1,766.13 vs. Odonil mean ₹306.22.
- **Business Interpretation**: Competitor brands anchor around distinct packaging formats and retail occasions.

### 8. Dashboard Walkthrough — Page 3: Price Positioning & Unit Economics (60 sec)
- **What to Show**: Route `/price-positioning` showing Price vs. Rating scatter plot, promotional discount chart, and segregated unit economics cards.
- **What to Say**: "Page 3 highlights empirical positioning. In the scatter plot, unrated products are excluded rather than plotted at zero. Notice the weak correlation (r = +0.24)—higher price does not guarantee higher customer ratings. Furthermore, we strictly separate liquid unit pricing (₹1,575.96/100ml) from solid unit pricing (₹411.30/100g) without artificial density assumptions."
- **Key Number**: Liquids ₹1,575.96/100ml; Solids ₹411.30/100g; Discount depth 39.5%.
- **Business Interpretation**: Liquid refills generate higher realization per standard unit than solid blocks.

### 9. Dashboard Walkthrough — Page 4: Product Analysis (45 sec)
- **What to Show**: Route `/products` interacting with filter dropdowns, keyword search ('lavender'), pagination, and opening a product drawer.
- **What to Say**: "Page 4 enables interactive catalogue exploration across all 767 products. Users can filter by brand, category, platform, format, availability, price, and rating threshold. Server-side pagination guarantees rapid response times. Clicking any row opens a product drawer revealing verified attributes and direct public source links."
- **Key Number**: 767 browsable SKUs with 20/50/100 pagination.
- **Business Interpretation**: Enables tactical competitor benchmarking at the individual SKU and pack level.

### 10. Dashboard Walkthrough — Page 5: Business Insights & Category Matrix (90 sec)
- **What to Show**: Route `/insights` showing Category Presence Matrix and 7 diagnostic insight cards.
- **What to Say**: "Page 5 delivers our strategic diagnostic framework. In the category presence matrix, '0' strictly indicates no observed listing in our collected sample—not absence from commercial production. Each of our 7 insights strictly separates four dimensions: Factual Observation, Analytical Interpretation, Commercial Business Question, and Internal Validation Required. We avoid commands like 'Brand X should launch Y', framing gaps instead as commercial hypotheses for category managers."
- **Key Number**: 7 structured diagnostic insights; 7x5 category presence matrix.
- **Business Interpretation**: Ensures executives receive rigorous decision support rather than speculative leaps.

### 11. Limitations & Validation Needs (40 sec)
- **What to Show**: Methodology Guardrail Banner on Insights page.
- **What to Say**: "We emphasize analytical boundaries: this dataset reflects an online public catalogue snapshot collected during September 2026. It excludes offline kirana distribution and proprietary sales velocity. Any strategic decision regarding portfolio expansion must be validated internally against point-of-sale sell-through, gross margins, and customer demand data."
- **Key Number**: Public online catalogue snapshot; 0 offline POS extrapolation.
- **Business Interpretation**: Maintains professional integrity and avoids misleading executive leadership.

### 12. Closing & Summary (20 sec)
- **What to Show**: Top Header showing connected FastAPI and SQLite status badge.
- **What to Say**: "In summary, we have built a complete, automated, reproducible market intelligence solution—from raw web extraction to analytical SQLite database, REST API, and interactive React dashboard. Thank you, and I invite your questions."
- **Key Message**: 100% compliant, fully reproducible, presentation-ready business intelligence platform.

