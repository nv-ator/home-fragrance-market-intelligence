# Data Quality & Validation Report

**Run ID**: `20260923_184809`  
**Execution Pipeline**: `python main.py --stage clean`  
**Processed Dataset**: `data/processed/products_clean.csv`  
**Rejected Audit Log**: `data/processed/products_rejected.csv`  

---

## 1. Executive Summary

The data cleaning, validation, and normalization pipeline processed **1,436 candidate observations** across the five target brands. Applying strict canonical deduplication, home-fragrance scope evaluation, price sanity checks, and unit standardization resulted in **767 validated unique products**.

All five brands comfortably surpass the recommended threshold of **20+ unique valid products per brand**, and the total of **767 unique valid products** exceeds the required **100+ product minimum by more than 7.6x**.

| Metric | Overall Count |
| :--- | :--- |
| **Total Raw Candidates Processed** | **1,436** |
| **Total Validated Analytical Products** | **767** |
| **Total Rejected Observations** | **669** |
| **- Duplicate Canonical Observations** | **556** |
| **- Out-of-Scope (Car-only / Pest control / Cleaners)** | **68** |
| **- Invalid or Zero Selling Price** | **41** |
| **- Invalid / Unmatched Brand** | **4** |

---

## 2. Brand Breakdown

Every candidate was evaluated symmetrically against the standardized schema and validation rules.

| Brand | Raw Candidates | Validated Products | Duplicate Obs. | Out-of-Scope Excluded | Invalid / Zero Price | % Valid / Raw | Target Met (>= 20)? |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **AromaPure** | 403 | **360** | 0 | 37 | 6 | 89.3% | **YES (360)** |
| **Odonil** | 364 | **145** | 203 | 0 | 16 | 39.8% | **YES (145)** |
| **Godrej aer** | 189 | **129** | 53 | 1 | 6 | 68.3% | **YES (129)** |
| **Air Wick** | 297 | **91** | 193 | 2 | 11 | 30.6% | **YES (91)** |
| **Ambi Pur** | 179 | **42** | 107 | 28 | 2 | 23.5% | **YES (42)** |
| **Total / Overall** | **1,436** | **767** | **556** | **68** | **41** | **53.4%** | **YES (767 >= 100)** |

---

## 3. Canonical Product Identity & Duplicate Handling

- **Identity Strategy**:
  - **Amazon Listings**: Identified canonically by unique marketplace **ASIN**. When the same product appeared across multiple search queries (e.g., brand-level search vs. format-level search), only the first canonical instance was retained.
  - **AromaPure Catalogue**: Identified by **Product ID + Variant ID** (e.g. `9631889031450_49826106179866`). Each scent/size SKU represents an independent purchasable item.
- **Duplicate Observations**:
  - A total of **556 duplicate observations** were identified and moved to `products_rejected.csv` with reason `duplicate_canonical_product`.
  - Air Wick (193 duplicates) and Odonil (203 duplicates) exhibited the highest duplication rate due to broad marketplace query overlap.

---

## 4. Product Scope & Exclusion Analysis

The project enforces a strict **Home Fragrance** boundary:
1. **Car-Only Fragrance Exclusions**:
   - Products explicitly targeted for vehicles (e.g., "car vent clips", "car dashboard perfume", "car perfume flakes", "car hanging perfume") without home/closet/linen application were flagged as `out_of_scope_car_only` (**66 records**).
   - This affected **37 AromaPure car items** and **28 Ambi Pur car vent items**.
2. **Unrelated Cleaners / Pest Control**:
   - Items such as toilet bowl acid cleaners or mosquito repellents returned under brand searches were excluded as `unrelated_product_*` (**2 records**).
3. **Invalid Brand**:
   - Marketplace search sponsored bleed from non-target brands accounted for **4 records** rejected as `invalid_brand`.

---

## 5. Field Completeness & Missing Value Statistics

In accordance with data integrity guidelines, **missing values were preserved as NULL rather than fabricated**:

| Field | Populated Records | Missing Records | Completeness (%) | Notes |
| :--- | :---: | :---: | :---: | :--- |
| `selling_price` | 767 | 0 | **100.0%** | Non-zero numeric selling price in INR. |
| `mrp` | 751 | 16 | **97.9%** | Compare-at / List price in INR. |
| `discount_pct` | 545 | 222 | **71.1%** | Computed strictly when `mrp >= selling_price > 0`. |
| `rating` | 364 | 403 | **47.5%** | Sourced from Amazon reviews (AromaPure D2C lacks star ratings on JSON feed). |
| `review_count` | 364 | 403 | **47.5%** | Sourced from Amazon customer review count. |
| `total_quantity` | 325 | 442 | **42.4%** | Successfully extracted from pack volume/weight/count. |
| `price_per_unit` | 767 | 0 | **100.0%** | Price per pack/unit. |
| `price_per_100ml` | 271 | 496 | **35.3%** | Sourced from liquid sprays, refills, and diffusers. |
| `price_per_100g` | 30 | 737 | **3.9%** | Sourced from solid blocks, candles, and gel pucks. |

### Symmetrical Metric Handling:
- **Missing Discount**: When MRP was missing or equal to selling price, `discount_pct` remained `NULL` and `discount_source` was tagged `unavailable` (never assumed 0% discount).
- **Ratings & Reviews**: AromaPure D2C products have no marketplace star ratings; they are cleanly maintained as `NULL` without imputation.
- **Physical Normalization**: Mass ($g$) and Volume ($ml$) were strictly separated. No arbitrary density conversions (e.g. $1g \neq 1ml$) were applied.

---

## 6. Category Breakdown in Cleaned Dataset

| Standardized Category | Valid Products | Share of Assortment | Primary Formats |
| :--- | :---: | :---: | :--- |
| **Ambient Fragrance (General)** | 415 | 54.1% | Electric aroma warmers, aroma oils, decorative diffusers |
| **Scented Candle & Wax** | 153 | 19.9% | Soy jar candles, pillar candles, scented wax melts |
| **Reed Diffuser & Fragrance Oil** | 80 | 10.4% | Reed diffusers, essential diffuser sets |
| **Room Spray & Aerosol** | 61 | 8.0% | Instant room freshener sprays, linen sprays |
| **Automatic Spray & Refill** | 19 | 2.5% | Automatic matic devices & aerosol refills |
| **Freshener Gel & Pocket** | 12 | 1.6% | Fragrance gel cans, hanging pocket gels |
| **Bathroom Freshener & Block** | 11 | 1.4% | Evaporating fragrance blocks, toilet air blocks |

---

## 7. Compliance Verification
- **Zero data fabricated**: All numbers trace back to `data/raw/` source documents.
- **Raw layer intact**: All files in `data/raw/` remain completely untouched.
- **Traceability**: Each clean record retains its `product_id`, `product_url`, `scraped_at`, and `raw_reference`.
