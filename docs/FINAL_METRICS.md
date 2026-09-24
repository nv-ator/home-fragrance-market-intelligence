# Home Fragrance Market Intelligence — Authoritative Project Metrics

This document establishes the single authoritative source of truth for all quantitative metrics across the Home Fragrance Market Intelligence and Brand Positioning project. 

Every document, API endpoint, React dashboard component, test assertion, and presentation material synchronizes with the values recorded below.

---

## 1. Authoritative Dataset Scope

- **Primary Analytical Database**: `data/market_intelligence.db` (Table: `products`, Analytical View: `vw_products_analytical`)
- **Primary Processed Dataset**: `data/processed/products_clean.csv` (and `data/processed/products_transformed.csv`)
- **Total Validated Analytical Products**: **684** (after car-only product exclusion)
- **Raw Candidate Observations Collected**: **1,012** (immutable in `data/raw/`)
- **Duplicate Observations Excluded**: **169**
- **Out-of-Scope Items Filtered**: **135** (all automotive-only items)
- **Invalid / Zero Selling Price Filtered**: **20**
- **Invalid / Unmatched Brand Filtered**: **4**
- **Target Competitor Brands**: **5** (evaluated symmetrically)

### Brand Counts & Assortment Distribution

| Brand Name | Product Count | Share of Collected Assortment (%) |
| :--- | :---: | :---: |
| **AromaPure** | 298 | 43.57% |
| **Odonil** | 132 | 19.30% |
| **Godrej aer** | 132 | 19.30% |
| **Air Wick** | 91 | 13.30% |
| **Ambi Pur** | 31 | 4.53% |
| **Total** | **684** | **100.00%** |

### Platform Counts & Channel Distribution

| Platform | Product Count | Share of Assortment (%) |
| :--- | :---: | :---: |
| **Amazon India** | 386 | 56.43% |
| **AromaPure Official Catalogue** | 298 | 43.57% |
| **Total** | **684** | **100.00%** |

### Category Counts & Assortment Breakdown

| Category | Product Count | Share of Assortment (%) | Product Format |
| :--- | :---: | :---: | :--- |
| **Ambient Fragrance (General)** | 383 | 55.99% | Mixed / Diffuser / Device |
| **Scented Candle & Wax** | 153 | 22.37% | Candle / Wax Melt |
| **Reed Diffuser & Fragrance Oil** | 80 | 11.70% | Liquid Oil & Reeds |
| **Room Spray & Aerosol** | 40 | 5.85% | Aerosol / Liquid Spray |
| **Automatic Spray & Refill** | 15 | 2.19% | Automated Device / Canister |
| **Bathroom Freshener & Block** | 10 | 1.46% | Solid Block / Hanging Pod |
| **Freshener Gel & Pocket** | 3 | 0.44% | Evaporative Gel / Card |
| **Total** | **684** | **100.00%** | |

---

## 2. Market-Wide Pricing & Engagement Metrics

*Note: All monetary figures are in Indian Rupees (₹).*

| Metric | Exact Value | Methodological Notes |
| :--- | :---: | :--- |
| **Mean Selling Price** | **₹663.42** | Arithmetic average across all 684 products |
| **Median Selling Price** | **₹434.00** | Exact 50th percentile across all 684 products |
| **Minimum Selling Price** | **₹51.00** | Observed on single pocket freshener (Godrej aer / Odonil) |
| **Maximum Selling Price** | **₹6,345.00** | Observed on multi-pack automated refill bundle (Air Wick) |
| **Rated Products Count** | **340** | Exactly 49.71% of total catalogue (Amazon listings only) |
| **Mean Customer Rating** | **4.16 ★** | Calculated across the 340 products with observed ratings |
| **Median Customer Rating** | **4.20 ★** | 50th percentile across rated items |
| **Rating Range** | **1.0 ★ to 5.0 ★** | Minimum: 1.0 ★, Maximum: 5.0 ★ |
| **Total Observed Reviews** | **9,261** | Sum of observed reviews across 491 listings |
| **Discounted Products (>0%)** | **431** | 63.01% of products have active promotional discounts |
| **Mean Discount Depth (>0%)** | **43.70%** | Average markdown among products with discounts > 0% |
| **Total Products with MRP Observed**| **479** | Includes 431 discounted (>0%) + 48 selling at MRP (0% discount) |
| **Mean Discount (all non-null)** | **39.33%** | Calculated across all 479 products where valid MRP exists |

---

## 3. Brand-by-Brand Analytical Matrix

Symmetrical empirical benchmark across the five competitors:

