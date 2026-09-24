import os
import json
import pytest
from src.scrapers.aromapure import AromaPureScraper
from src.scrapers.amazon import AmazonScraper
from src.utils.manifest import ManifestManager

FIXTURE_DIR = os.path.join(os.path.dirname(__file__), "fixtures")

@pytest.fixture
def mock_config():
    return {
        "selected_brands": [
            {"name": "AromaPure", "source_type": "shopify_json"},
            {"name": "Godrej aer", "source_type": "amazon_search"}
        ],
        "request_settings": {
            "timeout": 5,
            "delay_range": [0.1, 0.2],
            "retry_count": 2,
            "backoff_factor": 1.5,
            "user_agent": "TestAgent"
        },
        "storage": {
            "raw_base_dir": "tests/test_raw"
        }
    }

def test_aromapure_parser(mock_config):
    scraper = AromaPureScraper({"name": "AromaPure"}, mock_config)
    with open(os.path.join(FIXTURE_DIR, "sample_aromapure.json"), "r", encoding="utf-8") as f:
        data = json.load(f)
    candidates = scraper.parse_raw_products(data, "mock_raw.json")
    
    # 2 variants in product 1, 1 variant in product 2 -> 3 candidates
    assert len(candidates) == 3
    
    first = candidates[0]
    assert first["brand"] == "Aromahpure"
    assert first["product_id"] == "9901_8801"
    assert first["price_raw"] == "499.00"
    assert first["mrp_raw"] == "699.00"
    assert first["availability_raw"] == "In Stock"
    assert "100ml" in first["product_name"]

    second = candidates[1]
    assert second["product_id"] == "9901_8802"
    assert second["price_raw"] == "899.00"
    assert second["availability_raw"] == "Out of Stock"


def test_aromapure_review_fields_require_explicit_public_values(mock_config):
    scraper = AromaPureScraper({"name": "AromaPure"}, mock_config)
    html = '''
    <html><script type="application/ld+json">
    {"@type":"Product","aggregateRating":{"ratingValue":"4.7","reviewCount":"128"}}
    </script></html>
    '''
    fields = scraper._review_fields_from_html(html)
    assert fields["rating_raw"] == "4.7"
    assert fields["review_count_raw"] == "128"

    no_reviews = scraper._review_fields_from_html("<html>No reviews</html>")
    assert no_reviews["rating_raw"] is None
    assert no_reviews["review_count_raw"] == "0"

def test_amazon_parser_and_brand_matching(mock_config):
    scraper = AmazonScraper({"name": "Godrej aer", "search_queries": ["Godrej aer air freshener"]}, mock_config)
    with open(os.path.join(FIXTURE_DIR, "sample_amazon.html"), "r", encoding="utf-8") as f:
        html_content = f.read()

    candidates = scraper.parse_search_html(html_content, "mock_amazon.html", "https://amazon.in/s?k=test")
    
    # Out of 2 items in HTML, only 1 belongs to Godrej aer; the other unrelated brand item must be excluded
    assert len(candidates) == 1
    
    item = candidates[0]
    assert item["asin"] == "B08XYZ1234"
    assert "Godrej aer Pocket" in item["product_name"]
    assert item["price_raw"] == "165"
    assert item["mrp_raw"] == "180"
    assert item["rating_raw"] == "4.3"
    assert item["review_count_raw"] == "15420"
    assert "Best Seller" in item["tags_raw"]

def test_amazon_parser_empty_or_malformed(mock_config):
    scraper = AmazonScraper({"name": "Godrej aer"}, mock_config)
    candidates = scraper.parse_search_html("<div>Empty page</div>", "empty.html", "https://test.com")
    assert candidates == []

def test_manifest_manager(tmp_path):
    mgr = ManifestManager(raw_base_dir=str(tmp_path))
    run_id = "test_run_123"
    results = [
        {
            "brand": "AromaPure",
            "source": "AromaPure Official",
            "candidates_count": 10,
            "http_status": 200,
            "response_size": 5000,
            "elapsed_time_sec": 1.2,
            "errors": []
        }
    ]
    manifest_path = mgr.save_manifest(run_id, results)
    assert os.path.exists(manifest_path)
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest_data = json.load(f)
    assert manifest_data["run_id"] == run_id
    assert manifest_data["total_candidates"] == 10
    assert len(manifest_data["brands"]) == 1
