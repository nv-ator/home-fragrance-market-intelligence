import os
import json
import pandas as pd
from typing import Dict, Any, List, Tuple
from datetime import datetime, timezone

from src.utils.logger import setup_logger
from src.cleaning.text_parsers import clean_text, parse_price, calculate_discount, parse_rating, parse_review_count
from src.cleaning.quantity_normalizer import parse_pack_quantity, calculate_normalized_prices
from src.cleaning.classifier import normalize_brand, evaluate_home_fragrance_scope, classify_category_and_format

logger = setup_logger("cleaning_pipeline")

class CleaningPipeline:
    """End-to-end cleaning, validation, and standardization pipeline."""

    def __init__(self, raw_data_path: str, output_dir: str = "data/processed"):
        self.raw_data_path = raw_data_path
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

        self.stats = {
            "total_raw_candidates": 0,
            "validated_products": 0,
            "rejections": {},
            "duplicates": 0,
            "by_brand": {},
            "missing_fields": {
                "selling_price": 0,
                "mrp": 0,
                "discount": 0,
                "rating": 0,
                "review_count": 0,
                "quantity": 0
            },
            "normalization_coverage": {
                "price_per_unit": 0,
                "price_per_100g": 0,
                "price_per_100ml": 0
            }
        }

    def _determine_canonical_id(self, item: Dict[str, Any]) -> str:
        """
        Determines canonical product ID strategy:
        - Amazon: ASIN
        - AromaPure: Product ID (or ProductID_VariantID if variant exists)
        """
        asin = item.get("asin")
        if asin and str(asin).strip():
            return str(asin).strip().upper()

        prod_id = item.get("product_id")
        if prod_id and str(prod_id).strip():
            return str(prod_id).strip()

        sku = item.get("sku")
        if sku and str(sku).strip():
            return str(sku).strip()

        # Fallback to normalized product URL
        p_url = item.get("product_url")
        if p_url and str(p_url).strip():
            return str(p_url).strip().lower()

        return ""

    def run(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        logger.info(f"Loading raw candidates from {self.raw_data_path}")
        with open(self.raw_data_path, "r", encoding="utf-8") as f:
            raw_items = json.load(f)

        self.stats["total_raw_candidates"] = len(raw_items)
        logger.info(f"Loaded {len(raw_items)} raw candidate records")

        valid_records = []
        rejected_records = []
        seen_canonical_keys = set()

        for item in raw_items:
            raw_title = item.get("product_name") or ""
            clean_title = clean_text(raw_title)

            # 1. Identity validation
            canonical_id = self._determine_canonical_id(item)
            if not canonical_id:
                rejection_reason = "missing_product_id"
                self.stats["rejections"][rejection_reason] = self.stats["rejections"].get(rejection_reason, 0) + 1
                rejected_records.append({**item, "rejection_reason": rejection_reason})
                continue

            # 2. Brand validation
            norm_brand, brand_err = normalize_brand(item.get("brand"), raw_title)
            if brand_err:
                self.stats["rejections"][brand_err] = self.stats["rejections"].get(brand_err, 0) + 1
                rejected_records.append({**item, "rejection_reason": brand_err})
                continue

            # 3. Product Scope validation (Home fragrance vs car-only / cleaners)
            in_scope, scope_err = evaluate_home_fragrance_scope(raw_title, item.get("product_type_raw"))
            if not in_scope:
                self.stats["rejections"][scope_err] = self.stats["rejections"].get(scope_err, 0) + 1
                rejected_records.append({**item, "rejection_reason": scope_err})
                continue

            # 4. Price validation
            selling_price = parse_price(item.get("price_raw"))
            if selling_price is None or selling_price <= 0:
                rejection_reason = "invalid_or_zero_price"
                self.stats["rejections"][rejection_reason] = self.stats["rejections"].get(rejection_reason, 0) + 1
                rejected_records.append({**item, "rejection_reason": rejection_reason})
                continue

            # 5. Deduplication using (brand, platform, canonical_id)
            platform = "AromaPure Official" if "aromapure" in str(item.get("source", "")).lower() else "Amazon India"
            dedup_key = f"{norm_brand}|{platform}|{canonical_id}"
            if dedup_key in seen_canonical_keys:
                self.stats["duplicates"] += 1
                rejection_reason = "duplicate_canonical_product"
                self.stats["rejections"][rejection_reason] = self.stats["rejections"].get(rejection_reason, 0) + 1
                rejected_records.append({**item, "rejection_reason": rejection_reason})
                continue
            seen_canonical_keys.add(dedup_key)

            # --- FIELD STANDARDIZATION ---
            mrp = parse_price(item.get("mrp_raw"))
            discount_pct, discount_source = calculate_discount(selling_price, mrp, item.get("discount_raw"))
            rating = parse_rating(item.get("rating_raw"))
            review_count = parse_review_count(item.get("review_count_raw"))

            # Pack quantity normalization
            qty_info = parse_pack_quantity(clean_title or raw_title, item.get("pack_size_raw"))
            norm_prices = calculate_normalized_prices(selling_price, qty_info)

            # Category & format normalization
            category, product_format = classify_category_and_format(clean_title or raw_title, item.get("product_type_raw"))

            # Availability
            raw_avail = str(item.get("availability_raw", "")).lower()
            if "in stock" in raw_avail:
                availability = "In Stock"
            elif "out of stock" in raw_avail:
                availability = "Out of Stock"
            else:
                availability = "In Stock" if item.get("price_raw") else "Unavailable"

            clean_record = {
                "product_id": canonical_id,
                "brand": norm_brand,
                "platform": platform,
                "title_clean": clean_title,
                "title_raw": raw_title,
                "category": category,
                "product_format": product_format,
                "selling_price": selling_price,
                "mrp": mrp,
                "discount_pct": discount_pct,
                "discount_source": discount_source,
                "rating": rating,
                "review_count": review_count,
                "rating_source": item.get("rating_source") if rating is not None else None,
                "review_source": item.get("review_source") if review_count is not None else None,
                "seller": item.get("seller_raw") or None,
                "availability": availability,
                "pack_count": qty_info["pack_count"],
                "unit_quantity": qty_info["unit_quantity"],
                "unit": qty_info["unit"],
                "total_quantity": qty_info["total_quantity"],
                "price_per_unit": norm_prices["price_per_unit"],
                "price_per_100g": norm_prices["price_per_100g"],
                "price_per_100ml": norm_prices["price_per_100ml"],
                "product_url": item.get("product_url"),
                "scraped_at": item.get("scraped_at"),
                "raw_reference": item.get("raw_page_reference") or item.get("raw_source_reference")
            }
            valid_records.append(clean_record)

            # Update brand stats
            self.stats["by_brand"][norm_brand] = self.stats["by_brand"].get(norm_brand, 0) + 1

            # Track missing fields
            if mrp is None:
                self.stats["missing_fields"]["mrp"] += 1
            if discount_pct is None:
                self.stats["missing_fields"]["discount"] += 1
            if rating is None:
                self.stats["missing_fields"]["rating"] += 1
            if review_count is None:
                self.stats["missing_fields"]["review_count"] += 1
            if qty_info["total_quantity"] is None:
                self.stats["missing_fields"]["quantity"] += 1

            # Track normalization coverage
            if norm_prices["price_per_unit"] is not None:
                self.stats["normalization_coverage"]["price_per_unit"] += 1
            if norm_prices["price_per_100g"] is not None:
                self.stats["normalization_coverage"]["price_per_100g"] += 1
            if norm_prices["price_per_100ml"] is not None:
                self.stats["normalization_coverage"]["price_per_100ml"] += 1

        self.stats["validated_products"] = len(valid_records)

        df_clean = pd.DataFrame(valid_records)
        df_rejected = pd.DataFrame(rejected_records)

        # Save to data/processed
        clean_csv_path = os.path.join(self.output_dir, "products_clean.csv")
        df_clean.to_csv(clean_csv_path, index=False, encoding="utf-8")
        logger.info(f"Saved {len(df_clean)} validated products to {clean_csv_path}")

        rejected_csv_path = os.path.join(self.output_dir, "products_rejected.csv")
        df_rejected.to_csv(rejected_csv_path, index=False, encoding="utf-8")
        logger.info(f"Saved {len(df_rejected)} rejected records to {rejected_csv_path}")

        return df_clean, df_rejected
