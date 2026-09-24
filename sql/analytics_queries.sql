-- ========================================================
-- REUSABLE ANALYTICAL QUERIES FOR HOME FRAGRANCE MARKET INTELLIGENCE
-- Compatible with SQLite 3.25+ (Supports Window Functions)
-- ========================================================

-- 1. Market Overview KPI Summary
SELECT
    COUNT(*) AS total_products,
    COUNT(DISTINCT brand) AS total_brands,
    ROUND(AVG(selling_price), 2) AS avg_selling_price,
    ROUND(MIN(selling_price), 2) AS min_price,
    ROUND(MAX(selling_price), 2) AS max_price,
    ROUND(AVG(rating), 2) AS avg_rating,
    SUM(review_count) AS total_reviews,
    ROUND(AVG(discount_pct), 2) AS avg_discount_pct,
    COUNT(DISTINCT category) AS total_categories
FROM vw_products_analytical;

-- 2. Exact Median Selling Price across Market (Window Function Methodology)
WITH RankedPrices AS (
    SELECT
        selling_price,
        ROW_NUMBER() OVER (ORDER BY selling_price) AS row_num,
        COUNT(*) OVER () AS total_count
    FROM vw_products_analytical
    WHERE selling_price IS NOT NULL
)
SELECT
    ROUND(AVG(selling_price), 2) AS market_median_price
FROM RankedPrices
WHERE row_num IN ((total_count + 1) / 2, (total_count + 2) / 2);

-- 3. Products by Platform Breakdown
SELECT
    platform,
    COUNT(*) AS product_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM products), 2) AS pct_share,
    ROUND(AVG(selling_price), 2) AS avg_platform_price
FROM vw_products_analytical
GROUP BY platform;

-- 4. Products by Category Assortment Breakdown
SELECT
    category,
    COUNT(*) AS product_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM products), 2) AS pct_share,
    ROUND(AVG(selling_price), 2) AS avg_category_price,
    ROUND(AVG(rating), 2) AS avg_rating,
    SUM(review_count) AS total_reviews
FROM vw_products_analytical
GROUP BY category
ORDER BY product_count DESC;

-- 5. Brand Comparison Benchmark Matrix
SELECT
    brand,
    COUNT(*) AS assortment_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM products), 2) AS share_of_collected_assortment_pct,
    ROUND(AVG(selling_price), 2) AS avg_price,
    ROUND(MIN(selling_price), 2) AS min_price,
    ROUND(MAX(selling_price), 2) AS max_price,
    ROUND(AVG(rating), 2) AS avg_rating,
    COALESCE(SUM(review_count), 0) AS total_reviews,
    ROUND(AVG(discount_pct), 2) AS avg_discount_pct,
    COUNT(DISTINCT category) AS categories_covered
FROM vw_products_analytical
GROUP BY brand
ORDER BY assortment_count DESC;

-- 6. Median Selling Price by Brand (Window Function Methodology)
WITH BrandRankedPrices AS (
    SELECT
        brand,
        selling_price,
        ROW_NUMBER() OVER (PARTITION BY brand ORDER BY selling_price) AS row_num,
        COUNT(*) OVER (PARTITION BY brand) AS total_count
    FROM vw_products_analytical
    WHERE selling_price IS NOT NULL
)
SELECT
    brand,
    ROUND(AVG(selling_price), 2) AS brand_median_price
FROM BrandRankedPrices
WHERE row_num IN ((total_count + 1) / 2, (total_count + 2) / 2)
GROUP BY brand
ORDER BY brand_median_price DESC;

-- 7. Price vs. Rating Scatter View
SELECT
    product_id,
    canonical_id,
    brand,
    category,
    title_clean,
    selling_price,
    rating,
    review_count
FROM vw_products_analytical
WHERE rating IS NOT NULL AND selling_price IS NOT NULL
ORDER BY rating DESC;

-- 8. Price-per-Unit Comparison by Format
SELECT
    product_format,
    unit,
    COUNT(*) AS product_count,
    ROUND(AVG(price_per_unit), 2) AS avg_price_per_unit,
    ROUND(AVG(price_per_100ml), 2) AS avg_price_per_100ml,
    ROUND(AVG(price_per_100g), 2) AS avg_price_per_100g
FROM vw_products_analytical
WHERE unit IS NOT NULL
GROUP BY product_format, unit;

-- 9. Discount Depth Distribution
SELECT
    brand,
    COUNT(CASE WHEN discount_pct IS NULL THEN 1 END) AS no_discount_available_count,
    COUNT(CASE WHEN discount_pct = 0 THEN 1 END) AS zero_discount_count,
    COUNT(CASE WHEN discount_pct > 0 AND discount_pct <= 20 THEN 1 END) AS discount_1_to_20_pct,
    COUNT(CASE WHEN discount_pct > 20 AND discount_pct <= 40 THEN 1 END) AS discount_21_to_40_pct,
    COUNT(CASE WHEN discount_pct > 40 THEN 1 END) AS discount_above_40_pct,
    ROUND(AVG(discount_pct), 2) AS avg_discount_pct
FROM vw_products_analytical
GROUP BY brand;

-- 10. Availability Distribution
SELECT
    availability,
    brand,
    COUNT(*) AS count
FROM vw_products_analytical
GROUP BY availability, brand;

-- 11. Category Coverage Matrix by Brand
SELECT
    c.category_name,
    COUNT(CASE WHEN b.brand_name = 'AromaPure' THEN 1 END) AS AromaPure_Assortment,
    COUNT(CASE WHEN b.brand_name = 'Odonil' THEN 1 END) AS Odonil_Assortment,
    COUNT(CASE WHEN b.brand_name = 'Godrej aer' THEN 1 END) AS Godrej_aer_Assortment,
    COUNT(CASE WHEN b.brand_name = 'Air Wick' THEN 1 END) AS Air_Wick_Assortment,
    COUNT(CASE WHEN b.brand_name = 'Ambi Pur' THEN 1 END) AS Ambi_Pur_Assortment
FROM categories c
CROSS JOIN brands b
LEFT JOIN products p ON p.category_id = c.category_id AND p.brand_id = b.brand_id
GROUP BY c.category_name;
