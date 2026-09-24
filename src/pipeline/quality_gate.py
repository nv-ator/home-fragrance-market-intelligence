import os
import json
import sqlite3
import pandas as pd
from datetime import datetime, timezone
from typing import Dict, Any, List, Tuple

from src.utils.logger import setup_logger

logger = setup_logger("quality_gate")

REQUIRED_BRANDS = ["AromaPure", "Odonil", "Godrej aer", "Air Wick", "Ambi Pur"]

class QualityGateError(Exception):
    """Raised when the analytical dataset fails a mandatory quality check."""
    pass

class DataQualityGate:
    """
    Automated gate verifying:
    1. Products dataset exists
    2. Dynamic product count >= 100
    3. Exactly the 5 required brands exist
    4. Each brand has approximately 20+ valid products
    5. Selling prices are positive and numeric
    6. Canonical IDs are unique
    7. SQLite database exists and matches CSV row count
    8. Database analytical views are operational
    """

    def __init__(self, db_path: str = "data/market_intelligence.db", csv_path: str = "data/processed/products_clean.csv"):
        self.db_path = db_path
        self.csv_path = csv_path

    def run_checks(self) -> Dict[str, Any]:
        logger.info("[VALIDATE] Running final automated data-quality gate...")
        report = {
            "passed": False,
            "checks": {},
            "errors": []
        }

        # 1. Check CSV existence
        if not os.path.exists(self.csv_path):
            err = f"Processed dataset not found at {self.csv_path}"
            report["errors"].append(err)
            raise QualityGateError(err)
        report["checks"]["csv_exists"] = True

        df = pd.read_csv(self.csv_path)
        total_csv_products = len(df)
        report["checks"]["total_csv_products"] = total_csv_products

        # 2. Dynamic product count >= 100
        if total_csv_products < 100:
            err = f"Total product count {total_csv_products} is below required threshold of 100"
            report["errors"].append(err)
            raise QualityGateError(err)
        report["checks"]["min_100_products_passed"] = True

        # 3. Dynamic check: Exactly 5 required brands exist
        present_brands = sorted(list(df["brand"].unique()))
        expected_brands = sorted(REQUIRED_BRANDS)
        if present_brands != expected_brands:
            err = f"Brand mismatch. Expected: {expected_brands}, Found: {present_brands}"
            report["errors"].append(err)
            raise QualityGateError(err)
        report["checks"]["all_5_brands_present"] = True

        # 4. Each brand has >= ~20 products
        brand_counts = df["brand"].value_counts().to_dict()
        report["checks"]["brand_counts"] = brand_counts
        low_brands = [b for b, cnt in brand_counts.items() if cnt < 20]
        if low_brands:
            err = f"Brands with insufficient coverage (< 20 products): {low_brands}"
            report["errors"].append(err)
            raise QualityGateError(err)
        report["checks"]["each_brand_ge_20_products"] = True

        # 5. Check selling prices
        invalid_prices = df[df["selling_price"].isna() | (df["selling_price"] <= 0)]
        if len(invalid_prices) > 0:
            err = f"Found {len(invalid_prices)} products with invalid or non-positive selling prices"
            report["errors"].append(err)
            raise QualityGateError(err)
        report["checks"]["selling_prices_valid"] = True

        # 6. Canonical ID uniqueness
        if df["product_id"].duplicated().any():
            dup_cnt = df["product_id"].duplicated().sum()
            err = f"Found {dup_cnt} duplicate canonical product IDs in clean dataset"
            report["errors"].append(err)
            raise QualityGateError(err)
        report["checks"]["canonical_ids_unique"] = True

        # 7. Check SQLite database existence and row match
        if not os.path.exists(self.db_path):
            err = f"SQLite database not found at {self.db_path}"
            report["errors"].append(err)
            raise QualityGateError(err)

        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()
            db_row_count = cursor.execute("SELECT COUNT(*) FROM products;").fetchone()[0]
            report["checks"]["db_row_count"] = db_row_count

            if db_row_count != total_csv_products:
                err = f"Row mismatch between SQLite ({db_row_count}) and CSV ({total_csv_products})"
                report["errors"].append(err)
                raise QualityGateError(err)
            report["checks"]["db_matches_csv"] = True

            # 8. Check views existence
            views = [r[0] for r in cursor.execute("SELECT name FROM sqlite_master WHERE type='view';").fetchall()]
            required_views = ["vw_products_analytical", "vw_market_overview", "vw_brand_comparison", "vw_category_coverage"]
            for v in required_views:
                if v not in views:
                    err = f"Required analytical view {v} missing in database"
                    report["errors"].append(err)
                    raise QualityGateError(err)
            report["checks"]["required_views_operational"] = True

        finally:
            conn.close()

        report["passed"] = True
        logger.info("[VALIDATE] PASSED: All 8 data-quality gates successfully verified.")
        return report
