# Pipeline Execution Run Report

**Run ID**: `20260923_184809`  
**Execution Command**: `python main.py`  
**Start Time**: `2026-09-23T18:48:09Z`  
**End Time**: `2026-09-23T18:50:30Z`  
**Total Duration**: `141.0s`  
**Overall Status**: `SUCCESS`  
**Orchestration Engine**: `PipelineOrchestrator` (`src/pipeline/orchestrator.py`)  

---

## 1. Stage Execution Summary

| Stage | Status | Input Artifact | Output Artifact / Metric | Notes |
| :--- | :---: | :--- | :--- | :--- |
| **1. Collection** | `SUCCESS` | Public Endpoints & Marketplace Search | **1,436 raw candidates** | Saved to `data/raw/` (JSON & HTML) |
| **2. Cleaning & Validation** | `SUCCESS` | `data/raw/` candidates | **767 valid products** (669 rejected) | Saved to `data/processed/products_clean.csv` |
| **3. Transformation** | `SUCCESS` | `products_clean.csv` | **767 transformed records** | Saved to `data/processed/products_transformed.csv` (strictly factual typing; zero arbitrary business labels) |
| **4. Database Storage** | `SUCCESS` | Clean CSV dataset | **767 rows loaded** into SQLite | Relational schema in `data/market_intelligence.db` |
| **5. Quality Gate Gatekeeper** | `SUCCESS` | Database & CSV | **8/8 quality gates passed** | Dynamic validation of all assignment criteria |

---

## 2. Validated Products by Brand

| Brand | Valid Products in Primary Dataset | Minimum Assignment Gate (>=20) Met? |
| :--- | :---: | :---: |
| **AromaPure** | **360** | **YES** |
| **Odonil** | **145** | **YES** |
| **Godrej aer** | **129** | **YES** |
| **Air Wick** | **91** | **YES** |
| **Ambi Pur** | **42** | **YES** |
| **Total Products** | **767** | **YES (7.6x above 100-product floor)** |

---

## 3. Data Integrity & Automated Quality Gate Results

1. **Existence Verification**: `products_clean.csv` and `market_intelligence.db` exist and are in sync.
2. **Dynamic Volume Threshold**: Evaluates dataset dynamically ($767 \ge 100$ products) with zero hardcoded sample sizes.
3. **Exact Brand Parity**: Validates the presence of exactly the 5 target competitor brands.
4. **Per-Brand Sufficiency**: Confirms that every individual brand possesses at least 20 validated products (lowest brand has 42).
5. **Commercial Price Integrity**: 100% of validated products feature positive numeric selling prices in INR.
6. **Canonical Uniqueness**: 100% of canonical product IDs are unique (zero collision).
7. **Idempotent Reruns**: Executing `python main.py` sequentially deterministically rebuilds the analytical database without generating duplicate records.
8. **Analytical Views Operational**: `vw_products_analytical`, `vw_market_overview`, `vw_brand_comparison`, and `vw_category_coverage` verified functional.

---

## 4. Run Manifest Path
- Saved JSON Manifest: `data/pipeline_runs/run_20260923_184809.json`
