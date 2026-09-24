import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_api_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["database"] == "connected"

def test_market_overview():
    response = client.get("/api/overview")
    assert response.status_code == 200
    data = response.json()
    assert data["total_products"] == 684
    assert data["total_brands"] == 5
    assert data["average_price"] == 663.42
    assert data["median_price"] == 434.0
    assert len(data["products_by_brand"]) == 5
    assert len(data["products_by_platform"]) == 2
    assert "price_distribution" in data
    assert len(data["price_distribution"]) == 5
    dist_total = sum(d["product_count"] for d in data["price_distribution"])
    assert dist_total == 684


def test_brands_list():
    response = client.get("/api/brands")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    names = [b["brand_name"] for b in data]
    assert "AromaPure" in names
    assert "Odonil" in names
    assert "Godrej aer" in names

def test_brand_comparison():
    response = client.get("/api/brands/comparison")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    first = data[0]
    assert "brand" in first
    assert "product_count" in first
    assert "median_price" in first
    assert "share_of_collected_assortment_pct" in first

def test_brand_detail_valid():
    response = client.get("/api/brands/AromaPure")
    assert response.status_code == 200
    data = response.json()
    assert data["brand"] == "AromaPure"
    assert data["product_count"] == 298
    assert "price_statistics" in data
    assert "category_distribution" in data

def test_brand_detail_not_found():
    response = client.get("/api/brands/NonExistentBrand")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

def test_product_pagination():
    response = client.get("/api/products?page=1&page_size=20")
    assert response.status_code == 200
    data = response.json()
    assert len(data["products"]) == 20
    assert data["total"] == 684
    assert data["page"] == 1
    assert data["page_size"] == 20
    assert data["total_pages"] == 35

def test_product_filters():
    # Filter by brand
    resp_b = client.get("/api/products?brand=Odonil&page_size=200")
    assert resp_b.status_code == 200
    data_b = resp_b.json()
    assert data_b["total"] == 132
    for p in data_b["products"]:
        assert p["brand"] == "Odonil"

    # Filter by price range
    resp_p = client.get("/api/products?min_price=100&max_price=300")
    assert resp_p.status_code == 200
    data_p = resp_p.json()
    for p in data_p["products"]:
        assert 100.0 <= p["selling_price"] <= 300.0

def test_product_filter_invalid():
    resp = client.get("/api/products?min_price=-50")
    assert resp.status_code == 400

    resp2 = client.get("/api/products?min_rating=6.5")
    assert resp2.status_code == 400

def test_product_detail_valid():
    # Fetch first product to get its ID
    list_resp = client.get("/api/products?page=1&page_size=1")
    first_id = list_resp.json()["products"][0]["product_id"]

    resp = client.get(f"/api/products/{first_id}")
    assert resp.status_code == 200
    p = resp.json()
    assert p["product_id"] == first_id
    assert p["selling_price"] > 0

def test_product_detail_not_found():
    resp = client.get("/api/products/9999999")
    assert resp.status_code == 404

def test_null_preservation_in_json():
    # AromaPure products should return rating as JSON null, not 0
    resp = client.get("/api/products?brand=AromaPure&page=1&page_size=1")
    p = resp.json()["products"][0]
    assert p["rating"] is None
    assert p["review_count"] is None

def test_price_positioning_endpoint():
    resp = client.get("/api/analytics/price-positioning")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 684
    sample = data[0]
    assert "selling_price" in sample
    assert "rating" in sample
    assert "brand" in sample

def test_price_normalization_endpoint():
    resp = client.get("/api/analytics/price-normalization")
    assert resp.status_code == 200
    data = resp.json()
    assert "price_per_unit" in data
    assert "price_per_100g" in data
    assert "price_per_100ml" in data
    assert data["price_per_100g"]["unit"] == "INR/100g"
    assert data["price_per_100ml"]["unit"] == "INR/100ml"
    # Never combined into same metric
    assert data["price_per_100g"]["count"] == 23
    assert data["price_per_100ml"]["count"] == 231

def test_category_analysis():
    resp = client.get("/api/analytics/categories")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 7
    first = data[0]
    assert "category" in first
    assert "product_count" in first
    assert "average_price" in first

def test_platform_analysis():
    resp = client.get("/api/analytics/platforms")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 2
    names = [p["platform"] for p in data]
    assert "Amazon India" in names
    assert "AromaPure Official" in names

def test_discount_analysis():
    resp = client.get("/api/analytics/discounts")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 479
    for item in data:
        assert item["discount_pct"] is not None
        assert item["discount_pct"] >= 0

def test_product_search():
    resp = client.get("/api/products?search=lavender")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] > 0
    for p in data["products"]:
        assert "lavender" in p["title_clean"].lower() or "lavender" in p["title_raw"].lower()

def test_category_coverage():
    resp = client.get("/api/analytics/category-coverage")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["categories"]) == 7
    assert len(data["brands"]) == 5
    assert "methodology_note" in data
    assert "matrix" in data
    assert len(data["matrix"]) == 7
    for row in data["matrix"]:
        brand_sum = sum(row[b] for b in data["brands"])
        assert row["total"] == brand_sum

def test_filter_options():
    resp = client.get("/api/filters")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["brands"]) == 5
    assert len(data["platforms"]) == 2
    assert len(data["categories"]) == 7
    assert "pack_sizes" in data
    assert len(data["pack_sizes"]) > 0
    assert data["price_range"]["min"] >= 0
    assert data["price_range"]["max"] > 0

def test_product_clusters():
    resp = client.get("/api/analytics/product-clusters")
    assert resp.status_code == 200
    data = resp.json()
    assert data["usable_product_count"] == 159
    assert data["total_catalogue_count"] == 684
    assert data["selected_k"] in [2, 3, 4, 5]
    assert data["silhouette_score"] > 0.3
    assert len(data["clusters"]) == data["selected_k"]
    total_clustered = sum(c["product_count"] for c in data["clusters"])
    assert total_clustered == 159
    for c in data["clusters"]:
        assert c["cluster_name"].startswith("Cluster ")
        assert c["average_price"] > 0
        assert c["median_price"] > 0

def test_product_pack_size_filter():
    resp = client.get("/api/products?pack_count=1")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 599
    assert len(data["products"]) > 0

    resp_multi = client.get("/api/products?pack_size=20")
    assert resp_multi.status_code == 200
    data_multi = resp_multi.json()
    assert data_multi["total"] == 19

