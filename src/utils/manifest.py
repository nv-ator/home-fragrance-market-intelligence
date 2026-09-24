import os
import json
import time
from datetime import datetime, timezone
from typing import Dict, Any, List
from src.utils.logger import setup_logger

logger = setup_logger("manifest_manager")

class ManifestManager:
    """Manages collection run manifests for auditability and provenance."""

    def __init__(self, raw_base_dir: str = "data/raw"):
        self.manifest_dir = os.path.join(raw_base_dir, "manifests")
        os.makedirs(self.manifest_dir, exist_ok=True)

    def create_run_id(self) -> str:
        return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

    def save_manifest(self, run_id: str, results: List[Dict[str, Any]]) -> str:
        timestamp = datetime.now(timezone.utc).isoformat()
        manifest_path = os.path.join(self.manifest_dir, f"collection_{run_id}.json")

        total_candidates = sum(r.get("candidates_count", 0) for r in results)
        brand_summaries = []
        for r in results:
            brand_summaries.append({
                "brand": r.get("brand"),
                "source": r.get("source"),
                "candidates_count": r.get("candidates_count", 0),
                "http_status": r.get("http_status"),
                "response_size_bytes": r.get("response_size", 0),
                "elapsed_time_sec": round(r.get("elapsed_time_sec", 0), 2),
                "errors": r.get("errors", [])
            })

        manifest = {
            "run_id": run_id,
            "created_at": timestamp,
            "total_candidates": total_candidates,
            "brands_attempted": len(results),
            "brands": brand_summaries
        }

        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

        logger.info(f"Manifest written successfully to {manifest_path} (Total candidates: {total_candidates})")
        return manifest_path
