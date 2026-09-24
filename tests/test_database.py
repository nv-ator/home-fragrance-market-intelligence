import os
import sqlite3
import pytest
import pandas as pd
from src.database.database import DatabaseLoader

DB_PATH = "data/market_intelligence.db"
CSV_PATH = "data/processed/products_clean.csv"

@pytest.fixture(scope="session")
def db_conn():
    assert os.path.exists(DB_PATH), "Database file must exist"
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()

def test_database_tables_exist(db_conn):
    cursor = db_conn.cursor()
    tables = [r[0] for r in cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()]
    assert "products" in tables
    assert "brands" in tables
    assert "categories" in tables
    assert "data_sources" in tables

def test_database_views_exist(db_conn):
    cursor = db_conn.cursor()
    views = [r[0] for r in cursor.execute("SELECT name FROM sqlite_master WHERE type='view';").fetchall()]
    assert "vw_products_analytical" in views
    assert "vw_market_overview" in views
    assert "vw_brand_comparison" in views
    assert "vw_category_coverage" in views

def test_product_count_matches_csv(db_conn):
    cursor = db_conn.cursor()
    db_count = cursor.execute("SELECT COUNT(*) FROM products;").fetchone()[0]
    df_csv = pd.read_csv(CSV_PATH)
    assert db_count == len(df_csv)
    assert db_count == 767

def test_five_brands_exist_and_match(db_conn):
    cursor = db_conn.cursor()
    brands = [r[0] for r in cursor.execute("SELECT brand_name FROM brands ORDER BY brand_name;").fetchall()]
    expected_brands = sorted(["AromaPure", "Odonil", "Godrej aer", "Air Wick", "Ambi Pur"])
    assert brands == expected_brands

def test_no_duplicate_canonical_ids(db_conn):
    cursor = db_conn.cursor()
    total_rows = cursor.execute("SELECT COUNT(*) FROM products;").fetchone()[0]
    unique_ids = cursor.execute("SELECT COUNT(DISTINCT canonical_id) FROM products;").fetchone()[0]
    assert total_rows == unique_ids

def test_null_values_preserved(db_conn):
    cursor = db_conn.cursor()
    # Check that AromaPure products retain NULL rating rather than 0.0
    null_ratings = cursor.execute("""
        SELECT COUNT(*) FROM products p
        JOIN brands b ON p.brand_id = b.brand_id
        WHERE b.brand_name = 'AromaPure' AND p.rating IS NULL;
    """).fetchone()[0]
    aromapure_total = cursor.execute("""
        SELECT COUNT(*) FROM products p
        JOIN brands b ON p.brand_id = b.brand_id
        WHERE b.brand_name = 'AromaPure';
    """).fetchone()[0]
    assert null_ratings == aromapure_total
    assert null_ratings == 360

def test_numeric_ranges_and_constraints(db_conn):
    cursor = db_conn.cursor()
    # Price positive
    invalid_prices = cursor.execute("SELECT COUNT(*) FROM products WHERE selling_price <= 0 OR selling_price IS NULL;").fetchone()[0]
    assert invalid_prices == 0

    # Rating range 0.0 to 5.0 when present
    invalid_ratings = cursor.execute("SELECT COUNT(*) FROM products WHERE rating IS NOT NULL AND (rating < 0.0 OR rating > 5.0);").fetchone()[0]
    assert invalid_ratings == 0

    # Review count non-negative when present
    invalid_reviews = cursor.execute("SELECT COUNT(*) FROM products WHERE review_count IS NOT NULL AND review_count < 0;").fetchone()[0]
    assert invalid_reviews == 0

def test_format_specific_normalized_prices(db_conn):
    cursor = db_conn.cursor()
    # Price per 100g only on mass based
    mass_check = cursor.execute("SELECT COUNT(*) FROM products WHERE price_per_100g IS NOT NULL AND unit != 'g';").fetchone()[0]
    assert mass_check == 0

    # Price per 100ml only on volume based
    vol_check = cursor.execute("SELECT COUNT(*) FROM products WHERE price_per_100ml IS NOT NULL AND unit != 'ml';").fetchone()[0]
    assert vol_check == 0
