import re
import html
from typing import Tuple, Optional, Dict, Any

def clean_text(text: Optional[str]) -> Optional[str]:
    """Decodes HTML entities, strips extraneous unicode artifacts, and standardizes spacing."""
    if not text:
        return None
    # Unescape HTML entities (e.g. &amp;, &#39;)
    t = html.unescape(text)
    # Remove surrogate characters and weird replacement chars
    t = t.replace("\ufffd", "").replace("", "")
    # Normalize multiple whitespace
    t = re.sub(r"\s+", " ", t).strip()
    return t if t else None

def parse_price(price_raw: Optional[Any]) -> Optional[float]:
    """Converts price strings like '₹ 199.00' or '199' to numeric float in INR."""
    if price_raw is None:
        return None
    p_str = str(price_raw).strip()
    if not p_str:
        return None
    # Remove currency symbol, comma, spaces
    cleaned = re.sub(r"[^\d.]", "", p_str)
    if not cleaned:
        return None
    try:
        val = float(cleaned)
        return round(val, 2)
    except ValueError:
        return None

def calculate_discount(selling_price: Optional[float], mrp: Optional[float], discount_raw: Optional[Any] = None) -> Tuple[Optional[float], str]:
    """Calculates discount percentage and returns (discount_pct, discount_source)."""
    # Check if raw discount was provided
    if discount_raw is not None:
        raw_val = parse_price(discount_raw)
        if raw_val is not None and 0.0 <= raw_val <= 100.0:
            return round(raw_val, 2), "source"

    # Compute from selling price and MRP if available
    if mrp is not None and selling_price is not None and mrp > 0 and mrp >= selling_price:
        pct = ((mrp - selling_price) / mrp) * 100.0
        return round(pct, 2), "calculated"

    return None, "unavailable"

def parse_rating(rating_raw: Optional[Any]) -> Optional[float]:
    """Validates and parses rating between 0.0 and 5.0."""
    if rating_raw is None:
        return None
    m = re.search(r"(\d+(\.\d+)?)", str(rating_raw))
    if m:
        try:
            val = float(m.group(1))
            if 0.0 <= val <= 5.0:
                return round(val, 1)
        except ValueError:
            pass
    return None

def parse_review_count(review_raw: Optional[Any]) -> Optional[int]:
    """Normalizes review count to integer, handling thousands separators or 'K' multipliers."""
    if review_raw is None:
        return None
    r_str = str(review_raw).strip().lower().replace(",", "")
    # Check for '8.5k'
    m_k = re.search(r"(\d+(\.\d+)?)\s*k", r_str)
    if m_k:
        try:
            return int(float(m_k.group(1)) * 1000)
        except ValueError:
            pass
    m = re.search(r"\d+", r_str)
    if m:
        try:
            return int(m.group(0))
        except ValueError:
            pass
    return None
