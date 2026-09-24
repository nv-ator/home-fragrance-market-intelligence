# Pipeline Execution Run Report

**Run ID**: `20260924_050352`  
**Start Time**: `2026-09-24T05:03:52.704331+00:00`  
**End Time**: `2026-09-24T05:08:56.270489+00:00`  
**Total Duration**: `303.57s`  
**Overall Status**: `SUCCESS`  

---

## 1. Stage Execution Summary

| Stage | Status | Input | Output / Metrics |
| :--- | :---: | :--- | :--- |
| **Collection** | `SUCCESS` | Public Endpoints & Search | 1012 raw candidate observations |
| **Cleaning & Validation** | `SUCCESS` | Raw Candidates JSON | 684 valid products, 328 rejected |
| **Transformation** | `SUCCESS` | `products_clean.csv` | 684 transformed records |
| **Database Storage** | `SUCCESS` | Clean CSV | 684 rows loaded into SQLite |
| **Final Quality Gate** | `SUCCESS` | Full Analytical DB & CSV | Dynamic checks verified (>=100 products, 5 brands) |

---

## 2. Brand Breakdown in Primary Dataset

| Brand | Valid Products Loaded | Minimum Target (>=20) Met? |
| :--- | :---: | :---: |
| **Air Wick** | 91 | **YES** |
| **Ambi Pur** | 31 | **YES** |
| **AromaPure** | 298 | **YES** |
| **Godrej aer** | 132 | **YES** |
| **Odonil** | 132 | **YES** |

---

## 3. Data Integrity & Automated Quality Gate Results

- **Dynamic Row Check**: 684 products (exceeds assignment threshold >= 100).
- **Exact Brand Parity**: All 5 required brands present with >=20 products.
- **Selling Price Sanity**: 100% of analytical products have positive numeric prices.
- **Canonical ID Uniqueness**: 100% unique identifiers with zero collision.
- **Idempotency Guarantee**: Sequential re-executions rebuild deterministically without creating duplicate records.

---

## 4. Run Manifest Path
- Saved JSON Manifest: `data/pipeline_runs/run_20260924_050352.json`
