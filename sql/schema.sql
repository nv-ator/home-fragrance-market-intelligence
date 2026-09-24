-- Schema Definition for Home Fragrance Market Intelligence Database

PRAGMA foreign_keys = ON;

-- 1. Brands Dimension Table
CREATE TABLE IF NOT EXISTS brands (
    brand_id INTEGER PRIMARY KEY AUTOINCREMENT,
    brand_name TEXT UNIQUE NOT NULL
);

-- 2. Categories Dimension Table
CREATE TABLE IF NOT EXISTS categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT UNIQUE NOT NULL,
    product_format TEXT
);

-- 3. Data Sources Dimension Table
CREATE TABLE IF NOT EXISTS data_sources (
    source_id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_name TEXT NOT NULL,
    platform TEXT NOT NULL,
    source_type TEXT NOT NULL,
    UNIQUE(source_name, platform)
);

-- 4. Unified Products Table
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    canonical_id TEXT UNIQUE NOT NULL,
    brand_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    source_id INTEGER NOT NULL,
    title_clean TEXT NOT NULL,
    title_raw TEXT NOT NULL,
    platform TEXT NOT NULL,
    product_url TEXT,
    selling_price REAL NOT NULL,
    mrp REAL,
    discount_pct REAL,
    discount_source TEXT,
    rating REAL,
    review_count INTEGER,
    rating_source TEXT,
    review_source TEXT,
    seller TEXT,
    availability TEXT NOT NULL,
    pack_count INTEGER,
    unit_quantity REAL,
    unit TEXT,
    total_quantity REAL,
    price_per_unit REAL NOT NULL,
    price_per_100g REAL,
    price_per_100ml REAL,
    scraped_at TEXT,
    raw_reference TEXT,
    FOREIGN KEY (brand_id) REFERENCES brands(brand_id),
    FOREIGN KEY (category_id) REFERENCES categories(category_id),
    FOREIGN KEY (source_id) REFERENCES data_sources(source_id)
);

-- Indexes for Query Performance and Dashboard Acceleration
CREATE INDEX IF NOT EXISTS idx_products_brand_id ON products(brand_id);
CREATE INDEX IF NOT EXISTS idx_products_category_id ON products(category_id);
CREATE INDEX IF NOT EXISTS idx_products_source_id ON products(source_id);
CREATE INDEX IF NOT EXISTS idx_products_platform ON products(platform);
CREATE INDEX IF NOT EXISTS idx_products_selling_price ON products(selling_price);
CREATE INDEX IF NOT EXISTS idx_products_rating ON products(rating);
CREATE INDEX IF NOT EXISTS idx_products_review_count ON products(review_count);
CREATE INDEX IF NOT EXISTS idx_products_availability ON products(availability);
CREATE INDEX IF NOT EXISTS idx_products_unit ON products(unit);

-- ========================================================
-- ANALYTICAL VIEWS
-- ========================================================

-- View 1: Complete Analytical Product View
DROP VIEW IF EXISTS vw_products_analytical;
CREATE VIEW vw_products_analytical AS
SELECT
    p.product_id,
    p.canonical_id,
    b.brand_name AS brand,
    c.category_name AS category,
    c.product_format,
    s.source_name AS source,
    p.platform,
    p.title_clean,
    p.title_raw,
    p.selling_price,
    p.mrp,
    p.discount_pct,
    p.discount_source,
    p.rating,
    p.review_count,
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
JOIN data_sources s ON p.source_id = s.source_id;

-- View 2: Market Overview Aggregates
DROP VIEW IF EXISTS vw_market_overview;
CREATE VIEW vw_market_overview AS
SELECT
    COUNT(*) AS total_products,
    COUNT(DISTINCT brand) AS total_brands,
    ROUND(AVG(selling_price), 2) AS avg_selling_price,
    ROUND(AVG(rating), 2) AS avg_rating,
    SUM(review_count) AS total_reviews,
    ROUND(AVG(discount_pct), 2) AS avg_discount_pct,
    COUNT(DISTINCT category) AS total_categories
FROM vw_products_analytical;

-- View 3: Brand Comparison Benchmarks
DROP VIEW IF EXISTS vw_brand_comparison;
CREATE VIEW vw_brand_comparison AS
SELECT
    b.brand_name AS brand,
    COUNT(p.product_id) AS total_products,
    ROUND(COUNT(p.product_id) * 100.0 / (SELECT COUNT(*) FROM products), 2) AS share_of_collected_assortment_pct,
    ROUND(AVG(p.selling_price), 2) AS avg_price,
    ROUND(MIN(p.selling_price), 2) AS min_price,
    ROUND(MAX(p.selling_price), 2) AS max_price,
    ROUND(AVG(p.rating), 2) AS avg_rating,
    COALESCE(SUM(p.review_count), 0) AS total_reviews,
    ROUND(AVG(p.discount_pct), 2) AS avg_discount_pct,
    COUNT(DISTINCT p.category_id) AS categories_covered
FROM products p
JOIN brands b ON p.brand_id = b.brand_id
GROUP BY b.brand_name;

-- View 4: Category Coverage Breakdown
DROP VIEW IF EXISTS vw_category_coverage;
CREATE VIEW vw_category_coverage AS
SELECT
    c.category_name AS category,
    b.brand_name AS brand,
    COUNT(p.product_id) AS product_count,
    ROUND(AVG(p.selling_price), 2) AS avg_category_price,
    ROUND(AVG(p.rating), 2) AS avg_category_rating,
    COALESCE(SUM(p.review_count), 0) AS category_reviews
FROM products p
JOIN brands b ON p.brand_id = b.brand_id
JOIN categories c ON p.category_id = c.category_id
GROUP BY c.category_name, b.brand_name;
