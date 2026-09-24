# Raw Data Collection Report

**Run ID**: `20260923_184809`  
**Timestamp**: `2026-09-23T18:49:40Z`  
**Execution Pipeline**: `python main.py --stage collect`  
**Compliance Status**: Fully compliant. Zero CAPTCHA solving, zero authentication/access-control bypass, polite sequential rate limiting (2.5s–4.0s).

---

## 1. Executive Summary
The data collection layer successfully queried public endpoints and catalogue search pages for all five target home-fragrance brands. A total of **1,016 raw candidate product records** were extracted and immutably archived across source-specific JSON files and raw HTML pages, backed by a cryptographic collection manifest.

| Metric | Value |
| :--- | :--- |
| **Total Raw Candidates** | **1,016** |
| **Brands Attempted** | **5 / 5** |
| **Brands Successful** | **5 / 5** |
| **Total Sources Ingested** | 2 (AromaPure Official Shopify Catalogue & Amazon India Public Search) |
| **Failed Requests** | **0** |
| **Raw Content Archived** | ~31 MB across 16 HTML pages and 1 JSON file |
| **Manifest Path** | `data/raw/manifests/collection_20260923_184809.json` |

---

## 2. Candidates by Brand

| Brand | Source | Raw Candidates | Response Size (Bytes) | Elapsed Time (s) | Feasibility for Cleaning (Target: 20+) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **AromaPure** | AromaPure Official | **407** | 998,022 | 0.57s | **Super-sufficient** (407 candidates) |
| **Odonil** | Amazon India | **183** | 7,629,465 | 21.82s | **Super-sufficient** (183 candidates) |
| **Godrej aer** | Amazon India | **189** | 7,794,301 | 24.29s | **Super-sufficient** (189 candidates) |
| **Air Wick** | Amazon India | **148** | 7,228,394 | 21.30s | **Super-sufficient** (148 candidates) |
| **Ambi Pur** | Amazon India | **89** | 7,438,541 | 21.95s | **Super-sufficient** (89 candidates) |
| **Total** | | **1,016** | **31,088,723** | **89.93s** | **High Margin across all brands** |

*Note: In the AromaPure catalogue response, 403 records are authored under vendor "Aromahpure" and 4 under bundle utility "Box Builder". All variants have been preserved as candidates.*

---

## 3. Candidates by Source Channel

| Source Channel | Source Type | Raw Candidate Records | Archival Location |
| :--- | :--- | :---: | :--- |
| **AromaPure Official** | Shopify REST JSON API | 407 | `data/raw/aromapure/products_20260923T184626Z.json` |
| **Amazon India** | Public Search HTML (Targeted) | 609 | `data/raw/amazon/<brand>/search_q*.html` |

---

## 4. Fields Captured & Completeness Assessment

Every candidate record complies with the provenance schema:

```json
{
  "source": "...",
  "brand_query": "...",
  "source_url": "...",
  "product_url": "...",
  "product_id": "...",
  "asin": "...",
  "sku": "...",
  "product_name": "...",
  "brand": "...",
  "category_raw": "...",
  "subcategory_raw": null,
  "product_type_raw": "...",
  "tags_raw": [...],
  "price_raw": "...",
  "mrp_raw": "...",
  "discount_raw": null,
  "pack_size_raw": "...",
  "rating_raw": "...",
  "review_count_raw": "...",
  "availability_raw": "...",
  "seller_raw": "...",
  "description_raw": "...",
  "scraped_at": "...",
  "raw_source_reference": "..."
}
```

### Field Presence by Source:
- **AromaPure Official**:
  - `product_id`, `sku`, `product_name`, `brand`, `product_type_raw`, `tags_raw`, `price_raw`, `mrp_raw`, `availability_raw`, `pack_size_raw` (from `grams` or variant title), `product_url`, `description_raw` are populated.
  - Marketplace reviews (`rating_raw`, `review_count_raw`) and `asin` are null (by nature of direct D2C catalogue).
- **Amazon India (Odonil, Godrej aer, Air Wick, Ambi Pur)**:
  - `asin`, `product_id`, `product_name`, `brand`, `price_raw`, `mrp_raw`, `rating_raw`, `review_count_raw`, `availability_raw`, `tags_raw` (e.g. Best Seller badges), `product_url` are populated.
  - `sku` and `description_raw` are null on the top-level search card.

---

## 5. Observations & Pre-Cleaning Insights

1. **Duplicate Identifiers**:
   - Because multiple queries were executed per brand on Amazon (e.g., "Odonil air freshener" and "Odonil room spray pocket"), certain high-ranking hero ASINs appeared across multiple search queries. These duplicates are deliberately preserved in `data/raw/` to maintain the integrity of raw source observations; deduplication will take place in Step 3.
2. **Category Scope**:
   - Both AromaPure and Amazon candidate sets include items spanning Room Sprays, Diffusers, Candles, Bathroom Fresheners, Automatic Refills, and Car Fresheners.
   - The subsequent cleaning stage will systematically filter and standardize home fragrance scope vs. car-only products according to project rules.
3. **Price Sanity**:
   - AromaPure variants include a few 0.00 freebie promo items (e.g., gift-with-purchase tags); the cleaning stage will handle these according to non-zero price validation rules.

---

## 6. Conclusion
The collection layer is 100% complete, verified, and test-covered. All 5 brands have between 89 and 407 raw candidate records, vastly exceeding the required minimum of 20 products per brand and 100 products total. We are fully prepared to proceed to the Cleaning & Validation step.

## 7. AromaPure Review Enrichment

The AromaPure official Shopify catalogue remains the canonical source for product identity, variants, pricing, availability, and URLs. A public product-page enrichment step now attempts to archive each official PDP and extract only explicitly published aggregate review fields from JSON-LD or visible page text. Explicit `No reviews` is represented as review count `0`; absent review information remains `NULL`.

Amazon India remains a secondary source for marketplace observations only. Official-site and Amazon review counts are stored with source fields and are not added together. Seller values are stored only when an actual merchant name is explicitly exposed.

Source selection was based on public accessibility and reproducibility. The official AromaPure catalogue was retained for canonical product coverage, while marketplace data is used as a secondary source for publicly visible marketplace signals.

### Enrichment Run Result (2026-09-24)

- AromaPure official candidates reprocessed: **407**
- Unique official PDP responses archived: **176**
- AromaPure validated products after enrichment: **360**
- Products with explicit official review count: **39**
- Products with explicit official aggregate rating: **0**
- Products with official seller name: **0**
- Unmatched/unfetched candidate PDPs: **231**
- Observed official review count across enriched validated rows: **2,239**
- Amazon AromaPure marketplace observations added: **0**

The public host was slow and intermittently closed PDP connections, so the run was bounded after 176 unique pages. No values were inferred from rating distributions, no seller names were fabricated, and unavailable ratings/reviews remain `NULL`. The existing 767 validated product total and all canonical IDs were preserved.
