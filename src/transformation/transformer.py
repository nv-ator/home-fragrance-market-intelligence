import os
import pandas as pd
from typing import Dict, Any
from src.utils.logger import setup_logger

logger = setup_logger("transformer")

class AnalyticalTransformer:
    """
    Factual and deterministic transformation stage:
    Takes validated products_clean.csv and prepares the analytical dataset schema.
    Validates numeric types, enforces consistent null representations, and produces
    products_transformed.csv containing strictly observed and standardized factual metrics.
    No arbitrary business labels or speculative tier categorizations are introduced.
    """

    def __init__(self, input_csv_path: str = "data/processed/products_clean.csv", output_csv_path: str = "data/processed/products_transformed.csv"):
        self.input_csv_path = input_csv_path
        self.output_csv_path = output_csv_path

    def transform(self) -> pd.DataFrame:
        logger.info(f"[TRANSFORM] Reading cleaned dataset from {self.input_csv_path}")
        if not os.path.exists(self.input_csv_path):
            raise FileNotFoundError(f"Input cleaned CSV not found at {self.input_csv_path}")

        df = pd.read_csv(self.input_csv_path)

        # 1. Deterministic Type Normalization
        df["product_id"] = df["product_id"].astype(str)
        df["brand"] = df["brand"].astype(str)
        df["category"] = df["category"].astype(str)
        df["product_format"] = df["product_format"].astype(str)
        df["platform"] = df["platform"].astype(str)
        df["title_clean"] = df["title_clean"].astype(str)
        df["title_raw"] = df["title_raw"].astype(str)
        df["availability"] = df["availability"].astype(str)

        # Numeric Factual Fields
        df["selling_price"] = pd.to_numeric(df["selling_price"], errors="coerce")
        df["mrp"] = pd.to_numeric(df["mrp"], errors="coerce")
        df["discount_pct"] = pd.to_numeric(df["discount_pct"], errors="coerce")
        df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
        df["review_count"] = pd.to_numeric(df["review_count"], errors="coerce")
        for field in ["rating_source", "review_source", "seller"]:
            if field not in df.columns:
                df[field] = None
            df[field] = df[field].where(df[field].notna(), None)
        df["pack_count"] = pd.to_numeric(df["pack_count"], errors="coerce").fillna(1).astype(int)
        df["unit_quantity"] = pd.to_numeric(df["unit_quantity"], errors="coerce")
        df["total_quantity"] = pd.to_numeric(df["total_quantity"], errors="coerce")
        df["price_per_unit"] = pd.to_numeric(df["price_per_unit"], errors="coerce")
        df["price_per_100g"] = pd.to_numeric(df["price_per_100g"], errors="coerce")
        df["price_per_100ml"] = pd.to_numeric(df["price_per_100ml"], errors="coerce")

        # 2. Save strictly factual transformed analytical dataset
        os.makedirs(os.path.dirname(self.output_csv_path), exist_ok=True)
        df.to_csv(self.output_csv_path, index=False, encoding="utf-8")
        logger.info(f"[TRANSFORM] Transformed {len(df)} factual analytical records and saved to {self.output_csv_path}")

        return df
