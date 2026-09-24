import sqlite3
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from api.database import get_db
from api.schemas import BrandItem, BrandComparisonItem, BrandDetailResponse

router = APIRouter(prefix="/api/brands", tags=["Brands"])

@router.get("", response_model=List[BrandItem])
def list_brands(db: sqlite3.Connection = Depends(get_db)):
    """Returns the list of tracked competitor brands with observed catalogue counts."""
    cursor = db.cursor()
    rows = cursor.execute("""
        SELECT b.brand_id, b.brand_name, COUNT(p.product_id) AS product_count
        FROM brands b
        LEFT JOIN products p ON b.brand_id = p.brand_id
        GROUP BY b.brand_id, b.brand_name
        ORDER BY product_count DESC;
    """).fetchall()
    return [BrandItem(brand_id=r["brand_id"], brand_name=r["brand_name"], product_count=r["product_count"]) for r in rows]

@router.get("/comparison", response_model=List[BrandComparisonItem])
def get_brand_comparison(db: sqlite3.Connection = Depends(get_db)):
    """
    Returns side-by-side empirical benchmark metrics across all 5 brands.
    Includes exact median price calculated via window functions.
    """
    cursor = db.cursor()
    total_products = cursor.execute("SELECT COUNT(*) FROM products;").fetchone()[0] or 1

    # 1. Medians per brand
    medians = {}
    median_rows = cursor.execute("""
        WITH BrandRankedPrices AS (
            SELECT
                b.brand_name,
                p.selling_price,
                ROW_NUMBER() OVER (PARTITION BY b.brand_name ORDER BY p.selling_price) AS row_num,
                COUNT(*) OVER (PARTITION BY b.brand_name) AS total_count
            FROM products p
            JOIN brands b ON p.brand_id = b.brand_id
            WHERE p.selling_price IS NOT NULL
        )
        SELECT brand_name, ROUND(AVG(selling_price), 2) AS median_price
        FROM BrandRankedPrices
        WHERE row_num IN ((total_count + 1) / 2, (total_count + 2) / 2)
        GROUP BY brand_name;
    """).fetchall()
    for m in median_rows:
        medians[m["brand_name"]] = m["median_price"]

    # 2. Benchmark aggregates
    rows = cursor.execute("""
        SELECT
            b.brand_name AS brand,
            COUNT(p.product_id) AS product_count,
            ROUND(AVG(p.selling_price), 2) AS average_price,
            ROUND(AVG(p.rating), 2) AS average_rating,
            COALESCE(SUM(p.review_count), 0) AS total_reviews,
            ROUND(AVG(p.discount_pct), 2) AS average_discount,
            COUNT(DISTINCT p.category_id) AS category_count,
            COUNT(DISTINCT p.platform) AS platform_count
        FROM brands b
        JOIN products p ON b.brand_id = p.brand_id
        GROUP BY b.brand_name
        ORDER BY product_count DESC;
    """).fetchall()

    results = []
    for r in rows:
        b_name = r["brand"]
        results.append(BrandComparisonItem(
            brand=b_name,
            product_count=r["product_count"],
            share_of_collected_assortment_pct=round((r["product_count"] * 100.0) / total_products, 2),
            average_price=r["average_price"] or 0.0,
            median_price=medians.get(b_name, r["average_price"] or 0.0),
            average_rating=r["average_rating"],
            total_reviews=r["total_reviews"],
            average_discount=r["average_discount"],
            category_count=r["category_count"],
            platform_count=r["platform_count"]
        ))
    return results

