import sqlite3
import numpy as np
from fastapi import APIRouter, Depends
from typing import List, Dict, Any
from api.database import get_db
from api.schemas import (
    PricePositioningItem,
    PriceNormalizationMetrics,
    CategoryAnalysisItem,
    PlatformAnalysisItem,
    DiscountAnalysisItem,
    CategoryCoverageResponse,
    FilterOptionsResponse,
    ProductClustersResponse,
    ProductClusterItem
)

router = APIRouter(prefix="/api", tags=["Analytics"])

@router.get("/analytics/price-positioning", response_model=List[PricePositioningItem])
def get_price_positioning(db: sqlite3.Connection = Depends(get_db)):
    """
    Returns empirical points for Price vs. Rating scatter analysis.
    Preserves factual ratings without imputation.
    """
    cursor = db.cursor()
    rows = cursor.execute("""
        SELECT
            p.product_id,
            p.canonical_id,
            p.title_clean AS product_name,
            b.brand_name AS brand,
            c.category_name AS category,
            c.product_format,
            p.selling_price,
            p.rating,
            p.review_count,
            p.discount_pct,
            p.price_per_unit,
            p.price_per_100g,
            p.price_per_100ml
        FROM products p
        JOIN brands b ON p.brand_id = b.brand_id
        JOIN categories c ON p.category_id = c.category_id
        ORDER BY p.selling_price ASC;
    """).fetchall()
    return [PricePositioningItem(**dict(r)) for r in rows]

@router.get("/analytics/price-normalization", response_model=PriceNormalizationMetrics)
def get_price_normalization(db: sqlite3.Connection = Depends(get_db)):
    """
    Returns normalized price statistics strictly segregated by unit type.
    Never conflates ₹/100g and ₹/100ml.
    """
    cursor = db.cursor()

    ppu_row = cursor.execute("""
        SELECT COUNT(price_per_unit) AS cnt, ROUND(AVG(price_per_unit), 2) AS avg_val,
               ROUND(MIN(price_per_unit), 2) AS min_val, ROUND(MAX(price_per_unit), 2) AS max_val
        FROM products WHERE price_per_unit IS NOT NULL;
    """).fetchone()

    pp100g_row = cursor.execute("""
        SELECT COUNT(price_per_100g) AS cnt, ROUND(AVG(price_per_100g), 2) AS avg_val,
               ROUND(MIN(price_per_100g), 2) AS min_val, ROUND(MAX(price_per_100g), 2) AS max_val
        FROM products WHERE price_per_100g IS NOT NULL AND unit = 'g';
    """).fetchone()

    pp100ml_row = cursor.execute("""
        SELECT COUNT(price_per_100ml) AS cnt, ROUND(AVG(price_per_100ml), 2) AS avg_val,
               ROUND(MIN(price_per_100ml), 2) AS min_val, ROUND(MAX(price_per_100ml), 2) AS max_val
        FROM products WHERE price_per_100ml IS NOT NULL AND unit = 'ml';
    """).fetchone()

    return PriceNormalizationMetrics(
        price_per_unit={
            "description": "Normalized price per individual product/pack unit",
            "count": ppu_row["cnt"],
            "average": ppu_row["avg_val"],
            "min": ppu_row["min_val"],
            "max": ppu_row["max_val"],
            "unit": "INR/unit"
        },
        price_per_100g={
            "description": "Normalized price per 100 grams for solid blocks, candles, and gels",
            "count": pp100g_row["cnt"],
            "average": pp100g_row["avg_val"],
            "min": pp100g_row["min_val"],
            "max": pp100g_row["max_val"],
            "unit": "INR/100g"
        },
        price_per_100ml={
            "description": "Normalized price per 100 milliliters for liquid sprays, aerosols, and diffusers",
            "count": pp100ml_row["cnt"],
            "average": pp100ml_row["avg_val"],
            "min": pp100ml_row["min_val"],
            "max": pp100ml_row["max_val"],
            "unit": "INR/100ml"
        }
    )

@router.get("/analytics/categories", response_model=List[CategoryAnalysisItem])
def get_category_analysis(db: sqlite3.Connection = Depends(get_db)):
    """Returns comparative metrics by standardized fragrance category."""
    cursor = db.cursor()
    rows = cursor.execute("""
        SELECT
            c.category_name AS category,
            COUNT(p.product_id) AS product_count,
            COUNT(DISTINCT p.brand_id) AS brand_count,
            ROUND(AVG(p.selling_price), 2) AS average_price,
            ROUND(AVG(p.rating), 2) AS average_rating,
            ROUND(AVG(p.discount_pct), 2) AS average_discount
        FROM categories c
        LEFT JOIN products p ON c.category_id = p.category_id
        GROUP BY c.category_name
        ORDER BY product_count DESC;
    """).fetchall()
    return [CategoryAnalysisItem(**dict(r)) for r in rows]

