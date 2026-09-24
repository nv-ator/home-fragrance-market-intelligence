# Home Fragrance Market Intelligence — Authoritative Project Metrics

This document establishes the single authoritative source of truth for all quantitative metrics across the Home Fragrance Market Intelligence and Brand Positioning project. 

Every document, API endpoint, React dashboard component, test assertion, and presentation material must strictly synchronize with the values recorded below.

---

## 1. Authoritative Dataset Scope

- **Primary Analytical Database**: `data/market_intelligence.db` (Table: `products`, Analytical View: `vw_products_analytical`)
- **Primary Processed Dataset**: `data/processed/products_clean.csv` (and `data/processed/products_transformed.csv`)
- **Total Validated Analytical Products**: **767**
- **Raw Candidate Observations Collected**: **1,436** (immutable in `data/raw/`)
- **Duplicate Observations Excluded**: **556**
- **Out-of-Scope Items Filtered**: **68** (66 automotive-only items, 2 non-air care cleaners)
- **Target Competitor Brands**: **5** (evaluated symmetrically)

### Brand Counts & Assortment Distribution

| Brand Name | Product Count | Share of Collected Assortment (%) |
| :--- | :---: | :---: |
| **AromaPure** | 360 | 46.94% |
| **Odonil** | 145 | 18.90% |
| **Godrej aer** | 129 | 16.82% |
| **Air Wick** | 91 | 11.86% |
| **Ambi Pur** | 42 | 5.48% |
| **Total** | **767** | **100.00%** |

### Platform Counts & Channel Distribution

| Platform | Product Count | Share of Assortment (%) |
| :--- | :---: | :---: |
| **Amazon India** | 407 | 53.06% |
| **AromaPure Official Catalogue** | 360 | 46.94% |
| **Total** | **767** | **100.00%** |

### Category Counts & Assortment Breakdown

| Category | Product Count | Share of Assortment (%) | Product Format |
| :--- | :---: | :---: | :--- |
| **Ambient Fragrance (General)** | 430 | 56.06% | Mixed / Diffuser / Device |
| **Scented Candle & Wax** | 153 | 19.95% | Candle / Wax Melt |
| **Reed Diffuser & Fragrance Oil** | 81 | 10.56% | Liquid Oil & Reeds |
| **Room Spray & Aerosol** | 61 | 7.95% | Aerosol / Liquid Spray |
| **Automatic Spray & Refill** | 19 | 2.48% | Automated Device / Canister |
| **Freshener Gel & Pocket** | 12 | 1.56% | Evaporative Gel / Card |
| **Bathroom Freshener & Block** | 11 | 1.43% | Solid Block / Hanging Pod |
| **Total** | **767** | **100.00%** | |

---

## 2. Market-Wide Pricing & Engagement Metrics

*Note: All monetary figures are in Indian Rupees (₹).*

| Metric | Exact Value | Methodological Notes |
| :--- | :---: | :--- |
| **Mean Selling Price** | **₹667.81** | Arithmetic average across all 767 products |
| **Median Selling Price** | **₹448.00** | Exact 50th percentile (50% of items ≤ ₹448.00) |
| **Price Standard Deviation** | **₹843.94** | Reflects heavy positive skew from electronic hardware/gift sets |
| **Minimum Selling Price** | **₹50.00** | Observed on single pocket freshener (Odonil) |
| **Maximum Selling Price** | **₹6,345.00** | Observed on multi-pack automated refill bundle (Air Wick) |
| **Rated Products Count** | **364** | Exactly 47.46% of total catalogue (Amazon listings only) |
| **Mean Customer Rating** | **4.15 ★** | Calculated across the 364 products with observed ratings |
| **Median Customer Rating** | **4.20 ★** | 50th percentile across rated items |
| **Rating Range** | **1.0 ★ to 5.0 ★** | Minimum: 1.0 ★, Maximum: 5.0 ★ |
| **Total Observed Reviews** | **1,387** | Sum of public reviews across 364 rated marketplace listings |
| **Mean Reviews (per rated item)** | **3.81** | Arithmetic average across the 364 rated listings |
| **Median Reviews (per rated item)**| **4.00** | Median review count for rated products |
| **Discounted Products (>0%)** | **494** | 64.41% of products have active promotional discounts |
| **Mean Discount Depth (>0%)** | **43.54%** | Average markdown among products with discounts > 0% |
| **Total Products with MRP Observed**| **545** | Includes 494 discounted (>0%) + 51 selling at MRP (0% discount) |
| **Mean Discount (all non-null)** | **39.47%** | Calculated across all 545 products where valid MRP exists |

---

## 3. Brand-by-Brand Analytical Matrix

