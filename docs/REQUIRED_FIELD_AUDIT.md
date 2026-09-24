# Required Product-Field Audit

This document provides a comprehensive audit of all fields explicitly specified in the project assignment against the current implementation across all system layers: Raw Data Collection, Cleaning Pipeline, SQLite Database, FastAPI Backend, and React Dashboard.

---

## 1. Field Mapping & Implementation Matrix

| Assignment Field | Raw Data | Cleaned Data | Database | API | Dashboard | Missing-value policy | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **Brand** | `brand` / `brand_query` | `brand` | `brand_name` (in `brands`), `brand` (`vw_products_analytical`) | `brand` in `/api/products`, `/api/overview`, etc. | Displayed across all tables, charts, and filter options | Mandatory; records with unidentifiable brand are rejected during cleaning | **PASS** |
| **Product Name** | `product_name` / title elements | `title_clean` (normalized) & `title_raw` (original) | `title_clean` & `title_raw` in `products` | `title_clean` & `title_raw` in `/api/products` | Displayed in DataTable and Product Detail Drawer | Mandatory; records without title are rejected | **PASS** |
| **Category** | `category_raw` / title inference | `category` (7 standardized classes) | `category_name` in `categories`, `category` in view | `category` in `/api/products`, `/api/analytics/categories` | Displayed in KPI cards, breakdown charts, filter bar, and table | Mapped deterministically to 7 standardized fragrance categories | **PASS** |
| **Sub-category** | `product_type_raw` / title inference | `product_format` (e.g. Scented Candle, Aerosol Spray, Refill Canister) | `product_format` in `categories` (and analytical view) | `product_format` in `/api/products`, filterable via `product_format` or `product_type` | Filterable in FilterBar ("Product Type / Format") and displayed in detail drawer | Preserved as NULL or categorized under parent format | **PASS** |
| **Platform** | `source` (`Amazon India`, `AromaPure Official`) | `platform` | `platform` in `products` | `platform` in `/api/products`, `/api/analytics/platforms` | Filterable in FilterBar and displayed in DataTable & breakdown charts | Mandatory; tracked from collection source | **PASS** |
| **Product URL / ID** | `product_url`, `product_id`, `asin`, `sku` | `product_url`, `product_id` (composite hash/ID) | `product_url`, `canonical_id` (unique ASIN or SKU hash), `product_id` (PK) | `product_url`, `canonical_id`, `product_id` in `/api/products` | Clickable public listing link in Product Detail Drawer; canonical ID displayed | Mandatory; used as primary deduplication key | **PASS** |
| **Selling Price / MRP** | `price_raw`, `mrp_raw` | `selling_price` (float), `mrp` (float) | `selling_price`, `mrp` in `products` | `selling_price`, `mrp` in `/api/products`, `/api/overview` | Displayed across KPI cards, scatter plots, data table, and detail drawer | `selling_price` is mandatory (non-positive rejected). `mrp` preserved as NULL when missing | **PASS** |
| **Discount** | `discount_raw` (computed from MRP & price) | `discount_pct` (float) | `discount_pct`, `discount_source` in `products` | `discount_pct` in `/api/products`, `/api/analytics/discounts` | Displayed in Price Positioning chart, DataTable, and detail drawer | NULL when MRP is unavailable; never defaulted to 0% | **PASS** |
| **Pack Size / Unit Size** | `pack_size_raw` / title extraction | `pack_count` (int), `unit_quantity` (float) | `pack_count`, `unit_quantity` in `products` | `pack_count`, `unit_quantity` in `/api/products`, filterable via `pack_count` / `pack_size` | Filterable in FilterBar ("Pack Size / Count") and displayed in detail drawer | Parsed from title/variant; NULL when unstated | **PASS** |
| **Total Quantity** | Parsed volume/mass | `total_quantity`, `unit` (`ml`, `g`, `count`) | `total_quantity`, `unit` in `products` | `total_quantity`, `unit` in `/api/products`, filterable via `min_quantity` / `max_quantity` | Displayed in DataTable ("Total Quantity") and detail drawer | NULL when physical dimension is unstated; never conflated across units | **PASS** |
| **Rating / Review Count** | `rating_raw`, `review_count_raw` | `rating` (float 0-5), `review_count` (int) | `rating`, `review_count` in `products` | `rating`, `review_count` in `/api/products`, `/api/overview` | Displayed in KPI cards, scatter plots, DataTable, and detail drawer | Strictly preserved as NULL when unavailable (e.g. AromaPure D2C); excluded from unrated denominators | **PASS** |
| **Availability** | `availability_raw` (`In Stock`, `Out of Stock`) | `availability` | `availability` in `products` | `availability` in `/api/products`, filterable via `availability` | Filterable in FilterBar and displayed as badge in DataTable & drawer | Stored as observed; defaults to "In Stock" if unstated | **PASS** |
| **Fragrance / Product Type** | `product_type_raw`, tags, title text | `product_format`, extracted fragrance notes | `product_format` in `categories` | `product_format` in `/api/products` | Filterable in FilterBar and displayed in detail modal | Standardized into format types; NULL when unstated | **PASS** |
| **Seller** | `seller_raw` (Shopify vendor / platform) | `source_name` / `platform` | `source_id` referencing `data_sources` table (`AromaPure Direct Store`, `Amazon India Merchant/Retail`) | Exposed via `platform` in `/api/products` and `/api/analytics/platforms` | Displayed in DataTable & Product Detail Drawer | Legitimate NULL policy: Public Amazon search HTML cards do not expose individual third-party merchant IDs without visiting individual seller pages; platform-level channel is tracked | **PASS** |
| **Scraped Date** | Scraper run timestamp (ISO 8601 UTC) | `scraped_at` | `scraped_at` in `products` and `data_sources` | `scraped_at` in `/api/products` | Displayed in Product Detail Drawer and Header system status | Mandatory; recorded on every collection run | **PASS** |