@router.get("/analytics/platforms", response_model=List[PlatformAnalysisItem])
def get_platform_analysis(db: sqlite3.Connection = Depends(get_db)):
    """Returns comparative metrics by source channel / platform."""
    cursor = db.cursor()
    rows = cursor.execute("""
        SELECT
            platform,
            COUNT(product_id) AS product_count,
            COUNT(DISTINCT brand_id) AS brand_count,
            ROUND(AVG(selling_price), 2) AS average_price,
            ROUND(AVG(rating), 2) AS average_rating,
            ROUND(AVG(discount_pct), 2) AS average_discount
        FROM products
        GROUP BY platform
        ORDER BY product_count DESC;
    """).fetchall()
    return [PlatformAnalysisItem(**dict(r)) for r in rows]

@router.get("/analytics/discounts", response_model=List[DiscountAnalysisItem])
def get_discount_analysis(db: sqlite3.Connection = Depends(get_db)):
    """
    Returns records with verified, non-null discounts.
    Missing discounts are excluded and never treated as 0%.
    """
    cursor = db.cursor()
    rows = cursor.execute("""
        SELECT
            b.brand_name AS brand,
            c.category_name AS category,
            p.title_clean AS product_name,
            p.selling_price,
            p.mrp,
            p.discount_pct
        FROM products p
        JOIN brands b ON p.brand_id = b.brand_id
        JOIN categories c ON p.category_id = c.category_id
        WHERE p.discount_pct IS NOT NULL AND p.mrp IS NOT NULL
        ORDER BY p.discount_pct DESC;
    """).fetchall()
    return [DiscountAnalysisItem(**dict(r)) for r in rows]

@router.get("/analytics/category-coverage", response_model=CategoryCoverageResponse)
def get_category_coverage(db: sqlite3.Connection = Depends(get_db)):
    """
    Returns brand-by-category coverage matrix.
    Note: Zero observed items indicates 'No observed product in collected dataset',
    not an absence of commercial production.
    """
    cursor = db.cursor()
    categories = [r[0] for r in cursor.execute("SELECT category_name FROM categories ORDER BY category_name;").fetchall()]
    brands = [r[0] for r in cursor.execute("SELECT brand_name FROM brands ORDER BY brand_name;").fetchall()]

    matrix = []
    for cat in categories:
        row_dict = {"category": cat}
        row_total = 0
        for b in brands:
            cnt = cursor.execute("""
                SELECT COUNT(p.product_id)
                FROM products p
                JOIN brands br ON p.brand_id = br.brand_id
                JOIN categories ca ON p.category_id = ca.category_id
                WHERE ca.category_name = ? AND br.brand_name = ?;
            """, (cat, b)).fetchone()[0]
            row_dict[b] = cnt
            row_total += cnt
        row_dict["total"] = row_total
        matrix.append(row_dict)

    return CategoryCoverageResponse(
        categories=categories,
        brands=brands,
        matrix=matrix,
        coverage_matrix=matrix,
        methodology_note="Values represent observed assortment counts in the collected public dataset. Zero indicates no product observed in sample, not absence of commercial offering."
    )


