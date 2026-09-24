from typing import Optional, Tuple

ALLOWED_BRANDS = ["AromaPure", "Odonil", "Godrej aer", "Air Wick", "Ambi Pur"]

# Car-only indicators
CAR_EXCLUSION_KEYWORDS = [
    "car perfume",
    "car perfume spray",
    "car spray",
    "car freshener",
    "car air freshener",
    "car vent",
    "vent clip",
    "car hanging",
    "hanging card",
    "dashboard perfume",
    "car fragrance",
    "auto fragrance",
]

# Dual or home indicators that can override ambiguous car mention (e.g. "for home and car")
HOME_OVERRIDE_KEYWORDS = [
    "room", "linen", "bathroom", "bedroom", "diffuser", "candle", "wardrobe", "closet", "home"
]

def normalize_brand(brand_raw: Optional[str], title_raw: Optional[str]) -> Tuple[Optional[str], Optional[str]]:
    """
    Validates and normalizes brand to one of the five target brands.
    Returns (normalized_brand, rejection_reason).
    """
    combined = f"{brand_raw or ''} {title_raw or ''}".lower()

    if "godrej" in combined and "aer" in combined:
        return "Godrej aer", None
    if "odonil" in combined:
        return "Odonil", None
    if "air wick" in combined or "airwick" in combined:
        return "Air Wick", None
    if "ambi pur" in combined or "ambipur" in combined:
        return "Ambi Pur", None
    if "aromahpure" in combined or "aromapure" in combined:
        return "AromaPure", None

    return None, "invalid_brand"

def evaluate_home_fragrance_scope(title: str, product_type: Optional[str] = None) -> Tuple[bool, Optional[str]]:
    """
    Evaluates whether a product falls within the Home Fragrance scope.
    Excludes explicitly car-only products, insecticides/cleaners, or un-related cosmetics.
    Returns (is_in_scope, rejection_reason).
    """
    text = f"{title} {product_type or ''}".lower()

    # Check for unrelated household cleaners / pest control / personal care
    unrelated_terms = [
        "mosquito", "repellent", "cockroach", "insecticide", "toilet cleaner",
        "floor cleaner", "hand wash", "sanitizer", "shampoo", "body wash",
        "agarbatti stand", "incense burner only"
    ]
    for term in unrelated_terms:
        if term in text:
            return False, f"unrelated_product_{term.replace(' ', '_')}"

    # Check for car-only products
    is_car_mention = any(k in text for k in CAR_EXCLUSION_KEYWORDS)
    is_home_mention = any(k in text for k in HOME_OVERRIDE_KEYWORDS)

    if is_car_mention and not is_home_mention:
        return False, "out_of_scope_car_only"

    return True, None

def classify_category_and_format(title: str, product_type_raw: Optional[str] = None) -> Tuple[str, str]:
    """
    Assigns a standardized category and product_format based on observed text.
    Categories:
      - Room Spray & Aerosol
      - Bathroom Freshener & Block
      - Automatic Spray & Refill
      - Reed Diffuser & Fragrance Oil
      - Scented Candle & Wax
      - Freshener Gel & Pocket
      - Ambient Fragrance (General)
    """
    text = f"{title} {product_type_raw or ''}".lower()

    if "automatic" in text or "matic" in text or "refill" in text:
        return "Automatic Spray & Refill", "Automatic Refill / Device"
    elif "candle" in text or "wax" in text:
        return "Scented Candle & Wax", "Scented Candle"
    elif "diffuser" in text or "fragrance oil" in text or "essential oil" in text or "reed" in text:
        return "Reed Diffuser & Fragrance Oil", "Diffuser / Aroma Oil"
    elif "block" in text or "pocket" in text or "bathroom" in text or "toilet" in text:
        return "Bathroom Freshener & Block", "Block / Pocket Freshener"
    elif "gel" in text:
        return "Freshener Gel & Pocket", "Fragrance Gel"
    elif "spray" in text or "air effects" in text or "aerosol" in text or "linen" in text or "mist" in text:
        return "Room Spray & Aerosol", "Room Spray"
    else:
        return "Ambient Fragrance (General)", "Ambient Freshener"
