import os
import json
import pytest
import pandas as pd
from unittest.mock import MagicMock, patch

from src.pipeline.orchestrator import PipelineOrchestrator
from src.pipeline.quality_gate import DataQualityGate, QualityGateError
from src.transformation.transformer import AnalyticalTransformer

MOCK_CONFIG = {
    "selected_brands": [
        {"name": "AromaPure", "source_type": "shopify_json"},
        {"name": "Godrej aer", "source_type": "amazon_search"}
    ],
    "request_settings": {
        "timeout": 5,
        "delay_range": [0.1, 0.2],
        "retry_count": 1,
        "backoff_factor": 1.0,
        "user_agent": "TestAgent"
    },
    "storage": {
        "raw_base_dir": "data/raw"
    }
}

def test_pipeline_orchestrator_initialization():
    orchestrator = PipelineOrchestrator(config=MOCK_CONFIG, runs_dir="data/test_runs")
    assert orchestrator.config == MOCK_CONFIG
    assert os.path.exists("data/test_runs")

def test_transformation_stage(tmp_path):
    # Test that transformation preserves rows, ensures deterministic typing, and avoids arbitrary labels
    input_csv = tmp_path / "test_clean.csv"
    output_csv = tmp_path / "test_transformed.csv"

    df_sample = pd.DataFrame([
        {
            "product_id": "P101",
            "brand": "Odonil",
            "category": "Room Spray & Aerosol",
            "product_format": "Room Spray",
            "platform": "Amazon India",
            "title_clean": "Odonil Spray",
            "title_raw": "Odonil Spray Raw",
            "selling_price": 180.0,
            "mrp": 200.0,
            "discount_pct": 10.0,
            "rating": 4.2,
            "review_count": 650,
            "availability": "In Stock",
            "pack_count": 1,
            "unit_quantity": 250.0,
            "unit": "ml",
            "total_quantity": 250.0,
            "price_per_unit": 180.0,
            "price_per_100g": None,
            "price_per_100ml": 72.0
        },
        {
            "product_id": "P102",
            "brand": "AromaPure",
            "category": "Reed Diffuser & Fragrance Oil",
            "product_format": "Diffuser / Aroma Oil",
            "platform": "AromaPure Official",
            "title_clean": "AromaPure Diffuser",
            "title_raw": "AromaPure Diffuser Raw",
            "selling_price": 899.0,
            "mrp": 1200.0,
            "discount_pct": 25.08,
            "rating": None,
            "review_count": None,
            "availability": "In Stock",
            "pack_count": 1,
            "unit_quantity": 100.0,
            "unit": "ml",
            "total_quantity": 100.0,
            "price_per_unit": 899.0,
            "price_per_100g": None,
            "price_per_100ml": 899.0
        }
    ])
    df_sample.to_csv(input_csv, index=False)

    transformer = AnalyticalTransformer(input_csv_path=str(input_csv), output_csv_path=str(output_csv))
    df_out = transformer.transform()

    assert len(df_out) == 2
    # Verify factual fields exist
    assert "selling_price" in df_out.columns
    assert "price_per_unit" in df_out.columns
    assert "price_per_100ml" in df_out.columns
    assert df_out.iloc[0]["selling_price"] == 180.0
    assert df_out.iloc[1]["price_per_unit"] == 899.0

    # Verify absence of arbitrary business labels
    assert "price_tier" not in df_out.columns
    assert "engagement_tier" not in df_out.columns

def test_quality_gate_passes_on_valid_data():
    gate = DataQualityGate(db_path="data/market_intelligence.db", csv_path="data/processed/products_clean.csv")
    report = gate.run_checks()
    assert report["passed"] is True
    assert report["checks"]["min_100_products_passed"] is True
    assert report["checks"]["all_5_brands_present"] is True
    assert report["checks"]["each_brand_ge_20_products"] is True
    assert report["checks"]["db_matches_csv"] is True

def test_quality_gate_fails_on_insufficient_products(tmp_path):
    # Test that quality gate rejects if products < 100
    mock_csv = tmp_path / "under_100.csv"
    df_small = pd.DataFrame([{"product_id": f"P{i}", "brand": "Odonil", "selling_price": 100.0} for i in range(10)])
    df_small.to_csv(mock_csv, index=False)

    gate = DataQualityGate(db_path="data/market_intelligence.db", csv_path=str(mock_csv))
    with pytest.raises(QualityGateError, match="below required threshold of 100"):
        gate.run_checks()

def test_idempotency_database_loading():
    # Verify that repeated database loading does not produce duplicate rows
    from src.database.database import DatabaseLoader
    loader = DatabaseLoader()
    count1 = loader.load_processed_csv("data/processed/products_clean.csv")
    count2 = loader.load_processed_csv("data/processed/products_clean.csv")
    assert count1 == 767
    assert count2 == 767
    
    val = loader.validate_database()
    assert val["total_products"] == 767
    assert val["unique_canonical"] == 767