| Metric | AromaPure | Odonil | Godrej aer | Air Wick | Ambi Pur | Total / Overall |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Product Count** | 298 | 132 | 132 | 91 | 31 | **684** |
| **Assortment Share** | 43.57% | 19.30% | 19.30% | 13.30% | 4.53% | **100.00%** |
| **Mean Price (₹)** | ₹633.21 | ₹292.49 | ₹397.72 | ₹1,730.95 | ₹530.97 | **₹663.42** |
| **Median Price (₹)** | ₹485.00 | ₹237.00 | ₹372.50 | ₹905.00 | ₹539.00 | **₹434.00** |
| **Min Price (₹)** | ₹99.00 | ₹51.00 | ₹51.00 | ₹156.00 | ₹229.00 | **₹51.00** |
| **Max Price (₹)** | ₹4,899.00 | ₹5,499.00 | ₹1,590.00 | ₹6,345.00 | ₹999.00 | **₹6,345.00** |
| **Rated Products** | 0 (0.0%) | 112 (84.8%)| 117 (88.6%)| 86 (94.5%) | 25 (80.6%) | **340 (49.7%)** |
| **Mean Rating (★)** | *N/A (NULL)* | 4.11 ★ | 4.13 ★ | 4.29 ★ | 4.08 ★ | **4.16 ★** |
| **Median Rating (★)** | *N/A (NULL)* | 4.20 ★ | 4.20 ★ | 4.30 ★ | 4.20 ★ | **4.20 ★** |
| **Total Reviews** | 7,958 | 427 | 449 | 332 | 95 | **9,261** |
| **Discount Count (>0%)** | 289 (97.0%) | 46 (34.8%) | 62 (47.0%) | 25 (27.5%) | 9 (29.0%) | **431 (63.0%)** |
| **Mean Discount (>0%)** | 45.21% | 52.56% | 35.51% | 41.56% | 12.61% | **43.70%** |
| **Total MRP Observed** | 289 | 131 | 131 | 90 | 31 | **479** |
| **Mean Discount (all MRP)** | 45.21% | 35.55% | 31.91% | 23.61% | 12.61% | **39.33%** |
| **Categories Spanned** | 6 | 3 | 3 | 3 | 5 | **7** |
| **Platforms Observed** | 1 (Official) | 1 (Amazon) | 1 (Amazon) | 1 (Amazon) | 1 (Amazon) | **2** |

---

## 4. Retail Price Distribution Brackets

Defined with continuous, mutually exclusive boundaries:

| Price Bracket | Boundary Definition | Product Count | Share of Catalogue (%) | Cumulative (%) |
| :--- | :--- | :---: | :---: | :---: |
| **Under ₹250** | `selling_price < 250` | 160 | 23.39% | 23.39% |
| **₹250–₹499** | `250 <= selling_price < 500` | 264 | 38.60% | 61.99% |
| *(Combined Sub-₹500)* | `selling_price < 500` | **424** | **61.99%** | **61.99%** |
| **₹500–₹999** | `500 <= selling_price < 1000` | 170 | 24.85% | 86.84% |
| **₹1,000–₹1,999** | `1000 <= selling_price < 2000` | 55 | 8.04% | 94.88% |
| **₹2,000+** | `selling_price >= 2000` | 35 | 5.12% | 100.00% |
| **Total** | | **684** | **100.00%** | **100.00%** |

### Brand Concentration in Sub-₹500 Products

- **Odonil**: 124 out of 132 products (**93.94%**) list below ₹500
- **Godrej aer**: 93 out of 132 products (**70.45%**) list below ₹500
- **Ambi Pur**: 14 out of 31 products (**45.16%**) list below ₹500
- **AromaPure**: 161 out of 298 products (**54.03%**) list below ₹500
- **Air Wick**: 32 out of 91 products (**35.16%**) list below ₹500

---

## 5. Unit Economics (Standardized Price Normalization)

Strictly segregated by physical state to prevent physical unit conflation:

| Normalization Metric | Count | Mean (₹) | Median (₹) | Min (₹) | Max (₹) | Formats Included |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Per Product / Unit** (`price_per_unit`) | 684 | ₹614.93 | ₹434.00 | ₹13.96 | ₹6,345.00 | All individual pack units |
| **Liquid Formats** (`price_per_100ml`) | 231 | **₹1,203.48** | **₹665.00** | **₹34.04** | **₹3,993.33** | Sprays, liquid refills, oils |
| **Solid Formats** (`price_per_100g`) | 23 | **₹369.28** | **₹330.00** | **₹78.67** | **₹1,133.33** | Solid blocks, gels, wax |

