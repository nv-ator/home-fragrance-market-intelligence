import sqlite3
from fastapi import APIRouter, Depends
from typing import Dict, Any, List
from api.database import get_db
from api.schemas import MarketOverviewResponse, CountShareItem

router = APIRouter(prefix="/api/overview", tags=["Market Overview"])

@router.get("", response_model=MarketOverviewResponse)
def get_market_overview(db: sqlite3.Connection = Depends(get_db)):
    """Returns top-level macro market indicators, averages, and distribution breakdowns."""
    cursor = db.cursor()

    # 1. Macro KPIs from view
    kpi_row = cursor.execute("""
        SELECT
            COUNT(*) AS total_products,
            COUNT(DISTINCT brand) AS total_brands,
            ROUND(AVG(selling_price), 2) AS average_price,
            ROUND(AVG(rating), 2) AS average_rating,
            ROUND(AVG(review_count), 2) AS average_review_count,
            ROUND(AVG(discount_pct), 2) AS average_discount
        FROM vw_products_analytical;
    """).fetchone()

    total_products = kpi_row["total_products"] or 0

    # 2. Exact Median Selling Price via Window Function
    median_row = cursor.execute("""
        WITH RankedPrices AS (
            SELECT
                selling_price,
                ROW_NUMBER() OVER (ORDER BY selling_price) AS row_num,
                COUNT(*) OVER () AS total_count
            FROM vw_products_analytical
            WHERE selling_price IS NOT NULL
        )
        SELECT ROUND(AVG(selling_price), 2) AS median_price
        FROM RankedPrices
        WHERE row_num IN ((total_count + 1) / 2, (total_count + 2) / 2);
    """).fetchone()
    median_price = median_row["median_price"] or 0.0

    # 3. Products by Brand
    by_brand = []
    for r in cursor.execute("""
        SELECT brand, COUNT(*) AS cnt
        FROM vw_products_analytical
        GROUP BY brand
        ORDER BY cnt DESC;
    """).fetchall():
        by_brand.append(CountShareItem(
            name=r["brand"],
            product_count=r["cnt"],
            pct_share=round((r["cnt"] * 100.0) / total_products, 2) if total_products > 0 else 0.0
        ))

    # 4. Products by Platform
    by_platform = []
    for r in cursor.execute("""
        SELECT platform, COUNT(*) AS cnt
        FROM vw_products_analytical
        GROUP BY platform
        ORDER BY cnt DESC;
    """).fetchall():
        by_platform.append(CountShareItem(
            name=r["platform"],
            product_count=r["cnt"],
            pct_share=round((r["cnt"] * 100.0) / total_products, 2) if total_products > 0 else 0.0
        ))

    # 5. Products by Category
    by_category = []
    for r in cursor.execute("""
        SELECT category, COUNT(*) AS cnt
        FROM vw_products_analytical
        GROUP BY category
        ORDER BY cnt DESC;
    """).fetchall():
        by_category.append(CountShareItem(
            name=r["category"],
            product_count=r["cnt"],
            pct_share=round((r["cnt"] * 100.0) / total_products, 2) if total_products > 0 else 0.0
        ))

    # 6. Price Distribution
    price_brackets = [
        ("Under ₹250", "selling_price < 250"),
        ("₹250 - ₹499", "selling_price >= 250 AND selling_price < 500"),
        ("₹500 - ₹999", "selling_price >= 500 AND selling_price < 1000"),
        ("₹1,000 - ₹1,999", "selling_price >= 1000 AND selling_price < 2000"),
        ("₹2,000+", "selling_price >= 2000")
    ]
    price_dist = []
    for label, cond in price_brackets:
        cnt = cursor.execute(f"SELECT COUNT(*) FROM vw_products_analytical WHERE {cond};").fetchone()[0]
        price_dist.append(CountShareItem(
            name=label,
            product_count=cnt,
            pct_share=round((cnt * 100.0) / total_products, 2) if total_products > 0 else 0.0
        ))

    return MarketOverviewResponse(
        total_products=total_products,
        total_brands=kpi_row["total_brands"] or 0,
        average_price=kpi_row["average_price"] or 0.0,
        median_price=median_price,
        average_rating=kpi_row["average_rating"],
        average_review_count=kpi_row["average_review_count"],
        average_discount=kpi_row["average_discount"],
        products_by_brand=by_brand,
        products_by_platform=by_platform,
        products_by_category=by_category,
        price_distribution=price_dist
    )