Symmetrical empirical benchmark across the five competitors:

| Metric | AromaPure | Odonil | Godrej aer | Air Wick | Ambi Pur | Total / Overall |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Product Count** | 360 | 145 | 129 | 91 | 42 | **767** |
| **Assortment Share** | 46.94% | 18.90% | 16.82% | 11.86% | 5.48% | **100.00%** |
| **Mean Price (₹)** | ₹665.21 | ₹306.22 | ₹368.11 | ₹1,766.13 | ₹479.19 | **₹667.81** |
| **Median Price (₹)** | ₹499.00 | ₹239.00 | ₹299.00 | ₹905.00 | ₹518.50 | **₹448.00** |
| **Min Price (₹)** | ₹99.00 | ₹50.00 | ₹51.00 | ₹158.00 | ₹160.00 | **₹50.00** |
| **Max Price (₹)** | ₹4,899.00 | ₹5,499.00 | ₹1,590.00 | ₹6,345.00 | ₹999.00 | **₹6,345.00** |
| **Rated Products** | 0 (0.0%) | 124 (85.5%)| 118 (91.5%)| 87 (95.6%) | 35 (83.3%) | **364 (47.5%)** |
| **Mean Rating (★)** | *N/A (NULL)* | 4.11 ★ | 4.13 ★ | 4.30 ★ | 3.97 ★ | **4.15 ★** |
| **Median Rating (★)** | *N/A (NULL)* | 4.20 ★ | 4.20 ★ | 4.30 ★ | 4.10 ★ | **4.20 ★** |
| **Total Reviews** | 0 *(NULL)* | 473 | 453 | 336 | 125 | **1,387** |
| **Discount Count (>0%)** | 348 (96.7%) | 51 (35.2%) | 52 (40.3%) | 26 (28.6%) | 17 (40.5%) | **494 (64.4%)** |
| **Mean Discount (>0%)** | 43.80% | 50.53% | 38.74% | 42.37% | 33.83% | **43.54%** |
| **Total MRP Observed** | 348 | 75 | 60 | 44 | 18 | **545** |
| **Mean Discount (all MRP)** | 43.80% | 34.36% | 33.58% | 25.04% | 31.95% | **39.47%** |
| **Categories Spanned** | 7 | 5 | 3 | 2 | 5 | **7** |
| **Platforms Observed** | 1 (Official) | 1 (Amazon) | 1 (Amazon) | 1 (Amazon) | 1 (Amazon) | **2** |

---

## 4. Retail Price Distribution Brackets

Defined with continuous, mutually exclusive boundaries:

| Price Bracket | Boundary Definition | Product Count | Share of Catalogue (%) | Cumulative (%) |
| :--- | :--- | :---: | :---: | :---: |
| **Under ₹250** | `selling_price < 250` | 181 | 23.60% | 23.60% |
| **₹250–₹499** | `250 <= selling_price < 500` | 288 | 37.55% | 61.15% |
| *(Combined Sub-₹500)* | `selling_price < 500` | **469** | **61.15%** | **61.15%** |
| **₹500–₹999** | `500 <= selling_price < 1000` | 199 | 25.95% | 87.09% |
| **₹1,000–₹1,999** | `1000 <= selling_price < 2000` | 59 | 7.69% | 94.78% |
| **₹2,000+** | `selling_price >= 2000` | 40 | 5.22% | 100.00% |
| **Total** | | **767** | **100.00%** | **100.00%** |

### Brand Concentration in Sub-₹500 Products

- **Odonil**: 134 out of 145 products (**92.41%**) list below ₹500
- **Godrej aer**: 102 out of 129 products (**79.07%**) list below ₹500
- **Ambi Pur**: 20 out of 42 products (**47.62%**) list below ₹500
- **AromaPure**: 181 out of 360 products (**50.28%**) list below ₹500
- **Air Wick**: 32 out of 91 products (**35.16%**) list below ₹500

---

## 5. Unit Economics (Standardized Price Normalization)

Strictly segregated by physical state to prevent physical unit conflation:

| Normalization Metric | Count | Mean (₹) | Median (₹) | Min (₹) | Max (₹) | Formats Included |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Per Product / Unit** (`price_per_unit`) | 767 | ₹616.92 | ₹448.00 | ₹13.96 | ₹6,345.00 | All individual pack units |
| **Liquid Formats** (`price_per_100ml`) | 271 | **₹1,575.96** | **₹790.00** | **₹34.04** | **₹8,090.00** | Sprays, liquid refills, oils |
| **Solid Formats** (`price_per_100g`) | 30 | **₹411.30** | **₹366.00** | **₹78.67** | **₹1,133.33** | Solid blocks, gels, wax |