*Methodology Rule*: Solid mass (grams) and fluid volume (milliliters) are never summed, averaged, or converted using arbitrary density assumptions.

---

## 6. Price vs. Rating Relationship

- **Total Rated Products**: **340** (ratings strictly between 1.0 ★ and 5.0 ★)
- **Pearson Correlation Coefficient ($r$)**: **+0.24**
- **Interpretation**: A weak positive statistical correlation. Visually, products are widely dispersed across 3.0 to 5.0 stars across all price brackets from ₹51 to ₹6,345. Price alone is not a decisive driver of consumer satisfaction.
- **Causation Guardrail**: Correlation does not establish causation. Higher pricing reflects hardware, pack sizes, and packaging complexity rather than guaranteed superior sentiment.

---

## 7. Observed Category Coverage Matrix

Cross-tabulation of catalog presence across 5 brands:

| Category | Air Wick | Ambi Pur | AromaPure | Godrej aer | Odonil | Total |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Ambient Fragrance (General)** | 82 | 11 | 42 | 121 | 127 | **383** |
| **Automatic Spray & Refill** | 8 | 4 | 3 | 0 | 0 | **15** |
| **Bathroom Freshener & Block** | 0 | 0 | 4 | 5 | 1 | **10** |
| **Freshener Gel & Pocket** | 0 | 3 | 0 | 0 | 0 | **3** |
| **Reed Diffuser & Fragrance Oil** | 0 | 2 | 78 | 0 | 0 | **80** |
| **Room Spray & Aerosol** | 1 | 11 | 18 | 6 | 4 | **40** |
| **Scented Candle & Wax** | 0 | 0 | 153 | 0 | 0 | **153** |
| **Total Products** | **91** | **31** | **298** | **132** | **132** | **684** |

*Methodology Guardrail*: Zero cells ("0") represent **absence of observation in the collected public dataset**, not proof of non-existence in offline commercial markets.

---

## 8. Statistical Product Clusters (K-Means)

- **Clustering Population**: 159 products with non-null `selling_price`, `rating`, `discount_pct`, and `review_count`.
- **Feature Set**: Standardized `[selling_price, rating, discount_pct, log1p(review_count)]`.
- **Optimal K**: **5** (Silhouette Score: **0.4912**).
- **Cluster Profiles**:
  - **Cluster 1** ($n=30$): Median Price ₹238.00 (Mean ₹381.17), Mean Rating 4.28★, Mean Discount 86.88%, Mean Reviews 4.00. Deeply discounted entry-level offerings.
  - **Cluster 2** ($n=33$): Median Price ₹360.00 (Mean ₹432.24), Mean Rating 3.55★, Mean Discount 26.68%, Mean Reviews 2.91. Accessible pricing with lower average rating signals.
  - **Cluster 3** ($n=10$): Median Price ₹384.00 (Mean ₹460.70), Mean Rating 5.00★, Mean Discount 15.12%, Mean Reviews 5.00. Perfect 5-star ratings with modest discounting.
  - **Cluster 4** ($n=70$): Median Price ₹441.50 (Mean ₹477.09), Mean Rating 4.23★, Mean Discount 16.39%, Mean Reviews 4.00. Core market volume anchor with steady positive ratings.
  - **Cluster 5** ($n=16$): Median Price ₹3,833.00 (Mean ₹3,584.62), Mean Rating 4.44★, Mean Discount 20.21%, Mean Reviews 3.94. Hardware devices, automatic diffusers, and multipack bundles.

*Methodology Rule*: Clusters are assigned neutral identifiers (Cluster 1, Cluster 2, etc.) rather than subjective marketing labels ("Budget", "Premium", "Mass").

---

## 9. Pack-Size & Volume Distribution

- **Total Products**: 684
- **Pack Count Breakdown**:
  - Single unit (1-pack): 599 products (**87.57%**)
  - 2-pack: 38 products (**5.56%**)
  - 3-pack: 10 products (**1.46%**)
  - 4-pack: 3 products (0.44%)
  - 5-pack: 1 product (0.15%)
  - 6-pack: 7 products (1.02%)
  - 10-pack: 2 products (0.29%)
  - 12-pack: 1 product (0.15%)
  - 15-pack: 1 product (0.15%)
  - 20-pack: 19 products (**2.78%**)
  - 25-pack: 3 products (0.44%)
  - *Multipacks total*: **85 products (12.43%)**
- **Explicit Volume/Mass Documented**: 274 products (40.06% of catalogue)
  - Liquid volume (`ml`): 231 products (Median: 100ml)
  - Solid mass (`g`): 23 products (Median: 150g)