@router.get("/analytics/product-clusters", response_model=ProductClustersResponse)
def get_product_clusters(db: sqlite3.Connection = Depends(get_db)):
    """
    Computes objective product clusters on products with non-null quantitative features:
    selling_price, rating, discount_pct, and log-transformed review_count.
    Standardizes features, tests K=2..5, and selects optimal K using silhouette score.
    Clusters are labeled neutrally as Cluster 1, Cluster 2, etc.
    """
    cursor = db.cursor()
    total_count = cursor.execute("SELECT COUNT(*) FROM products;").fetchone()[0]

    rows = cursor.execute("""
        SELECT
            selling_price,
            rating,
            discount_pct,
            COALESCE(review_count, 0) AS reviews
        FROM products
        WHERE selling_price IS NOT NULL
          AND rating IS NOT NULL
          AND discount_pct IS NOT NULL;
    """).fetchall()

    if len(rows) < 10:
        return ProductClustersResponse(
            clusters=[],
            usable_product_count=len(rows),
            total_catalogue_count=total_count,
            selected_k=0,
            silhouette_score=0.0,
            methodology_note="Insufficient products with complete feature sets for statistical clustering."
        )

    prices = np.array([r["selling_price"] for r in rows], dtype=float)
    ratings = np.array([r["rating"] for r in rows], dtype=float)
    discounts = np.array([r["discount_pct"] for r in rows], dtype=float)
    log_reviews = np.log1p(np.array([r["reviews"] for r in rows], dtype=float))

    X = np.column_stack([prices, ratings, discounts, log_reviews])
    mean = X.mean(axis=0)
    std = X.std(axis=0)
    std[std == 0] = 1.0
    X_norm = (X - mean) / std

    def run_kmeans(data, k, max_iters=100, seed=42):
        np.random.seed(seed)
        n = len(data)
        centroids = data[np.random.choice(n, k, replace=False)]
        for _ in range(max_iters):
            dists = np.linalg.norm(data[:, np.newaxis] - centroids, axis=2)
            lbls = np.argmin(dists, axis=1)
            new_c = np.array([
                data[lbls == j].mean(axis=0) if np.sum(lbls == j) > 0 else centroids[j]
                for j in range(k)
            ])
            if np.allclose(centroids, new_c):
                break
            centroids = new_c
        return lbls, centroids

    def compute_silhouette(data, lbls, k):
        n = len(data)
        if k < 2 or k >= n:
            return 0.0
        s_vals = []
        for i in range(n):
            same_c = (lbls == lbls[i])
            if np.sum(same_c) <= 1:
                s_vals.append(0.0)
                continue
            a_i = np.mean(np.linalg.norm(data[same_c] - data[i], axis=1))
            b_i = np.inf
            for j in range(k):
                if j == lbls[i]:
                    continue
                other_c = (lbls == j)
                if np.sum(other_c) > 0:
                    d_other = np.mean(np.linalg.norm(data[other_c] - data[i], axis=1))
                    b_i = min(b_i, d_other)
            s_i = (b_i - a_i) / max(a_i, b_i)
            s_vals.append(s_i)
        return float(np.mean(s_vals))

    # Evaluate K = 2 through 5
    best_k = 2
    best_score = -1.0
    best_labels = None

    for k in range(2, 6):
        lbls, _ = run_kmeans(X_norm, k)
        sc = compute_silhouette(X_norm, lbls, k)
        if sc > best_score:
            best_score = sc
            best_k = k
            best_labels = lbls

    cluster_items = []
    for c_id in range(best_k):
        mask = (best_labels == c_id)
        c_prices = prices[mask]
        c_ratings = ratings[mask]
        c_discounts = discounts[mask]
        c_reviews = np.array([r["reviews"] for idx, r in enumerate(rows) if mask[idx]], dtype=float)

        p_mean = round(float(np.mean(c_prices)), 2)
        p_median = round(float(np.median(c_prices)), 2)
        r_mean = round(float(np.mean(c_ratings)), 2)
        d_mean = round(float(np.mean(c_discounts)), 2)
        rev_mean = round(float(np.mean(c_reviews)), 2)

        desc = f"Price ~₹{int(p_median)}, Rating ~{r_mean}★, Discount ~{int(d_mean)}%"

        cluster_items.append(ProductClusterItem(
            cluster_id=c_id + 1,
            cluster_name=f"Cluster {c_id + 1}",
            product_count=int(np.sum(mask)),
            average_price=p_mean,
            median_price=p_median,
            average_rating=r_mean,
            average_discount=d_mean,
            average_reviews=rev_mean,
            key_characteristics=desc
        ))

    cluster_items.sort(key=lambda x: x.median_price)
    for idx, item in enumerate(cluster_items):
        item.cluster_id = idx + 1
        item.cluster_name = f"Cluster {idx + 1}"

    return ProductClustersResponse(
        clusters=cluster_items,
        usable_product_count=len(rows),
        total_catalogue_count=total_count,
        selected_k=best_k,
        silhouette_score=round(best_score, 4),
        methodology_note="K-Means clustering on standardized features (selling_price, rating, discount_pct, log1p(reviews)). Optimal K selected via silhouette score. Clusters represent statistical groupings within usable records, not exhaustive market segments."
    )


@router.get("/filters", response_model=FilterOptionsResponse)
def get_filter_options(db: sqlite3.Connection = Depends(get_db)):
    """Provides dynamic unique options for dashboard filter controls."""
    cursor = db.cursor()
    brands = [r[0] for r in cursor.execute("SELECT DISTINCT brand_name FROM brands ORDER BY brand_name;").fetchall()]
    platforms = [r[0] for r in cursor.execute("SELECT DISTINCT platform FROM products ORDER BY platform;").fetchall()]
    categories = [r[0] for r in cursor.execute("SELECT DISTINCT category_name FROM categories ORDER BY category_name;").fetchall()]
    formats = [r[0] for r in cursor.execute("SELECT DISTINCT product_format FROM categories WHERE product_format IS NOT NULL ORDER BY product_format;").fetchall()]
    pack_sizes = [r[0] for r in cursor.execute("SELECT DISTINCT pack_count FROM products WHERE pack_count IS NOT NULL ORDER BY pack_count;").fetchall()]
    availability = [r[0] for r in cursor.execute("SELECT DISTINCT availability FROM products ORDER BY availability;").fetchall()]

    price_bounds = cursor.execute("SELECT MIN(selling_price) AS min_p, MAX(selling_price) AS max_p FROM products;").fetchone()
    rating_bounds = cursor.execute("SELECT MIN(rating) AS min_r, MAX(rating) AS max_r FROM products WHERE rating IS NOT NULL;").fetchone()

    return FilterOptionsResponse(
        brands=brands,
        platforms=platforms,
        categories=categories,
        product_formats=formats,
        pack_sizes=pack_sizes,
        availability=availability,
        price_range={"min": price_bounds["min_p"] or 0.0, "max": price_bounds["max_p"] or 1000.0},
        rating_range={"min": rating_bounds["min_r"] or 0.0, "max": rating_bounds["max_r"] or 5.0}
    )
