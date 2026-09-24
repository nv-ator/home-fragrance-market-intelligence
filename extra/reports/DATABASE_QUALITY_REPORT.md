# Analytical Database Quality Report

**Database Path**: `data/market_intelligence.db`  
**Execution Command**: `python main.py --stage database --rebuild`  
**Source Dataset**: `data/processed/products_clean.csv`  
**Engine**: SQLite 3.25+ with Foreign Keys (`PRAGMA foreign_keys = ON`) and Window Functions  

---

## 1. Executive Summary

The relational analytical model has been constructed, indexed, and populated. The database loader mapped all **767 validated products** from the processed CSV into a 3rd Normal Form (3NF) relational star/snowflake schema with **zero row loss** and **100% data fidelity**.

All dimension entities (`brands`, `categories`, `data_sources`) and analytical views (`vw_products_analytical`, `vw_market_overview`, `vw_brand_comparison`, `vw_category_coverage`) are active and verified.

---

## 2. Table Summary & Row Counts

| Table Name | Type | Row Count | Primary Key | Purpose |
| :--- | :---: | :---: | :--- | :--- |
| `products` | Fact / Entity | **767** | `product_id` (INTEGER AUTOINCREMENT) | Canonical validated product records. |
| `brands` | Dimension | **5** | `brand_id` (INTEGER AUTOINCREMENT) | Master list of the 5 target competitor brands. |
| `categories` | Dimension | **7** | `category_id` (INTEGER AUTOINCREMENT) | Standardized home fragrance categories & formats. |
| `data_sources` | Dimension | **2** | `source_id` (INTEGER AUTOINCREMENT) | Ingestion channels & API/search source types. |

---

## 3. Schema & Index Structure

### Tables
1. **`brands`**: `brand_id`, `brand_name` (UNIQUE)
2. **`categories`**: `category_id`, `category_name` (UNIQUE), `product_format`
3. **`data_sources`**: `source_id`, `source_name`, `platform`, `source_type` (UNIQUE `source_name, platform`)
4. **`products`**:
   - Primary Identifiers: `product_id`, `canonical_id` (UNIQUE), `brand_id` (FK), `category_id` (FK), `source_id` (FK)
   - Core Attributes: `title_clean`, `title_raw`, `platform`, `product_url`, `availability`, `scraped_at`, `raw_reference`
   - Commercial Pricing: `selling_price`, `mrp`, `discount_pct`, `discount_source`
   - Customer Engagement: `rating`, `review_count`
   - Physical Standardized Units: `pack_count`, `unit_quantity`, `unit`, `total_quantity`
   - Normalized Metrics: `price_per_unit`, `price_per_100g`, `price_per_100ml`

### Indexes Created for Dashboard & Query Acceleration:
- `idx_products_brand_id` on `products(brand_id)`
- `idx_products_category_id` on `products(category_id)`
- `idx_products_source_id` on `products(source_id)`
- `idx_products_platform` on `products(platform)`
- `idx_products_selling_price` on `products(selling_price)`
- `idx_products_rating` on `products(rating)`
- `idx_products_review_count` on `products(review_count)`
- `idx_products_availability` on `products(availability)`
- `idx_products_unit` on `products(unit)`

---

## 4. Analytical Views

The analytical layer provides reusable, pre-joined views in [`sql/schema.sql`](file:///c:/Users/ndauj/OneDrive/Desktop/Assignment/sql/schema.sql):
- **`vw_products_analytical`**: Complete denormalized view joining `products`, `brands`, `categories`, and `data_sources` for consumption by the FastAPI layer and React dashboard.
- **`vw_market_overview`**: Aggregated macro market metrics (Total products, total brands, market average selling price, average rating, total reviews, average discount, categories covered).
- **`vw_brand_comparison`**: Side-by-side benchmark matrix displaying each brand's assortment count, share of collected assortment, price range, average rating, and review share.
- **`vw_category_coverage`**: Category-by-brand coverage matrix tracking product count, average price, and customer engagement across fragrance types.

---

## 5. Metric Breakdown & Verification

### A. Assortment by Brand

| Brand | Database Product Count | CSV Product Count | Share of Collected Assortment (%) | Categories Covered |
| :--- | :---: | :---: | :---: | :---: |
| **AromaPure** | **360** | 360 | 46.94% | 7 |
| **Odonil** | **145** | 145 | 18.90% | 5 |
| **Godrej aer** | **129** | 129 | 16.82% | 3 |
| **Air Wick** | **91** | 91 | 11.86% | 2 |
| **Ambi Pur** | **42** | 42 | 5.48% | 5 |
| **Total** | **767** | **767** | **100.0%** | **7** |

### B. Assortment by Platform

| Platform | Products | % Share |
| :--- | :---: | :---: |
| **Amazon India** | 407 | 53.06% |
| **AromaPure Official** | 360 | 46.94% |

### C. Assortment by Category

| Category | Products | % Share |
| :--- | :---: | :---: |
| **Ambient Fragrance (General)** | 430 | 56.06% |
| **Scented Candle & Wax** | 153 | 19.95% |
| **Reed Diffuser & Fragrance Oil** | 81 | 10.56% |
| **Room Spray & Aerosol** | 61 | 7.95% |
| **Automatic Spray & Refill** | 19 | 2.48% |
| **Freshener Gel & Pocket** | 12 | 1.56% |
| **Bathroom Freshener & Block** | 11 | 1.43% |

---

## 6. NULL & Missing Value Integrity

Strict adherence to data integrity principles was maintained:
- **No Zero Imputation**: 403 products without ratings remain `NULL`. They were **not** converted to 0.0.
- **No Freebie Discard**: 16 products with missing MRP remain `NULL` with `discount_pct` set to `NULL` and `discount_source = 'unavailable'`.
- **Physical Separation**: `price_per_100g` is strictly populated for mass units ($g$, 30 products) and `price_per_100ml` strictly for volume units ($ml$, 271 products).

---

## 7. Reproducibility & Build Instructions

The entire analytical database can be cleanly dropped, recreated, and repopulated at any time via a single command:
```bash
python main.py --stage database --rebuild
```
The rebuild process:
1. Removes any existing `data/market_intelligence.db`.
2. Executes `sql/schema.sql` (creating tables, indexes, and views).
3. Reads `data/processed/products_clean.csv`.
4. Populates dimensions (`brands`, `categories`, `data_sources`).
5. Inserts 767 products with foreign key enforcement.
6. Runs built-in validation checks and outputs the brand distribution.
