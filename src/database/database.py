import os
import sqlite3
import pandas as pd
from typing import Dict, Any, Tuple
from src.utils.logger import setup_logger

logger = setup_logger("database_loader")

class DatabaseLoader:
    """Manages the creation, population, and validation of the SQLite analytical database."""

    def __init__(self, db_path: str = "data/market_intelligence.db", schema_path: str = "sql/schema.sql"):
        self.db_path = db_path
        self.schema_path = schema_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.row_factory = sqlite3.Row
        return conn

    def init_schema(self, rebuild: bool = False):
        """Initializes database tables, indexes, and views from schema.sql."""
        if rebuild and os.path.exists(self.db_path):
            logger.info(f"Rebuilding database: removing existing {self.db_path}")
            os.remove(self.db_path)

        with open(self.schema_path, "r", encoding="utf-8") as f:
            schema_sql = f.read()

        conn = self.get_connection()
        try:
            with conn:
                conn.executescript(schema_sql)
                existing_columns = {
                    row["name"] for row in conn.execute("PRAGMA table_info(products);").fetchall()
                }
                for column in ("rating_source", "review_source", "seller"):
                    if column not in existing_columns:
                        conn.execute(f"ALTER TABLE products ADD COLUMN {column} TEXT;")
            logger.info(f"Initialized database schema and views at {self.db_path}")
        finally:
            conn.close()

    def load_processed_csv(self, csv_path: str = "data/processed/products_clean.csv") -> int:
        """Loads validated products from CSV into normalized SQLite tables preserving exact NULLs."""
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"Clean CSV file not found at {csv_path}")

        df = pd.read_csv(csv_path)
        logger.info(f"Read {len(df)} validated products from {csv_path}")

        # Ensure correct Python None for all NaN values
        df = df.where(pd.notnull(df), None)

        conn = self.get_connection()
        try:
            cursor = conn.cursor()

            # 1. Populate Dimension: brands
            unique_brands = df["brand"].dropna().unique()
            for b in unique_brands:
                cursor.execute(
                    "INSERT OR IGNORE INTO brands (brand_name) VALUES (?);",
                    (str(b),)
                )

            # 2. Populate Dimension: categories
            cat_format_pairs = df[["category", "product_format"]].drop_duplicates().values
            for cat, fmt in cat_format_pairs:
                cursor.execute(
                    "INSERT OR IGNORE INTO categories (category_name, product_format) VALUES (?, ?);",
                    (str(cat), str(fmt) if fmt else None)
                )

            # 3. Populate Dimension: data_sources
            platforms = df["platform"].unique()
            for p in platforms:
                s_name = "AromaPure Official Catalogue" if "AromaPure" in str(p) else "Amazon India Search"
                s_type = "JSON_REST_API" if "AromaPure" in str(p) else "HTML_PUBLIC_SEARCH"
                cursor.execute(
                    "INSERT OR IGNORE INTO data_sources (source_name, platform, source_type) VALUES (?, ?, ?);",
                    (s_name, str(p), s_type)
                )

            # Query dimension IDs for fast lookup
            brand_map = {row["brand_name"]: row["brand_id"] for row in cursor.execute("SELECT brand_id, brand_name FROM brands;").fetchall()}
            cat_map = {row["category_name"]: row["category_id"] for row in cursor.execute("SELECT category_id, category_name FROM categories;").fetchall()}
            source_map = {row["platform"]: row["source_id"] for row in cursor.execute("SELECT source_id, platform FROM data_sources;").fetchall()}

            # 4. Insert Products
            inserted_count = 0
            for _, row in df.iterrows():
                brand_id = brand_map.get(row["brand"])
                category_id = cat_map.get(row["category"])
                source_id = source_map.get(row["platform"])

                def safe_int(v):
                    return int(v) if v is not None and not pd.isna(v) else None

                def safe_float(v):
                    return float(v) if v is not None and not pd.isna(v) else None

                def safe_str(v):
                    return str(v) if v is not None and not pd.isna(v) else None

                cursor.execute("""
                    INSERT OR REPLACE INTO products (
                        canonical_id, brand_id, category_id, source_id,
                        title_clean, title_raw, platform, product_url,
                        selling_price, mrp, discount_pct, discount_source,
                        rating, review_count, rating_source, review_source, seller,
                        availability, pack_count,
                        unit_quantity, unit, total_quantity,
                        price_per_unit, price_per_100g, price_per_100ml,
                        scraped_at, raw_reference
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                """, (
                    str(row["product_id"]),
                    brand_id,
                    category_id,
                    source_id,
                    str(row["title_clean"]),
                    str(row["title_raw"]),
                    str(row["platform"]),
                    safe_str(row["product_url"]),
                    safe_float(row["selling_price"]),
                    safe_float(row["mrp"]),
                    safe_float(row["discount_pct"]),
                    safe_str(row["discount_source"]),
                    safe_float(row["rating"]),
                    safe_int(row["review_count"]),
                    safe_str(row.get("rating_source")),
                    safe_str(row.get("review_source")),
                    safe_str(row.get("seller")),
                    str(row["availability"]),
                    safe_int(row["pack_count"]) or 1,
                    safe_float(row["unit_quantity"]),
                    safe_str(row["unit"]),
                    safe_float(row["total_quantity"]),
                    safe_float(row["price_per_unit"]),
                    safe_float(row["price_per_100g"]),
                    safe_float(row["price_per_100ml"]),
                    safe_str(row["scraped_at"]),
                    safe_str(row["raw_reference"])
                ))
                inserted_count += 1

            conn.commit()
            logger.info(f"Successfully loaded {inserted_count} products into SQLite database.")
            return inserted_count
        finally:
            conn.close()

    def validate_database(self) -> Dict[str, Any]:
        """Runs validation checks against the loaded SQLite database."""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()

            total_products = cursor.execute("SELECT COUNT(*) FROM products;").fetchone()[0]
            unique_canonical = cursor.execute("SELECT COUNT(DISTINCT canonical_id) FROM products;").fetchone()[0]

            # Brand breakdown
            brand_counts = {}
            for r in cursor.execute("""
                SELECT b.brand_name, COUNT(p.product_id) AS cnt
                FROM products p
                JOIN brands b ON p.brand_id = b.brand_id
                GROUP BY b.brand_name;
            """).fetchall():
                brand_counts[r["brand_name"]] = r["cnt"]

            # Platform breakdown
            platform_counts = {}
            for r in cursor.execute("SELECT platform, COUNT(*) as cnt FROM products GROUP BY platform;").fetchall():
                platform_counts[r["platform"]] = r["cnt"]

            # Category breakdown
            cat_counts = {}
            for r in cursor.execute("""
                SELECT c.category_name, COUNT(p.product_id) AS cnt
                FROM products p
                JOIN categories c ON p.category_id = c.category_id
                GROUP BY c.category_name;
            """).fetchall():
                cat_counts[r["category_name"]] = r["cnt"]

            # Metric counts
            valid_price = cursor.execute("SELECT COUNT(*) FROM products WHERE selling_price IS NOT NULL AND selling_price > 0;").fetchone()[0]
            with_ratings = cursor.execute("SELECT COUNT(*) FROM products WHERE rating IS NOT NULL;").fetchone()[0]
            with_reviews = cursor.execute("SELECT COUNT(*) FROM products WHERE review_count IS NOT NULL;").fetchone()[0]
            with_discount = cursor.execute("SELECT COUNT(*) FROM products WHERE discount_pct IS NOT NULL;").fetchone()[0]
            with_ppu = cursor.execute("SELECT COUNT(*) FROM products WHERE price_per_unit IS NOT NULL;").fetchone()[0]
            with_pp100g = cursor.execute("SELECT COUNT(*) FROM products WHERE price_per_100g IS NOT NULL;").fetchone()[0]
            with_pp100ml = cursor.execute("SELECT COUNT(*) FROM products WHERE price_per_100ml IS NOT NULL;").fetchone()[0]

            return {
                "total_products": total_products,
                "unique_canonical": unique_canonical,
                "brands": brand_counts,
                "platforms": platform_counts,
                "categories": cat_counts,
                "valid_price_count": valid_price,
                "rating_count": with_ratings,
                "review_count": with_reviews,
                "discount_count": with_discount,
                "price_per_unit_count": with_ppu,
                "price_per_100g_count": with_pp100g,
                "price_per_100ml_count": with_pp100ml
            }
        finally:
            conn.close()
