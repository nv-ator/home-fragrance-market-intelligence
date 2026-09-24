import re
from typing import Optional, Dict, Any, Tuple

def parse_pack_quantity(title: str, pack_size_raw: Optional[str] = None) -> Dict[str, Any]:
    """
    Extracts pack count, unit quantity, normalized unit (ml, g, count), and total quantity.
    Never converts between mass (g) and volume (ml).
    """
    text = f"{pack_size_raw or ''} {title}".lower()

    pack_count = 1
    unit_qty = None
    unit = None
    total_qty = None

    # 1. Check for pack multiplier patterns, e.g. "pack of 3", "pack of 4", "3 x 75g", "3x75 g"
    pack_match = re.search(r"(?:pack\s+of\s+|combo\s+of\s+|set\s+of\s+)(\d+)", text)
    if pack_match:
        pack_count = int(pack_match.group(1))

    # Pattern like "3 x 75g" or "3x75 ml"
    multi_match = re.search(r"(\d+)\s*[xX*]\s*(\d+(?:\.\d+)?)\s*(ml|l|ltr|litres|g|gm|gms|grams|kg)\b", text)
    if multi_match:
        pack_count = int(multi_match.group(1))
        unit_qty = float(multi_match.group(2))
        raw_u = multi_match.group(3)
        unit = "ml" if raw_u in ["ml", "l", "ltr", "litres"] else "g"
        if raw_u in ["l", "ltr", "litres"]:
            unit_qty *= 1000
        elif raw_u == "kg":
            unit_qty *= 1000
        total_qty = round(pack_count * unit_qty, 2)
        return {
            "pack_count": pack_count,
            "unit_quantity": unit_qty,
            "unit": unit,
            "total_quantity": total_qty
        }

    # 2. Check for single quantity patterns, e.g. "275 ml", "100ml", "50g", "10 g", "1 litre", "1.2 kg"
    qty_match = re.search(r"(\d+(?:\.\d+)?)\s*(ml|l|ltr|litres|g|gm|gms|grams|kg)\b", text)
    if qty_match:
        raw_qty = float(qty_match.group(1))
        raw_u = qty_match.group(2)
        if raw_u in ["l", "ltr", "litres"]:
            unit = "ml"
            raw_qty *= 1000
        elif raw_u == "kg":
            unit = "g"
            raw_qty *= 1000
        elif raw_u in ["ml"]:
            unit = "ml"
        else:
            unit = "g"

        unit_qty = raw_qty
        total_qty = round(pack_count * unit_qty, 2)
        return {
            "pack_count": pack_count,
            "unit_quantity": unit_qty,
            "unit": unit,
            "total_quantity": total_qty
        }

    # 3. Check for unit/count items (e.g. "Pack of 3", "Pack of 2", "3 units")
    if pack_count > 1 or re.search(r"\b(\d+)\s*(?:units?|pieces?|pcs?|n)\b", text):
        unit_match = re.search(r"\b(\d+)\s*(?:units?|pieces?|pcs?|n)\b", text)
        if unit_match:
            pack_count = int(unit_match.group(1))
        return {
            "pack_count": pack_count,
            "unit_quantity": 1.0,
            "unit": "count",
            "total_quantity": float(pack_count)
        }

    return {
        "pack_count": 1,
        "unit_quantity": None,
        "unit": None,
        "total_quantity": None
    }

def calculate_normalized_prices(selling_price: Optional[float], quantity_info: Dict[str, Any]) -> Dict[str, Optional[float]]:
    """
    Computes price_per_unit, price_per_100g, or price_per_100ml strictly by unit type.
    Never converts mass to volume or vice versa.
    """
    res = {
        "price_per_unit": None,
        "price_per_100g": None,
        "price_per_100ml": None
    }
    if not selling_price or selling_price <= 0:
        return res

    unit = quantity_info.get("unit")
    total_qty = quantity_info.get("total_quantity")
    pack_count = quantity_info.get("pack_count", 1)

    if not total_qty or total_qty <= 0:
        if pack_count and pack_count > 0:
            res["price_per_unit"] = round(selling_price / pack_count, 2)
        return res

    if unit == "count":
        res["price_per_unit"] = round(selling_price / total_qty, 2)
    elif unit == "g":
        # Price per 100 grams
        res["price_per_100g"] = round((selling_price / total_qty) * 100.0, 2)
        res["price_per_unit"] = round(selling_price / pack_count, 2) if pack_count else None
    elif unit == "ml":
        # Price per 100 milliliters
        res["price_per_100ml"] = round((selling_price / total_qty) * 100.0, 2)
        res["price_per_unit"] = round(selling_price / pack_count, 2) if pack_count else None

    return res