*Methodology Rule*: Solid mass (grams) and fluid volume (milliliters) are never summed, averaged, or converted using arbitrary density assumptions.

---

## 6. Price vs. Rating Relationship

- **Total Rated Products**: **364** (ratings strictly between 1.0 ★ and 5.0 ★)
- **Pearson Correlation Coefficient ($r$)**: **+0.2424**
- **Interpretation**: A weak positive statistical correlation. Visually, products are widely dispersed across 3.0 to 5.0 stars across all price brackets from ₹50 to ₹6,345. Price alone is not a decisive driver of consumer satisfaction.
- **Causation Guardrail**: Correlation does not establish causation. Higher pricing reflects hardware, pack sizes, and packaging complexity rather than guaranteed superior sentiment.

---

## 7. Observed Category Coverage Matrix

Cross-tabulation of catalog presence across 5 brands:

| Category | Air Wick | Ambi Pur | AromaPure | Godrej aer | Odonil | Total |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Ambient Fragrance (General)** | 81 | 16 | 78 | 117 | 138 | **430** |
| **Scented Candle & Wax** | 0 | 0 | 153 | 0 | 0 | **153** |
| **Reed Diffuser & Fragrance Oil** | 0 | 2 | 78 | 0 | 1 | **81** |
| **Room Spray & Aerosol** | 0 | 12 | 39 | 6 | 4 | **61** |
| **Automatic Spray & Refill** | 10 | 5 | 3 | 0 | 1 | **19** |
| **Freshener Gel & Pocket** | 0 | 7 | 5 | 0 | 0 | **12** |
| **Bathroom Freshener & Block** | 0 | 0 | 4 | 6 | 1 | **11** |
| **Total Products** | **91** | **42** | **360** | **129** | **145** | **767** |

*Methodology Guardrail*: Zero cells ("0") represent **absence of observation in the collected public dataset**, not proof of non-existence in offline commercial markets.

---

## 8. Statistical Product Clusters (K-Means)

- **Clustering Population**: 171 products with non-null `selling_price`, `rating`, `discount_pct`, and `review_count`.
- **Feature Set**: Standardized `[selling_price, rating, discount_pct, log1p(review_count)]`.
- **Optimal K**: **4** (Silhouette Score: **0.4717**).
- **Cluster Profiles**:
  - **Cluster 1** ($n=36$): Median Price ₹224.50 (Mean ₹390.36), Mean Rating 4.31★, Mean Discount 81.15%, Mean Reviews 4.08. High discount depth, accessible entry pricing.
  - **Cluster 2** ($n=41$): Median Price ₹295.00 (Mean ₹340.12), Mean Rating 3.56★, Mean Discount 33.36%, Mean Reviews 2.93. Moderate price points, lower customer ratings.
  - **Cluster 3** ($n=80$): Median Price ₹435.00 (Mean ₹484.94), Mean Rating 4.32★, Mean Discount 12.00%, Mean Reviews 4.09. Mainstream pricing, modest discounts, consistent positive ratings.
  - **Cluster 4** ($n=14$): Median Price ₹4,153.00 (Mean ₹3,892.57), Mean Rating 4.42★, Mean Discount 23.65%, Mean Reviews 3.93. Multi-pack refills and automated dispenser hardware bundles (Air Wick).

*Methodology Rule*: Clusters are assigned neutral identifiers (Cluster 1, Cluster 2, etc.) rather than subjective marketing labels ("Budget", "Premium", "Mass").

---

## 9. Pack-Size & Volume Distribution

- **Total Products**: 767
- **Pack Count Breakdown**:
  - Single unit (1-pack): 677 products (**88.27%**)
  - 2-pack: 40 products (**5.22%**)
  - 3-pack: 12 products (**1.56%**)
  - 4-pack: 2 products (0.26%)
  - 5-pack: 3 products (0.39%)
  - 6-pack: 7 products (0.91%)
  - 10-pack: 2 products (0.26%)
  - 12-pack: 1 product (0.13%)
  - 15-pack: 1 product (0.13%)
  - 20-pack: 19 products (**2.48%**)
  - 25-pack: 3 products (0.39%)
- **Standardized Physical Volume Coverage**: 325 products (42.37% of catalogue)
  - Liquid volume (`ml`): 271 products (Median: 60ml, Mean: 104.5ml, Min: 7.5ml, Max: 1000ml)
  - Solid mass (`g`): 30 products (Median: 75g, Mean: 110.5g, Min: 10g, Max: 275g)
  - Unit count (`count`): 24 products (Single-piece devices / diffusers)
