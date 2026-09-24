import os
import json
from typing import List, Dict, Any
from src.utils.logger import setup_logger

logger = setup_logger("raw_storage")

def save_raw_candidates(candidates: List[Dict[str, Any]], output_filepath: str):
    """Saves candidate records to JSON Lines or JSON file in data/raw."""
    os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
    with open(output_filepath, "w", encoding="utf-8") as f:
        json.dump(candidates, f, indent=2, ensure_ascii=False)
    logger.info(f"Saved {len(candidates)} raw candidate records to {output_filepath}")
