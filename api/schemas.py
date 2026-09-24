from typing import List, Optional, Dict, Any
from pydantic import BaseModel, ConfigDict

class HealthResponse(BaseModel):
    status: str
    database: str

class CountShareItem(BaseModel):
    name: str
    product_count: int
    pct_share: float

class MarketOverviewResponse(BaseModel):
    total_products: int
    total_brands: int
    average_price: float
    median_price: float
    average_rating: Optional[float]
    average_review_count: Optional[float]
    average_discount: Optional[float]
    products_by_brand: List[CountShareItem]
    products_by_platform: List[CountShareItem]
    products_by_category: List[CountShareItem]
    price_distribution: List[CountShareItem]

class BrandItem(BaseModel):
    brand_id: int
    brand_name: str
    product_count: int

class BrandComparisonItem(BaseModel):
    brand: str
    product_count: int
    share_of_collected_assortment_pct: float
    average_price: float
    median_price: float
    average_rating: Optional[float]
    total_reviews: int
    average_discount: Optional[float]
    category_count: int
    platform_count: int

class BrandDetailResponse(BaseModel):
    brand: str
    product_count: int
    share_of_collected_assortment_pct: float
    category_distribution: List[Dict[str, Any]]
    platform_distribution: List[Dict[str, Any]]
    price_statistics: Dict[str, Any]
    rating_statistics: Dict[str, Any]
    discount_statistics: Dict[str, Any]
    quantity_statistics: Dict[str, Any]

class ProductItem(BaseModel):
    product_id: int
    canonical_id: str
    brand: str
    category: str
    product_format: Optional[str]
    platform: str
    title_clean: str
    title_raw: str
    selling_price: float
    mrp: Optional[float]
    discount_pct: Optional[float]
    discount_source: Optional[str]
    rating: Optional[float]
    review_count: Optional[int]
    rating_source: Optional[str] = None
    review_source: Optional[str] = None
    seller: Optional[str] = None
    availability: str
    pack_count: Optional[int]
    unit_quantity: Optional[float]
    unit: Optional[str]
    total_quantity: Optional[float]
    price_per_unit: float
    price_per_100g: Optional[float]
    price_per_100ml: Optional[float]
    product_url: Optional[str]
    scraped_at: Optional[str]
    raw_reference: Optional[str]

class PaginatedProductsResponse(BaseModel):
    products: List[ProductItem]
    total: int
    page: int
    page_size: int
    total_pages: int

class PricePositioningItem(BaseModel):
    product_id: int
    canonical_id: str
    product_name: str
    brand: str
    category: str
    product_format: Optional[str]
    selling_price: float
    rating: Optional[float]
    review_count: Optional[int]
    discount_pct: Optional[float]
    price_per_unit: float
    price_per_100g: Optional[float]
    price_per_100ml: Optional[float]

class PriceNormalizationMetrics(BaseModel):
    price_per_unit: Dict[str, Any]
    price_per_100g: Dict[str, Any]
    price_per_100ml: Dict[str, Any]

class CategoryAnalysisItem(BaseModel):
    category: str
    product_count: int
    brand_count: int
    average_price: float
    average_rating: Optional[float]
    average_discount: Optional[float]

class PlatformAnalysisItem(BaseModel):
    platform: str
    product_count: int
    brand_count: int
    average_price: float
    average_rating: Optional[float]
    average_discount: Optional[float]

class DiscountAnalysisItem(BaseModel):
    brand: str
    category: str
    product_name: str
    selling_price: float
    mrp: float
    discount_pct: float

class CategoryCoverageResponse(BaseModel):
    categories: List[str]
    brands: List[str]
    matrix: List[Dict[str, Any]]
    coverage_matrix: Optional[List[Dict[str, Any]]] = None
    methodology_note: str


class ProductClusterItem(BaseModel):
    cluster_id: int
    cluster_name: str
    product_count: int
    average_price: float
    median_price: float
    average_rating: Optional[float]
    average_discount: Optional[float]
    average_reviews: Optional[float]
    key_characteristics: str

class ProductClustersResponse(BaseModel):
    clusters: List[ProductClusterItem]
    usable_product_count: int
    total_catalogue_count: int
    selected_k: int
    silhouette_score: float
    methodology_note: str

class FilterOptionsResponse(BaseModel):
    brands: List[str]
    platforms: List[str]
    categories: List[str]
    product_formats: List[str]
    pack_sizes: List[int] = []
    availability: List[str]
    price_range: Dict[str, float]
    rating_range: Dict[str, float]