@router.get("/{brand_name}", response_model=BrandDetailResponse)
def get_brand_detail(brand_name: str, db: sqlite3.Connection = Depends(get_db)):
    """Returns detailed factual portfolio diagnostics for a specific brand."""
    cursor = db.cursor()
    brand_row = cursor.execute("SELECT brand_id, brand_name FROM brands WHERE LOWER(brand_name) = LOWER(?);", (brand_name,)).fetchone()
    if not brand_row:
        raise HTTPException(status_code=404, detail=f"Brand '{brand_name}' not found")

    b_id = brand_row["brand_id"]
    canonical_brand = brand_row["brand_name"]
    total_market_products = cursor.execute("SELECT COUNT(*) FROM products;").fetchone()[0] or 1

    # Product count
    prod_cnt = cursor.execute("SELECT COUNT(*) FROM products WHERE brand_id = ?;", (b_id,)).fetchone()[0]

    # Category distribution
    cat_dist = []
    for cr in cursor.execute("""
        SELECT c.category_name, COUNT(p.product_id) AS cnt, ROUND(AVG(p.selling_price), 2) AS avg_price
        FROM products p
        JOIN categories c ON p.category_id = c.category_id
        WHERE p.brand_id = ?
        GROUP BY c.category_name
        ORDER BY cnt DESC;
    """, (b_id,)).fetchall():
        cat_dist.append({
            "category": cr["category_name"],
            "count": cr["cnt"],
            "pct_of_brand": round((cr["cnt"] * 100.0) / prod_cnt, 2) if prod_cnt > 0 else 0.0,
            "average_price": cr["avg_price"]
        })

    # Platform distribution
    plat_dist = []
    for pr in cursor.execute("""
        SELECT platform, COUNT(*) as cnt
        FROM products WHERE brand_id = ? GROUP BY platform ORDER BY cnt DESC;
    """, (b_id,)).fetchall():
        plat_dist.append({
            "platform": pr["platform"],
            "count": pr["cnt"],
            "pct_of_brand": round((pr["cnt"] * 100.0) / prod_cnt, 2) if prod_cnt > 0 else 0.0
        })

    # Price stats
    price_stats_row = cursor.execute("""
        SELECT
            ROUND(MIN(selling_price), 2) AS min_price,
            ROUND(MAX(selling_price), 2) AS max_price,
            ROUND(AVG(selling_price), 2) AS avg_price
        FROM products WHERE brand_id = ?;
    """, (b_id,)).fetchone()

    # Brand median
    b_median_row = cursor.execute("""
        WITH BrandRankedPrices AS (
            SELECT
                selling_price,
                ROW_NUMBER() OVER (ORDER BY selling_price) AS row_num,
                COUNT(*) OVER () AS total_count
            FROM products
            WHERE brand_id = ? AND selling_price IS NOT NULL
        )
        SELECT ROUND(AVG(selling_price), 2) AS median_price
        FROM BrandRankedPrices
        WHERE row_num IN ((total_count + 1) / 2, (total_count + 2) / 2);
    """, (b_id,)).fetchone()

    price_stats = {
        "min_price": price_stats_row["min_price"],
        "max_price": price_stats_row["max_price"],
        "avg_price": price_stats_row["avg_price"],
        "median_price": b_median_row["median_price"] if b_median_row else price_stats_row["avg_price"]
    }

    # Rating stats
    rating_row = cursor.execute("""
        SELECT
            COUNT(rating) AS rated_products_count,
            ROUND(AVG(rating), 2) AS avg_rating,
            COALESCE(SUM(review_count), 0) AS total_reviews,
            ROUND(AVG(review_count), 2) AS avg_reviews_per_rated_product
        FROM products WHERE brand_id = ? AND rating IS NOT NULL;
    """, (b_id,)).fetchone()
    rating_stats = {
        "rated_products_count": rating_row["rated_products_count"],
        "avg_rating": rating_row["avg_rating"],
        "total_reviews": rating_row["total_reviews"],
        "avg_reviews": rating_row["avg_reviews_per_rated_product"]
    }

    # Discount stats
    discount_row = cursor.execute("""
        SELECT
            COUNT(discount_pct) AS discounted_count,
            ROUND(AVG(discount_pct), 2) AS avg_discount_pct,
            ROUND(MAX(discount_pct), 2) AS max_discount_pct
        FROM products WHERE brand_id = ? AND discount_pct IS NOT NULL;
    """, (b_id,)).fetchone()
    discount_stats = {
        "discounted_products_count": discount_row["discounted_count"],
        "avg_discount_pct": discount_row["avg_discount_pct"],
        "max_discount_pct": discount_row["max_discount_pct"]
    }

    # Quantity stats
    qty_row = cursor.execute("""
        SELECT
            COUNT(total_quantity) AS products_with_qty,
            ROUND(AVG(price_per_unit), 2) AS avg_price_per_unit,
            ROUND(AVG(price_per_100ml), 2) AS avg_price_per_100ml,
            ROUND(AVG(price_per_100g), 2) AS avg_price_per_100g
        FROM products WHERE brand_id = ?;
    """, (b_id,)).fetchone()
    quantity_stats = {
        "products_with_standardized_qty": qty_row["products_with_qty"],
        "avg_price_per_unit": qty_row["avg_price_per_unit"],
        "avg_price_per_100ml": qty_row["avg_price_per_100ml"],
        "avg_price_per_100g": qty_row["avg_price_per_100g"]
    }

    return BrandDetailResponse(
        brand=canonical_brand,
        product_count=prod_cnt,
        share_of_collected_assortment_pct=round((prod_cnt * 100.0) / total_market_products, 2),
        category_distribution=cat_dist,
        platform_distribution=plat_dist,
        price_statistics=price_stats,
        rating_statistics=rating_stats,
        discount_statistics=discount_stats,
        quantity_statistics=quantity_stats
    )
