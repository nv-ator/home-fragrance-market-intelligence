import pytest
from src.cleaning.text_parsers import (
    clean_text,
    parse_price,
    calculate_discount,
    parse_rating,
    parse_review_count
)
from src.cleaning.quantity_normalizer import parse_pack_quantity, calculate_normalized_prices
from src.cleaning.classifier import normalize_brand, evaluate_home_fragrance_scope, classify_category_and_format

def test_price_parsing():
    assert parse_price("₹199") == 199.0
    assert parse_price("₹ 1,299.50") == 1299.50
    assert parse_price("199.00") == 199.0
    assert parse_price(None) is None
    assert parse_price("free") is None

def test_discount_calculation():
    # Calculated discount
    pct, src = calculate_discount(selling_price=160.0, mrp=200.0)
    assert pct == 20.0
    assert src == "calculated"

    # Selling price > MRP should yield unavailable
    pct_invalid, src_invalid = calculate_discount(selling_price=250.0, mrp=200.0)
    assert pct_invalid is None
    assert src_invalid == "unavailable"

    # Missing MRP should not default to 0% discount
    pct_missing, src_missing = calculate_discount(selling_price=199.0, mrp=None)
    assert pct_missing is None
    assert src_missing == "unavailable"

def test_rating_and_review_normalization():
    assert parse_rating("4.3 out of 5 stars") == 4.3
    assert parse_rating("5.0") == 5.0
    assert parse_rating("6.5") is None  # Invalid range
    assert parse_rating(None) is None

    assert parse_review_count("15,420") == 15420
    assert parse_review_count("8.5K") == 8500
    assert parse_review_count(None) is None

def test_quantity_parsing():
    # Multi-pack with volume
    res1 = parse_pack_quantity("Ambi Pur Room Spray (2 x 275 ml)")
    assert res1["pack_count"] == 2
    assert res1["unit"] == "ml"
    assert res1["unit_quantity"] == 275.0
    assert res1["total_quantity"] == 550.0

    # Multi-pack with mass
    res2 = parse_pack_quantity("Odonil Bathroom Air Freshener Blocks - 3 x 75g")
    assert res2["pack_count"] == 3
    assert res2["unit"] == "g"
    assert res2["unit_quantity"] == 75.0
    assert res2["total_quantity"] == 225.0

    # Pack count only
    res3 = parse_pack_quantity("Godrej aer Pocket Bathroom Freshener - Pack of 3")
    assert res3["pack_count"] == 3
    assert res3["unit"] == "count"
    assert res3["total_quantity"] == 3.0

def test_price_normalization_by_unit():
    # Mass based: 225g @ Rs 180 -> Rs 80 per 100g
    qty_mass = {"unit": "g", "total_quantity": 225.0, "pack_count": 3}
    prices_mass = calculate_normalized_prices(180.0, qty_mass)
    assert prices_mass["price_per_100g"] == 80.0
    assert prices_mass["price_per_100ml"] is None
    assert prices_mass["price_per_unit"] == 60.0

    # Volume based: 500ml @ Rs 250 -> Rs 50 per 100ml
    qty_vol = {"unit": "ml", "total_quantity": 500.0, "pack_count": 2}
    prices_vol = calculate_normalized_prices(250.0, qty_vol)
    assert prices_vol["price_per_100ml"] == 50.0
    assert prices_vol["price_per_100g"] is None
    assert prices_vol["price_per_unit"] == 125.0

def test_brand_normalization():
    b1, err1 = normalize_brand("Godrej", "Godrej aer Pocket Bathroom Freshener")
    assert b1 == "Godrej aer"
    assert err1 is None

    b2, err2 = normalize_brand("Aromahpure", "AromaPure Reed Diffuser")
    assert b2 == "AromaPure"
    assert err2 is None

    b3, err3 = normalize_brand("Unknown", "Generic Unrelated Brand Diffuser")
    assert b3 is None
    assert err3 == "invalid_brand"

def test_home_fragrance_scope():
    # Valid room freshener
    valid_home, err_home = evaluate_home_fragrance_scope("Odonil Room Air Freshener Spray 240ml")
    assert valid_home is True
    assert err_home is None

    # Excluded car-only product
    car_only, err_car = evaluate_home_fragrance_scope("Aromahpure Premium Car Dashboard Perfume Peach")
    assert car_only is False
    assert err_car == "out_of_scope_car_only"

    # Excluded insecticide
    pest, err_pest = evaluate_home_fragrance_scope("Godrej aer Mosquito Repellent Refill")
    assert pest is False
    assert "unrelated_product" in err_pest
