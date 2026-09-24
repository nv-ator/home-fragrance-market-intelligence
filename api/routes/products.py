import sqlite3
import math
from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Optional, List
from api.database import get_db
from api.schemas import PaginatedProductsResponse, ProductItem

router = APIRouter(prefix="/api/products", tags=["Products"])

@router.get("", response_model=PaginatedProductsResponse)
def list_products(
    brand: Optional[str] = Query(None, description="Filter by brand name"),
    platform: Optional[str] = Query(None, description="Filter by platform"),
    category: Optional[str] = Query(None, description="Filter by category"),
    product_format: Optional[str] = Query(None, description="Filter by product format"),
    product_type: Optional[str] = Query(None, description="Alias for product format"),
    search: Optional[str] = Query(None, description="Keyword search in title"),
    availability: Optional[str] = Query(None, description="Filter by stock availability"),
    min_price: Optional[float] = Query(None, description="Minimum selling price in INR"),
    max_price: Optional[float] = Query(None, description="Maximum selling price in INR"),
    min_rating: Optional[float] = Query(None, description="Minimum star rating (0-5)"),
    max_rating: Optional[float] = Query(None, description="Maximum star rating (0-5)"),
    min_quantity: Optional[float] = Query(None, description="Minimum total standardized quantity"),
    max_quantity: Optional[float] = Query(None, description="Maximum total standardized quantity"),
    pack_count: Optional[int] = Query(None, description="Filter by exact pack count/size"),
    pack_size: Optional[int] = Query(None, description="Alias for pack_count"),
    page: int = Query(1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(50, ge=1, le=200, description="Items per page (max 200)"),
    limit: Optional[int] = Query(None, description="Alias for page_size"),
    db: sqlite3.Connection = Depends(get_db)
):
    """Returns paginated, multi-attribute filterable list of validated analytical products."""
    cursor = db.cursor()

    effective_page_size = limit if limit is not None else page_size
    effective_format = product_format or product_type
    effective_pack = pack_count if pack_count is not None else pack_size

    conditions = []
    params = []

    if search:
        conditions.append("(LOWER(p.title_clean) LIKE LOWER(?) OR LOWER(p.title_raw) LIKE LOWER(?))")
        params.extend([f"%{search}%", f"%{search}%"])
    if brand:
        conditions.append("LOWER(b.brand_name) = LOWER(?)")
        params.append(brand)
    if platform:
        conditions.append("LOWER(p.platform) = LOWER(?)")
        params.append(platform)
    if category:
        conditions.append("LOWER(c.category_name) = LOWER(?)")
        params.append(category)
    if effective_format:
        conditions.append("LOWER(c.product_format) = LOWER(?)")
        params.append(effective_format)

    if availability:
        conditions.append("LOWER(p.availability) = LOWER(?)")
        params.append(availability)
    if min_price is not None:
        if min_price < 0:
            raise HTTPException(status_code=400, detail="min_price cannot be negative")
        conditions.append("p.selling_price >= ?")
        params.append(min_price)
    if max_price is not None:
        conditions.append("p.selling_price <= ?")
        params.append(max_price)
    if min_rating is not None:
        if min_rating < 0 or min_rating > 5:
            raise HTTPException(status_code=400, detail="min_rating must be between 0 and 5")
        conditions.append("p.rating >= ?")
        params.append(min_rating)
    if max_rating is not None:
        conditions.append("p.rating <= ?")
        params.append(max_rating)
    if min_quantity is not None:
        conditions.append("p.total_quantity >= ?")
        params.append(min_quantity)
    if max_quantity is not None:
        conditions.append("p.total_quantity <= ?")
        params.append(max_quantity)
    if effective_pack is not None:
        conditions.append("p.pack_count = ?")
        params.append(effective_pack)

    where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""

    # Count total matching
    count_sql = f"""
        SELECT COUNT(p.product_id)
        FROM products p
        JOIN brands b ON p.brand_id = b.brand_id
        JOIN categories c ON p.category_id = c.category_id
        {where_clause};
    """
    total = cursor.execute(count_sql, params).fetchone()[0]

    offset = (page - 1) * effective_page_size
    query_params = list(params) + [effective_page_size, offset]

    query_sql = f"""
        SELECT
            p.product_id,
            p.canonical_id,
            b.brand_name AS brand,
            c.category_name AS category,
            c.product_format,
            p.platform,
            p.title_clean,
            p.title_raw,
            p.selling_price,
            p.mrp,
            p.discount_pct,
            p.discount_source,
            p.rating,
            p.review_count,
            p.rating_source,
            p.review_source,
            p.seller,
            p.availability,
            p.pack_count,
            p.unit_quantity,
            p.unit,
            p.total_quantity,
            p.price_per_unit,
            p.price_per_100g,
            p.price_per_100ml,
            p.product_url,
            p.scraped_at,
            p.raw_reference
        FROM products p
        JOIN brands b ON p.brand_id = b.brand_id
        JOIN categories c ON p.category_id = c.category_id
        {where_clause}
        ORDER BY p.product_id ASC
        LIMIT ? OFFSET ?;
    """
    rows = cursor.execute(query_sql, query_params).fetchall()
    products = [ProductItem(**dict(r)) for r in rows]

    total_pages = math.ceil(total / effective_page_size) if total > 0 else 1

    return PaginatedProductsResponse(
        products=products,
        total=total,
        page=page,
        page_size=effective_page_size,
        total_pages=total_pages
    )


@router.get("/{product_id}", response_model=ProductItem)
def get_product_detail(product_id: int, db: sqlite3.Connection = Depends(get_db)):
    """Returns the complete factual product record for a given product_id."""
    cursor = db.cursor()
    row = cursor.execute("""
        SELECT
            p.product_id,
            p.canonical_id,
            b.brand_name AS brand,
            c.category_name AS category,
            c.product_format,
            p.platform,
            p.title_clean,
            p.title_raw,
            p.selling_price,
            p.mrp,
            p.discount_pct,
            p.discount_source,
            p.rating,
            p.review_count,
            p.rating_source,
            p.review_source,
            p.seller,
            p.availability,
            p.pack_count,
            p.unit_quantity,
            p.unit,
            p.total_quantity,
            p.price_per_unit,
            p.price_per_100g,
            p.price_per_100ml,
            p.product_url,
            p.scraped_at,
            p.raw_reference
        FROM products p
        JOIN brands b ON p.brand_id = b.brand_id
        JOIN categories c ON p.category_id = c.category_id
        WHERE p.product_id = ?;
    """, (product_id,)).fetchone()

    if not row:
        raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found")

    return ProductItem(**dict(row))