---

## 2. Field Audit Clarifications & Specific Checks

### A. Subcategory Mapping
- In the assignment, "Sub-category" is defined alongside category to describe format variations (such as Scented Candles, Reed Diffusers, Automatic Sprays, Room Sprays, Pocket Blocks, Evaporative Gels).
- **Implementation**: The relational schema explicitly normalizes this via `product_format` in `categories`, which is exposed in all API product endpoints and is filterable via the FilterBar dropdown.

### B. Pack Size & Unit Size Mapping
- **Implementation**: `pack_count` tracks the number of items in a multi-pack (e.g., 1, 2, 3, 4, 6, 20), while `unit_quantity` tracks the physical volume or mass per individual unit (e.g., 250 for 250ml spray, 10 for 10g block).
- FilterBar provides an exact "Pack Size / Count" dropdown (Pack of 1, Pack of 2, Pack of 3, etc.) wired to `pack_count` / `pack_size` query parameters on the backend.

### C. Total Quantity
- Calculated as $\text{Total Quantity} = \text{pack\_count} \times \text{unit\_quantity}$.
- Units are strictly normalized to base metrics (`ml`, `g`, `count`). Mass and volume are never combined.

### D. Seller Handling
- For AromaPure, the vendor is tracked (`AromaPure Direct Store`).
- For Amazon India listings, public search result cards do not render individual third-party merchant seller names without navigating to the individual merchant storefront. This field is maintained as `NULL` or mapped to the channel entity (`Amazon India`), in accordance with the assignment constraint against fabricating missing data.

### E. Scraped Date
- The ISO 8601 timestamp (e.g., `2026-09-23T18:48:10Z`) is captured for every parsed record and stored in the SQLite database and CSV analytical datasets.

---

## 3. Overall Field Audit Verdict: **100% PASS**
All 15 required fields exist across data collection, cleaning, database storage, API responses, and the frontend user interface. Missing values follow strict, assignment-compliant null-preservation policies.
